"""New word tiles for the gantry / lane-use plates of roadsigns.dae (Phase 6, glyph signs).

ONLY, CARPOOLS ONLY / 2 OR MORE PERSONS / PER VEHICLE, the fractions 1/4 1/2 3/4 and MILES are opacity cut-out
words of t_roadsigns whose atlas cells are SHARED with other signs (the toll booth builds DO NOT STOP from the
O/N of ONLY, the no-parking sign uses the P of CARPOOLS). They are therefore not edited in place: each word
gets a new tile of the same size in transparent atlas space that no mesh of the game samples, and the quads of
roadsigns.dae (mod copy) are re-targeted to it (tools/production/glyph_rewrite.py, custom "uv_map").

Distances (LOCALIZATION_RULES, distances): 1/4 mi = 0,4 km -> "400 m"; 1/2 mi -> "800 m"; 3/4 mi -> "1,2 km".
The unit goes into the fraction tile, so the MILES quads are mapped to an empty transparent cell.

Writes glyph_tiles.json: {"elements": [...] (op glyph, read by build_t_roadsigns.py), "uv_map": [...]}."""
import json
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[2]
foot = np.load(REPO / "working/temporary/rs_footprint_all.npy")
o0 = np.asarray(Image.open(REPO / "source/originals/png/t_roadsigns_o.data.png").convert("L")).astype(int)
free = (o0 < 8) & ~foot
M = 6
BLACK, WHITE = [28, 28, 28], [240, 240, 240]
B = {"wght": 650, "wdth": 90, "min_wdth": 65}


def lines_two(w, h, a, b, big=0.46, small=0.30):
    """Two centred lines: number (big) over unit (small)."""
    ca, cb = big * h, small * h
    gap = (h - ca - cb) / 3
    return [{"text": a, "box": [3, round(gap), w - 3, round(gap + ca)]},
            {"text": b, "box": [3, round(2 * gap + ca), w - 3, round(2 * gap + ca + cb)]}]


T = [  # (id, matrix, source rects, lines(w, h) relative to the tile, letter colour, style)
 ("rs_only", "roadsigns_only", [(352, 141, 440, 185), (354, 144, 439, 185)],
  lambda w, h: [{"text": "SOMENTE", "box": [3, round(0.22 * h), w - 3, round(0.78 * h)]}], BLACK, B),
 ("rs_carpools_1", "roadsigns_carpools", [(1409, 0, 1699, 44)],
  lambda w, h: [{"text": "FAIXA EXCLUSIVA", "box": [6, 10, w - 8, h - 9]}], BLACK, B),
 ("rs_carpools_2", "roadsigns_carpools", [(1417, 41, 1706, 84)],
  lambda w, h: [{"text": "2", "box": [8, 6, 34, h - 6]}, {"text": "OU MAIS OCUPANTES", "box": [46, 13, w - 10, h - 12]}], BLACK, B),
 ("rs_per_vehicle", "roadsigns_per_vehicle", [(685, 72, 876, 116)],
  lambda w, h: [{"text": "POR VEÍCULO", "box": [22, 13, w - 22, h - 11]}], BLACK, B),
 ("rs_frac_quarter", "roadsigns_fractions_miles", [(343, 85, 395, 138)], lambda w, h: lines_two(w, h, "400", "m"), WHITE, B),
 ("rs_frac_half", "roadsigns_fractions_miles", [(398, 84, 459, 143), (405, 85, 457, 138)], lambda w, h: lines_two(w, h, "800", "m"), WHITE, B),
 ("rs_frac_3q", "roadsigns_fractions_miles", [(453, 86, 520, 141), (461, 85, 513, 138)], lambda w, h: lines_two(w, h, "1,2", "km"), WHITE, B),
]
I = np.pad(free.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
ok = lambda x, y, w, h: I[y + h, x + w] - I[y, x + w] - I[y + h, x] + I[y, x] == w * h
taken = np.zeros_like(free)


def place(w, h):
    W, H = w + 2 * M, h + 2 * M
    for y in range(0, 1024 - H, 2):
        for x in range(1400, 2048 - W, 2):
            if ok(x, y, W, H) and not taken[y:y + H, x:x + W].any():
                taken[y:y + H, x:x + W] = True
                return x + M, y + M
    raise SystemExit(f"no free space for {w}x{h}")


elements, uv_map = [], []
for tid, matrix, srcs, mk, col, style in T:
    for k, (x0, y0, x1, y1) in enumerate(srcs):
        w, h = x1 - x0, y1 - y0
        nx, ny = place(w, h)
        lines = [{"text": l["text"], "box": [nx + l["box"][0], ny + l["box"][1], nx + l["box"][2], ny + l["box"][3]]} for l in mk(w, h)]
        eid = tid if len(srcs) == 1 else f"{tid}_{k}"
        elements.append({"id": eid, "matrix": matrix, "op": "glyph", "box": [nx, ny, nx + w, ny + h], "style": style,
                         "letters_from": [x0, y0, x1, y1], "letter_rgb": col, "lines": lines,
                         "uv_override": "UV of the PT-BR roadsigns.dae of the mod (quads re-targeted from "
                                        f"[{x0}, {y0}, {x1}, {y1}]); Phase 6 glyph signs"})
        uv_map.append({"from": [x0, y0, x1, y1], "to": [nx, ny, nx + w, ny + h], "id": eid})
# MILES: unit moved into the fraction tiles -> quads point at an empty transparent cell
for src in [(638, 118, 754, 151), (641, 116, 779, 153)]:
    w, h = src[2] - src[0], src[3] - src[1]
    nx, ny = place(w, h)
    uv_map.append({"from": list(src), "to": [nx, ny, nx + w, ny + h], "id": "rs_miles_blank"})
json.dump({"_doc": __doc__, "elements": elements, "uv_map": uv_map}, open(HERE / "glyph_tiles.json", "w", encoding="utf8"),
          indent=1, ensure_ascii=False)
for e in uv_map:
    print(e["id"], e["from"], "->", e["to"])
