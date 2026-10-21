# Changelog

Este projeto segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/) a partir da 1.0.0 (ver [`CONTRIBUTING.md`](CONTRIBUTING.md)). As versões 0.x foram marcos internos de desenvolvimento e não foram distribuídas.

## [1.0.0] — 2026-10-21

Primeira versão pública. Desenvolvida e validada no BeamNG.drive 0.39.4.0.

### Adicionado
- Placas **R-19** próprias de 10, 40, 50, 70 e 120 km/h (malha, materiais e texturas), derivadas de um master único.
- Grupo de nível `ptbr_functional_signs`, com as placas R-19 dos trechos regulamentados novos.
- Pacote de release gerado por script (`tools/release/build_release.py`): ZIP determinístico, manifesto com SHA-256 por arquivo e conferência do conteúdo extraído.

### Localizado
- **Placas de trânsito** (atlas `t_roadsigns`): R-1 PARE, R-2, R-3, painéis, destinos, avisos, placas de obra e de estacionamento.
- **Placas de velocidade embutidas no mapa:** 23 placas regulamentares passam a R-19 com o limite da via e 24 placas de advertência passam a km/h. As cabines do pedágio passam a "NÃO PARE / R-19 40".
- **Marcações no pavimento:** PARE, NÃO BLOQUEIE, SEM SAÍDA, SÓ SAÍDA, ÔNIBUS.
- **Postos e placas genéricas:** bombas (COMUM/ADITIVADA/PREMIUM), avisos de segurança.
- **Outdoors, néons, fachadas, concessionárias e oficinas** (`t_billboards`, `clutter_commercial`), com preços em R$.
- **Indústria e transporte:** refinaria Spearleaf, siderúrgica Hot Rolled, estúdio de cinema, mapa de ônibus de Belasco, pontos de ônibus, arrancada.
- **25 letreiros cujas letras são peças da malha 3D**, recompostos em português, com acentos.

### Funcional
- Limites em **km/h** coerentes entre placa, navgraph, tráfego (`slotTraffic.json`), radares e zonas:
  - vias que eram 25 mph → 40;
  - vias que eram 35 mph → 60;
  - cabines das docas → 10;
  - praça de pedágio → 40;
  - limites automáticos de 100/120 preservados.
- **Radares:** cada um fiscaliza o limite da sua via (60, 70 ou 100), com a tolerância de 10 % do jogo.
- **Zonas** do mapa e das missões garageToGarage em 50/60/80 km/h.
- **Trechos regulamentados para cenários de pesquisa:** zona de 50 km/h na via expressa e corredor de 70 km/h na avenida do Event 01, ambos sinalizados.
- **Combustível em litro:** os painéis dos postos mostram o preço por litro.

### Técnico
- Override puro pelo sistema de arquivos virtual do BeamNG. Nenhum arquivo da instalação do jogo é alterado.
- O pacote não contém cópias sem modificação de arquivos do jogo, o que é conferido por SHA-256 no build.
- Cada malha alterada vai com seu `.cdae` compilado pelo jogo, com data posterior à do `.dae`. Assim, nada fica no cache do usuário quando o mod é desativado.
- Dados de nível gerados de forma determinística a partir de decisões versionadas (`working/functional/`, `working/speed/`).

### QA
- Validadores automáticos: texturas, DDS, famílias, árvore do mod, consistência de velocidades, assets novos, regressão e testes unitários.
- QA no jogo pelo BeamNG MCP: capturas de dia e de noite, matriz do navgraph, IA, radares, cenários ADAS, teste com o mod desligado.
- QA global e testes com usuários externos (Fase 8), sem problemas bloqueadores reportados.
- Teste do ZIP real de release numa instalação limpa (Fase 9).

Limitações conhecidas: [`docs/release/KNOWN_ISSUES.md`](docs/release/KNOWN_ISSUES.md).
