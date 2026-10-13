# Fase 7 — Integração funcional de velocidades, radares, zonas, missões e ADAS

**Período:** 06–13/10/2026 · **Mapa:** West Coast USA (BeamNG.drive 0.39.4.0) · **Mod:** 0.7.0

**Situação:** a camada funcional da localização está concluída.
- Placa = via = radar = zona = missão = ADAS de limite, em km/h, nos itens regulamentares do West Coast.
- Validador de velocidade: **13 → 0 FAIL**, sem mudança de regra, tolerância ou SKIP.
- O Reaction Test segue como faixa experimental.

## Entrada

Antes de qualquer mudança:
- Fase 6 concluída (v0.6.0, `1e44b9a`, publicada em `origin/main`);
- leitura obrigatória feita;
- snapshot `validate.py speeds --refresh` salvo em `tests/reports/phase7/speed_before.md/json`, com 13 FAIL:
  - 11 vias a 56,3;
  - 3 zonas do mapa e 4 zonas de missão em mph;
  - 6 radares com valor de mph e o radar 4 ≠ via;
  - os 3 ADAS de limite fora da via no início.

## Plano e reprodutibilidade

- **`working/functional/phase7_plan.json`:** 19 entradas (id, tipo, alvo km/h e m/s, vias, zonas, radares, missões, placas, motivo, status). O gerador recusa decisão sem entrada no plano e confere se cada objeto listado no plano mudou exatamente como declarado.
- **Decisões:**
  - `working/functional/{speed_changes, radar_changes, zone_changes, adas_zones, fuel_units, speed_plates}.json`;
  - tiles: `working/layered/t_roadsigns/{speed_plate_tiles, toll_booth_tiles}.json`.
- **Gerador único e determinístico:** `tools/production/apply_phase7_functional.py`. Junta Fase 5 e Fase 7 sobre o motor `speed_overrides.py` (que agora delega a ele) e faz, numa execução:
  - os `items.level.json`;
  - o grupo novo `ptbr_functional_signs`;
  - o `slotTraffic.json`;
  - `city.sites.json`, `garages.sites.json` e `info.json`;
  - o `sign_regulation.json`;
  - o diff estruturado `tests/reports/phase7/functional_diff.md/json`.

  `--check` verifica; `--scenarios` aplica o patch do cenário de pesquisa do Event 01, fora do repositório e com backup.
- **Overrides que são cópias de arquivos do jogo** continuam fora do Git (`.gitignore`) e são regenerados a partir da instalação local. A instalação do jogo não foi tocada.

## Resultado por bloco

| Bloco | Resultado | Documento |
|---|---|---|
| A — limites | 8 vias ex-35 mph → 60; DR652 → 70 (Event 01); DR312 → 50 (ADAS); DR758 120 explícito; waypoints inertes alinhados a 100; 100/120 automáticos preservados; 10/40 da Fase 5 intactos | [SPEED_LIMITS](phase7/SPEED_LIMITS.md) |
| B — radares | radar = via fiscalizada: 2 → 70, 3/5/6/7 → 60, 4 → 100 (sem zona, placa ou transição de 60); tolerância de 10 % e o `11.176` de exemplo preservados; 18/18 passagens no jogo | [RADARS](phase7/RADARS.md) |
| C — zonas e missões | city.sites 50/60/80; garageToGarage 50/50/60/80 por override em `gameplay/`; arrive inativas não alteradas (SKIP); missão Docas executada | [ZONES_AND_MISSIONS](phase7/ZONES_AND_MISSIONS.md) |
| D — slotTraffic | regenerado pelo método da Fase 5 (1109 linhas); 0 valores de mph; 0 casos navgraph 60 × slot 56,3 | [SLOTTRAFFIC](phase7/SLOTTRAFFIC.md) |
| E — ADAS 50 | `SpeedLimitKmh = 50` inalterado; zona de 50 no DR312 (a via sob o spawn); R-19 50 na entrada e à frente do spawn; R-19 120 na saída; <50 sem alerta, >50 alerta, redução desliga | [ADAS_50](phase7/ADAS_50.md) |
| F — Event 01 | alerta 70 / rearme 65 inalterados; corredor 70 na avenida DR652; início movido para o corredor (a via original é local, a 40); R-19 70 na entrada e repetição; 65/69 sem alerta, 70 alerta no corredor, rearme a 64,8, novo alerta | [EVENT01_70](phase7/EVENT01_70.md) |
| G — Reaction Test | sem zona, navgraph ou placa próprios; smoke test `armed → event → finished`. Efeito colateral documentado: a zona de 50 do ADAS passa sob o mesmo spawn | [ADAS_50](phase7/ADAS_50.md) |
| H — combustível | `localUnits` removido (o padrão métrico do jogo; não existe string de litro); preço por litro nos painéis; custo inalterado; sem câmbio | [FUEL_UNITS](phase7/FUEL_UNITS.md) |
| I — validador | FAIL 13 → 0. Checagens novas: placas do `roadsigns.dae` e da praça de pedágio; zonas lidas com precedência do VFS | `tests/reports/phase7/speed_after.md` |
| Placas herdadas da Fase 6 | 23 SPEED LIMIT do `roadsigns.dae` → R-19 com o limite da via regulada; 24 advertências MPH → km/h; cabine DO NOT STOP / SPEED LIMIT 25 → NÃO PARE / R-19 40, com as 5 faixas a 40 | [SPEED_PLATES](phase7/SPEED_PLATES.md) |

## Assets criados (só os que comunicam a mudança funcional)

- **R-19 50 / 70 / 120:** derivados do master aprovado da Fase 5 (`build_r19.py` + `r19_mesh.py`). Números de 3 dígitos na largura mais estreita da mesma fonte; as saídas de 10 e 40 ficaram idênticas byte a byte. Materiais `roadsigns_ptbr_r19_{50,70,120}` e `.cdae` do jogo. São 7 instâncias novas (placa + poste).
- **`t_roadsigns`:** 19 tiles novos em espaço livre (faces das placas e cabines); os 54 elementos das Fases 5/6 ficaram idênticos.
- **Malhas `roadsigns.dae` e `s_toll_booth_center(_alt).dae`:** só re-apontamento de UV quad a quad, com `.cdae` do jogo.

## QA (tudo em `tests/reports/phase7/` e `tests/screenshots/phase7/`)

- Matriz do navgraph 19/19.
- IA 7/7.
- Radares 18/18.
- ADAS 50 ×2, Event 01 e Reaction Test.
- garageToGarage.
- MOD OFF/ON com cache limpo.
- Smoke visual sem regressão.
- Validadores: selftest 121, regressão 10/10, mod 273, `mod --installed` 274, new 108, speeds FAIL 0.
- 59 testes unitários.

Resumo em [`regression_summary.md`](../../tests/reports/phase7/regression_summary.md).

## Limitações e registros

- **Granularidade por DecalRoad:** a zona de 50 é o DR312 inteiro (1268 m). Encurtá-la exigiria dividir o objeto.
- **Event 01:** o alerta do cenário é só por velocidade. Uma segunda passagem por 70 depois do corredor de 216 m ocorre na alça seguinte (60/80).
- **Reaction Test:** o tráfego ambiente roda a 50 na zona ADAS, e o participante vê R-19 50 com a instrução 40–70. Fica para o pesquisador avaliar. O teste automático gravou um resultado em `settings/reaction_test/results/reaction_1791337000_8277.json`; não é dado de participante.
- **Placas urbanas a 100** (Chinatown, trevo junction1): mostram o limite automático do motor. Reduzir a via é decisão de limite urbano, para revisão humana.
- **Placas da arrancada:** mostram a velocidade de saída em mph por código global do jogo (`gameplay/drag/display.lua`, todos os mapas; a timeslip já mostra KM/H). Não foram alteradas.
- **Painel de preço do posto** (`s_fuel_sign_trilobite.dae`: SELF SERVE GASOLINE, Unleaded, FOOD MART): textos em inglês, fora da matriz. É trabalho visual e foi registrado para a Fase 8.
- **Sessão MCP fora do freeroam:** o `gameplay_speedTraps` não carrega; os testes de radar o carregam explicitamente. Numa sessão nova, o motor do carro do jogador começa desligado (os testes ligam a ignição).

## Ferramentas novas

| Arquivo | Função |
|---|---|
| `tools/production/apply_phase7_functional.py` | build e verificação |
| `working/functional/place_signs.py` | posições das placas, medidas no navgraph |
| `working/functional/speed_plates_survey.py` | levantamento das placas do `roadsigns.dae` e da via que cada uma regula |
| `working/layered/t_roadsigns/speed_plate_tiles.py`, `toll_booth_tiles.py` | faces novas |
| `working/functional/{ai_test, radar_test, adas_test, navgraph_matrix, slot_consistency, mod_off_check, sign_shots, plate_shots, qa_reports}.py` | QA no jogo |
