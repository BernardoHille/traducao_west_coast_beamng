# PNG validation

**Alvo:** `working/png/decalroad/t_decal_roadmarkings_ao.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/decalroad/t_decal_roadmarkings_ao.data.png`
- texture: `t_decal_roadmarkings_ao.data`
- allowed_regions: `7`
- heatmaps: `['export/reports/validation/images/t_decal_roadmarkings_ao.data_diff.png', 'export/reports/validation/images/t_decal_roadmarkings_ao.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (87aa71893f96…) |
| PASS | Resolution | 512x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 18.4872% changed · RGB mean 3.2012 max 107 · alpha mean 0.0 max 0 · PSNR 29.15 dB · bbox {'x': 0, 'y': 0, 'width': 512, 'height': 512} |
| PASS | Changes outside allowed regions | 0 px changed outside; 48463 px inside 7 region(s) |
