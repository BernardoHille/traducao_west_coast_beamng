# PNG validation

**Alvo:** `source/reference_ptbr/t_sealbrik_logo_b.color_ptbr.png`  

**Resultado:** `PASS` · PASS 6 · WARN 0 · FAIL 0 · SKIP 1

- original: `source/originals/png/t_sealbrik_logo_b.color.png`
- texture: `t_sealbrik_logo_b.color`
- allowed_regions: `0`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | Original integrity | SHA-256 matches manifest (9f56c0b2e673…) |
| PASS | Resolution | 1024x512 |
| SKIP | Alpha preservation | original has no fully transparent pixels outside allowed regions |
| PASS | Semi-transparency | 0.00% of 36390 originally semi-transparent pixels changed outside allowed regions |
| PASS | Alpha noise | no opaque pixel lost opacity outside allowed regions |
| PASS | Pixel diff (global, informative) | 0.0% changed · RGB mean 0.0 max 0 · alpha mean 0.0 max 0 · PSNR ∞ dB · bbox None |
| PASS | Changes (no allowed regions configured) | 0 px changed outside; 0 px inside 0 region(s) |
