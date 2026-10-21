# Retrato pré-release

Estado do mod **antes** de qualquer mudança de metadados da Fase 9, em 21/10/2026.

| Item | Valor |
|---|---|
| Commit | `1973cdb` (`main` = `origin/main`), árvore limpa |
| Versão do mod (`info.json`) | 0.7.0 |
| BeamNG.drive de referência | 0.39.4.0 (`integrity.json` da instalação) |
| Pasta | `mod/traducao_ptbr_wcusa/` |
| Arquivos | **117** |
| Tamanho total | **98.973.589 bytes** (94,4 MiB) |
| Arquivos versionados no Git | 97 |
| Arquivos gerados localmente (fora do Git) | 20, regenerados da instalação do jogo por `apply_phase7_functional.py` / `decal_overrides.py` |

## Por tipo

| Tipo | Quantidade | Substituem arquivo do jogo | Novos |
|---|---:|---:|---:|
| Texturas DDS | 31 | 25 | 6 (R-19 10/40/50/70/120 e a opacidade comum) |
| Malhas `.dae` | 32 | 28 | 4 (R-19 10/50/70/120) |
| Malhas compiladas `.cdae` | 32 | 28 | 4 |
| Materiais (`*.materials.json`) | 1 | 0 | 1 (`roadsigns_ptbr/main.materials.json`) |
| Dados de nível/gameplay (JSON) | 20 | 19 | 1 (grupo `ptbr_functional_signs`) |
| Metadado (`mod_info/.../info.json`) | 1 | — | — |
| **Total** | **117** | **100** | **16** |

- **Cópias idênticas a arquivos do jogo:** 0. Cada arquivo foi comparado por SHA-256 com o arquivo do jogo no mesmo caminho virtual (zips de `content/` e `gameplay/` solto da instalação).
- **Scripts/runtime:** nenhum. O mod não tem Lua, flowgraph nem JavaScript; ele só substitui e acrescenta dados (texturas, malhas, materiais e JSON de nível).
- **Dependências:** nenhuma. Os mods de pesquisa (ADAS, Event 01, Reaction Test) são pastas separadas no `mods/unpacked` e nenhum arquivo deles está aqui.

## Verificações feitas neste retrato

- `validate_mod_tree`: 123 verificações, 0 FAIL.
- `apply_phase7_functional.py --check`: 132 linhas alteradas / 132 declaradas, 15 objetos adicionados / 15 declarados.
- `decal_overrides.py --check`: OK (9 removidas, 6 `rectIdx` trocados).
- Varredura de texto (54 arquivos JSON/DAE): sem caminhos locais, nomes de usuário, e-mails ou segredos. O único nome próprio é o autor no `info.json`.

A classificação arquivo a arquivo está em [`SCOPE_AUDIT.md`](SCOPE_AUDIT.md).
