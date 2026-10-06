# PNG validation

**Alvo:** `source/reference_ptbr/t_movie_studio_signage_b.color_ptbr.png`  

**Resultado:** `FAIL` · PASS 3 · WARN 1 · FAIL 2 · SKIP 1

- original: `source/originals/png/t_movie_studio_signage_b.color.png`
- texture: `t_movie_studio_signage_b.color`
- allowed_regions: `37`
- heatmaps: `['export/reports/validation/images/t_movie_studio_signage_b.color_ptbr_diff.png', 'export/reports/validation/images/t_movie_studio_signage_b.color_ptbr_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (831ec96ebd0c…) |
| PASS | Resolution | 1024x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| WARN | Semi-transparency | 0.34% of 127259 originally semi-transparent pixels changed outside allowed regions |
| FAIL | Alpha noise | 2633 originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min 220) |
| PASS | Pixel diff (global, informative) | 88.7356% changed · RGB mean 42.576 max 255 · alpha mean 0.4106 max 35 · PSNR 11.48 dB · bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 512} |
| FAIL | Changes outside allowed regions | 87.6822% of pixels outside allowed regions changed (350207 px, bbox {'x': 0, 'y': 0, 'width': 1024, 'height': 512}) |
