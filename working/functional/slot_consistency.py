"""Phase 7 block D: navgraph (game, mod loaded) vs slotTraffic.json (mod) lane by lane.

For every slotTraffic road (lane) the navgraph limit is read at 25/50/75 % of its centerline (map.findClosestRoad);
the lane value must equal the navgraph value where they overlap. Writes tests/reports/phase7/slottraffic_consistency.md/.json.
"""
import collections
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
sys.path.insert(0, str(REPO / "tools/production"))
from mcp_client import BeamNGMCP  # noqa: E402

slot = json.loads((REPO / "mod/traducao_ptbr_wcusa/levels/west_coast_usa/slotTraffic.json").read_text(encoding="utf8"))
diff = json.loads((REPO / "tests/reports/phase7/functional_diff.json").read_text(encoding="utf8"))
p5 = json.loads((REPO / "tests/reports/phase5_speed_diff.json").read_text(encoding="utf8"))
edited = {e["lane"] for e in diff["slotTraffic"]["edits"]}
edited_p5 = {e["lane"] for e in p5["slotTraffic"]["edits"]}
pts, owners = [], []
for rid, cl in slot["centerlines"].items():
    P = np.array([[p["x"], p["y"], p.get("z", 0)] for p in cl.get("samples") or cl["points"]])
    if len(P) < 2:
        continue
    seg = np.linalg.norm(np.diff(P[:, :2], axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    for f in (0.25, 0.5, 0.75):
        d = f * s[-1]
        i = min(np.searchsorted(s, d), len(P) - 1)
        pts.append([round(float(v), 3) for v in P[i]])
        owners.append(rid)
LUA = r"""
local pts = jsonDecode(%s)
local mp = map.getMap()
local out = {}
for i, p in ipairs(pts) do
  local a, b, d = map.findClosestRoad(vec3(p[1], p[2], p[3]))
  local l = a and ((mp.nodes[a].links[b]) or (mp.nodes[b] and mp.nodes[b].links[a]))
  out[i] = l and {l.speedLimit, d} or false
end
return jsonEncode(out)
"""
m = BeamNGMCP()
res = []
for k in range(0, len(pts), 1500):
    res += json.loads(m.lua(LUA % json.dumps(json.dumps(pts[k:k + 1500]))))
nav = collections.defaultdict(list)
for o, r in zip(owners, res):
    if r and r[1] < 3.0:
        nav[o].append(r[0])
rows, stats = [], collections.Counter()
for rid, props in ((k, v["properties"]) for k, v in slot["roads"].items()):
    v = props.get("speedLimit")
    vals = nav.get(rid)
    if v is None or not vals:
        stats["no_navgraph_overlap"] += 1
        continue
    mode = collections.Counter(round(x, 3) for x in vals).most_common(1)[0][0]
    ok = abs(mode - v) <= 2e-3
    group = "phase7_edited" if rid in edited - edited_p5 else ("phase5_edited" if rid in edited_p5 else "untouched")
    stats[(group, ok)] += 1
    if not ok:
        rows.append({"lane": rid, "group": group, "slot_kmh": round(v * 3.6, 1), "navgraph_kmh": round(mode * 3.6, 1), "samples": len(vals)})
mph = [r for r in rows if abs(r["slot_kmh"] - 56.3) < 0.2 or abs(r["navgraph_kmh"] - 56.3) < 0.2]
out = {"lanes": len(slot["roads"]), "stats": {f"{k[0]}:{'match' if k[1] else 'differ'}" if isinstance(k, tuple) else k: v for k, v in stats.items()},
       "mph_56_3_mismatches": mph, "differ": rows}
(REPO / "tests/reports/phase7/slottraffic_consistency.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf8")
print(json.dumps(out["stats"], indent=1), "mph mismatches:", len(mph))
by = collections.Counter((r["group"], r["slot_kmh"], r["navgraph_kmh"]) for r in rows)
for k, v in by.most_common(25):
    print(v, k)
