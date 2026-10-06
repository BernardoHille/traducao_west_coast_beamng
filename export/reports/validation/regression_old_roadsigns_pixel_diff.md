# PNG validation

**Alvo:** `source/reference_ptbr/t_roadsigns_b.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 1 · FAIL 2 · SKIP 1

- original: `source/originals/png/t_roadsigns_b.color.png`
- texture: `t_roadsigns_b.color`
- allowed_regions: `54`
- heatmaps: `['export/reports/validation/images/t_roadsigns_b.color_ptbr_diff.png', 'export/reports/validation/images/t_roadsigns_b.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (4933c5e942b8…) |
| PASS | Resolution | 2048x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| WARN | Semi-transparency | 0.13% of 749 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 6101 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 201) |
| PASS | Pixel diff (global, informative) | 65.8141% changed · RGB mean 26.0951 max 255 · alpha mean 0.0855 max 54 · PSNR 13.88 dB · bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024} |
| FAIL | Changes outside allowed regions | 61.8713% of pixels outside allowed regions changed (919319 px, bbox {'x': 0, 'y': 0, 'width': 2048, 'height': 1024}) |
