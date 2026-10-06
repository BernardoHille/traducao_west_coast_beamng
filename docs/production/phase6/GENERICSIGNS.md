# 6B — Postos / placas genéricas (`eca_genericsigns`)

**Data:** 05–06/10/2026 · **Status:** produção + QA no jogo (dia e noite).

## Qual arquivo o West Coast realmente usa (correção da Fase 3)
O material `eca_genericsigns` tem três definições no jogo:
- `art_shapes.zip`, `garage_and_dealership/Clutter`: material PBR com `t_eca_genericsigns_b.color` + `_o`/`_nm`/`_ao`/`_r`, `alphaRef` 60, sem emissivo;
- `east_coast_usa.zip` e `utah.zip`: legado, com `eca_genericsigns_d.dds` + `eca_genericsigns_emissive.dds` (glow).

Consultado com o mapa carregado (05/10/2026, `scenetree.findObject("eca_genericsigns")`), o West Coast usa o **PBR**: `baseColorMap` resolve para `assets/materials/billboard_label/eca_genericsigns/t_eca_genericsigns_b.color.dds`, e **não há emissivo**. A nota da Fase 3, segundo a qual o mapa carregava o `eca_genericsigns_d` do East Coast, está superada. A configuração do validador (`texture_families.json`) e a regressão foram corrigidas: a referência antiga continua reprovada, agora por `shape_changed`.

**Consequência para o emissivo:** a regra "cor = emissivo" não se aplica ao asset usado no West Coast. O par legado `eca_genericsigns_d` + emissivo pertence aos mapas East Coast, Utah e Hirochi e não foi alterado.

## Mapas
`_o`, `_nm`, `_ao` e `_r` contêm só o **contorno das placas**, sem letras (conferido visualmente). Os textos mudaram dentro das mesmas placas, então `shape_changed: false` e só a cor é entregue.

## Uso real (pegada UV dos meshes instanciados)
Meshes: `s_fuel_pump_2015` / `2000`, `s_fuel_charger_car_2020` / `2022`, `s_fuel_structure_01` / `03` / `05` / `06` / `07`, `s_fuel_sign_*` (14 meshes, incluindo prefabs de bombas).

| Região | Uso no West Coast | Resultado |
|---|---|---|
| NO SMOKING | sim | PROIBIDO FUMAR (*implemented*: face não localizada pela câmera) |
| DANGER / Highly Flammable | sim | PERIGO / ALTAMENTE INFLAMÁVEL |
| FLAMMABLE GAS 2 (girado 45°) | sim | GÁS INFLAMÁVEL 2 (texto girado na textura; fica horizontal na placa em losango) |
| STOP ENGINE / AVOID FIRE + legendas | sim | DESLIGUE O MOTOR / EVITE INCÊNDIO + legendas traduzidas |
| DANGER / FIRE RISK / FILLING CONTAINERS | sim | PERIGO / RISCO DE INCÊNDIO / AO ENCHER RECIPIENTES |
| NO PARKING ANY TIME | sim | PROIBIDO (branco sobre vermelho) / ESTACIONAR (vermelho sobre branco) + seta |
| NOTICE / AUTHORIZED PERSONNEL ONLY | sim | AVISO / SOMENTE PESSOAL AUTORIZADO |
| DIESEL / PUSH HERE | sim | DIESEL / APERTE AQUI |
| octanagem 87 / 89 / 93 | sim | GASOLINA COMUM / ADITIVADA / PREMIUM + OCTANAGEM (R+M)/2 + número preservado + APERTE AQUI |
| alfabeto e algarismos (glifos) | sim (letreiros compostos) | preservados |
| WARNING (bomba), PUMP NUMBER 1/2/3, distintivo, FIRWOOD INN, NODEOLINE, display de 7 segmentos | **não** | não editados |

**Octanagem:** 87/89/93 são AKI, (R+M)/2. O número fica, rotulado corretamente como `(R+M)/2`, e a categoria comercial brasileira vai no cabeçalho. Nunca "RON".

**Letras miúdas:** as legendas de 3–8 px do painel DESLIGUE O MOTOR foram traduzidas. Os parágrafos de 2–3 px da coluna direita são ilegíveis no jogo e ficaram como no original (classificados como ilegíveis, não como esquecimento).

**Preços:** os totens de preço do posto (painel "Unleaded/Premium/Diesel" + FOOD MART) não vêm deste atlas; ver `COMMERCIAL.md`.

## Método e validação
- **Master:** `working/layered/eca_genericsigns/layout.json` → `tools/production/compose.py`. A legenda antiga é detectada por cor e cresce pelos componentes conexos dentro da placa; o fundo é preenchido por difusão com o grão reaplicado, e o texto novo é desenhado na fonte de sistema.
- **PNG:** PASS, com 27 regiões (todas com evidência UV) e 0 px alterados fora delas.
- **DDS:** BC7_UNORM_SRGB, 11 mips, igual ao original. Família e mod: PASS.
- **QA:** `gs_*` em `tests/qa_locations.json`; capturas em `tests/screenshots/phase6/eca_genericsigns/` (dia; noite para octanagem e DESLIGUE O MOTOR).

## Revisão humana
- Alinhamento e recorte: sem deslocamento.
- Tipografia: Arial / Arial Narrow Bold no lugar da Helvetica condensada original (`human_typography_review_required`).
- Noite: placas legíveis sob a iluminação da cobertura.
