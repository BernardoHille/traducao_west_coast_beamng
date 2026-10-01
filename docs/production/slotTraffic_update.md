# Atualização do `slotTraffic.json` (Fase 5)

## O que é
`levels/west_coast_usa/slotTraffic.json` (23,5 MB, JSON indentado, ~1 milhão de linhas) é a rede do sistema de tráfego por "slots":
- `roads.*.properties.speedLimit`, por faixa;
- `nodes.*.links.*.speedLimit`, por ligação.

Os dois valores ficam em **m/s** e são uma **cópia derivada** do navgraph. Inclui os limites automáticos (8,333 / 13,889 / 16,667 / 22,222 / 27,778 / 33,333) e os explícitos herdados de mph (11,18 / 11,5 / 12 / 15,6464).

## Por que não foi regenerado
O jogo referencia um editor (`editor_slotTrafficEditor`, ações em `lua/ge/extensions/core/input/actions/editor.json`), mas **o código desse editor não vem no BeamNG.drive 0.39.4.0**: não há `.lua` correspondente na instalação. Sem o gerador oficial, foi usada a alternativa prevista: **edição determinística só das entradas derivadas das vias alteradas**. Nenhum dado foi inventado.

## Como foi atualizado (`tools/production/speed_overrides.py`)
O arquivo é percorrido linha a linha, com o caminho JSON acompanhado por uma pilha de chaves. **Só linhas `"speedLimit":<valor>` são reescritas.** A formatação, a ordem das chaves e todos os outros bytes são copiados do arquivo do jogo. Há duas regras:

1. **Classe de valor (exata):** 11,18, 11,5 e 12 m/s nunca saem do limite automático (lista métrica 30/50/60/80/100/120 km/h). **Todas** as vias do navgraph com esses valores são convertidas nesta fase; o script aborta se alguma ficar de fora. Logo, no arquivo derivado o valor identifica a origem sem ambiguidade e é trocado por **11,1111**.
2. **Geometria + valor antigo:** para as vias que antes tinham limite **automático** e passam a ter explícito (placas R-19 40 e 10), as faixas do slot traffic são casadas pela geometria: ≥ 90 % das amostras da linha central a ≤ 1,6 m + meia largura do eixo da via. Além disso, só é alterada a faixa cujo valor atual é igual ao limite efetivo antigo da via, lido do navgraph em execução (`map.findClosestRoad` nos nós da via, valor modal). Faixas vizinhas casadas por proximidade, mas com outro valor (ex.: rodovia de 100 km/h ao lado), são **ignoradas** e listadas no relatório.

## O que mudou
Detalhe linha a linha: `tests/reports/phase5_speed_diff.json`. A tabela abaixo é preenchida pelo relatório da execução final.

| Regra | Linhas | De → para (m/s) |
|---|---:|---|
| classe de valor | 630 | 11,18 / 11,5 / 12 → 11,1111 (172 faixas + 458 ligações: todas as ocorrências) |
| geometria (40 km/h) | 197 | 16,667 / 8,333 → 11,1111 |
| geometria (10 km/h) | 112 | 8,333 / 13,889 / 16,667 → 2,7778 |
| **total** | **939** | 243 faixas + 696 ligações |

- **Ignoradas:** 28 faixas, cujo valor diverge do limite efetivo antigo da via. São 20 conectores manuais de 50 m/s, próprios do slot traffic, e 8 faixas de vias vizinhas de 60/80/100 km/h, casadas só por proximidade.
- **Sem faixa no slot traffic:** 6 vias com decisão por placa: 5 faixas internas das cabines das docas e o conector de 13 m `285c1e9e`. O slot traffic não modela essas faixas; o navgraph (IA, polícia) continua sendo a fonte do limite e foi conferido no jogo. As 33 vias explícitas sem casamento geométrico já estão cobertas pela regra de classe de valor.

## Verificação
- `python tools/validation/validate.py new`: cada linha diferente do `slotTraffic.json` do jogo precisa ser uma linha `"speedLimit": <número>` com a mesma estrutura; nada mais pode mudar.
- O arquivo é reaberto com `json.loads` ao final da geração.

## Como reproduzir
```bash
python tools/production/speed_overrides.py          # level overrides + slotTraffic + relatório + sign_regulation.json
python tools/production/speed_overrides.py --check  # só verifica o que está no mod
python tools/validation/validate.py new
```
Se o BeamNG passar a trazer o editor de slot traffic, a regeneração oficial substitui este procedimento. As decisões por via continuam em `working/speed/speed_changes.json`.
