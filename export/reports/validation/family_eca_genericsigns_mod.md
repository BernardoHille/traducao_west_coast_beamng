# Family validation

**Alvo:** `eca_genericsigns (mod)`  

**Resultado:** `PASS` · PASS 8 · WARN 0 · FAIL 0 · SKIP 0

- scope: `global (East Coast path)`
- wcusa_usage: `confirmed`
- delivered: `{'base_color': 'mod/traducao_ptbr_wcusa/assets/materials/billboard_label/eca_genericsigns/t_eca_genericsigns_b.color.dds'}`
- notes: `Phase 6 correction (checked in game 05/10/2026): the West Coast loads the PBR material eca_genericsigns of art_shapes.zip -> t_eca_genericsigns_b.color + _o/_nm/_ao/_r (resolved to assets/materials/billboard_label/eca_genericsigns), with NO emissive. The legacy eca_genericsigns_d + emissive (East Coast / Utah / Hirochi paths) belong to those maps' own materials. Phase 3 note superseded.`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | diffuse_legacy (eca_genericsigns_d.dds) | not delivered — original stays in use |
| PASS | emissive (eca_genericsigns_emissive.dds) | not delivered — original stays in use |
| PASS | base_color (t_eca_genericsigns_b.color.dds) | delivered |
| PASS | opacity (t_eca_genericsigns_o.data.dds) | not delivered — original stays in use |
| PASS | normal (t_eca_genericsigns_nm.normal.dds) | not delivered — original stays in use |
| PASS | ao (t_eca_genericsigns_ao.data.dds) | not delivered — original stays in use |
| PASS | roughness (t_eca_genericsigns_r.data.dds) | not delivered — original stays in use |
| PASS | shape_changed | declared false (only colours/text inside the original silhouette) |
