# Status do projeto

**Última atualização:** 01/10/2026
**Fase atual:** Fase 5 — t_roadsigns e R-19 10/40 concluídos

## Ambiente

- BeamNG.drive **0.39.4.0** (Steam)
- Mapa principal: **West Coast USA** (`levels/west_coast_usa`)
- Idioma destino: **PT-BR**

## Estado atual

- **Originais extraídos:** 35 texturas, cada uma em DDS (formato do jogo) e PNG (base de edição). Ficam em `source/originals/`, só localmente, fora do Git.
- **Traduções existentes:** 13 PNG `_ptbr` em `source/reference_ptbr/`, que correspondem a 11 texturas traduzidas e 1 máscara. O `t_sealbrik_logo` `_ptbr` é cópia idêntica do original.
- **Status das traduções existentes:** servem **só de referência** até serem reconstruídas a partir dos originais. Não são masters aprovados.
- **DDS PT-BR definitivos:** `t_roadsigns_b.color` e `t_roadsigns_o.data` (`export/dds/t_roadsigns/`), mais os R-19 (`export/dds/r19/`). O DDS do PoC (`export/dds/poc/`) é só histórico.
- **Mod** (`mod/traducao_ptbr_wcusa/`, versão 0.5.0):
  - atlas `t_roadsigns` definitivo;
  - família `roadsigns_ptbr_r19` (texturas, materiais, meshes e `.cdae`);
  - overrides de dados do nível (limites de via, `slotTraffic.json`, 7 `shapeName`), gerados localmente e não versionados.
- **Inventário:** `docs/inventory/original_files_manifest.csv` (SHA-256) e `docs/inventory/texture_families.md`.
- **Especificação de localização:** `docs/LOCALIZATION_RULES.md` (fonte de verdade) + `docs/localization/` + `docs/inventory/speed_*.md`.
- **Auditoria inicial:** `docs/AUDITORIA_PROJETO_TRADUCAO.md`, snapshot de 30/09/2026 que não deve ser editado.

## Pipeline

- [x] Auditoria inicial
- [x] Estrutura do projeto
- [x] Versionamento
- [x] Proof of Concept do override
- [x] Regras definitivas de localização
- [x] Validador
- [ ] Reconstrução das traduções existentes (`t_roadsigns` concluída na Fase 5; demais famílias legadas pendentes)
- [ ] Tradução das texturas pendentes
- [ ] QA West Coast
- [ ] QA East Coast / Utah
- [ ] QA ADAS
- [ ] Release

## Resultado da Fase 1 — PoC do override

Detalhes em [`BEAMNG_OVERRIDE_POC.md`](BEAMNG_OVERRIDE_POC.md).

- **Textura testada:** `t_roadsigns_b.color` (família `t_roadsigns`). O `t_roadsigns_o.data` não foi alterado.
- **Caminho virtual confirmado:** `assets/materials/signage/roadsigns/t_roadsigns_b.color.dds` (original em `content/assets/materials/signage.zip`).
- **Formato DDS:** DX10 BC7_UNORM_SRGB, 2048×1024, 12 mipmaps, gerado com texconv (DirectXTex may2026).
- **User folder:** `C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\` → mod em `mods\unpacked\traducao_ptbr_wcusa\`.
- **Teste A/B/C** (placa STOP id 94335, West Coast): ON = "PARE" · OFF = "STOP" · ON de novo = "PARE" ✔
- **Asset global:** não confirmado nesta fase. O East Coast define o material `roadsigns`, mas as placas visíveis de lá usam `signs_usa`.
- **Status da textura:** *override técnico validado*. **Tradução NÃO aprovada.**
- **Achado:** o PoC mostrou na prática o deslocamento de UV da referência PT-BR (octógono do PARE deslocado, "E" cortado), o que confirma o problema 2 abaixo.

## Resultado da Fase 2: Automação de QA

Detalhes em [`BEAMNG_MCP_CAPABILITIES.md`](BEAMNG_MCP_CAPABILITIES.md), [`../tools/beamng/QA_PROTOCOL.md`](../tools/beamng/QA_PROTOCOL.md) e [`../tests/reports/t_roadsigns_automation_test.md`](../tests/reports/t_roadsigns_automation_test.md).

- **MCP validado:** servidor `beamng-game` em `http://127.0.0.1:29292/mcp`, com 86 ferramentas. O que foi testado está documentado.
- **Capacidades principais:**
  - `load_level` / `get_status`;
  - `set_free_camera` / `get_camera_state`;
  - `set_time_of_day`;
  - `toggle_ui`;
  - `screenshot` (assíncrono);
  - `file_info` (origem VFS);
  - `get_logs`;
  - `run_lua` para mods (`core_modmanager`), objetos/materiais (`scenetree`, `getMaterialNames`) e ambiente (`core_environment`).
- **Automação:** runner `tools/beamng/qa_runner.py`, que fala direto com o MCP, mais o protocolo equivalente em `QA_PROTOCOL.md`.
- **Catálogo:** `tests/qa_locations.json`, com **3 pontos** de `t_roadsigns` (STOP Chinatown, YIELD, SPEED LIMIT 25). Câmeras lidas do jogo.
- **Presets:**
  - `tests/presets/day.json`: `time 0.0` (meio-dia observado), `windSpeed 0`, `cloudCover 0`;
  - `night.json`: `time 0.5`, mesmo ambiente;
  - `camera_defaults.json`: free cam, FOV 50, UI oculta.
- **Screenshot:** `screenshot` do MCP, com espera até o arquivo estabilizar. PNG 1920×993, copiado para `tests/screenshots/baseline|current/<família>/<ponto>_<estado>[_night].png`.
- **ON/OFF:** `core_modmanager.activateMod/deactivateMod` **+ `load_level` obrigatório**. Sem recarga, o resultado é não determinístico. O runner sempre recarrega no início.
- **Reprodutibilidade:** pose restaurada com deslocamento de 0 px. Diferença A×B de 0,5–1,0, contra ruído de 0,1–0,4.
- **Limitações:**
  - resolução presa ao tamanho da janela;
  - ids de objeto mudam a cada carga (catálogo usa shape + posição);
  - ~75 s por troca de estado do mod;
  - semântica de `time` invertida em relação à descrição da ferramenta;
  - sem ferramenta dedicada para mods e clima;
  - `raycast` sem material.
- **Achado de conteúdo** (para a reconstrução): a referência antiga também desloca o triângulo da YIELD. A SPEED LIMIT continua em inglês.

## Resultado da Fase 3 — Especificação de localização PT-BR

Detalhes em [`LOCALIZATION_RULES.md`](LOCALIZATION_RULES.md).

- **Matriz:** [`localization/LOCALIZATION_MASTER.csv`](localization/LOCALIZATION_MASTER.csv), com 308 entradas:
  - 219 `rule_defined`;
  - 13 `approved_rule`;
  - 18 `needs_implementation`;
  - 12 `needs_context`;
  - 46 `preserve_original`.
- **Documentos complementares:**
  - glossário ([`GLOSSARY_PTBR.md`](localization/GLOSSARY_PTBR.md));
  - placas de trânsito ([`traffic_signs.csv`](localization/traffic_signs.csv));
  - adaptações culturais ([`cultural_adaptations.md`](localization/cultural_adaptations.md));
  - revisão das traduções antigas ([`legacy_translation_review.md`](localization/legacy_translation_review.md)).
- **Velocidades:** [`inventory/speed_limits.md`](inventory/speed_limits.md) e [`inventory/speed_dependencies.md`](inventory/speed_dependencies.md).
- **Fontes normativas:** MBST SENATRAN/CONTRAN Vol. I (regulamentação) e Vol. IV (horizontal), com página citada para cada regra.
- **Achados técnicos que afetam a implementação:**
  - o R-19 exige material e mesh próprios, porque os algarismos do atlas são compartilhados;
  - os postos do West Coast usam `eca_genericsigns_d.dds`, no caminho do East Coast;
  - os outdoors usam `t_billboards_b`;
  - há uma família nova, `t_bus_routes_utah_d`;
  - os letreiros de fachada são montados por glifos sem acento;
  - hoje placas e limite funcional já divergem no jogo original.

## Resultado da Fase 4 — Pipeline de validação

Detalhes em [`../tools/validation/README.md`](../tools/validation/README.md) e [`../tests/reports/validation_baseline.md`](../tests/reports/validation_baseline.md).

- **Comando central:** `python tools/validation/validate.py texture|dds|family|mod|speeds|selftest|regression|all`. Exit 0/1/2; relatórios MD + JSON em `export/reports/validation/`; heatmaps regeneráveis (fora do Git).
- **Parser DDS próprio** (sem depender do texconv): legado e DX10, BC1–BC7 com sRGB/linear, mipmaps e tamanho. Reconhece os 35 originais e o PoC, com tamanho calculado igual ao real byte a byte.
- **PNG:** resolução, perda de transparência, ruído de alfa, diff RGB e alfa separados, regiões autorizadas (só as confirmadas por UV/decal) e heatmaps.
- **Famílias** (`config/texture_families.json`) com a regra `shape_changed` → mapas auxiliares obrigatórios. **Árvore do mod:** nomes, caminhos virtuais, `_ptbr`, lixo e cópia instalada.
- **Velocidades:** múltiplos de 10; placa = via; radar = via (salvo zona); ADAS de limite = via; Reaction Test excluído.
- **Baseline:**
  - self-test 72/72 PASS;
  - regressão 10/10: as traduções antigas foram pegas e a cópia idêntica passou;
  - mapa atual com 17 FAIL de velocidade, que são inconsistências reais.
- **Testes:** 33 testes unitários (unittest, fixtures sintéticos), todos OK.

## Resultado da Fase 5 - Primeira produção definitiva

Detalhes em [`production/PHASE5_ROADSIGNS.md`](production/PHASE5_ROADSIGNS.md):
- plano e inventário: [`production/t_roadsigns_plan.md`](production/t_roadsigns_plan.md);
- `slotTraffic`: [`production/slotTraffic_update.md`](production/slotTraffic_update.md);
- relatórios em `tests/reports/`: `r19_mesh_validation.md`, `phase5_speed_delta.md`, `phase5_navgraph_check.json` e `phase5_ai_test.json`.

| Item | Situação |
|---|---|
| `t_roadsigns` | **reconstruído** a partir do original. 44 regiões com evidência de UV; 0 px fora das regiões; alfa intacto; BC7 sRGB/linear, 12 mips; máscara de opacidade refeita para as palavras recortadas |
| R-19 10 | **implementado**: mesh próprio para as 7 placas reais de 5 mph (o `sign_speed5.dae` original continua nas 30 placas de baia do porto) |
| R-19 40 | **implementado**: `sign_speed25.dae` substituído no mesmo caminho (11 placas) |
| Limites associados | **sincronizados**: 83 vias a 40 km/h (11,1111 m/s) e 18 a 10 km/h (2,7778 m/s); `slotTraffic.json` coerente (939 linhas) |
| PoC antigo | **substituído** (a referência antiga ficou como `superseded_by_phase5`) |
| QA | **aprovado**: 33 pontos com par original × PT-BR (5 também à noite); navgraph 13/13; IA respeita 40/10; mod desligado volta ao original sem cache residual |
| Matriz | 40 entradas `qa_passed`; `needs_context` 11 → 10 (Rush Rd: não usado no West Coast) |
| Validador de velocidade | 17 → 13 FAIL, todos fora do escopo (60 km/h, zonas, radares, ADAS) |

**Achados técnicos que valem para as próximas fases:**
- **Recarregar o mesmo mapa não limpa caches:** texturas, shapes e dados do nível persistem. O QA passa por outro mapa a cada troca de estado.
- **Mod com `.dae`:** precisa distribuir o `.cdae`, senão fica cache em `current/temp` válido mesmo com o mod desligado.
- **`sign_speed5.dae` também é decalque das baias do porto:** antes de substituir um mesh no mesmo caminho, verificar o `decalType` das instâncias.
- **Janela do jogo minimizada ou em segundo plano:** cargas de mapa travam se minimizada, e o `TimeOfDay` pode não tickar. Os presets fixam a elevação do sol.
- **Palavras compostas por UV:** várias são recortadas pelo `_o.data` e compartilhadas entre placas. O `tools/production/render_signs.py` reconstrói as composições offline.

## Problemas conhecidos

Resumo da auditoria (detalhes em `docs/AUDITORIA_PROJETO_TRADUCAO.md`). **Nenhum foi resolvido ainda.**

| # | Problema | Referência |
|---|---|---|
| 1 | **Perda de alfa** em PNG PT-BR (`eca_roadsigns_d`, `t_billboardsigns_dealers_b`, `t_sponsors_b`, `t_spearleaf_refinery_logo_b`, `t_movie_studio_signage_b`) e ruído no alfa de todos os PNG PT-BR | Auditoria §4.3 |
| 2 | **Imagens regeneradas:** entre 26% e 78% dos pixels mudaram fora das áreas de texto, com risco de desalinhar a UV | Auditoria §4.2 |
| 3 | **Road markings incompletos:** só o `_b.color` foi traduzido. `_o.data`, `_nm`, `_ao`, `_r` e `_m` continuam com as letras em inglês | Auditoria §4.1 |
| 4 | **Emissivos incompatíveis:** `eca_genericsigns_emissive` não acompanha o novo layout | Auditoria §4.4 |
| 5 | **Formatos DDS diferentes** entre texturas (BC7 sRGB, BC7 linear, BC4, DXT1, DXT5). Não dá para exportar tudo como BC7 | Auditoria §4.5 |
| 6 | **Assets globais afetam outros mapas:** a maioria fica em `assets/materials/` e é usada também por East Coast, Utah etc. | Auditoria §3 |
| 7 | ~~Política mph/km/h pendente~~ → **definida na Fase 3**. A implementação continua pendente: R-19 com material/mesh próprios e `speedLimit` funcional | `LOCALIZATION_RULES.md` §2–3 |
| 8 | Mapas auxiliares **não citados na auditoria** (`eca_genericsigns` `_o/_nm/_ao/_r`, `steel_factory_brand` `_nm/_ao/_r`, `billboardsigns_dealers` `_o`…) | `docs/inventory/texture_families.md` |
| 9 | A auditoria diz "41 texturas", mas são **35** | `docs/inventory/texture_families.md` |

## Decisões tomadas (Fase 3)

- **Velocidades em km/h**, com limite visual e funcional **coincidentes** (placa = via = radar = zona = missão = ADAS).
- Velocidades de placa em **múltiplos de 10** (MBST-I). Tabela padrão: 5→10, 15→20, 25→40, 30→50, 35→60, 50→80 mph→km/h.
- **R$ sem conversão cambial** (`R$ 4,99`, `R$ 400`).
- **Sistema métrico** (km, m, t, °C, litro), vírgula decimal e horário de 24 h.
- **Assets globais permanecem globais.** O override fica no caminho original, e os efeitos em outros mapas serão testados no QA.
- **Marcas e nomes próprios fictícios preservados.** Só o tipo de logradouro é adaptado.
- **R-2 sem legenda e R-3 sem texto**, conforme o MBST.

## Decisões tomadas (Fase 4)

- **Distintivo Firwood:** preservar o original.
- **Radar:** o limite acompanha o limite regulamentado da via, salvo zona explicitamente sinalizada com outro valor.
- **ADAS de reconhecimento/alerta de limite:** o limiar acompanha o limite regulamentado do cenário (ADAS 50 = R-19 50 = via 50).
- **Reaction Test:** a faixa 40–70 km/h é experimental e independente do limite da via.

Essas regras estão implementadas no validador (`validate.py speeds`). Nenhuma alteração funcional foi feita no mapa.

## Decisões tomadas (Fase 5)

- **R-19 com material, textura e mesh próprios** (família `roadsigns_ptbr_r19`, escopo de nível); o atlas compartilhado não muda.
- **Mesh no mesmo caminho só quando todas as instâncias são o alvo:** `sign_speed25` sim; o R-19 10 é por instância.
- **Placa = via:** limites explícitos por `DecalRoad` (granularidade do jogo), decididos por posição, orientação e contexto; vias públicas não são reduzidas a 10.
- **`slotTraffic.json`:** edição determinística das entradas derivadas, porque o editor oficial não vem no jogo.
- **Overrides de dados do nível não são versionados:** são regenerados a partir da instalação local.

## Decisões pendentes

- **Como aplicar as regras ADAS/radar no mapa** (fase de implementação funcional):
  - rota das missões de 50 km/h: via de 120 km/h hoje;
  - Event 01: 70 km/h numa via de 40,2 km/h;
  - radar 4 a 56,3 km/h numa via de 100 km/h.
- **`ONLY` no pavimento** (BUS ONLY / EXIT ONLY): proposta de override de `main.decals.json` com slots livres — não investigado além da Fase 3.
- **Itens `needs_context`** da matriz (nomes de paradas, departamentos do estúdio, letreiros de fachada): não resolvidos. Rush Rd foi resolvido na Fase 5.
- **Placas compostas por glifos compartilhados** (SPEED LIMIT/MPH do `roadsigns.dae`, cabine de pedágio, ONLY, CARPOOLS, ½ MILE): exigem assets/meshes próprios.
- **Estratégia para mapas auxiliares não extraídos** (quais extrair e quando).
- **Regiões autorizadas** para as demais texturas: registrar antes de produzir cada uma.
