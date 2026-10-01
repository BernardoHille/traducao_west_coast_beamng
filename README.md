# Tradução PT-BR — West Coast USA | BeamNG.drive

Projeto de tradução para o português do Brasil dos **elementos visuais** (texturas de placas, letreiros, outdoors, sinalização e marcações no asfalto) do mapa **West Coast USA** do BeamNG.drive.

> ⚠️ **Projeto em produção.** A primeira família definitiva (`t_roadsigns` + placas R-19 10/40 km/h) está pronta e validada no jogo. Ainda não há instruções de instalação para usuários finais: elas virão com o pacote de release.

## Estado

**Fase 5 — `t_roadsigns` e R-19 10/40 concluídos.** Detalhes em [`docs/production/PHASE5_ROADSIGNS.md`](docs/production/PHASE5_ROADSIGNS.md):
- atlas de placas reconstruído a partir do original (PARE, R-2, R-3, painéis, destinos);
- placas R-19 10/40 km/h próprias;
- 101 vias com limite funcional sincronizado.

Ferramentas e referências: validador em [`tools/validation/`](tools/validation/README.md), ferramentas de produção em `tools/production/`, regras em [`docs/LOCALIZATION_RULES.md`](docs/LOCALIZATION_RULES.md) e QA visual em [`tools/beamng/QA_PROTOCOL.md`](tools/beamng/QA_PROTOCOL.md).

**Clone novo:** os overrides de dados do nível (limites de via, `slotTraffic.json`) não são versionados, porque são cópias dos arquivos do jogo. Gere-os a partir da sua instalação com `python tools/production/speed_overrides.py`.

O acompanhamento detalhado fica em [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md).

## Escopo

- Tradução de **texturas**: placas de trânsito, comércio, postos, outdoors, pontos de ônibus, estúdios, indústria, pistas e marcações no asfalto.
- Mapa principal: **West Coast USA**.
- Versão de referência: **BeamNG.drive 0.39.4.0**.
- Velocidades localizadas **de forma funcional** para km/h: placa, limite da via, radares, zonas e missões mudam juntos (ver `docs/inventory/speed_dependencies.md`).
- Fora do escopo por enquanto: textos da interface do jogo.

## Aviso: assets globais

A maioria das texturas de placas fica em `assets/materials/` do BeamNG, que é **compartilhado entre mapas**. Um override nesses caminhos muda a textura em **todos os mapas** que a usam (East Coast USA, Utah etc.), não só no West Coast. A política definitiva ainda está pendente (ver `docs/PROJECT_STATUS.md`).

## Estrutura

```
├── docs/                      Documentação
│   ├── AUDITORIA_PROJETO_TRADUCAO.md   Auditoria inicial (snapshot 30/09/2026)
│   ├── PROJECT_STATUS.md               Status, pipeline e decisões pendentes
│   ├── WORKFLOW.md                     Fluxo obrigatório por textura
│   ├── TEXTURE_GUIDELINES.md           Regras técnicas (formato, alfa, UV…)
│   ├── inventory/                      Manifesto SHA-256 e famílias de texturas
│   └── legacy/                         Guia antigo (histórico)
├── source/
│   ├── originals/             Originais do jogo (DDS + PNG). SÓ LOCAL, fora do Git
│   └── reference_ptbr/        Primeira tentativa de tradução (referência, não master)
├── working/
│   ├── layered/               Masters editáveis (PSD/XCF)
│   ├── png/                   PNG intermediários aprovados
│   └── temporary/             Temporários (fora do Git)
├── export/
│   ├── dds/                   DDS finais gerados pelo pipeline
│   └── reports/               Relatórios dos validadores
├── mod/traducao_ptbr_wcusa/   Árvore do mod (pronta para o BeamNG)
├── tools/                     validation/ · conversion/ · beamng/
└── tests/                     screenshots/ · reports/
```

## Originais do jogo

Os arquivos extraídos do BeamNG (`source/originals/`) **não são versionados**: são assets do jogo e servem só de fonte local para o pipeline. A integridade deles pode ser conferida pelo SHA-256 em [`docs/inventory/original_files_manifest.csv`](docs/inventory/original_files_manifest.csv).

## Fluxo de trabalho

Ver [`docs/WORKFLOW.md`](docs/WORKFLOW.md) e [`docs/TEXTURE_GUIDELINES.md`](docs/TEXTURE_GUIDELINES.md).

## Git LFS

Arquivos binários de textura (DDS, PNG, PSD, XCF e outros) são versionados com **Git LFS** (ver `.gitattributes`). Instale o Git LFS antes de clonar.
