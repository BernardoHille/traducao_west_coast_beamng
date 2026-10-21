# Índice de figuras — artigo final (v1.0.0)

38 figuras:
- **7 reutilizadas sem alteração** da primeira edição;
- **13 diagramas e gráficos** gerados de dados, incluindo o mapa do navgraph;
- **15 composições de capturas reais** do jogo;
- **3 figuras de textura ou render offline** de malha.

Todas são geradas por `docs/article_final/tools/build_figures_final.py`; nenhuma usa edição generativa. As capturas novas desta edição estão em `figures/raw/` (imutável), registradas em `figures/raw/capture_log.json` com pose de câmera, mods ativos e origem VFS.

Legenda dos estados:
- **ZIP on / off:** só o pacote `traducao_ptbr_wcusa_v1.0.0.zip` instalado, ativo ou desativado (21/10/2026);
- **dev on / off:** cópia de desenvolvimento do mod (fases anteriores);
- **original:** mod desligado.

Mapa sempre West Coast USA, BeamNG.drive 0.39.4.0. As câmeras "catálogo" são poses de `tests/qa_locations.json`; "custom" são poses de `capture_final.py` (ou de `docs/article/tools/capture_article.py`).

## Figuras reutilizadas da primeira edição

| ID | Arquivo final | source_article_figure | original_file | Estado | Commit da figura |
|---|---|---|---|---|---|
| 3 | `figures/validation/heatmap_legacy_vs_phase5.jpg` | Figura 2 | `docs/article/figures/validation/fig_02_heatmap_t_roadsigns_legacy_vs_phase5.jpg` | heatmaps do validador: referência antiga × atlas da Fase 5 | `56f37b2` (conteúdo da Fase 5, `70329b1`) |
| 4 | `figures/textures/stop_uv_region_zoom.png` | Figura 4 | `…/textures/fig_04_stop_uv_region_zoom.png` | atlas original, antigo e Fase 5 | `56f37b2` |
| 5 | `figures/textures/alpha_loss_legacy.png` | Figura 8 | `…/textures/fig_08_alpha_loss_legacy.png` | alfa dos originais e das traduções antigas | `56f37b2` |
| 7 | `figures/comparisons/poc_override_on_off_on.jpg` | Figura 7 | `…/comparisons/fig_07_poc_override_on_off_on.jpg` (de `tests/screenshots/poc/`, 30/09/2026) | PoC Fase 1, ON/OFF/ON | `56f37b2` (capturas `107e849`) |
| 10 | `figures/textures/roadmarkings_atlas_slots.png` | Figura 9 | `…/textures/fig_09_roadmarkings_atlas_slots.png` | atlas original das marcações, estado da Fase 5 | `56f37b2` |
| 15 | `figures/textures/r19_texture_and_mask.png` | Figura 17 | `…/textures/fig_17_r19_texture_and_mask.png` | asset R-19 da Fase 5 | `56f37b2` |
| 17 | `figures/validation/port_bay_plate_side_effect.jpg` | Figura 18 | `…/validation/fig_18_port_bay_plate_side_effect.jpg` (de `tests/screenshots/phase5/`) | resultado negativo da Fase 5 | `56f37b2` |

## Todas as figuras

| ID | Arquivo final | Fonte / raw | Data das capturas | Estado | Câmera | Objetivo | Anotações |
|---|---|---|---|---|---|---|---|
| 1 | `figures/final/opening_chinatown_v100.jpg` | `raw/chinatown_driver_a__on_opening.png` | 21/10/2026 | ZIP on, dia | custom `chinatown_driver_a` (pos −699,5; 534,5; 122,4 → −712,4; 550,0; 121,0; FOV 55) | abertura: PARE na placa e no pavimento | 2 rótulos e 2 setas sobre cópia |
| 2 | `figures/diagrams/problem_expansion.svg` | — | — | — | — | expansão do problema | diagrama |
| 3 | ver tabela acima | | | | | auditoria: onde a imagem mudou | |
| 4 | ver tabela acima | | | | | deslocamento UV do STOP | |
| 5 | ver tabela acima | | | | | perda de alfa | |
| 6 | `figures/diagrams/vfs_override_release.svg` | números de `tests/reports/release/release_smoke.json` | — | — | — | VFS com o ZIP de release | diagrama |
| 7 | ver tabela acima | | | | | PoC ON/OFF/ON | |
| 8 | `figures/comparisons/stop_original_poc_v100.jpg` | `raw/roadsigns_chinatown_stop__off_day.png`; `docs/article/figures/raw/roadsigns_chinatown_stop__poc.png` (02/10/2026, 1920 × 993); `raw/roadsigns_chinatown_stop__on_day.png` | 21/10 e 02/10/2026 | ZIP off / PoC / ZIP on | catálogo `roadsigns_chinatown_stop` | STOP original, PoC, 1.0.0 | enquadramento comum 1765 × 993; recorte (513, 280, 1253, 920) |
| 9 | `figures/diagrams/qa_state_protocol.svg` | — | — | — | — | protocolo de troca de estado e cache | diagrama |
| 10 | ver tabela acima | | | | | atlas e uso das marcações | |
| 11 | `figures/textures/roadmarkings_opacity_original_v100.png` | `source/originals/png/decalroad/t_decal_roadmarkings_o.data.png`; `working/png/t_decal_roadmarkings_o.data.png` | — | textura | — | a letra está na opacidade | grade 4 × 4 desenhada |
| 12 | `figures/diagrams/reproducible_master.svg` | — | — | — | — | master reproduzível | diagrama |
| 13 | `figures/comparisons/r2_original_legacy_v100.jpg` | `raw/roadsigns_downtown_yield__off_day.png`; `docs/article/figures/raw/roadsigns_downtown_yield__poc.png` (02/10); `raw/roadsigns_downtown_yield__on_day.png` | 21/10 e 02/10/2026 | ZIP off / referência antiga / ZIP on | catálogo `roadsigns_downtown_yield` | R-2 | enquadramento comum; recorte (543, 170, 1223, 790) |
| 14 | `figures/diagrams/speed_conversion_chain_v100.svg` | `working/*/speed_changes.json` | — | — | — | conversão e tabela final | diagrama |
| 15 | ver tabela acima | | | | | asset R-19 | |
| 16 | `figures/textures/r19_values_10_to_120.png` | `working/png/r19/t_r19_{10,40,50,70,120}_b.color.png` | — | textura | — | R-19 distribuídos | recorte em torno do disco e correção para a proporção física |
| 17 | ver tabela acima | | | | | placas de baia (resultado negativo) | |
| 18 | `figures/comparisons/roadmarkings_ingame_original_v100.jpg` | `raw/decal_keep_clear_top__{off,on}_day.png`; `docs/article/figures/raw/decal_bus_only_top__original.png` (02/10); `raw/decal_bus_only_top__on_day.png`; `raw/decal_stop_chinatown_oblique__{off,on}_day.png` | 21/10 e 02/10/2026 | ZIP off/on; original | custom (poses da primeira edição) | marcações no pavimento | enquadramento comum |
| 19 | `figures/comparisons/fuel_pump_original_day_night.jpg` | `tests/screenshots/phase6/eca_genericsigns/gs_octane_pump_original.jpg`; `tests/screenshots/release/on/gs_octane_pump_{day,night}.jpg` | 06/10 e 21/10/2026 | original; ZIP on | catálogo `gs_octane_pump` | posto de dia e de noite | enquadramento comum; recorte central |
| 20 | `figures/comparisons/billboard_turbo_burger.jpg` | `phase6/t_billboards/bb_turbo_burger_original.jpg`; `release/on/bb_turbo_burger_{day,night}.jpg` | 06/10 e 21/10/2026 | original; ZIP on | catálogo `bb_turbo_burger` | outdoor | — |
| 21 | `figures/comparisons/industry_original_v100.jpg` | `phase6/{ind_industrial_signs,t_spearleaf_refinery_logo,t_steel_factory_brand}/*_original.jpg`; `release/on/*_day.jpg` | 06/10 e 21/10/2026 | original; ZIP on | catálogo `ind_in_flam_no`, `t_spea_refinery`, `t_stee_steel_descriptor` | indústria | — |
| 22 | `figures/comparisons/transport_bus_map.jpg` | `phase6/t_bus_routes_wca/bus_map_shelter_original.jpg`; `release/on/bus_map_shelter_day.jpg`; `phase6/glyph_signs/gl_s_busstop_wcu_mapa_{original,ptbr}.jpg` | 06/10 e 21/10/2026 | original; ZIP on; dev on | catálogo | transporte | — |
| 23 | `figures/comparisons/commercial_neon_lemon.jpg` | `phase6/clutter_commercial/cc_neon_nails_original_night.jpg`; `release/on/cc_neon_nails_night.jpg`; `phase6/clutter_commercial/cc_lemon_{original,ptbr}.jpg` | 06/10 e 21/10/2026 | original; ZIP on; dev on | catálogo | comércio | — |
| 24 | `figures/textures/glyph_sign_motel_explained.png` | malhas `source/originals/meshes/phase6/…/s_motel_sign.dae` e `mod/…/s_motel_sign.dae`; atlas original e PT-BR | — | render offline | vista frontal calculada da malha | como funciona um letreiro de glifos | contornos das células em ciano |
| 25 | `figures/comparisons/glyph_signs_examples.jpg` | `phase6/glyph_signs/gl_{motel_sign_motel,food_mart_sign_001_delifoodmart,roadsigns_rs_frac_half_0_9}_{original,ptbr}.jpg` | 06/10/2026 | original; dev on | catálogo `gl_*` | exemplos de glifos | — |
| 26 | `figures/diagrams/final_architecture.svg` | números do build e da Fase 7 | — | — | — | arquitetura final | diagrama |
| 27 | `figures/functional/navgraph_histogram_original_v100.svg` | `raw/navgraph_edges__{off,on}.json` | 21/10/2026 | ZIP off/on | — | distribuição de limites | gráfico |
| 28 | `figures/functional/speed_map_navgraph_v100.png` | `raw/navgraph_edges__{on,off}.json`; pontos de `working/functional/navgraph_matrix.py` | 21/10/2026 | ZIP on | vista de cima calculada (norte para cima) | mapa funcional de velocidades | desenhado das arestas; legenda e rótulos |
| 29 | `figures/comparisons/speed_limit_to_r19.jpg` | `raw/r19_40_hill__{off,on}_day.png`; `tests/screenshots/phase7/speed_plates/{reg_02,adv_00}_{original,ptbr}.jpg` | 21/10 e 13/10/2026 | ZIP off/on; dev off/on | catálogo `r19_40_hill`; poses de `plate_shots.py` | SPEED LIMIT → R-19 | recorte (590, 0, 1110, 993) |
| 30 | `figures/functional/toll_booth_original_v100.jpg` | `tests/screenshots/phase7/toll_booth/toll_booth_close_{original,ptbr}.jpg` | 13/10/2026 | dev off/on | pose de `look.py` | cabine de pedágio | — |
| 31 | `figures/functional/radar_trigger_chart.svg` | `tests/reports/phase7/radar_test.json`; `tests/reports/release/release_smoke.json` | 07–13/10 e 21/10/2026 | dev on; ZIP on | — | radares | gráfico |
| 32 | `figures/functional/adas_speed_alert_event01.jpg` | `phase7/adas/speed_alert_spawn.jpg`; `release/on/signs/r19_50_spawn_left.jpg`; `phase7/adas/mod_{off,on}_event01_entry.jpg` | 13/10 e 21/10/2026 | dev on/off; ZIP on | visão do motorista; poses de `sign_shots.py` e `mod_off_check.py` | ADAS 50 e Event 01 | as capturas de release do Speed Alert não foram usadas (menu do jogo sobre a cena; ver `METHODOLOGY_NOTES_FINAL.md`) |
| 33 | `figures/diagrams/qa_pipeline_final.svg` | — | — | — | — | pipeline final | diagrama |
| 34 | `figures/validation/validator_progress_by_phase.svg` | relatórios de cada fase (`DATA_SUMMARY_FINAL.md` §6) | — | — | — | progressão do validador | gráfico |
| 35 | `figures/qa/qa_coverage_growth.svg` | `tests/qa_locations.json`; contagem de `tests/screenshots/` | — | — | — | crescimento do QA visual | gráfico |
| 36 | `figures/release/release_pipeline_v100.svg` | `release/output/…_build.json`; `release_smoke.json` | — | — | — | engenharia da release | diagrama |
| 37 | `figures/release/mod_off_on_reversibility.jpg` | `raw/{chinatown_driver_a,r19_40_hill,decal_keep_clear_top}__off_day.png` e `__on_{opening,day}.png` | 21/10/2026 | ZIP off/on | custom e catálogo | reversibilidade | enquadramento comum; recortes |
| 38 | `figures/final/chinatown_day_night_v100.jpg` | `raw/chinatown_driver_a__on_opening.png`; `raw/chinatown_driver_a__on_night.png` | 21/10/2026 | ZIP on, dia e noite | custom `chinatown_driver_a` | dia e noite | recorte (430, 200, 1450, 760) do quadro comum |

## Capturas novas não usadas

Mantidas em `raw/` (imutável):
- `chinatown_street__on_day.png`: a placa ficou fora do quadro;
- `chinatown_driver_b__on_opening.png`: candidata de abertura não escolhida;
- `aerial_downtown__on_day.png`;
- `decal_stop_chinatown_oblique__on_night.png`.

## Reprodução

```bash
python docs/article_final/tools/capture_final.py on day          # e: on opening, on night, off day, navgraph on, navgraph off
python docs/article_final/tools/build_figures_final.py           # todas as figuras (ou nomes específicos)
```
