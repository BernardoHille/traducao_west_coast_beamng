# PNG validation

**Alvo:** `working/png/t_steel_factory_brand_r.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_steel_factory_brand_r.data.png`
- texture: `t_steel_factory_brand_r.data`
- allowed_regions: `1`
- heatmaps: `['export/reports/validation/images/t_steel_factory_brand_r.data_diff.png', 'export/reports/validation/images/t_steel_factory_brand_r.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (f9960a87fec8…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 3.4413% changed · RGB mean 0.5 max 75 · alpha mean 0.0 max 0 · PSNR 37.9 dB · bbox {'x': 78, 'y': 916, 'width': 870, 'height': 100} |
| PASS | Changes outside allowed regions | 0 px changed outside; 36085 px inside 1 region(s) |
