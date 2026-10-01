# Fase 5 — `t_roadsigns` definitivo, R-19 10/40 e limites funcionais

**Data:** 30/09–01/10/2026 · **BeamNG.drive:** 0.39.4.0 · **Mapa:** West Coast USA · **Mod:** `traducao_ptbr_wcusa` 0.5.0.
Primeira produção definitiva do projeto.
- Plano e inventário: [`t_roadsigns_plan.md`](t_roadsigns_plan.md)
- `slotTraffic`: [`slotTraffic_update.md`](slotTraffic_update.md)
- Meshes: [`../../tests/reports/r19_mesh_validation.md`](../../tests/reports/r19_mesh_validation.md)
- Velocidade: [`../../tests/reports/phase5_speed_delta.md`](../../tests/reports/phase5_speed_delta.md)

## 1. Atlas `t_roadsigns` (PT-BR definitivo)

**Base:** os PNG originais, com SHA-256 conferido pelo script. A referência antiga (`source/reference_ptbr/t_roadsigns_b.color_ptbr.png`) foi usada só para consultar textos e agora está marcada como `superseded_by_phase5`.

**Master:** `working/layered/t_roadsigns/` (`layout.json` + `build_t_roadsigns.py` + `regions.json`). A composição é determinística, e todo pixel fora das caixas editadas é cópia do original.

### Regiões editadas: 44 (todas com evidência de UV de meshes instanciados)

| Tipo | Elementos | Mapas |
|---|---|---|
| Regulamentação | PARE (R-1) · R-2 sem legenda · R-3 sem texto · CONTRAMÃO | `_b.color` |
| Painéis | PROIBIDO ESTACIONAR · PROIBIDO ESTACIONAR / PONTO DE ÔNIBUS · AVANÇO DE SINAL VERMELHO / MULTA R$ 400 · NÃO BLOQUEIE O CRUZAMENTO · 2 h ESTACIONAMENTO 8h ÀS 21h SEG A SÁB … ZONA (C) (2 regiões) · 2 h ESTACIONAMENTO 7h ÀS 18h EXCETO DOMINGOS · CONVERSÃO À ESQUERDA SOMENTE COM SETA VERDE | `_b.color` |
| Perigo / fiscalização | PERIGO / ALTA TENSÃO (2 regiões) · FISCALIZAÇÃO ELETRÔNICA DE VELOCIDADE · FISCALIZAÇÃO ELETRÔNICA / AVANÇO DE SINAL | `_b.color` |
| Palavras recortadas pela máscara | SAÍDA · PRÓXIMA · LESTE · OESTE · NORTE · SUL · PEDÁGIO (×2) · ATENÇÃO · À FRENTE · OBRAS + NA VIA · VIA INTERDITADA (estêncil) · ATENÇÃO / EM OBRAS | `_b.color` + `_o.data` |
| Nomes de vias / destinos | Rua Brittlebush · Belasco · Estrada Mojave · Estrada Agave Trail · Calçadão · Autódromo · Praia Casilda · Monte Wallis · Rua do Canal · Docas · Centro Financeiro · Centro de Belasco · Ilha + Spearleaf | `_b.color` + `_o.data` |

**Contagem:**
- **Localizados:** 41 textos/elementos (40 entradas da matriz em `qa_passed`, mais o R-2 e o R-3, que viraram pictogramas sem texto).
- **Preservados (13):** 9 pictogramas, algarismos, Sierra Vista, San Amaro e Fog Hill.
- **Pendentes (registrados):**
  - glifos compartilhados que não podem mudar sem mesh/asset próprio: SPEED LIMIT e MPH das placas do `roadsigns.dae`, ONLY, CARPOOLS / 2 OR MORE PERSONS / PER VEHICLE, ¼ ½ ¾ / MILES;
  - regiões que nenhum mesh do West Coast usa (`not_used_wcusa`): ONE WAY, NO U TURN, TUNNEL, ROAD CLOSED (placa branca), SPEED & RED LIGHT, 6 nomes de rua.

### Validação da textura
| | `t_roadsigns_b.color` | `t_roadsigns_o.data` |
|---|---|---|
| PNG: resolução | 2048×1024 PASS | 2048×1024 PASS |
| PNG: alfa | inalterado (alpha mean diff 0), sem perda nem ruído | idem |
| PNG: pixels fora das regiões | **0** (188.445 px alterados, todos dentro de 44 regiões) | **0** (99.928 px dentro de 28 regiões) |
| DDS | DX10 **BC7_UNORM_SRGB**, sRGB, **12 mips**, 2.796.388 bytes, PASS | DX10 BC7_UNORM, linear, 12 mips, PASS |
| Família | `shape_changed: true`: a opacidade foi entregue (PASS) | |

**Heatmap:** tudo o que mudou está dentro dos elementos pretendidos (contagem por elemento em §8). A única variação ao redor das palavras apagadas é o grão reaplicado; não há "fantasma" legível, conferido com contraste forçado.

## 2. R-19 10 e 40 km/h (assets novos)

| Item | R-19 10 | R-19 40 |
|---|---|---|
| Master | `working/layered/r19/r19_10.svg` (+ `build_r19.py`) | `working/layered/r19/r19_40.svg` |
| Textura cor | `t_r19_10_b.color.dds`: 512×1024, BC7_UNORM_SRGB, 11 mips | `t_r19_40_b.color.dds`: idem |
| Opacidade | `t_r19_o.data.dds`: 512×1024, **BC4_UNORM** linear, 11 mips, disco (cobertura 0,564), compartilhada pelos dois valores e pelo verso | idem |
| Material | `roadsigns_ptbr_r19_10` | `roadsigns_ptbr_r19_40` |
| Verso | `roadsigns_ptbr_r19_back` (mapas do `metal_galvanized` + máscara do disco; o verso original é doubleSided e mostraria o retângulo pela frente) | idem |
| Mesh | `levels/.../objects/roadsigns_ptbr/sign_r19_10.dae` (+ `.cdae`): **mesh novo**, atribuído por `shapeName` às **7** placas reais de 5 mph | `levels/.../objects/sign_speed25.dae` (+ `.cdae`): **mesmo caminho virtual**, as **11** placas trocam sem editar TSStatic |
| Caminho dos assets | `levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/` | idem |

- **Escopo de nível:** o material é carregado com o mapa (`lua/ge/server/server.lua` lê todo `*materials.json` do diretório do nível). Não tem efeito em outros mapas e não colide com nada do jogo.
- **Expansão:** `build_r19.py 50 60 80 …` gera novos valores (só múltiplos de 10). Cada valor novo precisa de textura, material e mesh.
- **Material:** `alphaTest true`, `alphaRef 128`, `retroreflectivity 0.5`, `vertColor true` e `annotation TRAFFIC_SIGNS`, os mesmos parâmetros do `roadsigns` original. Fora do disco a cor é a da orla, então não há halo (verificado: 1.904 pixels de borda na cor da orla).
- **Mesh:** muda só material e UV; geometria, normais, cores de vértice, triângulos, nós e bounding box são idênticos (detalhe no relatório de meshes).

### Por que o 10 não substitui `sign_speed5.dae` no mesmo caminho
Das 37 instâncias de `sign_speed5.dae`, **30** (`port/portNumbersSigns`) são **decalques de malha que formam a placa cinza atrás dos números das baias** dos armazéns do porto. Substituir o mesh no mesmo caminho transformou essas placas em discos R-19 (efeito colateral capturado). Por isso o R-19 10 é um mesh novo, apontado só pelas 7 placas reais, e as placas das baias ficaram idênticas ao original.

### `.cdae` distribuído
Sem o `.cdae` no mod, o jogo compila o `.dae` para `current/temp/levels/…`, e esse cache **continua valendo com o mod desligado** (testado: placas com shape R-19 e materiais inexistentes). O mod distribui o `.cdae` compilado pelo próprio motor, mais novo que o `.dae`.
- Verificado numa sessão nova: carga com o mod desligado → original; mod ligado → R-19; mod desligado de novo → original. Nenhum arquivo foi gravado fora do mod.

## 3. Limites funcionais (PLACA = VIA = COMPORTAMENTO)

**Decisões por via:** `working/speed/speed_changes.json`, com motivo, placas e valor efetivo antigo lido do navgraph. **Placas → vias:** `tools/validation/config/sign_regulation.json`.

| Grupo | Vias | m/s | Como foi decidido |
|---|---:|---|---|
| 40: explícitas herdadas de 25 mph | **74** | 11,18 / 11,5 / 12 → **11,1111** | 65 ruas da malha residencial oeste (11,18); 8 vias de mão única da Ilha Spearleaf (12; a ilha tem placa de 25 mph na entrada); 1 conector (11,5). Todas são vias locais (MBST-I Tabela 1: 30/40) |
| 40: vias vistas por placa de 25 mph | **9** | automático 60/30 → **11,1111** | Via cuja direção é paralela à face da placa e cujo tráfego vê a face: ilha (`bd32eea0`); rua com 3 placas no pátio APM (`515427bb`); `69a8ea4e`; `f01c2753`; colina, ponto da Fase 2 (`794151eb` + conector `285c1e9e`); docas, as 3 faixas **depois** da saída da cobertura das cabines (`124bf149`, `fdd1cc5c`, `3dd0522d`) |
| 10: placas de 5 mph | **18** | automático 30/60/50 → **2,7778** | Docas: 4 faixas das cabines de entrada (placa de 5 mph na entrada da cabine) e 5 faixas do portão norte. Centro: 9 caminhos internos de estacionamento (`road_invisible`, dirigibilidade 0,2) a ≤ 15 m das 4 placas |
| **Total** | **101** vias + **7** TSStatic com `shapeName` → R-19 10 | | |

- **Nenhuma via pública foi reduzida a 10.** As únicas vias de dirigibilidade 1 com 10 km/h são as faixas das cabines dentro do portão das docas.
- **Exemplo de esquina** (−150/−144; 22): a via pública `69a8ea4e` ficou com 40 (placa de 25 mph) e o caminho do estacionamento `0176e4b4` ficou com 10 (placa de 5 mph). Conferido no navgraph.
- **Pátio do porto revertido:** a primeira versão punha 29 caminhos do pátio a 10 km/h, com base nos 30 "sinais de 5 mph" do grupo `portNumbersSigns`. Esses objetos são as placas das baias, não placas de velocidade, então a decisão foi desfeita e o pátio continua no automático (30 km/h).
- **Não alterados (§30):** 60/50/80/100/120, radares, zonas `city.sites.json`, garageToGarage, ADAS e Event 01.

### Arquivos funcionais sobrescritos pelo mod (gerados por `tools/production/speed_overrides.py`)
| Arquivo virtual | Mudança |
|---|---|
| `main/MissionGroup/AIWaypointsGroup/items.level.json` | 43 `speedLimit` |
| `main/MissionGroup/DecalRoads/items.level.json` | 38 `speedLimit` |
| `main/MissionGroup/island/island_ai_roads/items.level.json` | 8 `speedLimit` |
| `main/MissionGroup/island_shippingYard/dock_aiRoads/items.level.json` | 12 `speedLimit` |
| `main/MissionGroup/island_shippingYard/dock_entrance/items.level.json` | 1 `shapeName` (R-19 10) |
| `main/MissionGroup/island_shippingYard/dock_exit/items.level.json` | 2 `shapeName` |
| `main/MissionGroup/road_signs/items.level.json` | 4 `shapeName` |
| `slotTraffic.json` | 939 linhas `speedLimit` (243 faixas + 696 ligações) |

**Garantias e versionamento:**
- Cada linha editada é reaberta e comparada com o objeto original: só `speedLimit` ou o `shapeName` declarado podem mudar.
- `validate.py new` repete a verificação contra o zip do jogo.
- Esses arquivos são cópias dos dados do jogo e **não são versionados** (`.gitignore`); são regenerados de forma determinística a partir da instalação local. O diff estruturado fica em `tests/reports/phase5_speed_diff.json`.

## 4. Validações

| Verificação | Resultado |
|---|---|
| `validate.py texture` (cor e opacidade) | PASS / PASS: 0 px fora das regiões |
| `validate.py dds` (2 DDS do atlas) | PASS: BC7 sRGB / BC7 linear, 12 mips |
| `validate.py family t_roadsigns --source dir --dir export/dds/t_roadsigns --shape-changed true` | PASS |
| `validate.py new` (R-19 + overrides) | PASS 24/24 |
| `validate.py mod --installed` | PASS 48/48 (cópia instalada idêntica) |
| `validate.py selftest` / `regression` | PASS 75 / PASS 10 |
| `validate.py speeds --refresh` | 17 → 13 FAIL (todos fora do escopo); placas 10/40: unidade e valor = via PASS |
| Testes unitários | 44 OK |

## 5. QA no jogo (MCP)

Sessão reiniciada. Cada troca de estado do mod passou por outro mapa (`smallgrid`), porque recarregar o mesmo mapa mantém texturas, shapes e dados do nível em cache. As capturas estão em `tests/screenshots/phase5/`, todas em pares original × PT-BR com a mesma pose de câmera do catálogo `tests/qa_locations.json`.

| Grupo | Pontos | Dia | Noite |
|---|---|---|---|
| PARE | `roadsigns_chinatown_stop`, `roadsigns_hill_speed25`, `r19_40_dock_gate` | ✔ | ✔ (chinatown) |
| R-2 | `roadsigns_downtown_yield` | ✔ | — |
| R-3 + CONTRAMÃO | `roadsigns_do_not_enter_wrong_way` | ✔ | — |
| Painéis | `roadsigns_no_parking`, `roadsigns_bus_stop`, `roadsigns_red_light_violation`, `roadsigns_do_not_block`, `roadsigns_parking_2h`, `roadsigns_parking_2h_7am`, `roadsigns_left_turn` | ✔ | — |
| Perigo / fiscalização | `roadsigns_danger_high_voltage`, `roadsigns_speed_camera`, `roadsigns_red_light_camera` | ✔ | — |
| Obras | `roadsigns_construction_caution`, `roadsigns_road_closed`, `roadsigns_road_work_ahead` | ✔ | — |
| Pórticos | `roadsigns_gantry_mount_wallis`, `_next_exit`, `_mojave`, `_belasco_canal`, `_brittlebush`, `_downtown`, `_spearleaf`, `_autodromo`, `_oeste`, `roadsigns_toll_plaza`, `roadsigns_toll_north` | ✔ | — |
| R-19 40 | `r19_40_hill` (ponto da Fase 2), `r19_40_downtown`, `r19_40_dock_gate` | ✔ | ✔ (hill, downtown) |
| R-19 10 | `r19_10_downtown_parking` (estacionamento junto à via pública), `r19_10_dock_exit` (pátio das docas) | ✔ | ✔ (ambos) |

**Outras verificações:**
- **VFS:** todas as execuções sem problema.
- **Log:** nenhuma linha cita o mod. Os erros e avisos são idênticos com e sem mod (só muda o contador do próprio `screenshot`). O ruído vem do mod de veículo `hcity7`.
- **Render offline das composições do `roadsigns.dae`:** `tests/screenshots/phase5/t_roadsigns/composites_offline_render_original_vs_ptbr.jpg`.
- **Navgraph:** 13/13 PASS (`tests/reports/phase5_navgraph_check.json`).
- **IA em modo legal:** 40,4 km/h máximo na via de 40 e 6,8 km/h na faixa de 10 (`tests/reports/phase5_ai_test.json`).
- **Noite:** nesta sessão o `TimeOfDay` não ticka (janela em segundo plano, `speedFactor` 0). Os presets agora fixam o sol direto no `ScatterSky`: −20° à noite e 40,66° de dia.

## 6. Revisão humana (feita sobre as capturas)

Inspecionei visualmente todas as capturas antes/depois, de dia e de noite, e o render das composições.
- **Alinhamento:** octógono, triângulo, disco do R-3 e painéis sem deslocamento; o "E" de PARE está inteiro.
- **Legibilidade:** PARE, R-19 e pórticos legíveis à distância de QA, de dia e de noite.
- **Compressão:** sem blocos nem halo visíveis nas bordas do disco ou das letras recortadas.

Aproximações declaradas (`human_typography_review_required`):
- **Fonte:** Bahnschrift no lugar da Série D/E(M) e da gótica rodoviária.
- **Estêncil:** o ROAD CLOSED perdeu o estêncil.
- **Nomes longos espremidos pelo eixo de largura:** "Estrada Agave Trail", "Estrada Mojave", "PRÓXIMA".
- **Texto pequeno em placas pequenas:** "ESTACIONAMENTO" e "EXCETO VEÍCULOS COM PERMISSÃO" (o texto original já era pequeno).

**human_review: PASS**, com essas ressalvas tipográficas.

## 7. Limitações e pendências
1. **Glifos compartilhados:** placas SPEED LIMIT 30/40/70 mph e de advertência 15–30 MPH do `roadsigns.dae`, "DO NOT STOP / SPEED LIMIT 25" da cabine de pedágio, ONLY, CARPOOLS e "½ MILE" continuam em inglês/mph. Exigem meshes/assets próprios numa fase funcional.
2. **Velocidades fora do escopo:** radares, zonas, 60 km/h, ADAS e Event 01 (13 FAILs no validador).
3. **Granularidade:** `speedLimit` é por objeto `DecalRoad`. Nas faixas das cabines das docas, os ~13 m depois das placas de 25 mph ficam a 10 até a via seguinte.
4. **Slot traffic:** o editor oficial não vem no jogo; a edição é determinística e documentada.
5. **Overrides de nível sem versionamento:** são regenerados da instalação local (`speed_overrides.py`). Se o BeamNG atualizar o mapa, a regeneração falha de propósito quando os valores esperados não batem.
6. **Escopo:** o atlas `t_roadsigns` é global. Nenhum zip de outro mapa tem `.dae` com o material `roadsigns`; fora do West Coast, só os cavaletes `construction_sign_big_a/b/c` de `art_shapes.zip` o usam (ATENÇÃO / EM OBRAS e VIA INTERDITADA aparecem traduzidos onde quer que sejam colocados). R-19 e limites são do West Coast.

## 8. Pixels alterados por elemento (cor)
Fonte: `build_t_roadsigns.py` + diff do validador. Total: 188.445 px.

stop_r1 3.544 · yield_r2 2.181 · do_not_enter_r3 3.590 · wrong_way 6.235 · no_parking_any_time 6.766 · no_parking_bus_stop 7.266 · red_light_violation 6.399 · do_not_block 6.937 · parking_2h_green_box 1.056 · parking_2h_green_text 10.189 · parking_2h_7am_6pm 7.852 · left_turn 3.208 · danger_header 2.951 · danger_body 4.130 · speed_camera 7.548 · red_light_camera 17.470 · g_exit 1.639 · g_next 1.917 · g_east 1.584 · g_west 1.668 · g_north 1.676 · g_south 1.120 · g_toll 1.698 · g_caution 3.240 · g_toll_plaza 2.916 · g_ahead 2.873 · g_road 1.322 · g_work 1.296 · road_closed_stencil 4.703 · caution_under_construction 13.647 · 15 nomes 1.372–5.891.

## 9. Como reproduzir
```bash
python working/layered/t_roadsigns/build_t_roadsigns.py regions && python working/layered/t_roadsigns/build_t_roadsigns.py build
python working/layered/r19/build_r19.py
python tools/production/r19_mesh.py build source/originals/meshes/objects/sign_speed25.dae mod/traducao_ptbr_wcusa/levels/west_coast_usa/art/shapes/objects/sign_speed25.dae --value 40
python tools/production/r19_mesh.py build source/originals/meshes/objects/sign_speed5.dae mod/traducao_ptbr_wcusa/levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/sign_r19_10.dae --value 10
python tools/production/speed_overrides.py
python tools/production/install_mod.py
python tools/validation/validate.py all --refresh
```
A conversão para DDS segue os comandos do `README.md` de cada master. O `.cdae` é gerado pelo jogo na primeira carga (em `current/temp/…`), copiado para o mod e apagado de `temp`.
