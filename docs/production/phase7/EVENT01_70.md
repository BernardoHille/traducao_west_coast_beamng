# Fase 7 — Event 01: corredor de 70 km/h

O Event 01 dispara o alerta ADAS a **70 km/h** e rearma a **65**. Os dois valores já estão em km/h e **não mudaram** (não se troca 70 por 40). O problema era o cenário viário.

## Rota (medida no navgraph)

- **Início original:**
  - (−472,5; 155,0) + 2 m à direita, voltado para o leste, no semáforo do fim do **DR272**;
  - o DR272 é uma via local, com 25 mph explícito, a **40 km/h desde a Fase 5** (valor que deve permanecer);
  - o validador acusava "70 ≠ 40 no início".
- **Percurso do experimento:**
  - cruzamento DR186_4 → conector DR192;
  - entra na **pista norte da avenida dividida, DR652** (2 faixas, mão única, 216 m, 35 mph explícito);
  - depois segue pela alça DR663/DR659 → Bridge36, com limites automáticos de 100/80/60.
- **O desenho antigo do próprio autor** (`_archive/…zones_v1`): zona de 70 do início até o meio do DR652, depois 40. Ou seja, o corredor de 70 é a avenida.

## Decisão

| Item | Decisão |
|---|---|
| Corredor | **DR652 inteiro a 19,4444 m/s (70)**. É uma avenida dividida, não uma rua residencial. 216 m bastam para chegar a 70 (o teste chega aos 70 a cerca de 110 m) |
| Pista sul (DR666) | 60, pela regra dos ex-35 mph; o experimento não a usa |
| Radar 2 | Fica no corredor, então vai a 70 (dispara acima de 77) |
| Início | **Movido 45 m à frente, para a faixa da direita do DR652, 12 m depois do cruzamento** (spec §32: a rota original não comporta 70 no início, porque o DR272 é local e a 40). Direção (0,366; 0,931) |
| Placas | R-19 70 a ~20 m à frente do início (entrada do corredor) e repetição depois dos cruzamentos laterais (autojunction_86, DR187_2), ambas à direita |
| Saída | O DR652 termina na alça DR663/DR659 (outra via, limite automático do jogo). Sem placa, como as demais alças do mapa |

## Patch do cenário de pesquisa (fora do repositório)

Mod `adas_event01_speed_limit` em `current/mods/unpacked`. O patch é aplicado por `apply_phase7_functional.py --scenarios`, com o texto antigo conferido antes de trocar, e o backup fica no `_archive/` do próprio mod (`*.pre_ptbr_phase7`):

- `lua/ge/extensions/event01SpeedLimitRecognition.lua`: `playerSpawn = vec3(-428.227, 164.318, 100.31)`, `startRoadDirection = (0.3661, 0.9306)`, com comentário da Fase 7 e do valor original;
- `gameplay/missions/…/001-speedLimitRecognition/info.json`: marcador de início (`startTrigger.pos/rot`) no novo ponto; o texto do cartão deixou de dizer "Parta do semáforo".

O patch é do mod de pesquisa, não do mod de tradução: com a tradução desligada, o Event 01 continua começando no corredor, que volta a 56,3 km/h.

## Testes (`tests/reports/phase7/adas_qa.md`)

| Situação | Resultado |
|---|---|
| Navgraph no novo início | 70 km/h (aresta DR192_5 → DR652_2) |
| 65 km/h e depois 69 km/h | nenhum alerta (máx. 68,4) |
| ≥ 70 | `SPEED LIMIT REACHED`, alerta #1 a 70,8 km/h, **dentro do corredor (via 70)** |
| acima de 70 mantido | nenhum novo alerta |
| redução abaixo do rearme | `Speed alert rearmed (64.8 km/h)` |
| acima de 70 de novo | alerta #2 a 70,0 km/h |

**Observação:** no teste, o alerta #2 ocorreu depois do fim do corredor (216 m), na alça Bridge36 (60). O alerta do Event 01 é só por velocidade, não por posição, e isso é comportamento original do cenário. O evento principal (primeira passagem por 70) acontece no corredor regulamentado a 70.

**Capturas:** `tests/screenshots/phase7/adas/event01_*.jpg`. O cenário fixa a hora em ~22 h, então a cena é noturna. As placas aparecem de dia em `tests/screenshots/phase7/signs*/r19_70_*.jpg`.
