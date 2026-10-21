# Estado final do projeto — versão 1.0.0

Estado congelado da versão 1.0.0, em 21/10/2026. Mudanças posteriores entram em versões novas (1.0.1, 1.1.0…), conforme o [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Objetivo

Localizar o mapa **West Coast USA** do BeamNG.drive para o português do Brasil, de forma coerente: sinalização no padrão brasileiro e unidades métricas que valem tanto na imagem quanto no comportamento do jogo (IA, tráfego, radares). Tudo é feito por override no sistema de arquivos virtual do jogo, sem alterar a instalação.

## Escopo da 1.0.0

- **Visual:**
  - atlas de placas `t_roadsigns`;
  - placas R-19 próprias;
  - marcações no pavimento;
  - placas de posto;
  - outdoors;
  - estúdio, indústria (Spearleaf, Hot Rolled) e mapa de ônibus;
  - `clutter_commercial`;
  - 25 letreiros cujas letras são peças da malha, recompostos;
  - placas de velocidade embutidas no `roadsigns.dae`;
  - cabines do pedágio.
- **Funcional:**
  - limites em km/h nas vias e no `slotTraffic`;
  - radares coerentes com a via;
  - zonas do mapa e do garageToGarage;
  - trechos regulamentados para os cenários de pesquisa;
  - combustível em litro.
- **Fora do escopo:** interface do jogo, painel de preço do posto, placar da arrancada em mph, QA documentado em outros mapas (ver [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)).

## Implementação

- O mod `traducao_ptbr_wcusa` tem 117 arquivos. Destes, 100 substituem um arquivo do jogo e estão todos modificados, 16 são novos e 1 é metadado.
- Cada textura é refeita a partir do original do jogo, mudando só as regiões com evidência de UV, e sai no formato DDS do original.
- Cada malha alterada vai com seu `.cdae` compilado pelo próprio jogo.
- Os dados de nível são gerados de forma determinística a partir de decisões versionadas (`working/functional/`, `working/speed/`) e conferidos linha a linha contra os arquivos do jogo.
- As fases e decisões estão em [`docs/PROJECT_STATUS.md`](../PROJECT_STATUS.md). O artigo técnico está em [`docs/article/ARTIGO_TECNICO_PTBR.md`](../article/ARTIGO_TECNICO_PTBR.md).

## Validação

| Camada | Resultado |
|---|---|
| Validadores automáticos | unittest 63 · selftest 121 · regressão 10/10 · mod 273 · instalado 274 · new 108 · speeds 0 FAIL (1 WARN informativo, 7 SKIPs legítimos) |
| QA no jogo (Fases 5–7) | capturas de dia e de noite por família, matriz do navgraph, IA, radares, cenários ADAS, mod OFF/ON |
| QA global e usuários externos (Fase 8) | aprovado pelo responsável, sem problemas bloqueadores reportados ([registro](../production/PHASE8_GLOBAL_QA.md)) |
| ZIP real de release (Fase 9) | instalação limpa, VFS 116/116 do ZIP, smoke visual e funcional, dia e noite, logs sem erro do mod, mod OFF restaura o original ([RC](../../tests/reports/release/RC_VALIDATION.md)) |

## Versão e pacote

| Campo | Valor |
|---|---|
| Versão | **1.0.0** |
| Tag | `v1.0.0` |
| Pacote | `traducao_ptbr_wcusa_v1.0.0.zip`, 29.846.362 bytes |
| SHA-256 | `684bcf6c2e93c9397fa1acc667dd37792d2e55b05973c32bc1a1bd33396e3b57` |
| Build | [`BUILD_1.0.0.md`](BUILD_1.0.0.md) |

## Compatibilidade

Desenvolvido e validado no **BeamNG.drive 0.39.4.0**. Não há promessa de compatibilidade com outras versões: os dados de nível são cópias dos arquivos da 0.39.4. O pacote não depende de nenhum outro mod.

## Limitações conhecidas

Nenhum problema bloqueador conhecido. Limitações de escopo:
- texturas compartilhadas também aparecem traduzidas em outros mapas;
- interface do jogo, painel de preço do posto e placar da arrancada não foram localizados;
- duas placas urbanas mostram 100 km/h, o limite automático do jogo;
- os trechos de pesquisa (50 na via expressa, 70 no Event 01) estão no pacote;
- o gerenciador de mods mostra o nome do arquivo.

Detalhes em [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).
