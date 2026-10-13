# Fase 7 — diff estruturado dos overrides funcionais

Gerado por `tools/production/apply_phase7_functional.py`. Cada linha corresponde a uma decisão de `working/functional/`, ligada a uma entrada de `phase7_plan.json`.

**Verificação:** OK — 132 changed lines / 132 declared; 15 added objects / 15 declared.

## Objetos do nível (só o campo `speedLimit`)

| Plano | Objeto | Classe | Arquivo | De (m/s) | Para (m/s) | km/h |
|---|---|---|---|---|---|---|
| ex35mph_60 | DR571 `2388e8bc` | DecalRoad | `AIWaypointsGroup/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR666 `af746a38` | DecalRoad | `AIWaypointsGroup/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR625 `6777a576` | DecalRoad | `AIWaypointsGroup/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR989 `d241454f` | DecalRoad | `island/island_ai_roads/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR1003 `be0f5b74` | DecalRoad | `island/island_ai_roads/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR1009 `1e4035d1` | DecalRoad | `island/island_ai_roads/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR1213 `c5865b41` | DecalRoad | `island_shippingYard/dock_aiRoads/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | DR1216 `af1085ba` | DecalRoad | `island_shippingYard/dock_aiRoads/items.level.json` | 15.6464 | 16.6667 | 60 |
| event01_corridor_70 | DR652 `989ef979` | DecalRoad | `AIWaypointsGroup/items.level.json` | 15.6464 | 19.4444 | 70 |
| adas50_zone | DR312 `cfca014d` | DecalRoad | `DecalRoads/items.level.json` | auto 33.3333 | 13.8889 | 50 |
| adas50_exit_120 | DR758 `512c9f8f` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto 33.3333 | 33.3333 | 120 |
| junction1_waypoints_inert | junction1_wp19 `8e3763b3` | BeamNGWaypoint | `AIWaypointsGroup/items.level.json` | 15.6464 | 27.7778 | 100 |
| junction1_waypoints_inert | junction1_wp25 `f9da8bdf` | BeamNGWaypoint | `AIWaypointsGroup/items.level.json` | 15.6464 | 27.7778 | 100 |
| toll_plaza_40 | DR535 `ae1e74da` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto [13.8889, 16.6667, 22.2222, 27.7778, 33.3333] | 11.1111 | 40 |
| toll_plaza_40 | DR559 `13d4fcdd` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto [13.8889, 16.6667, 22.2222, 27.7778, 33.3333] | 11.1111 | 40 |
| toll_plaza_40 | DR595 `3e983d96` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto [13.8889, 16.6667, 22.2222, 27.7778, 33.3333] | 11.1111 | 40 |
| toll_plaza_40 | DR630 `6c12511f` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto [13.8889, 16.6667, 22.2222, 27.7778, 33.3333] | 11.1111 | 40 |
| toll_plaza_40 | DR672 `b9b67a72` | DecalRoad | `AIWaypointsGroup/items.level.json` | auto [13.8889, 16.6667, 22.2222, 27.7778, 33.3333] | 11.1111 | 40 |
| event01_corridor_70 | speedTrapTrigger2 `4d7dbade` | BeamNGTrigger | `trafficCameras_wip/speedCamera_002/items.level.json` | 15.6464 | 19.4444 | 70 |
| ex35mph_60 | speedTrapTrigger3 `8f20ac08` | BeamNGTrigger | `trafficCameras_wip/speedCamera_003/items.level.json` | 15.6464 | 16.6667 | 60 |
| radar4_outlier_100 | speedTrapTrigger4 `dbe59e36` | BeamNGTrigger | `trafficCameras_wip/speedCamera_004/items.level.json` | 15.6464 | 27.7778 | 100 |
| ex35mph_60 | speedTrapTrigger5 `2777327b` | BeamNGTrigger | `trafficCameras_wip/speedCamera_005/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | speedTrapTrigger6 `0a259251` | BeamNGTrigger | `trafficCameras_wip/speedCamera_006/items.level.json` | 15.6464 | 16.6667 | 60 |
| ex35mph_60 | speedTrapTrigger7 `68bbd35b` | BeamNGTrigger | `trafficCameras_wip/speedCamera_007/items.level.json` | 15.6464 | 16.6667 | 60 |

## Objetos novos (grupo `ptbr_functional_signs`)

| Placa | Valor | Posição | Regulamenta |
|---|---|---|---|
| r19_50_entry_right | R-19 50 | [530.505, 783.94] | cfca014d |
| r19_50_entry_left | R-19 50 | [541.93, 767.389] | cfca014d |
| r19_50_spawn_right | R-19 50 | [264.591, 590.172] | cfca014d |
| r19_50_spawn_left | R-19 50 | [400.271, 668.015] | cfca014d |
| r19_120_exit_right | R-19 120 | [-439.326, -31.776] | 512c9f8f |
| r19_70_entry_right | R-19 70 | [-417.765, 181.221] | 989ef979 |
| r19_70_repeat_right | R-19 70 | [-382.44, 243.795] | 989ef979 |

Mais 1 `SimGroup` acrescentado ao `MissionGroup/items.level.json` e 1 poste `pole_fence1` por placa (15 objetos).

## Zonas (`customFields.values.speedLimit`)

| Plano | Arquivo | Zona | De | Para |
|---|---|---|---|---|
| zones_50 | `levels/west_coast_usa/city.sites.json` | levels.west_coast_usa.zones.horizon_estates | 13.3999996 | 13.8889 |
| ex35mph_60 | `levels/west_coast_usa/city.sites.json` | levels.west_coast_usa.zones.the_dockyards | 15.6000004 | 16.6667 |
| zones_80 | `levels/west_coast_usa/city.sites.json` | levels.west_coast_usa.zones.mount_wallis | 22.3999996 | 22.2222 |
| zones_50 | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | missions.wcusa.garage.zones.downtownBelasco.name | 13.3999996 | 13.8889 |
| zones_50 | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | missions.wcusa.garage.zones.residential.name | 13.3999996 | 13.8889 |
| ex35mph_60 | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | missions.wcusa.garage.zones.dockyard.name | 15.6000004 | 16.6667 |
| zones_80 | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | missions.wcusa.garage.zones.mountWallis.name | 22.3999996 | 22.2222 |

## Unidades

- `levels/west_coast_usa/info.json`: chave `localUnits` removida (era {"gasoline": "gallonUS", "diesel": "gallonUS"}).

## slotTraffic.json

- linhas editadas: 1109 (276 faixas, 833 ligações);
- já iguais ao alvo (não tocadas): 2; valor divergente (não tocadas): 28;
- vias sem faixa casada por geometria: 44.
- valores de mph restantes: 0; edições da Fase 5 conferidas: 939 (perdidas: 0).

## Cenários de pesquisa (fora do repositório)

- `event01_start_on_corridor`: already applied (`C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\mods\unpacked\adas_event01_speed_limit\lua\ge\extensions\event01SpeedLimitRecognition.lua`)
- `event01_mission_start_marker`: already applied (`C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\mods\unpacked\adas_event01_speed_limit\gameplay\missions\west_coast_usa\adasEvent01\001-speedLimitRecognition\info.json`)
