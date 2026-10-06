# Family validation

**Alvo:** `t_decal_roadmarkings (mod)`  

**Resultado:** `PASS` · PASS 7 · WARN 0 · FAIL 0 · SKIP 0

- scope: `global`
- wcusa_usage: `confirmed`
- delivered: `{'base_color': 'mod/traducao_ptbr_wcusa/assets/materials/decal/marking/m_decal_roadmarkings_01/t_decal_roadmarkings_b.color.dds', 'opacity': 'mod/traducao_ptbr_wcusa/assets/materials/decal/marking/m_decal_roadmarkings_01/t_decal_roadmarkings_o.data.dds', 'normal': 'mod/traducao_ptbr_wcusa/assets/materials/decal/marking/m_decal_roadmarkings_01/t_decal_roadmarkings_nm.normal.dds', 'ao': 'mod/traducao_ptbr_wcusa/assets/materials/decal/marking/m_decal_roadmarkings_01/t_decal_roadmarkings_ao.data.dds'}`
- notes: `Letter shape lives in opacity + normal + AO (audit §4.1). Roughness/metallic may stay original. Phase 6: a second copy of the atlas lives in assets/materials/decalroad/lines/roadmarkings1 (opacity 1024, AO 512); both copies are overridden, each rebuilt from its own original (source/originals/*/decalroad/).`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | base_color (t_decal_roadmarkings_b.color.dds) | delivered |
| PASS | opacity (t_decal_roadmarkings_o.data.dds) | delivered |
| PASS | normal (t_decal_roadmarkings_nm.normal.dds) | delivered |
| PASS | ao (t_decal_roadmarkings_ao.data.dds) | delivered |
| PASS | roughness (t_decal_roadmarkings_r.data.dds) | not delivered — original stays in use |
| PASS | metallic (t_decal_roadmarkings_m.data.dds) | not delivered — original stays in use |
| PASS | shape_changed | all shape-dependent maps delivered: opacity, normal, ao |
