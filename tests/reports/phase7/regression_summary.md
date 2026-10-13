# Fase 7 — Resumo de regressão e validação

Executado em 13/10/2026 com o BeamNG.drive 0.39.4 aberto, West Coast carregado e mod instalado (cópia instalada idêntica ao repositório).

| Verificação | Resultado |
|---|---|
| `validate.py selftest` | PASS 121 |
| `validate.py regression` | PASS 10/10: as traduções antigas continuam reprovadas e a cópia idêntica continua aprovada |
| `validate.py mod` | PASS 273 (inclui o `t_roadsigns` com os 19 tiles novos dentro das regiões autorizadas) |
| `validate.py mod --installed` | PASS 274; cópia instalada idêntica (117 arquivos) |
| `validate.py new` | PASS 108:<br>· R-19 50/70/120: textura, material, malha, `.cdae`;<br>· `roadsigns.dae` e as 2 malhas de cabine: estrutura igual ao original salvo os quads re-apontados, `.cdae` atual;<br>· overrides funcionais: zonas, `info.json`, grupo novo e grupo acrescentado |
| `validate.py speeds --refresh` | **FAIL 0** · PASS 27 · WARN 1 · SKIP 7 (antes: FAIL 13 · PASS 9 · WARN 1 · SKIP 7) |
| Testes unitários | 59 OK (44 anteriores + 15 da Fase 7) |
| Gerador (`apply_phase7_functional.py --check`) | OK: 132 linhas alteradas / 132 declaradas; 15 objetos novos / 15 declarados; zonas e `info.json` só com os valores declarados; slotTraffic sem mph, 939 edições da Fase 5 preservadas |

**WARN restante:** "Speed signs: nearest navgraph edge", 21/25. As 4 placas que diferem são as R-19 40 das cabines das docas da Fase 5: elas ficam na transição e regulam a via seguinte. A situação é a mesma desde a Fase 5, e o check é informativo. As 7 placas novas da Fase 7 coincidem com a aresta mais próxima.

**SKIPs:**
- Reaction Test (faixa experimental, por política);
- 6 missões `arrive` (`maxSpeedActive = false`, funcionalidade inativa).

Nenhum SKIP, tolerância ou regra foi acrescentado para zerar o relatório. As mudanças no validador são:
- leitura das zonas com precedência do VFS;
- declaração dos meshes R-19 novos;
- checagens novas das placas do `roadsigns.dae` e da praça de pedágio, que **aumentam** a cobertura.

## Smoke visual (sem revisão visual geral)

Capturas em `tests/screenshots/phase7/visual_smoke/`, com 0 problemas de VFS:
- PARE (placa e pavimento);
- R-2;
- R-19 10 e 40;
- octanagem do posto;
- outdoor Turbo Burger.

Nada regrediu.

## QA funcional (detalhes nos relatórios ao lado)

| Relatório | Resultado |
|---|---|
| `navgraph_matrix.md` | 19/19 pontos reais (10/40/50/60/70/80/100/120) |
| `slottraffic_consistency.md` | 0 casos navgraph 60 × slotTraffic 56,3; faixas da Fase 7 coerentes |
| `ai_qa.md` | 7/7 (IA não passa do limite em 40/50/60/70/80 nem no pedágio) |
| `radar_qa.md` | 18/18 passagens (abaixo, dentro da tolerância, acima; radar 4 a 100) |
| `adas_qa.md` | ADAS 50 (teste e web) PASS; Event 01 PASS; Reaction Test smoke PASS |
| `zones_missions_qa.md` | zonas lidas do mod; missão garageToGarage Docas iniciada e com trabalho sorteado |
| `mod_off_qa.md` | mod desligado: originais de volta (vias, radares, zonas, `gallonUS`, placas mph, cabine), sem `.cdae` no cache; mod ligado: tudo restaurado |
