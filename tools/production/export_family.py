"""PNG -> DDS in the ORIGINAL format of each map, then copy into the mod at the declared virtual paths.

    python tools/production/export_family.py working/layered/<family>/export.json

export.json:
  {"family": "...", "items": [{"png": "working/png/x.png", "install": ["assets/materials/..."]}, ...]}

The DDS format, sRGB/linear flag, header type (legacy FourCC or DX10) and mip count are read from the
original DDS that the validator associates with the PNG (tools/validation/common.find_original, which
also picks original variants by folder). Output: export/dds/<family>/[<variant>/]<name>.dds and
mod/traducao_ptbr_wcusa/<install dir>/<name>.dds (exact original file name, never _ptbr).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/validation"))
import common  # noqa: E402
import dds_parser  # noqa: E402

TEXCONV = REPO / "tools/conversion/bin/texconv.exe"
MOD = REPO / "mod/traducao_ptbr_wcusa"


def convert(png: Path, out_dir: Path) -> tuple[Path, dict]:
    stem = common.texture_stem(str(png))
    orig, row = common.find_original(stem, "dds", hint_path=str(png))
    if not orig:
        raise SystemExit(f"{png}: no original DDS in the manifest")
    info = dds_parser.parse(orig)
    fmt = info["format"]
    args = [str(TEXCONV), "-nologo", "-y", "-o", str(out_dir), "-m", str(info["mip_count"]), "-f", fmt]
    if info["srgb"]:
        args += ["-srgb"]
    if info["dx10"]:
        args += ["-dx10"]
    out_dir.mkdir(parents=True, exist_ok=True)
    args.append(str(png))
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stdout + r.stderr)
    dds = out_dir / (png.stem + ".dds")
    return dds, {"original": common.rel(orig), "format": fmt, "srgb": info["srgb"], "dx10": info["dx10"], "mips": info["mip_count"]}


def main(argv=None) -> int:
    spec_path = Path((argv or sys.argv[1:])[0]).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf8"))
    fam = spec["family"]
    log = []
    for it in spec["items"]:
        png = REPO / it["png"]
        variant = png.parent.name if png.parent.name not in ("png",) else ""
        out_dir = REPO / "export/dds" / fam / variant
        dds, meta = convert(png, out_dir)
        targets = []
        for d in it.get("install", []):
            t = MOD / d / dds.name
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(dds, t)
            targets.append(common.rel(t))
        log.append({"png": it["png"], "dds": common.rel(dds), **meta, "installed": targets})
        print(f"{common.rel(dds)}  {meta['format']}{' sRGB' if meta['srgb'] else ''} mips={meta['mips']} -> {len(targets)} mod path(s)")
    (spec_path.parent / "export_log.json").write_text(json.dumps(log, indent=1) + "\n", encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
