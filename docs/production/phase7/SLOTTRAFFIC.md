# Fase 7 — slotTraffic.json

Método da Fase 5 (`docs/production/slotTraffic_update.md`), estendido em `tools/production/speed_overrides.py`. A edição é determinística e nunca manual. O editor oficial não vem no 0.39.4.

## Regras

1. **Geometria primeiro.** As faixas do arquivo casam com cada DecalRoad alterado: ≥ 90 % das amostras da linha central ficam a até 1,6 m + meia largura do eixo da via. Uma faixa só é reescrita se o valor atual for o valor antigo efetivo da via: o explícito, ou o automático. Para as faixas do pedágio, a via tem vários automáticos ao longo do comprimento (50/60/80/100/120), e todos são aceitos.
2. **Classe de valor.** Os valores explícitos vindos de mph (11,18 / 11,5 / 12 / 15,6464) nunca saem da lista métrica automática. Como **todas** as vias com esses valores foram convertidas, o próprio valor identifica a origem: 15,6464 → 16,6667. O gerador recusa a execução se alguma via de uma classe ficar sem decisão.
3. Uma faixa casada por geometria com uma via de decisão própria fica com essa decisão. É o caso do DR652, ex-35 mph, que vai a 70, e não a 60.
4. Duas vias com alvos diferentes na mesma faixa interrompem a geração (erro).
5. Faixa que já tem o valor alvo (DR758: 33,333333 ≈ 33,3333) não é tocada.

## Resultado (`tests/reports/phase7/functional_diff.md`)

| Item | Valor |
|---|---:|
| linhas editadas | 1109 (939 da Fase 5, todas conferidas uma a uma, + 170 da Fase 7) |
| DR652 → 19,4444 | 31 linhas (geometria) |
| DR312 → 13,8889 | 7 linhas (geometria) |
| 15,6464 → 16,6667 | por geometria (DR666, DR571, DR989, DR1003, DR1009, DR1216) e por classe (faixas sem casamento geométrico: ilha, docas, fim do DR571) |
| faixas do pedágio → 11,1111 | casadas por geometria (as faixas do pedágio do arquivo cobrem só parte das 5 vias) |
| valores de mph restantes | **0** |
| JSON | válido; só linhas `"speedLimit": n` diferem do arquivo do jogo |

## Consistência com o navgraph (`tests/reports/phase7/slottraffic_consistency.md`)

O valor de cada faixa foi comparado com o navgraph (jogo, mod ativo) a 25/50/75 % da linha central.
- **navgraph 60 × slotTraffic 56,3: 0 casos** (nenhum valor de mph em lugar nenhum).
- Faixas da Fase 7: todas iguais ao navgraph, exceto a LE71 (8 m no fim do DR652). O valor dela está certo (70); a amostra caiu na aresta seguinte da junção.
- As diferenças das faixas não tocadas vêm do próprio arquivo do jogo (o valor da faixa é um resumo; em junções e vias sobrepostas, a amostra cai em outra aresta). Não envolvem nenhum valor alterado.
