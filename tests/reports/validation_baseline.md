# Baseline do validador (Fase 4)

**Data:** 30/09/2026 · **Comando:** `python tools/validation/validate.py all` (+ `speeds --refresh` para o snapshot do navgraph) · **Relatórios:** `export/reports/validation/` (`summary`, `selftest`, `regression*`, `mod_tree`, `speed_consistency`).

Objetivo: provar que o validador **aprova o que está certo e acusa o que está errado**. Nenhum input foi corrigido para "ficar verde".

## Resultado geral

```text
[PASS] Texture infrastructure (self-test): PASS 72 · WARN 0 · FAIL 0
[PASS] Regression (legacy images caught):  PASS 10 · WARN 0 · FAIL 0
[WARN] Mod tree + families:                PASS 6  · WARN 1 · FAIL 0   (PoC sem declaração shape_changed)
[FAIL] Current map speed consistency:      PASS 5  · FAIL 17 · SKIP 7  (inconsistências reais do jogo)
exit code 1
```

Exatamente o esperado: infraestrutura aprovada, defeitos conhecidos detectados.

## Tabela de verificação

| Dataset | Esperado | Obtido |
|---|---|---|
| original vs original (35 DDS + 35 PNG) | PASS | **PASS** — 70/70 idênticos a si mesmos (SHA do manifesto conferido; diff 0; alfa preservado; formato/mips/sRGB iguais) |
| PoC DDS metadata (`export/dds/poc/` e cópia no mod) | PASS | **PASS** — 2048×1024, BC7_UNORM_SRGB, sRGB, 12 mipmaps (cadeia completa), tamanho = calculado; alpha mode STRAIGHT × UNKNOWN compatível. *Não é tradução aprovada.* |
| old `eca_roadsigns_d` — alfa | FAIL | **FAIL** — `Alpha preservation`: transparência 11,64 % → 0 % (fundo virou opaco); também semitransparência e 76,9 % de pixels alterados |
| old `t_billboardsigns_dealers_b` — alfa | FAIL | **FAIL** — `Alpha preservation`: 100 % dos pixels alfa 0 (13,94 %) ficaram opacos; `Alpha noise`: 2.311 px opacos com alfa até 201 |
| old `t_roadsigns_b` — pixel diff | FAIL | **FAIL** — `Changes outside allowed regions`: 64,74 % dos pixels **fora** das 7 regiões confirmadas mudaram (bbox = atlas inteiro); `Alpha noise`: 6.139 px com alfa 201–254 |
| old `t_decal_roadmarkings` — família | FAIL | **FAIL** — `shape_changed`: só `_b.color` entregue; faltam `_o.data`, `_nm.normal`, `_ao.data` |
| current speed consistency | inconsistências | **17 FAIL** (detalhe abaixo) |

Casos extras do dataset negativo (todos detectados):

| Caso | Obtido | Motivo |
|---|---|---|
| old `eca_genericsigns` — família | FAIL | layout mudou sem emissivo/opacidade; e o `eca_genericsigns_d.dds` (o arquivo que o West Coast usa) não foi entregue |
| old `t_movie_studio_signage_b` | FAIL | 88,7 % dos pixels alterados sem região autorizada; ruído de alfa (2.633 px) |
| old `ind_industrial_signs_d` | FAIL | 95,2 % alterados; ruído de alfa (2.842 px) |
| old `t_sponsors_b` | FAIL | canto transparente (2,96 %) virou opaco; ruído de alfa (4.078 px) |
| old `t_decal_roadmarkings_b` (textura) | FAIL | 76,6 % alterados **fora** dos slots de texto (inclui setas e grelha, que não tinham texto) |
| old `t_sealbrik_logo_b` (cópia idêntica) | **PASS** | controle negativo: não há falso positivo |

Nota: as porcentagens de pixels alterados são maiores que as da auditoria (25–78 %) porque o validador compara todos os pixels com tolerância 2 (a auditoria amostrava a cada 4 px com tolerância 12).

## Consistência de velocidades do jogo atual (17 FAIL)

| Tipo | Detecção |
|---|---|
| Limites explícitos de via | 85 não são múltiplos de 10 km/h: 40,2 (×65), 41,4 (×1), 43,2 (×8), 56,3 (×11) km/h |
| Zonas do mapa (`city.sites.json`) | horizon_estates 48,2 · the_dockyards 56,2 · mount_wallis 80,6 km/h |
| Zonas das missões garageToGarage | downtownBelasco 48,2 · residential 48,2 · dockyard 56,2 · mountWallis 80,6 km/h |
| Radares (6) | todos a 56,3 km/h (35 mph, não múltiplo de 10); **radar 4 ≠ via** (via de 100 km/h, sem zona que regulamente 56,3); os outros 5 = via |
| Placas 5 mph (37) | unidade mph; 37/37 divergem da via ao lado (30 e 60 km/h) |
| Placas 25 mph (11) | unidade mph; 11/11 divergem da via ao lado (30 e 60 km/h) |
| ADAS `event01` (detecção) | 70 km/h ≠ via no início (40,2 km/h) |
| ADAS `adasSpeedAlertTest` / `Web` (alerta) | 50 km/h ≠ via no início (120 km/h) |
| Reaction Test | **SKIP** — faixa experimental 40–70 km/h, excluída por política (sem falso positivo) |
| Missões `arrive` (6) | SKIP — `maxSpeedActive=false` |

## Correções feitas no próprio validador durante a construção
1. Expectativa do caso `dealers`: a auditoria falava em "22 % semitransparente", mas quase todos esses pixels têm alfa 253–254 (a mudança para 255 está dentro da tolerância). A detecção correta é a perda de **100 % dos pixels alfa 0** — a expectativa foi ajustada, **o input não**.
2. Tolerância de "múltiplo de 10": 0,3 km/h deixava 11,18 m/s (40,25 km/h, herdado de 25 mph) passar; reduzida para 0,05 km/h.
