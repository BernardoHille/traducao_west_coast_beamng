# Notas de metodologia — artigo final (v1.0.0)

## Snapshot documentado

| Item | Valor |
|---|---|
| Tag | `v1.0.0` → `b4a745082ef76fd511342b1f15ad88856f92b5dc` |
| Branch | `main`, igual a `origin/main` (`git ls-remote`, 21/10/2026) |
| Estado do Git ao iniciar | árvore limpa; `git describe --tags` = `v1.0.0` |
| Pacote | `traducao_ptbr_wcusa_v1.0.0.zip`, SHA-256 `684bcf6c2e93c9397fa1acc667dd37792d2e55b05973c32bc1a1bd33396e3b57` |
| GitHub Release | não encontrada na API pública em 21/10/2026 (`releases/tags/v1.0.0` → 404). O SHA documentado é o do ZIP gerado pelo build reprodutível |
| BeamNG.drive | 0.39.4.0 (Steam) |
| Data | 21/10/2026 |

Esta edição não alterou o mod, a tag, o ZIP nem nenhum arquivo de runtime. Os únicos arquivos novos estão em `docs/article_final/`. Fora dela, só `docs/PROJECT_STATUS.md` (registro do artigo) e uma errata em `tests/reports/release/RC_VALIDATION.md` (seção "Erratas" abaixo) foram alterados.

## Verificação antes de escrever

1. `git status`, `git log --oneline --decorate -30`, `git branch --show-current`, `git remote -v`, `git describe --tags --always`, `git fetch --tags` e `git ls-remote origin main refs/tags/v1.0.0`.
2. Leitura de `PROJECT_STATUS.md`, `release/FINAL_PROJECT_STATUS.md`, `BUILD_1.0.0.md`, `RC_VALIDATION.md`, `KNOWN_ISSUES.md`, `SCOPE_AUDIT.md`, dos documentos das Fases 5 a 8 (`docs/production/`), da primeira edição inteira (`docs/article/`) e dos relatórios da Fase 7 (`tests/reports/phase7/`).
3. Números reconferidos na fonte primária, e não copiados de resumos:
   - matriz contada no CSV da tag;
   - DDS lidos com `dds_parser`;
   - capturas e pontos de QA contados nos diretórios e no catálogo;
   - navgraph exportado do jogo duas vezes;
   - malhas contadas em `mod/`;
   - quadriláteros do motel lidos da malha.

   As discordâncias encontradas estão em `DATA_SUMMARY_FINAL.md` §9.

## Capturas novas

**Ambiente:** só o ZIP de release instalado, igual ao procedimento do teste de instalação limpa da Fase 9.
1. A cópia de desenvolvimento (`mods/unpacked/traducao_ptbr_wcusa`) foi retirada da pasta `mods` e guardada fora da pasta do jogo.
2. `traducao_ptbr_wcusa_v1.0.0.zip` foi copiado para `mods/`, com o SHA-256 da cópia conferido.
3. O script recusa rodar se a cópia de desenvolvimento estiver registrada no gerenciador de mods.
4. Ao final, o ZIP foi retirado, a cópia de desenvolvimento devolvida e `validate.py mod --installed` deu cópia instalada idêntica ao repositório. O cache não tinha nenhum `.cdae` do pacote.

Outros mods ativos na máquina (veículo `hcity7`, mapa `gniar_br_costa_oeste`, mods de pesquisa ADAS) não têm nenhum arquivo nos caminhos do pacote (conferido na Fase 9).

**Ferramenta:** `docs/article_final/tools/capture_final.py`. Ela usa `tools/beamng/qa_runner.py` com o nome de mod do ZIP e as mesmas poses customizadas da primeira edição (`decal_stop_chinatown_oblique`, `aerial_downtown`, `decal_bus_only_top`, `decal_keep_clear_top`), mais poses de catálogo e duas poses novas na altura do motorista. Cada troca de estado passa pelo `smallgrid`. Cada captura registra pose, mods ativos e a origem VFS de `t_roadsigns_b.color.dds` e de `main.decals.json` (`figures/raw/capture_log.json`).

**Estados:** `on` (ZIP ativo) e `off` (ZIP desativado). Presets `day` e `night` de `tests/presets/`; vento 0, céu limpo, sol fixado no `ScatterSky`; interface oculta.

**Incidentes:**
- A primeira tentativa esgotou os 30 s de espera do utilitário de captura. Uma captura isolada feita logo depois levou 22 s para ser gravada, com o jogo em segundo plano. O script passou a esperar até 120 s. Nenhuma configuração do jogo foi alterada.
- A pose `chinatown_street` ficou com a placa fora do quadro. Ela foi mantida no `raw/` (imutável) e não foi usada. Duas poses na altura do motorista foram testadas para a abertura, e a `chinatown_driver_a` foi escolhida.
- A captura diurna dessa pose está gravada como `__on_opening.png`, porque o plano que a gerou usava o preset diurno com esse rótulo.

**Navgraph:** `capture_final.py navgraph on|off` exportou todas as arestas (posição dos nós, limite em km/h, dirigibilidade, nomes) com o ZIP ativo e desativado. A comparação foi feita pela geometria (extremos arredondados a 1 m), porque os nomes automáticos dos nós mudam entre cargas.

## Enquadramento comum entre 1920 × 1080 e 1920 × 993

As capturas da primeira edição e das Fases 5 e 6 têm 1920 × 993; as de 21/10/2026, 1920 × 1080 (tamanho da janela do jogo, que o MCP não controla). As câmeras usam FOV **vertical** fixo, como medido na primeira edição. Por isso, a mesma pose cobre o mesmo ângulo vertical nos dois tamanhos e só o ângulo horizontal difere.

O gerador de figuras leva as duas ao mesmo campo de visão, 1765 × 993:
- a de 1080 é reduzida por 993/1080;
- a de 993 é recortada no centro.

Nas Figuras 8, 13 e 18, a coincidência de placas, faixas e prédios entre colunas confirma o procedimento.

## Figuras

- **Gerador:** `docs/article_final/tools/build_figures_final.py`. Faz recortes, composição lado a lado, rótulos e setas (Pillow); gráficos a partir de dados (SVG escrito à mão, ou PIL no mapa do navgraph); renders offline de malha com `tools/production/glyph_signs.py`. Sem edição generativa e sem retoque de pixel.
- **`raw/`** nunca é alterado. As anotações são feitas em cópias.
- **Figuras reutilizadas da primeira edição** são copiadas sem mudança, com a procedência em `FIGURE_INDEX_FINAL.md`.
- **Revisão visual:** cada figura foi inspecionada em folhas de contato e, nos SVG, renderizada pelo Edge em modo headless. Correções feitas:
  - o recorte do R-19 (disco fora do quadro e texels não quadrados);
  - títulos cortados;
  - textos que vazavam de caixas em três diagramas;
  - a legenda do gráfico de radares sobreposta ao eixo;
  - a série "mod" do gráfico do validador, que misturava `mod` e `mod --installed`;
  - a Fase 2 com "0 capturas" (são 8);
  - a figura de ADAS (ver "Erratas").

## Texto, HTML e PDF

- **Markdown:** `ARTIGO_TECNICO_FINAL_PTBR.md`.
- **HTML:** `tools/md_to_html_final.py`, adaptado do conversor mínimo da primeira edição. Acrescenta capa, sumário navegável e quebras de página de impressão. O conversor da primeira edição não foi alterado.
- **PDF:** Microsoft Edge (`--headless --print-to-pdf`), o mesmo método da primeira edição.
- **Revisão:** as páginas do PDF foram renderizadas em imagem e inspecionadas, procurando quebras, tabelas, figuras cortadas e páginas em branco.

## Erratas registradas nesta edição

1. **Capturas de ADAS do teste de release.** `tests/reports/release/RC_VALIDATION.md` cita `tests/screenshots/release/on/adas/speed_alert_*.jpg`. Inspecionadas agora, essas duas imagens mostram o menu principal do jogo sobre a cena.
   - O resultado funcional daquele teste não depende delas: veio dos contadores do controlador do cenário (`release_smoke.json`).
   - O artigo usa as capturas da Fase 7 e uma captura nova da placa R-19 50 feita com o ZIP.
   - A errata foi acrescentada ao relatório, sem mudar nenhum resultado, nenhum arquivo de runtime nem a tag.

## O que não foi feito

- Nenhum asset, malha, dado de nível ou arquivo de runtime foi alterado.
- A tag `v1.0.0` e o ZIP não foram tocados nem refeitos.
- A primeira edição (`docs/article/`) não foi alterada.
- A instalação do jogo não foi tocada.
