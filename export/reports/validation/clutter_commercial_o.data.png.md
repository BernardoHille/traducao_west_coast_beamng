# PNG validation

**Alvo:** `working/png/art_shapes/clutter_commercial_o.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/art_shapes/clutter_commercial_o.data.png`
- texture: `clutter_commercial_o.data`
- allowed_regions: `85`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (fbe52b46a82d…) |
| PASS | Resolution | 2048x2048 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 0.8511% changed · RGB mean 0.8472 max 255 · alpha mean 0.0 max 0 · PSNR 26.77 dB · bbox {'x': 0, 'y': 2, 'width': 388, 'height': 316} |
| PASS | Changes outside allowed regions | 0 px changed outside; 35699 px inside 85 region(s) |
