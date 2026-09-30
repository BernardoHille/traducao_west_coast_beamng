# PoC de override

**Data:** 30/09/2026 · **Fase 1 — Proof of Concept do override de textura**

## Ambiente

- **Versão do BeamNG:** BeamNG.drive 0.39.4.0 (Steam), instalado em `C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive`
- **User folder:** `C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\`
  - O `beamng.log` registra `Virtual Filesystem: user path: C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\ (Default behaviour)`.
  - `BeamNG.drive.ini` tem `UserPath =` vazio, então vale o padrão.
  - Os mods existentes (`adas_*`, `reaction_test`, `gniar_br_costa_oeste.zip`, `hcity7_*.zip`) estão nessa pasta.
- **Pasta do mod:** `<user folder>\mods\unpacked\traducao_ptbr_wcusa\`
- **Outros mods ativos durante o teste:** `gniar_br_costa_oeste.zip` (só `levels/`), `hcity7_BAIXX0_v1.3.3.zip` (só `vehicles/`), `adas_event01_speed_limit`, `adas_lab_first_person`, `adas_speed_alert_test`, `adas_speed_alert_web`, `reaction_test`. **Nenhum** deles contém `t_roadsigns` nem arquivos em `assets/materials/signage/`.

## Textura testada

- **Família:** `t_roadsigns` (`t_roadsigns_b.color` + `t_roadsigns_o.data`)
- **Arquivo substituído:** somente `t_roadsigns_b.color`. O `t_roadsigns_o.data` **não** foi alterado.
- **Resolução:** 2048×1024
- **Formato:** DX10 `BC7_UNORM_SRGB` (DXGI 99), sRGB
- **Mipmaps:** 12 (cadeia completa)
- **Conteúdo do PoC:** a referência PT-BR antiga (`source/reference_ptbr/t_roadsigns_b.color_ptbr.png`), usada **só** como marcador visual. **Não** é uma tradução aprovada.

## Caminho original

- ZIP: `C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive\content\assets\materials\signage.zip`
- Caminho interno: `assets/materials/signage/roadsigns/t_roadsigns_b.color.dds`, com o nome exato confirmado no ZIP, só por leitura.
- **Como o mapa referencia a textura:** o material `roadsigns` do West Coast declara `baseColorMap = /art/shapes/objects/t_roadsigns_b.color.png` e `opacityMap = /art/shapes/objects/t_roadsigns_o.data.png`. São caminhos legados, e o motor resolve esses caminhos para o DDS em `/assets/materials/signage/roadsigns/`.

## Caminho do override

Dentro do mod (espelha o caminho virtual do jogo):

```
traducao_ptbr_wcusa/
├── assets/materials/signage/roadsigns/t_roadsigns_b.color.dds
└── mod_info/traducao_ptbr_wcusa/info.json
```

Com o mod ativo, o sistema de arquivos virtual (MCP `file_info`) resolve `/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds` para o arquivo do mod. Com o mod desativado, resolve para o `signage.zip`.

**`info.json`**: segue o formato dos mods locais que funcionam (`name`, `author`, `version`, `description`). Nenhum campo extra foi necessário. O BeamNG registrou o mod com `modType: "unknown"`, igual aos outros mods unpacked.

## Conversão

- **Ferramenta:** texconv (Microsoft DirectXTex), release `may2026`, versão `2026.5.8.1`
  - Baixada de `github.com/microsoft/DirectXTex/releases` com autorização explícita.
  - SHA-256 `dcfdec10…5eef06` confere com o digest publicado, e a assinatura Authenticode da Microsoft é válida.
  - Local: `tools/conversion/bin/` (fora do Git).
- **Comando:**

```
texconv.exe -nologo -f BC7_UNORM_SRGB -srgb -m 0 -dx10 -y -o export/dds/poc working/temporary/poc/t_roadsigns_b.color_poc.png
```

- **Resultado:** a comparação completa está em `export/reports/poc_t_roadsigns.md`. Dimensões, formato, mipmaps e tamanho são iguais aos do original. A única diferença é o metadado `alphaMode`: STRAIGHT no PoC, UNKNOWN no original.

## Resultado

Local do teste: West Coast USA, placa **STOP** `sign_stop.dae` (TSStatic id 94335) em (-712.7, 552.9, 122.4), num cruzamento de Chinatown. Câmera livre fixa, meio-dia (`time = 0`), interface oculta. As capturas foram feitas pelo MCP do BeamNG.

| Teste | Estado do mod | Resultado | Captura |
|---|---|---|---|
| A | ativo | A placa mostra **"PARE"** (textura do PoC). Outra placa do atlas mostra "PROIBIDO ESTACIONAR" | `tests/screenshots/poc/roadsigns_mod_on.png`, `…_mod_on_proibido_estacionar.png` |
| B | desativado (`core_modmanager.deactivateMod`) + recarga do mapa | A mesma placa volta a **"STOP"** (original) | `tests/screenshots/poc/roadsigns_mod_off.png` |
| C | reativado (`core_modmanager.activateMod`) + recarga do mapa | **"PARE"** volta | `tests/screenshots/poc/roadsigns_mod_on_again.png` |

**Observações visuais** (dados para a reconstrução, não são falhas do override):
- A máscara original `t_roadsigns_o.data` continuou recortando o octógono da placa. Não apareceu transparência estranha.
- Com a textura do PoC, o octógono vermelho aparece **deslocado** dentro da placa: surge uma faixa branca à esquerda e o "E" de "PARE" fica **cortado** na borda direita. Com o original, a placa fica centralizada. Isso confirma na prática o risco da auditoria §4.2: a referência PT-BR regenerada deslocou elementos do atlas em relação à UV.
- Não houve cache mascarando o resultado. A troca ON → OFF → ON apareceu logo após cada recarga do mapa, sem limpar nenhum cache.

**Asset global:** **não confirmado nesta fase.**
- O arquivo é resolvido de forma global. O `file_info` não depende do mapa, e o East Coast USA também define o material `roadsigns` com o mesmo `t_roadsigns_b`.
- Porém, no East Coast nenhum TSStatic usa o material `roadsigns`. As placas STOP de lá usam `signs_usa` (família `eca_roadsigns`). Por isso não havia placa visível para confirmar a textura na tela.
- Procurar usos em itens de Forest ou em outros mapas fica para o QA de East Coast/Utah.

## Log

Resumo em `tests/reports/poc_override_log.md`:
- O mod foi montado (`mountEntry -- /mods/unpacked/traducao_ptbr_wcusa/`).
- **Nenhuma** mensagem sobre `t_roadsigns`, DDS, textura ausente ou material do nosso mod.
- Os erros existentes (veículo hcity7, CEF, jobs de screenshot do MCP) aparecem igual com o mod ligado e desligado.

## Integridade

- Nenhum arquivo da instalação do BeamNG foi modificado: nenhum arquivo em `steamapps\common\BeamNG.drive` tem data de modificação no dia do teste, e o `signage.zip` continua com data de 25/08/2026.
- Os originais em `source/originals/` foram validados por SHA-256 e não foram alterados.
- As mudanças de horário, câmera e interface foram só de sessão, feitas pelo MCP. Nenhum arquivo de configuração foi alterado.

## Conclusão

**OVERRIDE VALIDADO**

Um DDS colocado em `mods/unpacked/<mod>/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds`, com o mesmo nome e formato do original, substitui a textura do jogo no West Coast USA sem tocar na instalação. Desativar o mod restaura o original.
