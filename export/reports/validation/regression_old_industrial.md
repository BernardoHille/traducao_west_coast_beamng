# PNG validation

**Alvo:** `source/reference_ptbr/ind_industrial_signs_d.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 1 · FAIL 2 · SKIP 1

- original: `source/originals/png/ind_industrial_signs_d.color.png`
- texture: `ind_industrial_signs_d.color`
- allowed_regions: `13`
- heatmaps: `['export/reports/validation/images/ind_industrial_signs_d.color_ptbr_diff.png', 'export/reports/validation/images/ind_industrial_signs_d.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (df833ebfc55e…) |
| PASS | Resolution | 1024x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| WARN | Semi-transparency | 0.76% of 27330 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 2740 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 220) |
| PASS | Pixel diff (global, informative) | 95.2467% changed · RGB mean 29.1094 max 207 · alpha mean 0.1575 max 35 · PSNR 16.71 dB · bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 512} |
| FAIL | Changes outside allowed regions | 94.9332% of pixels outside allowed regions changed (452779 px, bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 512}) |
