# Delta do validador de velocidade — Fase 4 × Fase 5

**Antes:** `validate.py speeds` do commit `0256004` (Fase 4, mapa original).
**Depois:** `validate.py speeds --refresh` em 30/09/2026 22:00, na sessão reiniciada, com o mod ativo e o navgraph recoletado no jogo (`tools/validation/data/wcusa_speed_snapshot.json`).
**Relatórios:** `export/reports/validation/speed_consistency.md` / `.json`.

## Resumo

| | Fase 4 | Fase 5 |
|---|---:|---:|
| FAIL | **17** | **13** |
| PASS | 5 | 9 |
| WARN | 0 | 1 |
| SKIP | 7 | 7 |

Os 13 FAILs restantes pertencem todos a sistemas **fora do escopo da Fase 5**: 60 km/h, zonas, radares e ADAS.

## FAILs eliminados (escopo da Fase 5)

| Verificação (Fase 4) | Mensagem na Fase 4 | Fase 5 |
|---|---|---|
| Speed sign 5 mph: unit | "37 signs show mph" | **PASS**: "Speed sign 10 km/h: unit — 7 signs show km/h (R-19 mesh of the mod)" |
| Speed sign 5 mph vs road | "37/37 signs disagree with the road limit next to them (30/60 km/h)" | **PASS**: "7 signs == explicit limit of the 18 distinct roads they regulate" |
| Speed sign 25 mph: unit | "11 signs show mph" | **PASS**: "Speed sign 40 km/h: unit — 11 signs show km/h" |
| Speed sign 25 mph vs road | "11/11 signs disagree … (30/60 km/h)" | **PASS**: "11 signs == explicit limit of the 9 distinct roads they regulate" |

**Correção da contagem da Fase 4:** os "37 signs" de 5 mph incluíam os 30 objetos `sign_speed5.dae` do grupo `port/portNumbersSigns`. Esses objetos são **decalques de fundo dos números das baias** (`decalType: Visible Mesh Final`), não placas. O validador agora ignora decalques de malha, e as placas reais de 5 mph são 7.

## FAIL reduzido (escopo parcial)

| Verificação | Fase 4 | Fase 5 |
|---|---|---|
| Road limits: multiples of 10 km/h | **85** limites explícitos fora de múltiplo de 10: 40,2 ×65 · 41,4 ×1 · 43,2 ×8 · 56,3 ×11 | **11**: só 56,3 km/h (15,6464 m/s, ex-35 mph) ×11 |

Os 74 limites herdados de 25 mph (11,18 / 11,5 / 12 m/s) viraram **11,1111 m/s (40 km/h)**. Os 11 restantes são do grupo de 60 km/h, fora do escopo (§30).

## Novo aviso (informativo)

| Verificação | Resultado | Explicação |
|---|---|---|
| Speed signs: nearest navgraph edge | WARN: 14/18 placas têm a via mais próxima com o mesmo valor | As 4 que diferem são as placas de 25 mph na **saída da cobertura das cabines das docas** (x = 476,9). Elas ficam no fim das faixas das cabines (10 km/h, placa de 5 mph na entrada da cabine) e regulamentam a via seguinte (40 km/h). A associação declarada placa → via (`config/sign_regulation.json`) passa |

## FAILs que permanecem (fora do escopo, inalterados)

| Verificação | Valor | Fase prevista |
|---|---|---|
| Road limits: multiples of 10 | 56,3 km/h ×11 (6 AIWaypoints, 3 ilha, 2 docas) | funcional 60 km/h |
| Map zones (`city.sites.json`) | horizon_estates 48,2 · mount_wallis 80,6 · the_dockyards 56,2 | zonas |
| Mission zones (garageToGarage) | downtownBelasco 48,2 · residential 48,2 · dockyard 56,2 · mountWallis 80,6 | zonas |
| Radares speedTrapTrigger2…7: valor regulatório | 56,3 km/h ×6 | radares |
| Radar speedTrapTrigger4 vs via | 56,3 ≠ via 100 km/h | radares |
| ADAS event01SpeedLimitRecognition | alerta 70 km/h ≠ via no início | ADAS |
| ADAS adasSpeedAlertTest / Web | alerta 50 km/h ≠ via 120 km/h | ADAS |

**Event 01:** a via no ponto de partida passou de 40,2 km/h (11,18 m/s) para **40,0 km/h (11,1111 m/s)**, pela conversão desta fase. O alerta de 70 km/h não foi tocado (§52) e continua divergente.

## Verificações complementares no jogo (sessão nova, mod ativo)

- **Navgraph (`tests/reports/phase5_navgraph_check.json`):** 13/13 PASS. 40 km/h em 7 vias de controle e 10 km/h em 4. A via pública ao lado do estacionamento não foi reduzida (60 km/h), e o pátio do porto, sem placa, continua no automático (30 km/h).
- **IA (`tests/reports/phase5_ai_test.json`):** veículo com IA em modo `legal`:
  - na via `515427bb` (40 km/h): máximo **40,4 km/h**, p90 39,5;
  - na faixa `c7478227` (10 km/h): máximo **6,8 km/h**.
