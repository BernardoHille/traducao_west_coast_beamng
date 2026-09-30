# Mod tree validation

**Alvo:** `mod/traducao_ptbr_wcusa`  

**Resultado:** `WARN` · PASS 6 · WARN 1 · FAIL 0 · SKIP 0

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | mod_info | Tradução PT-BR — West Coast USA 0.1.0-poc |
| PASS | Case-insensitive duplicates | none |
| PASS | Asset path | assets/materials/signage/roadsigns/t_roadsigns_b.color.dds → t_roadsigns/base_color |
| PASS | Installed copy | identical to repo (2 files) |
| PASS | t_roadsigns: base_color (t_roadsigns_b.color.dds) | delivered |
| PASS | t_roadsigns: opacity (t_roadsigns_o.data.dds) | not delivered — original stays in use |
| WARN | t_roadsigns: shape_changed | modification does not declare shape_changed (config/modifications.json); auxiliary-map rule not evaluated |
