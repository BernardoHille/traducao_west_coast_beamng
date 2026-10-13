# Fase 7 — Placas de velocidade embutidas (roadsigns.dae) e praça de pedágio

A Fase 6 deixou estes itens para a Fase 7, porque são limite de velocidade: os tiles SPEED LIMIT e MPH do `roadsigns.dae` e a placa DO NOT STOP / SPEED LIMIT 25 da cabine de pedágio. O validador de velocidade da Fase 4 só olhava os objetos `sign_speed*.dae`, então essas placas não apareciam no relatório. Na Fase 7 elas passaram a ser conferidas (placa = dado).

## Onde estão

- **`roadsigns.dae`:** um único TSStatic (grupo StaticObjects, sem transformação: malha = mundo) com toda a sinalização montada do mapa. Levantamento por célula do atlas (`working/functional/speed_plates_survey.py` → `speed_plates.json`):
  - **23 placas regulamentares**: placa branca + "SPEED LIMIT" + 2 algarismos. Valores: 30 (4), 40 (10), 45 (1), 50 (3), 70 (5) mph;
  - **24 placas amarelas de advertência** sob placas de curva: 15 (9), 20 (5), 25 (7), 30 (3) MPH.
- **Praça de pedágio:** 5 cabines (prefab `p_toll_booth`, malhas `s_toll_booth_center.dae` e `_alt.dae`). Na ponta voltada ao trânsito ficam "DO NOT STOP" e "SPEED LIMIT 25".

Todas as células (placa, SPEED LIMIT, MPH, a linha de algarismos) são **compartilhadas** com outras placas: escudos de rodovia, saídas, pedágio. Nada foi editado no lugar.

## Decisão de valor

| Tipo | Regra | Resultado |
|---|---|---|
| Regulamentar | **R-19 com o limite aplicado na via que a placa regula**: a aresta mais próxima cujo fluxo legal vê a face (medida no jogo). É a mesma regra dos radares (spec §14/15): não se reduz uma via só porque o valor americano era menor. Nenhuma via muda por causa dessas placas. Vias da Fase 5 a 40 prevalecem | 40 ×2 (vias da Fase 5), 60 ×5 (vias de pista simples a 60), 80 ×3, 100 ×8 (vias rápidas/alças), 120 ×5 (rodovia) |
| Advertência | Tabela do projeto (LOCALIZATION_RULES §2.3), sem efeito funcional | 15 → 20, 20 → 30, 25 → 40, 30 → 50 km/h |
| Cabine de pedágio | 25 mph → **R-19 40** (tabela); as **5 faixas que atravessam as cabines** (DR535, DR559, DR595, DR630, DR672) recebem 40 explícito, como as cabines das docas na Fase 5. A malha é a mesma nas 5 cabines, então mostra um valor só, e as faixas tinham automáticos variados (50–120) | NÃO PARE / R-19 40 |

**Registro para revisão humana:** duas placas urbanas mostram 100 km/h porque o motor dá 100 às vias de duas faixas de mão única, inclusive na cidade:
- reg_03, Chinatown, era 30 mph;
- reg_07, trevo junction1, era 30 mph.

A placa diz a verdade sobre o que a IA faz. Reduzir essas vias a 50 seria uma decisão de limite urbano (como no Bloco A), fora do que a especificação mandou nesta fase: a especificação preserva os automáticos coerentes, e o mesmo trevo já teve o radar mantido em 100.

| Placa | Antes | Via regulada (aresta) | R-19 |
|---|---|---|---:|
| reg_00 | 30 mph | DR435 (Fase 5) | 40 |
| reg_01 | 30 mph | DR92 / wpTown (Fase 5) | 40 |
| reg_02, 09, 10, 15, 20 | 70 mph | rodovia (DR294, Bridge29) | 120 |
| reg_03 | 30 mph | DR554/DR677, Chinatown | 100 |
| reg_04 | 50 mph | DR623/DR641 | 80 |
| reg_05 | 70 mph | DR555 (alça) | 80 |
| reg_06, 11 | 40 mph | Bridge13, Bridge32 (alças elevadas) | 100 |
| reg_07 | 30 mph | junction1 wp10 → wp26 | 100 |
| reg_08, 12, 19, 22 | 45/50/40 mph | DR455, DR661, DR251, DR698 (pista dupla) | 100 |
| reg_13 | 40 mph | DR580 (alça) | 80 |
| reg_14, 16, 17, 18, 21 | 40 mph | DR149, DR252, DR230, DR676 (pista simples) | 60 |

## Como foi feito (sem tocar célula compartilhada)

1. **Faces novas em espaço livre do `t_roadsigns`.** "Livre" quer dizer opacidade original < 8 e nenhuma UV de malha do jogo; os tiles da Fase 6 ficam reservados. Gerador: `working/layered/t_roadsigns/speed_plate_tiles.py`; composição: `build_t_roadsigns.py`.
   - **R-19:** cópia da placa branca original com o disco do **master aprovado** (`build_r19.render`), desenhado em metros na proporção física da placa (0,678 : 1), para o disco sair redondo. O retângulo da placa fica: há uma face metálica 6 cm atrás de cada placa (malha compartilhada), e um disco recortado mostraria um retângulo cinza em volta. É a única diferença em relação ao R-19 dos `sign_speed*` (disco recortado), que têm malha própria.
   - **Advertência:** cópia da placa amarela original com "nn" sobre "km/h" em preto, na mesma face tipográfica dos números do R-19.
   - Tiles a 80 % da resolução da placa (cerca de 120 px/m), para caber no espaço livre.
2. **Re-apontamento quad a quad** (`glyph_rewrite.py`, `uv_map` com `"at"`: centroide do quad, raio de 2 cm). A placa de cada uma aponta para a face do seu valor; a legenda e os algarismos apontam para uma célula vazia (transparente). Foram 189 quads, cada um casado exatamente uma vez.
3. **Cabine de pedágio** (`toll_booth_tiles.py`). A placa de baixo é um conjunto 2 × 2 de quads com UV sobreposta (placa esticada). A face nova é **assada**: a placa inteira é desenhada em metros e cada quad recebe um tile próprio com exatamente a parte que cobre, amostrada pelo referencial de textura do próprio quad. São 2 LODs e 2 malhas (a `_alt` tem a face em y = −7,06), 10 tiles e 68 re-apontamentos.
4. `.cdae` compilado pelo jogo, copiado para o mod e apagado de `current/temp`.
5. Atlas: 19 tiles novos. Os 54 elementos das Fases 5/6 ficaram idênticos byte a byte (conferido refazendo o atlas sem os tiles novos). Tudo dentro das regiões autorizadas (73 de cor, 57 de opacidade).

## QA

- **Validador** (`validate.py speeds`):
  - 47 placas mostram a face decidida, lida da malha do mod, sem nenhum quad de legenda americana;
  - 23 R-19 = limite do navgraph na via regulada;
  - 24 advertências = tabela;
  - cabines: face NÃO PARE / R-19 40 nas 2 malhas e 5 faixas a 40 explícito;
  - teste negativo: a malha original faz a checagem reprovar as 47 placas.
- **No jogo:**
  - as 47 placas foram fotografadas de frente com o mod ligado e desligado: `tests/screenshots/phase7/speed_plates/*_ptbr.jpg` × `*_original.jpg` e folhas `_sheet_*.jpg`;
  - cabines em `tests/screenshots/phase7/toll_booth/`;
  - navgraph da faixa do pedágio: 40 (mod ligado) / 60 (desligado);
  - IA em `legal` pela praça: máx. 40,05 km/h.
