# Fluxo de trabalho por textura

Toda textura traduzida passa por este fluxo. Nenhuma etapa pode ser pulada.

```
ORIGINAL DO JOGO (SHA-256 conferido)
      ↓
IDENTIFICAR MATERIAL E MAPAS ASSOCIADOS
      ↓
REGISTRAR REGIÃO AUTORIZADA (config/allowed_regions.json)
      ↓
COPIAR PARA WORKING
      ↓
EDITAR
      ↓
VALIDATE PNG ............ validate.py texture <png>
      ↓
CONVERTER
      ↓
VALIDATE DDS ............ validate.py dds <dds>
      ↓
VALIDATE FAMILY ......... validate.py family <família> --source dir --dir <pacote> --shape-changed true|false
      ↓
MONTAR MOD
      ↓
VALIDATE MOD TREE ....... validate.py mod --installed
      ↓
QA MCP .................. tools/beamng/qa_runner.py capture …
      ↓
APROVAR (humano)
      ↓
COMMIT
```

Para assets funcionais (placas R-19, meshes, limites de via, radares, zonas, ADAS):

```
IMPLEMENTAR PLACA / MESH / LIMITE
      ↓
VALIDATE SPEED CONSISTENCY ... validate.py speeds --refresh   (mapa carregado no BeamNG)
      ↓
QA MCP
```

Um passo só avança com **zero FAIL** (`exit code 0`). WARN exige justificativa no relatório de QA. Antes de um commit de produção: `python tools/validation/validate.py all` e `python -m unittest discover -s tools/validation/tests`.

## Regra de base

> **Nunca usar automaticamente a versão PT-BR antiga como base da nova textura.**
> **A base é sempre o original** (`source/originals/png/`, conferido com o SHA-256 do manifesto).

Os arquivos em `source/reference_ptbr/` servem só de consulta: texto escolhido, estilo pretendido e posição aproximada. A auditoria mostrou que eles foram regenerados, perderam alfa e mudaram de layout.

## Etapas em detalhe

| Etapa | O que fazer | Onde |
|---|---|---|
| 1. Original do jogo | Confirmar que o original local bate com o SHA-256 em `docs/inventory/original_files_manifest.csv` | `source/originals/` (imutável) |
| 2. Material e mapas | Achar o material que usa a textura e todos os mapas da família (opacidade, emissivo, normal, AO, rugosidade, metálico). Extrair do jogo, **só lendo**, os mapas que faltam | `docs/inventory/texture_families.md` |
| 3. Copiar para working | Copiar o original para um master em camadas. O original nunca é editado diretamente | `working/layered/` |
| 4. Editar | Só as regiões com texto. Nada de reposicionar, redimensionar ou regenerar o resto | `working/layered/` |
| 5. Preservar | Mesma resolução, mesmas coordenadas UV, canal alfa do original (ou da máscara refeita) | — |
| 6. Validar PNG | `validate.py texture`: resolução, alfa (perda e ruído), mudanças fora das regiões autorizadas (≈0) | `export/reports/validation/` |
| 7. Converter | PNG → DDS no **mesmo formato do original**, com cadeia completa de mipmaps | `tools/conversion/` → `export/dds/` |
| 8. Validar DDS | `validate.py dds` e `validate.py family`: formato, sRGB/linear, mipmaps, dimensões, mapas auxiliares | `export/reports/validation/` |
| 9. Árvore do mod | Copiar para o caminho virtual exato do jogo, com o nome original (sem `_ptbr`) | `mod/traducao_ptbr_wcusa/` |
| 10. Testar | Carregar o West Coast, conferir de dia e de noite. Se a textura for global, conferir também outros mapas | BeamNG |
| 11. Screenshot / QA | Capturas antes/depois e relatório | `tests/screenshots/`, `tests/reports/` |
| 12. Aprovar | Revisão humana | — |
| 13. Commit | Uma família por commit, sempre que possível | Git |

## O que nunca fazer

- Editar ou sobrescrever arquivos em `source/originals/` ou `source/reference_ptbr/`.
- Alterar arquivos dentro da instalação do BeamNG ou dos seus `.zip`.
- Converter em lote sem validação individual.
- Apagar arquivos antigos sem autorização explícita.
