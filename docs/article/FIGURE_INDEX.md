# Índice de figuras

Todas as figuras são geradas por `docs/article/tools/build_figures.py`, a partir de capturas reais do jogo, de texturas do projeto ou de relatórios do validador. As capturas novas (`figures/raw/`) foram feitas por `docs/article/tools/capture_article.py` em 02/10/2026. O registro de cada captura (pose de câmera lida do jogo, estado do mod e origem VFS do atlas) está em `figures/raw/capture_log.json`.

**Regras seguidas:**
- os arquivos em `raw/` nunca são editados;
- anotações e recortes são feitos em cópias, com Pillow (caixas, círculos, setas, rótulos, composição lado a lado);
- não houve edição generativa;
- recortes não redimensionam a evidência, exceto quando indicado (heatmaps, atlas do alfa e miniatura de inset).

**Ambiente comum das capturas novas:**
- BeamNG.drive 0.39.4.0 (Direct3D 12), mapa `west_coast_usa`, janela 1920 × 993;
- preset `day` (`windSpeed 0`, `cloudCover 0`, sol a 40,66°), interface oculta;
- antes de cada estado, carga de `smallgrid` seguida de `west_coast_usa`.

---

### Figura 1: Vista aérea do West Coast
- **Arquivo:** `figures/aerial/fig_01_wcusa_aerial_annotated.jpg`
- **Raw:** `figures/raw/aerial_downtown__original.png` (também existe `aerial_downtown__ptbr.png`, não usado)
- **Fonte:** captura MCP (`screenshot`), câmera livre em (−420; 330; 760), apontada para baixo, norte para cima, FOV vertical 50°
- **Estado do mod:** desligado (original)
- **Local:** centro de Belasco e Chinatown
- **Objetivo:** situar os pontos de teste
- **Anotada:** sim. Seis marcadores numerados, seta de norte e escala aproximada de 100 m. Posições das esferas de depuração em `docs/article/tools/annotation_points.json` (erro de projeção ≤ 6 px)

### Figura 2: Heatmaps do validador
- **Arquivo:** `figures/validation/fig_02_heatmap_t_roadsigns_legacy_vs_phase5.jpg`
- **Raw:** `export/reports/validation/images/t_roadsigns_b.color_ptbr_diff.png` e `t_roadsigns_b.color_diff.png` (gerados em 02/10/2026; fora do Git, regeneráveis)
- **Fonte:** `validate.py texture` sobre `source/reference_ptbr/t_roadsigns_b.color_ptbr.png` (A) e `working/png/t_roadsigns_b.color.png` (B)
- **Estado do mod:** não se aplica (arquivos)
- **Objetivo:** mostrar onde a referência antiga mudou pixels, comparado com a Fase 5
- **Anotada:** só os títulos. As imagens foram reduzidas de 2048 para 1400 px de largura

### Figura 3: Atlas `t_roadsigns` com regiões
- **Arquivo:** `figures/textures/fig_03_atlas_roadsigns_regions.jpg`
- **Raw:** `source/originals/png/t_roadsigns_b.color.png` (local, fora do Git; SHA-256 no manifesto)
- **Fonte:** regiões de `tools/validation/config/allowed_regions.json` (44) e áreas compartilhadas do inventário UV em `docs/production/t_roadsigns_plan.md`
- **Objetivo:** explicar o atlas, as regiões editáveis e os glifos compartilhados
- **Anotada:** sim (retângulos por categoria, rótulos e legenda)

### Figura 4: Zoom da região STOP no atlas
- **Arquivo:** `figures/textures/fig_04_stop_uv_region_zoom.png`
- **Raw:** PNG original, `source/reference_ptbr/t_roadsigns_b.color_ptbr.png` e `working/png/t_roadsigns_b.color.png`
- **Fonte:** recorte x 1134–1320, y 201–387, ampliado 3× sem interpolação; contorno ciano = UV x 1164–1290, y 231–358
- **Objetivo:** mostrar o deslocamento de 10 px do octógono na referência antiga
- **Anotada:** sim (contorno UV)

### Figura 5: STOP em Chinatown (A/B/C)
- **Arquivo:** `figures/comparisons/fig_05_stop_chinatown_A_B_C.jpg`
- **Raw:** `figures/raw/roadsigns_chinatown_stop__original.png`, `__poc.png`, `__ptbr.png`
- **Fonte:** captura MCP na pose de catálogo `roadsigns_chinatown_stop` (`tests/qa_locations.json`)
- **Estado do mod:**
  - A: desligado;
  - B: estado PoC temporário. A cópia **instalada** recebeu o DDS `export/dds/poc/t_roadsigns_b.color.dds` e ficou sem o `_o.data` novo; foi restaurada logo depois por `install_mod.py`, e `validate.py mod --installed` deu PASS 48/48;
  - C: ligado, commit `70329b1`.
- **Local:** placa `sign_stop.dae` em (−712,667; 552,899; 122,435)
- **Objetivo:** original × PoC defeituoso × definitivo na mesma câmera
- **Anotada:** não (só recorte x 590–1330, y 280–920 e rótulos)

### Figura 6: Diagrama do VFS
- **Arquivo:** `figures/pipeline/fig_06_vfs_override.svg`
- **Fonte:** diagrama gerado pelo script, com base em `BEAMNG_OVERRIDE_POC.md` e nos resultados de `file_info`
- **Anotada:** não se aplica

### Figura 7: PoC ON/OFF/ON (Fase 1)
- **Arquivo:** `figures/comparisons/fig_07_poc_override_on_off_on.jpg`
- **Raw:** `tests/screenshots/poc/roadsigns_mod_on.png`, `roadsigns_mod_off.png`, `roadsigns_mod_on_again.png` (capturas originais de 30/09/2026)
- **Estado do mod:** ligado, desligado e religado (Fase 1, com a referência antiga como marcador)
- **Local:** mesma placa da Figura 5. A câmera da Fase 1 é parecida, mas não idêntica, à de catálogo
- **Objetivo:** evidência histórica do PoC
- **Anotada:** não (recorte x 600–1380, y 290–930)

### Figura 8: Perda de alfa
- **Arquivo:** `figures/textures/fig_08_alpha_loss_legacy.png`
- **Raw:** `source/originals/png/eca_roadsigns_d.png`, `t_billboardsigns_dealers_b.color.png` e os `_ptbr` correspondentes em `source/reference_ptbr/`
- **Fonte:** canal alfa extraído e reduzido para 640 px de largura. As porcentagens foram calculadas sobre os arquivos completos
- **Objetivo:** mostrar o recorte perdido
- **Anotada:** títulos e borda cinza

### Figura 9: Atlas das marcações de asfalto
- **Arquivo:** `figures/textures/fig_09_roadmarkings_atlas_slots.png`
- **Raw:** `source/originals/png/t_decal_roadmarkings_b.color.png`
- **Fonte:** grade de `managedDecalData.json` (4 × 4) e contagem de `rectIdx` em `levels/west_coast_usa/main.decals.json`, ambos lidos do zip do jogo só por leitura. A tradução de cada slot vem de `LOCALIZATION_RULES.md` §12
- **Objetivo:** mostrar que o pavimento usa palavras soltas
- **Anotada:** sim (faixa com índice, contagem e regra)

### Figura 10: BUS ONLY e KEEP CLEAR vistos de cima
- **Arquivo:** `figures/aerial/fig_10_roadmarkings_top_view.jpg`
- **Raw:** `figures/raw/decal_bus_only_top__original.png`, `decal_keep_clear_top__original.png`
- **Fonte:** câmera livre apontada para baixo, a ~22 m sobre (−445,7; 499,0) e (−335,4; 477,9)
- **Estado do mod:** desligado
- **Objetivo:** composição das frases no pavimento
- **Anotada:** sim. Círculos e rótulos; BUS e CLEAR na posição medida com esfera de depuração; ONLY e KEEP colocados sobre a palavra visível, porque a esfera ficou sob a superfície. Distâncias calculadas do `main.decals.json`

### Figura 11: Pipeline de QA
- **Arquivo:** `figures/pipeline/fig_11_qa_pipeline.svg`
- **Fonte:** `docs/WORKFLOW.md`
- **Anotada:** não se aplica

### Figura 12: Ponto de QA visto de cima
- **Arquivo:** `figures/final/fig_12_qa_point_chinatown_top.jpg`
- **Raw:** `figures/raw/qa_context_top__ptbr.png`. O *inset* é `roadsigns_chinatown_stop__ptbr.png`, reduzido para 576 px
- **Fonte:** câmera livre a 139 m de altitude sobre o cruzamento
- **Estado do mod:** ligado
- **Objetivo:** explicar a reprodutibilidade (pose fixa, objeto e câmera)
- **Anotada:** sim. Posições da placa e da câmera medidas com esfera de depuração; cunha de visada horizontal de ~84°
- **Observação:** uma primeira tentativa de vista lateral, de (−700,4; 559,8; 128), ficou dentro de um prédio. A captura foi descartada e o descarte está registrado em `capture_log.json`

### Figura 13: Conversão de velocidade
- **Arquivo:** `figures/pipeline/fig_13_speed_conversion.svg`
- **Fonte:** `LOCALIZATION_RULES.md` §2
- **Anotada:** não se aplica

### Figura 14: Distribuição do navgraph
- **Arquivo:** `figures/validation/fig_14_navgraph_speed_distribution.svg`
- **Fonte:** `docs/inventory/speed_limits.md` §2 (consulta `map.getMap()` via MCP, Fase 3)
- **Anotada:** não se aplica

### Figura 15: Placa → lógica
- **Arquivo:** `figures/pipeline/fig_15_sign_to_logic.svg`
- **Fonte:** `speed_dependencies.md` §1 e resultados da Fase 5
- **Anotada:** não se aplica

### Figura 16: YIELD / R-2 (A/B/C)
- **Arquivo:** `figures/comparisons/fig_16_yield_r2_A_B_C.jpg`
- **Raw:** `figures/raw/roadsigns_downtown_yield__original.png`, `__poc.png`, `__ptbr.png`
- **Fonte:** pose de catálogo `roadsigns_downtown_yield`
- **Estado do mod:** como na Figura 5
- **Anotada:** não (recorte x 620–1300, y 170–790)

### Figura 17: Textura e máscara do R-19
- **Arquivo:** `figures/textures/fig_17_r19_texture_and_mask.png`
- **Raw:** `working/png/r19/t_r19_40_b.color.png`, `t_r19_10_b.color.png`, `t_r19_o.data.png` (saídas de `build_r19.py`, fora do Git e regeneráveis; os DDS correspondentes estão em `export/dds/r19/`)
- **Objetivo:** mostrar o asset próprio e o recorte por alphaTest 128
- **Anotada:** títulos e nota

### Figura 18: Efeito colateral nas placas das baias
- **Arquivo:** `figures/validation/fig_18_port_bay_plate_side_effect.jpg`
- **Raw:** `tests/screenshots/phase5/roadsigns_ptbr_r19/port_bay_plate_side_effect_original_vs_inplace_override.jpg` e `port_bay_plate_after_fix_original_vs_mod.jpg` (composições lado a lado feitas na Fase 5)
- **Estado do mod:** original | mod com substituição no mesmo caminho (A); original | mod corrigido (B)
- **Anotada:** só os títulos

### Figura 19: R-19 40 e 10 no jogo
- **Arquivo:** `figures/comparisons/fig_19_r19_40_and_10_ingame.jpg`
- **Raw:** `figures/raw/r19_40_hill__original.png`, `__ptbr.png`, `r19_10_downtown_parking__original.png`, `__ptbr.png`
- **Fonte:** poses de catálogo `r19_40_hill` e `r19_10_downtown_parking`
- **Estado do mod:** desligado (A, C) e ligado (B, D)
- **Anotada:** não (recortes de altura inteira)

### Figura 20: Pórtico do pedágio
- **Arquivo:** `figures/comparisons/fig_20_gantry_toll_plaza.jpg`
- **Raw:** `tests/screenshots/phase5/t_roadsigns/roadsigns_toll_plaza_original.jpg` e `_ptbr.jpg` (QA da Fase 5; JPEG q92 das capturas PNG originais, run reports em `tests/reports/runs/`)
- **Estado do mod:** desligado / ligado
- **Anotada:** não (recorte x 400–1580, y 360–640)

### Figura 21: PARE com STOP no pavimento
- **Arquivo:** `figures/final/fig_21_pare_sign_with_stop_pavement.jpg`
- **Raw:** `figures/raw/decal_stop_chinatown_oblique__ptbr.png`
- **Estado do mod:** ligado
- **Objetivo:** mostrar o limite atual (pavimento ainda não produzido)
- **Anotada:** sim (posições medidas com esfera de depuração)

---

## Capturas raw desta fase (não editadas)

| Arquivo | Estado | Usada em |
|---|---|---|
| `aerial_downtown__original.png` | original | Fig. 1 |
| `aerial_downtown__ptbr.png` | ptbr | — (contexto) |
| `roadsigns_chinatown_stop__original/poc/ptbr.png` | 3 estados | Fig. 5; *inset* da Fig. 12 |
| `roadsigns_downtown_yield__original/poc/ptbr.png` | 3 estados | Fig. 16 |
| `r19_40_hill__original/ptbr.png` | 2 estados | Fig. 19 |
| `r19_10_downtown_parking__original/ptbr.png` | 2 estados | Fig. 19 |
| `decal_bus_only_top__original/ptbr.png` | 2 estados | Fig. 10 (original) |
| `decal_keep_clear_top__original.png` | original | Fig. 10 |
| `decal_stop_chinatown_oblique__original/ptbr.png` | 2 estados | Fig. 21 (ptbr) |
| `qa_context_chinatown__original.png` | original | — (substituída pela vista de cima) |
| `qa_context_top__ptbr.png` | ptbr | Fig. 12 |

Total: 19 PNG de 1920 × 993 (53 MB, versionados via Git LFS). O `capture_log.json` tem 20 registros porque inclui a captura descartada. As capturas de calibração com esferas de depuração **não** foram guardadas; só as posições medidas estão em `docs/article/tools/annotation_points.json`.
