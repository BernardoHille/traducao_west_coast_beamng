# Regression: legacy PT-BR images (negative dataset)

**Resultado:** `PASS` · PASS 10 · WARN 0 · FAIL 0 · SKIP 0

- cases: `[{'case': 'old_eca_roadsigns_alpha', 'expected': ['Alpha preservation'], 'obtained': 'FAIL', 'fail_checks': ['Alpha preservation', 'Changes (no allowed regions configured)', 'Semi-transparency'], 'ok': True}, {'case': 'old_dealers_alpha', 'expected': ['Alpha preservation', 'Alpha noise'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Alpha preservation', 'Changes (no allowed regions configured)'], 'ok': True}, {'case': 'old_roadsigns_pixel_diff', 'expected': ['Changes outside allowed regions', 'Alpha noise'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Changes outside allowed regions'], 'ok': True}, {'case': 'old_roadmarkings_family', 'expected': ['shape_changed'], 'obtained': 'FAIL', 'fail_checks': ['shape_changed'], 'ok': True}, {'case': 'old_genericsigns_family', 'expected': ['shape_changed'], 'obtained': 'FAIL', 'fail_checks': ['shape_changed'], 'ok': True}, {'case': 'old_movie_studio', 'expected': ['Changes outside allowed regions'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Changes outside allowed regions'], 'ok': True}, {'case': 'old_industrial', 'expected': ['Changes outside allowed regions'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Changes outside allowed regions'], 'ok': True}, {'case': 'old_sponsors', 'expected': ['Alpha preservation'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Alpha preservation', 'Changes (no allowed regions configured)', 'Semi-transparency'], 'ok': True}, {'case': 'old_roadmarkings_texture', 'expected': ['Changes outside allowed regions'], 'obtained': 'FAIL', 'fail_checks': ['Alpha noise', 'Changes outside allowed regions'], 'ok': True}, {'case': 'old_sealbrik_identical', 'expected': 'PASS', 'obtained': 'PASS', 'fail_checks': [], 'ok': True}]`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | old_eca_roadsigns_alpha | detected as expected — got FAIL; FAIL checks: ['Alpha preservation', 'Changes (no allowed regions configured)', 'Semi-transparency'] |
| PASS | old_dealers_alpha | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Alpha preservation', 'Changes (no allowed regions configured)'] |
| PASS | old_roadsigns_pixel_diff | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Changes outside allowed regions'] |
| PASS | old_roadmarkings_family | detected as expected — got FAIL; FAIL checks: ['shape_changed'] |
| PASS | old_genericsigns_family | detected as expected — got FAIL; FAIL checks: ['shape_changed'] |
| PASS | old_movie_studio | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Changes outside allowed regions'] |
| PASS | old_industrial | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Changes outside allowed regions'] |
| PASS | old_sponsors | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Alpha preservation', 'Changes (no allowed regions configured)', 'Semi-transparency'] |
| PASS | old_roadmarkings_texture | detected as expected — got FAIL; FAIL checks: ['Alpha noise', 'Changes outside allowed regions'] |
| PASS | old_sealbrik_identical | detected as expected — got PASS; FAIL checks: none |
