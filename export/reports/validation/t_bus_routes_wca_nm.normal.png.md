# PNG validation

**Alvo:** `working/png/t_bus_routes_wca_nm.normal.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_bus_routes_wca_nm.normal.png`
- texture: `t_bus_routes_wca_nm.normal`
- allowed_regions: `30`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (dd81809966ef…) |
| PASS | Resolution | 512x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 5.3139% changed · RGB mean 1.0227 max 68 · alpha mean 0.0 max 0 · PSNR 37.59 dB · bbox {'x': 8, 'y': 8, 'width': 461, 'height': 503} |
| PASS | Changes outside allowed regions | 0 px changed outside; 13930 px inside 30 region(s) |
