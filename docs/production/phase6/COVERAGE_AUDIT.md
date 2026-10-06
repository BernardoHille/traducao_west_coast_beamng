# 6H — Auditoria final de cobertura

**Data:** 06/10/2026.

**Pergunta:** depois da Fase 6, que inglês visível ainda resta no West Coast, e por quê?

## Método
1. **Matriz:** cada uma das 311 linhas (320 após o 6I) de `LOCALIZATION_MASTER.csv` foi classificada pelo status e pelo uso real no West Coast.
2. **Uso real:** a evidência é a pegada UV dos meshes **instanciados** (`compose.py regions`, `asset_usage.py`), não a presença no zip.
   - Uma família usada pode ter regiões que nenhum mesh amostra. Essas linhas passaram a `wcusa_usage = not_found`, com 12 correções nesta auditoria.
3. **Revisão visual:** os atlas usados foram percorridos inteiros, em especial `clutter_commercial`, com 188 meshes instanciados. O objetivo era achar inglês que não estivesse na matriz ou que tivesse ficado para trás.
4. **Malhas que montam palavras com glifos:** foram inspecionadas reconstruindo a placa a partir do `.dae` (`working/temporary/glyph_probe.py`).

## Classificação (320 linhas, após o bloco 6I)
| Classe | Linhas | Significado |
|---|---|---|
| produzido + QA no jogo | 148 | Textura ou malha nova no mod e captura PT-BR conferida (127 no fechamento do 6H + 21 do bloco 6I de letreiros de glifos) |
| produzido, sem ponto de QA próprio | 11 | Validado (regiões, DDS, família) e com evidência UV, mas sem enquadramento próprio. Inclui a lista de serviços, cuja face não aparece no jogo |
| `not_used` | 101 | Região ou família sem nenhum mesh/decal instanciado no West Coast |
| `preserve_original` | 45 | Marcas, nomes próprios, logos, pictogramas, chinês de Chinatown, "% OFF" |
| `out_of_scope` (Fase 7) | 15 | Dados funcionais (limites de velocidade, radares, zonas, slotTraffic) e tiles de unidade (MPH, SPEED LIMIT), inclusive a placa DO NOT STOP / SPEED LIMIT 25 da cabine de pedágio |
| pendente | 0 | As 12 linhas "pendente de mesh" do 6H foram resolvidas no bloco 6I (`GLYPH_SIGNS.md`) |
| `needs_context` | 0 | Todos resolvidos: bus_stops, studio_departments, bus_utah_stops, glifos |

## Inglês encontrado e corrigido durante a auditoria (`missed_translation`)
| Onde | Original | PT-BR | Evidência |
|---|---|---|---|
| Placa chinesa (8 prédios de Chinatown) | NO ENTRY | ENTRADA PROIBIDA (chinês preservado) | QA `cc_no_entry_cn` |
| RENT-A-BOX (`sign_rentabox`, `s_port_warehouse`) | SECURE STORAGE | GUARDA-VOLUMES SEGURO | QA `cc_rentabox` |

Os dois estavam na matriz (`commerce_chinese`, `commerce_rentabox`), mas tinham ficado fora do layout do atlas.

## Inglês que continua visível, e por quê
### 1. Palavras montadas por glifos no mesh: resolvidas no bloco 6I
Na auditoria, ainda estavam em inglês as palavras que o mapa monta letra por letra **no mesh**:
- fachadas e totens (MOTEL, FOOD MART, FULL SERVICE, EXHAUST, FIX, SOUND, STEREO, CAR PARTS);
- cartazes de preço e fachadas de prédios;
- MAP do abrigo;
- túnel do autódromo, pista de arrancada;
- ONLY, CARPOOLS, PER VEHICLE e ½ MILE dos pórticos.

Esses textos não existem como palavra no atlas, e trocar a célula de um glifo mudaria a mesma letra em todas as palavras.

**O que foi feito no 6I** (`GLYPH_SIGNS.md`):
- 25 meshes reescritos (quads das letras removidos e recriados no mesmo plano);
- 13 células de acento/sinal no `clutter_commercial`;
- 10 tiles novos no `t_roadsigns`;
- `.cdae` compilado pelo jogo distribuído junto.

**Verificação:**
- `validate.py new` confere que nada além das letras mudou em cada mesh;
- QA no jogo com 86 pontos original × PT-BR.

**Fora:** a placa DO NOT STOP / SPEED LIMIT 25 da cabine de pedágio, porque é limite de velocidade (Fase 7).

### 2. Unidades e limites de velocidade (Fase 7)
- Os tiles MPH e SPEED LIMIT do `roadsigns.dae` (placas de advertência 15/20/25/30 MPH) ficam para a Fase 7.
- Trocar só a unidade criaria "25 km/h" falso.
- O valor tem de mudar junto com os dados funcionais (decal roads, waypoints de IA, zonas, radares), como já registrado na Fase 5.

### 3. Preservado de propósito
- **Marcas e nomes próprios:** LENS FLARE, SPEARLEAF, HOT ROLLED INC., RENT-A-BOX, TORRES TIRES, SMASH AUTO, BELASCO AUTO, TURBO BURGER, RIVERSIDE PLAZA, Jerry Riggs', Natalie's Nail 4, QUARRYSIDE, TRUSTED AUTO SALES e os patrocinadores.
- **Termos correntes no Brasil:** "% OFF", PEDICURE/MANICURE, DRIFT, DIESEL, PRE-STAGE/STAGE (arrancada).
- **Chinês de Chinatown.**
- **Letras miúdas ilegíveis** (2–3 px).

## Verificações automáticas desta auditoria
- **Matriz:** 0 linhas `needs_context`. Linhas abertas sem classificação: 0.
- **`clutter_commercial`:** 85 elementos, todos com evidência UV (170 regiões). Os 8 sem evidência foram retirados do layout.
- **6G:** 8 famílias globais conferidas no índice de uso (`GLOBAL_SIGNS.md`).
