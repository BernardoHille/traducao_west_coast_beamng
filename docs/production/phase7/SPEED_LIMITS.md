# Fase 7 — Limites de velocidade (vias)

**Decisões:** `working/functional/speed_changes.json` (cada registro aponta para uma entrada de `working/functional/phase7_plan.json`).
**Aplicação:** `tools/production/apply_phase7_functional.py`, sobre o motor da Fase 5 (`speed_overrides.py`). Os valores são em m/s, com 4 casas e sem conversão encadeada a partir de mph.

## Hierarquia aplicada

| Contexto | km/h | Onde |
|---|---:|---|
| estacionamento/pátio | 10 | Fase 5, intacto (18 vias) |
| via local | 40 | Fase 5, intacto (83 vias) + 5 faixas da praça de pedágio (Fase 7) |
| zona ADAS 50 | 50 | DR312 (via expressa sob o spawn do ADAS Speed Alert) |
| ex-35 mph | 60 | 8 DecalRoads (AIWaypoints, ilha, docas) |
| corredor do Event 01 | 70 | DR652 (pista norte da avenida) |
| Mount Wallis | 80 | zona (dado; ver `ZONES_AND_MISSIONS.md`) |
| via rápida / rodovia | 100 / 120 | automáticos do jogo, preservados; DR758 recebe 120 explícito (= automático) na saída da zona ADAS |

Os limites automáticos do motor (30/50/60/80/100/120, `lua/ge/map.lua`) não foram mexidos, salvo as exceções declaradas acima.

## Vias alteradas na Fase 7

| Plano | Via (pid) | Antes | Depois | Contexto |
|---|---|---|---|---|
| ex35mph_60 | DR571 `2388e8bc` | 15,6464 (56,3) | 16,6667 (60) | urbana, saída do fim da avenida; radar 3 |
| ex35mph_60 | DR666 `af746a38` | 15,6464 | 16,6667 | pista sul da avenida (o Event 01 usa a norte) |
| ex35mph_60 | DR625 `6777a576` | 15,6464 | 16,6667 | alça do trevo junction1 para a via local |
| ex35mph_60 | DR989 `d241454f` | 15,6464 | 16,6667 | ilha; radar 5 |
| ex35mph_60 | DR1003 `be0f5b74` | 15,6464 | 16,6667 | acesso ilha → docas |
| ex35mph_60 | DR1009 `1e4035d1` | 15,6464 | 16,6667 | ilha; radar 7 |
| ex35mph_60 | DR1213 `c5865b41` | 15,6464 | 16,6667 | portaria das docas; radar 6 |
| ex35mph_60 | DR1216 `af1085ba` | 15,6464 | 16,6667 | via interna das docas |
| event01_corridor_70 | DR652 `989ef979` | 15,6464 | 19,4444 (70) | ver `EVENT01_70.md` |
| adas50_zone | DR312 `cfca014d` | automático 120 | 13,8889 (50) | ver `ADAS_50.md` |
| adas50_exit_120 | DR758 `512c9f8f` | automático 120 | 33,3333 (120) | sem mudança funcional; a placa R-19 120 regula uma via com limite declarado |
| toll_plaza_40 | DR535, DR559, DR595, DR630, DR672 | automático 50/60/80/100/120 | 11,1111 (40) | faixas que atravessam as cabines; ver `SPEED_PLATES.md` |

Os IDs foram reconfirmados no zip 0.39.4 e no navgraph: as 96 arestas de 56,3 km/h pertenciam todas a estes 9 DecalRoads. A lista antiga não foi usada às cegas.

## Waypoints inertes

`junction1_wp19` e `junction1_wp25` (BeamNGWaypoint) tinham `speedLimit` 15,6464. No 0.39.4 o campo é inerte: `map.lua` só usa a posição e o raio do waypoint, e o limite da aresta vem do DecalRoad. A aresta wp25 → wp19 é 100 km/h no navgraph. O campo foi alinhado a 27,7778 (100), o mesmo valor do radar 4, sem efeito na IA (plano `junction1_waypoints_inert`).

## Verificação

- Gerador: 132 linhas alteradas, todas declaradas (101 da Fase 5, 7 `shapeName` da Fase 5 e 24 da Fase 7); 15 objetos novos declarados; cada linha relida e comparada com o objeto original, só `speedLimit` muda (`tests/reports/phase7/functional_diff.md`).
- Matriz do navgraph: 19/19 pontos reais de 10 a 120 km/h com o valor esperado (`tests/reports/phase7/navgraph_matrix.md`).
- IA em modo `legal`: 7 casos (40, 40 no pedágio, 50, 60 ×2, 70, 80), todos sem passar do limite (`tests/reports/phase7/ai_qa.md`).
- Mod desligado: as vias voltam a 56,3 / 120 / 40,2 (original) (`tests/reports/phase7/mod_off_qa.md`).
