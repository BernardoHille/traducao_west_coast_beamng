# PNG validation

**Alvo:** `source/reference_ptbr/eca_roadsigns_d_ptbr.png`  

**Resultado:** `FAIL` · PASS 4 · WARN 0 · FAIL 3 · SKIP 0

- original: `source/originals/png/eca_roadsigns_d.png`
- texture: `eca_roadsigns_d`
- allowed_regions: `0`
- heatmaps: `['export/reports/validation/images/eca_roadsigns_d_ptbr_diff.png', 'export/reports/validation/images/eca_roadsigns_d_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (8a346ff9688a…) |
| PASS | Resolution | 1024x1024 |
| FAIL | Alpha preservation | 100.0% of originally transparent pixels outside allowed regions lost transparency (122077 px) |
| FAIL | Semi-transparency | 95.38% of 38285 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 76.921% changed · RGB mean 17.7545 max 255 · alpha mean 34.5441 max 255 · PSNR 15.35 dB · bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 1024} |
| FAIL | Changes (no allowed regions configured) | 76.921% of pixels outside allowed regions changed (806575 px, bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 1024}) |
