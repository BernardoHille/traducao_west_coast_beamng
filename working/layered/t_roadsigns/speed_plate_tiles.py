"""New tiles for the speed plates built into roadsigns.dae (Phase 7, speed signage coherence).

The 23 regulatory "SPEED LIMIT nn" plates and the 24 yellow advisory "nn MPH" plates of roadsigns.dae are assembled
from shared atlas cells (white/yellow board, SPEED LIMIT, MPH, the digit row also used by route shields, exits and
the toll plaza). As in Phase 6 (glyph_tiles.py), no shared cell is edited: each plate's BOARD quad is re-targeted to a
new tile in transparent atlas space that no game mesh samples, and its legend/digit quads to an empty transparent
cell, so the plate shows only the new face. Quads are selected one by one (uv_map "at": the quad centroid), never by
cell alone.

  regulatory -> copy of the original white bordered board with the R-19 disc of the approved master
                (working/layered/r19/build_r19.py, drawn in metres at the board's physical size, so the disc is round).
                The board keeps its rectangle: a galvanized back face sits 6 cm behind every plate (shared mesh), so
                a cut-out disc would show a grey rectangle around it. Value = working/functional/speed_plates.json.
  advisory   -> copy of the original yellow board with "nn" over "km/h" in black (same face as the R-19 numerals).

Writes speed_plate_tiles.json: {"elements": [...] (ops r19_plate / advisory_plate, read by build_t_roadsigns.py),
"uv_map": [...] (read by tools/production/glyph_rewrite.py)}.

    python working/layered/t_roadsigns/speed_plate_tiles.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
import glyph_signs as G  # noqa: E402

PLATES = json.loads((REPO / "working/functional/speed_plates.json").read_text(encoding="utf8"))["plates"]
GLYPH = json.loads((HERE / "glyph_tiles.json").read_text(encoding="utf8"))
DAE = REPO / "source/originals/meshes/roads/roadsigns.dae"
BOARD = {"regulatory": [370, 188, 517, 381], "advisory": [370, 383, 517, 530]}
M = 6
SCALE = 0.8   # tile texels per board texel: the free atlas space holds the 9 faces at 80 % (still ~120 px/m on the plate)

foot = np.load(REPO / "working/temporary/rs_footprint_all.npy")   # UV footprint of every game mesh using t_roadsigns
o0 = np.asarray(Image.open(REPO / "source/originals/png/t_roadsigns_o.data.png").convert("L")).astype(int)
free = (o0 < 8) & ~foot
taken = np.zeros_like(free)
for box in [e["box"] for e in GLYPH["elements"]] + [u["to"] for u in GLYPH["uv_map"]]:   # Phase 6 tiles
    x0, y0, x1, y1 = box
    taken[max(y0 - M, 0):y1 + M, max(x0 - M, 0):x1 + M] = True
I = np.pad(free.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)


def ok(x, y, w, h):
    return I[y + h, x + w] - I[y, x + w] - I[y + h, x] + I[y, x] == w * h


def place(w, h):
    W, H = w + 2 * M, h + 2 * M
    for y in range(0, 1024 - H, 2):
        for x in range(0, 2048 - W, 2):
            if ok(x, y, W, H) and not taken[y:y + H, x:x + W].any():
                taken[y:y + H, x:x + W] = True
                return x + M, y + M
    raise SystemExit(f"no free space for {w}x{h}")


def board_metres(kind):
    """Physical size of the board quad (m) from its texture frame (median over the plates of that kind)."""
    q = G.read_quads(DAE, "roadsigns", (2048, 1024))
    w, h = BOARD[kind][2] - BOARD[kind][0], BOARD[kind][3] - BOARD[kind][1]
    sizes = []
    for p in PLATES:
        if p["kind"] != kind:
            continue
        c = np.array(p["quads"]["board"][1])
        x = min(q, key=lambda y: np.linalg.norm(y["centroid"] - c))
        Mx = np.linalg.lstsq(np.c_[x["uv_px"][0], np.ones(3)], x["tris"][0], rcond=None)[0]
        sizes.append((np.linalg.norm(Mx[0]) * w, np.linalg.norm(Mx[1]) * h))
    s = np.median(np.array(sizes), axis=0)
    return [round(float(s[0]) / float(s[1]), 4), 1.0]   # aspect only: the drawing scales with the board


elements, uv_map = [], []
tile_of = {}
for kind, op, matrix in (("regulatory", "r19_plate", "roadsigns_speed_limit_tile"), ("advisory", "advisory_plate", "roadsigns_mph_tile")):
    bw, bh = round((BOARD[kind][2] - BOARD[kind][0]) * SCALE), round((BOARD[kind][3] - BOARD[kind][1]) * SCALE)
    panel = board_metres(kind)
    for v in sorted({p["value_kmh"] for p in PLATES if p["kind"] == kind}):
        x, y = place(bw, bh)
        eid = f"sp_{'r19' if kind == 'regulatory' else 'adv'}_{v}"
        elements.append({"id": eid, "matrix": matrix, "op": op, "box": [x, y, x + bw, y + bh], "board_from": BOARD[kind], "value": v,
                         "panel": panel, "uv_override": "UV of the PT-BR roadsigns.dae of the mod (board quads of the speed plates "
                                                        "re-targeted here); Phase 7 speed plates"})
        tile_of[(kind, v)] = [x, y, x + bw, y + bh]
bx, by = place(24, 24)
BLANK = [bx, by, bx + 24, by + 24]   # left transparent (original opacity 0): collapsed legend / digit quads
for p in PLATES:
    qd = p["quads"]
    uv_map.append({"id": f"{p['id']}_board", "from": qd["board"][0], "to": tile_of[(p["kind"], p["value_kmh"])], "at": [qd["board"][1]], "radius": 0.02})
    uv_map.append({"id": f"{p['id']}_legend", "from": qd["legend"][0], "to": BLANK, "at": [qd["legend"][1]], "radius": 0.02})
    for k, (r, c) in enumerate(qd["digits"]):
        uv_map.append({"id": f"{p['id']}_digit{k}", "from": r, "to": BLANK, "at": [c], "radius": 0.02})
json.dump({"_doc": __doc__, "elements": elements, "blank": BLANK, "uv_map": uv_map}, open(HERE / "speed_plate_tiles.json", "w", encoding="utf8"),
          indent=1, ensure_ascii=False)
for e in elements:
    print(e["id"], e["box"], e["panel"])
print("blank", BLANK, "uv_map", len(uv_map))
