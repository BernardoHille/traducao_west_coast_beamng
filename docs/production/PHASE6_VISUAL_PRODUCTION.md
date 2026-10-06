# Fase 6 — Produção visual das famílias restantes

**Período:** 05–06/10/2026 · **Mapa:** West Coast USA (BeamNG.drive 0.39.4.0).

**Situação:** todas as famílias visuais usadas pelo West Coast foram produzidas, validadas e conferidas no jogo, inclusive as palavras montadas por glifos no mesh (bloco 6I). Fica para a Fase 7 apenas o que é **limite de velocidade** (tiles MPH / SPEED LIMIT e a placa da cabine de pedágio), conforme a regra da fase.

## Pipeline aplicado a cada família
1. **Hash** do original: manifesto SHA-256.
2. **Regiões** com evidência UV dos meshes instanciados: `compose.py regions`, `dae_uv.py`, `asset_usage.py`.
3. **Master** por elemento: `working/layered/<família>/layout.json`.
4. **PNG.**
5. **Validação:** regiões, alfa e diferença fora das regiões.
6. **Mapas auxiliares**, quando a letra está neles (opacidade, normal, AO, rugosidade).
7. **Família.**
8. **DDS** no formato e com os mips do original: `export_family.py`.
9. **Mod.**
10. **QA MCP** com par original × PT-BR, de dia e, nos pontos marcados, à noite: `qa_cycle.py`.
11. **Revisão humana** nas folhas de contato.
12. **Matriz** e **commit.**

Regras mantidas o tempo todo:
- sem IA generativa (o preenchimento é feito por difusão a partir dos vizinhos);
- `source/reference_ptbr` usado só como referência;
- regiões só com evidência, nunca ampliadas para passar no validador;
- nada de radares, ADAS, zonas ou velocidades (Fase 7).

## Resultado por bloco
| Bloco | Família(s) | Resultado | Documento |
|---|---|---|---|
| 6A | `t_decal_roadmarkings` (2 cópias, 8 mapas) | PARE, NÃO BLOQUEIE, SAÍDA, SEM SAÍDA, ÔNIBUS, SÓ SAÍDA. Override de `main.decals.json` (9 instâncias removidas, 6 `rectIdx`) | [ROADMARKINGS](phase6/ROADMARKINGS.md) |
| 6B | `eca_genericsigns` (PBR de art_shapes) | Placas de posto: PERIGO, DESLIGUE O MOTOR, octanagem (R+M)/2, PROIBIDO ESTACIONAR… | [GENERICSIGNS](phase6/GENERICSIGNS.md) |
| 6C | `t_billboards`; `t_billboardsigns_dealers` | 14 outdoors com QA. Os painéis de concessionária não são amostrados no West Coast (só glifos MAP/INFO); os textos equivalentes foram produzidos no 6F | [BILLBOARDS_DEALERS](phase6/BILLBOARDS_DEALERS.md) |
| 6D | `t_movie_studio_signage`, `ind_industrial_signs` (2 cópias), `t_spearleaf_refinery_logo` (cor + opacidade), `t_steel_factory_brand` (cor + nm/ao/r) | 17 placas do estúdio, 9 grupos industriais, REFINARIA, FABRICAÇÃO DE AÇO | [STUDIO_INDUSTRY_SPONSORS](phase6/STUDIO_INDUSTRY_SPONSORS.md) |
| 6E | `t_bus_routes_wca` (cor + normal) | Mapa de linhas: título, legenda e 23 paradas. MAP → MAPA no abrigo (malha, 6I) | [BUS_TRANSPORT](phase6/BUS_TRANSPORT.md) |
| 6F | `clutter_commercial` (cor + opacidade) | 85 elementos: néons, cartazes, galpões, concessionárias, oficinas, limão, ENTRADA PROIBIDA, GUARDA-VOLUMES. Letreiros de glifos pendentes (mesh) | [COMMERCIAL](phase6/COMMERCIAL.md) |
| 6G | placas globais restantes | Nenhuma usada no West Coast (0 instâncias); DRIFT preservado | [GLOBAL_SIGNS](phase6/GLOBAL_SIGNS.md) |
| 6H | auditoria | 311 linhas classificadas; 2 traduções esquecidas achadas e produzidas; 12 linhas pendentes de mesh, resolvidas no 6I | [COVERAGE_AUDIT](phase6/COVERAGE_AUDIT.md) |
| 6I | letreiros montados por glifos (25 meshes) | Fachadas, totens, cartazes de preço (R$), MAPA do abrigo, túnel do autódromo (ALTURA MÁXIMA 3,9 m), arrancada, pórticos (SOMENTE, FAIXA EXCLUSIVA, 400 m / 800 m / 1,2 km); 13 acentos + 10 tiles novos; `.cdae` do jogo distribuído | [GLYPH_SIGNS](phase6/GLYPH_SIGNS.md) |

## Números
- **DDS no mod:** 28, todos no formato e com os mips do original (BC7 sRGB para cor, BC4 para opacidade/AO/rugosidade, BC5 para normal).
  - 23 novos na Fase 6, somados aos 5 da Fase 5.
  - O `t_roadsigns` foi re-exportado com os 10 tiles novos; os 44 elementos da Fase 5 ficaram idênticos.
- **Malhas no mod:** 27 `.dae` + 27 `.cdae` (25 de letreiros de glifos + 2 da Fase 5).
- **Pontos de QA da Fase 6** em `tests/qa_locations.json`: 170 (84 de textura + 86 de letreiros de glifos).
- **Capturas JPEG** em `tests/screenshots/phase6/`: 365 (pares original/PT-BR, 22 à noite).
- **Runs** em `tests/reports/phase6/runs/`: 92, com 0 problemas de VFS.
- **Matriz (320 linhas):**

| Classe | Linhas |
|---|---|
| produzido + QA | 148 |
| produzido sem ponto próprio | 11 |
| não usado no West Coast | 101 |
| `preserve_original` | 45 |
| Fase 7 | 15 |
| pendente | 0 |
| `needs_context` | 0 |

## Ferramentas criadas ou ampliadas
- **`tools/production/compose.py`:** compositor genérico de painéis e glifos. Inclui:
  - legenda por cor/neon/auto;
  - apagamento girado (`erase_rot`) e em anel (`erase_ring`);
  - texto girado e em arco;
  - regras auxiliares `mask_from_text`, `cutout`, `flatten_hole`, `edge_profile(_normal)` e `gradient_normal`.
- **`tools/production/dae_uv.py`** e **`asset_usage.py`:** evidência UV e uso real das texturas no nível.
- **`tools/production/extract_originals.py`, `export_family.py`, `decal_overrides.py`, `matrix_update.py`.**
- **`tools/production/glyph_signs.py`, `glyph_rewrite.py`, `glyph_sync.py`:** leitura, render e reescrita das palavras montadas por glifos no mesh; envio de `.dae` + `.cdae`.
- **`tools/beamng/catalog_add.py`:** pontos de QA por UV/decal com pose calculada no jogo.
- **`tools/beamng/qa_cycle.py`, `qa_sheet.py`, `frame_check.py`, `shots_to_jpeg.py`.**
- **Validador:**
  - variantes de originais por pasta;
  - famílias com múltiplos caminhos;
  - verificação de `main.decals.json`;
  - expectativas de regressão atualizadas para as famílias que ganharam regiões autorizadas.

## Validação final (06/10/2026)
| Verificação | Resultado |
|---|---|
| `validate.py selftest` | PASS (121) |
| `validate.py regression` | PASS (10/10): as imagens PT-BR antigas continuam reprovadas |
| `validate.py mod --installed` | PASS (217) |
| `validate.py new` | PASS (75), incluindo os 25 meshes de glifos (estrutura igual ao original exceto as letras; `.cdae` atual) |
| Testes unitários | 44 OK |
| `validate.py speeds` | FAIL 13, **idêntico ao fim da Fase 5** (radares/ADAS/zonas, escopo da Fase 7) |

## Fora do escopo da Fase 6 (Fase 7)
- Tiles MPH e SPEED LIMIT do `roadsigns.dae` (placas 15–30 MPH, SPEED LIMIT 30/40/70).
- Placa DO NOT STOP / SPEED LIMIT 25 da cabine de pedágio.

Trocar a unidade sem mudar o valor e o limite funcional criaria "25 km/h" falso. A regra da Fase 6 proíbe mexer em velocidades.

## Revisões humanas registradas
- Tipografia substituta (Bahnschrift/Arial/Impact/Georgia).
- Cabide do néon LAVANDERIA com falhas.
- Brilho dos néons novos um pouco menor.
- Face da lista de serviços da oficina não localizada no jogo.
- Letreiros de glifos: acentos desenhados (não existiam nos alfabetos) e palavras longas condensadas até 52 % (ESCAPAMENTO, "Consertamos todas as marcas!"). WIN LIGHT → VENCEDOR pertence ao prefab da missão de arrancada e só foi conferido no render offline.

## Veredito
**FASE 6 APROVADA — produção visual do mod concluída.**
