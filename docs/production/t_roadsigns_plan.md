# Plano de produção — família `t_roadsigns` (Fase 5)

**Base:** somente os originais (`source/originals/png/t_roadsigns_b.color.png` e `t_roadsigns_o.data.png`, SHA-256 conferido contra `docs/inventory/original_files_manifest.csv` pelo próprio script).
**Referência antiga** (`source/reference_ptbr/t_roadsigns_b.color_ptbr.png`): consultada só para o texto; nenhum pixel dela foi usado.
**Master reproduzível:** `working/layered/t_roadsigns/` (`layout.json` + `build_t_roadsigns.py` + `regions.json`).

## 1. Como as regiões foram confirmadas

1. **Meshes que usam o material `roadsigns`:** os 45 `.dae` do West Coast que referenciam o material foram extraídos, só por leitura, para `source/originals/meshes/` (fora do Git; SHA em `_extracted.csv`).
2. **Instâncias reais:** `tools/production/scan_level_usage.py` contou os `shapeName` no zip do nível (`working/layered/t_roadsigns/mesh_usage.json`).
3. **Pegada UV:** `tools/production/dae_uv.py` rasteriza os triângulos UV de cada mesh sobre o atlas 2048×1024. Um elemento só é editado se meshes **instanciados** cobrem ≥ 40 % da caixa dele. O limiar de 40 % existe porque o R-2, triangular, preenche ~50 % do retângulo. O resultado vai para `regions.json`, com a cobertura por mesh, e alimenta `tools/validation/config/allowed_regions.json`.
4. **Composição:** `tools/production/render_signs.py` reconstrói offline cada placa composta (painel + quads de palavras flutuando à frente, recorte pelo mapa de opacidade e cor de vértice). Foi assim que se viu que:
   - várias palavras são **recortadas pelo `_o.data`** (nomes de ruas, EXIT/NEXT, pontos cardeais, TOLL, CAUTION/TOLL PLAZA/AHEAD, ROAD/WORK, ROAD CLOSED estêncil, CAUTION UNDER CONSTRUCTION). Traduzi-las exige reescrever também a máscara (`shape_changed: true`);
   - **ROAD + WORK + AHEAD** formam "ROAD WORK AHEAD" no losango, e **AHEAD** também fecha "CAUTION TOLL PLAZA AHEAD". Por isso AHEAD → "À FRENTE" serve aos dois: "OBRAS / NA VIA / À FRENTE" e "ATENÇÃO / PEDÁGIO / À FRENTE";
   - **Spearleaf Island** são dois quads ("Spearleaf" + "Island"). Viram "Ilha" + "Spearleaf", o que lê certo empilhado ou lado a lado;
   - **glifos compartilhados que não podem mudar** (ver §3).
5. **Uso parcial:** um quad que mostra só um pedaço do elemento indica glifo reutilizado. Esses elementos foram preservados.

## 2. Inventário

Ação: `edit` (alterado), `preserve`, `dedicated_asset`, `needs_implementation` (regra definida, mas exige mesh/recomposição), `not_used_wcusa` (nenhum mesh instanciado amostra a região: não editado; regiões sem UV não viram região autorizada).

| id | original | PT-BR | UV (px, x × y) | mesh (instâncias no WCUSA) | uso WCUSA | ação |
|---|---|---|---|---|---|---|
| stop_r1 | STOP | PARE | 1164–1290 × 231–358 | sign_stop.dae ×52, roadsigns.dae ×1 | sim | edit (cor) |
| yield_r2 | YIELD | R-2 sem legenda (campo branco, orla vermelha) | 1282–1456 × 236–384 | sign_yield.dae ×4 | sim | edit (cor) |
| do_not_enter_r3 | DO NOT ENTER | R-3 sem texto (disco vermelho + barra branca) | 640–794 × 166–314 | s_police_station.dae ×1, offramp_port.dae ×1, roadsigns.dae ×1 | sim | edit (cor) |
| wrong_way | WRONG WAY | CONTRAMÃO | 643–791 × 316–418 | offramp_port.dae ×1, roadsigns.dae ×1 | sim | edit (cor) |
| no_parking_any_time | NO PARKING ANY TIME (+ seta) | PROIBIDO / ESTACIONAR | 800–918 × 198–324 | roadsigns.dae ×1 | sim | edit (cor) |
| no_parking_bus_stop | NO PARKING BUS STOP (+ seta) | PROIBIDO / ESTACIONAR / PONTO DE / ÔNIBUS | 919–1035 × 199–371 | roadsigns.dae ×1 | sim | edit (cor) |
| red_light_violation | RED LIGHT VIOLATION $400 FINE | AVANÇO DE SINAL / VERMELHO / MULTA / R$ 400 | 1035–1162 × 197–350 | roadsigns.dae ×1 | sim | edit (cor) |
| do_not_block_intersection | DO NOT BLOCK INTERSECTION | NÃO / BLOQUEIE O / CRUZAMENTO | 1157–1283 × 359–510 | roadsigns.dae ×1 | sim | edit (cor) |
| parking_2h_green_box | 2 HOUR PARKING 8 A.M. TO 9 P.M. MON THRU SAT EXCEPT VEHICLES WITH AREA C PERMITS | 2 h | 1004–1054 × 431–476 | roadsigns.dae ×1 | sim | edit (cor) |
| parking_2h_green_text | 2 HOUR PARKING 8 A.M. TO 9 P.M. MON THRU SAT EXCEPT VEHICLES WITH AREA C PERMITS | ESTACIONAMENTO / 8h ÀS 21h / SEG A SÁB / EXCETO VEÍCULOS COM PERMISSÃO / ZONA | 1005–1153 × 430–592 | roadsigns.dae ×1 | sim | edit (cor) |
| parking_2h_7am_6pm | 2 HOUR PARKING 7AM TO 6PM EXCEPT SUNDAY | 2 h / ESTACIONAMENTO / 7h ÀS 18h / EXCETO DOMINGOS | 860–970 × 519–683 | roadsigns.dae ×1 | sim | edit (cor) |
| left_turn_green_arrow | LEFT TURN ON GREEN ARROW ONLY | CONVERSÃO À ESQUERDA / SOMENTE COM / SETA VERDE | 1094–1198 × 592–728 | roadsigns.dae ×1 | sim | edit (cor) |
| danger_header | DANGER HIGH VOLTAGE | PERIGO | 924–1092 × 712–772 | transformer_ground.dae ×31 | sim | edit (cor) |
| danger_body | DANGER HIGH VOLTAGE | ALTA TENSÃO | 924–1092 × 772–836 | transformer_ground.dae ×31 | sim | edit (cor) |
| speed_camera | MUNICIPAL SPEED CAMERA IN USE | FISCALIZAÇÃO / ELETRÔNICA / DE / VELOCIDADE | 1643–1803 × 788–1019 | s_sign_speedcam.dae ×6 | sim | edit (cor) |
| red_light_camera | RED LIGHT PHOTO ENFORCED | FISCALIZAÇÃO / ELETRÔNICA / AVANÇO DE SINAL | 1805–2047 × 789–1019 | s_sign_lightcam.dae ×1 | sim | edit (cor) |
| g_exit | EXIT | SAÍDA | 244–340 × 8–46 | s_police_station.dae ×1, roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_next | NEXT | PRÓXIMA | 244–340 × 48–85 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_east | EAST | LESTE | 244–342 × 87–125 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_west | WEST | OESTE | 244–342 × 126–162 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_north | NORTH | NORTE | 247–356 × 162–198 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_south | SOUTH | SUL | 247–356 × 199–236 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_toll | TOLL | PEDÁGIO | 438–521 × 146–181 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_caution | CAUTION TOLL PLAZA AHEAD | ATENÇÃO | 960–1120 × 10–42 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_toll_plaza | CAUTION TOLL PLAZA AHEAD | PEDÁGIO | 926–1148 × 43–74 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_ahead | CAUTION TOLL PLAZA AHEAD | À FRENTE | 978–1101 × 75–109 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_road | ROAD WORK | OBRAS | 657–749 × 656–690 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_work | ROAD WORK | NA VIA | 750–849 × 656–690 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| g_road_closed_stencil | ROAD CLOSED (letreiro estêncil) | VIA / INTERDITADA | 1208–1390 × 587–699 | construction_sign_small_c.dae ×3, construction_sign_big_b.dae ×1 | sim | edit (cor + opacidade) |
| g_caution_under_construction | CAUTION UNDER CONSTRUCTION | ATENÇÃO / EM OBRAS | 1409–1742 × 88–234 | construction_sign_small_a.dae ×3, construction_sign_big_b.dae ×1 | sim | edit (cor + opacidade) |
| n_brittlebush_st | Brittlebush St | Rua Brittlebush | 1–234 × 231–268 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_belasco_city | Belasco City | Belasco | 1–212 × 269–309 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_mojave_rd | Mojave Rd | Estrada Mojave | 1–196 × 496–536 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_agave_trail_rd | Agave Trail Rd | Estrada Agave Trail | 1–244 × 574–614 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_promenade | Promenade | Calçadão | 1–188 × 614–649 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_motorsports_park | Motorsports Park | Autódromo | 1–286 × 682–722 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_casilda_beach | Casilda Beach | Praia Casilda | 1–235 × 755–790 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_mount_wallis | Mount Wallis | Monte Wallis | 1–213 × 790–825 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_canal_st | Canal St | Rua do Canal | 1–152 × 825–858 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_dockyards | Dockyards | Docas | 0–210 × 858–896 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_financial_district | Financial District | Centro Financeiro | 2–288 × 896–934 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_downtown_belasco | Downtown Belasco | Centro de Belasco | 2–316 × 934–973 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_spearleaf_island_a | Spearleaf Island | Ilha | 3–172 × 978–1023 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| n_spearleaf_island_b | Spearleaf Island | Spearleaf | 172–285 × 978–1017 | roadsigns.dae ×1 | sim | edit (cor + opacidade) |
| roadsigns_digits | 0 1 2 … 9 | (inalterado) | 340–900 × 0–84 | roadsigns, sign_speed5/25 (antes), toll booth, túneis, armazéns | sim | preserve — glifos compartilhados |
| roadsigns_speed_limit_tile | SPEED LIMIT | (inalterado) | 229–363 × 284–381 | roadsigns.dae (SPEED LIMIT 30/40/70 mph), s_toll_booth (letras S,P,E,D,L,I,M,T avulsas) | sim | preserve — glifos compartilhados; pendência (R-19 próprios para as placas do roadsigns.dae) |
| roadsigns_mph_tile | MPH | (inalterado) | 256–352 × 244–279 | roadsigns.dae (placas de advertência 15/20/25/30 MPH) | sim | needs_implementation — trocar a unidade sem trocar o número mentiria (25 MPH → "25 km/h") |
| roadsigns_only | ONLY | (inalterado) | 352–440 × 141–186 | roadsigns.dae ×12; s_toll_booth_center(_alt): letras O e N avulsas em "DO NOT STOP" | sim | preserve — glifos compartilhados; pendência |
| roadsigns_carpools | CARPOOLS ONLY / 2 OR MORE PERSONS / PER VEHICLE | (inalterado) | 1409–1742 × 0–88; 685–876 × 72–116 | roadsigns.dae; o "P" de CARPOOLS (1484–1505 × 11–37) é reutilizado pela placa "proibido estacionar (P)" | sim | preserve — glifo compartilhado; pendência (asset dedicado) |
| roadsigns_fractions_miles | ¼ ½ ¾ + MILES | (inalterado) | 340–520 × 84–143; 638–780 × 116–153 | roadsigns.dae (pórticos, pedágio "½ MILE") | sim | needs_implementation — conversão exige recompor a placa |
| roadsigns_no_u_turn_text | NO U TURN | — | 805–922 × 118–192 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_tunnel | TUNNEL | — | 636–800 × 612–655 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_one_way | ONE WAY | — | 926–1160 × 116–196 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_road_closed_board | ROAD CLOSED (placa branca) | — | 1040–1160 × 352–420 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_cam_speed_red | SPEED & RED LIGHT | — | 1473–1640 × 786–1021 | s_sign_speedlightcam.dae (0 instâncias) | não | not_used_wcusa |
| roadsigns_place_creosote_st | Creosote St | — | 5–190 × 313–340 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_place_fog_hill | Fog Hill | — | 5–120 × 349–382 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_place_rush_rd | Rush Rd | — | 5–134 × 390–416 | nenhum mesh instanciado | não | not_used_wcusa (needs_context resolvido) |
| roadsigns_place_mariposa_st | Mariposa St | — | 5–191 × 425–458 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_place_outcrop_rd | Outcrop Rd | — | 4–184 × 540–573 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_place_sorrel_st | Sorrel St | — | 4–144 × 652–679 | nenhum mesh instanciado | não | not_used_wcusa |
| roadsigns_place_sierra_vista | Sierra Vista | Sierra Vista | 4–190 × 465–492 | roadsigns.dae | sim | preserve — nome próprio |
| roadsigns_place_san_amaro | San Amaro | San Amaro | 4–179 × 726–752 | roadsigns.dae | sim | preserve — nome próprio |
| roadsigns_picto_* | pictogramas (reboque, caminhão, retorno, semáforo, setas, diamante, trabalhador, escudo) | (inalterado) | vários | vários | sim | preserve — sem texto |

O R-19 virou `dedicated_asset`: família nova `roadsigns_ptbr_r19` (ver `PHASE5_ROADSIGNS.md`).
- `sign_speed25.dae` é substituído no mesmo caminho (11 placas).
- O R-19 10 é um mesh novo, atribuído só às 7 placas reais de 5 mph. Os outros 30 `sign_speed5.dae` (`port/portNumbersSigns`) são decalques de fundo dos números das baias e continuam usando o painel branco do atlas.
- O painel branco (370–516 × 189–381), o tile SPEED LIMIT e os algarismos **não** foram alterados.

## 3. Elementos preservados por compartilhamento (pendências registradas)

| Elemento | Por que não muda | Caminho futuro |
|---|---|---|
| Algarismos 0–9 | compõem docas, pedágios, túneis, armazéns e as placas de velocidade do `roadsigns.dae` | — (preservar) |
| SPEED LIMIT / MPH | o `roadsigns.dae` tem placas SPEED LIMIT **30/40/70** e de advertência **15/20/25/30 MPH**; o `s_toll_booth_center` monta "DO NOT STOP / SPEED LIMIT 25" com **letras avulsas** de SPEED/LIMIT/ONLY | R-19/advertência próprios para esses objetos (fase funcional futura) |
| ONLY | letras O e N reutilizadas pela cabine de pedágio | idem |
| CARPOOLS ONLY / 2 OR MORE PERSONS / PER VEHICLE | o "P" de CARPOOLS é o pictograma da placa "proibido estacionar (P)" | asset dedicado |
| ¼ ½ ¾ / MILES | distância em milhas composta por glifos | recomposição (`needs_implementation`) |

## 4. `needs_context` desta família

| Entrada | Resolução |
|---|---|
| `roadsigns_place_rush_rd` (Rush Rd) | **not_used_wcusa**: nenhum mesh instanciado do West Coast amostra a região (pegada UV = 0 %). Sem objeto físico não há contexto para decidir entre Rua e Estrada. O tile fica como no original. Se algum mapa vier a usá-lo, vale o padrão da regra (§4, "Rd" fora do centro → **Estrada Rush**). |

## 5. Tipografia

Todas as fontes são do sistema (Windows) e não foram copiadas para o repositório.

| Categoria | Fonte | Observação |
|---|---|---|
| Regulamentação (PARE, CONTRAMÃO, PROIBIDO ESTACIONAR, NÃO BLOQUEIE…), fiscalização, perigo, estacionamento | **Bahnschrift** (Microsoft, desenho DIN 1451), peso 450–700, largura variável 75–100 | `human_typography_review_required`: aproximação da **Série D/E(M)** do MBST, que não está disponível |
| Nomes de vias e destinos (tiles recortados) | **Bahnschrift** SemiBold, largura ajustada (eixo *wdth*) até caber no quad UV | `human_typography_review_required`: o original usa uma gótica rodoviária americana |
| Pontos cardeais | Bahnschrift com versalete (inicial 100 %, demais 76 %) | reproduz "EAST" → "LESTE" no mesmo estilo |
| ROAD CLOSED (estêncil) | Bahnschrift Bold | o original é estêncil; a fonte não tem pontes de estêncil (`human_typography_review_required`) |

Primeiro o script estreita a largura variável da fonte (eixo *wdth*, até 75). Só se o texto ainda não couber é que ele comprime na horizontal, de modo que as letras continuam sendo letras desenhadas e não esticadas.

## 6. Método de edição (determinístico)

1. Abre os PNG **originais** e confere o SHA-256.
2. **Painéis** (texto no `_b.color`, máscara opaca): o script detecta os pixels da legenda por distância de cor (legenda × fundo, incluindo a borda anti-aliased) dentro das caixas `erase`. Depois preenche por difusão a partir do fundo vizinho e reaplica o grão com resíduos do próprio fundo limpo, e desenha o texto novo (supersampling 4×) na cor mediana da legenda original.
3. **Tiles recortados**: reescreve a máscara do tile (texto novo em 0–255, borda anti-aliased) e pinta o `_b.color` das letras com a cor original, mais 3 px de sangria para o filtro bilinear e os mips não puxarem o fundo.
4. **R-2**: o triângulo externo e a borda branca externa ficam. O campo branco é ampliado até deixar uma orla vermelha de 20 px, medidos pelas arestas do triângulo vermelho original (ajuste robusto, sem tocar o octógono do PARE ao lado).
5. **R-3**: o disco, a barra e o aro são detectados automaticamente; só as palavras saem.
6. Fora das 44 caixas, o PNG é cópia **pixel a pixel** do original (validador: 0 px fora das regiões).

Comando: `python working/layered/t_roadsigns/build_t_roadsigns.py build && … preview`.
