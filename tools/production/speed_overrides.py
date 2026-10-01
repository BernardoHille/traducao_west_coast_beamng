"""Apply the functional speed-limit decisions as minimal mod overrides of the West Coast level files.

Input : working/speed/speed_changes.json   (one record per DecalRoad: persistentId, file, from, to, reason)
Output: mod/traducao_ptbr_wcusa/levels/west_coast_usa/main/MissionGroup/<group>/items.level.json
        mod/traducao_ptbr_wcusa/levels/west_coast_usa/slotTraffic.json
        tests/reports/phase5_speed_diff.json (+ printed summary)

Rules (docs/production/slotTraffic_update.md):
- level files are one JSON object per line: only the target lines change, and only the "speedLimit"
  field (replaced, or inserted in alphabetical key position); every other byte is copied from the game zip;
- every edited line is re-parsed and compared with the original object: only speedLimit may differ;
- slotTraffic.json is derived from the navgraph: its lanes are matched to the edited DecalRoads by
  geometry (lane centerline samples within MATCH_M of the road polyline, >= 90 % of samples) and only
  the "speedLimit" lines of those lanes (roads.*.properties and nodes.*.links.*) are rewritten, keeping
  the file's formatting. Lanes are only touched if their current value equals the road's old effective
  value (explicit value, or the auto value read from the navgraph snapshot).

    python tools/production/speed_overrides.py            # build overrides + diff report
    python tools/production/speed_overrides.py --check    # verify the mod files against the zip
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
GAME_ZIP = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/west_coast_usa.zip")
CHANGES = REPO / "working/speed/speed_changes.json"
INSTANCES = REPO / "working/speed/sign_instances.json"
MOD_LEVEL = REPO / "mod/traducao_ptbr_wcusa/levels/west_coast_usa"
REPORT = REPO / "tests/reports/phase5_speed_diff.json"
LEVEL_PREFIX = "levels/west_coast_usa/main/MissionGroup/"
SLOT = "levels/west_coast_usa/slotTraffic.json"
MATCH_M = 1.6
TOL = 1e-3
TOL_AUTO = 2e-3  # navgraph auto values are read with 4 decimals


# ---------------------------------------------------------------- level files
def edit_line(line: str, pid: str, old, new: str) -> str:
    obj = json.loads(line)
    if obj.get("persistentId") != pid or obj.get("class") != "DecalRoad":
        raise SystemExit(f"{pid}: line is not that DecalRoad")
    cur = obj.get("speedLimit")
    if (cur is None and old is not None) or (cur is not None and old is None) or (cur is not None and float(cur) != float(old)):
        raise SystemExit(f"{pid}: expected speedLimit {old!r}, found {cur!r}")
    if cur is not None:
        new_line, n = re.subn(r'"speedLimit":"[^"]*"', f'"speedLimit":"{new}"', line)
        if n != 1:
            raise SystemExit(f"{pid}: speedLimit not found exactly once")
    else:
        # insert keeping the serializer's order: keys after "position" are alphabetical
        keys = list(obj.keys())
        tail = keys[keys.index("position") + 1:] if "position" in keys else keys
        after = [k for k in tail if k > "speedLimit"]
        if after:
            anchor = f',"{after[0]}":'
            i = line.index(anchor)
            new_line = line[:i] + f',"speedLimit":"{new}"' + line[i:]
        else:
            new_line = line[:line.rindex("}")] + f',"speedLimit":"{new}"' + line[line.rindex("}"):]
    a, b = json.loads(line), json.loads(new_line)
    a.pop("speedLimit", None)
    b2 = dict(b)
    b2.pop("speedLimit")
    if a != b2 or b["speedLimit"] != new:
        raise SystemExit(f"{pid}: edit changed more than speedLimit")
    return new_line


def edit_shape(line: str, pid: str, old: str, new: str) -> str:
    obj = json.loads(line)
    if obj.get("persistentId") != pid or obj.get("class") != "TSStatic" or obj.get("shapeName") != old:
        raise SystemExit(f"{pid}: not the TSStatic with shapeName {old}")
    new_line = line.replace(f'"shapeName":"{old}"', f'"shapeName":"{new}"')
    a, b = json.loads(line), json.loads(new_line)
    a.pop("shapeName"), b.pop("shapeName")
    if a != b or json.loads(new_line)["shapeName"] != new:
        raise SystemExit(f"{pid}: shape edit changed more than shapeName")
    return new_line


def load_instances():
    return json.loads(INSTANCES.read_text(encoding="utf8"))["instances"] if INSTANCES.exists() else []


def build_level_files(changes, zf):
    by_file = {}
    for c in changes:
        by_file.setdefault(c["file"], []).append(c)
    for inst in load_instances():
        by_file.setdefault(inst["file"], []).append(dict(inst, kind="shape"))
    # stale overrides from earlier decisions are removed (only files this tool generates live here)
    root = MOD_LEVEL / "main/MissionGroup"
    if root.exists():
        for f in root.rglob("items.level.json"):
            if f.relative_to(root).as_posix() not in by_file:
                f.unlink()
    out = []
    for rel, items in sorted(by_file.items()):
        raw = zf.read(LEVEL_PREFIX + rel).decode("utf8")
        lines = raw.split("\n")
        idx = {}
        for i, l in enumerate(lines):
            m = re.search(r'"persistentId":"([0-9a-f-]+)"', l)
            if m:
                idx[m.group(1)] = i
        for c in items:
            i = idx[c["pid"]]
            if c.get("kind") == "shape":
                lines[i] = edit_shape(lines[i], c["pid"], c["from"], c["to"])
            else:
                lines[i] = edit_line(lines[i], c["pid"], c["from"], c["to"])
        dst = MOD_LEVEL / "main/MissionGroup" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes("\n".join(lines).encode("utf8"))
        out.append({"file": rel, "edited_objects": len(items), "lines_total": len(lines)})
    return out


# ---------------------------------------------------------------- slotTraffic
def walk_speed_lines(lines):
    """Yield (line_no, kind, owner_id, value) for every speedLimit leaf: kind = 'road' (roads.<id>.properties)
    or 'link' (nodes.<n>.links.<m>, owner = its roadId)."""
    stack, link_road = [], None
    key_open = re.compile(r'\s*"([^"]+)":\s*([\{\[])\s*$')
    leaf = re.compile(r'\s*"([^"]+)":\s*(.*?),?\s*$')
    for i, l in enumerate(lines):
        s = l.strip()
        m = key_open.match(l)
        if m:
            stack.append(m.group(1))
            if len(stack) == 5 and stack[0] == "nodes" and stack[2] == "links":
                link_road = None
            continue
        if s in ("{", "["):
            if i == 0:
                continue          # root object
            stack.append("[]")
            continue
        if s in ("}", "},", "]", "],"):
            if stack:
                stack.pop()
            continue
        m = leaf.match(l)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        if k == "roadId" and len(stack) == 4 and stack[0] == "nodes" and stack[2] == "links":
            link_road = json.loads(v)
        if k == "speedLimit":
            if len(stack) == 3 and stack[0] == "roads" and stack[2] == "properties":
                yield i, "road", stack[1], float(v)
            elif len(stack) == 4 and stack[0] == "nodes" and stack[2] == "links":
                yield i, "link", link_road, float(v)


def polyline_dist(points, poly):
    d = np.full(len(points), np.inf)
    for a, b in zip(poly[:-1], poly[1:]):
        ab = b - a
        t = np.clip(((points - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
        q = a + t[:, None] * ab
        d = np.minimum(d, np.linalg.norm(points - q, axis=1))
    return d


def match_lanes(slot, roads):
    """DecalRoad pid -> [slot road ids] (geometric match of lane centerlines, XY)."""
    cls = []
    for rid, cl in slot["centerlines"].items():
        pts = np.array([[p["x"], p["y"]] for p in cl.get("samples") or cl["points"]])
        cls.append((rid, pts, pts.min(0), pts.max(0)))
    res = {}
    for pid, poly in roads.items():
        lo, hi = poly.min(0) - MATCH_M, poly.max(0) + MATCH_M
        hits = []
        for rid, pts, a, b in cls:
            if (a > hi).any() or (b < lo).any():
                continue
            d = polyline_dist(pts, poly)
            # lanes are offset from the road axis by up to ~half the road width
            if (d < MATCH_M + roads_width.get(pid, 0) / 2).mean() >= 0.9:
                hits.append(rid)
        res[pid] = hits
    return res


roads_width = {}


def build_slot(changes, zf, report):
    raw = zf.read(SLOT).decode("utf8")
    slot = json.loads(raw)
    lines = raw.split("\n")
    level = {}
    for c in changes:
        for l in zf.read(LEVEL_PREFIX + c["file"]).decode("utf8").split("\n"):
            if c["pid"] in l:
                o = json.loads(l)
                level[c["pid"]] = np.array([[n[0], n[1]] for n in o["nodes"]])
                roads_width[c["pid"]] = float(np.median([n[3] for n in o["nodes"]]))
                break
    lanes = match_lanes(slot, level)
    want = {}
    for c in changes:
        old_eff = float(c["from"]) if c["from"] is not None else c["old_effective_mps"]
        for rid in lanes.get(c["pid"], []):
            want[rid] = (old_eff, float(c["to"]), c["pid"])
    # Explicit mph-derived values (11.18 / 11.5 / 12 m/s) never come from the automatic metric list
    # (30/50/60/80/100/120 km/h), and EVERY navgraph road holding one of them is converted in this
    # phase, so in the derived file the value itself identifies the source: exact value replacement.
    explicit = {}
    for c in changes:
        if c["from"] is not None and c.get("category", "").startswith("40_explicit"):
            explicit[float(c["from"])] = float(c["to"])
    navgraph_explicit = {float(o) for o in data_explicit_values(zf)}
    if not set(explicit) >= (navgraph_explicit & {11.18, 11.5, 12.0}):
        raise SystemExit("value-class replacement requires converting every road of the class")
    edits, skipped, geo_hits = [], [], 0
    for i, kind, owner, val in walk_speed_lines(lines):
        if any(abs(val - k) <= TOL for k in explicit):
            new = next(v for k, v in explicit.items() if abs(val - k) <= TOL)
            in_geo = owner in want
            geo_hits += in_geo
            lines[i] = re.sub(r'("speedLimit":\s*)[-0-9.eE+]+', lambda m: m.group(1) + c_num(new), lines[i])
            edits.append({"line": i + 1, "kind": kind, "lane": owner, "old": val, "new": float(c_num(new)),
                          "rule": "value_class", "geometry_match": in_geo})
            continue
        if owner not in want:
            continue
        old_eff, new, pid = want[owner]
        if abs(val - old_eff) > TOL_AUTO:
            skipped.append({"line": i + 1, "kind": kind, "lane": owner, "value": val, "expected_old": old_eff, "road": pid})
            continue
        lines[i] = re.sub(r'("speedLimit":\s*)[-0-9.eE+]+', lambda m: m.group(1) + c_num(new), lines[i])
        edits.append({"line": i + 1, "kind": kind, "lane": owner, "old": val, "new": float(c_num(new)), "road": pid,
                      "rule": "geometry"})
    dst = MOD_LEVEL / "slotTraffic.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes("\n".join(lines).encode("utf8"))
    json.loads(dst.read_text(encoding="utf8"))  # still valid JSON
    report["slotTraffic"] = {
        "matched_lanes": {pid: v for pid, v in lanes.items()},
        "unmatched_roads": [pid for pid, v in lanes.items() if not v],
        "edited_lines": len(edits), "edited_road_properties": sum(e["kind"] == "road" for e in edits),
        "edited_links": sum(e["kind"] == "link" for e in edits), "value_class_lines_also_matched_by_geometry": geo_hits,
        "skipped_value_mismatch": skipped, "edits": edits}


def data_explicit_values(zf):
    vals = set()
    for n in zf.namelist():
        if n.startswith(LEVEL_PREFIX) and n.endswith("items.level.json"):
            for l in zf.read(n).decode("utf8", "replace").splitlines():
                if '"class":"DecalRoad"' in l and '"speedLimit"' in l:
                    vals.add(json.loads(l)["speedLimit"])
    return vals


def c_num(v: float) -> str:
    """Same style as the file (Lua %.14g)."""
    return f"{v:.14g}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only verify existing overrides against the zip")
    a = ap.parse_args(argv)
    data = json.loads(CHANGES.read_text(encoding="utf8"))
    changes = data["changes"]
    zf = zipfile.ZipFile(GAME_ZIP)
    report = {"changes": len(changes), "by_target": {}}
    for c in changes:
        report["by_target"][c["to"]] = report["by_target"].get(c["to"], 0) + 1
    if not a.check:
        report["level_files"] = build_level_files(changes, zf)
        build_slot(changes, zf, report)
    report["verification"] = verify(changes, zf)
    if not a.check:
        write_sign_regulation(changes, zf)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=1) + "\n", encoding="utf8")
    s = report.get("slotTraffic", {})
    print(json.dumps({k: report[k] for k in ("changes", "by_target")}, indent=1))
    for f in report.get("level_files", []):
        print(f"  {f['file']}: {f['edited_objects']} objects edited")
    if s:
        print(f"  slotTraffic.json: {s['edited_lines']} lines ({s['edited_road_properties']} lanes, {s['edited_links']} links), "
              f"unmatched roads {len(s['unmatched_roads'])}, skipped {len(s['skipped_value_mismatch'])}")
    v = report["verification"]
    print(f"verification: {'OK' if v['ok'] else 'FAIL'} {v['summary']}")
    return 0 if v["ok"] else 1


SIGN_REG = REPO / "tools/validation/config/sign_regulation.json"


def write_sign_regulation(changes, zf):
    """Config for validate.py speeds: each speed sign -> roads it regulates (declared, reviewed decision)."""
    signs = []
    shape_of = {i["pid"]: i["to"] for i in load_instances()}
    for n in zf.namelist():
        if not (n.startswith(LEVEL_PREFIX) and n.endswith("items.level.json")):
            continue
        for l in zf.read(n).decode("utf8", "replace").splitlines():
            if '"shapeName":' not in l or "sign_speed" not in l:
                continue
            o = json.loads(l)
            if o.get("class") != "TSStatic" or not re.search(r"/sign_speed\d+\.dae$", o.get("shapeName", "")):
                continue
            if o.get("decalType"):
                continue  # mesh decal (port bay-number plates), not a speed sign
            shape = shape_of.get(o["persistentId"], o["shapeName"])
            signs.append({"shape": shape.rsplit("/", 1)[-1].rsplit(".", 1)[0], "persistentId": o["persistentId"],
                          "position": [round(v, 2) for v in o["position"]], "group": n[len(LEVEL_PREFIX):].rsplit("/", 1)[0]})
    for sg in signs:
        regs = []
        for c in changes:
            for sp in c.get("signs", []):
                if abs(sp[0] - sg["position"][0]) < 1.0 and abs(sp[1] - sg["position"][1]) < 1.0:
                    regs.append({"persistentId": c["pid"], "file": c["file"], "to_mps": float(c["to"]), "category": c["category"]})
        sg["regulated_roads"] = regs
    out = {"_doc": "Generated by tools/production/speed_overrides.py from working/speed/speed_changes.json. Each West Coast "
                   "speed sign with the DecalRoads it regulates (semantic + spatial decision, docs/production/PHASE5_ROADSIGNS.md). "
                   "validate.py speeds checks sign value == explicit limit of every regulated road.",
           "signs": signs}
    SIGN_REG.write_text(json.dumps(out, indent=1) + "\n", encoding="utf8")


def verify(changes, zf):
    """Every mod level file differs from the zip only in the speedLimit of the declared objects."""
    want = {(c["file"], c["pid"]): c["to"] for c in changes}
    shapes = {(i["file"], i["pid"]): i["to"] for i in load_instances()}
    problems, n_diff = [], 0
    for dst in sorted((MOD_LEVEL / "main/MissionGroup").rglob("items.level.json")):
        rel = dst.relative_to(MOD_LEVEL / "main/MissionGroup").as_posix()
        a = zf.read(LEVEL_PREFIX + rel).decode("utf8").split("\n")
        b = dst.read_text(encoding="utf8").split("\n")
        if len(a) != len(b):
            problems.append(f"{rel}: line count {len(a)} -> {len(b)}")
            continue
        for x, y in zip(a, b):
            if x == y:
                continue
            n_diff += 1
            ox, oy = json.loads(x), json.loads(y)
            pid = oy.get("persistentId")
            if (rel, pid) in shapes:
                ox.pop("shapeName", None)
                if oy.pop("shapeName") != shapes[(rel, pid)] or ox != oy:
                    problems.append(f"{rel}: {pid} changed beyond shapeName")
                continue
            if (rel, pid) not in want:
                problems.append(f"{rel}: undeclared change in {pid}")
                continue
            ox.pop("speedLimit", None)
            if oy.pop("speedLimit") != want[(rel, pid)] or ox != oy:
                problems.append(f"{rel}: {pid} changed beyond speedLimit")
    declared = len(want) + len(shapes)
    return {"ok": not problems and n_diff == declared, "summary": f"{n_diff} changed lines / {declared} declared",
            "problems": problems}


if __name__ == "__main__":
    sys.exit(main())
