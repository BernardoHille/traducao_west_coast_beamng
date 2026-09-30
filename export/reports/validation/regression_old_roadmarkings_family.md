# Family validation

**Alvo:** `t_decal_roadmarkings (reference)`  

**Resultado:** `FAIL` · PASS 6 · WARN 0 · FAIL 1 · SKIP 0

- scope: `global`
- wcusa_usage: `confirmed`
- delivered: `{'base_color': 'source/reference_ptbr/t_decal_roadmarkings_b.color_ptbr.png'}`
- notes: `Letter shape lives in opacity + normal + AO (audit §4.1). Roughness/metallic may stay original.`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | base_color (t_decal_roadmarkings_b.color.dds) | delivered |
| PASS | opacity (t_decal_roadmarkings_o.data.dds) | not delivered — original stays in use |
| PASS | normal (t_decal_roadmarkings_nm.normal.dds) | not delivered — original stays in use |
| PASS | ao (t_decal_roadmarkings_ao.data.dds) | not delivered — original stays in use |
| PASS | roughness (t_decal_roadmarkings_r.data.dds) | not delivered — original stays in use |
| PASS | metallic (t_decal_roadmarkings_m.data.dds) | not delivered — original stays in use |
| FAIL | shape_changed | shape changed but these maps were not updated: opacity (t_decal_roadmarkings_o.data.dds), normal (t_decal_roadmarkings_nm.normal.dds), ao (t_decal_roadmarkings_ao.data.dds) |
