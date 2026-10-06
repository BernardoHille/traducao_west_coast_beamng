# 6F — Comercial (`clutter_commercial`)

**Data:** 06/10/2026 · **Status:** atlas produzido e validado; QA no jogo (dia, e noite nos néons e na concessionária). Os letreiros compostos por glifos foram refeitos na malha (6I, `GLYPH_SIGNS.md`).

## Qual arquivo o West Coast usa
O material `clutter_commercial` carregado no West Coast é o de `art_shapes.zip`:
- `art/shapes/garage_and_dealership/Clutter/clutter_commercial_b.color.dds`;
- opacidade `clutter_commercial_o.data.dds` com `alphaTest` 64.

A pasta do nível (`levels/west_coast_usa/art/shapes/buildings`) tem **outra cópia**, que difere nos tiles de néon e liquidação e inclui, por exemplo, "Business Hours" e "NO WALK-INS". O material carregado não a referencia, então ela não foi alterada (variante `art_shapes` em `source/originals/png/`). A nota da família no validador, que dizia que as cópias eram idênticas, foi corrigida.

**Atlas:** 2048 × 2048. Contém:
- placas de comércio e concessionária;
- néons de Chinatown;
- cartazes de liquidação;
- alfabetos de glifos;
- logos de marcas.

## O que foi produzido
**85 elementos**, todos com evidência UV (pegada dos 188 meshes com instância). Resultado: 170 regiões registradas (cor + opacidade) e 0 px alterados fora delas.

| Grupo | PT-BR | Mesh com instância (exemplo) | QA |
|---|---|---|---|
| Néons de Chinatown | UNHAS E DEPILAÇÃO · SALÃO DE BELEZA · ABERTO · LAVANDERIA · Depilação FACIAL | `s_bld_chinatown_001/003` | cc_neon_nails (dia/noite), cc_neon_dry |
| Cardápio do salão | Design 3D · Aerografia · Unha em Gel · Unha Acrílica (PEDICURE/MANICURE já são português) | `s_bld_chinatown_001` | cc_nail_menu |
| Cartazes | OFERTA% (×2) · ITENS SELECIONADOS · LOJA TODA · QUEIMA TOTAL ("% OFF" mantido, uso corrente no varejo) | `chinatown_corner2`, `s_bld_chinatown_002/013` | cc_sale |
| Placa chinesa | 此路不通 preservado · NO ENTRY → ENTRADA PROIBIDA | 8 prédios de Chinatown | cc_no_entry_cn |
| Logística / galpões | LOGÍSTICA E DISTRIBUIÇÃO · ESTACIONAMENTO EXCLUSIVO DE FUNCIONÁRIOS (×2) · VISITANTES DEVEM SE APRESENTAR AO ESCRITÓRIO | `sign_logistics`, `s_port_warehouse`, `warehouse_awning` | cc_logistics |
| Cerca industrial | ATENÇÃO / ESTACIONE POR SUA CONTA E RISCO · PROIBIDO JOGAR LIXO · PROPRIEDADE PRIVADA ENTRADA PROIBIDA · SEMINOVOS (letras empilhadas) | `industrial1_fencing` | cc_fencing_risk, cc_used_cars |
| Portão / garagem | PROIBIDO ESTACIONAR · VEÍCULOS BLOQUEANDO O PORTÃO SERÃO GUINCHADOS · ATENÇÃO / PROIBIDO FUMAR | `garage_industrial`, `dealership_mid` | cc_garage_gate |
| Cilindros de gás | GÁS INFLAMÁVEL 2 (girado) · PERIGO / Altamente Inflamável · AVISO / SOMENTE PESSOAL AUTORIZADO | `gas_cylinder` | cc_gas_cylinder |
| RENT-A-BOX | marca preservada · SECURE STORAGE → GUARDA-VOLUMES SEGURO | `sign_rentabox`, `s_port_warehouse` | cc_rentabox |
| Concessionárias | GARANTIA / DE 3 ANOS (em arco) / DISPONÍVEL · SEM / ENTRADA · MELHORES OFERTAS GARANTIDAS · MEGA OFERTA! · ÓTIMAS OFERTAS · CARROS NOVOS · SAIA DIRIGINDO / HOJE · VENDAS E SERVIÇOS | `dealership_mid/new`, `s_dealership_sign` | cc_warranty, cc_no_deposit, cc_best_deals, cc_big_sale (dia/noite), cc_drive_away, cc_auto_sales |
| Oficinas | ESCRITÓRIO · ENTRADA · SAÍDA · PROIBIDO FUMAR · SERVIÇOS · AVISO + avisos · PROIBIDO ESTACIONAR · GARAGEM EM USO CONSTANTE… · lista de serviços · Posto de Inspeção Veicular · RECEBEMOS ÓLEO USADO E BATERIAS GRATUITAMENTE | `warehouse_awning`, `garage_bridge`, `s_workshop` | cc_facility |
| Pneus / freios | As pastilhas certas para o seu veículo · TROCA DE PNEUS E ALINHAMENTO · 15% DE DESCONTO · NA COMPRA DE UM JOGO DE PNEUS · Atendemos Todas as Marcas! · Conserto Rápido e Instalação de Peças (Jerry Riggs' preservado) | `garage_racetrack`, `garage_industrial` | cc_tire, cc_rapid_repair |
| Placa do limão | TEM UMA BOMBA? · Pagamos o melhor preço por carros para sucata de qualquer marca! | `sign_lemon` | cc_lemon |

**Sem uso no West Coast** (cobertura UV menor que 0,4; não editados):
- ENTIRE STORE 60% OFF;
- os dois BIG SALE ovais;
- o ícone NO SMOKING pequeno;
- EAST BELASCO TENNIS CLUB;
- WARNING da bomba;
- STOP ENGINE desta cópia;
- a bandeira AUTO REPAIR.

**Lista de serviços** (`garage_bridge`, cobertura UV 1,0): produzida e validada, mas a face que a UV indica aparece no jogo como painel corrugado liso dos dois lados. Fica `implemented`, não `qa_passed`.

## Método
1. **Caixas medidas sobre o original:**
   - as leituras iniciais em grade grossa erravam até 20 px;
   - cada caixa foi conferida numa folha de contato ou medida em zooms de 2–8× com grade de 10 px (`make_layout.py`, conjuntos `ACCEPT_FIT` e `M`).
2. **Detecção da legenda:**
   - por cor; em faixas desbotadas (WARNING, AVAILABLE), por "tudo que não é o vermelho da faixa";
   - o preenchimento é feito por difusão a partir dos vizinhos, sem passo generativo.
3. **Acentos:** a área de desenho de cada elemento reserva 45% da altura das maiúsculas acima e 30% abaixo. Assim o acento de ÓTIMAS, LOGÍSTICA e TÊNIS não é cortado.
4. **Texto em arco:** "DE 3 ANOS" segue o anel do selo de garantia, como WARRANTY no original (`compose.py`, linhas com `arc` e apagamento por setor anular `erase_ring`).
5. **Recortes de opacidade:**
   - os néons e os cartazes SALE% são recortados letra a letra pela máscara (`alphaTest` 64);
   - a regra `cutout` limpa a máscara onde a legenda antiga foi apagada e acrescenta as letras novas, com contorno e brilho;
   - nos néons, toda a área apagada é limpa; na LAVANDERIA, só a legenda dilatada, para preservar o cabide;
   - a família passa a declarar `shape_changed: true` e entrega `_o.data`.

## Validação
- **PNG** cor e opacidade: PASS (85 regiões, 0 px fora).
- **DDS:** cor BC7 sRGB e opacidade BC4, 12 mips, iguais aos originais.
- **Família:** PASS (mapa de opacidade entregue). **Mod:** PASS.

## QA MCP
- **Ciclos:** `qa_cycle.py` de 06/10/2026 (≈11:55–12:05 e ≈12:07–12:17; o segundo com a versão final), cada um com estado original e PT-BR.
- **Cobertura:** 21 pontos, todos de dia; noite em `cc_neon_nails` e `cc_big_sale`.
- **Resultado:** 0 problemas de VFS. A sanidade da Fase 5 (PARE, R-2, R-19 40) segue intacta.
- **Correções feitas a partir do QA:**
  - SAIA DIRIGINDO saía cortado ("SAIA DIRIGINI"). O texto girado era montado na horizontal além da borda do atlas (x > 2048). Agora `compose.py` desenha textos girados numa tela com margem e recorta depois da rotação. Recompor `eca_genericsigns`, `t_billboards` e `t_bus_routes_wca` deu 0 px de diferença;
  - pontos `cc_auto_sales`, `cc_services` e `cc_tire` reenquadrados (instância, lado, altura).
- **Revisão humana:**
  - o cabide da LAVANDERIA ficou com falhas onde as letras DRY o cruzavam;
  - os néons novos têm brilho um pouco menor que o original, porque o halo abaixo do `alphaTest` é cortado;
  - tipografia Bahnschrift/Arial/Impact no lugar das fontes originais (`human_typography_review_required`).

## Letreiros compostos por glifos
Fachadas como MOTEL, FOOD MART, FULL SERVICE, EXHAUST, FIX, SOUND, STEREO e CAR PARTS **não estão escritas no atlas**: cada letra é um quad do mesh apontando para uma célula de alfabeto.

Foram traduzidas reescrevendo as malhas (bloco 6I). Detalhes, lista completa e QA em [`GLYPH_SIGNS.md`](GLYPH_SIGNS.md). O atlas recebeu 13 células de acento/sinal em espaço que nenhum mesh do jogo amostra.

Os nomes próprios (TORRES TIRES, SMASH AUTO REPAIRS, BELASCO AUTO, TURBO BURGER, RIVERSIDE PLAZA, MOUNTAINVIEW) seguem `preserve_original`.
