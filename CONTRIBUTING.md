# Desenvolvimento e versões

Guia para quem trabalha no repositório. Para instalar o mod, veja o [`README.md`](README.md).

## Repositório × pacote

O **repositório** guarda o projeto inteiro: auditoria, regras, masters, ferramentas, validadores, relatórios, capturas e o artigo técnico. Nada disso é apagado para "limpar" o repositório, porque ele é também a documentação da pesquisa e do desenvolvimento.

O **pacote de release** (ZIP) contém só os arquivos que o jogo carrega. Ele é montado por `tools/release/build_release.py` a partir de `mod/traducao_ptbr_wcusa/` (ver [`docs/release/SCOPE_AUDIT.md`](docs/release/SCOPE_AUDIT.md)).

## Estrutura

```
├── docs/                      Documentação (status, regras, inventário, produção, release, artigo)
├── source/
│   ├── originals/             Originais extraídos do jogo (DDS + PNG). SÓ LOCAL, fora do Git
│   └── reference_ptbr/        Primeira tentativa de tradução (referência histórica)
├── working/
│   ├── layered/               Masters e scripts de composição
│   ├── functional/, speed/    Decisões funcionais versionadas (limites, radares, zonas)
│   ├── png/                   PNG intermediários (gerados)
│   └── temporary/             Temporários (fora do Git)
├── export/                    DDS exportados e relatórios dos validadores
├── mod/traducao_ptbr_wcusa/   Árvore do mod (o que vai para o ZIP)
├── release/                   staging/ e output/ do build (ZIP fora do Git)
├── tools/                     validation/ · production/ · beamng/ · conversion/ · release/
└── tests/                     screenshots/ · reports/
```

## Clone novo

1. Instale o **Git LFS** antes de clonar: texturas, capturas e `.cdae` são versionados com LFS (ver `.gitattributes`).
2. Python 3.11+ com `pip install -r tools/validation/requirements.txt`.
3. Os **originais do jogo** (`source/originals/`) e os **dados de nível do mod** não são versionados, porque são cópias de arquivos do BeamNG. Gere-os a partir da sua instalação 0.39.4.0:
   ```
   python tools/production/apply_phase7_functional.py   # limites, radares, zonas, slotTraffic, info.json do nível
   python tools/production/decal_overrides.py           # frases do pavimento (main.decals.json)
   ```
   Os dois geradores aceitam `--check`, que confere o mod contra os arquivos do jogo sem gravar nada.
4. `texconv` (Microsoft DirectXTex) fica em `tools/conversion/bin/`, fora do Git (ver `docs/BEAMNG_OVERRIDE_POC.md`).

## Regras

- **Nunca alterar a instalação do BeamNG.** Tudo é override pelo mod.
- `source/originals/` e `source/reference_ptbr/` não são editados.
- Fluxo de cada textura: [`docs/WORKFLOW.md`](docs/WORKFLOW.md). Regras técnicas: [`docs/TEXTURE_GUIDELINES.md`](docs/TEXTURE_GUIDELINES.md). Regras de localização: [`docs/LOCALIZATION_RULES.md`](docs/LOCALIZATION_RULES.md).
- Validação antes de qualquer commit no mod: ver [`tools/validation/README.md`](tools/validation/README.md).

## Versionamento semântico

A partir da **1.0.0** o projeto segue o [SemVer](https://semver.org/lang/pt-BR/):

| Tipo | Exemplo | Quando |
|---|---|---|
| **PATCH** | 1.0.1 | correção sem mudança significativa de escopo (textura com erro, valor funcional errado, arquivo faltando) |
| **MINOR** | 1.1.0 | nova tradução ou recurso compatível (nova família de texturas, painel do posto, outro mapa como adição) |
| **MAJOR** | 2.0.0 | mudança grande de arquitetura ou de compatibilidade (nova versão do BeamNG que exige refazer os dados de nível, mudança de estrutura do pacote) |

**Uma versão publicada não muda.** O ZIP da 1.0.0 nunca é substituído por conteúdo diferente com o mesmo número; qualquer correção vira uma versão nova.

## Como fazer uma release

1. Atualize a versão em `mod/traducao_ptbr_wcusa/mod_info/traducao_ptbr_wcusa/info.json`, `tools/release/release_config.json` (versão e `zip_timestamp`), `CHANGELOG.md` e `README.md`.
2. Rode a suíte completa (comandos em `tests/reports/release/RC_VALIDATION.md`).
3. Faça o commit e rode `python tools/release/build_release.py`. O build recusa uma árvore com mudanças não commitadas.
4. Teste o ZIP real numa instalação limpa: a versão de desenvolvimento desativada e só o ZIP ativo. Confira a origem dos arquivos pelo VFS.
5. Registre o build em `docs/release/BUILD_<versão>.md`, faça o commit, rode o build de novo a partir desse commit e confira que o SHA-256 é o mesmo.
6. Crie a tag anotada `v<versão>`, faça o push de `main` e da tag (sem `--force`) e publique a GitHub Release com o ZIP e o `.sha256` anexados.
