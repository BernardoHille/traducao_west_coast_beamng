# Fase 8 — QA global e testes externos

**Registro formal feito em:** 21/10/2026, no início da Fase 9.
**Status:** aprovada pelo responsável do projeto.

## Origem deste documento

A Fase 8 foi conduzida e aprovada **fora do repositório**: o responsável do projeto aplicou testes com usuários externos e comunicou o aceite em 21/10/2026, ao abrir a Fase 9. Até essa data **não havia relatório local da Fase 8**: nenhum arquivo em `tests/reports/`, nenhuma captura e nenhum commit posterior à versão 0.7.0.

Este documento registra **só o que pode ser comprovado**: o aceite comunicado e o estado do repositório. Os campos sem evidência local estão marcados como tal, e nada foi completado por suposição.

## Dados

| Campo | Valor | Fonte |
|---|---|---|
| Data do aceite | 21/10/2026 | comunicado do responsável ao abrir a Fase 9 |
| Data dos testes | não registrada no repositório | — |
| Versão testada | **0.7.0** | confirmada pelo responsável |
| Commit testado | **`1973cdb`** (`main`, igual a `origin/main` em 21/10/2026) | confirmado pelo responsável; não há commit posterior à 0.7.0 |
| BeamNG.drive | **0.39.4.0** (versão do desenvolvimento e da validação da Fase 7). A versão usada por cada testador externo não foi registrada | `integrity.json` da instalação de referência |
| Escopo de QA | West Coast USA com o mod: sinalização, marcações no pavimento, comércio/postos/publicidade, indústria, transporte, camada funcional em km/h (limites, radares, zonas, missões) | escopo da versão 0.7.0 (Fases 5–7) |
| Testes por usuários externos | **sim**, confirmados pelo responsável | comunicado do responsável |
| Testadores | anônimos ("testadores voluntários da fase de QA"); quantidade e perfil não registrados | decisão do responsável |
| Resultado geral | aprovado, sem problemas bloqueadores reportados para o escopo da versão | comunicado do responsável |
| Bugs encontrados/corrigidos | nenhum documentado; nenhuma alteração do mod depois da 0.7.0 | histórico Git |

## Evidência automática disponível da versão testada

A versão 0.7.0 é a mesma que fechou a Fase 7, cujo QA está versionado:
- `tests/reports/phase7/regression_summary.md`: selftest 121, regressão 10/10, `mod` 273, `mod --installed` 274, `new` 108, `speeds` FAIL 0, 59 testes unitários;
- QA no jogo: matriz do navgraph 19/19, IA 7/7, radares 18/18, ADAS 50 (×2), Event 01, Reaction Test, garageToGarage, MOD OFF/ON, smoke visual.

## Limitações conhecidas no momento do aceite

As registradas na Fase 7 (`docs/production/PHASE7_FUNCTIONAL_INTEGRATION.md`, seção "Limitações e registros"). Nenhuma delas foi tratada na Fase 8 — por exemplo, o painel de preço do posto `s_fuel_sign_trilobite` segue em inglês. A lista consolidada para a 1.0.0 está em [`docs/release/KNOWN_ISSUES.md`](../release/KNOWN_ISSUES.md).

## Veredito

**FASE 8 APROVADA — QA global e testes externos concluídos.**

A versão candidata passou pela campanha de QA prevista e por testes externos, sem problemas bloqueadores reportados para o escopo da versão 1.0.0.
