# Dependências funcionais das velocidades (Fase 3)

Objetivo: permitir que a implementação altere **tudo junto** — placa, limite da via, radares, zonas, missões e ADAS.
Fonte da investigação: leitura do código/dados do jogo e dos mods + consultas via MCP (30/09/2026). Nada foi alterado.

## 1. Como cada sistema representa a velocidade

| Sistema | Onde | Unidade interna | Como obtém o valor |
|---|---|---|---|
| Navgraph (IA, tráfego, polícia) | `lua/ge/map.lua` | **m/s** | `DecalRoad.speedLimit` (campo dinâmico, texto numérico); se ausente/≤0 → `createSpeedLimits(true)` escolhe da lista **métrica** 30/50/60/80/100/120 km/h pelo raio/sentido/dirigibilidade da via |
| Tráfego novo (slots) | `levels/west_coast_usa/slotTraffic.json` | m/s (`roads.*.properties.speedLimit`) e km/h (`roadCategories[].speedKph`) | Arquivo **pré-calculado** a partir das vias — precisa ser regenerado/atualizado junto |
| Infrações do tráfego/polícia | `lua/ge/extensions/gameplay/traffic/vehicle.lua` | m/s | `tracking.speedLimit` do navgraph (excesso ≥ 1,2× o limite, mínimo 16,7 m/s) |
| Radares (speed traps) | `gameplay/speedTraps.lua` + `trafficCameras_wip/speedCamera_*` | m/s | Campo `speedLimit` de cada radar; tolerância padrão de 10 % (`speedLimitTolerance`). O código também contém um valor `"11.176"` (25 mph) na linha 35 — contexto (exemplo ou padrão) não verificado |
| Zonas do mapa | `city.sites.json` → `zones[].customFields.values.speedLimit` | m/s | Número fixo por zona |
| Missões garageToGarage | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | m/s | Número fixo por zona |
| Missões arrive | `…/arrive/*/info.json` `speedLimit` | m/s (+1,39 de tolerância no flowgraph) | Fixo; **inativo** (`maxSpeedActive=false`) |
| ADAS Event 01 | `mods/unpacked/adas_event01_speed_limit/lua/ge/extensions/event01SpeedLimitRecognition.lua` | **km/h** (velocidade m/s × 3,6) | Constantes `alertSpeedKmh = 70`, `rearmSpeedKmh = 65` — **não lê o mapa** |
| ADAS Speed Alert (test/web) | `…/adasSpeedAlertTest.lua`, `…/adasSpeedAlertWeb.lua` + flowgraph | **km/h** | Variável `SpeedLimitKmh = 50` do flowgraph — **não lê o mapa** |
| Reaction test | `…/reactionTest.lua` | km/h | Texto de instrução "entre 40 e 70 km/h" |
| HUD/mensagens | configurações do jogador | conforme `uiUnits` | Jogador atual: `uiUnits: metric` (km/h) |
| Preço de combustível (UI) | `levels/west_coast_usa/info.json` `localUnits` | `gallonUS` | Unidade local do mapa — trocar para litro na implementação |

Sem conversões encadeadas: gravar o valor final em m/s a partir do km/h escolhido (`40 ÷ 3,6 = 11,1111`).

## 2. Árvores de dependência

```text
40 km/h visual (antigo 25 mph)
├── t_roadsigns (NÃO editar glifos) → material/textura R-19 novos
├── mesh levels/west_coast_usa/art/shapes/objects/sign_speed25.dae (override)
├── speedLimit 11.1111 nas DecalRoads junto às 11 placas
│     (DR286, DR459, DR726, DR728, autojunction_134, DR1130, DR1212, DR1221, DR1235)
├── speedLimit 11.1111 nas 35 DecalRoads + 30 AIWaypoints que hoje têm 11.18
├── speedLimit 11.1111 nas vias de 11.5 / 12 m/s (ilha e 2 DecalRoads)
└── slotTraffic.json regenerado

10 km/h visual (antigo 5 mph — estacionamentos)
├── material/textura R-19 "10"
├── mesh sign_speed5.dae (override)
├── speedLimit 2.7778 nas vias de estacionamento junto às 37 placas
│     (DR748, DR837–DR852, DR1165–DR1169, DR459, DR725, DR730, DR773,
│      DR1221, DR1246, DR1261, autojunction_1/151/174/1791)
└── slotTraffic.json regenerado

60 km/h (antigo 35 mph)
├── speedLimit 16.6667 nas 6 AIWaypoints + 3 ilha + 2 docas
├── 6 radares speedCamera_002…007 → 16.6667 (revisar o de 100 km/h)
├── zona the_dockyards (city.sites.json) → 16.6667
├── zona dockyard (garageToGarage) → 16.6667
└── slotTraffic.json

50 km/h (antigo 30 mph)
├── zona horizon_estates (city.sites.json) → 13.8889
└── zonas downtownBelasco + residential (garageToGarage) → 13.8889

80 km/h (antigo 50 mph)
├── zona mount_wallis (city.sites.json) → 22.2222
└── zona mountWallis (garageToGarage) → 22.2222

20 km/h (antigo 15 mph)
└── textura industrial (placa desenhada; sem sistema funcional associado)

ADAS (já em km/h)
├── Event 01: alerta 70 / rearme 65 km/h — spawn (-472,5; 155,0) em via de 25 mph
│     explícita (40,2 km/h) que leva a vias de 30 e 120 km/h
├── Speed Alert 50 / Web / Reaction test: spawn (431,2; 701,6), rota em via de
│     4 faixas com limite AUTOMÁTICO de 120 km/h
└── não dependem de placas nem do navgraph
```

## 3. Conflitos que exigem decisão (não resolvidos na Fase 3)

1. **ADAS × via:** as missões de 50 km/h e o reaction test (40–70 km/h) rodam numa via de **120 km/h** funcional, sem R-19. Para "placa = limite = ADAS" seria preciso **definir 50 km/h explícito nessa rota e instalar R-19 50** (objetos novos no mapa), ou aceitar que o limiar ADAS é experimental e independente da via. **Decisão do dono do projeto (pesquisa ADAS).**
2. **Event 01 (70 km/h):** nenhuma via da rota tem 70. Mesma decisão do item 1.
3. **Radar em via de 100 km/h** (`junction1_wp25`): igualar o radar à via ou a via ao radar.
4. **Arquivos fora do mapa:** `garages.sites.json` está em `gameplay/` da instalação — o override vai no mod em `gameplay/missions/west_coast_usa/...`.
5. **`slotTraffic.json`:** arquivo derivado — confirmar na implementação como regenerá-lo (editor) ou editá-lo de forma consistente.

## 4. Ordem de implementação recomendada (fases futuras)
1. R-19 (material + textura + meshes) e validação visual.
2. `speedLimit` explícito das DecalRoads/AIWaypoints (override dos `items.level.json` do West Coast).
3. `slotTraffic.json`, radares e zonas.
4. QA funcional: IA respeitando 40/10 km/h, radar multando acima de 60, missões garageToGarage.
5. ADAS conforme decisão do §3.


## Atualização da Fase 5 (implementado)

- **40 km/h:** 83 vias a 11,1111 m/s.
  - 74 explícitas herdadas de 25 mph (65 com 11,18, 8 com 12 e 1 com 11,5);
  - 9 vias vistas pelas placas de 25 mph.
- **10 km/h:** 18 vias a 2,7778 m/s (faixas das cabines das docas e caminhos de estacionamento junto às placas de 5 mph).
- **Correção do inventário:** das "37 placas de 5 mph", só **7** são placas. As outras 30 (`port/portNumbersSigns`) são decalques de malha (`sign_speed5.dae`, `decalType: Visible Mesh Final`) que formam o fundo dos números das baias do porto.
- Decisões por via em `working/speed/speed_changes.json`; detalhes em `docs/production/PHASE5_ROADSIGNS.md` e `tests/reports/phase5_speed_delta.md`.
- Grupos 60/50/80, radares, zonas e ADAS **não** foram alterados.
