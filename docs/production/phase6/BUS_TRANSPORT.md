# 6E — Transporte público

**Data:** 06/10/2026 · **Status:** mapa de linhas produzido, validado e com QA no jogo (dia e noite); rótulo MAP → MAPA refeito na malha do abrigo (6I).

## Mapa de linhas (`t_bus_routes_wca`, material `m_bus_routes_wca`)
**Uso:**
- abrigos `s_busstop_wcu` (31 instâncias) e `s_busstop_wcu_04` (9), cobertura UV 1,0;
- o material resolve para `assets/materials/billboard_label/m_bus_routes_wca/`;
- atlas 512 × 512.

**Mapas:**
- **cor:** BC7 sRGB, 10 mips;
- **normal:** BC5, 10 mips. O normal map **gravava o relevo de cada rótulo** e foi refeito para o texto novo (regra `gradient_normal`: amplitude do relevo antigo por mínimos quadrados, aplicada ao gradiente do texto novo, ganho 1,7);
- AO e rugosidade não têm texto e ficam como no original.

| Item | Original | PT-BR |
|---|---|---|
| Título | BELASCO CITY - TRANSPORT NETWORK | BELASCO — REDE DE TRANSPORTE |
| Legenda | BUS LINES | LINHAS DE ÔNIBUS |
| Nomes das linhas | Belasco Boulevard, Convention St., Central Hospital… | Avenida Belasco, Rua da Convenção, Hospital Central, Centro de Convenções, Rua Fjord |
| Paradas (23) | Fjord Street, Logan Park, Station, Stock Market, Dockyards, Motorsports Park, Agave Lookout… | Rua Fjord, Parque Logan, Estação, Bolsa de Valores, Docas, Autódromo, Mirante Agave… |

- **Nomes próprios preservados** (`LOCALIZATION_RULES` §4): Little China, Royal Bank, Snoots News, Star Diner, Riverway Plaza, Lens Flare Studios, Horizon Estates, Platin Gate, Single Pine, Redwood. Nos dois últimos, o tipo do negócio foi traduzido: Pousada Single Pine e Pousada Redwood.
- **Rótulos girados:** os nomes que acompanham as linhas no mapa foram medidos por PCA da legenda e redesenhados no mesmo ângulo.

**Validação:**
- PNG cor: PASS, 30 regiões, 0 px fora;
- PNG normal: PASS, 30 regiões, 0 px fora;
- DDS: PASS. Família: PASS (`shape_changed: true`, normal entregue).

**QA:** `bus_map_shelter` (abrigo `s_busstop_wcu`), dia e noite. O título e a legenda aparecem em PT-BR, sem resto do texto antigo. Capturas em `tests/screenshots/phase6/t_bus_routes_wca/`; 0 problemas de VFS.

## O que não foi alterado
| Asset | Motivo |
|---|---|
| `t_bus_routes_utah` (Canyonlands) | Cobertura UV 0 no West Coast: o mapa é do Utah |
| `t_sign_busstop`, atlas `busstop` | Pictograma de ônibus e colunas *lorem ipsum*: sem texto em inglês |

## Rótulo MAP do abrigo (6I)
"MAP" é feito de 3 quads do mesh `s_busstop_wcu` / `_04` apontando para glifos de `t_billboardsigns_dealers`. Nos dois meshes (31 + 9 instâncias), as duas faces foram reescritas para **MAPA**, com 4 quads e o mesmo alfabeto. INFO já é português. QA: `gl_s_busstop_wcu_mapa`, `gl_s_busstop_wcu_04_mapa`. Ver `GLYPH_SIGNS.md`.
