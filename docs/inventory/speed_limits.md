# Inventário de velocidades (Fase 3)

Levantado em 30/09/2026, BeamNG.drive 0.39.4.0, **somente leitura**: zips do jogo (`content/levels/west_coast_usa.zip`, `assets/*.zip`), `gameplay/` da instalação, código Lua do motor (`lua/ge/map.lua`), mods ADAS em `mods/unpacked/` e consultas ao navgraph em execução via MCP (`map.getMap()`).

Regra de conversão (ver `../LOCALIZATION_RULES.md` §2): `mph × 1,609344` → múltiplo de 10 coerente com a hierarquia; armazenamento em m/s = `km/h ÷ 3,6`.

## 1. Tabela geral

| Contexto | Original | Conversão matemática | Valor PT-BR proposto | Fonte | Dependências |
|---|---:|---:|---:|---|---|
| Placa `sign_speed25.dae` (11 instâncias; ruas locais, acesso ao porto) | 25 mph | 40,23 km/h | **40 km/h** | TSStatic no mapa; atlas `t_roadsigns_b` | R-19 novo (material+mesh); `speedLimit` explícito 11,1111 m/s nas vias adjacentes; `slotTraffic.json` |
| Placa `sign_speed5.dae` (37 instâncias; corredores de estacionamento) | 5 mph | 8,05 km/h | **10 km/h** | TSStatic no mapa | R-19 novo; `speedLimit` explícito 2,7778 m/s nas vias de estacionamento; `slotTraffic.json` |
| Placa desenhada `SPEED LIMIT 15` (pátio industrial) | 15 mph | 24,14 km/h | **20 km/h** | `ind_industrial_signs_d` / `t_industrial_signs_b` | Só visual (área privada) |
| `eca_roadsigns_d` `SPEED LIMIT 50` (atlas do East Coast) | 50 mph | 80,47 km/h | **80 km/h** | atlas | Uso no West Coast não encontrado |
| `eca_roadsigns_d` placas de curva 25 / 35 | 25 / 35 mph | 40,23 / 56,33 | **40 / 60 km/h** | atlas | idem |
| `eca_roadsigns_d` números soltos 40 / 30 / 35 / 15 | mph | 64,4 / 48,3 / 56,3 / 24,1 | 60(70*) / 50 / 60 / 20 | atlas | uso desconhecido (`needs_context`) |
| `ut_roadsigns_d` `RAMP 30 MPH` | 30 mph | 48,28 | **50 km/h** | atlas de Utah | uso no West Coast não encontrado |
| `speed_sign` (dígitos laranja MPH) | mph | — | usar a variante azul **km/h** já existente | textura | uso no West Coast não encontrado |
| DecalRoads com `speedLimit` explícito (35 vias) | 11,18 m/s (25 mph) | 40,25 km/h | **40 km/h = 11,1111 m/s** | `main/MissionGroup/DecalRoads/items.level.json` | navgraph → IA, tráfego, polícia |
| DecalRoads (2 vias) | 11,5 / 12 m/s | 41,4 / 43,2 km/h | **40 km/h** | idem | idem |
| AIWaypointsGroup (30 vias) | 11,18 m/s | 40,25 km/h | **40 km/h** | `main/MissionGroup/AIWaypointsGroup/items.level.json` | idem |
| AIWaypointsGroup (6 vias) | 15,6464 m/s (35 mph) | 56,33 km/h | **60 km/h = 16,6667 m/s** | idem | idem |
| Ilha — `island_ai_roads` (7 + 3 vias) | 12 / 15,6464 m/s | 43,2 / 56,3 | **40 / 60 km/h** | `island/island_ai_roads/items.level.json` | idem |
| Docas — `dock_aiRoads` (2 vias) | 15,6464 m/s | 56,33 | **60 km/h** | `island_shippingYard/dock_aiRoads/items.level.json` | idem |
| Radares `trafficCameras_wip/speedCamera_002…007` (6) | 15,6464 m/s (35 mph) | 56,33 | **60 km/h** (igualar à via; ver nota) | `items.level.json` de cada radar | `gameplay/speedTraps` (multa, mensagem, carreira) |
| Zonas `city.sites.json`: horizon_estates / the_dockyards / mount_wallis | 13,4 / 15,6 / 22,4 m/s (30/35/50 mph) | 48,2 / 56,2 / 80,6 | **50 / 60 / 80 km/h** | `city.sites.json` (`customFields.speedLimit`) | zonas de tráfego (`trafficType`) |
| Missões garageToGarage: downtownBelasco / residential / dockyard / mountWallis | 13,4 / 13,4 / 15,6 / 22,4 m/s | 48,2 / 48,2 / 56,2 / 80,6 | **50 / 50 / 60 / 80 km/h** | `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | pontuação/penalidade por excesso |
| Missões `arrive/001…006` | 60 m/s | 216 km/h | **inalterado** | `gameplay/missions/west_coast_usa/arrive/*/info.json` | `maxSpeedActive=false` (inativo) |
| `slotTraffic.json` | cópia do navgraph (m/s) + `roadCategories` urban 50 / rural 80 / highway 120 km/h | — | **regenerar** junto | `levels/west_coast_usa/slotTraffic.json` | novo sistema de tráfego |
| Limites automáticos do motor | lista métrica 30/50/60/80/100/120 km/h | — | **inalterado** (já métrico) | `lua/ge/map.lua` `createSpeedLimits(true)` | navgraph |
| Cenário `busdriver_stunt_minspeed` | 15 m/s mín. | 54 km/h | **inalterado** | `scenarios/busdriver_stunt/…minspeed.lua` | exibe na unidade do jogador |
| ADAS `event01SpeedLimitRecognition` | 70 / 65 km/h | — | **inalterado** (já km/h) | `mods/unpacked/adas_event01_speed_limit/lua/ge/extensions/…lua` | ver `speed_dependencies.md` |
| ADAS `adasSpeedAlertTest` / `adasSpeedAlertWeb` | 50 km/h (`SpeedLimitKmh`) | — | **inalterado** | `…/lua/ge/extensions/adasSpeedAlert*.lua` + flowgraph | idem |
| `reactionTest` | faixa 40–70 km/h (instrução) | — | **inalterado** | `…/reactionTest.lua` | idem |

\* 70 se coexistir com 35 mph no mesmo contexto (regra de hierarquia).

## 2. Distribuição do limite funcional atual (navgraph em execução)

`map.getMap()` com o West Coast carregado — 9.337 arestas:

| km/h | Arestas | Origem |
|---:|---:|---|
| 30 | 3.292 | automático |
| 40,2 | 200 | explícito 11,18 m/s (25 mph) |
| 41,4 | 1 | explícito 11,5 m/s |
| 43,2 | 58 | explícito 12 m/s |
| 50 | 674 | automático |
| 56,3 | 96 | explícito 15,6464 m/s (35 mph) |
| 60 | 2.579 | automático |
| 80 | 906 | automático |
| 100 | 1.049 | automático |
| 120 | 482 | automático |

**96 % da malha já está em múltiplos de 10 km/h.** Só as 355 arestas com valores explícitos herdados de mph precisam ser convertidas.

## 3. Inconsistências do jogo original

Limite funcional medido na via mais próxima de cada placa:

| Placa | Instâncias | Limite funcional ao lado hoje |
|---|---:|---|
| 5 mph (≈ 8 km/h) | 37 | 30 km/h (34) · 60 km/h (3) |
| 25 mph (≈ 40 km/h) | 11 | 60 km/h (9) · 30 km/h (2) |
| Radar 35 mph | 6 | 43,2 · 56,3 (3) · 60 · **100** km/h |
| `s_sign_lightcam` | 1 | 40,2 km/h |

Ou seja: **hoje placa e comportamento já divergem**. A localização deve fechar essa lacuna, definindo `speedLimit` explícito nas vias junto às placas (via local: 40; estacionamento: 10).

## 4. Hierarquia proposta (West Coast localizado)

| Tipo de via (MBST-I Tabela 1) | Valor |
|---|---:|
| Estacionamento / pátio | 10 (placa 5 mph) · 20 (pátio industrial) |
| Via local (placas 25 mph; vias 11,18/11,5/12 m/s) | 40 |
| Via coletora / zonas urbanas residenciais (30 mph) | 50 |
| Docas e vias de 35 mph | 60 |
| Automáticos existentes (arterial, rural, rodovia) | 60 / 80 / 100 / 120 (inalterados) |
| Montanha — zona Mount Wallis (50 mph) | 80 |

## 5. Pendências de contexto
- Radar `speedCamera` junto a `junction1_wp25` (via automática de 100 km/h): igualar a 100 ou definir 60 explícito na via? Decisão caso a caso.
- `eca_roadsigns_d` números soltos (40/30/35/15): uso real desconhecido (atlas de outro mapa).


## Atualização da Fase 5 (implementado)

- **40 km/h:** 83 vias a 11,1111 m/s.
  - 74 explícitas herdadas de 25 mph (65 com 11,18, 8 com 12 e 1 com 11,5);
  - 9 vias vistas pelas placas de 25 mph.
- **10 km/h:** 18 vias a 2,7778 m/s (faixas das cabines das docas e caminhos de estacionamento junto às placas de 5 mph).
- **Correção do inventário:** das "37 placas de 5 mph", só **7** são placas. As outras 30 (`port/portNumbersSigns`) são decalques de malha (`sign_speed5.dae`, `decalType: Visible Mesh Final`) que formam o fundo dos números das baias do porto.
- Decisões por via em `working/speed/speed_changes.json`; detalhes em `docs/production/PHASE5_ROADSIGNS.md` e `tests/reports/phase5_speed_delta.md`.
- Grupos 60/50/80, radares, zonas e ADAS **não** foram alterados.
