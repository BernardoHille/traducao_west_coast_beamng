"""Phase 7 block J: navgraph matrix - one or more real points per speed class (10/40/50/60/70/80/100/120), read in the
game with the mod loaded (map.findClosestRoad on the navgraph). Writes tests/reports/phase7/navgraph_matrix.md/.json.

    python working/functional/navgraph_matrix.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP  # noqa: E402

# (expected km/h, label, x, y, z, source, sign, radar, zone)
POINTS = [
    (10, "Docas: pista da cabine de saída (Fase 5, R-19 10)", 458.1, 1620.6, 76.2, "explícito (Fase 5)", "R-19 10", "—", "the_dockyards 60"),
    (10, "Docas: pátio norte (Fase 5)", 457.7, 1680.1, 76.2, "explícito (Fase 5)", "R-19 10", "—", "the_dockyards 60"),
    (40, "DR272, via local oeste (antigo início do Event 01)", -520.0, 163.0, 100.3, "explícito (Fase 5, ex-25 mph)", "—", "—", "—"),
    (40, "Malha residencial oeste (Fase 5)", -844.5, 555.1, 0, "explícito (Fase 5, ex-25 mph)", "R-19 40 (malha)", "—", "—"),
    (40, "Praça de pedágio, faixa DR630 entre as cabines", -878.8, -548.1, 106.6, "explícito (Fase 7, praça de pedágio)", "R-19 40 (cabines)", "—", "—"),
    (50, "DR312, spawn do ADAS Speed Alert", 431.2, 701.6, 115.9, "explícito (Fase 7, zona ADAS)", "R-19 50 (entrada e à frente do spawn)", "—", "—"),
    (50, "DR312, ~600 m depois do spawn", -42.0, 339.0, 116.0, "explícito (Fase 7, zona ADAS)", "R-19 50", "—", "—"),
    (60, "DR571, radar speedCamera_003", -305.4, 325.2, 101.5, "explícito (Fase 7, ex-35 mph)", "—", "speedTrapTrigger3 60", "—"),
    (60, "DR666, avenida pista sul", -374.3, 275.5, 101.3, "explícito (Fase 7, ex-35 mph)", "—", "—", "—"),
    (60, "DR989, ilha, radar speedCamera_005", -1001.7, 1902.1, 90.0, "explícito (Fase 7, ex-35 mph)", "—", "speedTrapTrigger5 60", "—"),
    (60, "DR1213, docas, radar speedCamera_006", 414.3, 1646.2, 74.0, "explícito (Fase 7, ex-35 mph)", "—", "speedTrapTrigger6 60", "the_dockyards 60"),
    (60, "DR1009, ilha, radar speedCamera_007", 393.0, 1848.0, 74.0, "explícito (Fase 7, ex-35 mph)", "—", "speedTrapTrigger7 60", "—"),
    (70, "DR652, corredor do Event 01, radar speedCamera_002", -416.1, 197.7, 100.5, "explícito (Fase 7, corredor 70)", "R-19 70 (entrada, repetição)", "speedTrapTrigger2 70", "—"),
    (70, "DR652, novo início do Event 01", -428.2, 164.3, 100.1, "explícito (Fase 7, corredor 70)", "R-19 70 a ~20 m", "—", "—"),
    (80, "Alça Bridge36 depois do corredor do Event 01 (automático)", -217.5, 350.5, 102.0, "automático do jogo", "—", "—", "—"),
    (80, "DR501, via de mão dupla perto da zona ADAS (automático)", 422.0, 791.0, 122.5, "automático do jogo", "—", "—", "—"),
    (100, "Trevo junction1, radar speedCamera_004", -423.7, 672.8, 75.0, "automático do jogo (waypoints inertes alinhados)", "—", "speedTrapTrigger4 100", "—"),
    (120, "DR758, saída da zona ADAS", -432.7, -38.2, 109.1, "explícito = automático (Fase 7)", "R-19 120", "—", "—"),
    (120, "DR694, antes da zona ADAS", 590.0, 810.0, 115.1, "automático do jogo", "—", "—", "—"),
]
LUA = r"""
local pts = jsonDecode(%s)
local mp = map.getMap()
local out = {}
for i, p in ipairs(pts) do
  local z = p[3]
  if z == 0 then z = (core_terrain and core_terrain.getTerrainHeight and core_terrain.getTerrainHeight(vec3(p[1], p[2], 0))) or 0 end
  local a, b, d = map.findClosestRoad(vec3(p[1], p[2], z))
  local l = a and ((mp.nodes[a].links[b]) or (mp.nodes[b] and mp.nodes[b].links[a]))
  out[i] = l and {a = a, b = b, d = d, lim = l.speedLimit, oneWay = l.oneWay, lanes = l.lanes} or false
end
return jsonEncode(out)
"""


def main():
    m = BeamNGMCP()
    res = json.loads(m.lua(LUA % json.dumps(json.dumps([[p[2], p[3], p[4]] for p in POINTS]))))
    rows, ok_all = [], True
    for p, r in zip(POINTS, res):
        got = round(r["lim"] * 3.6, 1) if r else None
        ok = got is not None and abs(got - p[0]) < 0.5
        ok_all &= ok
        rows.append({"expected_kmh": p[0], "label": p[1], "point": [p[2], p[3]], "edge": [r["a"], r["b"]] if r else None,
                     "distance_m": round(r["d"], 1) if r else None, "navgraph_kmh": got, "navgraph_mps": round(r["lim"], 4) if r else None,
                     "lanes": r.get("lanes") if r else None, "source": p[5], "sign": p[6], "radar": p[7], "zone": p[8], "result": "PASS" if ok else "FAIL"})
    out = REPO / "tests/reports/phase7"
    (out / "navgraph_matrix.json").write_text(json.dumps({"ok": ok_all, "rows": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    L = ["# Fase 7 — matriz do navgraph", "",
         "Pontos reais do West Coast, lidos no jogo com o mod ativo (`map.findClosestRoad` no navgraph). Gerado por "
         "`working/functional/navgraph_matrix.py`.", "",
         f"**Resultado:** {'PASS' if ok_all else 'FAIL'} ({sum(r['result'] == 'PASS' for r in rows)}/{len(rows)}).", "",
         "| km/h | Local | Ponto (x, y) | Aresta | Navgraph | Origem do limite | Placa | Radar | Zona | Resultado |",
         "|---:|---|---|---|---:|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['expected_kmh']} | {r['label']} | {r['point']} | `{r['edge'][0]}` → `{r['edge'][1]}` ({r['lanes']}) | "
                 f"{r['navgraph_kmh']} km/h ({r['navgraph_mps']} m/s) | {r['source']} | {r['sign']} | {r['radar']} | {r['zone']} | {r['result']} |")
    (out / "navgraph_matrix.md").write_text("\n".join(L) + "\n", encoding="utf8")
    for r in rows:
        print(r["result"], r["expected_kmh"], r["navgraph_kmh"], r["edge"], r["distance_m"], r["label"])


if __name__ == "__main__":
    main()
