# PNG validation

**Alvo:** `working/png/t_steel_factory_brand_nm.normal.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_steel_factory_brand_nm.normal.png`
- texture: `t_steel_factory_brand_nm.normal`
- allowed_regions: `1`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (ac372a514aa7…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 4.4477% changed · RGB mean 1.1399 max 178 · alpha mean 0.0 max 0 · PSNR 34.31 dB · bbox {'x': 78, 'y': 916, 'width': 870, 'height': 100} |
| PASS | Changes outside allowed regions | 0 px changed outside; 46637 px inside 1 region(s) |
