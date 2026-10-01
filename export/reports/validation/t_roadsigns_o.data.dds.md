# DDS validation

**Alvo:** `export/dds/t_roadsigns/t_roadsigns_o.data.dds`  

**Resultado:** `PASS` · PASS 8 · WARN 0 · FAIL 0 · SKIP 0

- original: `source/originals/dds/t_roadsigns_o.data.dds`
- original_format: `2048x1024 BC7_UNORM (DX10) linear, 12 mips`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | DDS header | 2048x1024 BC7_UNORM (DX10) linear, 12 mips |
| PASS | Original integrity | SHA-256 matches manifest (240ad8451abe…) |
| PASS | File size | 2796388 bytes consistent with header |
| PASS | Mipmaps | 12 (full chain to 1x1) |
| PASS | Resolution | 2048x1024 |
| PASS | DDS format | BC7_UNORM |
| PASS | Colour space | linear |
| PASS | DX10 alpha mode | STRAIGHT vs original UNKNOWN (compatible) |
