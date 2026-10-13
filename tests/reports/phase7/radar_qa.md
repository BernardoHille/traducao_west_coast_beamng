# Fase 7 — QA dos radares

Gerado por `working/functional/qa_reports.py` a partir de `radar_test.json` (`working/functional/radar_test.py`).

Método: largada lançada 25–45 m antes de cada radar (teleporte + velocidade inicial no sentido fiscalizado), IA em velocidade constante ('set') pelo gatilho, câmera do jogo seguindo o carro. O evento `onSpeedTrapTriggered` do próprio `gameplay/speedTraps.lua` é registrado (o jogo dispara acima de limite + 10 %). Num nível carregado pelo MCP o jogo não está em modo freeroam, então a extensão `gameplay_speedTraps` (preset do freeroam) foi carregada antes do teste.

| Radar | Limite | Dispara acima de | Alvo | Velocidade no gatilho | Disparou | Esperado | Resultado |
|---|---:|---:|---:|---:|---|---|---|
| speedTrapTrigger2 | 70 | 77.0 | 65 | 65.2 | não | não | PASS |
| speedTrapTrigger2 | 70 | 77.0 | 75 | 72.1 | não | não | PASS |
| speedTrapTrigger2 | 70 | 77.0 | 80 | 80.0 | sim | sim | PASS |
| speedTrapTrigger3 | 60 | 66.0 | 55 | 53.9 | não | não | PASS |
| speedTrapTrigger3 | 60 | 66.0 | 65 | 64.9 | não | não | PASS |
| speedTrapTrigger3 | 60 | 66.0 | 70 | 70.6 | sim | sim | PASS |
| speedTrapTrigger4 | 100 | 110.0 | 95 | 90.3 | não | não | PASS |
| speedTrapTrigger4 | 100 | 110.0 | 105 | 99.9 | não | não | PASS |
| speedTrapTrigger4 | 100 | 110.0 | 125 | 118.2 | sim | sim | PASS |
| speedTrapTrigger5 | 60 | 66.0 | 55 | 55.6 | não | não | PASS |
| speedTrapTrigger5 | 60 | 66.0 | 65 | 60.3 | não | não | PASS |
| speedTrapTrigger5 | 60 | 66.0 | 80 | 74.6 | sim | sim | PASS |
| speedTrapTrigger6 | 60 | 66.0 | 55 | 54.4 | não | não | PASS |
| speedTrapTrigger6 | 60 | 66.0 | 65 | 65.1 | não | não | PASS |
| speedTrapTrigger6 | 60 | 66.0 | 70 | 70.2 | sim | sim | PASS |
| speedTrapTrigger7 | 60 | 66.0 | 55 | 55.5 | não | não | PASS |
| speedTrapTrigger7 | 60 | 66.0 | 65 | 61.9 | não | não | PASS |
| speedTrapTrigger7 | 60 | 66.0 | 70 | 66.5 | sim | sim | PASS |

**Resultado:** PASS (18 passagens). Nos radares 4 e 5 (curva) a IA perde ~6 km/h antes do gatilho; por isso os alvos mais altos (125 / 80) — o que conta é a velocidade medida no gatilho.
