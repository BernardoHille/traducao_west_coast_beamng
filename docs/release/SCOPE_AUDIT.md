# Auditoria de escopo do pacote 1.0.0

Data: 21/10/2026. Objeto: todos os arquivos de `mod/traducao_ptbr_wcusa/` e o que fica de fora do ZIP público.

## 1. Conteúdo de `mod/traducao_ptbr_wcusa/` (117 arquivos)

Categorias pedidas: necessário para runtime · metadado · documentação necessária · desnecessário · temporário · desenvolvimento.

**Resultado:** 116 arquivos são **necessários para runtime** e 1 é **metadado**. Nenhum arquivo é desnecessário, temporário ou de desenvolvimento. Não há documentação dentro da árvore do mod, e o BeamNG não exige nenhuma.

"Mod." quer dizer que o arquivo substitui o arquivo do jogo no mesmo caminho virtual e difere dele (SHA-256). "Novo" quer dizer que o caminho não existe no jogo.

| Grupo (caminho no mod) | Arquivos | Mod. / novo | Função | Classe |
|---|---:|---|---|---|
| `mod_info/traducao_ptbr_wcusa/info.json` | 1 | — | nome, autor, versão, descrição no gerenciador de mods | metadado |
| `assets/materials/signage/roadsigns/` | 2 DDS | 2 / 0 | atlas `t_roadsigns` (PARE, R-2, R-3, painéis, placas de velocidade em km/h) | runtime |
| `assets/materials/decal/marking/…` e `decalroad/lines/…` | 8 DDS | 8 / 0 | marcações no pavimento (as duas cópias do jogo) | runtime |
| `assets/materials/billboard_label/…` | 12 DDS | 12 / 0 | outdoors, placas genéricas/postos, indústria, mapa de ônibus, estúdio, Spearleaf, Hot Rolled | runtime |
| `art/shapes/garage_and_dealership/Clutter/` | 2 DDS | 2 / 0 | `clutter_commercial` (néons, cartazes, concessionárias) | runtime |
| `levels/jungle_rock_island/art/shapes/buildings/` | 1 DDS | 1 / 0 | cópia de `ind_industrial_signs_d` que o West Coast carrega desse caminho | runtime |
| `art/shapes/objects/`, `art/shapes/race/dragstrip/` | 5 DAE + 5 CDAE | 10 / 0 | letreiros montados por glifos (ponto de ônibus, arrancada) | runtime |
| `levels/west_coast_usa/art/shapes/buildings/` | 18 DAE + 18 CDAE | 36 / 0 | letreiros de glifos de fachada (posto, motel, lojas, oficinas) | runtime |
| `levels/west_coast_usa/art/shapes/roads/` | 2 DAE + 2 CDAE | 4 / 0 | `roadsigns.dae` (placas de velocidade embutidas) e entrada do túnel | runtime |
| `levels/west_coast_usa/art/shapes/objects/` (fora de `roadsigns_ptbr`) | 3 DAE + 3 CDAE | 6 / 0 | cabines do pedágio, placa `sign_speed25` → R-19 40 | runtime |
| `levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/` | 6 DDS, 4 DAE, 4 CDAE, 1 materials | 0 / 15 | família R-19 10/40/50/70/120 | runtime |
| `levels/west_coast_usa/main/MissionGroup/…/items.level.json` | 15 | 14 / 1 | limites de via, radares, `shapeName` R-19, grupo novo `ptbr_functional_signs` | runtime |
| `levels/west_coast_usa/slotTraffic.json` | 1 | 1 / 0 | limites do tráfego por faixa, coerentes com o navgraph | runtime |
| `levels/west_coast_usa/main.decals.json` | 1 | 1 / 0 | frases do pavimento (EXIT ONLY → SÓ SAÍDA) | runtime |
| `levels/west_coast_usa/city.sites.json` | 1 | 1 / 0 | zonas do mapa em km/h | runtime |
| `levels/west_coast_usa/info.json` | 1 | 1 / 0 | combustível em litro (`localUnits` removido) | runtime |
| `gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json` | 1 | 1 / 0 | zonas das missões em km/h | runtime |

**Por que os `.dae` vão junto com os `.cdae`:** o nível referencia as malhas pelo `.dae`. O `.cdae` é a versão compilada pelo próprio jogo, e é ela que o motor carrega quando é mais nova que o `.dae`. Sem o `.dae`, o caminho referenciado não existiria no mod. Sem o `.cdae`, o jogo compilaria a malha no cache do usuário, e esse cache sobrevive à desativação do mod (achado da Fase 5). O ZIP grava cada `.cdae` com data posterior à do seu `.dae`.

## 2. Originais desnecessários

O build (`tools/release/build_release.py`) compara cada arquivo com o arquivo do jogo no mesmo caminho virtual. **Resultado: 0 cópias idênticas.** Uma cópia idêntica faria o build falhar.

Os JSON de nível são cópias completas dos arquivos do jogo com só os valores declarados alterados. O BeamNG substitui o arquivo inteiro, sem mesclar, por isso a cópia completa é necessária. A verificação do gerador confirma que só mudaram as linhas e objetos declarados (132 linhas, 15 objetos).

## 3. Escopo de pesquisa / ADAS

| Item | Onde está | No ZIP? |
|---|---|---|
| Mods `adas_speed_alert_test`, `adas_speed_alert_web`, `adas_event01_speed_limit`, `reaction_test`, `reaction_test_vr`, `adas_lab_first_person` | pastas próprias em `mods/unpacked/`, fora do repositório | **não** |
| Mudança do início do Event 01 (Fase 7) | dentro do mod de pesquisa `adas_event01_speed_limit`, com backup na pasta `_archive/` dele | **não** |
| Zona de 50 km/h no início dos cenários ADAS Speed Alert (DR312, R-19 50 e saída com R-19 120) | dados de nível do mod (`items.level.json`, `slotTraffic.json`) | sim |
| Corredor de 70 km/h do Event 01 (DR652, radar 2 a 70, R-19 70) | dados de nível do mod | sim |

**Decisão do responsável (21/10/2026):** os dois trechos de pesquisa ficam no pacote principal. Motivos:
- a 1.0.0 fica igual à versão aprovada na Fase 8;
- cada trecho funciona sozinho, com placa, limite de via e radar coerentes;
- separá-los mudaria velocidades já aprovadas;
- dois mods sobrescrevendo os mesmos arquivos do nível teriam precedência pouco previsível.

O pacote **não depende** de nenhum mod de pesquisa e não duplica nenhum arquivo deles. Os trechos estão descritos em `KNOWN_ISSUES.md`.

## 4. O que fica fora do ZIP (fica no repositório)

| Categoria | Exemplos | Motivo |
|---|---|---|
| Capturas de QA | `tests/screenshots/` | desenvolvimento |
| Masters editáveis | `working/layered/` (PSD/XCF/SVG, scripts de composição) | desenvolvimento |
| PNG intermediários | `working/png/` | desenvolvimento |
| Originais extraídos do jogo | `source/originals/` (só local, fora do Git) | direitos do jogo; não redistribuir |
| Referências antigas `_ptbr` | `source/reference_ptbr/` | histórico |
| PoC | `export/dds/poc/`, `tests/screenshots/poc/` | histórico |
| DDS exportados | `export/dds/` (fonte das cópias do mod) | duplicado |
| Heatmaps e relatórios | `export/reports/`, `tests/reports/` | desenvolvimento |
| Ferramentas | `tools/` (validação, produção, MCP, release), `tools/conversion/bin/` (texconv, fora do Git) | desenvolvimento |
| Documentação e artigo | `docs/` | desenvolvimento/pesquisa |
| Git, caches, temporários | `.git`, `__pycache__`, `working/temporary/` | — |

O build aceita só `.dds`, `.dae`, `.cdae` e `.json`, e falha se encontrar nomes proibidos: `*.psd`, `*.xcf`, `*.bak`, `*.tmp`, `*_ptbr.*`, `*_poc.*`, `Thumbs.db`, `desktop.ini`, `.env*`, `.git/`, `__pycache__/`, pastas `cache/` / `temp/` / `_archive/`, entre outros (lista em `build_release.py`).
