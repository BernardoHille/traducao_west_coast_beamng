"""Phase 7: measure in the game where the new R-19 signs (and the moved Event 01 start) go, and freeze the
result into working/functional/adas_zones.json ("signs" positions, "spawn" points).

Each placement is defined by a route (a start point + direction, followed along the legal navgraph flow), a
distance along it and a side. The script reads the navgraph through the BeamNG MCP (West Coast loaded):
  - position on the route polyline at that distance, flow direction f, road half-width (node radius);
  - lateral offset = half-width + clearance, to the right (f x up) or left;
  - ground height by a downward static ray.
The generator (tools/production/apply_phase7_functional.py) only reads the frozen numbers, so the build stays
deterministic and offline. Run again only if a placement definition changes:

    python working/functional/place_signs.py           # measure + write adas_zones.json
    python working/functional/place_signs.py --dry     # print only
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP  # noqa: E402

CFG = HERE / "adas_zones.json"

ROUTE_LUA = r"""
local mp = map.getMap()
local adj = {}
for a, n in pairs(mp.nodes) do
  for b, l in pairs(n.links) do
    adj[a] = adj[a] or {}; adj[b] = adj[b] or {}
    adj[a][b] = l; adj[b][a] = l
  end
end
local p = vec3(%f, %f, %f)
local dir = vec3(%f, %f, 0):normalized()
local a, b = map.findClosestRoad(p)
local prev, cur
if (mp.nodes[b].pos - mp.nodes[a].pos):dot(dir) > 0 then prev, cur = a, b else prev, cur = b, a end
-- start the polyline at the projection of p on the first edge
local pa, pb = mp.nodes[prev].pos, mp.nodes[cur].pos
local ab = pb - pa
local t = math.max(0, math.min(1, (p - pa):dot(ab) / ab:dot(ab)))
local s = pa + ab * t
local out = {{pos = {s.x, s.y, s.z}, r = mp.nodes[prev].radius + (mp.nodes[cur].radius - mp.nodes[prev].radius) * t, node = prev}}
local dist = 0
for i = 1, 200 do
  local cn = mp.nodes[cur]
  table.insert(out, {pos = {cn.pos.x, cn.pos.y, cn.pos.z}, r = cn.radius, node = cur, lim = adj[prev][cur].speedLimit})
  dist = dist + (cn.pos - mp.nodes[prev].pos):length()
  if dist > %f then break end
  local pdir = (cn.pos - mp.nodes[prev].pos):normalized()
  local best, bd = nil, -2
  for nid, l in pairs(adj[cur]) do
    if nid ~= prev then
      local legal = (not l.oneWay) or l.inNode == cur
      local dd = (mp.nodes[nid].pos - cn.pos):normalized():dot(pdir)
      if legal and dd > bd then best, bd = nid, dd end
    end
  end
  if not best then break end
  prev, cur = cur, best
end
return jsonEncode(out)
"""

GROUND_LUA = r"""
local pts = jsonDecode(%s)
local out = {}
for i, p in ipairs(pts) do
  local d = castRayStatic(vec3(p[1], p[2], p[3] + 6), vec3(0, 0, -1), 40)
  out[i] = (d and d < 40) and (p[3] + 6 - d) or false
end
return jsonEncode(out)
"""


def walk(poly, d):
    """Point, flow direction (xy) and half-width at distance d along the polyline."""
    acc = 0.0
    for a, b in zip(poly[:-1], poly[1:]):
        pa, pb = a["pos"], b["pos"]
        seg = ((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2) ** 0.5
        if seg > 1e-6 and acc + seg >= d:
            t = (d - acc) / seg
            p = [pa[i] + (pb[i] - pa[i]) * t for i in range(3)]
            f = [(pb[0] - pa[0]) / seg, (pb[1] - pa[1]) / seg]
            return p, f, a["r"] + (b["r"] - a["r"]) * t, a["node"], b["node"]
        acc += seg
    raise SystemExit(f"route shorter than {d} m")


def main(argv):
    dry = "--dry" in argv
    cfg = json.loads(CFG.read_text(encoding="utf8"))
    m = BeamNGMCP()
    st = m.call_json("get_status")
    if "west_coast_usa" not in (st.get("level") or ""):
        raise SystemExit("load West Coast USA first")
    routes = {}
    for rid, r in cfg["routes"].items():
        routes[rid] = json.loads(m.lua(ROUTE_LUA % (*r["start"], *r["dir"], r["length_m"])))
    pending = []
    for s in cfg["signs"] + cfg.get("spawns", []):
        pl = s["placement"]
        p, f, half, n0, n1 = walk(routes[pl["route"]], pl["distance_m"])
        right = [f[1], -f[0]]
        side = {"right": 1, "left": -1, "lane": 1}[pl["side"]]
        off = pl.get("lane_offset_m") if pl["side"] == "lane" else half + pl.get("clearance_m", 1.5)
        q = [p[0] + side * right[0] * off, p[1] + side * right[1] * off, p[2]]
        s["_measured"] = {"road_point": [round(v, 3) for v in p], "flow": [round(v, 4) for v in f], "half_width_m": round(half, 2),
                          "edge": [n0, n1], "xy": [round(q[0], 3), round(q[1], 3)], "road_z": round(p[2], 3)}
        pending.append((s, q))
    grounds = json.loads(m.lua(GROUND_LUA % json.dumps(json.dumps([q for _, q in pending]))))
    for (s, q), g in zip(pending, grounds):
        s["_measured"]["ground_z"] = round(g, 3) if g else None
        print(f'{s["id"]:28s} {s["_measured"]["xy"]} ground {s["_measured"]["ground_z"]} road_z {s["_measured"]["road_z"]} '
              f'flow {s["_measured"]["flow"]} edge {s["_measured"]["edge"]} half {s["_measured"]["half_width_m"]}')
    if not dry:
        CFG.write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
        print("written", CFG.relative_to(REPO))


if __name__ == "__main__":
    main(sys.argv[1:])
