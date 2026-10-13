# New assets (new_asset_spec)

**Alvo:** `mod/traducao_ptbr_wcusa`  

**Resultado:** `PASS` · PASS 108 · WARN 0 · FAIL 0 · SKIP 0

- functional_changed_lines: `1241`

| Status | Verificação | Mensagem |
|---|---|---|
| PASS | t_r19_10_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_40_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_50_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_70_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_120_b.color.dds: spec | 512x1024 BC7_UNORM_SRGB (DX10) sRGB, 11 mips |
| PASS | t_r19_o.data.dds: spec | 512x1024 BC4_UNORM (legacy BC4U) unspecified (legacy header), 11 mips |
| PASS | t_r19_o.data.dds: disc mask | corners transparent, centre opaque, coverage 0.564 (alphaTest 128) |
| PASS | t_r19_10_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | t_r19_40_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | t_r19_50_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | t_r19_70_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | t_r19_120_b.color.dds: edge halo | 1904 edge pixels carry the border colour (no halo) |
| PASS | Materials: no game material redefined | 6 own materials, none named ['roadsigns', 'metal_galvanized'] |
| PASS | Material roadsigns_ptbr_r19_10 | baseColor t_r19_10_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_40 | baseColor t_r19_40_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_50 | baseColor t_r19_50_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_70 | baseColor t_r19_70_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_120 | baseColor t_r19_120_b.color.dds · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | Material roadsigns_ptbr_r19_back | baseColor t_metal_galvanized_01_b.color.png · opacity t_r19_o.data.dds · alphaTest 128 |
| PASS | sign_r19_10.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_r19_10.dae: materials | ['roadsigns_ptbr_r19_10', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_r19_10.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | sign_speed25.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_speed25.dae: materials | ['roadsigns_ptbr_r19_40', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_speed25.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | sign_r19_50.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_r19_50.dae: materials | ['roadsigns_ptbr_r19_50', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_r19_50.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | sign_r19_70.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_r19_70.dae: materials | ['roadsigns_ptbr_r19_70', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_r19_70.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
| PASS | sign_r19_120.dae: structure vs original | geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ |
| PASS | sign_r19_120.dae: materials | ['roadsigns_ptbr_r19_120', 'roadsigns_ptbr_r19_back'] |
| PASS | sign_r19_120.dae: compiled .cdae | present and newer than the .dae (no recompilation, no temp cache) |
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
| PASS | s_toll_booth_center.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_toll_booth_center.dae: compiled .cdae | present and newer than the .dae |
| PASS | s_toll_booth_center_alt.dae: structure vs original | other materials, node tree and transforms identical; only glyph quads of clutter_commercial/m_billboardsigns_dealers/roadsigns changed, inside the original sign |
| PASS | s_toll_booth_center_alt.dae: compiled .cdae | present and newer than the .dae |
| PASS | Override gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json | only the 4 declared zone speedLimit values differ |
| PASS | Override levels/west_coast_usa/city.sites.json | only the 3 declared zone speedLimit values differ |
| PASS | Override levels/west_coast_usa/info.json | only the key localUnits removed |
| PASS | Override levels/west_coast_usa/main.decals.json | only the declared decal instances differ (9 deleted, 6 rectIdx changed) |
| PASS | Override levels/west_coast_usa/main/MissionGroup/AIWaypointsGroup/items.level.json | 55 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/DecalRoads/items.level.json | 39 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island/island_ai_roads/items.level.json | 11 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_aiRoads/items.level.json | 14 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_entrance/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/island_shippingYard/dock_exit/items.level.json | 2 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/items.level.json | game file + 1 declared object(s) appended, nothing else |
| PASS | Override levels/west_coast_usa/main/MissionGroup/ptbr_functional_signs/items.level.json | new file: exactly the 14 declared objects |
| PASS | Override levels/west_coast_usa/main/MissionGroup/road_signs/items.level.json | 4 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_002/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_003/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_004/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_005/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_006/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/main/MissionGroup/trafficCameras_wip/speedCamera_007/items.level.json | 1 line(s) differ from the game file, only in speedLimit / declared shapeName |
| PASS | Override levels/west_coast_usa/slotTraffic.json | 1109 line(s) differ from the game file, only in speedLimit / declared shapeName |
