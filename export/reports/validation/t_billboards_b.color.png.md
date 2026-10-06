# PNG validation

**Alvo:** `working/png/t_billboards_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_billboards_b.color.png`
- texture: `t_billboards_b.color`
- allowed_regions: `19`
- heatmaps: `['export/reports/validation/images/t_billboards_b.color_diff.png', 'export/reports/validation/images/t_billboards_b.color_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (cb03f1a05db2…) |
| PASS | Resolution | 2048x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 2960 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 5.9956% changed · RGB mean 5.1346 max 245 · alpha mean 0.0 max 0 · PSNR 20.96 dB · bbox {'x': 48, 'y': 12, 'width': 1960, 'height': 925} |
| PASS | Changes outside allowed regions | 0 px changed outside; 125737 px inside 19 region(s) |
