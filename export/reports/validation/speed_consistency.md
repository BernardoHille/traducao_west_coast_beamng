# Speed consistency

**Alvo:** `west_coast_usa`  

**Resultado:** `FAIL` · PASS 9 · WARN 1 · FAIL 13 · SKIP 7

- snapshot: `{'collected': '2026-09-30T21:38:06', 'level': '/levels/west_coast_usa/main.level.json', 'source': 'MCP map.getMap() + map.findClosestRoad, TSStatic sign_speed*.dae'}`
- rows: `[{'location': 'radar speedTrapTrigger2 @ [-416, 198]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger3 @ [-305, 325]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger4 @ [-424, 673]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '100.0 km/h (27.78 m/s)', 'result': 'FAIL'}, {'location': 'radar speedTrapTrigger5 @ [-1002, 1902]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger6 @ [414, 1646]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'radar speedTrapTrigger7 @ [393, 1848]', 'sign': '—', 'radar': '56.3 km/h (15.65 m/s)', 'zone': '—', 'road': '56.3 km/h (15.65 m/s)', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-1044, 2045]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [477, 1613]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [477, 1608]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [477, 1618]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [477, 1623]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [447, 1624]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [444, 1688]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [461, 1688]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-274, -58]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-151, 22]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-194, -78]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-169, 155]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-196, -57]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_speed25.dae @ [-260, -54]', 'sign': '40 km/h', 'road': '40.0 km/h (11.11 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [-259, -44]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [-191, -11]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [-144, 22]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'sign_r19_10.dae @ [-54, 78]', 'sign': '10 km/h', 'road': '10.0 km/h (2.778 m/s)', 'radar': '—', 'zone': '—', 'result': 'PASS'}, {'location': 'ADAS event01SpeedLimitRecognition spawn [-472, 155]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '70.0 km/h', 'road': '40.0 km/h (11.11 m/s)', 'result': 'FAIL'}, {'location': 'ADAS adasSpeedAlertTest spawn [431, 702]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '50.0 km/h', 'road': '120.0 km/h (33.33 m/s)', 'result': 'FAIL'}, {'location': 'ADAS adasSpeedAlertWeb spawn [431, 702]', 'sign': '—', 'radar': '—', 'zone': '—', 'adas': '50.0 km/h', 'road': '120.0 km/h (33.33 m/s)', 'result': 'FAIL'}, {'location': 'ADAS reactionTest', 'sign': '—', 'road': '—', 'radar': '—', 'zone': '—', 'adas': 'range [40, 70] km/h (experimental)', 'result': 'SKIP'}]`

| Status | Verificação | Mensagem |
|---|---|---|
| FAIL | Road limits: multiples of 10 km/h | 11 explicit road limits are not multiples of 10: 56.3 km/h (15.65 m/s) ×11 |
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
| PASS | Speed sign 10 km/h: unit | 7 signs show km/h (R-19 mesh of the mod) |
| PASS | Speed sign 10 km/h vs regulated roads | 7 signs == explicit limit of the 18 distinct road(s) they regulate |
| PASS | Speed sign 40 km/h: unit | 11 signs show km/h (R-19 mesh of the mod) |
| PASS | Speed sign 40 km/h vs regulated roads | 11 signs == explicit limit of the 9 distinct road(s) they regulate |
| WARN | Speed signs: nearest navgraph edge | 14/18 signs: nearest edge == sign value; 4 differ (sign at a transition: e.g. dock booths, where the sign regulates the next road) |
| FAIL | ADAS event01SpeedLimitRecognition (speed_limit_detection) | threshold 70.0 km/h ≠ road limit at the scenario start (40.0 km/h (11.11 m/s)); limit-alert systems must follow the regulated road |
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
| sign_speed25.dae @ [-1044, 2045] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [477, 1613] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [477, 1608] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [477, 1618] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [477, 1623] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [447, 1624] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [444, 1688] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [461, 1688] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-274, -58] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-151, 22] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-194, -78] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-169, 155] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-196, -57] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_speed25.dae @ [-260, -54] | 40 km/h | 40.0 km/h (11.11 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [-259, -44] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [-191, -11] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [-144, 22] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| sign_r19_10.dae @ [-54, 78] | 10 km/h | 10.0 km/h (2.778 m/s) | — | — | — | PASS |
| ADAS event01SpeedLimitRecognition spawn [-472, 155] | — | 40.0 km/h (11.11 m/s) | — | — | 70.0 km/h | FAIL |
| ADAS adasSpeedAlertTest spawn [431, 702] | — | 120.0 km/h (33.33 m/s) | — | — | 50.0 km/h | FAIL |
| ADAS adasSpeedAlertWeb spawn [431, 702] | — | 120.0 km/h (33.33 m/s) | — | — | 50.0 km/h | FAIL |
| ADAS reactionTest | — | — | — | — | range [40, 70] km/h (experimental) | SKIP |

