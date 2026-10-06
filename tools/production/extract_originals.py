"""Extract game textures (read-only) into source/originals and register them in the manifest.

For every entry of tools/production/originals_phase6.json:
  * reads the DDS from the game zip (never writes to the game);
  * if source/originals/dds/<name>.dds already exists: checks that it is byte-identical to the game file
    (the file the mod will override) and reports;
  * otherwise writes it, decodes a PNG with texconv (same resolution, top mip, sRGB kept for colour maps)
    and appends original_dds + original_png rows to docs/inventory/original_files_manifest.csv.

    python tools/production/extract_originals.py            # extract + verify
    python tools/production/extract_originals.py --verify   # only compare local originals with the game
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/validation"))
import dds_parser  # noqa: E402

GAME = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content")
SPEC = Path(__file__).with_name("originals_phase6.json")
MANIFEST = REPO / "docs/inventory/original_files_manifest.csv"
DDS_DIR = REPO / "source/originals/dds"
PNG_DIR = REPO / "source/originals/png"
TEXCONV = REPO / "tools/conversion/bin/texconv.exe"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def decode_png(dds: Path, srgb: bool, sub: str = "") -> Path:
    fmt = "R8G8B8A8_UNORM_SRGB" if srgb else "R8G8B8A8_UNORM"
    out = PNG_DIR / sub
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(TEXCONV), "-nologo", "-ft", "png", "-f", fmt, "-m", "1", "-y", "-o", str(out), str(dds)],
                   check=True, capture_output=True)
    return out / (dds.stem + ".png")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args(argv)
    spec = json.loads(SPEC.read_text(encoding="utf8"))
    rows = list(csv.DictReader(open(MANIFEST, encoding="utf8")))
    fields = list(rows[0].keys())
    known = {r["filename"]: r for r in rows}
    new_rows, problems = [], []
    for e in spec["textures"]:
        zpath, inner = GAME / e["zip"], e["path"]
        data = zipfile.ZipFile(zpath).read(inner)
        name = Path(inner).name
        if name.lower().endswith(".dds") and not name.endswith(".dds"):
            name = name[:-4] + ".dds"
        sub = e.get("variant", "")
        local = DDS_DIR / sub / name
        if local.exists():
            same = sha(local.read_bytes()) == sha(data)
            status = "identical" if same else "DIFFERENT"
            if not same:
                problems.append(f"{name}: local original differs from {e['zip']}::{inner}")
            print(f"{status:10s} {name}  <- {e['zip']}::{inner}")
            continue
        if a.verify:
            print(f"{'missing':10s} {name}")
            continue
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(data)
        info = dds_parser.parse(str(local))
        srgb = bool(info.get("srgb"))
        png = decode_png(local, srgb, sub)
        pngb = png.read_bytes()
        from PIL import Image
        with Image.open(png) as im:
            w, h, mode = im.width, im.height, im.mode
        fmt = ("DX10 " if info.get("dx10") else "") + info["format"]
        common = {"category": e.get("category", ""), "texture_family": e["family"], "map_role": e["role"]}
        new_rows.append({**{k: "" for k in fields}, "relative_path": f"game/{e['zip']}/{inner}", "filename": name,
                         "extension": ".dds", "size_bytes": str(len(data)), "width": str(info["width"]),
                         "height": str(info["height"]), "file_format": f"DDS {fmt}", "sha256": sha(data),
                         "classification": "original_dds",
                         "notes": f"mipmaps={info.get('mip_count')}; Phase 6 extraction (read-only) from {e['zip']}::{inner}",
                         "copied_to": f"source/originals/dds/{sub + '/' if sub else ''}{name}", **common})
        new_rows.append({**{k: "" for k in fields}, "relative_path": f"game/{e['zip']}/{inner[:-4]}.png", "filename": png.name,
                         "extension": ".png", "size_bytes": str(len(pngb)), "width": str(w), "height": str(h),
                         "file_format": f"PNG {mode}", "sha256": sha(pngb), "classification": "original_png",
                         "notes": "PNG decoded from the original DDS with texconv (top mip, same resolution); editing base",
                         "copied_to": f"source/originals/png/{sub + '/' if sub else ''}{png.name}", **common})
        print(f"{'extracted':10s} {name}  {info['width']}x{info['height']} {fmt}")
    if new_rows:
        with open(MANIFEST, "a", encoding="utf8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            for r in new_rows:
                if r["copied_to"] not in {k["copied_to"] for k in rows}:
                    w.writerow(r)
        print(f"manifest: +{len(new_rows)} rows")
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
