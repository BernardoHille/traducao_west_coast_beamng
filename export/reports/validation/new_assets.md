# New assets (new_asset_spec)

**Alvo:** `mod/traducao_ptbr_wcusa`  

**Resultado:** `PASS` · PASS 75 · WARN 0 · FAIL 0 · SKIP 0

- functional_changed_lines: `1047`

| Status | Verificação | Mensagem |
|---|---|---|
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
| PASS | s_motel_sign.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_motel_sign.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_food_mart_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_food_mart_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_full_service_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_full_service_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_exhaust_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_exhaust_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_exhaust_sign_002.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_exhaust_sign_002.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_fix_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_fix_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_sound_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_sound_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_stereo_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_stereo_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_car_parts_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_car_parts_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_torres_tires_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_torres_tires_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | diner_building.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | diner_building.dae: compiled .cdae | present and newer than the .dae |
| PASS | gasstation_north.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | gasstation_north.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_fuel_main_05.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_fuel_main_05.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_bld_food_mart_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_bld_food_mart_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_bld_laundomat_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_bld_laundomat_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_bld_shops_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_bld_shops_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_brick_walls_slums_car_shops.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_brick_walls_slums_car_shops.dae: compiled .cdae | present and newer than the .dae |
| PASS | tunnel_mainTrackEntrance.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | tunnel_mainTrackEntrance.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_smash_auto_sign_001.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_smash_auto_sign_001.dae: compiled .cdae | present and newer than the .dae |
| PASS | dragstrip_tree_alder.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | dragstrip_tree_alder.dae: compiled .cdae | present and newer than the .dae |
| PASS | dragDriversWinLightBoxShort.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | dragDriversWinLightBoxShort.dae: compiled .cdae | present and newer than the .dae |
| PASS | dragStrip_irSensorBox.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | dragStrip_irSensorBox.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_busstop_wcu.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_busstop_wcu.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_busstop_wcu_04.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_busstop_wcu_04.dae: compiled .cdae | present and newer than the .dae |
| PASS | roadsigns.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | roadsigns.dae: compiled .cdae | present and newer than the .dae |
| PASS | Override levels/west_coast_usa/main.decals.json | only the declared decal instances differ (9 deleted, 6 rectIdx changed) |
| PASS | Override levels/west_coast_usa/main/MissionGroup/AIWaypointsGroup/items.level.json | 43 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/DecalRoads/items.level.json | 38 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island/island_ai_roads/items.level.json | 8 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_aiRoads/items.level.json | 12 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_entrance/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_exit/items.level.json | 2 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/road_signs/items.level.json | 4 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/slotTraffic.json | 939 line(s) differ from the game file, only in speedLimit / declared shapeName |
