# QA — <família>

> Template de revisão visual. Preencha a partir dos run reports (`tests/reports/runs/*.json`) e das capturas. **O resultado final é sempre uma decisão humana**; nenhum campo é aprovado automaticamente.

## Ambiente

- BeamNG: <versão, ex.: 0.39.4.0>
- Mapa: <ex.: west_coast_usa>
- Mod: <nome + versão do info.json> (ativo/inativo por estado)
- Data: <AAAA-MM-DD>
- Runner / protocolo: `tools/beamng/qa_runner.py` · `tools/beamng/QA_PROTOCOL.md`
- Run reports: <lista de `tests/reports/runs/*.json`>

## Arquivos testados

| Arquivo no mod | Formato | SHA-256 | Origem VFS com mod ON | Origem VFS com mod OFF |
|---|---|---|---|---|
| `assets/...` | <BC7 sRGB 2048×1024, N mips> | `<sha>` | <realPath> | <realPath> |

Mapas da família que **não** foram alterados (e por quê):

## Pontos testados

| Location id | Objeto (shape) | Posição | Materiais | Câmera (pos / FOV) |
|---|---|---|---|---|
| | | | | |

## DAY

| Ponto | Original (baseline) | Traduzido (current) | Observação |
|---|---|---|---|
| | `tests/screenshots/baseline/<família>/<id>_original.png` | `tests/screenshots/current/<família>/<id>_<estado>.png` | |

## NIGHT

| Ponto | Original | Traduzido | Observação |
|---|---|---|---|
| | `..._original_night.png` | `..._<estado>_night.png` | |

## Verificações

- [ ] DDS carregou (origem VFS = mod; placa mudou em relação ao baseline)
- [ ] textura correta (conteúdo esperado no lugar esperado)
- [ ] UV correta (nenhum elemento deslocado, cortado ou invadindo o vizinho)
- [ ] alfa correto
- [ ] máscara correta (`_o.data` recorta o novo conteúdo)
- [ ] emissivo correto (NIGHT; N/A se a família não tem emissivo)
- [ ] sem artefatos (blocos de compressão, halos, mip errado à distância)
- [ ] sem erro novo no log (comparar `logs.relevant_lines` / `error_warning_counts` com o baseline)

## Observações

<diferenças esperadas vs. inesperadas; elementos dinâmicos (nuvens, tráfego) que não contam como regressão>

## Resultado

<APROVADO / REPROVADO / REQUER REVISÃO> — revisor: <nome>
