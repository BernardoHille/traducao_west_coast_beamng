# PNG validation

**Alvo:** `working/png/t_spearleaf_refinery_logo_o.data.png`  

**Resultado:** `PASS` · PASS 5 · WARN 0 · FAIL 0 · SKIP 2

- original: `source/originals/png/t_spearleaf_refinery_logo_o.data.png`
- texture: `t_spearleaf_refinery_logo_o.data`
- allowed_regions: `1`
- heatmaps: `['export/reports/validation/images/t_spearleaf_refinery_logo_o.data_diff.png', 'export/reports/validation/images/t_spearleaf_refinery_logo_o.data_alpha_diff.png']`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (079a076f785d…) |
| PASS | Resolution | 1024x1024 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| SKIP | Semi-transparency | original has no semi-transparent pixels outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 1.3863% changed · RGB mean 2.5137 max 255 · alpha mean 0.0 max 0 · PSNR 20.46 dB · bbox {'x': 305, 'y': 854, 'width': 402, 'height': 66} |
| PASS | Changes outside allowed regions | 0 px changed outside; 14536 px inside 1 region(s) |
