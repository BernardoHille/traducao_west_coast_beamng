# PNG validation

**Alvo:** `source/reference_ptbr/t_billboardsigns_dealers_b.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 1 · FAIL 3 · SKIP 0

- original: `source/originals/png/t_billboardsigns_dealers_b.color.png`
- texture: `t_billboardsigns_dealers_b.color`
- allowed_regions: `0`
- heatmaps: `['export/reports/validation/images/t_billboardsigns_dealers_b.color_ptbr_diff.png', 'export/reports/validation/images/t_billboardsigns_dealers_b.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (fc335ea5be0f…) |
| PASS | Resolution | 2048x1024 |
| FAIL | Alpha preservation | 100.0% of originally transparent pixels outside allowed regions lost transparency (292324 px) |
| WARN | Semi-transparency | 4.87% of 460009 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 2311 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 201) |
| PASS | Pixel diff (global, informative) | 85.1974% changed · RGB mean 26.2903 max 255 · alpha mean 38.0271 max 255 · PSNR 14.73 dB · bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024} |
| FAIL | Changes (no allowed regions configured) | 85.1974% of pixels outside allowed regions changed (1786718 px, bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024}) |
