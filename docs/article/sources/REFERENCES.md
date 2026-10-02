# Referências

O artigo separa três tipos de fonte:
- **Normativas:** padrão brasileiro de sinalização.
- **Técnicas externas:** documentação oficial de formatos e ferramentas.
- **Internas:** documentos e relatórios deste repositório, que registram as descobertas experimentais.

Afirmações sobre o comportamento do BeamNG.drive são **observações deste projeto** na versão 0.39.4.0. Não foi usada documentação oficial do BeamNG para elas.

## 1. Normativas (Brasil)

As páginas citadas são páginas do **arquivo PDF**, conforme registrado em `docs/LOCALIZATION_RULES.md` §1.

| Ref. | Documento | Páginas usadas | URL |
|---|---|---|---|
| MBST-I | SENATRAN/CONTRAN. *Manual Brasileiro de Sinalização de Trânsito, Vol. I: Sinalização Vertical de Regulamentação* (edição atual) | p.13 (§4.3.1 informação complementar), p.15 (cores R-1/R-2), p.35 (múltiplos de 10), p.36 (Tabela 1), p.154 (diagramação R-2), p.178 (R-15) | https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/docs/copy_of___01___MBST_Vol._I___Sin._Vert._Regulamentacao_F.pdf |
| MBST-I/2005 | Mesmo volume, edição aprovada pela Resolução CONTRAN nº 180/2005 | p.45 (inscrição "DÊ A PREFERÊNCIA" no pavimento), p.46–47 (múltiplos de 10; Tabela 1), p.193 (diagramação R-19) | https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/educacao/publicacoes/manual_vol_i_2.pdf |
| MBST-IV | SENATRAN/CONTRAN. *MBST, Vol. IV: Sinalização Horizontal* (2022) | p.118 (§8.3 legendas), p.123 (legenda PARE) | https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/docs/copy_of___04___MBST_Vol._IV___Sinalizacao_Horizontal.pdf |
| Índice | SENATRAN. *Manuais Brasileiros de Sinalização de Trânsito* (Vol. I–IX) | — | https://www.gov.br/transportes/pt-br/assuntos/transito/senatran/manuais-brasileiros-de-sinalizacao-de-transito |

## 2. Técnicas externas

| Ref. | Documento | Uso no artigo | URL (conferida em 02/10/2026) |
|---|---|---|---|
| MS-BC | Microsoft. *Texture Block Compression in Direct3D 11*. Microsoft Learn | Tabela de BC1/BC3/BC4/BC7: canais, alfa, bytes por bloco 4×4, variantes `_SRGB` | https://learn.microsoft.com/en-us/windows/win32/direct3d11/texture-block-compression-in-direct3d-11 |
| MS-TEXCONV | Microsoft. *Texconv* (DirectXTex wiki) | Significado das opções `-f`, `-m 0`, `-srgb`, `-dx10` usadas na conversão | https://github.com/microsoft/DirectXTex/wiki/Texconv |
| DirectXTex | Microsoft. DirectXTex, release `may2026` (texconv 2026.5.8.1), com digest SHA-256 e assinatura Authenticode verificados na Fase 1 | Ferramenta de conversão PNG → DDS | https://github.com/microsoft/DirectXTex/releases |

## 3. Internas (este repositório, commit `70329b1`)

| Documento | Fase | Conteúdo |
|---|---|---|
| `docs/AUDITORIA_PROJETO_TRADUCAO.md` | 0 | Auditoria inicial (*snapshot* de 30/09/2026) |
| `docs/inventory/original_files_manifest.csv` | 0 | 35 DDS + 35 PNG originais com SHA-256, formatos e papéis |
| `docs/inventory/texture_families.md` | 0/3 | Famílias, mapas auxiliares, correção 41 → 35 |
| `docs/BEAMNG_OVERRIDE_POC.md`, `tests/reports/poc_override_log.md` | 1 | PoC do *override* (ON/OFF/ON) |
| `docs/BEAMNG_MCP_CAPABILITIES.md`, `tools/beamng/QA_PROTOCOL.md` | 2/5 | Capacidades do MCP e protocolo de QA |
| `tests/reports/t_roadsigns_automation_test.md` | 2 | Automação e reprodutibilidade |
| `docs/LOCALIZATION_RULES.md` | 3 | Regras de localização (fonte de verdade) |
| `docs/localization/LOCALIZATION_MASTER.csv` | 3–5 | Matriz de 308 entradas |
| `docs/localization/legacy_translation_review.md` | 3 | Revisão das traduções antigas (160 itens) |
| `docs/localization/cultural_adaptations.md`, `GLOSSARY_PTBR.md`, `traffic_signs.csv` | 3 | Adaptações, glossário, placas |
| `docs/inventory/speed_limits.md`, `speed_dependencies.md` | 3/5 | Velocidades e dependências funcionais |
| `tools/validation/README.md`, `tests/reports/validation_baseline.md` | 4 | Validador e linha de base |
| `docs/production/PHASE5_ROADSIGNS.md`, `t_roadsigns_plan.md`, `slotTraffic_update.md` | 5 | Produção definitiva |
| `tests/reports/r19_mesh_validation.md`, `phase5_speed_delta.md`, `phase5_navgraph_check.json`, `phase5_ai_test.json` | 5 | Relatórios da Fase 5 |
