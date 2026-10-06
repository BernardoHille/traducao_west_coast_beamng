# 6I — Letreiros montados por glifos (malha)

**Data:** 06/10/2026.

## O problema
Muitas palavras do West Coast **não estão escritas em nenhum atlas**:
- fachadas, totens de posto e preços;
- o abrigo de ônibus;
- a pista de arrancada, o túnel do autódromo;
- os pórticos.

Cada letra é um **quad do mesh** (`.dae`) que aponta para uma célula de um alfabeto (`clutter_commercial`, `t_billboardsigns_dealers`, `t_roadsigns`), e a forma da letra vem do mapa de opacidade.

Trocar a célula no atlas mudaria a mesma letra em todas as palavras, inclusive de outros mapas. Por isso a tradução é feita **na geometria**:
- remover os quads da palavra antiga;
- criar os quads da palavra nova no mesmo plano;
- distribuir o `.dae` reescrito com o `.cdae` compilado pelo jogo (técnica do R-19 da Fase 5).

## Ferramentas
| Ferramenta | Função |
|---|---|
| `tools/production/glyph_signs.py` | Lê os quads de um material, decodifica cada letra pela massa de tinta do alfabeto (`glyph_fonts.json`: 9 alfabetos, maiúsculas, minúsculas, símbolos) e agrupa em linhas. Detecta linhas giradas, itálicas e verticais, faces opostas e cópias empilhadas (duas geometrias idênticas). Renderiza a placa como o jogo mostra (z-buffer, recorte pela opacidade) para revisão |
| `tools/production/glyph_rewrite.py` | Reescreve as linhas pedidas em `working/layered/glyph_signs/spec.json`, detalhado abaixo |
| `working/layered/glyph_signs/make_accents.py` | Células de acento (´ ~ ^ ¸, hífen, vírgula) no estilo de cada alfabeto, em espaço transparente que **nenhum mesh do jogo amostra** (pegada UV dos 245 meshes com `clutter_commercial`); desenhadas por `compose.py` (op `accent`) |
| `working/layered/t_roadsigns/glyph_tiles.py` | Novos tiles de palavra no `t_roadsigns` para os pórticos (os originais são compartilhados com a cabine de pedágio e a placa de proibido estacionar) |
| `tools/production/glyph_sync.py` | Copia os `.dae` alterados para o mod, apaga o `.cdae` obsoleto e, depois da carga do nível, copia o `.cdae` recém-compilado (força a compilação de shapes fora do nível com um TSStatic temporário) |
| `validate.py new` | Para cada mesh: triângulos dos outros materiais, árvore de nós e transformações **idênticos** ao original; quads novos dentro da placa original; `.cdae` presente e mais novo que o `.dae` |

O que `glyph_rewrite.py` faz em cada linha pedida:
- mesmo espaçamento e padding de célula do original;
- alinhamento detectado (esquerda, direita ou centro);
- condensação em X quando a palavra é mais longa, com redução uniforme abaixo de 70 %;
- acentos como quads extras;
- camadas de contorno (`E` atrás de `F`) e separadores (`&`, `:`, `-`) reaproveitados;
- `$` → `R$`;
- MAX CLEARANCE 13 FT 1 IN → ALTURA MÁXIMA 3,9 m, com os algarismos do `t_roadsigns` re-apontados;
- re-apontamento de quads para tiles novos (`uv_map`);
- normais, cores de vértice e lightmap copiados dos quads substituídos.

## O que foi traduzido (25 meshes)
| Mesh | Linhas | Quads |
|---|---|---|
| `s_motel_sign` | MOTEL → POUSADA · CABLE → TV A CABO (MOUNTAINVIEW, nome, preservado) | 20 → 28 |
| `s_food_mart_sign_001` | DELI & FOOD MART → LANCHES & MERCADO · ICE COLD BEER & SODA → CERVEJA & REFRI GELADOS | 58 → 70 |
| `s_full_service_sign_001` | FULL SERVICE → SERVIÇO COMPLETO · from $120 → a partir de R$120 | 32 → 54 |
| `s_exhaust_sign_001` / `_002` | EXHAUST → ESCAPAMENTO · CAR STEREO → SOM AUTOMOTIVO | 75 → 111 / 25 → 37 |
| `s_fix_sign_001` | WE FIX: → CONSERTAMOS: · RADIATORS / SUSPENSION / TRANSMISSIONS → RADIADORES / SUSPENSÃO / CÂMBIOS · AUTO GLASS → AUTO VIDROS | 43 → 46 |
| `s_sound_sign_001` | SOUND & TINT → SOM E INSULFILM | 20 → 26 |
| `s_stereo_sign_001` | STEREOS / ALARMS / WINDOWS → SOM / ALARMES / VIDROS | 20 → 16 |
| `s_car_parts_sign_001` | RIMS / TIRES / LIFT KITS / HYDRAULICS → RODAS / PNEUS / SUSPENSÃO / HIDRÁULICA | 108 → 124 |
| `s_torres_tires_sign_001` | TIRE ROTATION & WHEEL ALIGNMENT → RODÍZIO DE PNEUS & ALINHAMENTO · $59 → R$59 (TORRES TIRES, nome, preservado) | 56 → 58 |
| `s_smash_auto_sign_001` | We fix all brands! → Consertamos todas as marcas! (SMASH AUTO REPAIRS, nome, preservado) | 30 → 50 |
| `diner_building` | OPEN 24 HRS → ABERTO 24 HORAS · RESTAURANT → RESTAURANTE | 34 → 44 |
| `gasstation_north`, `s_fuel_main_05` | SAVE 40% → OFERTA 40% · 12 PACK → 12 MAÇO · NOW OPEN → ABERTO · ATM → CAIXA · $ → R$ | 27 → 37 / 54 → 74 |
| `s_bld_food_mart_001` | CANAL ST DELI & FOOD MART → CANAL ST DELI & MERCADO · CAR WASH → LAVA JATO · LOTTO - TOBACCO - COLD DRINKS - ATM → LOTERIA - TABACARIA - BEBIDAS - CAIXA · cartazes como no posto | 178 → 202 |
| `s_bld_laundomat_001` | LAUNDROMAT → LAVANDERIA | 40 → 40 |
| `s_bld_shops_001` | MINI MART → MERCADINHO · GROCERY → MERCEARIA (vertical) · ATM → CAIXA · PACK → MAÇO · $ → R$ | 90 → 126 |
| `s_brick_walls_slums_car_shops` | parede das oficinas: WE FIX, RADIATORS…, FULL SERVICE, AUTO GLASS, NEW & USED, QUALITY BRANDS, TIRES, GOT A FLAT?, ENTRY, preços → PT-BR (marcas ALDER, FOLK, GRIP ALL, CLOCKWISE, OKUDAI, TORRES TIRES preservadas) | 139 → 180 |
| `tunnel_mainTrackEntrance` | WELCOME TO → BEM-VINDO AO · THANKS FOR VISITING → OBRIGADO PELA VISITA · MAX CLEARANCE 13 FT 1 IN → ALTURA MÁXIMA 3,9 m (BELASCO MOTORSPORTS PARK, nome, preservado) | 71 → 67 |
| `dragstrip_tree_alder`, `dragStrip_irSensorBox` | IR SENSOR → SENSOR IV · NO STEP → NÃO PISE (PRE-STAGE / STAGE: jargão da arrancada, preservado) | 36 → 40 / 8 → 8 |
| `dragDriversWinLightBoxShort` | WIN LIGHT → VENCEDOR | 8 → 8 |
| `s_busstop_wcu`, `s_busstop_wcu_04` | MAP → MAPA (INFO já é português) | 6 → 8 |
| `roadsigns` (pórticos e placas de faixa) | ONLY → SOMENTE · CARPOOLS ONLY / 2 OR MORE PERSONS / PER VEHICLE → FAIXA EXCLUSIVA / 2 OU MAIS OCUPANTES / POR VEÍCULO · ¼ ½ ¾ (milhas) → 400 m / 800 m / 1,2 km · MILE(S) removido | 20 → 20 (re-apontados) |

**Atlas:**
- `clutter_commercial`: 13 células de acento/sinal.
- `t_roadsigns`: 10 tiles novos, em área livre e com evidência UV dos meshes do mod. Os 44 elementos da Fase 5 seguem idênticos.
- Os cartazes SALE% passaram a manter o `%` original, porque ele também é amostrado pelos cartazes de preço dos postos ("40%").

## O que fica de fora, e por quê
| Item | Motivo |
|---|---|
| Cabine de pedágio: DO NOT STOP / SPEED LIMIT 25 (`s_toll_booth_center`) | Placa de **limite de velocidade** (mph → km/h exige R-19 e o limite funcional da via): **Fase 7** |
| Tiles SPEED LIMIT e MPH do `roadsigns.dae` (placas 15–30 MPH, SPEED LIMIT 30/40/70) | Idem: **Fase 7** |
| `timerboard` (NOMI, BNG 48x16) | Marca/modelo do equipamento: preservado |
| PRE-STAGE / STAGE | Termos usados assim na arrancada brasileira: preservado |

## Validação
- `validate.py new`: 75 PASS, sendo 25 meshes de glifos com estrutura e `.cdae` verificados.
- PNG `clutter_commercial` (98 regiões) e `t_roadsigns` (54 regiões): 0 px fora das regiões. DDS no formato e com os mips originais.
- `.cdae`: compilados pelo próprio jogo a partir do `.dae` atual. `glyph_sync.py` apaga o `.cdae` antigo quando o `.dae` muda, porque `install_mod.py` re-carimba `.cdae` existentes e um `.cdae` obsoleto passaria por novo (encontrado e corrigido nesta etapa).

## QA MCP
- **Ciclo final** de 06/10/2026, 17:45–18:04, com o jogo reiniciado e o cache de shapes limpo: 86 pontos `gl_*`, cada um com o par original × PT-BR. Capturas em `tests/screenshots/phase6/glyph_signs/`.
- **Resultado:** 0 problemas de VFS. Sanidade da Fase 5 (PARE, R-2, R-19 40) intacta.
- **Cache:** durante o ciclo o jogo **não gravou nenhum `.cdae` no cache temporário** (mod ligado e desligado). Ou seja, os `.cdae` distribuídos impedem o cache que sobreviveria ao mod.
- **Achado:** os `.cdae` compilados durante o desenvolvimento ficam no cache do usuário (`current/temp`) e fazem o estado "mod desligado" mostrar PT-BR. Os 25 arquivos foram apagados do cache (procedimento da Fase 5) antes do ciclo final.
- **Correções feitas a partir do QA:**
  - o acento agudo da fonte R1 flutuava acima da letra e foi rebaixado 2 px;
  - 4 enquadramentos refeitos: placa CARPOOLS vista por trás, sensores da arrancada e MAPA longe demais;
  - um ponto descartado: o PACK do `s_bld_shops_001` caía atrás de um cartaz; o mesmo cartaz MAÇO está conferido nos postos.
- **Não conferido no jogo:** WIN LIGHT → VENCEDOR (`dragDriversWinLightBoxShort`), que só existe no prefab da missão de arrancada. Foi verificado no render offline e no `validate.py new`.
