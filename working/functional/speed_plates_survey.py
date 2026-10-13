"""Phase 7: survey of the speed plates built into roadsigns.dae (single TSStatic at the origin, StaticObjects group) and
the road each one regulates. Writes working/functional/speed_plates.json (decisions + measured data).

Plates are found in the mesh by their atlas cells (t_roadsigns, material roadsigns):
  regulatory: white board [370,188,517,381] + SPEED LIMIT [235,284,355,378] + two digit glyphs
  advisory:   yellow board [370,383,517,530] + two digit glyphs + MPH [256,244,351,279]
The regulated road is the nearest navgraph edge (mod loaded) whose legal flow runs against the plate's face
(traffic that sees the plate), read through the BeamNG MCP. Decision rule (docs/production/phase7/SPEED_PLATES.md):
  regulatory -> R-19 showing the limit enforced on that edge (same rule as the radars, spec 14/15); no road changes;
  advisory   -> mph value converted by the project table (LOCALIZATION_RULES 2.3), advisory only.

    python working/functional/speed_plates_survey.py
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/production"))
sys.path.insert(0, str(REPO / "tools/beamng"))
import glyph_signs as G  # noqa: E402
from mcp_client import BeamNGMCP  # noqa: E402

DAE = REPO / "source/originals/meshes/roads/roadsigns.dae"
BOARD_REG, SPEED_LIMIT = (370, 188, 517, 381), (235, 284, 355, 378)
BOARD_ADV, MPH = (370, 383, 517, 530), (256, 244, 351, 279)
TABLE = {15: 20, 20: 30, 25: 40, 30: 50, 35: 60}   # advisory mph -> km/h (LOCALIZATION_RULES 2.3)
# plates whose regulated road is not within the default search (sign on an overpass above the freeway)
EDGE_OVERRIDE = {(87.1, 406.7): {"edge": ["DR294_16", "DR294_15"], "why": "plate on the overpass railing, regulates the NE-bound freeway below"}}

LUA = r"""
local pls = jsonDecode(%s)
local mp = map.getMap()
local out = {}
for i, p in ipairs(pls) do
  local c = vec3(p[1], p[2], p[3]); local n = vec3(p[4], p[5], 0)
  local best = nil
  for a, na in pairs(mp.nodes) do
    for b, l in pairs(na.links) do
      local nb = mp.nodes[b]
      local want = p[6] ~= '' and ((a == p[6] and b == p[7]) or (a == p[7] and b == p[6]))
      local ab = nb.pos - na.pos
      local t = math.max(0, math.min(1, (c - na.pos):dot(ab) / math.max(ab:dot(ab), 1e-6)))
      local q = na.pos + ab * t
      local d = (vec3(q.x, q.y, 0) - vec3(c.x, c.y, 0)):length()
      if want or (p[6] == '' and d < 30 and math.abs(q.z - c.z) < 8 and l.drivability >= 0.5) then
        local fwd = ab:normalized()
        local dirs = l.oneWay and {(l.inNode == a) and fwd or -fwd} or {fwd, -fwd}
        for _, f in ipairs(dirs) do
          if want or f:dot(n) < -0.6 then
            if not best or want or d < best.d then
              best = {a = a, b = b, d = d, lim = l.speedLimit, lanes = l.lanes, oneWay = l.oneWay, q = {q.x, q.y, q.z}, flow = {f.x, f.y}}
            end
          end
        end
      end
    end
  end
  out[i] = best or false
end
return jsonEncode(out)
"""


def rect(q):
    return tuple(round(v) for v in q["rect"])


def same(r, cell, tol=1.5):
    return max(abs(a - b) for a, b in zip(r, cell)) <= tol


def main():
    q = G.read_quads(DAE, "roadsigns", (2048, 1024))
    digits = json.loads((HERE / "speed_plates_digits.json").read_text(encoding="utf8"))  # digit cell rect -> digit
    dig = {tuple(d["rect"]): d["digit"] for d in digits["cells"]}
    plates = []
    for kind, legend, board in (("regulatory", SPEED_LIMIT, BOARD_REG), ("advisory", MPH, BOARD_ADV)):
        for x in q:
            if not same(rect(x), legend):
                continue
            c = x["centroid"]
            near = [y for y in q if np.linalg.norm(y["centroid"] - c) < 0.9 and abs(float(y["normal"] @ x["normal"])) > 0.9]
            b = [y for y in near if same(rect(y), board)]
            dq = [y for y in near if rect(y) in dig]
            # stacked glyph layers (same place, e.g. a dark copy behind a digit) form one digit
            groups = []
            for y in dq:
                g = next((g for g in groups if np.linalg.norm(g[0]["centroid"] - y["centroid"]) < 0.05), None)
                (g.append(y) if g else groups.append([y]))
            if len(b) != 1 or len(groups) != 2:
                raise SystemExit(f"{kind} plate at {c}: board {len(b)}, digits {len(groups)}")
            # reading direction and front side from the legend's texture frame (vertex winding is not consistent in
            # this mesh): atlas u grows to the right and v downwards as seen from the front (glyph_signs.render)
            M = np.linalg.lstsq(np.c_[x["uv_px"][0], np.ones(3)], x["tris"][0], rcond=None)[0]
            right = M[0] / np.linalg.norm(M[0])
            n = np.cross(M[0], -M[1])
            n = n / np.linalg.norm(n)
            groups = sorted(groups, key=lambda g: float(g[0]["centroid"] @ right))
            if any(len({dig[rect(y)] for y in g}) != 1 for g in groups):
                raise SystemExit(f"{kind} plate at {c}: stacked glyphs disagree")
            mph = int("".join(str(dig[rect(g[0])]) for g in groups))
            ds = [y for g in groups for y in g]
            plates.append({"kind": kind, "center": [round(float(v), 3) for v in b[0]["centroid"]], "normal": [round(float(v), 3) for v in n],
                           "mph": mph, "quads": {"board": [rect(b[0]), [round(float(v), 3) for v in b[0]["centroid"]]],
                                                 "legend": [rect(x), [round(float(v), 3) for v in x["centroid"]]],
                                                 "digits": [[rect(y), [round(float(v), 3) for v in y["centroid"]]] for y in ds]}})
    plates.sort(key=lambda p: (p["kind"] != "regulatory", p["center"][0], p["center"][1]))
    k = {"regulatory": 0, "advisory": 0}
    for p in plates:
        p["id"] = f"{'reg' if p['kind'] == 'regulatory' else 'adv'}_{k[p['kind']]:02d}"
        k[p["kind"]] += 1
    m = BeamNGMCP()
    reg = [p for p in plates if p["kind"] == "regulatory"]
    def override(p):
        return next((v for k, v in EDGE_OVERRIDE.items() if abs(k[0] - p["center"][0]) < 1 and abs(k[1] - p["center"][1]) < 1), None)
    args = [[*p["center"], *p["normal"][:2], *((override(p) or {}).get("edge") or ["", ""])] for p in reg]
    res = json.loads(m.lua(LUA % json.dumps(json.dumps(args))))
    for p, r in zip(reg, res):
        if not r:
            raise SystemExit(f"{p['id']}: no regulated edge found")
        p["regulated_edge"] = {"nodes": [r["a"], r["b"]], "distance_m": round(r["d"], 1), "point": [round(v, 2) for v in r["q"]],
                               "lanes": r["lanes"], "limit_kmh": round(r["lim"] * 3.6, 1)}
        if override(p):
            p["regulated_edge"]["override"] = override(p)["why"]
        p["value_kmh"] = int(round(r["lim"] * 3.6))
        p["rule"] = "R-19 = limite aplicado na via regulada (mesma regra dos radares); via não alterada"
    for p in plates:
        if p["kind"] == "advisory":
            p["value_kmh"] = TABLE[p["mph"]]
            p["rule"] = f"advertência: {p['mph']} mph -> {TABLE[p['mph']]} km/h (LOCALIZATION_RULES 2.3); sem efeito funcional"
    out = {"_doc": __doc__, "mesh": "levels/west_coast_usa/art/shapes/roads/roadsigns.dae", "instance": "StaticObjects (no transform: mesh = world)",
           "plates": plates}
    (HERE / "speed_plates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    for p in plates:
        print(p["id"], p["kind"], p["mph"], "->", p["value_kmh"], p.get("regulated_edge", {}).get("nodes"), p["center"])


if __name__ == "__main__":
    main()
