# Capacidades do MCP do BeamNG (inventário da Fase 2)

**Data:** 30/09/2026 · **BeamNG.drive:** 0.39.4.0 · **Servidor:** `beamng-game` v1.0.0, `http://127.0.0.1:29292/mcp`, Streamable HTTP, protocolo `2024-11-05` (ativado em Opções → Geral → "Ativar servidor MCP").

O `tools/list` expõe **86 ferramentas**. Aqui estão só as relevantes para QA de texturas. A coluna **Testado** diz se a ferramenta foi executada nesta fase ou na Fase 1:
- ✅ testado, funcionou como descrito;
- ⚠️ testado, com limitação ou divergência;
- ❌ não testado; a descrição vem só do `tools/list` e não deve ser considerada comprovada.

Várias capacidades **não têm ferramenta dedicada** e são feitas com `run_lua`, que executa código Lua no VM "GE" do jogo. Esses casos estão marcados como *via run_lua*.

## Mapa

| Capacidade | Comando MCP | Parâmetros | Resultado observado | Limitações | Testado |
|---|---|---|---|---|---|
| Listar mapas | `list_levels` | — | `[{name,title,file}]`, inclui `west_coast_usa` e o mod `gniar_br_costa_oeste` | — | ✅ |
| Carregar / recarregar mapa | `load_level` | `name` ou `path` | Retorna na hora (`loading level: …`). A carga termina em ~70–85 s | **Assíncrono**: é preciso aguardar pronto com `get_status`. Recarregar o mesmo mapa funciona | ✅ |
| Mapa atual e estado | `get_status` | — | `level`, `vehicleCount`, veículo do jogador, `camera.pos/mode`, `sim` | Não indica "carregando". O critério de pronto usado é `level` + `vehicleCount ≥ 1` em duas leituras seguidas | ✅ |

## Objetos e materiais

| Capacidade | Comando MCP | Resultado observado | Limitações | Testado |
|---|---|---|---|---|
| Listar TSStatic, shape, posição, orientação, caixa | *via run_lua*: `scenetree.findClassObjects("TSStatic")`, `o:getField("shapeName",0)`, `o:getPosition()`, `o:getTransform():getColumn(0/1/2)`, `o:getWorldBox()` | Funciona. ~milhares de objetos em < 1 s | **Os ids mudam a cada carga** (a mesma placa foi 94335, 281094, 339733…). Identificar por shape + posição | ✅ |
| Materiais de um objeto | *via run_lua*: `o:getMaterialNames()` | Ex.: `sign_stop.dae` → `roadsigns, metal_galvanized` | Diz quais materiais o mesh usa, não quais faces | ✅ |
| Mapas de um material | *via run_lua*: `scenetree.findObject("roadsigns"):getField("baseColorMap",0)` | `roadsigns` → `baseColorMap /art/shapes/objects/t_roadsigns_b.color.png`, `opacityMap …t_roadsigns_o.data.png` | Caminhos legados. O arquivo real é resolvido pelo VFS | ✅ |
| Buscar por classe/nome | `find_objects` | `class` + `pattern` → `[{id,name,class}]` | Placas não têm nome (`name:""`), então `pattern` não serve para elas | ✅ |
| Objetos no campo de visão | `view_objects` | `class:"TSStatic"`, `maxDist` → `[{id,class,dist,pos}]` | Não informa shape nem material | ✅ |
| Inspecionar objeto | `get_object` | Testado só com id inválido (`object not found`) | Não validado com id real | ⚠️ |
| Raycast | `raycast` | `pt`, `norm`, `dist`, `hit`. Com `renderGeometry:true` acerta a placa | **Não retornou material** para TSStatic | ⚠️ |
| `persistentId` de TSStatic | *via run_lua* `getField("persistentId",0)` | Vazio | Não existe id estável acessível | ⚠️ |

## Câmera

| Capacidade | Comando MCP | Parâmetros | Resultado observado | Limitações | Testado |
|---|---|---|---|---|---|
| Free camera com pose exata | `set_free_camera` | `pos{x,y,z}`, `rot{x,y,z,w}` (quaternion), `fov` | Pose aplicada exatamente. Restaurar a pose dá **deslocamento 0 px** | O jogador pode mover a câmera com input | ✅ |
| Ler a pose atual | `get_camera_state` | — | `mode`, `pos`, `rot` (quat), `fov` | — | ✅ |
| Calcular orientação | *via run_lua* `quatFromDir(dir, vec3(0,0,1))` | — | Quaternion para olhar para um ponto | — | ✅ |
| Trocar modo (orbit/driver…) | `set_camera` | `name` | — | — | ❌ |
| Câmera orbital no veículo | `orbit_camera` | `yaw`, `pitch`, `distance` | — | Só em torno de veículos | ❌ |

## Ambiente

| Capacidade | Comando MCP | Resultado observado | Limitações | Testado |
|---|---|---|---|---|
| Horário | `set_time_of_day` `{time, play:false}` / `get_time_of_day` | **`time 0.0` = meio-dia; `0.5` = meia-noite** (observado) | ⚠️ **A descrição da ferramenta diz o contrário** ("0.5 = noon"). Vale a observação | ⚠️ |
| Vento / nuvens | *via run_lua* `core_environment.setState({windSpeed=0, cloudCover=0})`, `getState()` | `windSpeed 0` congela o deslocamento das nuvens. `cloudCover 0` remove as nuvens, que mudam a cada carga e alteram a exposição | Sem ferramenta dedicada. Vale até recarregar o nível (o runner reaplica) | ✅ |
| Outros campos de clima | `getState()` expõe `fogDensity`, `temperatureC`, `cloudCirrus*`, `gravity`… | Só leitura foi feita | — | ❌ (escrita) |

## Interface

| Capacidade | Comando MCP | Resultado observado | Testado |
|---|---|---|---|
| Ocultar/mostrar UI (HUD) | `toggle_ui` `{show:false/true}` | UI some das capturas | ✅ |
| Estado da UI / rota | `get_ui_state` | Rota atual (ex.: `options`, `menu`) | ✅ |
| Mensagem na tela | `show_message` | — | ❌ |

## Mods (sem ferramenta dedicada: *via run_lua*)

| Capacidade | Chamada | Resultado observado | Testado |
|---|---|---|---|
| Listar mods e estado | `core_modmanager.getMods()` → `{[nome]={active, dirname, modType…}}` | ✅ | ✅ |
| Detectar mod novo em `mods/unpacked` | `core_modmanager.initDB()` | Mod montado (`mountEntry …traducao_ptbr_wcusa`) | ✅ (Fase 1) |
| Ativar / desativar | `core_modmanager.activateMod("traducao_ptbr_wcusa")` / `deactivateMod(...)` | Muda `active` e a origem no VFS em ~1 s | ✅ |
| Efeito visual da troca | — | **Exige `load_level`**. Sem recarga, a textura carregada fica em cache e é relida mais tarde de forma **não determinística** | ✅ |

## Sistema de arquivos virtual (VFS)

| Capacidade | Comando MCP | Resultado observado | Testado |
|---|---|---|---|
| Origem real de um arquivo virtual | `file_info` `{path}` → `realPath`, `exists`, `stat` | Mod ON: `…\mods\unpacked\traducao_ptbr_wcusa\assets\…\t_roadsigns_b.color.dds`. Mod OFF: `…\content\assets\materials\signage.zip\assets\…` | ✅ |
| Listar diretório virtual | `list_dir` | `/mods/unpacked/traducao_ptbr_wcusa/assets/materials/signage/roadsigns` → o DDS | ✅ |
| Buscar arquivos | `find_files` `{path, pattern}` | `/assets/materials/signage/roadsigns/*.dds` → `_b.color` e `_o.data` | ✅ |
| Ler/escrever/copiar/apagar/renomear/criar pasta | `read_file`, `write_file`, `copy_file`, `delete_file`, `rename_file`, `make_dir` | — | ❌ **Não usar contra a instalação do jogo** |

## Captura

| Capacidade | Comando MCP | Resultado observado | Limitações | Testado |
|---|---|---|---|---|
| Screenshot em arquivo | `screenshot` (`jpg:false`) | PNG em `<user folder>\screenshots\mcp\shot_<data>_<n>.png`, **1920×993** (viewport atual), ~1,5–3 MB | ⚠️ **Assíncrono**: o caminho volta **antes** de o arquivo existir, então é preciso esperar o arquivo estabilizar. Sem parâmetro de resolução. Gera no log `E GELua.screenshot: unknown job id N` (inofensivo) | ✅ |
| Screenshot inline (JPG base64) | `screenshot_image` `{scale}` | — | Chamada dupla (assíncrona) | ❌ |

## Logs

| Capacidade | Comando MCP | Resultado observado | Limitações | Testado |
|---|---|---|---|---|
| Ler `beamng.log` | `get_logs` `{lines}` | 1ª chamada: últimas N linhas. Depois: **só as linhas novas** desde a chamada anterior | O cursor aparenta ser do servidor (compartilhado entre clientes). Não há filtro no servidor: o runner filtra | ✅ |

## Outros

| Capacidade | Comando MCP | Resultado observado | Testado |
|---|---|---|---|
| Info de render | `get_render_info` | Direct3D12, RTX 4060, driver 32.0.15.7680 | ✅ |
| Variáveis do motor | `get_var` | `$pref::Video::mode` voltou vazio (nome não existe nesta versão) | ⚠️ |
| Veículos, física, IA, input, perfil, debug draw | `spawn`, `set_ai`, `pause_physics`, `debug_draw`, `profiler_run`… | — | ❌ (fora do escopo) |

## O que não existe (ou não foi encontrado)
- Ferramenta dedicada para mods: usar `run_lua` + `core_modmanager`.
- Recarregar só um material ou textura: não encontrado. O procedimento confiável é `load_level`.
- Parâmetro de resolução no screenshot: a captura usa o tamanho da janela do jogo.
- Material atingido no `raycast` de TSStatic.
- Identificador estável de objeto entre cargas.
- Sinal de "nível pronto": é preciso fazer polling do `get_status`.


## Achados da Fase 5

| Capacidade | Observado | Testado |
|---|---|---|
| `load_level` do **mesmo** mapa | Recria os objetos, mas reaproveita texturas, shapes (`.dae`/`.cdae`) e dados do nível em cache da sessão. Para trocar o estado do mod de forma determinística, carregue outro mapa antes (`smallgrid`) | ✅ |
| `load_level` com a janela minimizada | Não progride (nem gera log); funciona depois de restaurar a janela | ✅ |
| `set_time_of_day` | Em algumas sessões o objeto `TimeOfDay` aceita o valor, mas não ticka (`get_simulation_state.speedFactor` = 0), e o sol fica parado. Contorno: `ScatterSky.elevation` via `run_lua` | ⚠️ |
| `set_ui_state` | `{"route":"play"}` fecha o menu de pausa | ✅ |
| `set_simulation_speed` | parâmetro `scale` | ✅ |
| `drive_to` + `set_ai {speedMode:"legal"}` | IA segue o limite da via do navgraph (usado no teste 40/10 km/h) | ✅ |
| Compilação de `.dae` | Um `.dae` mais novo que o `.cdae` é compilado para `current/temp/levels/…/*.cdae`; esse cache sobrevive à desativação do mod | ✅ |
| `TSStatic.decalType` | `"Visible Mesh Final"` = mesh usado como decalque (ex.: placas das baias do porto com `sign_speed5.dae`); placas normais: `"Collision Mesh"` | ✅ |
