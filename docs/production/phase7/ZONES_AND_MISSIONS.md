# Fase 7 — Zonas e missões

**Decisões:** `working/functional/zone_changes.json`. **Aplicação:** cópia do arquivo do jogo no mod, com só os valores declarados trocados (substituição token a token, conferida por releitura completa do JSON).

## Consumidores

Busca em `lua/` e `gameplay/missionTypes/garageToGarage` (0.39.4): **nenhum código lê o `speedLimit` das zonas.** O flowgraph do garageToGarage usa as zonas para sortear origem e destino, não a velocidade. Os valores são dado. Foram mantidos coerentes com a hierarquia em km/h, como pede a especificação.

## Zonas do mapa (`levels/west_coast_usa/city.sites.json`, override de nível)

| Zona | Antes (m/s) | Depois | Contexto (arestas do navgraph dentro do polígono) |
|---|---|---|---|
| horizon_estates | 13,3999996 (30 mph) | 13,8889 (50) | residencial urbana (`trafficType residential`); vias a 60/80 automático |
| the_dockyards | 15,6000004 (35 mph) | 16,6667 (60) | docas (`commercial`); 80/100 automático; radar 6 dentro (60 = via) |
| mount_wallis | 22,3999996 (50 mph) | 22,2222 (80) | serra; vias a 30/60 automático pela curvatura, que continuam valendo em cada via. 80 é o teto regional (rural), não sobe nenhuma via |

## garageToGarage (`gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json`)

É um arquivo do jogo base, fora do nível, por isso o override fica em `gameplay/…` no mod. A instalação não foi tocada.

| Zona | Antes | Depois |
|---|---|---|
| downtownBelasco | 13,3999996 | 13,8889 (50) |
| residential | 13,3999996 | 13,8889 (50) |
| dockyard | 15,6000004 | 16,6667 (60) |
| mountWallis | 22,3999996 | 22,2222 (80) |

**Smoke test** (`tests/reports/phase7/zones_missions_qa.md`):
- o VFS resolve os dois arquivos para o mod, e os valores lidos no jogo são os novos;
- a missão `garageToGarage/003-Dockyard` iniciou;
- depois de **Iniciar**, o fluxo sorteou um trabalho a partir da zona Docas ("Soliad Lansdale de Docas para Pista de corrida") e criou o veículo;
- erros: só um aviso genérico de etapa do `missionManager` (timeout de 5 s);
- capturas em `tests/screenshots/phase7/adas/garage_dockyard_*.jpg`.

## Missões arrive

As 6 missões `arrive` têm `speedLimit` 60 m/s com `maxSpeedActive = false` (reconfirmado pelo validador). Funcionalidade inativa: **não alteradas**. O validador as marca como `SKIP — inactive functionality`.

## Validador

`validate.py speeds` passou a ler `city.sites.json` e `garages.sites.json` com a precedência do VFS (arquivo do mod antes do arquivo do jogo), como já fazia com `items.level.json`. Resultado: map zones 3/3 e mission zones 4/4 PASS. As regras e as tolerâncias não mudaram.
