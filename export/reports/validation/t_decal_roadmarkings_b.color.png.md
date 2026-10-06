# PNG validation

**Alvo:** `working/png/decalroad/t_decal_roadmarkings_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_decal_roadmarkings_b.color.png`
- texture: `t_decal_roadmarkings_b.color`
- allowed_regions: `7`
- heatmaps: `['export/reports/validation/images/t_decal_roadmarkings_b.color_diff.png', 'export/reports/validation/images/t_decal_roadmarkings_b.color_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (1a0c9c9c1b89…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 5235 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 14.9827% changed · RGB mean 6.8575 max 247 · alpha mean 0.0 max 0 · PSNR 21.48 dB · bbox {'x': 0, 'y': 38, 'width': 996, 'height': 946} |
| PASS | Changes outside allowed regions | 0 px changed outside; 157105 px inside 7 region(s) |
