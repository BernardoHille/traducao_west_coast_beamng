# Notas de metodologia: Fase 5.5 (artigo técnico)

## Snapshot do projeto documentado

| Item | Valor |
|---|---|
| Commit documentado | `70329b1bbea173e72edd421eb74b6542d82df862` (`docs: fix phase 5 element counts`) |
| Branch | `main` |
| Remoto no momento da redação | `origin/main` = `02560049329becfc2e94abcc4a7b3d9da9ecee6f` (Fase 4), conferido por `git ls-remote` em 02/10/2026. Os 6 commits da Fase 5 estavam só no repositório local |
| Data | 02/10/2026 |
| BeamNG.drive | 0.39.4.0 (Steam), Direct3D 12 |
| Mod | `traducao_ptbr_wcusa` 0.5.0, instalado em `current/mods/unpacked/` como cópia de `mod/traducao_ptbr_wcusa/` |
| Estado do mod ao final | **ativo**, cópia instalada idêntica ao repositório (`validate.py mod --installed`: PASS 48/48, executado depois da restauração do estado PoC) |
| Estado máximo documentado | Fase 5 concluída (local). A Fase 6 **não** foi iniciada |

## Verificação do estado real antes de escrever

1. `git status`, `git log --oneline --decorate -15`, `git remote -v`, `git branch --show-current` e `git ls-remote origin main`: árvore limpa, 6 commits à frente do remoto.
2. Leitura de `PROJECT_STATUS.md`, dos documentos listados na especificação da fase e de todos os documentos posteriores à Fase 4 (`docs/production/*`, `tests/reports/phase5_*`, `r19_mesh_validation.md`).
3. Reexecução das verificações (02/10/2026):
   - `python -m unittest discover -s tools/validation/tests`: 44 OK;
   - `python tools/validation/validate.py all`: self-test 75, regressão 10, mod 48, velocidade 13 FAIL / 9 PASS / 1 WARN / 7 SKIP (snapshot salvo do navgraph);
   - `python tools/validation/validate.py new`: 24/24 PASS;
   - `validate.py texture` sobre a referência antiga e sobre o atlas da Fase 5, para regenerar os heatmaps.

   Os relatórios rastreados em `export/reports/validation/` só mudaram no carimbo de data e foram restaurados com `git checkout`. Os relatórios da referência antiga, que não são rastreados, foram removidos depois de consultados.
4. Os números da matriz foram contados a partir do CSV de cada commit (`git show <commit>:docs/localization/LOCALIZATION_MASTER.csv`).

## Capturas

**Ferramentas:**
- `docs/article/tools/capture_article.py`, que usa `tools/beamng/qa_runner.py` e `mcp_client.py`;
- servidor MCP `beamng-game` (`http://127.0.0.1:29292/mcp`).

**Estados:**

| Estado | Como foi obtido | Capturas |
|---|---|---|
| `original` | `deactivateMod`; carga de `smallgrid` → `west_coast_usa` | 9 (a 10ª tentativa, lateral, foi feita no estado ptbr e descartada) |
| `poc` | Na **cópia instalada** do mod, e não no repositório: `t_roadsigns_b.color.dds` substituído por `export/dds/poc/t_roadsigns_b.color.dds` e `t_roadsigns_o.data.dds` removido, reproduzindo a Fase 1; `smallgrid` → `west_coast_usa`. Ao final, `install_mod.py` restaurou a cópia (2 arquivos recopiados) | 2 |
| `ptbr` | Mod ativo, cópia idêntica ao commit `70329b1`; `smallgrid` → `west_coast_usa` | 7 + 1 extra (vista de cima) |

**Preset:** `tests/presets/day.json`, que inclui `windSpeed 0`, `cloudCover 0` e sol fixado em 40,66° no `ScatterSky`. Interface oculta.

**Resolução:** 1920 × 993 (tamanho da janela; o MCP não aceita resolução).

**Incidente:** na primeira tentativa a janela do jogo estava minimizada e o screenshot não foi gravado. A janela foi restaurada sem receber foco (`ShowWindow`, `SW_SHOWNOACTIVATE`) e a captura foi refeita. Nenhuma configuração do jogo foi alterada.

**Captura descartada:** `qa_context_side` (câmera dentro de um prédio). O arquivo foi apagado e o registro ficou em `figures/raw/capture_log.json`.

**Anotação:** as posições de objetos nas figuras anotadas foram **medidas no jogo**:
1. uma esfera de depuração magenta (`debug_draw`) foi desenhada na coordenada do mapa;
2. foi feita uma captura de calibração, que não foi guardada;
3. os pixels magenta foram localizados.

Para a vista aérea, o modelo de câmera pinhole com **FOV vertical** de 50° reproduziu as 5 esferas visíveis com erro ≤ 6 px. Os valores estão em `docs/article/tools/annotation_points.json`.

## Reversibilidade

- Nenhum arquivo do repositório foi alterado para reproduzir o PoC. A troca foi feita só na cópia instalada e desfeita por `install_mod.py`.
- `validate.py mod --installed` após a restauração: PASS 48/48 (cópia instalada idêntica).
- `git status` após as capturas e validações: só `docs/article/` novo e, ao final, `docs/PROJECT_STATUS.md` alterado.
- A instalação do jogo (`steamapps/common/BeamNG.drive`) não foi tocada. Zips do jogo foram lidos só por leitura: `main.decals.json` e `managedDecalData.json`.

## Ferramentas

| Ferramenta | Uso |
|---|---|
| Python 3.11, Pillow, NumPy | composição e anotação de figuras, contagens |
| MCP do BeamNG | carga de mapa, câmera, captura, `file_info`, `debug_draw`, Lua |
| `tools/validation/validate.py` | métricas e heatmaps |
| SVG escrito à mão (em `build_figures.py`) | diagramas |
| `docs/article/tools/md_to_html.py` | HTML a partir do Markdown (conversor mínimo próprio; nenhum pacote instalado) |
| Microsoft Edge (`--headless --print-to-pdf`) | PDF a partir do HTML (navegador já instalado) |

## O que não foi feito nesta fase

- Nenhuma textura nova foi traduzida.
- Nenhuma família nova foi iniciada.
- Road markings, postos, outdoors, ônibus, radares e ADAS não foram alterados.
- A Fase 6 não foi iniciada.
