# Protocolo de QA visual via MCP do BeamNG

Procedimento determinístico para comparar uma textura original com a versão do mod dentro do jogo.
A implementação de referência é `tools/beamng/qa_runner.py` (fala diretamente com o servidor MCP do jogo);
este documento descreve as **mesmas operações** em termos de ferramentas MCP, para quem executar à mão ou com outro agente.

Pré-requisitos
- BeamNG.drive 0.39.4.0 em execução, com **Opções → Geral → "Ativar servidor MCP"** ligado (`http://127.0.0.1:29292/mcp`, Streamable HTTP, protocolo `2024-11-05`).
- Mod em `<user folder>\mods\unpacked\traducao_ptbr_wcusa\` (user folder: `C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\`).
- Python 3 + Pillow (+ numpy para `repro`), a partir da raiz do repositório.
- Catálogo `tests/qa_locations.json`; presets em `tests/presets/`.

## Comandos do runner

| Objetivo | Comando |
|---|---|
| Estado atual (nível, mod, horário, câmera) | `python tools/beamng/qa_runner.py status` |
| Baseline (mod OFF) de uma família | `python tools/beamng/qa_runner.py capture --family t_roadsigns --state original --preset day` |
| Estado traduzido (mod ON) | `python tools/beamng/qa_runner.py capture --family t_roadsigns --state poc --preset day` |
| Um ponto só, noite | `python tools/beamng/qa_runner.py capture --location roadsigns_chinatown_stop --state poc --preset night` |
| Reprodutibilidade da câmera | `python tools/beamng/qa_runner.py repro --location roadsigns_chinatown_stop --preset day` |
| Ligar/desligar o mod (+ recarga) | `python tools/beamng/qa_runner.py mod --enable` / `--disable` |
| Cadastrar um ponto novo | ver "Adicionar um ponto" |

`--state original` = mod **desativado**; qualquer outro valor (`poc`, `ptbr`, …) = mod **ativado**.

## Sequência de uma execução `capture`

| # | Operação | Ferramenta MCP / chamada | Critério de sucesso |
|---|---|---|---|
| 1 | Marcar início do log | `get_logs` (descarta) | chamadas seguintes retornam só linhas novas |
| 2 | Pôr o mod no estado pedido (`enable_translation_mod` / `disable_translation_mod`) | `run_lua`: `core_modmanager.activateMod("traducao_ptbr_wcusa")` ou `deactivateMod(...)`; conferir `core_modmanager.getMods()["traducao_ptbr_wcusa"].active` | `active` = estado pedido |
| 3 | **Recarregar o nível** (sempre, no início de cada execução) | `load_level` `{name:"west_coast_usa"}` | ver passo 4 |
| 4 | Aguardar nível pronto | `get_status` a cada 5 s após 15 s iniciais | `level` contém `west_coast_usa` **e** `vehicleCount ≥ 1` em 2 leituras seguidas; depois +10 s de assentamento |
| 5 | Conferir origem do asset (VFS) | `file_info` `{path:"/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds"}` | `realPath` contém `mods\unpacked\traducao_ptbr_wcusa` (ON) ou `signage.zip` (OFF) |
| 6 | Aplicar preset | `set_time_of_day` `{time, play:false}` (DAY `0.0`, NIGHT `0.5`); `toggle_ui` `{show:false}` | — |
| 7 | Resolver o objeto do ponto | `run_lua`: TSStatic com `shapeName` igual e posição a ≤ 1 m; `getMaterialNames()` | objeto encontrado (os ids mudam a cada carga) |
| 8 | Posicionar câmera | `set_free_camera` `{pos, rot (quat), fov:50}` do catálogo | — |
| 9 | Assentar | esperar 4 s (streaming de texturas/LOD) | — |
| 10 | Capturar | `screenshot` → caminho em `<user folder>\screenshots\mcp\`; **esperar o arquivo existir e parar de crescer** (a ferramenta devolve o caminho antes de gravar) | arquivo PNG 1920×993 |
| 11 | Copiar para o repositório | `tests/screenshots/baseline/<família>/<id>_original[_night].png` ou `tests/screenshots/current/<família>/<id>_<estado>[_night].png` | — |
| 12 | Repetir 7–11 para cada ponto | | |
| 13 | Restaurar UI | `toggle_ui` `{show:true}` | — |
| 14 | Coletar log | `get_logs` e filtrar linhas `E`/`W` com: `missing`, `not found`, `failed to load`, `unable to load/mount/find`, `invalid`, `duplicat`, `.dds`, `texture`, `NO-MATERIAL`, nome da família, nome do mod | salvar contagens + linhas relevantes no run report |
| 15 | Run report | `tests/reports/runs/<timestamp>_<alvo>_<estado>_<preset>.json` | VFS OK, capturas com resolução esperada |

### Por que recarregar sempre
Teste da Fase 2: desativar o mod **sem** recarregar deixou a placa em PARE (textura em cache) mesmo com o VFS já
apontando para o `signage.zip`; minutos depois, após a câmera se afastar, a mesma placa voltou a STOP (textura relida
da nova origem). Estado sem recarga = não determinístico. Recarregar o nível (`load_level`) é o menor procedimento
confiável; **não** é necessário reiniciar o BeamNG nem limpar cache.

## Reprodutibilidade (`repro`)
`A` (pose do catálogo) → `A2` (mesma pose, sem mover: piso de ruído) → câmera levada 50 m / FOV 90 → pose restaurada → `B`.
Compara A×B contra A×A2 (média de diferença absoluta, PSNR, % de pixels com diferença > 16, centro da imagem).
Imagens ficam em `working/temporary/qa_repro/` (fora do Git).

## Adicionar um ponto
1. Com o nível carregado, localizar objetos cujo `getMaterialNames()` contenha o material da família
   (ex.: `roadsigns`) — evidência técnica, não aparência.
2. Acrescentar a entrada em `tests/qa_locations.json` com `object.shape`, `object.position`, `object.materials`, `camera: null`.
3. `python tools/beamng/qa_runner.py frame --location <id> --side -fwd --distance 3.5` → coloca uma câmera candidata
   olhando para o centro da caixa do objeto (não salva). Conferir com uma captura; trocar `--side +fwd` se estiver vendo o verso.
4. `python tools/beamng/qa_runner.py save-camera --location <id>` → grava a pose **lida do jogo** (`get_camera_state`).
5. Rodar `capture` original × traduzido e confirmar que a região muda (prova de que o ponto usa a textura).

## Revisão
Preencher `tests/reports/QA_TEMPLATE.md`. O resultado (APROVADO / REPROVADO / REQUER REVISÃO) é decidido por uma pessoa.
