# Dados quantitativos do artigo

Cada número usado no artigo, com a fonte interna. Quando havia duas medições diferentes, as duas aparecem com a explicação. Data da consolidação: 02/10/2026, commit `70329b1`. Os números marcados com "re-executado" foram medidos de novo nesta fase.

## 1. Inventário inicial

| Dado | Valor | Fonte |
|---|---:|---|
| Texturas originais (DDS + PNG) | 35 | `docs/inventory/original_files_manifest.csv` (`classification` = `original_dds` / `original_png`) |
| Contagem da auditoria | 41 "texturas" | `docs/AUDITORIA_PROJETO_TRADUCAO.md` §1. Contava ocorrências nos zips; ver `texture_families.md`, "Observações posteriores", item 1 |
| PNG `_ptbr` de referência | 13 | manifesto (`current_ptbr_reference`) |
| Texturas traduzidas nessas referências | 11 + 1 máscara + 1 cópia idêntica | `PROJECT_STATUS.md`; auditoria §2 (`t_sealbrik_logo` com mesmo MD5) |
| DDS PT-BR, mod, testes no jogo, versionamento no início | 0 / não / não / não | auditoria §1 e §7 |

## 2. Formatos DDS dos originais

| Formato | Texturas | Fonte |
|---|---:|---|
| DX10 BC7_UNORM_SRGB | 21 | manifesto, coluna `file_format` |
| DX10 BC7_UNORM | 2 | idem |
| BC4_UNORM | 3 | idem |
| BC3 (DXT5) | 5 | idem |
| BC1 (DXT1) | 4 | idem |
| Mipmaps nos originais | 7 a 12 níveis | `TEXTURE_GUIDELINES.md`, Regra 6 |

## 3. Auditoria das referências antigas

| Dado | Valor | Fonte / observação |
|---|---|---|
| Pixels alterados (auditoria, amostragem 1:4, tolerância 12) | 25,9% a 77,8% | auditoria §4.2 |
| Pixels alterados (validador, todos os pixels, tolerância 2) | ex.: `eca_roadsigns_d` 76,9%; `t_movie_studio` 88,7%; `ind_industrial` 95,2% | `validation_baseline.md`. Critérios diferentes, explicados na nota do relatório |
| Intervalo entre os dois lotes de PNG antigos | 31 min (14:18 e 14:49 de 16/09) | auditoria §4.2 |
| `t_roadsigns_b` antigo: pixels fora das regiões | 64,74% (7 regiões, Fase 4) · **59,88%** (44 regiões, re-executado em 02/10, 923.567 px) | `validation_baseline.md`; `validate.py texture source/reference_ptbr/t_roadsigns_b.color_ptbr.png` |
| `t_roadsigns_b` antigo: ruído de alfa | 6.139 px (Fase 4) · **6.101 px** fora das 44 regiões, alfa mínimo 201 (re-executado) | idem |
| `t_roadsigns_b` antigo: deslocamento do octógono | borda esquerda x 1167 → **1177** (10 px; região UV de 126 px) | medido nesta fase sobre os PNG (máscara vermelha na janela x 1120–1330, y 200–400) |
| `eca_roadsigns_d`: pixels transparentes | 11,64% → 0% | `validation_baseline.md` (11,6% / 0,0% recalculados para a Figura 8) |
| `t_billboardsigns_dealers_b` | 13,94% de alfa 0 → 0%; 2.311 px com ruído (até 201) | `validation_baseline.md` |
| Ruído de alfa em todos os PNG antigos | mínimos 193–221 onde era 255 | auditoria §4.3 |

## 4. PoC e QA

| Dado | Valor | Fonte |
|---|---|---|
| DDS do PoC | BC7_UNORM_SRGB, 2048 × 1024, 12 mipmaps | `BEAMNG_OVERRIDE_POC.md` |
| Ferramentas do servidor MCP | 86 | `BEAMNG_MCP_CAPABILITIES.md` |
| Tempo de carga do mapa | ~70–85 s | idem |
| Resolução da captura | 1920 × 993 | `tests/presets/camera_defaults.json`; registrada em cada captura |
| Reprodutibilidade A×A2 / A×B | ver Tabela 4 do artigo | `t_roadsigns_automation_test.md` |
| Diferença A×B com nuvens padrão / vento 0 / céu limpo | 6,15 / 0,79 / 0,5–1,0 | idem |
| Deslocamento após restaurar a pose | 0 px | idem |
| Pontos de QA no catálogo (Fase 5) | 33 | `tests/qa_locations.json` |
| Elevação do sol nos presets | 40,66° (dia), −20° (noite) | `tests/presets/day.json`, `night.json` |

## 5. Localização

| Dado | Valor | Fonte |
|---|---:|---|
| Entradas da matriz | 308 | `LOCALIZATION_MASTER.csv` |
| Status na Fase 3 | 219 rule_defined · 46 preserve · 18 needs_impl. · 13 approved · 12 needs_context | CSV do commit `511b91e` |
| Status na Fase 4 | 219 · 47 · 18 · 13 · 11 | CSV do commit `0256004` (Firwood → preserve) |
| Status na Fase 5 | 184 rule_defined · 47 preserve · 40 qa_passed · 16 needs_impl. · 11 approved · 10 needs_context · 0 implemented | CSV do commit `70329b1` |
| Transições Fase 4 → 5 | 36 rule_defined → qa_passed; 2 approved_rule → qa_passed; 2 needs_impl. → qa_passed; 1 needs_context → rule_defined (Rush Rd) | comparação dos dois CSV |
| Escopo | 275 global · 18 caminho do East Coast · 15 west_coast_only | CSV, coluna `scope` |
| Uso no West Coast | 268 confirmed · 39 not_found · 1 likely | CSV, coluna `wcusa_usage` |
| Família `t_roadsigns` | 70 entradas: 40 qa_passed · 13 preserve · 17 pendentes (7 glifos compartilhados, 10 não usados) | CSV + `PHASE5_ROADSIGNS.md` |
| Revisão das antigas | 160 itens: 97 manter · 40 corrigir · 16 substituir · 7 investigar | `legacy_translation_review.md` |
| `traffic_signs.csv` | 119 linhas | arquivo |

## 6. Velocidades

| Dado | Valor | Fonte |
|---|---|---|
| Arestas do navgraph (original) | 9.337 | `speed_limits.md` §2 |
| Distribuição | 30: 3.292 · 40,2: 200 · 41,4: 1 · 43,2: 58 · 50: 674 · 56,3: 96 · 60: 2.579 · 80: 906 · 100: 1.049 · 120: 482 | idem |
| Arestas com valor herdado de mph | 355 (≈ 4%) | idem |
| Placas 5 mph | 37 instâncias de `sign_speed5.dae`, das quais **7** são placas (30 são decalques das baias) | `speed_limits.md`, "Atualização da Fase 5"; `r19_mesh_validation.md` |
| Placas 25 mph | 11 | idem |
| Limite ao lado das placas (original) | 5 mph: 30 km/h (34), 60 km/h (3) · 25 mph: 60 (9), 30 (2) | `speed_limits.md` §3 |
| Limites explícitos fora de múltiplo de 10 | 85 (Fase 4): 40,2 ×65 · 41,4 ×1 · 43,2 ×8 · 56,3 ×11 → **11** (Fase 5): 56,3 ×11 | `phase5_speed_delta.md` |
| Vias alteradas na Fase 5 | 101 (83 a 40 km/h; 18 a 10 km/h) | `PHASE5_ROADSIGNS.md` §3 |
| Detalhe das 83 vias a 40 | 74 explícitas herdadas (65 com 11,18; 8 com 12; 1 com 11,5) + 9 vistas por placa | idem |
| TSStatic com `shapeName` trocado | 7 | `working/speed/sign_instances.json` |
| Linhas alteradas por arquivo do nível | AIWaypoints 43 · DecalRoads 38 · island 8 · dock_aiRoads 12 · shapeName 1 + 2 + 4 | `PHASE5_ROADSIGNS.md` |
| `slotTraffic.json` | 939 linhas (630 por valor + 197 geometria 40 + 112 geometria 10; 243 faixas + 696 ligações); 28 faixas ignoradas | `slotTraffic_update.md` |
| Navgraph de controle | 13/13 PASS | `tests/reports/phase5_navgraph_check.json` |
| IA via de 40 | máx. 40,4 km/h, p90 39,5 (59 amostras) | `tests/reports/phase5_ai_test.json` |
| IA faixa de 10 | máx. 6,8 km/h (69 amostras) | idem |

## 7. Validador

| Dado | Fase 4 | Fase 5 (re-executado em 02/10) | Fonte |
|---|---|---|---|
| Self-test | 72/72 PASS | 75/75 PASS | `validate.py all` |
| Regressão | 10/10 | 10/10 | idem |
| Árvore do mod | 6 PASS, 1 WARN | 48/48 PASS | `validate.py mod --installed` |
| Assets novos | — | 24/24 PASS | `validate.py new` |
| Testes unitários | 33 | 44 OK | `python -m unittest discover -s tools/validation/tests` |
| Velocidade | 17 FAIL · 5 PASS · 7 SKIP | 13 FAIL · 9 PASS · 1 WARN · 7 SKIP | `validate.py all` (snapshot salvo) |
| Tolerância de múltiplo de 10 | 0,3 → 0,05 km/h | — | `validation_baseline.md` |

## 8. Produção da Fase 5

| Dado | Valor | Fonte |
|---|---|---|
| Regiões editadas (cor) | 44 | `allowed_regions.json` |
| Regiões editadas (opacidade) | 28 | idem |
| Pixels alterados (cor / opacidade) | 188.445 / 99.928, todos dentro das regiões | `PHASE5_ROADSIGNS.md` §1; re-executado (cor) |
| Pixels fora das regiões | 0 | idem |
| Malhas `.dae` do West Coast com o material `roadsigns` | 45 | `t_roadsigns_plan.md` §1 |
| Instâncias de `sign_stop.dae` | 52 | `t_roadsigns_plan.md` §2 |
| Limiar de cobertura UV | ≥ 40% | idem |
| R-19: textura / máscara | 512 × 1024 BC7 sRGB, 11 mips / BC4, cobertura 0,564 | `PHASE5_ROADSIGNS.md` §2 |
| Pixels de borda na cor da orla (anti-halo) | 1.904 | idem |
| Malhas R-19: triângulos e vértices | 10/20 (`sign_speed25`) · 8/16 (`sign_r19_10`), idênticos ao original | `r19_mesh_validation.md` |
| Decalques `roadmarkings1` no mapa | 1.388 | `main.decals.json` do zip do nível (contado nesta fase) |
| Distância BUS–ONLY / KEEP–CLEAR | 7,4 m / 11,4 m | `main.decals.json` (posições) |

## 9. Commits

| Fase | Commit | Data (−03:00) |
|---|---|---|
| 0 | `8d10748` | 30/09/2026 14:55 |
| 1 | `107e849` | 30/09/2026 15:40 |
| 2 | `50911d5` | 30/09/2026 16:28 |
| 3 | `511b91e` | 30/09/2026 17:10 |
| 4 | `0256004` | 30/09/2026 17:44 |
| 5 | `f83e4ce`, `8eb0dac`, `415b767`, `8e95239`, `ae07cee`, `70329b1` | 30/09 21:22 → 01/10 01:07 |
