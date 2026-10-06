# 6C — Outdoors e concessionárias

**Data:** 06/10/2026.

## Outdoors (`t_billboards_b.color`)
O material `billboards` do West Coast resolve para `assets/materials/billboard_label/billboards/t_billboards_b.color.dds`. O `billboards_d` legado (sobre o qual a referência antiga foi feita) não é usado. A rugosidade `t_billboards_r` é uma textura genérica de painel, sem texto, e fica como no original.

Atlas 4 × 4 de painéis 512 × 256. Meshes: `billboards.dae` (um mesh único com todos os outdoors do mapa), placas da pista de arrancada (`dragbillboard_sign*`), fachadas (`s_bld_warehouse_002`, `s_diner_area_filler`, `s_building_stage_01`).

| Painel | Uso | PT-BR | QA |
|---|---|---|---|
| BLASTR | sim | SINTA A FÚRIA!! (logo preservado) | dia |
| Brightsmile | sim | "Recomendado por 4 em cada 5 dentistas" | dia |
| Turbo Burger | sim | NOVO MENU TURBO · R$ 4,99 (sem câmbio) | dia/noite |
| DriftGear | sim | SUPERANDO OS LIMITES DA INOVAÇÃO | dia |
| QUEENZ | **não** (nenhum mesh instanciado) | não editado | — |
| Feline Racerz | sim | JÁ / DISPONÍVEL · citação girada · DISPONÍVEL PARA GAMEMASTER720 E PC | dia |
| WCUSA | sim | WCUSA / AUTÓDROMO | dia |
| TastiCola | sim | NOVO SABOR! / AZUL / É O NOVO / VERMELHO | dia |
| Mente | sim | EXPRESSE-SE | dia |
| Rocking Rally Rental | sim | marca preservada · ECONOMIZE ATÉ / R$ 200 · linha Friendbook | dia |
| Clockwise | sim | logo preservado (sem alteração) | — |
| Alder | sim | Performance Americana Clássica | dia |
| eShock | sim | DESEMPENHO CHOCANTE | dia |
| GripAll | sim | A MARCA DE PNEUS / DE CONFIANÇA / DOS EUA (universo americano mantido) | dia |
| OJ | sim | VIVA SAUDÁVEL, / VIVA RÁPIDO | dia |
| Nodeoline | sim | Resistência / testada e / comprovada (nas 3 caixas vermelhas originais) | dia |

### Método
- Texto sobre fotos e ilustrações: a legenda antiga é detectada pelas cores de preenchimento e contorno (`rgbs`), com dilatação para pegar o anti-aliasing e o contorno. O preenchimento é feito por difusão a partir dos pixels vizinhos, sem passo generativo.
- O texto novo ocupa a mesma área, com contorno, sombra, inclinação ou rotação quando o original tinha.
- Correções feitas durante a revisão:
  - TastiCola: o azul-marinho do contorno casava com a onda do fundo, e a legenda passou a usar só preenchimento + sombra quase preta;
  - WCUSA, eShock e GripAll: os tons de cinza e escuros casavam com a foto, e a legenda passou a usar só o preenchimento claro.
- **Validação:** PNG PASS, com 19 regiões (todas com evidência UV) e 0 px fora delas. DDS BC7 sRGB, 12 mips.

## Concessionárias (`t_billboardsigns_dealers`)
- **Uso no West Coast:** a pegada UV dos 3 meshes instanciados (`s_busstop_wcu` ×31, `s_busstop_wcu_04` ×9, `s_flag_floor_teardrop_01` ×2) cobre **apenas glifos do alfabeto**. Nenhum painel é amostrado (BIG SALE, GREAT DEALS, USED CARS, 0% FINANCING…).
- **O que os glifos compõem:** pelo render offline (`render_signs.py`), o abrigo de ônibus mostra **"MAP"** e **"INFO"**.
  - "INFO" é corrente em português.
  - "MAP" exigia mesh próprio, porque "MAPA" precisa de mais um quad: refeito na malha do abrigo (`BUS_TRANSPORT.md`, `GLYPH_SIGNS.md`).
- **Consequência:**
  - os painéis da concessionária ficam como no original (asset global, sem uso no West Coast, prioridade baixa);
  - o problema de alfa da referência antiga não chega ao mod, porque nenhuma versão dela é distribuída;
  - QA de concessionária no West Coast não é possível, já que não há painel visível.
