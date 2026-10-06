# 6A — Marcações no pavimento (`t_decal_roadmarkings`)

**Data:** 05–06/10/2026 · **Status:** produção + QA no jogo (dia; PARE também à noite).

## Uso real no West Coast
Fonte: `levels/west_coast_usa/main.decals.json` (somente leitura), 1.388 decalques `decal_roadmarkings1`.
O decalque mostra **uma** célula da grade 4×4 (`managedDecalData.json`). As frases foram reconstruídas pelo eixo de leitura de cada instância. O "para cima" do texto é tangente × normal e a "direita" é −tangente; isso foi calibrado com os pares KEEP CLEAR.

| Frase original | Ocorrências | PT-BR |
|---|---:|---|
| STOP | 110 | PARE |
| KEEP CLEAR | 57 (56 lado a lado + 1 empilhado) | NÃO BLOQUEIE |
| EXIT (isolado) | 15 | SAÍDA |
| NO EXIT | 2 (lado a lado, 1,9 m) | SEM SAÍDA |
| BUS ONLY | 2 | ÔNIBUS (ONLY removido) |
| BUS STOP | 2 | ÔNIBUS (STOP removido) |
| ONLY + seta de faixa | 1 | seta apenas (ONLY removido) |
| EXIT ONLY (decalques de 0,9 m na face das barreiras dos portões das docas) | 3 | SÓ SAÍDA |
| ONLY isolado nas barreiras das docas | 4 | removido |
| LEFT / TURN | 0 | não produzidos (sem uso) |

## Decisão sobre ONLY
- Um único slot não concorda em gênero ("exclusivo/exclusiva") nem funciona na ordem brasileira. Por isso o **slot 5 passou a "SÓ"**.
- **EXIT ONLY:** em cada par, a instância da esquerda passou a mostrar o slot 5 (SÓ) e a da direita o slot 14 (SAÍDA). O resultado é "SÓ SAÍDA", só com troca de `rectIdx` por instância; os slots livres 10/11 não foram necessários.
- **Bus:** "BUS ONLY" e "BUS STOP" ficam só com **ÔNIBUS**. "ÔNIBUS SÓ" e "ÔNIBUS PARE" foram evitados.
- **Override estrutural:** `main.decals.json`, com 9 instâncias apagadas e 6 `rectIdx` trocados, identificadas por `uid` em `working/layered/t_decal_roadmarkings/decal_overrides.json`.
  - Gerado por `tools/production/decal_overrides.py`; é uma cópia do arquivo do jogo, por isso não é versionado.
  - Verificado por `validate.py new`: todo o resto é idêntico ao original.

## Mapas
O material `roadmarkings1` usa cor, opacidade, normal (BC5), AO, rugosidade e metálico.

| Mapa | Papel na letra | Fase 6 |
|---|---|---|
| `_o.data` | contorno + desgaste da tinta | refeito |
| `_b.color` | textura da tinta | refeito |
| `_nm.normal` | relevo da borda + rachaduras | refeito |
| `_ao.data` | contorno escuro + manchas | refeito |
| `_r.data`, `_m.data` | ruído independente da letra / preto | original |

**Duas cópias do atlas no jogo**, ambas sobrescritas porque o caminho legado do material é resolvido pelo nome:

| Caminho | Opacidade | AO |
|---|---|---|
| `assets/materials/decal/marking/m_decal_roadmarkings_01` | 512 | 2048 |
| `assets/materials/decalroad/lines/roadmarkings1` | 1024 | 512 |

Cada conjunto foi refeito a partir do seu próprio original (`source/originals/*/decalroad/` para a segunda cópia).

## Método (`working/layered/t_decal_roadmarkings/build_roadmarkings.py`)
Para cada célula e cada mapa, na resolução do mapa:
1. **Máscara antiga e perfil de borda:** a partir da opacidade original, calcula-se o perfil médio do mapa em função da distância à borda da letra. Na normal, a projeção é feita na direção da borda.
2. **Campo de tinta:** é a cópia do interior das letras originais, estendida por deslocamentos da própria textura. Não há síntese.
3. **Palavra nova:** renderizada com a Bahnschrift negrito condensada e recomposta como perfil(nova distância) + desvio de textura do campo de tinta. A opacidade é calculada como campo × cobertura.

O resultado é o mesmo contorno escuro de AO, o mesmo relevo de borda e o mesmo desgaste do original, nas letras novas.

## Validação
- PNG (8 mapas, 2 cópias): PASS, com 0 px fora dos 7 slots editados. As regiões estão em `allowed_regions.json` (fonte: `textureCoords`) e escalam por resolução.
- DDS: PASS. Formatos iguais aos originais: BC7 sRGB, BC4, BC5, BC4; mips iguais.
- Família: PASS. `shape_changed: true`, com opacidade, normal e AO entregues.
- `validate.py new`: o override do `main.decals.json` PASS.

## QA
Pontos `rm_*` em `tests/qa_locations.json`, capturas em `tests/screenshots/phase6/t_decal_roadmarkings/`. Há vista de cima (texto na orientação de leitura) e oblíqua de motorista.
- **Correção durante o QA:** "SEM SAÍDA" saiu colado na primeira versão, porque o SEM ocupava a largura total e invadia o vão de 1,9 m do par. O SEM foi limitado à extensão do NO original.
- **Oblíquas:** a primeira versão era distante demais, e o motor esmaece decalques pequenos na tela (`fadeStartPixelSize`).

## Revisão humana
- Alinhamento, ordem e recorte: OK.
- Tipografia (`human_typography_review_required`): a Bahnschrift condensada aproxima o estêncil original, mas sem as pontes. BLOQUEIE ficou muito condensado (8 letras na célula), como já era o caso de CLEAR.
- Os acentos (Ô, Ã, Í, Ó) reduzem a altura das maiúsculas dessas palavras.
