# Validador de assets

Pipeline automático que impede os erros das traduções antigas de voltarem: resolução, formato DDS, sRGB/linear, mipmaps, alfa (perda e ruído), pixels alterados fora das áreas autorizadas, mapas auxiliares esquecidos, nomes/caminhos no mod e coerência de velocidades.

Nenhum comando altera texturas, o mod, o jogo ou os originais.

## Instalação

Python 3.10+ com `numpy` e `Pillow` (`pip install -r tools/validation/requirements.txt`). O `pytest` é opcional: os testes usam `unittest` da biblioteca padrão.
O `texconv` **não** é necessário para validar: o cabeçalho DDS é lido direto do arquivo (`dds_parser.py`).
Para `speeds --refresh`: BeamNG aberto com o servidor MCP ligado e o West Coast carregado.

## Comandos

```bash
python tools/validation/validate.py --help
python tools/validation/validate.py texture working/png/t_roadsigns_b.color.png      # PNG vs original
python tools/validation/validate.py dds export/dds/t_roadsigns_b.color.dds          # DDS vs original
python tools/validation/validate.py family t_decal_roadmarkings --source reference   # mapas auxiliares
python tools/validation/validate.py family t_roadsigns --source dir --dir working/pkg --shape-changed true
python tools/validation/validate.py mod --installed                                 # árvore do mod (+ cópia instalada)
python tools/validation/validate.py new                                             # assets sem original (R-19) + overrides de nível
python tools/validation/validate.py speeds                                          # usa o snapshot salvo
python tools/validation/validate.py speeds --refresh                                # recoleta o navgraph via MCP
python tools/validation/validate.py selftest                                        # originais vs eles mesmos + DDS do PoC
python tools/validation/validate.py regression                                      # traduções antigas precisam ser pegas
python tools/validation/validate.py all                                             # tudo + summary
python -m unittest discover -s tools/validation/tests -v                            # testes unitários
```

O original é localizado **pelo nome** da textura (sufixos `_ptbr`/`_poc` ignorados) no manifesto da Fase 0, e o SHA-256 dele é conferido antes de qualquer comparação. Se não bater: `FAIL`.

## Resultados

Cada verificação devolve **PASS**, **WARN**, **FAIL** ou **SKIP** (não aplicável/sem dados). O relatório herda o pior status.
**Exit code:** `0` = nenhum FAIL · `1` = há FAIL · `2` = erro interno da ferramenta.

Relatórios em `export/reports/validation/<nome>.md` + `.json` (JSON estável para CI). Heatmaps em `export/reports/validation/images/` (`*_diff.png` = RGB em vermelho, `*_alpha_diff.png` = alfa em azul, regiões autorizadas contornadas em verde). Os heatmaps são regeneráveis e ficam fora do Git.

## O que é verificado

| Módulo | Verificações |
|---|---|
| `validate_texture.py` (PNG) | SHA do original · resolução idêntica · **perda de transparência** (alfa 0 → opaco; candidata totalmente opaca quando o original tinha transparência) · semitransparência alterada · **ruído de alfa** (`opaque_pixels_modified`, ex.: 193–221 onde era 255) · diff RGB e alfa separados (quantidade, %, média, máximo, PSNR, bounding box) · **mudanças dentro × fora das regiões autorizadas** · heatmaps |
| `validate_dds.py` | magic, cabeçalho, FourCC legado e DX10, DXGI (BC1/DXT1, BC2, BC3/DXT5, BC4, BC5, BC6H, BC7, BC7_SRGB, RGBA8) · resolução · formato idêntico ao original · **sRGB × linear** (não aceita BC7_UNORM no lugar de BC7_UNORM_SRGB) · mapas de dados (`_o.data`, `_r.data`, `_ao.data`, `_m.data`, `.normal`) nunca sRGB · **mipmaps** = original e cadeia coerente até 1×1 · tamanho do arquivo = tamanho calculado (detecta DDS truncado) · modo de alfa DX10 compatível |
| `validate_family.py` | mapas entregues por família (`config/texture_families.json`) · obrigatórios presentes · **regra `shape_changed`**: se a forma mudou, os mapas de `requires_on_shape_change` (ex.: road markings → opacity, normal, AO) têm de vir juntos |
| `validate_mod_tree.py` | `mod_info/<mod>/info.json` válido · cada DDS/PNG em um **caminho virtual conhecido** · proibidos `_ptbr`, `_poc`, backups, temporários, `Thumbs.db`, PSD/XCF · duplicatas (inclusive só por maiúsculas) · PNG no mod gera aviso · cópia instalada no BeamNG idêntica (`--installed`) |
| `validate_new_assets.py` (`new_asset_spec`, Fase 5) | assets sem original no jogo, contra a especificação declarada em `config/new_assets.json`: resolução, formato, sRGB/linear, mips completos e modo de alfa dos DDS; máscara de disco (cantos transparentes, centro opaco, cobertura); **halo** (borda da máscara na cor da orla); materiais (nomes próprios, nenhum material do jogo redefinido, texturas presentes no mod, alphaTest/alphaRef); meshes (estrutura idêntica ao original, exceto material/UV; `.cdae` presente e mais novo que o `.dae`); overrides de nível (só `speedLimit` e `shapeName` declarados mudam em relação ao zip do jogo) |
| `validate_speed_consistency.py` | limites explícitos em **múltiplos de 10 km/h** · zonas do mapa e de missões · **radar = via** (salvo zona que regulamente o valor) · **placa = via** (unidade km/h + valor) · ADAS de reconhecimento/alerta = via no início do cenário · Reaction Test excluído (faixa experimental) · missões `arrive` inativas ignoradas |

## Configuração (`config/`)

| Arquivo | Conteúdo |
|---|---|
| `thresholds.json` | Todos os limiares, cada um com justificativa (tolerâncias de pixel/alfa, % fora de região, tolerância de velocidade em m/s, múltiplo de 10). |
| `allowed_regions.json` | Regiões autorizadas por textura. **Só regiões confirmadas** (UV dos meshes ou `textureCoords` dos decais). Sem regiões → toda mudança conta como "fora". |
| `texture_families.json` | Famílias, mapas (papel, arquivo, caminho virtual, local/obrigatório), `requires_on_shape_change`, escopo. |
| `modifications.json` | Declaração por fonte (`mod`, `reference`) de `shape_changed` por família. |
| `regression_expectations.json` | Dataset negativo: quais verificações **precisam** falhar nas traduções antigas. |
| `speed_rules.json` | Caminhos do jogo, padrão das placas (`sign_speed<N>` = mph; `r19_overrides` = meshes R-19 do mod em km/h), classificação ADAS e política de radares. |
| `new_assets.json` | Especificação dos assets novos (R-19) e padrões dos arquivos funcionais permitidos no mod. |
| `sign_regulation.json` | Gerado por `tools/production/speed_overrides.py`: cada placa de velocidade real → vias que ela regulamenta. `speeds` exige placa = limite explícito dessas vias. Decalques de malha (placas das baias do porto) não contam. |

`data/wcusa_speed_snapshot.json`: limite da via no navgraph junto às placas, radares e pontos de início ADAS (coletado via MCP com `--refresh`).

## Regiões autorizadas

```json
"t_roadsigns_b.color": {"regions": [{"id": "stop_r1", "x": 1164, "y": 231, "width": 126, "height": 127, "source": "UV of sign_stop.dae"}]}
```
Antes de produzir uma tradução, registre a região que será editada com a **fonte técnica** da coordenada. Mudanças fora dela acima de `outside_region_change_fail_pct` → `FAIL`.

## Limitações

- O pixel diff não sabe se o texto novo está **correto** nem se está **bonito**: isso é revisão humana + QA no jogo.
- A validação de UV é **indireta** (mudança fora das regiões confirmadas). Só há regiões para `t_roadsigns_b.color` e `t_decal_roadmarkings_b.color`.
- DDS legados (DXT1/DXT5/BC4) não guardam sRGB/linear no cabeçalho: nesses casos só formato e header são comparados.
- A consistência de velocidade depende do snapshot do navgraph; após alterar vias, rode `speeds --refresh`.
- `speeds` lê os `items.level.json` com a mesma precedência do VFS (arquivo do mod primeiro). Num clone novo, rode `python tools/production/speed_overrides.py` antes, porque os overrides não são versionados.
- `validate_family` confere presença de arquivos, não se o mapa auxiliar realmente acompanha a nova forma (comparar máscaras é trabalho futuro).
