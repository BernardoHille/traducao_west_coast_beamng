# Dados quantitativos do artigo final (v1.0.0)

Cada número do artigo, com a fonte. Consolidação em 21/10/2026, sobre a tag `v1.0.0` (`b4a7450`). Quando duas fontes discordavam, a discordância foi investigada e está explicada na coluna de observações. Os números marcados com **(re)** foram medidos de novo para esta edição.

## 1. Snapshot

| Dado | Valor | Fonte |
|---|---|---|
| Commit documentado | `b4a745082ef76fd511342b1f15ad88856f92b5dc` | `git rev-parse v1.0.0^{commit}`; igual a `origin/main` (`git ls-remote`, 21/10/2026) **(re)** |
| Commits no histórico | 36 | `git rev-list --count HEAD` **(re)** |
| Versão do mod | 1.0.0 | `mod/traducao_ptbr_wcusa/mod_info/traducao_ptbr_wcusa/info.json` |
| BeamNG.drive | 0.39.4.0 | `integrity.json` da instalação |
| ZIP | `traducao_ptbr_wcusa_v1.0.0.zip`, 29.846.362 bytes | `release/output/traducao_ptbr_wcusa_v1.0.0_manifest.txt` |
| SHA-256 do ZIP | `684bcf6c…3b57` | `release/output/traducao_ptbr_wcusa_v1.0.0.sha256`; `sha256sum` da cópia instalada para as capturas desta edição **(re)** |
| Publicação | tag e `main` no GitHub; GitHub Release `v1.0.0` não encontrada na API pública em 21/10/2026 | `git ls-remote`; `api.github.com/repos/…/releases/tags/v1.0.0` → 404 **(re)** |

## 2. Estado inicial e auditoria (Fases 0–3)

| Dado | Valor | Fonte / observação |
|---|---|---|
| Texturas originais | 35 (21 BC7 sRGB, 2 BC7, 3 BC4, 5 BC3, 4 BC1) | `docs/inventory/original_files_manifest.csv` |
| Contagem da auditoria | 41 | ocorrências nos zips, não texturas únicas (`texture_families.md`) |
| Traduções antigas | 13 PNG = 11 texturas + 1 máscara + 1 cópia idêntica | `PROJECT_STATUS.md`; auditoria §2 |
| Pixels alterados nas antigas | 25,9% a 77,8% (1:4, tol. 12) | auditoria §4.2; Tabela 2 do artigo |
| `t_roadsigns` antigo fora das regiões | 59,88% (44 regiões) | primeira edição, `DATA_SUMMARY.md` §3 |
| Deslocamento do octógono | x 1167 → 1177 (10 px) | idem |
| Alfa `eca_roadsigns_d` | 11,64% transparente → 0% | `tests/reports/validation_baseline.md` |
| Revisão textual das antigas | 160: 97 manter · 40 corrigir · 16 substituir · 7 investigar | `docs/localization/legacy_translation_review.md` |
| Ferramentas do MCP | 86 | `docs/BEAMNG_MCP_CAPABILITIES.md` |
| Matriz inicial | 308 linhas | CSV do commit `511b91e` |

## 3. Produção visual (Fases 5–6)

| Dado | Valor | Fonte |
|---|---|---|
| Regiões do atlas na Fase 5 | 44; 188.445 px dentro, 0 fora | `PHASE5_ROADSIGNS.md` |
| Tiles novos em `t_roadsigns` | 10 (Fase 6) + 19 (Fase 7) = 29 | `phase6/GLYPH_SIGNS.md`; `phase7/SPEED_PLATES.md` |
| Decalques de marcação no mapa | 1.388 | `phase6/ROADMARKINGS.md` |
| Override de `main.decals.json` | 9 instâncias removidas, 6 `rectIdx` trocados | idem; `decal_overrides.py --check` **(re)** |
| Outdoors com QA | 14 | `phase6/BILLBOARDS_DEALERS.md` |
| Elementos `clutter_commercial` | 85 (188 malhas instanciadas) | `phase6/COMMERCIAL.md` |
| Paradas no mapa de ônibus | 23 | `phase6/BUS_TRANSPORT.md` |
| Malhas de glifos reescritas | 25 | `phase6/GLYPH_SIGNS.md`; contagem em `mod/` **(re)**: 32 `.dae` = 24 só de glifos + `roadsigns.dae` (glifos dos pórticos e, na Fase 7, placas embutidas) + 4 R-19 + `sign_speed25` + 2 cabines |
| Motel: quadriláteros | 46 → 54 (total da malha); 20 → 28 (linhas de texto) | `glyph_signs.read_quads` **(re)**; `GLYPH_SIGNS.md` |
| DDS no mod ao fim da Fase 6 | 28 | `PHASE6_VISUAL_PRODUCTION.md` |
| Pontos de QA da Fase 6 | 170 (84 textura + 86 glifos) | idem; `tests/qa_locations.json` = 203 **(re)** |

## 4. Matriz de localização (1.0.0)

| Dado | Valor | Fonte / observação |
|---|---|---|
| Linhas | 323 | `LOCALIZATION_MASTER.csv` na tag **(re)** |
| Status | 164 qa_passed · 92 rule_defined · 47 preserve · 11 implemented · 7 approved_rule · 1 needs_context · 1 needs_implementation | idem **(re)** |
| Uso no West Coast | 216 confirmed · 1 likely · 106 not_found | idem **(re)** |
| Linhas usadas e abertas | 0 | cruzamento status × uso **(re)**. O "0 needs_context" de `COVERAGE_AUDIT.md` é por classe de uso; por status há 1 `needs_context` e 1 `needs_implementation`, ambos `not_found` (atlas do East Coast e de Utah) |
| `traffic_signs.csv` | 119 linhas de dados | arquivo (120 com cabeçalho) **(re)** |

## 5. Velocidades e camada funcional (Fases 5 e 7)

| Dado | Valor | Fonte / observação |
|---|---|---|
| Arestas do navgraph, original | 9.337 | dump do jogo com o ZIP desativado, `figures/raw/navgraph_edges__off.json` **(re)**; igual a `speed_limits.md` §2 (Fase 3) |
| Distribuição original | 30: 3.292 · 40,2: 200 · 41,4: 1 · 43,2: 58 · 50: 674 · 56,3: 96 · 60: 2.579 · 80: 906 · 100: 1.049 · 120: 482 | idem **(re)** |
| Arestas na 1.0.0 | 9.338 | dump com o ZIP ativo **(re)**. A aresta a mais é a divisão em `Bridge30_1`, no fim da zona de 50 (diferença de limite entre DR312 e Bridge30) |
| Distribuição 1.0.0 | 10: 94 · 30: 3.227 · 40: 398 · 50: 668 · 60: 2.519 · 70: 13 · 80: 903 · 100: 1.046 · 120: 470 | idem **(re)** |
| Arestas com limite alterado | 598 | comparação geométrica on × off **(re)**; por nome de nó seriam 559, mas os nomes `autojunction_N` mudam entre cargas |
| Vias da Fase 5 | 101 (83 a 40, 18 a 10) | `PHASE5_ROADSIGNS.md` |
| Vias da Fase 7 | 8 a 60, 1 a 70, 1 a 50, 1 a 120 explícito, 5 faixas a 40 | `phase7/SPEED_LIMITS.md` |
| Linhas de nível alteradas | 132 (101 + 7 `shapeName` + 24) + 15 objetos | `apply_phase7_functional.py --check` **(re)** |
| Objetos novos | grupo `ptbr_functional_signs` + 14 (7 placas + 7 postes) | idem; jogo: grupo com 14 objetos (`release_smoke.json`) |
| `slotTraffic.json` | 1.109 linhas (939 + 170); 0 valores de mph | `phase7/SLOTTRAFFIC.md` |
| Placas embutidas | 23 regulamentares + 24 advertências | `phase7/SPEED_PLATES.md` |
| Radares | 2 → 70; 3, 5, 6, 7 → 60; 4 → 100 | `working/functional/radar_changes.json` |
| Zonas | 3 do mapa + 4 de missão | `phase7/ZONES_AND_MISSIONS.md` |
| Missões arrive | 6, inativas (SKIP) | `validate.py speeds` |
| IA (Fase 7) | 7 casos PASS | `tests/reports/phase7/ai_qa.md` |
| Radares (Fase 7 / Fase 9) | 18/18 / 7 passagens conforme a regra | `radar_test.json`; `release_smoke.json` |
| Speed Alert | alerta a 53,9 e 54,5; desliga a 42,3 e 42,7 km/h | `tests/reports/phase7/adas_qa.md` |
| Event 01 | sem alerta a 65/69 (máx. 68,4); alerta a 70,8; rearme a 64,8; 2º alerta a 70,0 | idem |

## 6. Validação

| Dado | Fase 4 | Fase 5 | Fase 6 | Fase 7 | Fase 9 (1.0.0) | Fonte |
|---|---|---|---|---|---|---|
| FAIL de velocidade | 17 | 13 | 13 | 0 | 0 | `validation_baseline.md`; primeira edição; `PHASE6…md`; `speed_after.md`; `RC_VALIDATION.md` |
| selftest | 72 | 75 | 121 | 121 | 121 | idem |
| regression | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | idem |
| mod / mod --installed | 6 + 1 WARN (`mod`) | 48 | 217 | 273 / 274 | 273 / 274 | idem |
| new | — | 24 | 75 | 108 | 108 | idem |
| unittest | 33 | 44 | 44 | 59 | 63 | idem |
| speeds (1.0.0) | | | | 27 PASS · 1 WARN · 7 SKIP | 27 · 1 · 7 | `RC_VALIDATION.md` |

## 7. QA visual

| Dado | Valor | Fonte |
|---|---|---|
| Pontos no catálogo | 3 (Fase 2) → 33 (Fase 5) → 203 (Fase 6) | `t_roadsigns_automation_test.md`; primeira edição; `tests/qa_locations.json` **(re)** |
| Capturas guardadas | 627 no total: poc 4, baseline 4, current 4, phase5 79, phase6 365, phase7 133, release 38 | contagem em `tests/screenshots/` **(re)** |
| Capturas da Fase 6 à noite | 22 | `PHASE6_VISUAL_PRODUCTION.md` |
| Runs de QA (relatórios JSON) | 159 | `tests/reports/**/runs/*.json` **(re)** |
| Capturas novas desta edição | 18 PNG (14 usadas em figuras; 4 sem uso, mantidas: `chinatown_street` com a placa fora do quadro, `chinatown_driver_b`, `aerial_downtown`, `decal_stop_chinatown_oblique__on_night`) + 2 dumps do navgraph | `figures/raw/capture_log.json` (18 registros) |

## 7a. Fase 8

| Dado | Valor | Fonte |
|---|---|---|
| Versão testada | 0.7.0 (`1973cdb`) | `docs/production/PHASE8_GLOBAL_QA.md` |
| Testadores | externos, anônimos; número e perfil **não registrados** | idem |
| Resultado | sem problemas bloqueadores reportados | idem |

## 8. Release (Fase 9)

| Dado | Valor | Fonte |
|---|---|---|
| Arquivos | 117 = 116 runtime + 1 metadado | manifesto; `SCOPE_AUDIT.md` |
| Por tipo | 31 DDS · 32 DAE · 32 CDAE · 1 materials · 20 JSON · 1 mod_info | `traducao_ptbr_wcusa_v1.0.0_build.json` |
| DDS por formato | 17 BC7 sRGB · 1 BC7 · 9 BC4 · 4 BC5 | `dds_parser.parse` sobre `mod/` **(re)** |
| Overrides / novos / idênticos | 100 / 16 / 0 | `build_release.py` |
| Arquivos de texto auditados | 54 | idem |
| Tamanho descompactado | 98.973.556 bytes | manifesto. O `PRE_RELEASE_SNAPSHOT.md` registra 98.973.589 bytes para a 0.7.0; a diferença de 33 bytes é o `info.json` (494 bytes na cópia de trabalho da 0.7.0, 461 na 1.0.0) **(re)** |
| Builds com o mesmo SHA | 4 (`ac2ddf6`, `896fa36` ×2, `b4a7450`) | `BUILD_1.0.0.md`; sessão da Fase 9 |
| VFS com o ZIP ativo / desativado | 116/116 / 0/116 | `tests/reports/release/release_smoke.json` |
| Navgraph no teste do ZIP | 19/19 pontos | idem |
| `.cdae` do pacote no cache | 0 | `RC_VALIDATION.md`; conferido de novo depois das capturas desta edição **(re)** |

## 9. Discordâncias investigadas

1. **41 × 35 texturas:** ocorrências × arquivos únicos (seção 5.2 do artigo).
2. **9.337 × 9.338 arestas:** a divisão `Bridge30_1` no fim da zona de 50.
3. **559 × 598 arestas alteradas:** comparação por nome de nó × por geometria; os nomes automáticos mudam entre cargas, e a geométrica é a usada.
4. **"0 needs_context" (Fase 6) × 1 `needs_context` na matriz:** classe de uso × status; a linha é de um atlas do East Coast, sem uso no West Coast.
5. **98.973.589 × 98.973.556 bytes:** 0.7.0 × 1.0.0, diferença do `info.json`.
6. **Série "mod" do validador:** a Fase 4 usou `mod` (sem cópia instalada); a partir da Fase 5 os números citados são de `mod --installed`, e a Fase 7 registra os dois (273 / 274).
7. **Capturas de ADAS do teste de release:** `RC_VALIDATION.md` cita `tests/screenshots/release/on/adas/`. Inspecionadas para esta edição, essas duas imagens mostram o menu principal do jogo sobre a cena. Não servem como evidência visual; o resultado funcional daquele teste veio dos contadores do cenário. Registro feito como errata no próprio relatório.
