# Fluxo de trabalho por textura

Toda textura traduzida passa por este fluxo. Nenhuma etapa pode ser pulada.

```
ORIGINAL DO JOGO
      ↓
IDENTIFICAR MATERIAL E MAPAS ASSOCIADOS
      ↓
COPIAR PARA WORKING
      ↓
EDITAR SOMENTE ÁREAS NECESSÁRIAS
      ↓
PRESERVAR UV / ALFA / RESOLUÇÃO
      ↓
VALIDAR
      ↓
CONVERTER PARA DDS NO FORMATO ORIGINAL
      ↓
VALIDAR DDS
      ↓
COLOCAR NA ÁRVORE DO MOD
      ↓
TESTAR NO BEAMNG
      ↓
SCREENSHOT / QA
      ↓
APROVAR
      ↓
COMMIT
```

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
| 6. Validar PNG | Resolução, alfa e diferença de pixels fora das áreas de texto (≈0) | `export/reports/` |
| 7. Converter | PNG → DDS no **mesmo formato do original**, com cadeia completa de mipmaps | `tools/conversion/` → `export/dds/` |
| 8. Validar DDS | Formato, sRGB/linear, número de mipmaps, dimensões | `export/reports/` |
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
