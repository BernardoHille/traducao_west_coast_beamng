"""layout.json (assets copy) + layout_jungle_rock_island.json (copy at the legacy path the material names)
for ind_industrial_signs (Phase 6, 6D). Boxes in atlas pixels (1024x512)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
B = {"font": "bahnschrift", "wght": 700, "wdth": 85, "min_wdth": 70}
E = [  # id, matrix, erase box, text, style, legend, colour
 ("flam_hdr", "ind_flammable_no_smoking", [392, 18, 507, 39], "INFLAMÁVEL", B, "white", [245, 240, 235]),
 ("flam_no", "ind_flammable_no_smoking", [448, 55, 494, 78], "PROIBIDO", B, "red", None),
 ("flam_smoking", "ind_flammable_no_smoking", [392, 91, 508, 116], "FUMAR", B, "red", None),
 ("exit", "ind_exit", [516, 196, 636, 252], "SAÍDA", dict(B, wght=800, wdth=75), "red", None),
 ("ext_hdr", "ind_fire_extinguisher", [647, 134, 764, 156], "Extintor", {"font": "arial_bold"}, "white", [245, 240, 235]),
 ("ext_co2", "ind_fire_extinguisher", [667, 163, 708, 179], "DIÓXIDO DE\nCARBONO", {"font": "arial_bold"}, "dark", [30, 30, 30]),
 ("think", "ind_think_safe", [774, 131, 890, 146], "PENSE EM SEGURANÇA", B, "dark", [60, 60, 60]),
 ("nosmoke_hdr", "ind_extinguish", [260, 318, 382, 338], "PROIBIDO FUMAR", B, "white", [245, 240, 235]),
 ("nosmoke_body", "ind_extinguish", [261, 346, 381, 371], "Apague o cigarro\nantes de entrar.", {"font": "segoe"}, "red", None),
 ("toxic", "ind_toxic", [645, 313, 699, 377], "PRODUTOS\nQUÍMICOS\nTÓXICOS EM\nUSO NESTE\nLOCAL · FDS\nDISPONÍVEIS", dict(B, wdth=75), "dark", [25, 25, 25]),
 ("emergency", "ind_emergency_exit", [420, 457, 507, 476], "Saída de emergência", {"font": "arial_bold"}, "white", [240, 245, 240]),
 ("trespass", "ind_no_trespassing", [903, 392, 1020, 511], "ENTRADA\nPROIBIDA", dict(B, wght=800, wdth=75), {"rgbs": [[235, 225, 220], [205, 190, 185], [180, 165, 160], [165, 155, 150], [150, 150, 130]], "tol": 28}, [236, 228, 222]),
 ("danger_small", "ind_caution_generic", [197, 462, 251, 488], "Perigo", {"font": "arial_bold"}, "dark", [25, 25, 25]),
]
BLOCK = {"exit": [520, 207, 632, 250], "trespass": [906, 398, 1016, 500]}  # room for the accent of SAÍDA inside the panel


def make(variant=""):
    els = []
    for i, m, box, text, st, leg, col in E:
        x0, y0, x1, y1 = box
        e = {"id": i, "matrix": m, "op": "panel", "box": [x0 - 1, y0 - 1, x1 + 1, y1 + 1], "legend": leg, "bg_tol": 30,
             "erase": [box], "erase_dilate": 2, "no_grow": True, "style": dict(st),
             "blocks": [{"box": BLOCK.get(i, [x0 + 2, y0 + 2, x1 - 2, y1 - 2]), "text": text, "max_lines": text.count("\n") + 1, "leading": 1.3}]}
        if col:
            e["color"] = col
        els.append(e)
    sub = variant + "/" if variant else ""
    return {"family": "ind_industrial_signs",
            "_doc": "Industrial safety signs (Phase 6, 6D). Material industrial_signs names /levels/jungle_rock_island/.../ind_industrial_signs_d.color.png; that legacy path exists in jungle_rock_island.zip with a near-identical copy, and the same name exists in assets/materials/billboard_label/industrial_signs. Both copies are overridden, each rebuilt from its own original. Only signs sampled by instanced West Coast meshes are edited (SPEED LIMIT 15, Texas Waste, MAX HEADROOM… are not used in the map).",
            "maps": {"color": {"original": f"source/originals/png/{sub}ind_industrial_signs_d.color.png", "out": f"working/png/{sub}ind_industrial_signs_d.color.png"}},
            "materials": ["industrial_signs"], "usage_texture": "ind_industrial_signs_d.color", "uv_min_coverage": 0.4, "seed": 20261006, "elements": els}
json.dump(make(), open(HERE / "layout.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(make("jungle_rock_island"), open(HERE / "layout_jungle_rock_island.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
