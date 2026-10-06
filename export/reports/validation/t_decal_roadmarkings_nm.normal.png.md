# PNG validation

**Alvo:** `working/png/decalroad/t_decal_roadmarkings_nm.normal.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_decal_roadmarkings_nm.normal.png`
- texture: `t_decal_roadmarkings_nm.normal`
- allowed_regions: `7`
- heatmaps: `['export/reports/validation/images/t_decal_roadmarkings_nm.normal_diff.png', 'export/reports/validation/images/t_decal_roadmarkings_nm.normal_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (d1f0f829b01b…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 6.9361% changed · RGB mean 2.1554 max 159 · alpha mean 0.0 max 0 · PSNR 33.7 dB · bbox {'x': 2, 'y': 40, 'width': 994, 'height': 700} |
| PASS | Changes outside allowed regions | 0 px changed outside; 72730 px inside 7 region(s) |
