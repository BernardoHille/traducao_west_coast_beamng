# West Coast USA — Localização PT-BR

Mod para o **BeamNG.drive** que localiza o mapa **West Coast USA** para o português do Brasil, com sinalização brasileira e o trânsito em km/h.

**Versão 1.0.0** · desenvolvido e validado no **BeamNG.drive 0.39.4.0** · nome técnico `traducao_ptbr_wcusa`

| | |
|---|---|
| ![Placa PARE em Chinatown](docs/release/images/01_pare_chinatown.jpg) | ![PARE e R-19 40 km/h](docs/release/images/02_pare_r19_40.jpg) |
| ![PARE pintado no pavimento](docs/release/images/04_pavimento_pare.jpg) | ![Outdoor à noite com preço em R$](docs/release/images/06_outdoor_noite.jpg) |

## Sobre

A cidade continua sendo Belasco, e as marcas fictícias do jogo continuam as mesmas. O que muda é a linguagem visual e as convenções:
- **idioma:** placas, letreiros, outdoors, avisos e marcações no asfalto em português;
- **sinalização brasileira:** R-1 PARE, R-2 "Dê a preferência", R-19 de velocidade máxima, no padrão brasileiro;
- **sistema métrico:** limites em km/h, distâncias em metros, combustível em litro;
- **moeda:** preços desenhados em R$;
- **coerência funcional:** a placa, o limite da via que a IA respeita, os radares e o tráfego usam o mesmo valor.

## O que é localizado

- **Trânsito:** placas de regulamentação e advertência, pórticos, cabines de pedágio, placas de velocidade em km/h.
- **Pavimento:** PARE, NÃO BLOQUEIE, SEM SAÍDA, SÓ SAÍDA, ÔNIBUS.
- **Comércio e publicidade:** postos de combustível, outdoors, néons, fachadas, concessionárias, oficinas.
- **Indústria e transporte:** refinaria, siderúrgica, estúdio de cinema, pontos e mapa de ônibus, arrancada.
- **Camada funcional:** limites de via, radares, zonas e missões coerentes em km/h.

## Características

- Placas **R-1 PARE**, **R-2** e **R-19** (10, 40, 50, 60, 70, 80, 100 e 120 km/h), feitas a partir das texturas originais do jogo.
- Letreiros cujas letras são peças da malha 3D, recompostos letra a letra em português.
- Velocidades em **km/h** nas placas, no navgraph (o limite que a IA segue), no tráfego, nos radares e nas zonas.
- Radares que fiscalizam o limite da via em que estão, com a tolerância de 10 % do jogo.
- Combustível exibido por litro.
- Funciona de dia e de noite, incluindo néons e letreiros com emissão de luz.

## Instalação

1. Baixe `traducao_ptbr_wcusa_v1.0.0.zip` na página de [Releases](https://github.com/BernardoHille/traducao_west_coast_beamng/releases).
2. Copie o ZIP, **sem descompactar**, para a pasta `mods` da sua pasta de usuário do BeamNG. No Windows, por padrão:
   `%LOCALAPPDATA%\BeamNG\BeamNG.drive\current\mods\`
3. Abra o BeamNG.drive, confira em **Mods** se o mod está ativo, e carregue o West Coast USA.

Detalhes, verificação do arquivo (SHA-256) e solução de problemas em [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

## Desinstalação

Desative o mod no gerenciador de mods do jogo, ou apague o ZIP da pasta `mods`. Depois, carregue o mapa de novo. O jogo volta ao original.

## Compatibilidade

- Desenvolvido e validado no **BeamNG.drive 0.39.4.0**. Outras versões do jogo não foram testadas.
- Mapa: West Coast USA. Algumas texturas são compartilhadas e também aparecem traduzidas em outros mapas.
- Não depende de nenhum outro mod.

## Limitações conhecidas

Nenhum problema bloqueador conhecido. Limitações de escopo, como a interface do jogo, o painel de preço do posto e o placar da arrancada em mph, estão em [`docs/release/KNOWN_ISSUES.md`](docs/release/KNOWN_ISSUES.md).

## Desenvolvimento

O repositório guarda também o processo de desenvolvimento: auditoria, regras de localização, validadores, ferramentas de produção e QA automatizado no jogo.
- Artigo técnico: [`docs/article/ARTIGO_TECNICO_PTBR.md`](docs/article/ARTIGO_TECNICO_PTBR.md)
- Status e histórico das fases: [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- Regras de localização: [`docs/LOCALIZATION_RULES.md`](docs/LOCALIZATION_RULES.md)
- Estrutura do repositório, fluxo de trabalho e versões: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Build do pacote: `python tools/release/build_release.py` (ver [`docs/release/BUILD_1.0.0.md`](docs/release/BUILD_1.0.0.md))
- Mudanças: [`CHANGELOG.md`](CHANGELOG.md)

## Créditos e direitos

Criado por **Bernardo Hille**. O BeamNG.drive e os assets originais do jogo pertencem à BeamNG GmbH. Este mod contém versões modificadas desses assets e só funciona com uma cópia legítima do jogo. As normas brasileiras de sinalização (CONTRAN/SENATRAN) foram usadas como referência. Nem a BeamNG GmbH nem esses órgãos endossam este projeto. Detalhes em [`docs/CREDITS.md`](docs/CREDITS.md).
