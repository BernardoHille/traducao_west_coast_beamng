# Family validation

**Alvo:** `eca_genericsigns (reference)`  

**Resultado:** `FAIL` · PASS 6 · WARN 0 · FAIL 2 · SKIP 0

- scope: `global (East Coast path)`
- wcusa_usage: `confirmed`
- delivered: `{'base_color': 'source/reference_ptbr/t_eca_genericsigns_b.color_ptbr.png'}`
- notes: `West Coast fuel stations load eca_genericsigns_d.dds from the East Coast level path (Phase 3). t_eca_genericsigns_b.color has the same content.`

| Status | Verificação | Mensagem |
|---|---|---|
| FAIL | diffuse_legacy (eca_genericsigns_d.dds) | required map missing from the package |
| PASS | emissive (eca_genericsigns_emissive.dds) | not delivered — original stays in use |
| PASS | base_color (t_eca_genericsigns_b.color.dds) | delivered |
| PASS | opacity (t_eca_genericsigns_o.data.dds) | not delivered — original stays in use |
| PASS | normal (t_eca_genericsigns_nm.normal.dds) | not delivered — original stays in use |
| PASS | ao (t_eca_genericsigns_ao.data.dds) | not delivered — original stays in use |
| PASS | roughness (t_eca_genericsigns_r.data.dds) | not delivered — original stays in use |
| FAIL | shape_changed | shape changed but these maps were not updated: diffuse_legacy (eca_genericsigns_d.dds), emissive (eca_genericsigns_emissive.dds), opacity (t_eca_genericsigns_o.data.dds) |
