# Mod tree validation

**Alvo:** `mod/traducao_ptbr_wcusa`  

**Resultado:** `PASS` · PASS 48 · WARN 0 · FAIL 0 · SKIP 0

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | mod_info | Tradução PT-BR — West Coast USA 0.5.0 |
| PASS | Case-insensitive duplicates | none |
| PASS | Asset path | assets/materials/signage/roadsigns/t_roadsigns_b.color.dds → t_roadsigns/base_color |
| PASS | Asset path | assets/materials/signage/roadsigns/t_roadsigns_o.data.dds → t_roadsigns/opacity |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/main.materials.json (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/sign_r19_10.cdae (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/sign_r19_10.dae (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/t_r19_10_b.color.dds (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/t_r19_40_b.color.dds (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/t_r19_o.data.dds (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/sign_speed25.cdae (config/new_assets.json; checked by validate.py new) |
| PASS | Declared new asset | levels/west_coast_usa/art/shapes/objects/sign_speed25.dae (config/new_assets.json; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/AIWaypointsGroup/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/DecalRoads/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/island/island_ai_roads/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_aiRoads/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_entrance/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_exit/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/main/MissionGroup/road_signs/items.level.json (speedLimit-only override; checked by validate.py new) |
| PASS | Declared functional override | levels/west_coast_usa/slotTraffic.json (speedLimit-only override; checked by validate.py new) |
| PASS | Installed copy | identical to repo (19 files) |
| PASS | t_roadsigns: base_color (t_roadsigns_b.color.dds) | delivered |
| PASS | t_roadsigns: opacity (t_roadsigns_o.data.dds) | delivered |
| PASS | t_roadsigns: shape_changed | all shape-dependent maps delivered: opacity |
| PASS | t_r19_10_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_40_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_o.data.dds: spec | 512x1024 BC4_UNORM (legacy BC4U) unspecified (legacy header), 11 mips |
| PASS | t_r19_o.data.dds: disc mask | corners transparent, centre opaque, coverage 0.564 (alphaTest 128) |
| PASS | t_r19_10_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | t_r19_40_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | Materials: no game material redefined | 3 own materials, none named ['roadsigns', 'metal_galvanized'] |
| PASS | Material roadsigns_ptbr_r19_10 | baseColor t_r19_10_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_40 | baseColor t_r19_40_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_back | baseColor t_metal_galvanized_01_b.color.png · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | sign_r19_10.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_r19_10.dae: materials | ['roadsigns_ptbr_r19_10', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_r19_10.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | sign_speed25.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_speed25.dae: materials | ['roadsigns_ptbr_r19_40', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_speed25.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | Override levels/west_coast_usa/main/MissionGroup/AIWaypointsGroup/items.level.json | 43 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/DecalRoads/items.level.json | 38 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island/island_ai_roads/items.level.json | 8 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_aiRoads/items.level.json | 12 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_entrance/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_exit/items.level.json | 2 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/road_signs/items.level.json | 4 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/slotTraffic.json | 939 line(s) differ from the game file, only in speedLimit / declared shapeName |
