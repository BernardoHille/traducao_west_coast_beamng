# Build 1.0.0

```
Version:              1.0.0
Commit:               896fa36914d95aa07dc4c58190634853e906603c (build validated in the game)
Tag:                  v1.0.0 → the commit that adds this record (docs only; same mod tree, same ZIP bytes)
ZIP:                  traducao_ptbr_wcusa_v1.0.0.zip
Size:                 29,846,362 bytes (uncompressed content: 98,973,556 bytes)
SHA-256:              684bcf6c2e93c9397fa1acc667dd37792d2e55b05973c32bc1a1bd33396e3b57
Files:                117 (31 DDS · 32 DAE · 32 CDAE · 1 materials · 20 level/gameplay JSON · 1 mod_info)
BeamNG compatibility: BeamNG.drive 0.39.4.0
Build date:           2026-10-21
```

## Arquivos

| Arquivo | Onde |
|---|---|
| `traducao_ptbr_wcusa_v1.0.0.zip` | `release/output/` (fora do Git) e anexo da GitHub Release `v1.0.0` |
| `traducao_ptbr_wcusa_v1.0.0.sha256` | `release/output/` (versionado) e anexo da release |
| `traducao_ptbr_wcusa_v1.0.0_manifest.txt` | `release/output/`: caminho, tamanho e SHA-256 de cada arquivo |
| `traducao_ptbr_wcusa_v1.0.0_build.json` | `release/output/`: registro do build |

## Como reproduzir

Requisitos: um clone com Git LFS, Python 3.11+ com Pillow/NumPy e uma instalação do **BeamNG.drive 0.39.4.0**. Ela é necessária para gerar os dados de nível, que não ficam no Git (ver `CONTRIBUTING.md`).

```
git checkout v1.0.0
python tools/production/apply_phase7_functional.py
python tools/production/decal_overrides.py
python tools/release/build_release.py
```

O resultado deve ter o mesmo SHA-256. O conteúdo do ZIP não depende do commit, da data do build nem das datas dos arquivos em disco. As datas dentro do ZIP são fixas (`tools/release/release_config.json`), as entradas vão ordenadas e as permissões são fixas.

## Verificação feita

- Três builds deram o mesmo SHA-256: um em `ac2ddf6` e dois em `896fa36`. Os dois commits têm a mesma árvore do mod; o segundo só corrige o script de build.
- Depois de criar a tag, o build foi refeito a partir do commit marcado e deu o mesmo SHA-256 (ver o relatório final da Fase 9).
- O ZIP foi testado no jogo como instalação limpa: [`tests/reports/release/RC_VALIDATION.md`](../../tests/reports/release/RC_VALIDATION.md).
