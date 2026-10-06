# PNG validation

**Alvo:** `working/png/t_steel_factory_brand_ao.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_steel_factory_brand_ao.data.png`
- texture: `t_steel_factory_brand_ao.data`
- allowed_regions: `1`
- heatmaps: `['export/reports/validation/images/t_steel_factory_brand_ao.data_diff.png', 'export/reports/validation/images/t_steel_factory_brand_ao.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (1e2c2502287e…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 2.4599% changed · RGB mean 0.2139 max 34 · alpha mean 0.0 max 0 · PSNR 45.22 dB · bbox {'x': 79, 'y': 916, 'width': 869, 'height': 100} |
| PASS | Changes outside allowed regions | 0 px changed outside; 25794 px inside 1 region(s) |
