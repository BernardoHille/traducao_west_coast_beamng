# 6D — Estúdio, indústria e patrocinadores

**Data:** 06/10/2026 · **Status:** produção + QA no jogo (dia; noite para SET FECHADO, ENTRADA PROIBIDA e REFINARIA).

Pipeline igual ao dos blocos anteriores:
1. hash do original;
2. pegada UV dos meshes instanciados no West Coast (`compose.py regions`);
3. master por elemento (`working/layered/<família>/make_layout.py` → `layout.json`);
4. PNG;
5. validação;
6. mapas auxiliares quando o texto é recortado ou tem relevo;
7. DDS no formato do original;
8. mod;
9. QA MCP com par original/PT-BR.

## Estúdio (`t_movie_studio_signage_b.color`, material `m_movie_studio_signage`)
**Atlas:** 1024 × 512, BC7 sRGB, 11 mips. Os logos LENS FLARE ficam como no original (marca). Resultado: 37 regiões com evidência UV, 0 px fora delas.

| Placa | PT-BR | QA |
|---|---|---|
| CLOSED SET (porta do estúdio) | PROIBIDA A ENTRADA COM LUZ VERMELHA ACESA / SET FECHADO / PROIBIDO FUMAR | st_closed_set (dia/noite) |
| STAGE 1/2/3 | ESTÚDIO 1/2/3 | st_stage1 |
| STOP + NO PEDESTRIAN / TRUCKS ONLY | PARE · PROIBIDO PEDESTRES · SOMENTE CAMINHÕES | st_stop_ped |
| EXIT ONLY / ENTRANCE ONLY | SOMENTE SAÍDA / SOMENTE ENTRADA | st_exit_entrance |
| Requisitos de entrada no estúdio | título, SET FECHADO, contato e telefones | st_requirements |
| GATE 1 / GATE 3 + legenda | PORTÃO 1 / PORTÃO 3 + "Visitantes e entregadores…" | st_gates |
| NO TAXI DROP OFF | PROIBIDO DESEMBARQUE DE TÁXI / USE O PORTÃO 3 | st_no_taxi |
| ENTRANCE FOR TRUCKS ONLY | ENTRADA SÓ PARA CAMINHÕES / VISITANTES USEM O PORTÃO PRINCIPAL | st_trucks_entrance |
| TOUR PARKING | ESTACIONAMENTO DA VISITA | st_tour_parking |
| STUDIO TOUR PARKING ENTRANCE / VISITOR ONLY | ENTRADA DO ESTACIONAMENTO / SOMENTE VISITANTES | st_tour_parking_entrance |
| STUDIO TOUR | VISITA AO ESTÚDIO | st_studio_tour |
| NO TRESPASSING / VIOLATORS… | ENTRADA PROIBIDA / INFRATORES SERÃO PROCESSADOS | st_trespassing |
| SECURITY CHECK + ALL VEHICLES… | PARE · INSPEÇÃO DE SEGURANÇA · VEÍCULOS E PERTENCES SUJEITOS A INSPEÇÃO | st_security |
| NOTICE / VIDEO SURVEILLANCE | AVISO / PRÉDIO SOB VIDEOMONITORAMENTO | st_surveillance |
| COURIER DELIVERY ZONE | ÁREA DE ENTREGAS | st_courier |
| NO PARKING / LOADING AREA | PROIBIDO ESTACIONAR / CARGA E DESCARGA | st_loading |
| Visitantes ao escritório | linha traduzida | st_visitors_office |

**Não usadas no West Coast** (cobertura UV 0, não editadas): DO NOT ENTER / ONE WAY, NOTICE de revista, cabeçalho NO TRUCKS e linha de ID, NO TRUCK IDLING, SOON TO RISE, PRIVATE PROPERTY, GATE 2, ONE WAY de portão, RESTRICTED AREA / Keep Out, STAGE 4, DANGER DEEP EXCAVATION, HARD HAT / PPE, mapa do estúdio, departamentos (DRAPERY…) e credenciais de visitante. Na matriz, `studio_departments` deixou de ser `needs_context`: não é usado.

**Correções durante a revisão:**
- ENTRANCE ONLY: a caixa grande apagava parte da placa vizinha e foi reduzida a `[905, 328, 1014, 359]`;
- título dos requisitos: sobravam restos e a legenda passou a ser escura;
- CLOSED SET: linha do REC com estilo próprio.

## Indústria (`ind_industrial_signs_d.color`, material `industrial_signs`)
O material aponta para `/levels/jungle_rock_island/art/shapes/buildings/ind_industrial_signs_d.color.png`. Esse caminho legado existe em `jungle_rock_island.zip`, e o mesmo nome existe em `assets/materials/billboard_label/industrial_signs`. As duas cópias diferem levemente; **cada uma** é reconstruída a partir do **seu** original (variante `jungle_rock_island` em `source/originals/png/`). Por isso a família declara os dois caminhos (`extra_paths`).

**Atlas:** 1024 × 512, BC7 sRGB, 11 mips. Resultado: 13 regiões, 0 px fora delas.

| Placa | PT-BR | QA |
|---|---|---|
| FLAMMABLE / NO SMOKING | INFLAMÁVEL / PROIBIDO / FUMAR | ind_in_flam_no, ind_in_flam_smoking |
| EXIT (placa vermelha suja) | SAÍDA | ind_in_exit |
| Fire Extinguisher / CARBON DIOXIDE | Extintor / DIÓXIDO DE CARBONO | ind_in_ext_hdr, ind_in_ext_co2 |
| THINK SAFE | PENSE EM SEGURANÇA | ind_in_think |
| NO SMOKING / Extinguish all cigarettes… | PROIBIDO FUMAR / Apague o cigarro antes de entrar. | ind_in_nosmoke_hdr / body |
| TOXIC HAZARDOUS CHEMICALS… | PRODUTOS QUÍMICOS TÓXICOS EM USO NESTE LOCAL · FDS DISPONÍVEIS | ind_in_toxic |
| Emergency exit | Saída de emergência | ind_in_emergency |
| NO TRESPASSING (placa enferrujada da cerca) | ENTRADA PROIBIDA | ind_in_trespass (dia/noite) |
| Danger (placa pequena) | Perigo | ind_in_danger_small |

- **Não usadas no West Coast** (31 linhas da matriz, `wcusa_usage = not_found`): Texas Waste, horário, SPEED LIMIT 15, MAX HEADROOM, EPI, empilhadeiras, alta tensão, balança, entre outras.
- **Letras miúdas:** a tabela de classes do extintor (2–3 px) é ilegível no jogo e ficou como no original.
- **NO TRESPASSING:** a legenda é cinza claro sobre ferrugem. A detecção usa vários tons de cinza (`rgbs`, tol 28), para que não sobrem contornos do NO.

## Patrocinadores e marcas
| Item | Decisão | Mapas | QA |
|---|---|---|---|
| Spearleaf (`t_spearleaf_refinery_logo`) | SPEARLEAF preservado; REFINERY → **REFINARIA** (Georgia, mesma linha) | cor + opacidade (`m_refinery_logo`, alphaTest 135: as letras são recortadas pela máscara, que foi refeita junto) | t_spea_refinery (dia/noite) |
| Hot Rolled (`t_steel_factory_brand`) | HOT ROLLED INC. preservado; STEEL MANUFACTURING → **FABRICAÇÃO DE AÇO** | cor + `_nm` / `_ao` / `_r` (as letras têm relevo; o perfil de borda foi refeito para o texto novo) | t_stee_steel_descriptor |
| `t_sponsors` (EK, GRIPALL, DriftGear, BLASTR…) | preserve_original (marcas) | — | — |
| Sealbrik, logos de concessionária, garagem da carreira | preserve_original | — | — |

**DDS:**
- Spearleaf: cor BC7 sRGB e opacidade BC4.
- Steel: cor BC7 sRGB, normal BC5, AO e rugosidade BC4.
- Todos com 11 mips, igual aos originais.

**Validação:**
- família PASS (`shape_changed` declarado e todos os mapas dependentes entregues);
- PNG: 1 região cada, 0 px fora.

## QA MCP
- Ciclo `tools/beamng/qa_cycle.py` de 06/10/2026, 07:16–07:37: instalação verificada byte a byte, depois capturas original e PT-BR (dia; noite com 12 s de assentamento do preset).
- **0 problemas de VFS** em todos os runs (`tests/reports/phase6/runs/`).
- Capturas: `tests/screenshots/phase6/{t_movie_studio_signage, ind_industrial_signs, t_spearleaf_refinery_logo, t_steel_factory_brand}/`.
- O mesmo ciclo repetiu a sanidade da Fase 5 em PT-BR: PARE em Chinatown, R-2 no centro e R-19 40 na colina. Nenhuma regressão.

## Revisão humana
- **Alinhamento:** sem deslocamento em nenhuma placa enquadrada.
- **Tipografia:**
  - estúdio e indústria usam Bahnschrift/Arial no lugar das fontes originais (`human_typography_review_required`);
  - REFINARIA usa Georgia, próxima da serifa original.
- **Noite:** SET FECHADO, ENTRADA PROIBIDA e REFINARIA legíveis.
