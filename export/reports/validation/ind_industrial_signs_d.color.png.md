# PNG validation

**Alvo:** `working/png/ind_industrial_signs_d.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/ind_industrial_signs_d.color.png`
- texture: `ind_industrial_signs_d.color`
- allowed_regions: `13`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (df833ebfc55e…) |
| PASS | Resolution | 1024x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 27330 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 6.439% changed · RGB mean 3.9668 max 210 · alpha mean 0.0 max 0 · PSNR 24.03 dB · bbox {'x': 197, 'y': 17, 'width': 823, 'height': 494} |
| PASS | Changes outside allowed regions | 0 px changed outside; 33759 px inside 13 region(s) |
