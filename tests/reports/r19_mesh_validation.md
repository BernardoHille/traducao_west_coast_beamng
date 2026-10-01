# Validação estrutural dos meshes R-19 (Fase 5)

**Ferramenta:** `tools/production/r19_mesh.py compare` (também executada por `validate.py new`). **Originais:** extraídos só por leitura de `content/levels/west_coast_usa.zip` para `source/originals/meshes/objects/` (fora do Git). **Data:** 30/09/2026.

## Resultado

A única mudança necessária foi **material e UV**. Geometria, normais, cores de vértice, listas de triângulos, transformações dos nós (pivot, posição, escala, orientação) e bounding box são idênticos byte a byte (comparação por SHA-256 dos arrays).

### `sign_speed25.dae` → R-19 40 km/h

| Verificação | Original | Mod | Igual |
|---|---|---|---|
| geometries | `1` | `1` | ✔ |
| triangles_total | `10` | `10` | ✔ |
| vertices | `20` | `20` | ✔ |
| bbox_min | `[-0.396981, -0.002485, -0.5]` | `[-0.396981, -0.002485, -0.5]` | ✔ |
| bbox_max | `[0.36584, 0.011354, 0.5]` | `[0.36584, 0.011354, 0.5]` | ✔ |
| bbox_used_min | `[-0.396981, -0.002485, -0.5]` | `[-0.396981, -0.002485, -0.5]` | ✔ |
| bbox_used_max | `[0.36584, 0.011354, 0.5]` | `[0.36584, 0.011354, 0.5]` | ✔ |
| nodes | `"4 nós (base00, start01, sign_speed25_a015, nulldetail10)"` | `"4 nós (base00, start01, sign_speed25_a015, nulldetail10)"` | ✔ |
| positions_sha | `"3d5bb547c381cd12"` | `"3d5bb547c381cd12"` | ✔ |
| normals_sha | `"5a17ff8b41e44705"` | `"5a17ff8b41e44705"` | ✔ |
| colors_sha | `"7f04acae01d08ecc"` | `"7f04acae01d08ecc"` | ✔ |
| p_lists_sha | `"b55a8811d5f311e0"` | `"b55a8811d5f311e0"` | ✔ |
| triangles_per_material | `{"roadsigns": 8, "metal_galvanized": 2}` | `{"roadsigns_ptbr_r19_40": 8, "roadsigns_ptbr_r19_back": 2}` | alterado (esperado) |
| materials | `["metal_galvanized", "roadsigns"]` | `["roadsigns_ptbr_r19_40", "roadsigns_ptbr_r19_back"]` | alterado (esperado) |

### `sign_speed5.dae` → R-19 10 km/h

| Verificação | Original | Mod | Igual |
|---|---|---|---|
| geometries | `1` | `1` | ✔ |
| triangles_total | `8` | `8` | ✔ |
| vertices | `16` | `16` | ✔ |
| bbox_min | `[-0.36584, -0.002485, -0.5]` | `[-0.36584, -0.002485, -0.5]` | ✔ |
| bbox_max | `[0.36584, 0.010507, 0.5]` | `[0.36584, 0.010507, 0.5]` | ✔ |
| bbox_used_min | `[-0.36584, -0.002485, -0.5]` | `[-0.36584, -0.002485, -0.5]` | ✔ |
| bbox_used_max | `[0.36584, 0.010507, 0.5]` | `[0.36584, 0.010507, 0.5]` | ✔ |
| nodes | `"6 nós (base00, start01, sign_speed5_a015, nulldetail10, Camera, Light)"` | `"6 nós (base00, start01, sign_speed5_a015, nulldetail10, Camera, Light)"` | ✔ |
| positions_sha | `"156fb6a2dbfb5672"` | `"156fb6a2dbfb5672"` | ✔ |
| normals_sha | `"5a17ff8b41e44705"` | `"5a17ff8b41e44705"` | ✔ |
| colors_sha | `"e9bf53c48fc9ec26"` | `"e9bf53c48fc9ec26"` | ✔ |
| p_lists_sha | `"e21f0c3af64ac48a"` | `"e21f0c3af64ac48a"` | ✔ |
| triangles_per_material | `{"roadsigns": 6, "metal_galvanized": 2}` | `{"roadsigns_ptbr_r19_10": 6, "roadsigns_ptbr_r19_back": 2}` | alterado (esperado) |
| materials | `["metal_galvanized", "roadsigns"]` | `["roadsigns_ptbr_r19_10", "roadsigns_ptbr_r19_back"]` | alterado (esperado) |

## O que mudou e por quê

| Parte | Antes | Depois | Motivo |
|---|---|---|---|
| Painel frontal (quad 0,7317 × 1,0 m) | `roadsigns`, UV no painel branco do atlas (370–516 × 189–381) | `roadsigns_ptbr_r19_<v>`, UV 0–1 sobre o painel inteiro | textura própria; o disco é recortado pela opacidade (alphaTest 128) |
| Quads sobrepostos (tile SPEED LIMIT e glifos "2"/"5") | `roadsigns`, UV nos glifos compartilhados | mesmo material do R-19, UV num texel transparente (canto da textura) | ficam **invisíveis**, mas continuam no mesh: topologia, contagem de triângulos e bounding box preservadas (o "2" do 25 se estende 3 cm além do painel) |
| Verso (quad galvanizado) | `metal_galvanized` (**doubleSided**) | `roadsigns_ptbr_r19_back` (mapas do galvanizado + a mesma máscara do disco) | o verso duplo-face apareceria **pela frente**, nos cantos transparentes do disco; agora também é um disco |

**Orientação da UV:** o painel branco original é simétrico, e a UV dele estava girada 180° sem efeito visível. A orientação foi tirada dos quads de texto (SPEED LIMIT/algarismos), que aparecem corretos no jogo: mapa afim por triângulo, votação de sinal (du/dx = +1, dv/dz = +1). Foi conferida no render offline (`render_signs.py`) e no jogo (R-19 legível, não espelhado).

**Colisão:** os meshes não têm nós de colisão (`Collision*`/`LOS*`), nem no original nem no mod.

**Material próprio:** nenhum material do jogo foi redefinido. `roadsigns` e `metal_galvanized` continuam intactos para todas as outras placas.

## `.cdae` compilado no mod

Ao carregar um `.dae` mais novo que o `.cdae` do zip, o jogo recompila e grava o resultado no **cache temporário do usuário** (`current/temp/levels/.../sign_speed*.cdae`). Esse cache **sobrevive à desativação do mod**: no teste, com o mod desligado, as placas continuaram usando o shape R-19 com materiais que já não existiam. Por isso o mod distribui o `.cdae` gerado pelo próprio motor a partir do `.dae` do mod, com data mais nova que a do `.dae`. Assim o jogo não recompila e não grava nada fora do mod.
- `install_mod.py` re-carimba a data (o Git não preserva datas).
- `validate.py new` recusa `.cdae` ausente ou mais velho que o `.dae`.
- Os dois `.cdae` gravados em `temp` durante o teste foram removidos (eram cache gerado por este teste).

## Instâncias

O caminho virtual do mesh é o mesmo, então as **11** instâncias de `sign_speed25.dae` e as **37** de `sign_speed5.dae` passaram a usar os materiais R-19 sem editar nenhum TSStatic. Isso foi confirmado no jogo com `TSStatic:getMaterialNames()` → `roadsigns_ptbr_r19_40/10, roadsigns_ptbr_r19_back` (48/48).
