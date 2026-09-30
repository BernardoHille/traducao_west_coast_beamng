# Diretrizes técnicas de textura

Regras tiradas da auditoria inicial (`docs/AUDITORIA_PROJETO_TRADUCAO.md`, §3 a §4). Os valores por arquivo estão em `docs/inventory/original_files_manifest.csv`.

## Regra 1 — Mesma resolução do original
A textura final tem **exatamente** a largura e a altura do original. Nada de upscale nem downscale.

## Regra 2 — Preservar o formato DDS original
Cada textura volta ao jogo no mesmo formato de compressão em que saiu. Formatos encontrados:

| Formato original | Exemplos |
|---|---|
| DX10 **BC7_UNORM_SRGB** | `t_roadsigns_b.color`, `t_eca_genericsigns_b.color`, `t_sponsors_b.color`, `clutter_commercial_b.color`… |
| DX10 **BC7_UNORM** (linear) | `t_roadsigns_o.data`, `ut_roadsigns_d` |
| **BC4_UNORM** (BC4U) | `clutter_commercial_o.data`, `t_spearleaf_refinery_logo_o.data`, `t_usa_roadsigns_text_o.data` |
| **BC1 (DXT1)** | `speed_sign`, `usa_roadsigns_turn_warning`, `billboards_d`, `checkpoint_sign` |
| **BC3 (DXT5)** | `eca_roadsigns_d`, `usa_roadsigns_text`, `busstop_d`, `eca_genericsigns_emissive`, `arrows_sign_d` |

## Regra 3 — Não usar BC7 indiscriminadamente
BC7 só vale onde o original é BC7. DXT1, DXT5 e BC4 continuam como estão.

## Regra 4 — Color maps em sRGB quando o original for sRGB
`*_b.color`, `*_d.color` e `*_e.color` em BC7_UNORM_SRGB devem ser exportados como sRGB.

## Regra 5 — Data maps continuam lineares
`*_o.data`, `*_r.data`, `*_ao.data`, `*_m.data` e `*.normal` **nunca** são sRGB.

## Regra 6 — Preservar a cadeia de mipmaps
Gerar a cadeia completa, com o mesmo número de níveis do original (7 a 12, conforme a resolução).

## Regra 7 — Preservar o canal alfa
O alfa final vem do original, ou da máscara refeita quando a forma mudou. Não pode ter ruído: pixels que eram 255 continuam 255. Materiais com `alphaTest` (por exemplo, ref 135 e 150) abrem buracos se o alfa cair abaixo da referência.

## Regra 8 — Modificar só as regiões necessárias
Fora das áreas de texto, a diferença de pixels em relação ao original deve ser ≈0.

## Regra 9 — Se a posição ou a forma mudar, revisar os mapas relacionados
Se o conteúdo mudar de lugar ou de contorno, revisar:
- opacity (`_o.data`)
- emissive (`_e.color`, `*_emissive`)
- normal (`_nm.normal`, `_n`)
- AO (`_ao.data`)
- roughness (`_r.data`)
- metallic (`_m.data`)
- specular legado (`_s`)
- outros mapas da família (ver `docs/inventory/texture_families.md`)

## Regra 10 — Atlas exige preservação rigorosa da UV
Em atlas, cada elemento ocupa coordenadas fixas usadas pelos modelos 3D. Nenhum elemento pode sair da sua região original.

## Regra 11 — Nome final exato
O DDS dentro do mod usa **exatamente** o nome e o caminho virtual que o BeamNG espera (por exemplo, `assets/materials/signage/roadsigns/t_roadsigns_b.color.dds`). **Nunca** `_ptbr` no nome final.

## Regra 12 — Assets em `assets/materials` podem afetar outros mapas
Substituir um arquivo em `assets/materials/...` muda essa textura em **todos** os mapas que a usam (East Coast, Utah etc.). Ver a decisão pendente em `docs/PROJECT_STATUS.md`.
