# Famílias de texturas e mapas associados

Levantado em 30/09/2026 (Fase 0) com BeamNG.drive 0.39.4.0. As fontes foram a pasta legada `Texturas de placas` e a **listagem somente leitura** dos `.zip` em `BeamNG.drive/content/`.

Uma "família" é o conjunto de mapas que um material usa juntos (cor, opacidade, emissivo, normal, AO, rugosidade, metálico). Se o conteúdo do mapa de cor mudar de posição ou de forma, os outros mapas da família também podem precisar mudar (ver `TEXTURE_GUIDELINES.md`, Regra 9).

Legenda da coluna **Local**: ✔ = existe em `source/originals/` · ✘ = existe só no jogo (ainda não extraído)
Coluna **Ref. PT-BR**: arquivo em `source/reference_ptbr/`, quando houver.

> Esta tabela complementa `AUDITORIA_PROJETO_TRADUCAO.md`, que é um snapshot e não foi alterada. As diferenças em relação à auditoria estão em "Observações posteriores à auditoria", no fim deste documento.

## 01 - Placas de Trânsito

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| t_roadsigns | `signage.zip` → `assets/materials/signage/roadsigns/` | `t_roadsigns_b.color` ✔ · `t_roadsigns_o.data` ✔ | `t_roadsigns_b.color_ptbr.png` |
| eca_roadsigns | `signage.zip` → `assets/materials/signage/signs_usa/` | `eca_roadsigns_d` ✔ · `eca_roadsigns_s` ✘ | `eca_roadsigns_d_ptbr.png` |
| ut_roadsigns | `signage.zip` → `assets/materials/signage/ut_roadsigns/` | `ut_roadsigns_d` ✔ · `ut_roadsigns_s` ✘ | — |
| speed_sign | `signage.zip` → `assets/materials/signage/speed_sign_mat/` | `speed_sign` ✔ | — |
| usa_roadsigns_turn_warning | `signage.zip` → `assets/materials/signage/usa_roadsigns_turn_warn/` | `usa_roadsigns_turn_warning` ✔ | — |
| usa_roadsigns_text ¹ | `atlas.zip` → `assets/materials/atlas/intro_text/` + `billboard_label.zip` → `assets/materials/billboard_label/usa_roadsigns_text/` | `usa_roadsigns_text` ✔ · `t_usa_roadsigns_text_e.color` ✔ · `t_usa_roadsigns_text_o.data` ✔ | — |

¹ Agrupamento inferido pelo nome. O atlas e os mapas `_e`/`_o` ficam em pastas diferentes do jogo. Confirmar pelo material antes de editar.

## 02 - Comercial

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| clutter_commercial | `west_coast_usa.zip` → `levels/west_coast_usa/art/shapes/buildings/` **e** `art_shapes.zip` → `art/shapes/garage_and_dealership/Clutter/` | `clutter_commercial_b.color` ✔ · `clutter_commercial_o.data` ✔ · `clutter_commercial_d` (.dds/.png, só em `art_shapes.zip`) ✘ | — |
| logos_dealership_garage_wca | `billboard_label.zip` → `…/m_logos_dealership_garage/` | `logos_dealership_garage_wca_d.color` ✔ | — |
| t_riverside_plaza_sign_LOD | `west_coast_usa.zip` → `levels/west_coast_usa/art/shapes/buildings/west_coast_LOD_materials/s_riverside_plaza_sign/` | `_b.color` ✔ · `_m.data` ✘ · `_r.data` ✘ | — |
| t_west_coast_garage_sign | `billboard_label.zip` → `…/m_west_coast_garage_sign/` | `_b.color` ✔ · `_o.data` ✘ · `_r.data` ✘ | — |

## 03 - Postos

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| eca_genericsigns | `billboard_label.zip` → `…/eca_genericsigns/` + `art_shapes.zip` → `art/shapes/garage_and_dealership/Clutter/` (emissivo) | `t_eca_genericsigns_b.color` ✔ · `eca_genericsigns_emissive` ✔ · `t_eca_genericsigns_o.data` ✘ · `_nm.normal` ✘ · `_ao.data` ✘ · `_r.data` ✘ | `t_eca_genericsigns_b.color_ptbr.png` |
| t_gasstation_tyrannos | `billboard_label.zip` → `…/m_gasstation_tyrannos/` | `_b.color` ✔ | — |

## 04 - Outdoors

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| billboards | `west_coast_usa.zip` → `levels/west_coast_usa/art/shapes/objects/` | `billboards_d` ✔ · `billboards_s` ✘ | `billboards_d_ptbr.png` |
| t_billboardsigns_dealers | `atlas.zip` → `…/m_billboardsigns_dealers/` | `_b.color` ✔ · `_o.data` ✘ | `t_billboardsigns_dealers_b.color_ptbr.png` |
| t_billboards | `billboard_label.zip` → `…/billboards/` | `_b.color` ✔ · `_r.data` ✘ | — |

## 05 - Ônibus

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| busstop | `atlas.zip` → `…/atlas/busstop/` | `busstop_d` ✔ · `busstop_n` ✘ · `busstop_r` ✘ · `busstop_s` ✘ | — |
| t_bus_routes_wca | `billboard_label.zip` → `…/m_bus_routes_wca/` | `_b.color` ✔ · `_nm.normal` ✘ · `_ao.data` ✘ · `_r.data` ✘ | — |
| t_sign_busstop | `signage.zip` → `…/m_sign_busstop/` | `_b.color` ✔ · `_o.data` ✘ | — |

## 06 - Estúdios

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| t_movie_studio_signage | `billboard_label.zip` → `…/m_movie_studio_signage/` | `_b.color` ✔ | `t_movie_studio_signage_b.color_ptbr.png` |

## 07 - Indústria

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| ind_industrial_signs | `billboard_label.zip` → `…/industrial_signs/` | `ind_industrial_signs_d.color` ✔ | `ind_industrial_signs_d.color_ptbr.png` |
| t_industrial_signs | `billboard_label.zip` → `…/industrial_signs/` | `_b.color` ✔ · `_r.data` ✘ | — |
| t_sealbrik_logo | `billboard_label.zip` → `…/m_sealbrick_logo/` | `_b.color` ✔ | `t_sealbrik_logo_b.color_ptbr.png` (**cópia idêntica do original**) |
| t_spearleaf_refinery_logo | `billboard_label.zip` → `…/m_refinery_logo/` | `_b.color` ✔ · `_o.data` ✔ | `…_b.color_ptbr.png` · `…_o.data_ptbr.png` |
| t_steel_factory_brand | `billboard_label.zip` → `…/m_steel_factory_brand/` | `_b.color` ✔ · `_nm.normal` ✘ · `_ao.data` ✘ · `_r.data` ✘ | `t_steel_factory_brand_b.color_ptbr.png` |

## 08 - Corridas

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| arrows_sign | `signage.zip` → `…/sign_arrows/` | `arrows_sign_d` ✔ · `arrows_sign_s` ✘ | — |
| checkpoint_sign | `signage.zip` → `…/checkpoint_sign/` | `checkpoint_sign` ✔ | — |
| t_sign_drift | `signage.zip` → `…/m_sign_drift/` | `t_sign_drift.color` ✔ · `t_sign_drift_o.data` ✘ | — |
| t_sponsors | `atlas.zip` → `…/sponsorboards/` | `_b.color` ✔ | `t_sponsors_b.color_ptbr.png` |

## 09 - Asfalto

| Família | Caminho no jogo | Mapas (Local) | Ref. PT-BR |
|---|---|---|---|
| t_decal_roadmarkings | `decal.zip` → `assets/materials/decal/marking/m_decal_roadmarkings_01/` | `_b.color` ✔ · `_o.data` ✘ · `_nm.normal` ✘ · `_ao.data` ✘ · `_r.data` ✘ · `_m.data` ✘ | `t_decal_roadmarkings_b.color_ptbr.png` |

Material do West Coast que usa essa família: `roadmarkings1` em `levels/west_coast_usa/art/decals/main.materials.json`. Ele é translúcido, tem `alphaTest` e usa `_o.data` como opacidade. Ver o problema crítico §4.1 da auditoria.

---

## Observações posteriores à auditoria (Fase 0)

1. **Contagem de texturas.** A auditoria fala em "41 texturas". No disco há **35 DDS originais**, cada um com seu PNG, ou seja, 35 texturas. O número 41 vinha de uma contagem de ocorrências nos zips do jogo, em que algumas texturas aparecem em mais de um zip.
2. **Mapas auxiliares que a auditoria não listou.** A listagem dos zips mostrou mapas associados que a auditoria não citou e que **não estão na pasta local**:
   - `eca_genericsigns`: `_o.data`, `_nm.normal`, `_ao.data`, `_r.data`. A referência PT-BR mudou o layout, então esses mapas podem estar desalinhados, além do emissivo já citado na auditoria.
   - `t_steel_factory_brand`: `_nm.normal`, `_ao.data`, `_r.data`. Isso afeta a referência PT-BR existente.
   - `t_billboardsigns_dealers`: `_o.data`. A opacidade pode vir desse mapa, e não do alfa do `_b.color`, o que muda a análise da §4.3.
   - `t_sign_busstop`, `t_sign_drift`, `t_west_coast_garage_sign`: `_o.data`.
   - `t_bus_routes_wca`, `busstop`, `t_billboards`, `t_industrial_signs`, `t_riverside_plaza_sign_LOD`, `eca_roadsigns`, `ut_roadsigns`, `arrows_sign`, `billboards`: mapas `_nm`, `_ao`, `_r`, `_m` e `_s`, conforme cada tabela acima.
3. **`clutter_commercial_d`** (.dds e .png) existe só em `art_shapes.zip` e também é da família `clutter_commercial`.

Nada disso foi corrigido na Fase 0. Os mapas marcados com ✘ serão extraídos quando a família entrar em trabalho.
