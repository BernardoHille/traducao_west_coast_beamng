"""Accent cells for the glyph-built signs (Phase 6): packed into transparent atlas space that no mesh samples.

Free space = opacity < 8 in the original AND outside the UV footprint of every mesh of the game that uses the
material clutter_commercial (245 meshes, all zips; working/temporary/cc_footprint_all.npy from asset_usage +
dae_uv). Writes accents.json (cells + placement metrics for glyph_rewrite.py; read by the clutter layout)."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[2]
o = np.asarray(Image.open(REPO / "source/originals/png/art_shapes/clutter_commercial_o.data.png").convert("L")).astype(int)
foot = np.load(REPO / "working/temporary/cc_footprint_all.npy")
free = (o < 8) & ~foot
M = 5  # margin (mip bleed)
# font metrics measured on the original (ink top/bottom of the caps, stem width)
A = {  # key: (w, h, stroke, style, ink_top, ink_bottom)
 "H:cedil": (16, 22, 6, {"fill": [180, 180, 180], "edge": [38, 38, 38], "edge_px": 2}, 396, 447),
 "R0:tilde": (16, 6, 2.4, {"fill": [254, 254, 254], "edge": [139, 139, 139], "edge_px": 1}, 9, 33),
 "R0:circ": (15, 6, 2.4, {"fill": [254, 254, 254], "edge": [139, 139, 139], "edge_px": 1}, 9, 33),
 "R1:acute": (12, 11, 4.5, {"fill": [255, 255, 255]}, 46, 70),
 "R1:cedil": (10, 13, 4, {"fill": [255, 255, 255]}, 46, 70),
 "R1:tilde": (16, 8, 4, {"fill": [255, 255, 255]}, 46, 70),
 "R1:hyphen": (14, 7, 5, {"fill": [255, 255, 255]}, 46, 70),
 "R1:comma": (9, 16, 5, {"fill": [255, 255, 255]}, 46, 70),
 "R0:acute": (10, 8, 2.4, {"fill": [254, 254, 254], "edge": [139, 139, 139], "edge_px": 1}, 9, 33),
 "F:tilde": (30, 15, 6, {"fill": [255, 255, 255], "edge": [10, 10, 10], "edge_px": 2}, 248, 309),
 "F:acute": (22, 18, 6, {"fill": [255, 255, 255], "edge": [10, 10, 10], "edge_px": 2}, 248, 309),
  "E:tilde": (36, 21, 6, {"fill": [254, 254, 254], "edge": [254, 254, 254], "edge_px": 0, "outline_layer": True, "dilate": 3, "ring": True}, 157, 222),
  "E:acute": (28, 24, 6, {"fill": [254, 254, 254], "edge": [254, 254, 254], "edge_px": 0, "outline_layer": True, "dilate": 3, "ring": True}, 157, 222),
}
I = np.pad(free.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
ok = lambda x, y, w, h: I[y + h, x + w] - I[y, x + w] - I[y + h, x] + I[y, x] == w * h
taken = np.zeros_like(free)
out = {}
for k, (w, h, stroke, style, it, ib) in sorted(A.items(), key=lambda kv: -kv[1][0] * kv[1][1]):
    W, H = w + 2 * M, h + 2 * M
    spot = None
    for y in range(0, 1024 - H, 2):  # top half first (next to the alphabets)
        for x in range(1024, 2048 - W, 2):
            if ok(x, y, W, H) and not taken[y:y + H, x:x + W].any():
                spot = (x, y)
                break
        if spot:
            break
    assert spot, k
    x, y = spot
    taken[y:y + H, x:x + W] = True
    out[k] = {"box": [x + M, y + M, x + M + w, y + M + h], "shape": k.split(":")[1], "stroke": stroke, **style,
              "ink_top": it, "ink_bottom": ib, "gap": 3 if k[0] != "R" else (0 if k.startswith("R0") else -2)}
json.dump(out, open(HERE / "accents.json", "w"), indent=1)
for k, v in out.items():
    print(k, v["box"])
