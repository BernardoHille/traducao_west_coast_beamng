# 6G — Placas globais restantes

**Data:** 06/10/2026 · **Status:** classificação com evidência; nada a produzir para o West Coast.

O critério é o mesmo das demais famílias. Uma textura só é produzida quando algum **mesh instanciado no West Coast** usa um material que a referencia.

O índice `tools/production/asset_usage.py` resolve essa cadeia:
1. varre os `*.materials.json` de todos os zips do jogo;
2. levanta os `.dae` que usam esses materiais;
3. conta as instâncias desses `.dae` no nível, incluindo TSStatic, prefabs e forest items.

Resultado completo em `working/temporary/usage_6g.json` (gerado, fora do Git).

| Família / textura | Material | Meshes que usam o material | Instâncias no West Coast | Classificação |
|---|---|---|---|---|
| `eca_roadsigns_d` | `signs_usa` | 33 | **0** | `not_used_wcusa`: placas do East Coast |
| `ut_roadsigns_d` | nenhum material do jogo referencia o arquivo | 0 | **0** | `not_used_wcusa` |
| `speed_sign` | `speed_sign_mat` | 0 | **0** | `not_used_wcusa` |
| `arrows_sign_d` | `sign_arrows` | 3 | **0** | `not_used_wcusa` |
| `checkpoint_sign` | `checkpoint_sign` | 8 | **0** | `not_used_wcusa` |
| `usa_roadsigns_text` | `intro_text`, `usa_roadsigns_text` | 58 | **0** | `not_used_wcusa` |
| `usa_roadsigns_turn_warning` | `usa_roadsigns_turn_warn` | 1 | **0** | `not_used_wcusa` |
| `t_sign_drift.color` | `m_sign_drift` | 1 (`s_sign_drift.dae`) | **14** | `preserve_original`: "DRIFT" é o nome da modalidade, usado assim no Brasil |

## Consequências
- Nenhum DDS dessas famílias entra no mod. As regras de tradução da matriz (`eca_*`, `ut_*`) continuam válidas para um eventual pacote de outros mapas, mas ficam **fora do escopo** do West Coast e não contam como pendência da Fase 6.
- As placas de trânsito que o West Coast **usa** estão no atlas `t_roadsigns` (Fase 5), com placas R-19 próprias.
- Os tiles de `t_roadsigns` ainda abertos na matriz são de dois tipos, ambos registrados em `docs/production/phase5/`:
  - **não amostrados** pelo mapa: TUNNEL, ROAD CLOSED, NO U TURN, nomes de rua do Utah e a câmera de velocidade;
  - **dependentes de recomposição de mesh**: MILES/frações e o tile SPEED LIMIT.
- Velocidades, radares e zonas são dados funcionais da **Fase 7** e não foram tocados.

## Verificação
- `python tools/production/asset_usage.py arrows_sign_d checkpoint_sign eca_roadsigns_d speed_sign t_sign_drift.color usa_roadsigns_text usa_roadsigns_turn_warning ut_roadsigns_d`: 0 instâncias para todas, exceto `t_sign_drift`.
- A matriz (`LOCALIZATION_MASTER.csv`) recebeu a nota da Fase 6 (6G) em cada linha dessas famílias.
