# PNG validation

**Alvo:** `working/png/t_roadsigns_o.data.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_roadsigns_o.data.png`
- texture: `t_roadsigns_o.data`
- allowed_regions: `28`
- heatmaps: `['export/reports/validation/images/t_roadsigns_o.data_diff.png', 'export/reports/validation/images/t_roadsigns_o.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (7429ef2a251e…) |
| PASS | Resolution | 2048x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 206 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 4.7649% changed · RGB mean 7.089 max 255 · alpha mean 0.0 max 0 · PSNR 16.36 dB · bbox {'x': 0, 'y': 8, 'width': 1733, 'height': 1013} |
| PASS | Changes outside allowed regions | 0 px changed outside; 99928 px inside 28 region(s) |
