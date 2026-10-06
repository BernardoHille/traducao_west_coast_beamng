"""Read-only map of how the game uses a texture: texture -> materials -> meshes -> West Coast instances.

Scans the game zips (never writes to them):
  * every *.materials.json  -> materials whose Stages reference the texture (matched by file stem,
    because legacy paths such as /art/shapes/objects/x.png are resolved by name by the engine);
  * every .dae               -> meshes whose COLLADA material list contains one of those materials;
  * the West Coast level      -> TSStatic/prefab instances (shapeName) and forest items of each mesh.

    python tools/production/asset_usage.py t_billboards_b.color eca_genericsigns_d --out usage.json
    python tools/production/asset_usage.py --extract-meshes source/originals/meshes  <texture...>

The index of the zips is cached in working/temporary/asset_index.json (regenerated when a zip changes).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GAME = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive")
CONTENT = GAME / "content"
LEVEL_ZIP = CONTENT / "levels/west_coast_usa.zip"
CACHE = REPO / "working/temporary/asset_index.json"


def game_zips() -> list[Path]:
    zs = [LEVEL_ZIP, CONTENT / "art_shapes.zip", CONTENT / "assets/meshes.zip"]
    zs += sorted((CONTENT / "assets/materials").glob("*.zip"))
    zs += [CONTENT / "levels/east_coast_usa.zip", CONTENT / "levels/utah.zip"]
    return [z for z in zs if z.exists()]


def stem(path: str) -> str:
    name = path.replace("\\", "/").rsplit("/", 1)[-1]
    for ext in (".dds", ".png", ".jpg", ".DDS", ".PNG"):
        if name.endswith(ext):
            name = name[: -len(ext)]
    return name.lower()


def _maps_of(mat: dict) -> set[str]:
    out = set()
    for st in mat.get("Stages", []) or []:
        if isinstance(st, dict):
            for k, v in st.items():
                if isinstance(v, str) and k.lower().endswith("map"):
                    out.add(stem(v))
    for k, v in mat.items():
        if isinstance(v, str) and k.lower().endswith("map"):
            out.add(stem(v))
    return out


def build_index() -> dict:
    sig = {str(z): z.stat().st_mtime for z in game_zips()}
    if CACHE.exists():
        old = json.loads(CACHE.read_text(encoding="utf8"))
        if old.get("_sig") == sig:
            return old
    materials = collections.defaultdict(list)   # material -> [{zip, file, maps}]
    dae_mats = {}                               # "zip::path.dae" -> [material names]
    for z in game_zips():
        with zipfile.ZipFile(z) as zf:
            for n in zf.namelist():
                low = n.lower()
                if low.endswith("materials.json"):
                    try:
                        data = json.loads(zf.read(n).decode("utf8", "replace"))
                    except ValueError:
                        continue
                    for name, mat in data.items():
                        if isinstance(mat, dict) and mat.get("class") in ("Material", "CustomMaterial", None):
                            maps = _maps_of(mat)
                            if maps:
                                materials[mat.get("mapTo", name)].append({"zip": z.name, "file": n, "name": name, "maps": sorted(maps)})
                elif low.endswith(".dae"):
                    text = zf.read(n).decode("utf8", "replace")
                    names = set(re.findall(r'<material\s[^>]*?name="([^"]+)"', text))
                    names |= {m.removesuffix("-material") for m in re.findall(r'<material\s[^>]*?id="([^"]+)"', text)}
                    dae_mats[f"{z.name}::{n}"] = sorted(names)
    idx = {"_sig": sig, "materials": materials, "dae_materials": dae_mats}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(idx), encoding="utf8")
    return idx


def _prefab_placements(zf) -> dict:
    """prefab file (lower, no leading slash) -> number of Prefab objects placing it in the level."""
    cnt = collections.Counter()
    for n in zf.namelist():
        if not n.endswith(".json") or n.endswith(".prefab.json"):
            continue
        text = zf.read(n).decode("utf8", "replace")
        if '"Prefab"' not in text:
            continue
        for line in text.splitlines():
            if '"class":"Prefab"' in line.replace(" ", ""):
                m = re.search(r'"filename"\s*:\s*"([^"]+)"', line)
                if m:
                    cnt[m.group(1).replace("\\", "/").lstrip("/").lower()] += 1
    return cnt


def level_instances() -> dict:
    """mesh path (zip path, lower case) -> {'instances': n, 'objects': [{file, line, pos, rot, scale, decalType}]} in the West Coast."""
    out = collections.defaultdict(lambda: {"instances": 0, "objects": []})
    with zipfile.ZipFile(LEVEL_ZIP) as zf:
        placements = _prefab_placements(zf)
        for n in zf.namelist():
            if not n.endswith(".json"):
                continue
            text = zf.read(n).decode("utf8", "replace")
            if "shapeName" not in text:
                continue
            for i, line in enumerate(text.splitlines()):
                if '"shapeName"' not in line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    m = re.search(r'"shapeName"\s*:\s*"([^"]+)"', line)
                    obj = {"shapeName": m.group(1)} if m else None
                if not obj or obj.get("class") == "ForestItemData":
                    continue
                s = obj["shapeName"].replace("\\", "/").lstrip("/").lower()
                s = s[:-5] + ".dae" if s.endswith(".cdae") else s
                rec = out[s]
                mult = 1
                if n.endswith(".prefab.json"):  # placed by Prefab objects of the level
                    mult = placements.get(n.lower(), 0)
                    rec.setdefault("prefabs", {})[n] = mult
                rec["instances"] += mult
                if len(rec["objects"]) < 400:
                    rec["objects"].append({"file": n, "line": i, "class": obj.get("class"), "pos": obj.get("position"),
                                           "rot": obj.get("rotationMatrix"), "scale": obj.get("scale"),
                                           "decalType": obj.get("decalType"), "pid": obj.get("persistentId")})
    return out


def usage(textures: list[str]) -> dict:
    idx = build_index()
    inst = level_instances()
    res = {}
    for tex in textures:
        t = stem(tex)
        mats = {m: recs for m, recs in idx["materials"].items() if any(t == mp for r in recs for mp in r["maps"])}
        meshes = {}
        for key, names in idx["dae_materials"].items():
            hit = [m for m in names if m in mats]
            if hit:
                s = key.split("::", 1)[1].lower()
                meshes[key] = {"materials": hit, "wcusa_instances": inst.get(s, {}).get("instances", 0)}
        res[tex] = {"materials": {m: [f"{r['zip']}::{r['file']}" for r in recs] for m, recs in mats.items()},
                    "meshes": meshes,
                    "instanced_meshes": {k: v for k, v in meshes.items() if v["wcusa_instances"]}}
    return res


def extract(keys: list[str], dest: Path) -> list[Path]:
    """Copy (read-only from the zip) the given 'zip::path' meshes to dest/<zip stem>/<path>."""
    by_zip = collections.defaultdict(list)
    for k in keys:
        z, p = k.split("::", 1)
        by_zip[z].append(p)
    out = []
    for z in game_zips():
        if z.name not in by_zip:
            continue
        with zipfile.ZipFile(z) as zf:
            for p in by_zip[z.name]:
                t = dest / z.stem / p
                t.parent.mkdir(parents=True, exist_ok=True)
                if not t.exists():
                    t.write_bytes(zf.read(p))
                out.append(t)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("textures", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--extract-meshes", help="copy the instanced meshes to this folder (outside Git)")
    a = ap.parse_args(argv)
    res = usage(a.textures)
    for tex, r in res.items():
        print(f"== {tex}: materials {sorted(r['materials'])}")
        for k, v in sorted(r["instanced_meshes"].items(), key=lambda kv: -kv[1]["wcusa_instances"]):
            print(f"   {v['wcusa_instances']:5d}  {k}  {v['materials']}")
        print(f"   ({len(r['meshes'])} meshes reference the materials, {len(r['instanced_meshes'])} instanced in WCUSA)")
        if a.extract_meshes:
            extract(list(r["instanced_meshes"]), Path(a.extract_meshes))
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
