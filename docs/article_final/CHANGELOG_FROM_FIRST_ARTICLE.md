# O que mudou em relação à primeira edição

## As duas edições

| | Primeira edição | Edição final |
|---|---|---|
| Local | `docs/article/` | `docs/article_final/` |
| Data | 02/10/2026 | 21/10/2026 |
| Estado documentado | Fase 5 (`70329b1`), mod 0.5.0 | Fase 9, release 1.0.0 (tag `v1.0.0`, `b4a7450`) |
| Fases cobertas | 0–5 | 0–9 |
| Figuras | 21 | 38 (7 reutilizadas da primeira, 31 novas) |
| Tamanho (arquivo inteiro, `wc -w`) | 15.077 palavras | 19.705 palavras; o corpo tem cerca de 16 mil palavras de texto corrido, 18,7 mil com tabelas |

A primeira edição é um **snapshot técnico intermediário**, correto para o seu momento, e continua em `docs/article/` sem alteração. Esta edição não a substitui: conta a história inteira sabendo como o projeto terminou.

## O que foi acrescentado

- **Produção visual completa (Fase 6):**
  - marcações no pavimento com mapas auxiliares e override do `main.decals.json`;
  - postos, outdoors, estúdio, indústria, Spearleaf, Hot Rolled, mapa de ônibus e `clutter_commercial`;
  - a auditoria de cobertura.
- **Letreiros montados por glifos:** a técnica de reescrever palavras na geometria das malhas (25 malhas), com figura explicativa feita a partir de renders offline.
- **Integração funcional (Fase 7):**
  - navgraph com exportação completa e comparação geométrica (598 arestas);
  - `slotTraffic.json` (1.109 linhas);
  - 47 placas embutidas no `roadsigns.dae` e praça de pedágio;
  - radares, com o caso do radar 4;
  - zonas do mapa e de missões;
  - combustível em litro;
  - R-19 50, 70 e 120.
- **Cenários de pesquisa:**
  - zona de 50 do ADAS Speed Alert e corredor de 70 do Event 01;
  - o Reaction Test como faixa experimental;
  - a decisão de manter os trechos no pacote.
- **Validação até 0 FAIL:** progressão completa das suítes (Fase 4 → 9), testes de IA, de radares e de ADAS.
- **QA global e testes externos (Fase 8),** com a distinção entre validação automatizada e avaliação por usuários e o que o registro sustenta ou não.
- **Engenharia da release (Fase 9):**
  - build reprodutível e auditoria de escopo;
  - originais desnecessários e varredura de texto;
  - teste do ZIP real numa instalação limpa;
  - VFS 116/116 e mod OFF.
- **Métricas finais e tabela de evolução** (`DATA_SUMMARY_FINAL.md`).
- **Discussão** sobre localização funcional, relevância para pesquisa, reprodutibilidade e reversibilidade.
- **Limitações reais da 1.0.0,** tiradas de `KNOWN_ISSUES.md`.

## O que foi reavaliado

- **A narrativa.** A primeira edição terminava na primeira família produzida e listava o resto como trabalho futuro. Esta edição organiza o projeto em torno da expansão do problema: texto → atlas → UV → alfa → material → malha → navgraph → radar → ADAS → QA → release.
- **A conversão de velocidades.** Na primeira edição, a tabela era em boa parte "regra ainda não implementada". Aqui ela mostra os valores realmente usados na 1.0.0 e onde cada um vale.
- **O cache.** A primeira edição registrava os achados da Fase 5. Esta mostra o protocolo consolidado, o caso dos 25 `.cdae` da Fase 6 e a regra de datas do ZIP.
- **Os postos.** A auditoria apontou o emissivo incompatível. A Fase 6 descobriu que o material carregado no West Coast não tem emissivo, e o QA noturno da 1.0.0 confirma.
- **A matriz.** De 308 para 323 linhas, com o cruzamento entre status e uso que mostra zero linhas usadas em aberto.

## Números históricos mantidos como históricos

Os números da primeira edição continuam corretos para o seu momento e aparecem neste texto no passado: 13 FAIL na Fase 5, 48 verificações do `mod --installed`, 33 pontos de QA, 44 testes unitários. A edição final marca explicitamente o que era verdade "naquele momento" e o que é verdade "na 1.0.0".

## Figuras

- **Reutilizadas sem alteração**, como registro histórico: heatmap do validador, zoom do STOP no atlas, perda de alfa, PoC ON/OFF/ON, atlas das marcações, asset R-19, placas de baia.
- **Refeitas com capturas da 1.0.0:**
  - comparação do STOP (original / PoC / 1.0.0);
  - R-2;
  - marcações no pavimento;
  - SPEED LIMIT → R-19;
  - abertura;
  - reversibilidade.
- **Diagramas atualizados:** VFS, pipeline e conversão de velocidades. Os da primeira edição não foram alterados.

## Ferramentas

`docs/article_final/tools/` contém versões novas das três ferramentas do artigo:
- `capture_final.py`: só o ZIP de release, estados on/off e exportação do navgraph;
- `build_figures_final.py`;
- `md_to_html_final.py`: capa, sumário e quebras de página.

As ferramentas de `docs/article/tools/` não foram alteradas, e a primeira edição continua reproduzível com elas.
