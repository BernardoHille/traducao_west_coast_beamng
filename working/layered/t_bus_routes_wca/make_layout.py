"""Bus network map of Belasco (t_bus_routes_wca, Phase 6 6E): title, legend and stop names.
Names follow LOCALIZATION_RULES section 4 (street type before the proper name; places/businesses preserved:
Little China, Royal Bank, Snoots News, Star Diner, Riverway Plaza, Lens Flare Studios). Atlas 512x512."""
import json
from pathlib import Path
F = {"font": "bahnschrift", "wght": 600, "wdth": 85, "min_wdth": 70}
GREY = {"rgbs": [[80, 80, 80], [105, 105, 105], [125, 125, 125]], "tol": 38}
INK = [78, 78, 80]
els = []


def flat(i, box, text, legend=GREY, color=INK, style=F, align="center", erase=None):
    x0, y0, x1, y1 = box
    els.append({"id": i, "op": "panel", "box": [x0 - 2, y0 - 2, x1 + 2, y1 + 2], "legend": legend, "erase": [erase or [x0 - 1, y0 - 1, x1 + 1, y1 + 1]],
                "erase_dilate": 1, "no_grow": True, "bg_tol": 22, "color": color, "style": dict(style, align=align),
                "lines": [{"text": text, "box": [x0, y0, x1, y1]}]})


def rot(i, cx, cy, ln, deg, text, cap=4, new_len=None):
    L = new_len or ln  # squeezed into the original label length (longer PT-BR names must not cross the route lines)
    els.append({"id": i, "op": "panel", "box": [max(0, int(cx - 40)), max(0, int(cy - 40)), int(cx + 40), int(cy + 40)], "legend": GREY,
                "erase_rot": [[cx, cy, ln + 2, cap + 4, deg]], "erase_dilate": 1, "no_grow": True, "bg_tol": 60, "color": INK,
                "style": dict(F), "rotate": {"deg": deg, "pivot": [cx, cy]},
                "lines": [{"text": text, "box": [int(round(cx - L / 2)), int(round(cy - cap / 2)), int(round(cx + L / 2)), int(round(cy - cap / 2)) + cap]}]})


# title and legend panel
flat("title", [10, 10, 266, 21], "BELASCO — REDE DE TRANSPORTE", legend={"rgbs": [[40, 40, 40], [70, 70, 70]], "tol": 45},
     color=[38, 38, 40], style=dict(F, wght=700, wdth=90), align="left", erase=[8, 7, 270, 24])
flat("bus_lines", [391, 127, 464, 134], "LINHAS DE ÔNIBUS", legend={"rgbs": [[40, 40, 40], [70, 70, 70]], "tol": 45},
     color=[40, 40, 42], style=dict(F, wght=700), erase=[400, 124, 456, 137])
for i, box, text, col in [("leg2b", [408, 176, 460, 180], "Avenida Belasco", [225, 205, 30]),
                          ("leg3b", [408, 196, 460, 200], "Rua da Convenção", [228, 140, 40]),
                          ("leg4a", [408, 207, 456, 211], "Hospital Central", [215, 40, 40]),
                          ("leg4b", [408, 216, 462, 220], "Centro de Convenções", [215, 40, 40]),
                          ("leg5b", [408, 236, 444, 240], "Rua Fjord", [45, 70, 225])]:
    flat(i, [box[0], box[1] - 1, box[2], box[3]], text, legend={"rgb": col, "tol": 70}, color=col,
         style=dict(F, wght=800, stroke={"px": 0.7, "color": [60, 50, 40]}), align="left", erase=[box[0] - 1, box[1] - 2, box[2] + 4, box[3] + 3])
# horizontal stop names
flat("belasco_boulevard", [52, 25, 98, 30], "Avenida Belasco")
flat("fjord_street", [48, 52, 78, 56], "Rua Fjord", align="left", erase=[47, 50, 83, 58])
flat("logan_park", [31, 80, 62, 84], "Parque Logan", align="left")
flat("convention_center", [155, 74, 205, 79], "Centro de Convenções", align="left")
flat("belasco_pier", [199, 100, 228, 105], "Píer Belasco", align="left")
flat("platin_gate", [258, 49, 305, 54], "Ponte Platin Gate", align="right")
flat("canal_st", [268, 145, 290, 149], "Rua do Canal", align="left")
flat("tennis", [266, 208, 322, 212], "Clube de Tênis/Basquete", align="left")
flat("harlem_st", [84, 260, 108, 265], "Rua Harlem", align="left")
flat("single_pine", [424, 493, 467, 497], "Pousada Single Pine", align="right")
# rotated stop names: centre, original length, angle (counter-clockwise, reading direction)
rot("station", 120, 82, 17, 42, "Estação")
rot("stock_market", 83.5, 134.4, 32, -47, "Bolsa de Valores")
rot("clinton_hotel", 105.6, 129, 31, -39, "Hotel Clinton")
rot("central_hospital", 208.8, 158, 42, -44, "Hospital Central")
rot("church_st", 37.5, 162.5, 25, -45, "Rua da Igreja")
rot("winchester_rd", 91.3, 187, 33, 46.5, "Rua Winchester")
rot("cloverfield_ln", 46, 217, 33, -46.5, "Rua Cloverfield")
rot("dockyards", 258, 107.5, 26, 42, "Docas")
rot("n_horizon", 130, 366.6, 42, 44, "Horizon Estates Norte")
rot("redwood_motel", 122, 467, 40, 44, "Pousada Redwood")
rot("e_horizon", 163.8, 493, 40, 41, "Horizon Estates Leste")
rot("motorsports_park", 380.4, 309.4, 43, 43, "Autódromo")
rot("agave_lookout", 409.8, 422.3, 36, 45, "Mirante Agave")
for e in els:  # the normal map embosses every printed label -> relief moved with the text (compose.py edge_profile)
    e["aux"] = {"nm": "gradient_normal"}
    e["relief_px"] = 2
    e["relief_gain"] = 1.7  # anti-aliased new letters have a softer gradient than the binary old mask
    e["matrix"] = "bus_title" if e["id"] == "title" else ("bus_legend" if e["id"] == "bus_lines" else ("bus_line_names" if e["id"].startswith("leg") else "bus_stops"))
lay = {"family": "t_bus_routes_wca", "_doc": __doc__,
       "maps": {"color": {"original": "source/originals/png/t_bus_routes_wca_b.color.png", "out": "working/png/t_bus_routes_wca_b.color.png"},
                "nm": {"original": "source/originals/png/t_bus_routes_wca_nm.normal.png", "out": "working/png/t_bus_routes_wca_nm.normal.png"}},
       "region_maps": ["color", "nm"],
       "materials": ["m_bus_routes_wca"], "usage_texture": "t_bus_routes_wca_b.color", "uv_min_coverage": 0.4, "seed": 20261006, "elements": els}
json.dump(lay, open(Path(__file__).with_name("layout.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(els))
