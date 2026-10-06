"""Override of levels/west_coast_usa/main.decals.json for the pavement phrases (Phase 6, 6A).

Reads the game's file (read-only), applies only the decisions of
working/layered/t_decal_roadmarkings/decal_overrides.json (instances identified by uid, never by
position alone) and writes mod/traducao_ptbr_wcusa/levels/west_coast_usa/main.decals.json.

Edits are line-based: the file keeps the game's formatting byte for byte except the touched instances.
Like the Phase 5 level overrides, the output is a copy of game data -> generated locally, not versioned.

    python tools/production/decal_overrides.py          # write + verify
    python tools/production/decal_overrides.py --check  # verify the file in the mod
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEVEL_ZIP = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/west_coast_usa.zip")
INNER = "levels/west_coast_usa/main.decals.json"
DECISIONS = REPO / "working/layered/t_decal_roadmarkings/decal_overrides.json"
OUT = REPO / "mod/traducao_ptbr_wcusa" / INNER


def game_text() -> str:
    return zipfile.ZipFile(LEVEL_ZIP).read(INNER).decode("utf8")


def blocks(lines, set_name):
    """(start, end) line spans of every instance array of `set_name` (end exclusive)."""
    start = next(i for i, l in enumerate(lines) if l.strip() == f'"{set_name}": [')
    out, i = [], start + 1
    while lines[i].strip() in ("[",):
        j = i + 1
        while not lines[j].strip().startswith("]"):
            j += 1
        out.append((i, j + 1))
        i = j + 1
    return start, out


def values(lines, span):
    return [json.loads(l.strip().rstrip(",")) for l in lines[span[0] + 1:span[1] - 1]]


def apply(text: str, dec: dict) -> str:
    lines = text.split("\n")
    _, spans = blocks(lines, dec["decal_set"])
    by_idx = {}
    for i, sp in enumerate(spans):
        by_idx[i] = (sp, values(lines, sp))
    delete, change = set(), {}
    for d in dec["delete"]:
        sp, v = by_idx[d["index"]]
        if v[12] != d["uid"] or v[0] != d["rectIdx"]:
            raise SystemExit(f"instance {d['index']}: uid/rectIdx mismatch - the game file changed, stop")
        delete.add(d["index"])
    for c in dec["set_rectIdx"]:
        sp, v = by_idx[c["index"]]
        if v[12] != c["uid"] or v[0] != c["from"]:
            raise SystemExit(f"instance {c['index']}: uid/rectIdx mismatch - the game file changed, stop")
        change[c["index"]] = c["to"]
    if max(delete, default=-1) == len(spans) - 1:
        raise SystemExit("refusing to delete the last instance (trailing comma handling)")
    out = []
    cursor = 0
    for idx, (sp, v) in sorted(by_idx.items()):
        out.extend(lines[cursor:sp[0]])
        block = lines[sp[0]:sp[1]]
        if idx in delete:
            pass
        elif idx in change:
            first = block[1]
            indent = first[: len(first) - len(first.lstrip())]
            block = block[:1] + [f"{indent}{change[idx]},"] + block[2:]
            out.extend(block)
        else:
            out.extend(block)
        cursor = sp[1]
    out.extend(lines[cursor:])
    return "\n".join(out)


def verify(new_text: str, dec: dict) -> list[str]:
    old, new = json.loads(game_text()), json.loads(new_text)
    errs = []
    for k in old:
        if k != "instances" and old[k] != new.get(k):
            errs.append(f"top-level {k} changed")
    for name, inst in old["instances"].items():
        if name != dec["decal_set"]:
            if inst != new["instances"].get(name):
                errs.append(f"decal set {name} changed")
            continue
        dels = {d["uid"] for d in dec["delete"]}
        chg = {c["uid"]: c["to"] for c in dec["set_rectIdx"]}
        expect = []
        for v in inst:
            if v[12] in dels:
                continue
            v = list(v)
            if v[12] in chg:
                v[0] = chg[v[12]]
            expect.append(v)
        if expect != new["instances"][name]:
            errs.append(f"{name}: result differs from the declared decisions")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    dec = json.loads(DECISIONS.read_text(encoding="utf8"))
    if not a.check:
        text = apply(game_text(), dec)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(text.encode("utf8"))
    errs = verify(OUT.read_text(encoding="utf8"), dec)
    n_lines = sum(1 for x, y in zip(game_text().split("\n"), OUT.read_text(encoding="utf8").split("\n")) if x != y)
    print(f"{OUT.relative_to(REPO)}: {len(dec['delete'])} deleted, {len(dec['set_rectIdx'])} rectIdx changed; "
          f"{'OK' if not errs else 'FAIL ' + '; '.join(errs)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
