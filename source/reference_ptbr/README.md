# Referências PT-BR (primeira tentativa de tradução)

**Estes arquivos são referências visuais da primeira tentativa de tradução. Eles não são masters tecnicamente aprovados.**

- Origem: pasta legada `Texturas de placas/<categoria>/PT-BR/`, arquivos gerados em 15 e 16/09/2026.
- Nome: `<nome_original>_ptbr.png`. Tirando o sufixo `_ptbr`, sobra o nome da textura original em `source/originals/`.
- Integridade: o SHA-256 de cada arquivo está em `docs/inventory/original_files_manifest.csv` (`classification = current_ptbr_reference`).

## Para que servem
- Consultar os textos já escolhidos.
- Consultar o estilo visual pretendido.
- Consultar a posição aproximada dos elementos.

## Para que NÃO servem
- Base de edição: a base é sempre o original (ver `docs/WORKFLOW.md`).
- Conversão direta para DDS.

## Problemas conhecidos (auditoria §4)
- Imagens regeneradas por inteiro (26–78% dos pixels alterados).
- Canal alfa perdido ou com ruído.
- Layout alterado em alguns atlas (por exemplo, `t_eca_genericsigns_b.color`).
- Mapas auxiliares (opacidade, emissivo, normal) não acompanham as mudanças.
- `t_sealbrik_logo_b.color_ptbr.png` é **cópia byte a byte** do original, sem tradução. Por isso fica **só localmente** (está no `.gitignore`), pela mesma regra que exclui os originais do jogo.

**Nunca sobrescreva nem edite estes arquivos.**
