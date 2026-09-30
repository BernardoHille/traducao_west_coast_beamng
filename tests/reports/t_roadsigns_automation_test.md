# Teste de automação de QA — `t_roadsigns` (Fase 2)

> `t_roadsigns` continua sendo **só PoC**: a textura do mod é a referência PT-BR antiga, usada como marcador visual.
> Este relatório valida o **pipeline de inspeção**, não a tradução. **Nada aqui é aprovação de tradução.**

## Ambiente

- BeamNG.drive 0.39.4.0 (Direct3D12, RTX 4060), mapa `west_coast_usa`
- Mod `traducao_ptbr_wcusa` 0.1.0-poc (`mods/unpacked`)
- Runner `tools/beamng/qa_runner.py` + protocolo `tools/beamng/QA_PROTOCOL.md`
- Presets: `tests/presets/day.json` (`time 0.0`, `windSpeed 0`, `cloudCover 0`), `night.json` (`time 0.5`, idem), `camera_defaults.json` (free cam, FOV 50, UI oculta, 4 s de assentamento)
- Data: 30/09/2026

## Pontos testados (`tests/qa_locations.json`)

Todos confirmados por `getMaterialNames()` = `roadsigns, metal_galvanized` **e** por diferença visual entre original e PoC com a mesma câmera.

| Location id | Shape | Posição | Câmera (pos / quat / FOV) | Elemento |
|---|---|---|---|---|
| `roadsigns_chinatown_stop` | `sign_stop.dae` | (-712.667, 552.899, 122.435) | (-710.782, 550.313, 122.835) / (0.00743, 0.00242, -0.309899, 0.950737) / 50 | STOP → PARE |
| `roadsigns_downtown_yield` | `sign_yield.dae` | (-108.5, 93.2, 127.0) | (-110.5606, 96.0784, 126.7581) / (-0.008825, 0.027138, 0.950593, 0.309125) / 50 | YIELD → DÊ A PREFERÊNCIA |
| `roadsigns_hill_speed25` | `sign_speed25.dae` (+ `sign_stop.dae` no mesmo poste) | (-169.321, 155.466, 123.426) | (-171.7348, 158.6505, 123.1267) / (-0.011993, 0.035447, 0.94659, 0.320262) / 50 | SPEED LIMIT 25; STOP → PARE |

As câmeras foram lidas do jogo com `get_camera_state` (`save-camera`). Descartado: `s_sign_lightcam.dae` (-520.6, 288.5) tem `roadsigns` na lista de materiais, mas as duas faces visíveis mostram só metal. Não serve como ponto visual.

## Execuções

| Run report | Estado | Preset | Recarga | VFS |
|---|---|---|---|---|
| `runs/20260930_162217_t_roadsigns_original_day.json` | original (mod OFF) | day | sim | ✅ `signage.zip` |
| `runs/20260930_162222_roadsigns_chinatown_stop_original_night.json` | original | night | não (mesma carga) | ✅ `signage.zip` |
| `runs/20260930_162416_t_roadsigns_poc_day.json` | poc (mod ON) | day | sim | ✅ `mods\unpacked\traducao_ptbr_wcusa` |
| `runs/20260930_162422_roadsigns_chinatown_stop_poc_night.json` | poc | night | não (mesma carga) | ✅ `mods\unpacked\traducao_ptbr_wcusa` |

Comandos:
```
python tools/beamng/qa_runner.py capture --family t_roadsigns --state original --preset day
python tools/beamng/qa_runner.py capture --location roadsigns_chinatown_stop --state original --preset night --no-reload
python tools/beamng/qa_runner.py capture --family t_roadsigns --state poc --preset day
python tools/beamng/qa_runner.py capture --location roadsigns_chinatown_stop --state poc --preset night --no-reload
```

## Baseline × PoC

Todas as capturas têm 1920×993 PNG, sem pós-processamento.

| Ponto | Baseline | PoC | Diferença média | Pixels alterados (>24) | Onde muda |
|---|---|---|---|---|---|
| chinatown_stop (DAY) | `baseline/t_roadsigns/roadsigns_chinatown_stop_original.png` | `current/t_roadsigns/roadsigns_chinatown_stop_poc.png` | 4,40 | 3,33 % | placa; leve nas bordas das faixas de pedestre e do poste |
| downtown_yield (DAY) | `…/roadsigns_downtown_yield_original.png` | `…/roadsigns_downtown_yield_poc.png` | 1,39 | 1,65 % | triângulo da placa |
| hill_speed25 (DAY) | `…/roadsigns_hill_speed25_original.png` | `…/roadsigns_hill_speed25_poc.png` | 1,54 | 1,94 % | octógono de cima + leve no "SPEED LIMIT" |
| chinatown_stop (NIGHT) | `…/roadsigns_chinatown_stop_original_night.png` | `…/roadsigns_chinatown_stop_poc_night.png` | 1,93 | 2,01 % | só a placa (caixa das mudanças 635–1712 × 123–779 px) |

Observações visuais (dados para a reconstrução; **não são falhas do pipeline**):
- **STOP → PARE:** octógono deslocado, com faixa branca à esquerda e o "E" cortado. Confirma a Fase 1.
- **YIELD → DÊ A PREFERÊNCIA:** o triângulo **também aparece deslocado**, com borda cinza/branca à esquerda. É mais um sinal de UV incompatível na referência regenerada.
- **SPEED LIMIT 25:** o texto **continua em inglês** no PoC. A região do atlas usada por essa placa não foi traduzida na referência antiga, mas mudou levemente por causa da regeneração. Relevante para a decisão pendente de mph/km/h.
- **NIGHT:** com `cloudCover 0` a noite fica iluminada pelo luar e a placa fica legível. Com as nuvens padrão, a placa virava silhueta preta. `t_roadsigns` não tem emissivo.

## Reprodutibilidade da câmera

Procedimento `repro`:
1. Captura `A` na pose do catálogo.
2. Captura `A2` na mesma pose, sem mover (piso de ruído).
3. Câmera levada ~50 m, com FOV 90.
4. Pose restaurada.
5. Captura `B`.

As imagens ficam em `working/temporary/qa_repro/`, fora do Git.

| Ponto | A×A2 (ruído) média / PSNR | A×B (restaurado) média / PSNR | Deslocamento A×B |
|---|---|---|---|
| chinatown_stop | 0,136 / 52,5 dB | 1,010 / 44,7 dB | — |
| downtown_yield | 0,295 / 49,9 dB | 0,806 / 46,6 dB | — |
| hill_speed25 | 0,415 / 38,7 dB | 0,509 / 37,2 dB | — |

O deslocamento foi medido por correlação de fase numa rodada anterior do mesmo teste, com nuvens: **0 px nos três pontos**.

Histórico da investigação:
- **Nuvens padrão:** diferença restaurada de até 6,15. Os mapas de diferença mostraram que ela vinha das nuvens em movimento.
- **`windSpeed 0`:** caiu para 0,79.
- **`windSpeed 0` + `cloudCover 0` (preset final):** 0,5–1,0, perto do ruído.

As diferenças que sobram são contornos finos, típicos de antialiasing temporal.

**Conclusão:** o enquadramento, a posição e o FOV são **reproduzíveis**. O resultado não é idêntico pixel a pixel, mas fica equivalente para inspeção visual.

## Mod ON/OFF

- Comandos: `core_modmanager.activateMod("traducao_ptbr_wcusa")` / `deactivateMod(...)`, via `run_lua`. O estado é confirmado com `getMods()[…].active`.
- **É preciso recarregar o nível (`load_level`)**. Teste sem recarga:
  1. Mod desativado com a placa em cena: a placa **continuou PARE**, mesmo com o VFS já apontando para o `signage.zip`.
  2. Depois de a câmera visitar outros pontos e voltar, a mesma placa estava **STOP**. A textura foi relida da nova origem quando voltou ao streaming.
  3. Resultado: estado não determinístico.
- O runner **recarrega o nível no início de cada `capture`** (~75 s). Não é preciso reiniciar o BeamNG nem limpar cache.

## Asset virtual

`file_info("/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds")` foi executado em cada `capture`. Os 4 `realPath` bateram com o esperado (mod em ON, `signage.zip` em OFF). O resultado fica no campo `vfs` de cada run report.

## Logs

- Filtro aplicado: linhas `E`/`W` com `missing`, `not found`, `failed to load`, `unable to load/mount/find`, `invalid`, `duplicat`, `.dds`, `texture`, `NO-MATERIAL`, `t_roadsigns`, `traducao_ptbr_wcusa`.
- Execuções com recarga: 73 linhas marcadas, **idênticas** entre original e PoC.
  - Todas vêm do mod de veículo `hcity7_BAIXX0` (`getTSMeshByName`, `prepareLinksDestructive`, `[NO-MATERIAL] hcity7…`, `controller/lua/needleSweep not found`) e do CEF.
  - **Nenhuma** cita `roadsigns`, `.dds`, textura ou o mod.
- Execuções na mesma carga (NIGHT): 0 linhas.
- Contagens E/W diferentes entre original e PoC apareceram só em:
  - `E GELua.screenshot` (`unknown job id`), que é efeito da própria ferramenta `screenshot`;
  - `libbeamng.controller.init:<id do veículo>`, que muda de id a cada carga. O runner passou a normalizar esse id.
- **Nenhum erro novo causado pelo mod.**

## Limitações encontradas

1. A captura segue o tamanho da janela do jogo (1920×993 aqui). O MCP não aceita resolução. O runner registra o tamanho e avisa se ele divergir.
2. Os ids de objeto mudam a cada carga, então o catálogo usa shape + posição (tolerância de 1 m).
3. A troca de mod exige recarregar o nível: ~75 s por mudança de estado.
4. `set_time_of_day` tem a semântica invertida em relação à própria descrição da ferramenta.
5. Vento e nuvens precisam de `run_lua` (`core_environment`), porque não há ferramenta dedicada.
6. O `screenshot` é assíncrono: o runner espera o arquivo estabilizar.
7. O `raycast` não informa material de TSStatic. A prova de uso da família é a lista de materiais do mesh mais a diferença visual.
8. O cursor do `get_logs` aparenta ser compartilhado. Chamadas de outro cliente no meio de uma execução "consomem" linhas.
9. Os logs do veículo `hcity7` poluem o filtro. A comparação útil é original × traduzido, não a contagem absoluta.
10. Tráfego ou veículos em cena mudam entre execuções. A recarga do nível voltou a `vehicleCount 1` (sem tráfego).

## Verificações (pipeline)

- [x] DDS carregou (VFS + mudança visual)
- [x] 3 pontos reais da família, com câmera salva
- [x] Baseline e PoC nas mesmas poses
- [x] Enquadramento reproduzível
- [x] Mod ON/OFF controlável
- [x] Sem erro novo no log
- [ ] UV correta: **não** (referência antiga deslocada; esperado, fica para a reconstrução)

## Resultado

Pipeline de QA: **validado**. Textura `t_roadsigns_b.color`: **REQUER REVISÃO**, pois continua PoC e não é uma tradução aprovada.
