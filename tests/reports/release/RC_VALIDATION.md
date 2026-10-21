# Release candidate 1.0.0 — validação

| Campo | Valor |
|---|---|
| Data | 21/10/2026 |
| Versão do mod | 1.0.0 |
| Commit do conteúdo validado | `896fa36` (a árvore do mod é a mesma de `ac2ddf6`; o commit seguinte mudou só o script de build) |
| ZIP testado | `traducao_ptbr_wcusa_v1.0.0.zip`, 29.846.362 bytes, SHA-256 `684bcf6c2e93c9397fa1acc667dd37792d2e55b05973c32bc1a1bd33396e3b57` |
| BeamNG.drive | 0.39.4.0 (`integrity.json` da instalação), Windows 11 |
| Dados brutos | `tests/reports/release/release_smoke.json`; capturas em `tests/screenshots/release/{on,off}/` |

## 1. Suíte automática (antes do freeze)

| Comando | Resultado |
|---|---|
| `python -m unittest discover -s tools/validation/tests -v` | 63 testes OK: os 59 anteriores e 4 novos do pacote de release |
| `validate.py selftest` | PASS 121 · FAIL 0 |
| `validate.py regression` | PASS 10 · FAIL 0 |
| `validate.py mod` (árvore, famílias, texturas, DDS) | PASS 273 · FAIL 0 |
| `validate.py mod --installed` | PASS 274 · FAIL 0 (cópia instalada idêntica ao repositório, 117 arquivos) |
| `validate.py new` (R-19, materiais, malhas, overrides de nível) | PASS 108 · FAIL 0 |
| `validate.py speeds --refresh` (snapshot novo do navgraph no jogo) | PASS 27 · WARN 1 · FAIL 0 · SKIP 7 |
| `apply_phase7_functional.py --check` | OK: 132 linhas alteradas / 132 declaradas; 15 objetos adicionados / 15 declarados |
| `decal_overrides.py --check` | OK |

Detalhe do `speeds`:
- o WARN é informativo e vem da Fase 5: 4 placas em transições das docas regulam a via seguinte;
- os 7 SKIPs são legítimos: o Reaction Test (faixa experimental 40–70, excluída por política) e as 6 missões `arrive`, inativas (`maxSpeedActive = false`).

Nenhuma regra, tolerância ou SKIP foi alterado.

**Critério:** sem FAIL de textura, DDS, família, árvore do mod ou consistência funcional; sem arquivo faltante, material quebrado ou asset não encontrado → **atendido**.

## 2. Build

`python tools/release/build_release.py`:
- Git limpo;
- árvore do mod com 0 FAIL;
- overrides gerados conferidos;
- 117 arquivos, todos de tipos de runtime, sem nomes proibidos;
- 100 arquivos substituem um arquivo do jogo, todos modificados, e 16 são novos: **0 cópias idênticas a originais**;
- varredura de texto em 54 arquivos: nenhum caminho local, nome de usuário, e-mail ou segredo;
- ZIP extraído numa pasta temporária nova: mesmos 117 arquivos, mesmos hashes do staging e da árvore do mod, nada a mais.

**Reprodutibilidade:** três builds (em `ac2ddf6` e duas vezes em `896fa36`) deram o mesmo SHA-256.

## 3. Instalação limpa

Procedimento:
1. Versão de desenvolvimento desativada no gerenciador de mods, jogo fechado.
2. Pasta `mods/unpacked/traducao_ptbr_wcusa` **retirada** de `mods`. Ela foi guardada fora da pasta do jogo e devolvida no fim.
3. Só `traducao_ptbr_wcusa_v1.0.0.zip` copiado para `mods/`. O SHA-256 da cópia foi conferido.
4. Jogo aberto: o gerenciador registrou `traducao_ptbr_wcusa_v1.0.0` **ativo por padrão** (`/mods/traducao_ptbr_wcusa_v1.0.0.zip`) e a versão de desenvolvimento como `mod vanished`. Nenhuma das duas cópias ficou montada ao mesmo tempo.
5. Carga do smallgrid e depois do West Coast (protocolo de cache da Fase 5).

Outros mods ativos durante o teste: `hcity7` (veículo), `gniar_br_costa_oeste` (mapa separado, só em `levels/gniar_br_costa_oeste/`) e os mods de pesquisa (ADAS, Event 01, Reaction Test). **Nenhum deles tem arquivos em algum dos 116 caminhos de runtime do pacote** (conferido arquivo a arquivo).

**VFS (`FS:getFileRealPath` para cada arquivo do manifesto e `file_info`):** **116 de 116** arquivos de runtime vêm de `mods\traducao_ptbr_wcusa_v1.0.0.zip`. Exemplos:
- `t_roadsigns_b.color.dds`;
- `roadsigns.cdae`;
- `sign_r19_50.cdae`;
- `DecalRoads/items.level.json`;
- `slotTraffic.json`;
- `garages.sites.json`.

**Cache:** depois de carregar o West Coast, nenhum `.cdae` do mod foi compilado em `temp/`. O jogo usou as malhas compiladas do pacote, gravadas no ZIP com data posterior à dos `.dae`.

## 4. Smoke test visual (só o ZIP)

Dia (`tests/screenshots/release/on/`), todos em PT-BR:

| Grupo | Verificado |
|---|---|
| Sinalização | PARE (Chinatown) · R-2 (Downtown) · R-19 10 (docas) · R-19 40 com PARE (morro) · R-19 50 (entrada e início da zona ADAS) · R-19 70 (entrada e repetição do corredor) · R-19 120 (saída da zona) |
| Pavimento | PARE · NÃO BLOQUEIE · SEM SAÍDA · ÔNIBUS |
| Comercial | bomba do posto (DIESEL, 87/89/93) · outdoor Turbo Burger (NOVO MENU TURBO, R$ 4,99) · néon UNHAS E DEPILAÇÃO |
| Indústria / transporte / globais | PROIBIDO FUMAR (industrial) · mapa de ônibus no abrigo · ESTÚDIO 1 · totem Spearleaf REFINARIA · HOT ROLLED INC. FABRICAÇÃO DE AÇO · letreiro de glifos MOUNTAINVIEW POUSADA |

## 5. Dia / noite

Noite (`*_night.jpg`): outdoor Turbo Burger iluminado, néon UNHAS E DEPILAÇÃO com emissão, bomba do posto, PARE no pavimento e PARE em Chinatown. Tudo legível e em PT-BR → **aprovado**.

## 6. Smoke test funcional (só o ZIP)

**Navgraph:** 19 de 19 pontos reais batem com o limite esperado:

| km/h | Pontos |
|---:|---|
| 10 | 2 (docas) |
| 40 | 3 (via local, malha residencial, praça de pedágio) |
| 50 | 2 (zona ADAS) |
| 60 | 5 (avenida, ilha, docas, radares) |
| 70 | 2 (corredor do Event 01) |
| 80 | 2 (automáticos) |
| 100 | 1 (trevo junction1, radar 4) |
| 120 | 2 |

**Objetos do nível:**
- radares 2–7 com 70/60/100/60/60/60 km/h (19,4444 / 16,6667 / 27,7778 m/s);
- grupo `ptbr_functional_signs` carregado com as suas 14 placas (os "15 objetos adicionados" do gerador são o grupo e as 14 placas);
- `localUnits` ausente, ou seja, combustível em litro.

**Radar** (regra do jogo: dispara acima do limite + 10 %):

| Radar | Limite | Velocidade no radar | Disparou | Esperado |
|---|---:|---:|---|---|
| 3 | 60 | 53,5 | não | não |
| 3 | 60 | 64,5 | não | não (dentro da tolerância) |
| 3 | 60 | 66,1 (registrada pelo jogo) | sim | sim: 66,1 > 66,0. O alvo era 65 e o carro passou um pouco |
| 3 | 60 | 72,4 | sim | sim |
| 4 (o antigo caso fora do padrão) | 100 | 89,3 | não | não |
| 4 | 100 | 100,4 | não | não |
| 4 | 100 | 118,3 | sim | sim |

**ADAS (opcional, externo):** o mod de pesquisa `adas_speed_alert_test` **não faz parte** do pacote. Rodado sobre a zona de 50 do ZIP, passou:
- início sobre a via de 50 (`DR253_6 → DR312_9`);
- sem alerta abaixo de 50, alerta acima de 50, alerta desliga ao reduzir;
- todas as amostras na zona a 50.

Capturas em `tests/screenshots/release/on/adas/`. O pacote não depende desse mod.

> **Errata (21/10/2026, artigo técnico final).** As duas capturas de `tests/screenshots/release/on/adas/` mostram o menu principal do jogo sobre a cena e não servem como evidência visual. O resultado acima não depende delas: ele vem dos contadores do controlador do cenário, registrados em `tests/reports/release/release_smoke.json` (`adas_speed_alert_optional`). Para a evidência visual da zona de 50, ver `tests/screenshots/release/on/signs/r19_50_*.jpg` (placas R-19 50 capturadas com o ZIP) e as capturas da Fase 7 em `tests/screenshots/phase7/adas/`. Nenhum resultado, arquivo de runtime ou a tag foram alterados.

## 7. Logs

Coletados com `get_logs` do MCP: na inicialização, na sessão com o ZIP (carga, capturas, radar, ADAS) e na sessão com o mod desligado. Filtro: linhas E/W com `mod|dds|material|mesh|cdae|dae|json|missing|unable to load|invalid|not found|failed|error`.

- **Linhas que citam o mod ou os caminhos dele** (`traducao`, `ptbr`, `roadsigns`, `r19`, `west_coast_usa`): **0** com o mod ligado e 0 desligado.
- **As mesmas categorias aparecem com o mod ligado e desligado:**
  - malhas, materiais, controlador `needleSweep`, links de jbeam e textura do GPS do veículo `hcity7` (outro mod);
  - o aviso do caminho das nuvens (jogo);
  - na inicialização: Steam offline, aviso de extensão dos mods de pesquisa e `mod vanished` da cópia de desenvolvimento retirada.
- **Só com o mod ligado:** 3 linhas `FATAL LUA ERROR freeroam.lua:392 … gameplay_speedTrapLeaderboards (nil)`, uma por disparo de radar do teste. Causa: o roteiro de teste carrega `gameplay_speedTraps` fora do modo freeroam, e o freeroam normal carrega também `gameplay_speedTrapLeaderboards` (`lua/ge/main.lua:365`). É efeito do roteiro de teste, não do mod; em jogo normal não ocorre.

**Erros novos relevantes causados pelo mod: nenhum.**

## 8. Mod OFF

O ZIP foi desativado no gerenciador e o mapa recarregado passando pelo smallgrid.

- **VFS:** 0 de 116 arquivos vêm do ZIP. Os modificados voltam aos zips do jogo (`signage.zip`, `west_coast_usa.zip`, `gameplay/` da instalação), e os novos (R-19) não existem.
- **Visual:** STOP, YIELD, SPEED LIMIT 25 e 5, STOP no pavimento, "NEW TURBO MENU 4.99-".
- **Funcional:**
  - vias de volta a 56,3 km/h (35 mph), 60 e 120;
  - radares todos a 15,6464 m/s (35 mph);
  - grupo `ptbr_functional_signs` ausente;
  - `localUnits` de volta a `gallonUS`.
- **Cache:** nenhum `.cdae` do mod em `temp/`.

O jogo voltou ao original → **aprovado**.

## 9. Usuário final

- Os testes externos da Fase 8 estão registrados em `docs/production/PHASE8_GLOBAL_QA.md`.
- Nesta fase não houve uma nova campanha com pessoas.
- O procedimento de `docs/INSTALLATION.md` (copiar o ZIP para `mods`, abrir o jogo) foi o mesmo usado no teste de instalação limpa acima. O mod apareceu ativo sem nenhum passo extra.

## 10. Ambiente ao final

O ZIP foi retirado da pasta `mods`; o original está em `release/output/`. A versão de desenvolvimento voltou a `mods/unpacked/`, idêntica ao repositório (`mod --installed`: 274 PASS).

## Veredito do RC

**Aprovado** para a release 1.0.0.
