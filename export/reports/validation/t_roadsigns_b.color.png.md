# PNG validation

**Alvo:** `working/png/t_roadsigns_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_roadsigns_b.color.png`
- texture: `t_roadsigns_b.color`
- allowed_regions: `54`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (4933c5e942b8…) |
| PASS | Resolution | 2048x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 749 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 10.0875% changed · RGB mean 9.0211 max 255 · alpha mean 0.0 max 0 · PSNR 17.29 dB · bbox {'x': 1, 'y': 8, 'width': 2041, 'height': 1009} |
| PASS | Changes outside allowed regions | 0 px changed outside; 211550 px inside 54 region(s) |
