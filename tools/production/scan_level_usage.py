"""Count how many times each shape is instanced in a level (read-only scan of the game zip).

    python tools/production/scan_level_usage.py --shapes sign_stop sign_yield ... --out usage.json

Looks at every `"shapeName"` in the level's *.json (TSStatic, prefabs) and at forest item data.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import zipfile
from pathlib import Path

GAME = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive")
LEVEL_ZIP = GAME / "content/levels/west_coast_usa.zip"


def scan(shapes: list[str], zip_path: Path = LEVEL_ZIP) -> dict:
    wanted = {s.lower() for s in shapes}
    count = collections.Counter()
    where = collections.defaultdict(set)
    forest_types = {}
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        for n in names:
            if not n.endswith(".json"):
                continue
            text = zf.read(n).decode("utf8", "replace")
            for m in re.finditer(r'"(?:shapeName|shapeFile)"\s*:\s*"([^"]+)"', text):
                stem = m.group(1).rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
                if stem in wanted:
                    if "ForestItemData" in text[max(0, m.start() - 400):m.start()]:
                        forest_types[stem] = True
                        continue
                    count[stem] += 1
                    where[stem].add(n)
    return {s: {"instances": count[s.lower()], "files": sorted(where[s.lower()]),
                "forest_item": bool(forest_types.get(s.lower()))} for s in shapes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shapes", nargs="+", required=True)
    ap.add_argument("--zip", default=str(LEVEL_ZIP))
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    res = scan(a.shapes, Path(a.zip))
    text = json.dumps(res, indent=1)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf8")
    for k, v in res.items():
        print(f"{k:28s} {v['instances']:4d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
