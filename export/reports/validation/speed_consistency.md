# Speed consistency

**Alvo:** `west_coast_usa`  

**Resultado:** `FAIL` · PASS 5 · WARN 0 · FAIL 17 · SKIP 7

- snapshot: `{'collected': '2026-09-30T17:39:50', 'level': '/levels/west_coast_usa/main.level.json', 'source': 'MCP map.getMap() + map.findClosestRoad, TSStatic sign_speed*.dae'}`
- rows: `[{'location': 'radar speedTrapTrigger2 @ [-416, 198]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger3 @ [-305, 325]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger4 @ [-424, 673]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '100.0 km/h (27.78 m/s)', 'result': 'FAIL'}, {'location': 'radar speedTrapTrigger5 @ [-1002, 1902]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger6 @ [414, 1646]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger7 @ [393, 1848]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-274, -58]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-151, 22]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-194, -78]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-169, 155]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-196, -57]', 'sign': '25 mph (= 40.2 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-260, -54]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-259, -44]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-191, -11]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-144, 22]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-54, 78]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 732]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 748]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 764]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 780]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 796]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-22, 805]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-13, 805]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-4, 805]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-26, 716]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-1, 796]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-1, 780]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-1, 764]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [2, 749]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 716]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 732]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 748]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 764]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 780]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 796]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 812]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-65, 828]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-22, 844]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-13, 844]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [-4, 844]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 828]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 812]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 796]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 780]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 764]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [39, 748]', 'sign': '5 mph (= 8.0 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [-1044, 2045]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [477, 1613]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [477, 1608]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [477, 1618]', 'sign': '25 mph (= 40.2 km/h)', 'road': '30.0 km/h (8.333 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed25.dae @ [477, 1623]', 'sign': '25 mph (= 40.2 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [447, 1624]', 'sign': '5 mph (= 8.0 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [444, 1688]', 'sign': '5 mph (= 8.0 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'sign_speed5.dae @ [461, 1688]', 'sign': '5 mph (= 8.0 km/h)', 'road': '60.0 km/h (16.67 m/s)', 'radar': '—', 'zone': '—', 'result': 'FAIL'}, {'location': 'ADAS event01SpeedLimitRecognition spawn [-472, 155]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '70.0 km/h', 'road': '40.2 km/h (11.18 m/s)', 'result': 'FAIL'}, {'location': 'ADAS adasSpeedAlertTest spawn [431, 702]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '50.0 km/h', 'road': '120.0 km/h (33.33 m/s)', 'result': 'FAIL'}, {'location': 'ADAS adasSpeedAlertWeb spawn [431, 702]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '50.0 km/h', 'road': '120.0 km/h (33.33 m/s)', 'result': 'FAIL'}, {'location': 'ADAS reactionTest', 'sign': '—', 'road': '—', 'radar': '—', 'zone': '—', 'adas': 'range [40, 70] km/h (experimental)', 'result': 'SKIP'}]`

| Status | Verificação | Mensagem |
|---|---|---|
| FAIL | Road limits: multiples of 10 km/h | 85 explicit road limits are not multiples of 10: 40.2 km/h (11.18 m/s) ×65; 41.4 km/h (11.5 m/s) ×1; 43.2 km/h (12 m/s) ×8; 56.3 km/h (15.65 m/s) ×11 |
| FAIL | Map zones | not multiples of 10: horizon_estates 48.2 km/h (13.4 m/s); mount_wallis 80.6 km/h (22.4 m/s); the_dockyards 56.2 km/h (15.6 m/s) |
| FAIL | Mission zones (garageToGarage) | not multiples of 10: downtownBelasco 48.2 km/h (13.4 m/s); residential 48.2 km/h (13.4 m/s); dockyard 56.2 km/h (15.6 m/s); mountWallis 80.6 km/h (22.4 m/s) |
| FAIL | Radar speedTrapTrigger2: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| PASS | Radar speedTrapTrigger2 vs road | radar 56.3 km/h (15.65 m/s) == road |
| FAIL | Radar speedTrapTrigger3: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| PASS | Radar speedTrapTrigger3 vs road | radar 56.3 km/h (15.65 m/s) == road |
| FAIL | Radar speedTrapTrigger4: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| FAIL | Radar speedTrapTrigger4 vs road | radar 56.3 km/h (15.65 m/s) ≠ road 100.0 km/h (27.78 m/s) and no zone regulates the radar value |
| FAIL | Radar speedTrapTrigger5: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| PASS | Radar speedTrapTrigger5 vs road | radar 56.3 km/h (15.65 m/s) == road |
| FAIL | Radar speedTrapTrigger6: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| PASS | Radar speedTrapTrigger6 vs road | radar 56.3 km/h (15.65 m/s) == road |
| FAIL | Radar speedTrapTrigger7: regulatory value | 56.3 km/h (15.65 m/s) is not a multiple of 10 km/h |
| PASS | Radar speedTrapTrigger7 vs road | radar 56.3 km/h (15.65 m/s) == road |
| FAIL | Speed sign 5 mph: unit | 37 signs show mph; project rule is km/h (R-19) |
| FAIL | Speed sign 5 mph vs road | 37/37 signs disagree with the road limit next to them (roads: [30.0, 60.0] km/h) |
| FAIL | Speed sign 25 mph: unit | 11 signs show mph; project rule is km/h (R-19) |
| FAIL | Speed sign 25 mph vs road | 11/11 signs disagree with the road limit next to them (roads: [30.0, 60.0] km/h) |
| FAIL | ADAS event01SpeedLimitRecognition (speed_limit_detection) | threshold 70.0 km/h ≠ road limit at the scenario start (40.2 km/h (11.18 m/s)); limit-alert systems must follow the regulated road |
| FAIL | ADAS adasSpeedAlertTest (speed_limit_alert) | threshold 50.0 km/h ≠ road limit at the scenario start (120.0 km/h (33.33 m/s)); limit-alert systems must follow the regulated road |
| FAIL | ADAS adasSpeedAlertWeb (speed_limit_alert) | threshold 50.0 km/h ≠ road limit at the scenario start (120.0 km/h (33.33 m/s)); limit-alert systems must follow the regulated road |
| SKIP | ADAS reactionTest (experimental_speed_instruction) | experimental_speed_range [40, 70] km/h — excluded from sign == road rule by policy |
| SKIP | Mission arrive/001-bruckellA | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |
| SKIP | Mission arrive/002-bruckellB | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |
| SKIP | Mission arrive/003-bruckellC | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |
| SKIP | Mission arrive/004-bruckellD | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |
| SKIP | Mission arrive/005-Gas | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |
| SKIP | Mission arrive/006-Picolina | speedLimit 216.0 km/h (60 m/s) (maxSpeedActive=false, inactive) |

## Tabela de consistência

| Local | Placa | Via | Radar | Zona | ADAS | Resultado |
|---|---|---|---|---|---|---|
| radar speedTrapTrigger2 @ [-416, 198] | — | 56.3 km/h (15.65 m/s) | 56.3 km/h (15.65 m/s) | — | — | PASS |
| radar speedTrapTrigger3 @ [-305, 325] | — | 56.3 km/h (15.65 m/s) | 56.3 km/h (15.65 m/s) | — | — | PASS |
| radar speedTrapTrigger4 @ [-424, 673] | — | 100.0 km/h (27.78 m/s) | 56.3 km/h (15.65 m/s) | — | — | FAIL |
| radar speedTrapTrigger5 @ [-1002, 1902] | — | 56.3 km/h (15.65 m/s) | 56.3 km/h (15.65 m/s) | — | — | PASS |
| radar speedTrapTrigger6 @ [414, 1646] | — | 56.3 km/h (15.65 m/s) | 56.3 km/h (15.65 m/s) | — | — | PASS |
| radar speedTrapTrigger7 @ [393, 1848] | — | 56.3 km/h (15.65 m/s) | 56.3 km/h (15.65 m/s) | — | — | PASS |
| sign_speed25.dae @ [-274, -58] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-151, 22] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-194, -78] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-169, 155] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-196, -57] | 25 mph (= 40.2 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-260, -54] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-259, -44] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-191, -11] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-144, 22] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-54, 78] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 732] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 748] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 764] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 780] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 796] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-22, 805] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-13, 805] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-4, 805] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-26, 716] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-1, 796] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-1, 780] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-1, 764] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [2, 749] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 716] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 732] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 748] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 764] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 780] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 796] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 812] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-65, 828] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-22, 844] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-13, 844] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [-4, 844] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 828] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 812] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 796] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 780] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 764] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [39, 748] | 5 mph (= 8.0 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [-1044, 2045] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [477, 1613] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [477, 1608] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [477, 1618] | 25 mph (= 40.2 km/h) | 30.0 km/h (8.333 m/s) | — | — | — | FAIL |
| sign_speed25.dae @ [477, 1623] | 25 mph (= 40.2 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [447, 1624] | 5 mph (= 8.0 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [444, 1688] | 5 mph (= 8.0 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| sign_speed5.dae @ [461, 1688] | 5 mph (= 8.0 km/h) | 60.0 km/h (16.67 m/s) | — | — | — | FAIL |
| ADAS event01SpeedLimitRecognition spawn [-472, 155] | — | 40.2 km/h (11.18 m/s) | — | — | 70.0 km/h | FAIL |
| ADAS adasSpeedAlertTest spawn [431, 702] | — | 120.0 km/h (33.33 m/s) | — | — | 50.0 km/h | FAIL |
| ADAS adasSpeedAlertWeb spawn [431, 702] | — | 120.0 km/h (33.33 m/s) | — | — | 50.0 km/h | FAIL |
| ADAS reactionTest | — | — | — | — | range [40, 70] km/h (experimental) | SKIP |

