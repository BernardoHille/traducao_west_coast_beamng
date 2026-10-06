# PNG validation

**Alvo:** `working/png/decalroad/t_decal_roadmarkings_o.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/decalroad/t_decal_roadmarkings_o.data.png`
- texture: `t_decal_roadmarkings_o.data`
- allowed_regions: `7`
- heatmaps: `['export/reports/validation/images/t_decal_roadmarkings_o.data_diff.png', 'export/reports/validation/images/t_decal_roadmarkings_o.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (2b603cc8fa31…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 15.3028% changed · RGB mean 9.6417 max 124 · alpha mean 0.0 max 0 · PSNR 19.42 dB · bbox {'x': 1, 'y': 39, 'width': 994, 'height': 983} |
| PASS | Changes outside allowed regions | 0 px changed outside; 160462 px inside 7 region(s) |
