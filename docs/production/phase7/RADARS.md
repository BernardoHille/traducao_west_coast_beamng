# Fase 7 — Radares (speed traps)

**Regra:** o radar acompanha o limite regulamentado da via que fiscaliza. **Decisões:** `working/functional/radar_changes.json`.

## Como o jogo fiscaliza (`lua/ge/extensions/gameplay/speedTraps.lua`, 0.39.4)

- Objeto `BeamNGTrigger` com `speedTrapType = speed` e `speedLimit` em m/s (string), evento `enter`.
- Dispara quando `velocidade > speedLimit + speedLimitTolerance`. Como nenhum gatilho do West Coast define `speedLimitTolerance`, vale o padrão `speedLimit * 0.1` (10 %). **Preservado**: a localização troca o limite, não a regra de fiscalização.
- Só no sentido do gatilho (eixo Y do trigger · velocidade > 0), só sem missão em primeiro plano e só com a câmera a até 100 m do carro.
- `11.176` aparece apenas no bloco de comentário `example data` do arquivo. Não é padrão, fallback nem constante usada: é código morto. **Preservado.**
- A extensão é um preset do modo freeroam (`lua/ge/main.lua`).

## Radares

O sentido fiscalizado foi medido no jogo: eixo Y do gatilho contra o fluxo legal da aresta mais próxima. Nos 6 radares o produto escalar foi 1,0.

| Radar | Posição | Via fiscalizada (navgraph) | Limite da via | Zona | Antes | Depois | Dispara acima de |
|---|---|---|---:|---|---|---|---:|
| speedTrapTrigger2 (`4d7dbade`) | (−416, 198) | DR652, corredor do Event 01 | 70 | — | 15,6464 | 19,4444 | 77 |
| speedTrapTrigger3 (`8f20ac08`) | (−305, 325) | DR571 | 60 | — | 15,6464 | 16,6667 | 66 |
| speedTrapTrigger4 (`dbe59e36`) | (−424, 673) | junction1_wp25 → wp19 (automático) | 100 | — | 15,6464 | 27,7778 | 110 |
| speedTrapTrigger5 (`2777327b`) | (−1002, 1902) | DR989, ilha | 60 | — | 15,6464 | 16,6667 | 66 |
| speedTrapTrigger6 (`0a259251`) | (414, 1646) | DR1213, portaria das docas | 60 | the_dockyards 60 | 15,6464 | 16,6667 | 66 |
| speedTrapTrigger7 (`68bbd35b`) | (393, 1848) | DR1009, ilha | 60 | — | 15,6464 | 16,6667 | 66 |

## Radar 4 (o caso fora da curva)

O radar 4 estava a 35 mph (56,3) numa aresta de 100 km/h do trevo junction1. Não há zona de 60, placa de 60 nem transição regulamentada para 60 no sentido que ele fiscaliza. O único dado de 35 mph são os campos inertes dos waypoints wp19/wp25. A placa SPEED LIMIT 30 do `roadsigns.dae` perto dali (reg_07) regula o sentido oposto. Pela decisão padrão do projeto, **radar = 100**, e a via não foi reduzida.

## QA no jogo

Arquivos: `tests/reports/phase7/radar_qa.md` e `radar_test.json`. Em cada passagem, largada lançada antes do radar, IA em velocidade constante pelo gatilho e registro do evento `onSpeedTrapTriggered` do próprio jogo.

- Abaixo do limite (55 / 65 / 95): não dispara.
- Dentro da tolerância de 10 % (65 a 60; 75 a 70; 100 a 100): não dispara.
- Acima da tolerância (70,6 / 66,5 / 70,2 / 74,6 a 60; 80,0 a 70; 118,2 a 100): dispara.
- **18/18 passagens como esperado**, inclusive o radar 4 a 100.
