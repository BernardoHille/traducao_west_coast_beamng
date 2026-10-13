# Fase 7 — ADAS Speed Alert: zona de 50 km/h

**Princípio** (Fase 4): o ADAS de alerta de limite acompanha o limite regulamentado do cenário. O cenário testa 50 km/h, então **`SpeedLimitKmh = 50` não muda**. O que muda é a via, que passa a ser um trecho regulamentado de 50.

## Rota efetiva (medida no navgraph)

- **Cenários:** `adasSpeedAlertTest` e `adasSpeedAlertWeb`.
  - Spawn em (431,2; 701,6; 115,9), direção (−0,80; −0,60), sudoeste.
  - Direção livre, sem NPC, sem tráfego.
- **Via:** pista sudoeste da via expressa, 4 faixas, mão única. A aresta sob o spawn é `DR253_6 → DR312_9`, a 1 m do eixo do **DR312**.
  - DR312 é uma via de IA invisível (`road_invisible`) de 1268 m.
  - Começa em DR694_9 (556,8; 790,0), cerca de 190 m antes do spawn, e termina em (−415; −20), cerca de 1030 m depois, onde continua o DR758.
- **Interseções no trecho:**
  - logo no spawn, a alça DR253 sai pela direita;
  - aos ~632 m, uma saída (BeamNGWaypoint_1 → DR562, 100);
  - aos ~761 m, um retorno de serviço (DR528, dirigibilidade 0,5);
  - nenhuma entrada pública dentro da zona além do início (DR694 e a alça DR277 se juntam antes dela).

## Zona

| Item | Decisão |
|---|---|
| Trecho | **DR312 inteiro** a 13,8889 m/s (50). O limite é por objeto DecalRoad. Encurtar a zona exigiria dividir o objeto (mudar a geometria), o que esta fase não faz. A zona cobre ~190 m antes e ~1030 m depois do spawn; a via expressa continua a 120 antes e depois |
| Entrada | R-19 50 nos dois lados, 25 m depois do início do DR312 (direita a 2 m da faixa; esquerda junto à mureta central) |
| À frente do spawn | R-19 50 no canteiro central, 45 m à frente (visível da posição inicial; à direita, ali, está a alça DR253) e repetição à direita a 200 m, quando a alça já se separou. O participante não começa sob uma regra sem placa |
| Saída | Fim do DR312 → DR758, na mesma pista: R-19 120, 25 m depois da transição. O DR758 recebe 120 explícito (= automático), para a placa regular uma via com limite declarado |
| Saída pela alça (632 m) | Sem placa: é outra via (alça), com o limite automático do jogo. Nenhuma alça do mapa original tem placa |

As placas são TSStatic novos (`sign_r19_50.dae` / `sign_r19_120.dae` + poste `pole_fence1`), montados como uma placa original do mapa (altura 2,224 m, poste invertido 0,11 m atrás). Ficam no grupo novo `MissionGroup/ptbr_functional_signs`. As posições foram medidas no jogo por `working/functional/place_signs.py` e fixadas em `working/functional/adas_zones.json`.

## Testes (`tests/reports/phase7/adas_qa.md`)

| Etapa | ADAS Speed Alert | ADAS Speed Alert Web |
|---|---|---|
| Navgraph no spawn | 50 km/h | 50 km/h |
| A: abaixo de 50 (40 km/h) | sem alerta | sem alerta |
| B: acima de 50 | alerta a 53,9 km/h | alerta a 54,5 km/h |
| C: redução | desliga a 42,3 km/h | desliga a 42,7 km/h |
| Amostras na zona | todas a 50 | todas a 50 |

As linhas `ALERT START/STOP` do log dependem do parâmetro `DebugEnabled` do flowgraph. Abertos pelo `load()`, os cenários não as escrevem. A transição foi conferida pelos contadores do controlador (`alertStartCount`, `alertStopCount`).

A placa R-19 50 do canteiro central aparece na captura do ponto de vista do motorista no início (`tests/screenshots/phase7/adas/speed_alert_spawn.jpg`).

## Efeito colateral: Reaction Test

O Reaction Test usa o mesmo spawn e a mesma via.

- **Tráfego ambiente:** os 5 veículos seguem o limite e passam a rodar a ~50 km/h na zona.
- **Veículo da fechada:** usa velocidade fixa ('set') e não muda.
- **Placa × instrução:** o participante vê R-19 50 enquanto a instrução do experimento é "dirija entre 40 e 70 km/h". A faixa 40–70 é experimental (decisão fechada: sem zona, sem navgraph, sem placa). Fica registrado para o pesquisador avaliar no briefing.
- **Smoke test:** fases `armed → event → finished`, fechada completa, sem erro.
