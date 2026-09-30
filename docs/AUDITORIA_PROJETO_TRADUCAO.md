# Auditoria — Projeto de Tradução das Placas (West Coast USA → PT-BR)

**Data da auditoria:** 30/09/2026
**Pasta auditada:** `C:\Users\Desktop\Desktop\Texturas de placas`
**Versão do jogo:** BeamNG.drive 0.39.4.0 (Steam, `C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive`)

---

## 1. Resumo

| Item | Situação |
|---|---|
| Texturas originais extraídas (DDS + PNG) | **41** texturas em 9 categorias. Todas batem com os arquivos do jogo (tamanho, resolução e formato). |
| Texturas traduzidas (pasta `PT-BR`) | **11** de ~28 texturas de cor que têm texto (**~40%**), mais 1 máscara. |
| Qualidade do texto traduzido | **Boa**: termos corretos na maior parte e bom estilo visual. Faltam ajustes de ordem das palavras e de unidades (seção 5). |
| Integridade técnica dos PNG PT-BR | **Problemas**: as imagens foram regeneradas por inteiro, alguns canais alfa se perderam e faltam mapas complementares (seção 4). |
| Conversão para DDS | **Não começou**: nenhum DDS PT-BR existe. |
| Mod montado no jogo | **Não existe.** `mods/unpacked/` só tem os mods ADAS/reaction_test. |
| Teste em jogo | **Nunca foi feito.** |
| Guia `LEIA-ME_GUIA_DE_TRADUCAO.md` | Está útil, mas tem **caminhos incompletos e instruções imprecisas** (seção 6). |

**Conclusão:** o levantamento e a primeira leva de traduções estão bem encaminhados. Antes de traduzir mais, é preciso corrigir três problemas técnicos que fariam placas saírem erradas no jogo: as máscaras das marcações no asfalto, a perda de alfa e a regeneração da imagem inteira. Depois disso, vale montar um mod mínimo e testar no jogo.

---

## 2. Inventário e progresso por textura

Legenda: ✅ traduzida · ⚠️ traduzida com problema técnico · ❌ pendente · ➖ sem texto (máscara, emissivo ou logo), mas pode precisar de ajuste

### 01 - Placas de Trânsito
| Textura | Res. / formato original | Status |
|---|---|---|
| `t_roadsigns_b.color` | 2048×1024 BC7 sRGB | ✅ Tradução completa (PARE, DÊ A PREFERÊNCIA, MÃO ÚNICA, km/h…). Ver ordem dos nomes de rua (§5). |
| `t_roadsigns_o.data` | 2048×1024 BC7 | ➖ Máscara. Confirmar que ainda recorta bem a versão PT-BR. |
| `eca_roadsigns_d` | 1024×1024 DXT5 | ⚠️ Traduzida, mas **perdeu o alfa** (11% transparente → 0%). |
| `speed_sign` | 512×256 DXT1 | ❌ |
| `usa_roadsigns_turn_warning` | 512×512 DXT1 | ❌ (ver se tem texto) |
| `usa_roadsigns_text` | 1024×256 DXT5 | ❌ Atlas de fontes. Se mudar, alinhar com `_o.data` e `_e.color`. |
| `t_usa_roadsigns_text_o.data` / `_e.color` | BC4 / BC7 | ➖ Acompanham a anterior. |
| `ut_roadsigns_d` | 1024×1024 BC7 | ❌ |

### 02 - Comercial
| Textura | Status |
|---|---|
| `clutter_commercial_b.color` (2048² BC7) | ❌ É **a maior pendência** (Turbo Burger, Motel, Food Mart…). |
| `clutter_commercial_o.data` | ➖ Máscara. Acompanha a anterior. |
| `logos_dealership_garage_wca_d.color` | ❌ |
| `t_west_coast_garage_sign_b.color` | ❌ |
| `t_riverside_plaza_sign_LOD_b.color` | ❌ |

### 03 - Postos
| Textura | Status |
|---|---|
| `t_eca_genericsigns_b.color` | ⚠️ Traduzida, mas o layout mudou ("Pousada Firwood" ocupa outra área, o logo Nodeoline foi redesenhado). |
| `eca_genericsigns_emissive` | ❌ **Precisa ser refeita** para bater com o novo layout, senão o brilho noturno fica desalinhado. |
| `t_gasstation_tyrannos_b.color` | ❌ |

### 04 - Outdoors
| Textura | Status |
|---|---|
| `billboards_d` | ✅ (preço "4.99-" não foi convertido para R$) |
| `t_billboardsigns_dealers_b.color` | ⚠️ Traduzida, mas **perdeu o alfa** (13% transparente + 22% semitransparente → 0%). |
| `t_billboards_b.color` | ❌ É **outra textura**, diferente de `billboards_d`. |

### 05 - Ônibus
| Textura | Status |
|---|---|
| `busstop_d`, `t_bus_routes_wca_b.color`, `t_sign_busstop_b.color` | ❌ As três estão pendentes. |

### 06 - Estúdios
| Textura | Status |
|---|---|
| `t_movie_studio_signage_b.color` | ✅ Tradução muito boa. O alfa semitransparente foi perdido, mas o material não usa alfa, então o risco é baixo. |

### 07 - Indústria
| Textura | Status |
|---|---|
| `ind_industrial_signs_d.color` | ✅ Tradução muito boa ("LIMITE 20 km/h", "ALTURA MÁXIMA 4,42 m", EPIs…). |
| `t_spearleaf_refinery_logo_b.color` + `_o.data` | ✅ "REFINARIA SPEARLEAF". A máscara `_o.data` foi **corretamente atualizada**. O alfa do `_b` sumiu, mas o material usa `opacityMap`, então não afeta. |
| `t_steel_factory_brand_b.color` | ✅ (sem revisão visual detalhada) |
| `t_sealbrik_logo_b.color` | ➖ O arquivo `_ptbr` é **cópia idêntica** do original (mesmo MD5). É só um logo, então tudo bem, mas não conta como traduzido. |
| `t_industrial_signs_b.color` | ❌ |

### 08 - Corridas
| Textura | Status |
|---|---|
| `t_sponsors_b.color` | ✅ ("ENERGIA", "ESPECIALISTAS EM CORRIDAS"). O canto transparente (3%) virou branco. |
| `checkpoint_sign`, `t_sign_drift.color` | ❌ |
| `arrows_sign_d` | ➖ Só tem setas. |

### 09 - Asfalto
| Textura | Status |
|---|---|
| `t_decal_roadmarkings_b.color` | ⚠️ **Crítico.** Ver §4.1. |

---

## 3. Onde cada textura fica no jogo (verificado nos .zip do jogo)

Quase todas ficam em **assets globais**, não no mapa:

| Arquivo do jogo | Texturas |
|---|---|
| `content/assets/materials/signage.zip` | `signage/roadsigns/t_roadsigns_b.color`, `t_roadsigns_o.data`, `signage/signs_usa/eca_roadsigns_d`, `signage/ut_roadsigns/ut_roadsigns_d`, `signage/speed_sign_mat/speed_sign`, `signage/usa_roadsigns_turn_warn/…`, `signage/checkpoint_sign/…`, `signage/sign_arrows/…`, `signage/m_sign_busstop/…`, `signage/m_sign_drift/…` |
| `content/assets/materials/billboard_label.zip` | `billboard_label/eca_genericsigns/…`, `billboards/t_billboards_b.color`, `industrial_signs/…` (ambas), `m_bus_routes_wca/…`, `m_gasstation_tyrannos/…`, `m_logos_dealership_garage/…`, `m_movie_studio_signage/…`, `m_refinery_logo/…` (b + o), `m_sealbrick_logo/…`, `m_steel_factory_brand/…`, `m_west_coast_garage_sign/…`, `usa_roadsigns_text/…` (e + o) |
| `content/assets/materials/atlas.zip` | `atlas/busstop/busstop_d`, `atlas/m_billboardsigns_dealers/…`, `atlas/sponsorboards/t_sponsors_b.color`, `atlas/intro_text/usa_roadsigns_text` |
| `content/assets/materials/decal.zip` | `decal/marking/m_decal_roadmarkings_01/t_decal_roadmarkings_*` |
| `content/levels/west_coast_usa.zip` | `levels/west_coast_usa/art/shapes/objects/billboards_d`, `…/buildings/clutter_commercial_*`, `…/buildings/west_coast_LOD_materials/s_riverside_plaza_sign/…` |
| `content/art_shapes.zip` | Cópias de `clutter_commercial_*` e `eca_genericsigns_emissive` em `art/shapes/garage_and_dealership/Clutter/` |

**Observações:**
- Os `main.materials.json` do West Coast apontam para caminhos antigos, como `/levels/west_coast_usa/art/shapes/buildings/t_movie_studio_signage_b.color.png`. Esses arquivos **não existem** no zip do mapa, e o log não registra textura faltando. O motor resolve esses caminhos para o DDS em `assets/materials` (pelo que parece, pelo nome do arquivo). **Confirmar com um teste** antes de montar o mod inteiro (§8, passo 1).
- **Consequência importante:** trocar uma textura em `assets/materials/...` muda essa textura em **todos os mapas** que a usam. East Coast usa `eca_roadsigns_d`/`eca_genericsigns`, Utah usa `ut_roadsigns_d`, e vários mapas usam `t_roadsigns_b`. O mod traduz o jogo inteiro, não só o West Coast. Isso deve ser uma decisão consciente, e o guia precisa mencionar.
- `clutter_commercial_*` existe em dois lugares: no mapa e em `art/shapes/garage_and_dealership/Clutter/`. Para cobrir tudo, substituir os dois.

---

## 4. Problemas técnicos encontrados

### 4.1 🔴 Marcações no asfalto: só a cor foi traduzida
O material `roadmarkings1` do West Coast é translúcido, com alphaTest, e usa `t_decal_roadmarkings_o.data` como **opacidade**. Também existem mapas `_nm.normal`, `_ao.data`, `_r.data` e `_m.data`. A **máscara de opacidade e o normal têm o formato das letras em inglês**. Trocar só o `_b.color` faz "PARE" aparecer recortado pelo contorno de "STOP", e o mesmo vale para "ÔNIBUS"/"BUS", "MANTENHA"/"KEEP" e assim por diante. Em outras palavras, o texto fica ilegível.
➡️ É preciso extrair e refazer pelo menos `t_decal_roadmarkings_o.data` e `_nm.normal`, e de preferência também `_ao` e `_r`, seguindo o novo layout. Hoje nenhum deles está na pasta do projeto.

### 4.2 🔴 As imagens PT-BR foram regeneradas por inteiro
Comparei os pixels de cada original com o `_ptbr` correspondente:

| Textura | Pixels alterados | Alteração forte |
|---|---|---|
| ind_industrial_signs_d | 77,8% | 21,2% |
| t_movie_studio_signage_b | 65,2% | 27,6% |
| t_billboardsigns_dealers_b | 51,5% | 16,9% |
| billboards_d | 50,2% | 7,5% |
| t_eca_genericsigns_b | 50,0% | 31,6% |
| t_decal_roadmarkings_b | 49,9% | 14,0% |
| t_roadsigns_b | 45,4% | 17,5% |
| t_sponsors_b | 32,7% | 1,7% |
| eca_roadsigns_d | 31,6% | 8,1% |
| t_steel_factory_brand_b | 26,0% | 6,6% |
| t_spearleaf_refinery_logo_b | 25,9% | 15,5% |

Uma edição que só troca o texto altera poucos por cento. Mudanças de 30 a 78% indicam que a imagem inteira foi redesenhada, provavelmente por IA ou upscaler. Os PNG foram salvos em dois lotes, em 16/09 às 14:18 e às 14:49. Isso traz riscos:
- **Desalinhamento de UV:** o modelo 3D aponta para coordenadas exatas do atlas, então qualquer deslocamento corta ou mistura placas. Isso já dá para ver em `t_eca_genericsigns_b`, onde "Pousada Firwood" e o logo Nodeoline mudaram de posição e de proporção.
- Partes sem texto (sujeira, desgaste, cores) mudam sem necessidade e deixam de combinar com os mapas de normal, AO e rugosidade originais.
- Letras pequenas que a IA inventa, como avisos minúsculos e legendas, podem ter erros difíceis de notar.

➡️ **Recomendação:** refazer as traduções a partir do PNG original, editando **só as áreas de texto**, em camadas (PSD/XCF), sem redimensionar nem reposicionar nada. Os PT-BR atuais servem como **referência de texto e de layout**.

### 4.3 🟠 Perda de canal alfa
Canal alfa medido por amostragem:

| Textura | Original | PT-BR | Impacto |
|---|---|---|---|
| eca_roadsigns_d (DXT5) | 11% transparente, 5% semi | 0% / 2% | **Alto.** O fundo ao redor das placas vira preto. |
| t_billboardsigns_dealers_b | 13% / 22% | 0% / 1% | **Verificar.** Fontes e recortes perdem transparência. |
| t_spearleaf_refinery_logo_b | 85% / 5% | 0% / 2% | Baixo, porque o material usa `opacityMap`. |
| t_sponsors_b | 3% / 0% | 0% / 1% | Baixo (canto sem uso). |
| t_movie_studio_signage_b | 0% / 31% | 0% / 2% | Baixo, porque o material não usa alfa. |

Todos os PNG PT-BR também ganharam **ruído no alfa**, com valores mínimos de 193 a 221 onde o original era 255. Em materiais com `alphaTest` (por exemplo, `m_sealbrick_logo` com ref 150 e `m_refinery_logo` com ref 135), isso pode abrir furos se o valor cair abaixo da referência.
➡️ Ao exportar, copiar o canal alfa do original, ou da máscara refeita quando o layout mudou.

### 4.4 🟠 Mapas complementares que precisam acompanhar a cor
- `eca_genericsigns_emissive` precisa acompanhar o novo layout de `t_eca_genericsigns_b`.
- `t_roadsigns_o.data`: conferir se o recorte ainda bate com a versão PT-BR.
- `t_decal_roadmarkings_o/nm/ao/r`: ver §4.1.
- Quando traduzirem `usa_roadsigns_text` e `clutter_commercial_b`, ajustar também `_o.data` e `_e.color`.

### 4.5 🟡 Formato DDS de destino
O guia diz para usar "BC7 com mipmaps" em tudo, mas os originais usam vários formatos. É melhor manter o formato de cada um:

| Tipo | Formato original | Exportar como |
|---|---|---|
| `*_b.color`, `*_d.color` (novos) | DX10 BC7_UNORM_**SRGB** | BC7 sRGB + mipmaps |
| `*_o.data`, `ut_roadsigns_d` | BC7_UNORM (linear) ou **BC4** | Mesmo formato, **linear** (sem sRGB) |
| Legados `*_d.dds`, `speed_sign`, `checkpoint_sign` | DXT1 / DXT5 | DXT1 (sem alfa) / DXT5 (com alfa) |

Usar sempre a **mesma resolução** do original e gerar a cadeia completa de mipmaps. Os originais têm 7 a 12 níveis.

---

## 5. Revisão de conteúdo (tradução)

**Pontos fortes:** vocabulário de trânsito do CTB bem aplicado (PARE, DÊ A PREFERÊNCIA, MÃO ÚNICA, PROIBIDO ESTACIONAR, SEM SAÍDA, LOMBADA, PISTA ESTREITA, VIA INTERDITADA, FISCALIZAÇÃO ELETRÔNICA), sinalização de segurança industrial (EPIs, ALTA TENSÃO) e textos publicitários naturais ("MEGA OFERTA!", "SEMINOVOS DE QUALIDADE", "LEVE HOJE").

**Ajustes sugeridos:**
1. **Ordem dos nomes de rua** (`t_roadsigns_b`). Em português o tipo do logradouro vem antes do nome:
   - `Brittlebush Rua` → **Rua Brittlebush** · `Creosote Rua` → **Rua Creosote** · `Mariposa Rua` → **Rua Mariposa** · `Sorrel Rua` → **Rua Sorrel** · `Canal Rua` → **Rua do Canal**
   - `Rush Estrada` → **Estrada Rush** (ou Rua Rush) · `Mojave/Outcrop/Agave Trail Estrada` → **Estrada Mojave**, etc.
   - `Belasco Cidade` → **Cidade de Belasco** (ou só "Belasco") · `Motorsports Parque` → **Parque Motorsports** · `Casilda Praia` → **Praia Casilda** · `Spearleaf Ilha` → **Ilha Spearleaf** · `Dockyards Docas` → **Docas** (ficou redundante)
2. **Velocidade (mph → km/h).** Os números das placas continuam os valores em mph (25, 35, 50…), mas agora aparecem como km/h. Uma placa "50 km/h" corresponde a um limite real de 50 mph (≈ 80 km/h) no jogo, porque o tráfego e o `signals.json` continuam em mph. Isso **afeta diretamente as missões ADAS** instaladas, como `adasSpeedAlertTest/001-speedAlert50` e `adasEvent01/001-speedLimitRecognition`. Opções:
   (a) manter mph e traduzir só os textos;
   (b) converter os números (30/40/50/60/80/100 km/h) sabendo que a física e a IA continuam em mph;
   (c) converter e também ajustar os limites do mapa ou da missão.
   Escolher uma e aplicar em tudo.
3. **Preços e moeda:** "$400" e "$200" viraram "R$ 400" e "R$ 200", mas o "4.99-" do Turbo Burger ficou igual. Padronizar como "R$ 4,99" (com vírgula).
4. **Octanagem** (`t_eca_genericsigns_b`): "OCTANAGEM MÍNIMA (RON) 87/89/93". Os números 87/89/93 são do método americano (R+M)/2, não RON. No Brasil faz mais sentido "COMUM / ADITIVADA / PREMIUM" ou "IAD 87". Outra opção é tirar o "(RON)".
5. **Distintivo "BOMBEIROS FIRWOOD POLÍCIA"** com folha de bordo canadense mistura dois órgãos. Sugiro "CORPO DE BOMBEIROS" ou manter o original.
6. **Marcações no asfalto:** cada palavra é um recorte independente, montado na ordem de leitura americana. Por exemplo, "BUS ONLY" vira "ÔNIBUS SÓ" na pista. Sugestões: usar ONLY → **EXCLUSIVO** (fica "ÔNIBUS EXCLUSIVO") e conferir no `main.decals.json` quais combinações o mapa realmente usa com LEFT/TURN/NO.
7. Nomes de marcas fictícias (Nodeoline, Gavril, Hirochi, Spearleaf, Sealbrik, Texas Waste) ficaram em inglês, o que está correto.

---

## 6. Revisão do `LEIA-ME_GUIA_DE_TRADUCAO.md`

| # | Problema | Correção sugerida |
|---|---|---|
| 1 | Diz que o PNG é uma "versão de alta resolução", mas tem **a mesma resolução** do DDS. | Chamar de "versão editável". |
| 2 | Só dá 3 exemplos de caminho. Os demais não estão documentados. | Usar a tabela da §3 deste relatório. |
| 3 | Manda usar "BC7" para tudo. | Usar a tabela de formatos da §4.5. |
| 4 | "Ou como PNG (se for usar substituição de material)" é vago e não explica como. | Recomendar só DDS no mesmo caminho e nome. Substituir material é outra técnica e precisaria de um `materials.json` próprio. |
| 5 | Não diz que a troca vale para todos os mapas. | Adicionar aviso (§3). |
| 6 | Não menciona mapas complementares (máscara, emissivo, normal). | Adicionar regra: "texto mudou de lugar ou de forma → refazer `_o`, `_e` e `_nm`". |
| 7 | Não fala do `mod_info/<nome>/info.json` nem de empacotar em zip. | Incluir a estrutura mínima do mod (§8, passo 1). |
| 8 | Descrição de `t_eca_genericsigns_b` cita "Apex, Trilobite". O atlas real tem Nodeoline, Firwood Inn e o distintivo de bombeiros. | Corrigir a descrição. |
| 9 | Os arquivos `_ptbr.png` precisam ser renomeados de volta. | Deixar explícito que o DDS final **tem o nome exato do original**, sem `_ptbr`. |

---

## 7. Outros achados no ambiente

- **Mod `gniar_br_costa_oeste.zip`** (~4,8 GB, **ativo**) é outro mapa, "Gniar Mods - Brasil Long Trip 100km+", derivado do West Coast. Tem posto Ipiranga, Habib's, favela e placas próprias em `art/shapes/Placas/`, com texturas renomeadas (`*_gniar`). Não conflita diretamente com este projeto, mas:
  - pode servir de **referência visual** de estética BR;
  - o mod de tradução em `assets/materials` também vai mudar as placas desse mapa, onde ele usar os assets globais.
- **Mods ADAS** (`adas_event01_speed_limit`, `adas_speed_alert_test`, `adas_speed_alert_web`, `reaction_test`) rodam no West Coast e dependem de limites de velocidade. Ver §5.2.
- **Servidor MCP do BeamNG** está ativado (`http://127.0.0.1:29292/mcp`). Dá para usá-lo para automatizar testes: carregar o mapa, teleportar até cada placa e tirar screenshots antes e depois.
- **Sem controle de versão ou backup** na pasta do projeto, e **sem arquivos de camadas** (PSD/XCF). As traduções existem só como PNG achatado.

---

## 8. Próximos passos recomendados (em ordem)

1. **Teste de viabilidade (30 min).** Criar `mods/unpacked/traducao_ptbr_wcusa/` com uma textura só, por exemplo `assets/materials/signage/roadsigns/t_roadsigns_b.color.dds` (BC7 sRGB, 2048×1024, mipmaps), mais `mod_info/traducao_ptbr_wcusa/info.json`. Abrir o West Coast e confirmar que as placas mudaram. Isso valida o caminho de override (§3) antes de investir mais.
2. **Decidir a política de velocidade** (mph ou km/h, §5.2) e **de moeda**.
3. **Refazer as traduções existentes sobre o original**, editando só as áreas de texto, em camadas e preservando o alfa. Os `_ptbr.png` atuais servem de gabarito. Prioridade: `t_decal_roadmarkings` (com `_o` e `_nm`), `eca_roadsigns_d`, `t_eca_genericsigns_b` (com o emissivo), `t_billboardsigns_dealers_b`.
4. **Traduzir o que falta**, por impacto visual: `clutter_commercial_b` → `t_billboards_b` → ônibus (3) → `speed_sign`/`ut_roadsigns_d`/`usa_roadsigns_*` → `t_industrial_signs_b` → `logos_dealership`, `west_coast_garage`, `riverside`, `tyrannos` → `checkpoint`/`drift`.
5. **Criar um script de verificação** para cada textura, que confira: mesma resolução, formato DDS igual ao original, contagem de mipmaps, % de pixels alterados fora das áreas de texto (deve ser ≈0) e alfa preservado.
6. **Montar o mod completo**, testar no West Coast (dia e noite, por causa dos emissivos), em East Coast e Utah (efeito colateral) e com as missões ADAS.
7. **Atualizar o LEIA-ME** com as correções da §6 e **versionar a pasta** (git ou backups datados).
