# Fase 7 — IA ('legal') por classe de velocidade

Gerado a partir de `ai_test.json` (`working/functional/ai_test.py`).

| Caso | Via | Limite | Máx. | p90 | Amostras na classe | Resultado |
|---|---|---:|---:|---:|---:|---|
| ai50_dr312 | DR312, zona ADAS 50 a partir do spawn | 50 | 50.78 | 50.67 | 207/213 | PASS |
| ai40_dr272 | DR272, via local (Fase 5, ex-25 mph) | 40 | 40.65 | 40.22 | 105/117 | PASS |
| ai60_dr1009 | DR1009, ilha (ex-35 mph), passa pelo radar 7 | 60 | 60.42 | 60.01 | 173/174 | PASS |
| ai60_dr989 | DR989, ilha (ex-35 mph), passa pelo radar 5 | 60 | 61.42 | 59.82 | 117/117 | PASS |
| ai70_dr652 | DR652, corredor 70 do Event 01 (novo início) | 70 | 67.23 | 66.97 | 84/86 | PASS |
| ai80_dr282 | DR282, via de mão dupla automática (80) | 80 | 67.16 | 61.4 | 117/117 | PASS |
| ai40_toll | Praça de pedágio, faixa DR630 entre as cabines (Fase 7, 40) | 40 | 40.05 | 39.74 | 33/89 | PASS |

Critério: máx. ≤ limite × 1,03 + 1 e ≥ 80 % do limite (a IA chega ao limite sem passar). Em 80 km/h (via sinuosa) a IA chega a ~67 km/h pela curvatura, abaixo do limite.
