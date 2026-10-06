# PNG validation

**Alvo:** `source/reference_ptbr/t_decal_roadmarkings_b.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 1 · FAIL 2 · SKIP 1

- original: `source/originals/png/t_decal_roadmarkings_b.color.png`
- texture: `t_decal_roadmarkings_b.color`
- allowed_regions: `7`
- heatmaps: `['export/reports/validation/images/t_decal_roadmarkings_b.color_ptbr_diff.png', 'export/reports/validation/images/t_decal_roadmarkings_b.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (1a0c9c9c1b89…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| WARN | Semi-transparency | 0.69% of 5235 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 2777 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 220) |
| PASS | Pixel diff (global, informative) | 86.5936% changed · RGB mean 13.7648 max 255 · alpha mean 0.0774 max 35 · PSNR 19.72 dB · bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 1024} |
| FAIL | Changes outside allowed regions | 80.7448% of pixels outside allowed regions changed (476252 px, bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 1024}) |
