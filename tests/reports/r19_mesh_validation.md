# Validação estrutural dos meshes R-19 (Fase 5)

**Ferramenta:** `tools/production/r19_mesh.py compare`, também executada por `validate.py new`.
**Originais:** extraídos só por leitura de `content/levels/west_coast_usa.zip` para `source/originals/meshes/objects/`, fora do Git.
**Data:** 30/09/2026.

## Resultado

A única mudança necessária foi **material e UV**. Ficam idênticos byte a byte (comparação por SHA-256 dos arrays):
- geometria, normais e cores de vértice;
- listas de triângulos;
- transformações dos nós: pivot, posição, escala e orientação;
- bounding box.

| Mesh no mod | Origem | Instâncias que o usam | Como |
|---|---|---|---|
| `levels/.../objects/sign_speed25.dae` → R-19 **40** | `sign_speed25.dae` | 11 (todas são placas de 25 mph) | **mesmo caminho virtual**: nenhum TSStatic editado |
| `levels/.../objects/roadsigns_ptbr/sign_r19_10.dae` → R-19 **10** | `sign_speed5.dae` | 7 placas reais de 5 mph | **mesh novo** + `shapeName` trocado só nesses 7 TSStatic (`working/speed/sign_instances.json`) |

### Por que o 10 não substitui `sign_speed5.dae` no mesmo caminho

O nível tem **37** instâncias de `sign_speed5.dae`, mas **30** delas, no grupo `port/portNumbersSigns`, não são placas.
- São decalques de malha (`"decalType":"Visible Mesh Final"`, deitados a 90°) que formam a **placa cinza de fundo dos números das baias** ("01", "24"…) nas paredes dos armazéns do porto.
- No teste da substituição no mesmo caminho, essas placas viraram discos R-19 escuros (`tests/screenshots/phase5/roadsigns_ptbr_r19/port_bay_plate_side_effect_original_vs_inplace_override.jpg`).
- Por isso, seguindo o §22 ("não alterar os objetos individualmente **se não for necessário**"), aqui foi necessário: o mesh original fica intacto, as placas das baias voltam a ser idênticas ao original (`…after_fix_original_vs_mod.jpg`) e só as 7 placas reais apontam para o mesh R-19 10.

### `sign_speed25.dae` → `sign_speed25.dae` (R-19 40 km/h)

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

### `sign_speed5.dae` → `roadsigns_ptbr/sign_r19_10.dae` (R-19 10 km/h)

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
| Quads sobrepostos (tile SPEED LIMIT e glifos "2"/"5") | `roadsigns`, UV nos glifos compartilhados | mesmo material do R-19, UV num texel transparente | ficam **invisíveis** mas continuam no mesh: topologia, contagem de triângulos e bounding box preservadas (o "2" do 25 passa 3 cm do painel) |
| Verso (quad galvanizado) | `metal_galvanized` (**doubleSided**) | `roadsigns_ptbr_r19_back` (mapas do galvanizado + a mesma máscara do disco) | o verso duplo-face apareceria **pela frente** nos cantos transparentes do disco; agora também é um disco |

**Orientação da UV:** o painel branco original é simétrico, e a UV dele estava girada 180° sem efeito visível. A orientação foi tirada dos quads de texto (mapa afim por triângulo, voto de sinal: du/dx = +1, dv/dz = +1). Foi conferida no render offline e no jogo: R-19 legível, não espelhado, de dia e de noite.

**Colisão:** os meshes não têm nós de colisão, nem no original nem no mod.
**Materiais do jogo:** `roadsigns` e `metal_galvanized` não foram redefinidos.

## `.cdae` compilado no mod

Ao carregar um `.dae` mais novo que o `.cdae` do zip, o jogo recompila e grava o resultado no cache do usuário (`current/temp/levels/.../*.cdae`). Esse cache **sobrevive à desativação do mod**: na primeira sessão de teste, com o mod desligado, as 48 placas continuaram com o shape R-19.

Por isso o mod distribui o `.cdae` gerado pelo próprio motor, com data mais nova que a do `.dae`:
- `install_mod.py` re-carimba a data, porque o Git não preserva datas;
- `validate.py new` recusa `.cdae` ausente ou mais velho que o `.dae`;
- os `.dae` estão como `-text` no `.gitattributes`, para continuarem byte a byte iguais aos que geraram o `.cdae`.

**Prova (sessão nova, 30/09 21:25):**
1. Carga a frio com o mod desligado: originais, sem `.cdae` em `temp`.
2. Mod ligado (troca via outro mapa): 11 + 7 placas R-19, sem nenhum `.cdae` novo em `temp`.
3. Mod desligado de novo: `roadsigns` original nas 11, nenhuma instância R-19.

## Instâncias (confirmado no jogo, `TSStatic:getMaterialNames()`)

| Shape | Instâncias | Materiais com o mod |
|---|---:|---|
| `sign_speed25.dae` | 11 | `roadsigns_ptbr_r19_40, roadsigns_ptbr_r19_back` |
| `roadsigns_ptbr/sign_r19_10.dae` | 7 | `roadsigns_ptbr_r19_10, roadsigns_ptbr_r19_back` |
| `sign_speed5.dae` (placas das baias do porto) | 30 | `roadsigns, metal_galvanized` (inalterado) |
