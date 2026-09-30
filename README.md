# Tradução PT-BR — West Coast USA | BeamNG.drive

Projeto de tradução para o português do Brasil dos **elementos visuais** (texturas de placas, letreiros, outdoors, sinalização e marcações no asfalto) do mapa **West Coast USA** do BeamNG.drive.

> ⚠️ **Projeto experimental.** Ainda não existe um mod validado no jogo. **Não há instruções de instalação**: elas serão escritas depois que o override de textura for testado e aprovado.

## Estado

**Fase 3 — Especificação de localização PT-BR (concluída).** As regras definitivas de localização estão em [`docs/LOCALIZATION_RULES.md`](docs/LOCALIZATION_RULES.md). O override de textura foi validado ([`docs/BEAMNG_OVERRIDE_POC.md`](docs/BEAMNG_OVERRIDE_POC.md)) e há um pipeline de QA visual ([`tools/beamng/QA_PROTOCOL.md`](tools/beamng/QA_PROTOCOL.md)). Ainda não existe tradução implementada.

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
