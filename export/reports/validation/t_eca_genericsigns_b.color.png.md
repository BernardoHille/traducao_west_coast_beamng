# PNG validation

**Alvo:** `working/png/t_eca_genericsigns_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_eca_genericsigns_b.color.png`
- texture: `t_eca_genericsigns_b.color`
- allowed_regions: `27`
- heatmaps: `['export/reports/validation/images/t_eca_genericsigns_b.color_diff.png', 'export/reports/validation/images/t_eca_genericsigns_b.color_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (78165798e5f1…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 6711 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 4.6758% changed · RGB mean 5.2569 max 255 · alpha mean 0.0 max 0 · PSNR 19.78 dB · bbox {'x': 13, 'y': 14, 'width': 777, 'height': 382} |
| PASS | Changes outside allowed regions | 0 px changed outside; 49029 px inside 27 region(s) |
