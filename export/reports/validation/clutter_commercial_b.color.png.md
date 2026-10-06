# PNG validation

**Alvo:** `working/png/art_shapes/clutter_commercial_b.color.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/art_shapes/clutter_commercial_b.color.png`
- texture: `clutter_commercial_b.color`
- allowed_regions: `98`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (a2f3d65f78a6…) |
| PASS | Resolution | 2048x2048 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 3174 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 8.3844% changed · RGB mean 7.3803 max 255 · alpha mean 0.0 max 0 · PSNR 19.75 dB · bbox {'x': 2, 'y': 5, 'width': 2042, 'height': 2043} |
| PASS | Changes outside allowed regions | 0 px changed outside; 351668 px inside 98 region(s) |
