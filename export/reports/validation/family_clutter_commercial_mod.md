# Family validation

**Alvo:** `clutter_commercial (mod)`  

**Resultado:** `PASS` · PASS 4 · WARN 0 · FAIL 0 · SKIP 0

- scope: `global`
- wcusa_usage: `confirmed`
- delivered: `{'base_color': 'mod/traducao_ptbr_wcusa/art/shapes/garage_and_dealership/Clutter/clutter_commercial_b.color.dds', 'opacity': 'mod/traducao_ptbr_wcusa/art/shapes/garage_and_dealership/Clutter/clutter_commercial_o.data.dds'}`
- notes: `Material used in West Coast loads the art/shapes path (verified in game). The level folder holds a copy that differs in the neon/sale tiles (original variant art_shapes); it is not referenced by the loaded material and is not overridden. Phase 6: opacity required on shape change (cut-out letters).`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | base_color (clutter_commercial_b.color.dds) | delivered |
| PASS | opacity (clutter_commercial_o.data.dds) | delivered |
| PASS | diffuse_legacy (clutter_commercial_d.dds) | not delivered — original stays in use |
| PASS | shape_changed | all shape-dependent maps delivered: opacity |
