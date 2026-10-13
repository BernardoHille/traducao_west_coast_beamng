# Fase 7 — slotTraffic × navgraph

Gerado a partir de `slottraffic_consistency.json` (`working/functional/slot_consistency.py`): para cada faixa do `slotTraffic.json` do mod, o limite do navgraph (jogo, mod ativo) a 25/50/75 % da linha central.

| Grupo | Igual | Diferente |
|---|---:|---:|
| phase7_edited | 31 | 1 |
| phase5_edited | 193 | 14 |
| untouched | 2053 | 192 |

- Faixas sem sobreposição com o navgraph (≤ 3 m): 172.
- **navgraph 60 × slotTraffic 56,3 (ou qualquer valor de mph): 0** — nenhum valor de mph restou (o gerador também confere: `mph_values_left = 0`).
- A faixa da Fase 7 marcada como diferente (LE71, 8 m no fim do DR652) tem o valor certo (70): a amostra caiu na aresta seguinte da junção (100).
- As diferenças das faixas não tocadas são do próprio arquivo do jogo (o valor da faixa é um resumo por faixa; nas junções e vias sobrepostas a amostra cai em outra aresta). Elas existem igualmente com o mod desligado e não envolvem valores alterados.
- Edições: 939 linhas da Fase 5 preservadas (conferidas uma a uma) + linhas da Fase 7 (ver `functional_diff.md`).
