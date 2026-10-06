# PNG validation

**Alvo:** `working/png/t_bus_routes_wca_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_bus_routes_wca_b.color.png`
- texture: `t_bus_routes_wca_b.color`
- allowed_regions: `30`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (7d158e869f6d…) |
| PASS | Resolution | 512x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 5601 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 3.9707% changed · RGB mean 2.2252 max 214 · alpha mean 0.0 max 0 · PSNR 26.01 dB · bbox {'x': 8, 'y': 8, 'width': 460, 'height': 503} |
| PASS | Changes outside allowed regions | 0 px changed outside; 10409 px inside 30 region(s) |
