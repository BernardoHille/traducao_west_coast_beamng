# Fase 7 — matriz do navgraph

Pontos reais do West Coast, lidos no jogo com o mod ativo (`map.findClosestRoad` no navgraph). Gerado por `working/functional/navgraph_matrix.py`.

**Resultado:** PASS (19/19).

| km/h | Local | Ponto (x, y) | Aresta | Navgraph | Origem do limite | Placa | Radar | Zona | Resultado |
|---:|---|---|---|---:|---|---|---|---|---|
| 10 | Docas: pista da cabine de saída (Fase 5, R-19 10) | [458.1, 1620.6] | `DR1221_5` → `DR1236_2` (+) | 10.0 km/h (2.7778 m/s) | explícito (Fase 5) | R-19 10 | — | the_dockyards 60 | PASS |
| 10 | Docas: pátio norte (Fase 5) | [457.7, 1680.1] | `DR1261_7` → `DR1252_1` (+) | 10.0 km/h (2.7778 m/s) | explícito (Fase 5) | R-19 10 | — | the_dockyards 60 | PASS |
| 40 | DR272, via local oeste (antigo início do Event 01) | [-520.0, 163.0] | `DR766_4` → `DR272_5` (-+) | 40.0 km/h (11.1111 m/s) | explícito (Fase 5, ex-25 mph) | — | — | — | PASS |
| 40 | Malha residencial oeste (Fase 5) | [-844.5, 555.1] | `DR384_2` → `DR384_3` (-+) | 40.0 km/h (11.1111 m/s) | explícito (Fase 5, ex-25 mph) | R-19 40 (malha) | — | — | PASS |
| 40 | Praça de pedágio, faixa DR630 entre as cabines | [-878.8, -548.1] | `DR630_3` → `DR630_4` (+) | 40.0 km/h (11.1111 m/s) | explícito (Fase 7, praça de pedágio) | R-19 40 (cabines) | — | — | PASS |
| 50 | DR312, spawn do ADAS Speed Alert | [431.2, 701.6] | `DR253_6` → `DR312_9` (++++) | 50.0 km/h (13.8889 m/s) | explícito (Fase 7, zona ADAS) | R-19 50 (entrada e à frente do spawn) | — | — | PASS |
| 50 | DR312, ~600 m depois do spawn | [-42.0, 339.0] | `DR312_7` → `BeamNGWaypoint_1` (++++) | 50.0 km/h (13.8889 m/s) | explícito (Fase 7, zona ADAS) | R-19 50 | — | — | PASS |
| 60 | DR571, radar speedCamera_003 | [-305.4, 325.2] | `DR571_5` → `DR655_1` (++) | 60.0 km/h (16.6667 m/s) | explícito (Fase 7, ex-35 mph) | — | speedTrapTrigger3 60 | — | PASS |
| 60 | DR666, avenida pista sul | [-374.3, 275.5] | `DR666_4` → `DR666_5` (++) | 60.0 km/h (16.6667 m/s) | explícito (Fase 7, ex-35 mph) | — | — | — | PASS |
| 60 | DR989, ilha, radar speedCamera_005 | [-1001.7, 1902.1] | `DR989_14` → `autojunction_711` (++) | 60.0 km/h (16.6667 m/s) | explícito (Fase 7, ex-35 mph) | — | speedTrapTrigger5 60 | — | PASS |
| 60 | DR1213, docas, radar speedCamera_006 | [414.3, 1646.2] | `DR1213_4` → `DR1253_5` (+) | 60.0 km/h (16.6667 m/s) | explícito (Fase 7, ex-35 mph) | — | speedTrapTrigger6 60 | the_dockyards 60 | PASS |
| 60 | DR1009, ilha, radar speedCamera_007 | [393.0, 1848.0] | `DR1009_26` → `DR1009_27` (+) | 60.0 km/h (16.6667 m/s) | explícito (Fase 7, ex-35 mph) | — | speedTrapTrigger7 60 | — | PASS |
| 70 | DR652, corredor do Event 01, radar speedCamera_002 | [-416.1, 197.7] | `DR652_2` → `autojunction_86` (++) | 70.0 km/h (19.4444 m/s) | explícito (Fase 7, corredor 70) | R-19 70 (entrada, repetição) | speedTrapTrigger2 70 | — | PASS |
| 70 | DR652, novo início do Event 01 | [-428.2, 164.3] | `DR192_5` → `DR652_2` (++) | 70.0 km/h (19.4444 m/s) | explícito (Fase 7, corredor 70) | R-19 70 a ~20 m | — | — | PASS |
| 80 | Alça Bridge36 depois do corredor do Event 01 (automático) | [-217.5, 350.5] | `DR659_5` → `Bridge36_3` (+) | 80.0 km/h (22.2222 m/s) | automático do jogo | — | — | — | PASS |
| 80 | DR501, via de mão dupla perto da zona ADAS (automático) | [422.0, 791.0] | `DR577_51` → `DR501_16` (-+) | 80.0 km/h (22.2222 m/s) | automático do jogo | — | — | — | PASS |
| 100 | Trevo junction1, radar speedCamera_004 | [-423.7, 672.8] | `junction1_wp25` → `junction1_wp19` (++) | 100.0 km/h (27.7778 m/s) | automático do jogo (waypoints inertes alinhados) | — | speedTrapTrigger4 100 | — | PASS |
| 120 | DR758, saída da zona ADAS | [-432.7, -38.2] | `Bridge30_1` → `Bridge30_2` (++++) | 120.0 km/h (33.3333 m/s) | explícito = automático (Fase 7) | R-19 120 | — | — | PASS |
| 120 | DR694, antes da zona ADAS | [590.0, 810.0] | `DR694_8` → `DR694_9` (++++) | 120.0 km/h (33.3333 m/s) | automático do jogo | — | — | — | PASS |
