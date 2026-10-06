# 6H — Auditoria final de cobertura

**Data:** 06/10/2026.

**Pergunta:** depois da Fase 6, que inglês visível ainda resta no West Coast, e por quê?

## Método
1. **Matriz:** cada uma das 311 linhas de `LOCALIZATION_MASTER.csv` foi classificada pelo status e pelo uso real no West Coast.
2. **Uso real:** a evidência é a pegada UV dos meshes **instanciados** (`compose.py regions`, `asset_usage.py`), não a presença no zip.
   - Uma família usada pode ter regiões que nenhum mesh amostra. Essas linhas passaram a `wcusa_usage = not_found`, com 12 correções nesta auditoria.
3. **Revisão visual:** os atlas usados foram percorridos inteiros, em especial `clutter_commercial`, com 188 meshes instanciados. O objetivo era achar inglês que não estivesse na matriz ou que tivesse ficado para trás.
4. **Malhas que montam palavras com glifos:** foram inspecionadas reconstruindo a placa a partir do `.dae` (`working/temporary/glyph_probe.py`).

## Classificação (311 linhas)
| Classe | Linhas | Significado |
|---|---|---|
| produzido + QA no jogo | 127 | Textura nova no mod e captura PT-BR conferida |
| produzido, sem ponto de QA próprio | 11 | Validado (regiões, DDS, família) e com evidência UV, mas sem enquadramento próprio. Inclui a lista de serviços, cuja face não aparece no jogo |
| `not_used` | 101 | Região ou família sem nenhum mesh/decal instanciado no West Coast |
| `preserve_original` | 45 | Marcas, nomes próprios, logos, pictogramas, chinês de Chinatown, "% OFF" |
| `out_of_scope` (Fase 7) | 15 | Dados funcionais (limites de velocidade, radares, zonas, slotTraffic) e tiles de unidade (MPH, SPEED LIMIT) |
| pendente de mesh/asset dedicado | 12 | Palavras compostas por glifos/tiles no mesh (ver abaixo) |
| `needs_context` | 0 | Todos resolvidos: bus_stops, studio_departments, bus_utah_stops, glifos |

## Inglês encontrado e corrigido durante a auditoria (`missed_translation`)
| Onde | Original | PT-BR | Evidência |
|---|---|---|---|
| Placa chinesa (8 prédios de Chinatown) | NO ENTRY | ENTRADA PROIBIDA (chinês preservado) | QA `cc_no_entry_cn` |
| RENT-A-BOX (`sign_rentabox`, `s_port_warehouse`) | SECURE STORAGE | GUARDA-VOLUMES SEGURO | QA `cc_rentabox` |

Os dois estavam na matriz (`commerce_chinese`, `commerce_rentabox`), mas tinham ficado fora do layout do atlas.

## Inglês que continua visível, e por quê
### 1. Palavras montadas por glifos no mesh (pendente)
| Item | Mesh (instâncias) |
|---|---|
| MOTEL e palavras menores do mesmo totem | `s_motel_sign` (1) |
| FOOD MART | `s_food_mart_sign_001` (1) |
| FULL SERVICE | `s_full_service_sign_001` (1) |
| EXHAUST, FIX, SOUND, STEREO, CAR PARTS | `s_exhaust_sign_001/002`, `s_fix_sign_001`, `s_sound_sign_001`, `s_stereo_sign_001`, `s_car_parts_sign_001` |
| MAP (abrigo de ônibus) | `s_busstop_wcu` (31), `s_busstop_wcu_04` (9) |
| Rótulos da pista de arrancada | `timerboard` (2), `dragStrip_irSensorBox` (14), `dragDriversWinLightBoxShort` (2) |
| ONLY, CARPOOLS, PER VEHICLE, ½ MILE (pórticos e cabine de pedágio) | `roadsigns.dae`, `s_toll_booth_center` |

Esses textos **não existem como palavra no atlas**. Cada letra é um quad do mesh que aponta para uma célula do alfabeto.

**Por que nenhuma edição de textura resolve:**
- trocar a célula muda a mesma letra em todas as palavras, inclusive de outros mapas, quando o alfabeto é global;
- as palavras PT-BR têm outro número de letras;
- os alfabetos não têm letras acentuadas (Ç, Ã, Á, Ê).

**O que é necessário:**
- recompor a geometria desses `.dae`, adicionando ou removendo quads e reposicionando-os;
- acrescentar glifos acentuados ao atlas;
- distribuir o `.cdae` gerado pelo jogo, como o R-19 da Fase 5, que já provou o caminho.

A técnica existe, mas é um pacote de trabalho próprio, de malha e não de textura, que não foi feito nesta fase.

### 2. Unidades e limites de velocidade (Fase 7)
- Os tiles MPH e SPEED LIMIT do `roadsigns.dae` (placas de advertência 15/20/25/30 MPH) ficam para a Fase 7.
- Trocar só a unidade criaria "25 km/h" falso.
- O valor tem de mudar junto com os dados funcionais (decal roads, waypoints de IA, zonas, radares), como já registrado na Fase 5.

### 3. Preservado de propósito
- **Marcas e nomes próprios:** LENS FLARE, SPEARLEAF, HOT ROLLED INC., RENT-A-BOX, TORRES TIRES, SMASH AUTO, BELASCO AUTO, TURBO BURGER, RIVERSIDE PLAZA, Jerry Riggs', Natalie's Nail 4, QUARRYSIDE, TRUSTED AUTO SALES e os patrocinadores.
- **Termos correntes no Brasil:** "% OFF", PEDICURE/MANICURE, DRIFT, DIESEL.
- **Chinês de Chinatown.**
- **Letras miúdas ilegíveis** (2–3 px).

## Verificações automáticas desta auditoria
- **Matriz:** 0 linhas `needs_context`. Linhas abertas sem classificação: 0.
- **`clutter_commercial`:** 85 elementos, todos com evidência UV (170 regiões). Os 8 sem evidência foram retirados do layout.
- **6G:** 8 famílias globais conferidas no índice de uso (`GLOBAL_SIGNS.md`).
