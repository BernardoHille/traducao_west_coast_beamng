# PNG validation

**Alvo:** `source/reference_ptbr/t_sponsors_b.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 0 · FAIL 4 · SKIP 0

- original: `source/originals/png/t_sponsors_b.color.png`
- texture: `t_sponsors_b.color`
- allowed_regions: `0`
- heatmaps: `['export/reports/validation/images/t_sponsors_b.color_ptbr_diff.png', 'export/reports/validation/images/t_sponsors_b.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (1acbc025c160…) |
| PASS | Resolution | 2048x1024 |
| FAIL | Alpha preservation | 100.0% of originally transparent pixels outside allowed regions lost transparency (62164 px) |
| FAIL | Semi-transparency | 44.88% of 5256 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 4078 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 201) |
| PASS | Pixel diff (global, informative) | 76.269% changed · RGB mean 6.9485 max 219 · alpha mean 7.6499 max 255 · PSNR 27.97 dB · bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024} |
| FAIL | Changes (no allowed regions configured) | 76.269% of pixels outside allowed regions changed (1599477 px, bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024}) |
