# Fase 7 — QA dos cenários ADAS

Gerado a partir de `adas_qa.json` (`working/functional/adas_test.py`). Cada cenário foi aberto pelo próprio `load()` (freeroam sem tráfego, como o usuário inicia), isolado dos outros controladores, e o Honda foi dirigido pela IA em velocidades-alvo ('set'), o mesmo método da validação original dos cenários.

## ADAS Speed Alert (teste) — PASS

- Spawn [431.7, 702.3, 115.9], aresta `DR253_6` → `DR312_9`, navgraph **50.0 km/h**; limiar 50 km/h (inalterado).
- A (< 50): máx. 40.0 km/h, sem alerta.
- B (> 50): alerta ativo a 53.9 km/h.
- C (redução): alerta desligado a 42.3 km/h.
- Todas as amostras na zona: limite 50 km/h.
- Checagens: spawn_on_50 = True, A_no_alert_below_50 = True, B_alert_above_50 = True, C_alert_stops_below_50 = True, all_samples_in_zone_are_50 = True, state_transitions_start_stop = True

Capturas: `tests/screenshots/phase7/adas/speed_alert_spawn.jpg`, `tests/screenshots/phase7/adas/speed_alert_alert_active.jpg`.

## ADAS Speed Alert (web) — PASS

- Spawn [431.7, 702.3, 115.9], aresta `DR253_6` → `DR312_9`, navgraph **50.0 km/h**; limiar 50 km/h (inalterado).
- A (< 50): máx. 40.0 km/h, sem alerta.
- B (> 50): alerta ativo a 54.5 km/h.
- C (redução): alerta desligado a 42.7 km/h.
- Todas as amostras na zona: limite 50 km/h.
- Checagens: spawn_on_50 = True, A_no_alert_below_50 = True, B_alert_above_50 = True, C_alert_stops_below_50 = True, all_samples_in_zone_are_50 = True, state_transitions_start_stop = True

Capturas: `tests/screenshots/phase7/adas/speed_alert_web_spawn.jpg`, `tests/screenshots/phase7/adas/speed_alert_web_alert_active.jpg`.

## Event 01 — PASS

- Novo início [-428.2, 163.3, 100.3], aresta `DR192_5` → `DR652_2`, navgraph **70.0 km/h**; alerta 70 / rearme 65 (inalterados).
- Execução 1 (65 e depois 69 km/h): máx. 68.4 km/h, nenhum alerta.
- Execução 2 (72 → 60 → 72 km/h):
  - alerta #1 a 70.8 km/h, via a 70.0 km/h em [-394.1, 232.7]
  - alerta #2 a 70.0 km/h, via a 60 km/h em [-182.1, 355.8]
- Log: [Event01] SPEED LIMIT REACHED · [Event01] Playing ADAS speed alert (#1) · [Event01] Speed alert rearmed (64.8 km/h) · [Event01] SPEED LIMIT REACHED · [Event01] Playing ADAS speed alert (#2)
- Checagens: spawn_on_70 = True, run1_no_alert_at_65_69 = True, run2_alert_at_70 = True, run2_first_alert_inside_corridor = True, run2_single_alert_while_above = True, run2_rearm_below_65 = True, run2_second_alert = True
- O primeiro alerta acontece dentro do corredor (70). O segundo, no teste, veio depois do corredor (216 m), na alça Bridge36 (60/80): o alerta do Event 01 é só por velocidade, não por posição — comportamento original do cenário.

Capturas (cena noturna fixa do cenário): `tests/screenshots/phase7/adas/event01_spawn.jpg`, `tests/screenshots/phase7/adas/event01_alert.jpg`.

## Reaction Test (smoke) — PASS

- Fases: playerSettling → waitingTraffic → armed → event → finished.
- Fechada: cutInCompleted = True; colisão = True (a IA do teste não reage: caminho de colisão do experimento, previsto na documentação do cenário).
- Tráfego ambiente: 5 veículos; na zona de 50 seguem o limite (amostras ~50 km/h); o veículo da fechada usa 'set' (60).
- Arquivo de resultado gravado pelo próprio cenário: `/settings/reaction_test/results/reaction_1791337000_8277.json` — **gerado pelo teste automático, não é dado de participante** (pode ser apagado pelo pesquisador).
- Faixa 40–70 experimental: sem zona, sem navgraph, sem placa (inalterado).

