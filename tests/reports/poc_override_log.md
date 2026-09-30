# Log do BeamNG — PoC de override `t_roadsigns_b.color`

**Data:** 30/09/2026 · **BeamNG.drive:** 0.39.4.0 · **Fonte:** `beamng.log`, lido pelo MCP `get_logs` em janelas separadas por teste

## Janelas analisadas

| Janela | Conteúdo | Linhas |
|---|---|---|
| A0 | releitura dos mods (`core_modmanager.initDB`), lida logo depois da releitura | — (só inspecionada) |
| A | 1ª carga do West Coast com o mod **ativo**, incluindo o fim do callback da releitura | 317 |
| B | recarga do West Coast com o mod **desativado** | 340 |
| C | recarga do West Coast com o mod **reativado** | 319 |
| EC | carga do East Coast USA com o mod ativo (verificação de asset global) | 297 |

## Mensagens relacionadas ao PoC

**Montagem do mod (janela A0):**
```
6045.27172|D|GELua.core_modmanager.initDB| mountEntry -- /mods/unpacked/traducao_ptbr_wcusa/:  : traducao_ptbr_wcusa
```

**Resolução do arquivo pelo sistema de arquivos virtual** (MCP `file_info` em `/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds`):

| Estado | `realPath` |
|---|---|
| Mod ativo | `…\BeamNG.drive\current\mods\unpacked\traducao_ptbr_wcusa\assets\materials\signage\roadsigns\t_roadsigns_b.color.dds` |
| Mod desativado | `C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive\content\assets\materials\signage.zip\assets\materials\signage\roadsigns\t_roadsigns_b.color.dds` |

**Busca por `t_roadsigns`, `roadsigns`, `traducao`, `signage`, `.dds` e `texture`:** **nenhuma ocorrência** de erro ou warning em nenhuma janela.

## Erros e warnings existentes (não relacionados ao PoC)

O perfil é **idêntico** com o mod ligado (A, C) e desligado (B), o que indica que não vêm do nosso mod:

| Origem | Qtde por carga | Causa |
|---|---|---|
| `E libbeamng.controller.init`, `E GELua.jbeam.pushToPhysics`, `E GELua.jbeam.fillSlots`, `E prop`, `W …getTSMeshByName`, `W GELua.jbeam.prepareLinksDestructive`, `W core_vehicle_partmgmt.mesh`, `W core_input_actions` | ~50 / 34 / 2 / 2 / 36 / 18 / 4 / 2 | Mod de veículo `hcity7_BAIXX0_v1.3.3.zip` (veículo padrão do spawn). Ex.: `module 'controller/lua/needleSweep' not found`, `unable to find rigid mesh: hcity7_dash_key` |
| `E MaterialList.mapMaterials` | 9 | `[NO-MATERIAL] … interiorfifthhcity / hcitygaugesredwarn / hcity7_interior_detail`, do mesmo veículo hcity7 |
| `E cef_local`, `E engine::BNGCefClient::OnResourceResponse` | 2 / 2 | Interface (CEF). Aparece nas quatro janelas |
| `E GELua.screenshot` (`screenshotProgress: unknown job id N`) | 4–16 | Efeito da ferramenta `screenshot` do MCP. As capturas foram salvas normalmente |
| `W GELua.core_modmanager.initDB.modScript` (`setExtensionUnloadMode`) | 7 (só em A) | modScripts dos mods ADAS/reaction_test na releitura dos mods. O nosso mod não tem scripts |
| `E GELua.core_levels` (`No entry point for level found: /levels/GridMap`) | 1 (só em A0) | Mapa GridMap sem `info.json`, que já existia antes do PoC |

## Conclusão

Nenhum erro, warning ou mensagem de textura ausente foi causado pelo override. O mod foi montado e o arquivo foi resolvido para o mod quando ativo e para o `signage.zip` original quando desativado.
