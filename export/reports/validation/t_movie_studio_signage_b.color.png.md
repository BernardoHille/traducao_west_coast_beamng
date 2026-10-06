# PNG validation

**Alvo:** `working/png/t_movie_studio_signage_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_movie_studio_signage_b.color.png`
- texture: `t_movie_studio_signage_b.color`
- allowed_regions: `37`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (831ec96ebd0c…) |
| PASS | Resolution | 1024x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 127259 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 12.1754% changed · RGB mean 13.4194 max 253 · alpha mean 0.0 max 0 · PSNR 15.68 dB · bbox {'x': 7, 'y': 7, 'width': 1012, 'height': 500} |
| PASS | Changes outside allowed regions | 0 px changed outside; 63834 px inside 37 region(s) |
