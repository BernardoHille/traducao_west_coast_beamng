# PNG validation

**Alvo:** `working/png/t_steel_factory_brand_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_steel_factory_brand_b.color.png`
- texture: `t_steel_factory_brand_b.color`
- allowed_regions: `1`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (9e73dcb3dd7d…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 8416 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 3.6115% changed · RGB mean 4.4435 max 207 · alpha mean 0.0 max 0 · PSNR 23.5 dB · bbox {'x': 81, 'y': 916, 'width': 867, 'height': 85} |
| PASS | Changes outside allowed regions | 0 px changed outside; 37869 px inside 1 region(s) |
