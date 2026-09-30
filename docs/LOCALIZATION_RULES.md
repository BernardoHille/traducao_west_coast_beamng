# Regras de localização PT-BR — West Coast USA

**Status:** fonte de verdade a partir da Fase 3 (30/09/2026). **Nenhuma textura é aprovada se contradizer este documento.**
Dados estruturados: [`localization/LOCALIZATION_MASTER.csv`](localization/LOCALIZATION_MASTER.csv) (308 entradas). Glossário: [`localization/GLOSSARY_PTBR.md`](localization/GLOSSARY_PTBR.md).

## 0. Princípio

> **West Coast USA localizado para jogadores brasileiros** — não é uma conversão total para o Brasil.
> Belasco continua sendo Belasco; marcas fictícias continuam as mesmas; o que muda é a **linguagem visual e as convenções** (idioma, unidades, moeda, sinalização).

Hierarquia de decisão (em ordem):
1. **Preservar o significado funcional** do elemento original.
2. **Português brasileiro natural** — nunca palavra por palavra.
3. **Convenção brasileira** quando houver equivalente claro (MBST/CONTRAN).
4. **Nomes próprios fictícios preservados** (marcas, empresas, lugares).
5. **Unidades e convenções adaptadas** (km/h, m, °C, R$, vírgula decimal, 24 h).

Coexistem naturalmente: nomes americanos/fictícios + português + km/h + R$ + sinalização brasileira.

## 1. Fontes normativas

| Ref. | Documento | Onde |
|---|---|---|
| MBST-I | Manual Brasileiro de Sinalização de Trânsito, **Vol. I — Sinalização Vertical de Regulamentação** (edição atual publicada pela SENATRAN) | [PDF oficial](https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/docs/copy_of___01___MBST_Vol._I___Sin._Vert._Regulamentacao_F.pdf) |
| MBST-I/2005 | Mesmo volume, edição aprovada pela **Resolução CONTRAN nº 180/2005** (usada para trechos não localizados na edição atual) | [PDF](https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/educacao/publicacoes/manual_vol_i_2.pdf) |
| MBST-IV | MBST **Vol. IV — Sinalização Horizontal**, CONTRAN 2022 | [PDF oficial](https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/docs/copy_of___04___MBST_Vol._IV___Sinalizacao_Horizontal.pdf) |
| Índice | Página dos manuais SENATRAN (Vol. I–IX) | [gov.br](https://www.gov.br/transportes/pt-br/assuntos/transito/senatran/manuais-brasileiros-de-sinalizacao-de-transito) |

Citações usadas neste projeto (página do **arquivo PDF**):

| Regra | Fonte |
|---|---|
| Velocidade regulamentada "deve sempre ter valores múltiplos de 10" | MBST-I p.35 · MBST-I/2005 p.46 |
| Tabela 1 — vias urbanas: trânsito rápido 80/90; arterial 60/70 (2+ faixas) ou 50/60 (1 faixa); coletora 40/50; local 30/40 km/h | MBST-I p.36 · MBST-I/2005 p.47 |
| Informação complementar: placa retangular, mesmas cores do sinal; **não se admite** para R-1 e R-2 | MBST-I p.13 (§4.3.1) |
| R-1: fundo vermelho, orla interna branca, orla externa vermelha, **letras brancas**. R-2: **fundo branco, orla vermelha** (sem letras) | MBST-I p.15 · diagramação R-2 p.154 |
| R-2 pode ser complementado pela **inscrição no pavimento** "DÊ A PREFERÊNCIA" | MBST-I/2005 p.45 |
| R-19: circular, **fundo branco, orla vermelha, algarismos e letras pretos, Série D ou E(M), centralizados** | MBST-I/2005 p.193 (diagramação) |
| R-15 Altura máxima: mesmas cores; letras e algarismos pretos centralizados | MBST-I p.178 |
| Legendas no pavimento: brancas; alturas por velocidade | MBST-IV p.118 (§8.3) |
| Legenda "PARE" ≥ 1,60 m antes da linha de retenção, reforço do R-1 | MBST-IV p.123 |

## 2. Velocidade (decisão definitiva)

**Unidade: km/h. Placa = limite funcional = ADAS = missão = interpretação do jogador.**
Detalhes: [`inventory/speed_limits.md`](inventory/speed_limits.md) e [`inventory/speed_dependencies.md`](inventory/speed_dependencies.md).

1. Converter `mph × 1,609344`, escolher o **múltiplo de 10** mais coerente (MBST-I p.35).
2. Preservar hierarquia viária (MBST-I p.36): quando dois limites distintos colapsarem no mesmo valor dentro do mesmo contexto, o maior sobe para o múltiplo seguinte.
3. Tabela padrão: **5→10 · 15→20 · 25→40 · 30→50 · 35→60 · 40→60 (70 se coexistir com 35) · 45→70 · 50→80 · 55→90 · 60→100 · 65→100 (110 se coexistir com 60) · 70→110 mph→km/h.**
4. Valor funcional é armazenado na unidade do sistema (m/s no mapa: `km/h ÷ 3,6`, com 4 casas: 10→2,7778; 20→5,5556; 40→11,1111; 50→13,8889; 60→16,6667; 80→22,2222). Sem conversões encadeadas a partir de mph.
5. **Nunca** gerar 56, 72 etc.
6. Implementação visual (R-19) **não** é troca de textura: ver §3.2.

## 3. Sinalização de trânsito regulamentar

### 3.1 PARE (R-1)
`STOP` → **`PARE`**, letras brancas em caixa alta sobre o octógono vermelho existente (MBST-I p.15).
Reconstruir **a partir do original**, sem mover o octógono (UV `t_roadsigns_b` 1164–1290 × 231–358 px, compartilhada por `sign_stop.dae` e `roadsigns.dae`). A referência antiga só serve para confirmar a palavra.

### 3.2 Limite de velocidade (R-19)
Especificação visual: placa **circular**, fundo branco, orla vermelha, número preto centralizado (Série D/E(M)) e **"km/h"** abaixo do número (MBST-I/2005 p.193). Sem "LIMITE DE VELOCIDADE".
Restrição técnica descoberta na Fase 3: `sign_speed25.dae` e `sign_speed5.dae` montam a placa por UV com **painel branco + tile "SPEED LIMIT" + glifos "2"/"5" da linha de algarismos compartilhada** (usada também por docas, pedágios e túnel). Consequências obrigatórias para a implementação:
- **não** alterar a linha de algarismos do atlas;
- criar **material + textura próprios de R-19** (ex.: `roadsigns_ptbr_r19`) e **meshes substitutos** (`levels/west_coast_usa/art/shapes/objects/sign_speed25.dae` → R-19 40; `sign_speed5.dae` → R-19 10), com o disco recortado por opacidade (cantos transparentes) na placa retangular existente;
- limite funcional das vias adjacentes alterado no mesmo pacote (§2, `speed_dependencies.md`).

### 3.3 Dê a preferência (R-2)
Decisão: **triângulo invertido branco com orla vermelha, sem legenda** — é o R-2 brasileiro (MBST-I p.15/p.154); informação complementar não é admitida (p.13). A palavra "YIELD" é removida e o interior fica branco.
"DÊ A PREFERÊNCIA" é o **nome** do sinal e pode aparecer como **inscrição no pavimento** (MBST-I/2005 p.45), não dentro da placa. A referência antiga que espremeu "DÊ A PREFERÊNCIA" no triângulo **não** é seguida.

### 3.4 Outras regulamentares
| Original | PT-BR | Base |
|---|---|---|
| DO NOT ENTER | R-3 **sem texto** (círculo vermelho + barra branca) | MBST-I (R-3) |
| NO PARKING ANY TIME | PROIBIDO ESTACIONAR (+ seta) — "ANY TIME" omitido | R-6a; sem complemento = permanente |
| NO PARKING BUS STOP | PROIBIDO ESTACIONAR — PONTO DE ÔNIBUS | R-6a + complemento |
| 2 HOUR PARKING … | ESTACIONAMENTO 2 h · horário 24 h · dias abreviados (SEG A SÁB) | R-6b + complemento (§4.3.1) |
| ONE WAY | **MÃO ÚNICA** (formato retangular com seta mantido) | R-24a é circular; geometria atual é retangular |
| WEIGHT LIMIT 10 TONS | PESO MÁXIMO **9 t** | R-14; 10 short tons = 9,07 t (arredonda para baixo) |
| MAX HEIGHT / HEADROOM | ALTURA MÁXIMA **4,42 m** | R-15; vírgula decimal |

Advertências (amarelas) seguem glossário; placas de fiscalização por câmera: **"FISCALIZAÇÃO ELETRÔNICA …"** (ver glossário).

## 4. Nomes de vias e lugares
- **Tipo do logradouro antes do nome:** `St` → **Rua**, `Rd` → **Estrada** (fora do centro) ou **Rua** (urbana — decidir por contexto; marcar `needs_context` na dúvida), `Blvd/Boulevard` → **Avenida**, `Beach` → **Praia**, `Island` → **Ilha**, `Mount` → **Monte**, `Park` (área verde) → **Parque**, `Pier` → **Píer**, `Bridge` → **Ponte**, `Lookout/Viewpoint` → **Mirante**.
- O **nome próprio fica intacto**: `Brittlebush St` → `Rua Brittlebush` (errado: `Brittlebush Rua`).
- Substantivos comuns dentro do nome são traduzidos: `Canal St` → `Rua do Canal`; `Church St` → `Rua da Igreja`; `Promenade` → `Calçadão`; `Dockyards` → `Docas`; `Downtown Belasco` → `Centro de Belasco`; `Financial District` → `Centro Financeiro`.
- `Belasco City` → **`Belasco`** em placas de destino; `Cidade de Belasco` só em contexto institucional com espaço.
- `Motorsports Park` (destino genérico) → **Autódromo**; nome completo de marca (`Burnside International Motorsports Park`) preservado.
- Nomes sem tipo de logradouro (`Fog Hill`, `Sierra Vista`, `San Amaro`, `Little China`) ficam como estão.

## 5. Unidades (sistema métrico)
| Grandeza | Regra | Exemplo |
|---|---|---|
| Velocidade | km/h (§2) | 25 mph → 40 km/h |
| Distância em placa | mi → km, arredondado para sinalização (1 casa) | 1/4 mi → 0,4 km; 1/2 → 0,8 km; 3/4 → 1,2 km |
| Altura/largura | ft/in → m com 2 casas | 14 ft 6 in → 4,42 m |
| Peso | short ton → t (para baixo em limite) | 10 tons → 9 t |
| Temperatura | °F → °C: `(°F − 32) × 5/9`, precisão do contexto | nenhuma ocorrência nas texturas inventariadas |
| Combustível (interface) | galão US → litro | `info.json` `localUnits` (dependência funcional, não textura) |

Não inventar unidade onde não existe.
**Distâncias compostas por UV** (frações + tile `MILES` no pórtico `roadsigns.dae`) só podem ser convertidas com recomposição da placa — status `needs_implementation`.

## 6. Números, data e hora
- Decimal **vírgula**, milhar **ponto**: `4.42 m` → `4,42 m`; `$1,499` → `R$ 1.499`.
- Horário público em **24 h**: `8AM-5PM` → `8h–17h`; `3:30 PM` → `15:30` (ou `15h30` em placa). Dias: `SEG`, `TER`, `QUA`, `QUI`, `SEX`, `SÁB`, `DOM`; intervalos com "A" ou travessão (`SEG A SÁB`, `SEG–SEX`).
- Datas visíveis `MM/DD/YYYY` → `DD/MM/YYYY`. Datas/timestamps técnicos não são alterados.
- `9/10` (nota de avaliação) é preservado.

## 7. Moeda (decisão definitiva)
- **Real brasileiro**, formato `R$ 4,99` — símbolo, espaço, vírgula decimal, ponto de milhar.
- **Sem conversão cambial**: `$400` → `R$ 400`; `$200` → `R$ 200`; `4.99-` → `R$ 4,99`. Mantém escala da arte e o mod atemporal.
- Limitação: preços montados por **glifos** (totens de posto, letreiros com `$` do atlas `clutter_commercial`) não têm "R", vírgula nem espaço prontos → recomposição (`needs_implementation`/`needs_context`).

## 8. Combustível
- Marcas preservadas: **Nodeoline, Apex, Trilobite, Tyrannos**.
- Octanagem: os valores `87/89/93` são **AKI (R+M)/2**, não RON — **nunca rotular como RON**. Padrão: **COMUM (87) · ADITIVADA (89) · PREMIUM (93)**. Se o layout exigir número, usar `(R+M)/2 87` sem converter para RON.
- Mensagens de bomba e segurança em PT-BR técnico (glossário).
- Preços: `R$` + vírgula (§7); não representar preço real de nenhum ano.
- **Arquivo a localizar no West Coast:** `levels/east_coast_usa/art/shapes/buildings/eca_genericsigns_d.dds` (+ `eca_genericsigns_emissive.dds`) — é o que o material `eca_genericsigns` carrega (achado da Fase 3). `t_eca_genericsigns_b.color` tem o mesmo conteúdo, mas não foi encontrado em uso no West Coast.

## 9. Comércio e publicidade
- Linguagem publicitária brasileira natural; variar conforme contexto: `SALE` → LIQUIDAÇÃO / OFERTA / PROMOÇÃO; `BIG SALE` → MEGA OFERTA / SUPER PROMOÇÃO; `STORE CLOSING` → QUEIMA TOTAL; `% OFF` pode ficar (uso corrente) ou `% DE DESCONTO`.
- **Texto integrado a logotipo é preservado** (`BLASTR ENERGY`, `CLOCKWISE RACING EXPERTS`, `BELASCO AUTO GARAGE`); slogans e textos auxiliares fora do logo são traduzidos.
- Nomes de produtos/jogos/veículos de imprensa fictícios preservados (`Feline Racerz`, `SeriousGamingJournalism`, `GameMaster720`, `Friendbook`).
- Universo americano mantido: `AMERICA'S TRUSTED TIRE BRAND` → "A MARCA DE PNEUS DE CONFIANÇA DOS EUA" (nunca "do Brasil").
- Letreiros de fachada **compostos por glifos** (MOTEL, FOOD MART…) exigem mesh/textura dedicada.

## 10. Hospedagem (motel/hotel)
`MOTEL`/`Motel` de beira de estrada → **POUSADA** (ou HOTEL conforme a identidade visual); `INN` → **POUSADA**. Ver [`localization/cultural_adaptations.md`](localization/cultural_adaptations.md).

## 11. Transporte público
- `BUS STOP` → **PONTO DE ÔNIBUS** (placa); `ÔNIBUS` quando o espaço exigir.
- Mapa de linhas: `TRANSPORT NETWORK` → REDE DE TRANSPORTE; `BUS LINES` → LINHAS DE ÔNIBUS; nomes de paradas seguem §4.
- Atlas (`busstop_d`), placa de ponto (`t_sign_busstop`) e mapas (`t_bus_routes_wca`, `t_bus_routes_utah`) são tratados separadamente — os dois primeiros só têm pictogramas.

## 12. Marcações no asfalto (`t_decal_roadmarkings`)
- Cada decal usa **uma palavra** (grade 4×4, `rectIdx`); frases são montadas pelo mapa. Combinações reais medidas no `main.decals.json`: **KEEP CLEAR** (44 pares, mesma linha), **NO EXIT** (2), **BUS ONLY** (2), **BUS STOP** (2), **EXIT ONLY** (docas). `LEFT` e `TURN` **não são usados** no West Coast.
- Mapeamento: STOP → **PARE** (MBST-IV p.123) · BUS → **ÔNIBUS** · KEEP → **NÃO** · CLEAR → **BLOQUEIE** (= "NÃO BLOQUEIE") · NO → **SEM** · EXIT → **SAÍDA** (= "SEM SAÍDA").
- `ONLY` (`needs_context`): um slot não concorda em gênero para "ônibus exclusivo"/"saída exclusiva". Proposta: BUS ONLY → só "ÔNIBUS" (legenda brasileira de faixa exclusiva); EXIT ONLY → "SÓ SAÍDA" usando os slots livres 10/11 via override de `main.decals.json` (west_coast_only).
- Toda palavra nova exige refazer `_o.data`, `_nm.normal` e `_ao.data` (a máscara define o contorno das letras).
- Não recriar a malha viária brasileira; só as marcações deste atlas.

## 13. Indústria e segurança
- Marcas preservadas (Texas Waste, Sealbrik, Spearleaf, Hot Rolled Inc.); descritores traduzidos (`SPEARLEAF REFINERY` → REFINARIA SPEARLEAF; `STEEL MANUFACTURING` → FABRICAÇÃO DE AÇO).
- EPIs/avisos em português técnico: USE CAPACETE, USE PROTETOR AURICULAR, EPI OBRIGATÓRIO, ALTA TENSÃO, EMPILHADEIRAS EM OPERAÇÃO. `SDS` → **FDS** (Ficha com Dados de Segurança, antiga FISPQ).
- Não inventar requisito inexistente no original.

## 14. Entidades públicas
- Órgãos fictícios **não** viram instituições brasileiras reais (`Department of Transport` → "Departamento de Transportes").
- Distintivo `FIRE · FIRWOOD · DEPARTMENT · POLICE`: recomendação **preservar** como emblema próprio; tradução só por decisão do dono (`CORPO DE BOMBEIROS DE FIRWOOD`, sem "POLICE"). Proibido: `BOMBEIROS FIRWOOD POLÍCIA`.

## 15. Tipografia
- Acentuação completa (ÔNIBUS, MÃO ÚNICA, TRÂNSITO, ELETRÔNICA, MÁXIMA, SAÍDA…). Remover acento só com limitação técnica **comprovada** — e registrar.
- Limitações comprovadas: atlas de fonte `usa_roadsigns_text`, alfabetos de `clutter_commercial`, `eca_genericsigns` e `t_billboardsigns_dealers` **não têm glifos acentuados** → textos compostos por glifo precisam de glifo novo ou arte dedicada.
- Sinalização em **caixa alta** (`PARE`, nunca `Pare`); publicidade mantém a tipografia do original.

## 16. Telefones
Números fictícios de publicidade (`444-999-2222`) são **preservados**. Nunca introduzir telefone real brasileiro ou de terceiros.

## 17. Escopo dos assets
- **Assets globais permanecem globais** (override no caminho original; efeito em outros mapas é aceito e testado no QA). Coluna `scope` da matriz: `global` / `west_coast_only` / `global (arquivo no caminho do East Coast)`.
- Assets em `levels/west_coast_usa/...` são naturalmente `west_coast_only`.
- Coluna `wcusa_usage`: `confirmed` (objeto do West Coast usa o material), `likely`, `not_found` (atlas de outro mapa — prioridade baixa, mas a regra vale).

## 18. Status da matriz
`inventory` · `needs_context` · `rule_defined` · `needs_implementation` (regra definida, mas exige mesh/JSON/sistema além da textura) · `approved_rule` (decisão explícita do dono) · `preserve_original`. Nada é `implemented` nesta fase.

## 19. Achados técnicos da Fase 3 que afetam a implementação
1. Placas de velocidade compostas por glifos compartilhados → R-19 exige material/mesh próprios (§3.2).
2. Postos no West Coast usam `eca_genericsigns_d.dds` do caminho do **East Coast** (§8).
3. Outdoors do West Coast usam `t_billboards_b.color` (a referência antiga foi feita sobre `billboards_d`).
4. Abrigos de ônibus usam também `t_bus_routes_utah_d.color` (fora do inventário da Fase 0).
5. Letreiros de fachada são montados por glifos do `clutter_commercial` (sem acentos).
6. Vias do jogo base já usam limites automáticos métricos (30/50/60/80/100/120 km/h); as placas visíveis (5 e 25 mph) **não** coincidem hoje com o limite funcional ao lado (30 e 60 km/h) — inconsistência do jogo original a ser resolvida junto.
