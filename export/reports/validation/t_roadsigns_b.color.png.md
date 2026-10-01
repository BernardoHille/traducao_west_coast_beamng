# PNG validation

**Alvo:** `working/png/t_roadsigns_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_roadsigns_b.color.png`
- texture: `t_roadsigns_b.color`
- allowed_regions: `44`
- heatmaps: `['export/reports/validation/images/t_roadsigns_b.color_diff.png', 'export/reports/validation/images/t_roadsigns_b.color_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (4933c5e942b8…) |
| PASS | Resolution | 2048x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 749 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 8.9858% changed · RGB mean 7.9103 max 255 · alpha mean 0.0 max 0 · PSNR 18.27 dB · bbox {'x': 1, 'y': 8, 'width': 2041, 'height': 1009} |
| PASS | Changes outside allowed regions | 0 px changed outside; 188445 px inside 44 region(s) |
