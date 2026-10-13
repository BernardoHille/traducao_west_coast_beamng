"""Apply the functional speed-limit decisions as minimal mod overrides of the West Coast level files.

Input : working/speed/speed_changes.json   (Phase 5: one record per DecalRoad: persistentId, file, from, to, reason)
        working/functional/speed_changes.json, radar_changes.json   (Phase 7: same format plus "class": DecalRoad,
        BeamNGWaypoint or BeamNGTrigger); objects ADDED to the level (Phase 7 R-19 signs) are passed in by
        tools/production/apply_phase7_functional.py, which is the build entry point since Phase 7
Output: mod/traducao_ptbr_wcusa/levels/west_coast_usa/main/MissionGroup/<group>/items.level.json
        mod/traducao_ptbr_wcusa/levels/west_coast_usa/slotTraffic.json

Rules (docs/production/slotTraffic_update.md):
- level files are one JSON object per line: only the target lines change, and only the "speedLimit"
  field (replaced, or inserted in alphabetical key position); every other byte is copied from the game zip;
  added objects are whole new lines after the last object of a file, or a new file (new SimGroup);
- every edited line is re-parsed and compared with the original object: only speedLimit may differ;
- slotTraffic.json is derived from the navgraph: its lanes are matched to the edited DecalRoads by
  geometry (lane centerline samples within MATCH_M of the road polyline, >= 90 % of samples) and only
  the "speedLimit" lines of those lanes (roads.*.properties and nodes.*.links.*) are rewritten, keeping
  the file's formatting. Lanes are only touched if their current value equals the road's old effective
  value (explicit value, or the auto value read from the navgraph snapshot). Explicit mph-derived values
  (11.18 / 11.5 / 12 / 15.6464 m/s) are also replaced by value class (see build_slot).

    python tools/production/speed_overrides.py            # = python tools/production/apply_phase7_functional.py
    python tools/production/speed_overrides.py --check    # verify the mod files against the zip
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
GAME_ZIP = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/west_coast_usa.zip")
CHANGES = REPO / "working/speed/speed_changes.json"
PHASE7_CHANGES = [REPO / "working/functional/speed_changes.json", REPO / "working/functional/radar_changes.json"]
INSTANCES = REPO / "working/speed/sign_instances.json"
MOD_LEVEL = REPO / "mod/traducao_ptbr_wcusa/levels/west_coast_usa"
REPORT = REPO / "tests/reports/phase5_speed_diff.json"   # Phase 5 record (kept as committed; Phase 7 reports go to tests/reports/phase7/)
LEVEL_PREFIX = "levels/west_coast_usa/main/MissionGroup/"
SLOT = "levels/west_coast_usa/slotTraffic.json"
MATCH_M = 1.6
TOL = 1e-3
TOL_AUTO = 2e-3  # navgraph auto values are read with 4 decimals
EQUAL_MPS = 1e-4  # a slotTraffic value already equal to the target (explicit value == automatic one) is left untouched
# explicit values that come from mph signs (never from the automatic metric list 30/50/60/80/100/120 km/h)
MPH_VALUES = {11.18, 11.5, 12.0, 15.6464}
VALUE_CLASS_CATEGORIES = ("40_explicit", "60_explicit")
NO_ADDITIONS = {"append": {}, "new": {}}


def load_changes():
    """Phase 5 records (DecalRoad) followed by the Phase 7 ones (DecalRoad, BeamNGWaypoint, BeamNGTrigger)."""
    changes = json.loads(CHANGES.read_text(encoding="utf8"))["changes"]
    for p in PHASE7_CHANGES:
        if p.exists():
            changes += json.loads(p.read_text(encoding="utf8"))["changes"]
    seen = set()
    for c in changes:
        if (c["file"], c["pid"]) in seen:
            raise SystemExit(f"{c['pid']}: declared twice")
        seen.add((c["file"], c["pid"]))
    return changes


# ---------------------------------------------------------------- level files
def edit_line(line: str, pid: str, old, new: str, cls: str = "DecalRoad") -> str:
    obj = json.loads(line)
    if obj.get("persistentId") != pid or obj.get("class") != cls:
        raise SystemExit(f"{pid}: line is not that {cls}")
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


def build_level_files(changes, zf, additions=NO_ADDITIONS):
    """additions: {"append": {rel: [lines]}, "new": {rel: [lines]}} - whole objects added after the last object of a
    game file, or files that do not exist in the game (a new SimGroup)."""
    by_file = {}
    for c in changes:
        by_file.setdefault(c["file"], []).append(c)
    for inst in load_instances():
        by_file.setdefault(inst["file"], []).append(dict(inst, kind="shape"))
    for rel in additions["append"]:
        by_file.setdefault(rel, [])
    # stale overrides from earlier decisions are removed (only files this tool generates live here)
    root = MOD_LEVEL / "main/MissionGroup"
    if root.exists():
        for f in root.rglob("items.level.json"):
            rel = f.relative_to(root).as_posix()
            if rel not in by_file and rel not in additions["new"]:
                f.unlink()
    out = []
    for rel, new_lines in sorted(additions["new"].items()):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(("\n".join(new_lines) + "\n").encode("utf8"))
        out.append({"file": rel, "new_file": True, "added_objects": len(new_lines)})
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
                lines[i] = edit_line(lines[i], c["pid"], c["from"], c["to"], c.get("class", "DecalRoad"))
        app = additions["append"].get(rel, [])
        if app:
            tail = 1 if lines[-1] == "" else 0
            lines = lines[:len(lines) - tail] + list(app) + [""] * tail
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes("\n".join(lines).encode("utf8"))
        out.append({"file": rel, "edited_objects": len(items), "appended_objects": len(app), "lines_total": len(lines)})
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
    roads = [c for c in changes if c.get("class", "DecalRoad") == "DecalRoad"]  # waypoints/triggers have no lanes
    level = {}
    for c in roads:
        for l in zf.read(LEVEL_PREFIX + c["file"]).decode("utf8").split("\n"):
            if c["pid"] in l:
                o = json.loads(l)
                level[c["pid"]] = np.array([[n[0], n[1]] for n in o["nodes"]])
                roads_width[c["pid"]] = float(np.median([n[3] for n in o["nodes"]]))
                break
    lanes = match_lanes(slot, level)
    want, conflicts = {}, []
    for c in roads:
        old_eff = float(c["from"]) if c["from"] is not None else c["old_effective_mps"]
        for rid in lanes.get(c["pid"], []):
            prev = want.get(rid)
            if prev and abs(prev[1] - float(c["to"])) > TOL:
                conflicts.append({"lane": rid, "roads": [prev[2], c["pid"]]})
            want[rid] = (old_eff, float(c["to"]), c["pid"])  # same target: the last record wins (Phase 5 behaviour)
    if conflicts:
        raise SystemExit(f"slotTraffic: lanes matched to roads with different decisions: {conflicts[:5]}")
    # Explicit mph-derived values never come from the automatic metric list (30/50/60/80/100/120 km/h), and EVERY
    # navgraph road holding one of them is converted, so in the derived file the value itself identifies the source:
    # exact value replacement towards the class target. Lanes matched by geometry to a road with its own decision
    # (Phase 7: DR652, 35 mph -> 70 corridor instead of 60) take that decision first.
    explicit = {}
    for c in roads:
        if c["from"] is not None and c.get("category", "").startswith(VALUE_CLASS_CATEGORIES):
            k = float(c["from"])
            if k in explicit and abs(explicit[k] - float(c["to"])) > TOL:
                raise SystemExit(f"value class {k}: two targets")
            explicit[k] = float(c["to"])
    decided = {c["pid"] for c in roads}
    missing = [pid for pid, v in data_explicit_roads(zf).items() if float(v) in MPH_VALUES and pid not in decided]
    if missing or not set(explicit) >= ({float(v) for v in data_explicit_values(zf)} & MPH_VALUES):
        raise SystemExit(f"value-class replacement requires converting every road of the class (missing: {missing[:5]})")
    edits, skipped, equal, geo_hits = [], [], [], 0
    for i, kind, owner, val in walk_speed_lines(lines):
        w = want.get(owner)
        if w and abs(val - w[0]) <= TOL_AUTO:
            new, rule, road = w[1], "geometry", w[2]
        elif any(abs(val - k) <= TOL for k in explicit):
            new, rule, road = next(v for k, v in explicit.items() if abs(val - k) <= TOL), "value_class", None
        else:
            if w:
                skipped.append({"line": i + 1, "kind": kind, "lane": owner, "value": val, "expected_old": w[0], "road": w[2]})
            continue
        if abs(new - val) <= EQUAL_MPS:
            equal.append({"line": i + 1, "kind": kind, "lane": owner, "value": val, "road": road})
            continue
        geo_hits += rule == "value_class" and owner in want
        lines[i] = re.sub(r'("speedLimit":\s*)[-0-9.eE+]+', lambda m: m.group(1) + c_num(new), lines[i])
        e = {"line": i + 1, "kind": kind, "lane": owner, "old": val, "new": float(c_num(new)), "rule": rule}
        if road:
            e["road"] = road
        if rule == "value_class":
            e["geometry_match"] = owner in want
        edits.append(e)
    dst = MOD_LEVEL / "slotTraffic.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes("\n".join(lines).encode("utf8"))
    json.loads(dst.read_text(encoding="utf8"))  # still valid JSON
    report["slotTraffic"] = {
        "matched_lanes": {pid: v for pid, v in lanes.items()},
        "unmatched_roads": [pid for pid, v in lanes.items() if not v],
        "edited_lines": len(edits), "edited_road_properties": sum(e["kind"] == "road" for e in edits),
        "edited_links": sum(e["kind"] == "link" for e in edits), "value_class_lines_also_matched_by_geometry": geo_hits,
        "already_equal_untouched": equal, "skipped_value_mismatch": skipped, "edits": edits}


def data_explicit_roads(zf):
    """persistentId -> explicit speedLimit of every DecalRoad of the level (game zip)."""
    out = {}
    for n in zf.namelist():
        if n.startswith(LEVEL_PREFIX) and n.endswith("items.level.json"):
            for l in zf.read(n).decode("utf8", "replace").splitlines():
                if '"class":"DecalRoad"' in l and '"speedLimit"' in l:
                    o = json.loads(l)
                    out[o["persistentId"]] = o["speedLimit"]
    return out


def data_explicit_values(zf):
    return set(data_explicit_roads(zf).values())


def c_num(v: float) -> str:
    """Same style as the file (Lua %.14g)."""
    return f"{v:.14g}"


SIGN_REG = REPO / "tools/validation/config/sign_regulation.json"


def write_sign_regulation(changes, zf, added_signs=()):
    """Config for validate.py speeds: each speed sign -> roads it regulates (declared, reviewed decision).
    added_signs (Phase 7): signs the mod adds to the level, already with their regulated_roads."""
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
    signs += list(added_signs)
    out = {"_doc": "Generated by tools/production/apply_phase7_functional.py (speed_overrides.write_sign_regulation) from "
                   "working/speed/speed_changes.json + working/functional/. Each West Coast speed sign (original sign_speed* "
                   "and the R-19 signs added in Phase 7, group ptbr_functional_signs) with the DecalRoads it regulates "
                   "(semantic + spatial decision, docs/production/PHASE5_ROADSIGNS.md, docs/production/phase7/). "
                   "validate.py speeds checks sign value == explicit limit of every regulated road.",
           "signs": signs}
    SIGN_REG.write_text(json.dumps(out, indent=1) + "\n", encoding="utf8")


def verify(changes, zf, additions=NO_ADDITIONS):
    """Every mod level file differs from the zip only in the speedLimit of the declared objects (and the shapeName
    of the declared R-19 10 instances); appended / new files hold exactly the declared objects."""
    want = {(c["file"], c["pid"]): c["to"] for c in changes}
    shapes = {(i["file"], i["pid"]): i["to"] for i in load_instances()}
    problems, n_diff, n_added = [], 0, 0
    root = MOD_LEVEL / "main/MissionGroup"
    for dst in sorted(root.rglob("items.level.json")):
        rel = dst.relative_to(root).as_posix()
        b = dst.read_text(encoding="utf8").split("\n")
        if rel in additions["new"]:
            exp = list(additions["new"][rel]) + [""]
            if b != exp:
                problems.append(f"{rel}: new file differs from the declared objects")
            n_added += len(additions["new"][rel])
            continue
        if LEVEL_PREFIX + rel not in zf.namelist():
            problems.append(f"{rel}: not in the game and not declared")
            continue
        a = zf.read(LEVEL_PREFIX + rel).decode("utf8").split("\n")
        app = list(additions["append"].get(rel, []))
        if app:
            tail = 1 if a[-1] == "" else 0
            if b[len(a) - tail:len(a) - tail + len(app)] != app:
                problems.append(f"{rel}: appended objects differ from the declared ones")
            b = b[:len(a) - tail] + b[len(a) - tail + len(app):]
            n_added += len(app)
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
    n_decl_add = sum(len(v) for v in additions["append"].values()) + sum(len(v) for v in additions["new"].values())
    return {"ok": not problems and n_diff == declared and n_added == n_decl_add,
            "summary": f"{n_diff} changed lines / {declared} declared; {n_added} added objects / {n_decl_add} declared",
            "problems": problems}


def main(argv=None) -> int:
    # Since Phase 7 the level overrides are built together with the Phase 7 decisions (one deterministic build):
    # running this file alone must not drop the Phase 7 objects, so it delegates.
    sys.path.insert(0, str(Path(__file__).parent))
    import apply_phase7_functional
    return apply_phase7_functional.main(argv)


if __name__ == "__main__":
    sys.exit(main())
