# Status do projeto

**Última atualização:** 30/09/2026
**Fase atual:** Fase 0 — Preparação e versionamento (concluída)

## Ambiente

- BeamNG.drive **0.39.4.0** (Steam)
- Mapa principal: **West Coast USA** (`levels/west_coast_usa`)
- Idioma destino: **PT-BR**

## Estado atual

- **Originais extraídos:** 35 texturas, cada uma em DDS (formato do jogo) e PNG (base de edição). Ficam em `source/originals/`, só localmente, fora do Git.
- **Traduções existentes:** 13 PNG `_ptbr` em `source/reference_ptbr/`, que correspondem a 11 texturas traduzidas e 1 máscara. O `t_sealbrik_logo` `_ptbr` é cópia idêntica do original.
- **Status das traduções existentes:** servem **só de referência** até serem reconstruídas a partir dos originais. Não são masters aprovados.
- **DDS PT-BR:** nenhum produzido (`export/dds/` vazio).
- **Mod:** ainda não montado nem validado no jogo (`mod/traducao_ptbr_wcusa/` vazio).
- **Inventário:** `docs/inventory/original_files_manifest.csv` (SHA-256) e `docs/inventory/texture_families.md`.
- **Auditoria inicial:** `docs/AUDITORIA_PROJETO_TRADUCAO.md`, snapshot de 30/09/2026 que não deve ser editado.

## Pipeline

- [x] Auditoria inicial
- [x] Estrutura do projeto
- [x] Versionamento
- [ ] Proof of Concept do override
- [ ] Regras definitivas de localização
- [ ] Validador
- [ ] Reconstrução das traduções existentes
- [ ] Tradução das texturas pendentes
- [ ] QA West Coast
- [ ] QA East Coast / Utah
- [ ] QA ADAS
- [ ] Release

## Problemas conhecidos

Resumo da auditoria (detalhes em `docs/AUDITORIA_PROJETO_TRADUCAO.md`). **Nenhum foi resolvido ainda.**

| # | Problema | Referência |
|---|---|---|
| 1 | **Perda de alfa** em PNG PT-BR (`eca_roadsigns_d`, `t_billboardsigns_dealers_b`, `t_sponsors_b`, `t_spearleaf_refinery_logo_b`, `t_movie_studio_signage_b`) e ruído no alfa de todos os PNG PT-BR | Auditoria §4.3 |
| 2 | **Imagens regeneradas:** entre 26% e 78% dos pixels mudaram fora das áreas de texto, com risco de desalinhar a UV | Auditoria §4.2 |
| 3 | **Road markings incompletos:** só o `_b.color` foi traduzido. `_o.data`, `_nm`, `_ao`, `_r` e `_m` continuam com as letras em inglês | Auditoria §4.1 |
| 4 | **Emissivos incompatíveis:** `eca_genericsigns_emissive` não acompanha o novo layout | Auditoria §4.4 |
| 5 | **Formatos DDS diferentes** entre texturas (BC7 sRGB, BC7 linear, BC4, DXT1, DXT5). Não dá para exportar tudo como BC7 | Auditoria §4.5 |
| 6 | **Assets globais afetam outros mapas:** a maioria fica em `assets/materials/` e é usada também por East Coast, Utah etc. | Auditoria §3 |
| 7 | **Política mph/km/h pendente:** placas PT-BR mostram km/h com números em mph | Auditoria §5.2 |
| 8 | Mapas auxiliares **não citados na auditoria** (`eca_genericsigns` `_o/_nm/_ao/_r`, `steel_factory_brand` `_nm/_ao/_r`, `billboardsigns_dealers` `_o`…) | `docs/inventory/texture_families.md` |
| 9 | A auditoria diz "41 texturas", mas são **35** | `docs/inventory/texture_families.md` |

## Decisões pendentes

- **DECISÃO PENDENTE — política de velocidade mph/km/h.** O jogo, o tráfego e as missões ADAS continuam em mph. Opções na auditoria §5.2.
- **DECISÃO PENDENTE — política de conversão $ → R$.** Preços como "4.99-" e "$400" estão inconsistentes entre as referências.
- **DECISÃO PENDENTE — política definitiva para assets globais.** Aceitar que o mod traduza também outros mapas, ou limitar ao West Coast com materiais próprios.
- **DECISÃO PENDENTE — estratégia para mapas auxiliares não extraídos** (quais extrair e quando).
