"""New faces for the two plates on the toll booths (s_toll_booth_center.dae / _alt.dae, 5 booths of the toll plaza),
Phase 7. The booth end facing traffic carries a "DO NOT STOP" plate and a "SPEED LIMIT 25" plate built from shared
t_roadsigns cells (white board, letters of ONLY/STOP, SPEED LIMIT, the digit row). The lower board is a 2 x 2 set of
quads with overlapping UVs (a stretched board), so the new face is BAKED: the whole plate is drawn in metres, then each
board quad gets its own new tile holding exactly the part of the plate it covers (sampled through the quad's own
texture frame), and the legend/letter/digit quads point at the empty cell of speed_plate_tiles.json.

  DO NOT STOP     -> NÃO PARE
  SPEED LIMIT 25  -> R-19 40 (25 mph -> 40 km/h, LOCALIZATION_RULES 2.3; the 5 lanes through the booths are set to 40,
                     working/functional/speed_changes.json, plan entry toll_plaza_40 - as the Phase 5 dock booths)

Writes toll_booth_tiles.json ({"elements": op "image", "uv_map"}) and the tile images in working/png/toll_booth/.

    python working/layered/t_roadsigns/toll_booth_tiles.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
sys.path.insert(0, str(REPO / "working/layered/r19"))
import glyph_signs as G  # noqa: E402
import build_r19 as R19  # noqa: E402

MESHES = ["source/originals/meshes/objects/s_toll_booth_center.dae", "source/originals/meshes/objects/s_toll_booth_center_alt.dae"]
OUT_IMG = REPO / "working/png/toll_booth"
ATLAS = np.asarray(Image.open(REPO / "source/originals/png/t_roadsigns_b.color.png").convert("RGB")).astype(np.float64)
OPAC = np.asarray(Image.open(REPO / "source/originals/png/t_roadsigns_o.data.png").convert("L"))
SPT = json.loads((HERE / "speed_plate_tiles.json").read_text(encoding="utf8"))
GLYPH = json.loads((HERE / "glyph_tiles.json").read_text(encoding="utf8"))
BLANK = SPT["blank"]
BOARDS = ([371, 189, 515, 380], [375, 189, 511, 380], [371, 189, 454, 285], [443, 189, 515, 285], [371, 234, 454, 380], [443, 234, 515, 380])
UPPER_Z, LOWER_Z = (2.82, 3.25), (2.30, 2.82)   # booth-local height of the two plates
PPM = 700   # canvas px per metre
M = 6
S = 0.5   # tile texels per original texel: the booth plates are ~0.3 m wide (0.5 still gives ~240 px/m)

foot = np.load(REPO / "working/temporary/rs_footprint_all.npy")
free = (OPAC.astype(int) < 8) & ~foot
taken = np.zeros_like(free)
for box in [e["box"] for e in GLYPH["elements"] + SPT["elements"]] + [u["to"] for u in GLYPH["uv_map"]] + [BLANK]:
    x0, y0, x1, y1 = box
    taken[max(y0 - M, 0):y1 + M, max(x0 - M, 0):x1 + M] = True
I = np.pad(free.astype(int), ((1, 0), (1, 0))).cumsum(0).cumsum(1)


def place(w, h):
    W, H = w + 2 * M, h + 2 * M
    for y in range(0, 1024 - H, 2):
        for x in range(0, 2048 - W, 2):
            if I[y + H, x + W] - I[y, x + W] - I[y + H, x] + I[y, x] == W * H and not taken[y:y + H, x:x + W].any():
                taken[y:y + H, x:x + W] = True
                return x + M, y + M
    raise SystemExit(f"no free space for {w}x{h}")


def frame(q):
    """px (u, v) -> booth-local position, and its inverse on the plate plane (x, z)."""
    Mx = np.linalg.lstsq(np.c_[q["uv_px"][0], np.ones(3)], q["tris"][0], rcond=None)[0]
    return Mx


def same(r, cell):
    return max(abs(a - b) for a, b in zip(r, cell)) <= 1.5


def plate_canvas(quads, zr):
    """Original look of a plate (board quads only, sampled from the atlas) on a canvas in metres."""
    pts = np.concatenate([q["tris"].reshape(-1, 3) for q in quads])
    x0, x1, z0, z1 = pts[:, 0].min(), pts[:, 0].max(), pts[:, 2].min(), pts[:, 2].max()
    W, H = int(round((x1 - x0) * PPM)), int(round((z1 - z0) * PPM))
    img = np.zeros((H, W, 3))
    have = np.zeros((H, W), bool)
    xs = x0 + (np.arange(W) + 0.5) / PPM
    zs = z1 - (np.arange(H) + 0.5) / PPM
    X, Z = np.meshgrid(xs, zs)
    for q in quads:
        Mx = frame(q)
        A = np.array([[Mx[0][0], Mx[1][0]], [Mx[0][2], Mx[1][2]]])   # (u, v) -> (x, z)
        uv = np.linalg.solve(A, np.stack([X.ravel() - Mx[2][0], Z.ravel() - Mx[2][2]]))
        u, v = uv[0].reshape(H, W), uv[1].reshape(H, W)
        r = q["rect"]
        inside = (u >= r[0]) & (u <= r[2]) & (v >= r[1]) & (v <= r[3]) & ~have
        ui = np.clip(u.round().astype(int), 0, 2047)
        vi = np.clip(v.round().astype(int), 0, 1023)
        img[inside] = ATLAS[vi[inside], ui[inside]]
        have |= inside
    return img, (x0, x1, z0, z1)


def bake(q, canvas, ext):
    """Tile for quad q: for each texel of its original rect, the canvas colour at the point the texel lands on."""
    x0, x1, z0, z1 = ext
    r = [int(round(v)) for v in q["rect"]]
    w, h = max(2, round((r[2] - r[0]) * S)), max(2, round((r[3] - r[1]) * S))
    Mx = frame(q)
    U, V = np.meshgrid(r[0] + (np.arange(w) + 0.5) * (r[2] - r[0]) / w, r[1] + (np.arange(h) + 0.5) * (r[3] - r[1]) / h)
    P = U[..., None] * Mx[0] + V[..., None] * Mx[1] + Mx[2]
    ci = np.clip(((P[..., 0] - x0) * PPM).astype(int), 0, canvas.shape[1] - 1)
    cj = np.clip(((z1 - P[..., 2]) * PPM).astype(int), 0, canvas.shape[0] - 1)
    col = canvas[cj, ci]
    opa = np.asarray(Image.fromarray(OPAC[r[1]:r[3], r[0]:r[2]]).resize((w, h), Image.LANCZOS))
    return col, opa, (w, h)


def text_canvas(canvas, ext, lines):
    """Black text lines (text, centre z, cap height m) on the canvas, same face as the R-19 numerals."""
    x0, x1, z0, z1 = ext
    H, W = canvas.shape[:2]
    mask = Image.new("L", (W * 4, H * 4), 0)
    d = ImageDraw.Draw(mask)
    for text, zc, cap in lines:
        f = R19._fit_font(text, cap * PPM * 4, {"wght": 700, "wdth": 75})
        b = f.getbbox(text)
        if b[2] - b[0] > 0.86 * W * 4:   # too wide for the board: scale down
            f = R19._fit_font(text, cap * PPM * 4 * 0.86 * W * 4 / (b[2] - b[0]), {"wght": 700, "wdth": 75})
            b = f.getbbox(text)
        d.text((W * 2 - (b[0] + b[2]) / 2, (z1 - zc) * PPM * 4 - (b[1] + b[3]) / 2), text, font=f, fill=255)
    m = np.asarray(mask.resize((W, H), Image.LANCZOS), np.float64)[..., None] / 255.0
    return canvas * (1 - m) + np.array(R19.COLORS["black"], float) * m


def r19_canvas(canvas, ext, value):
    x0, x1, z0, z1 = ext
    H, W = canvas.shape[:2]
    pw, ph = x1 - x0, z1 - z0
    face, mask = R19.render(value, panel=(pw, ph), tex=(W, H), disc=0.86 * min(pw, ph))
    m = np.asarray(mask, np.float64)[..., None] / 255.0
    return canvas * (1 - m) + np.asarray(face.convert("RGB"), np.float64) * m


OUT_IMG.mkdir(parents=True, exist_ok=True)
elements, uv_map, tiles = [], [], {}
for mesh in MESHES:
    qs = G.read_quads(REPO / mesh, "roadsigns", (2048, 1024))
    # the booth end facing traffic: where the board quads are (y = -3.06 on the short booth, -7.06 on the _alt one)
    yb = float(np.median([q["centroid"][1] for q in qs if any(same(q["rect"], b) for b in BOARDS)]))
    face = [q for q in qs if abs(q["centroid"][1] - yb) < 0.05]
    for zr, kind in ((UPPER_Z, "upper"), (LOWER_Z, "lower")):
        plate = [q for q in face if zr[0] <= q["centroid"][2] <= zr[1]]
        boards = [q for q in plate if any(same(q["rect"], b) for b in BOARDS)]
        others = [q for q in plate if not any(q is b for b in boards)]
        for lod in sorted({q["node"] for q in boards}):
            bq = [q for q in boards if q["node"] == lod]
            canvas, ext = plate_canvas(bq, zr)
            if kind == "upper":
                canvas = text_canvas(canvas, ext, [("NÃO", 3.10, 0.085), ("PARE", 2.96, 0.085)])
            else:
                canvas = r19_canvas(canvas, ext, 40)
            for q in bq:
                col, opa, (w, h) = bake(q, canvas, ext)
                key = (kind, tuple(int(round(v)) for v in q["rect"]), tuple(np.round([ext[0], ext[1], ext[2], ext[3]], 2)),
                       tuple(np.round(q["centroid"][[0, 2]] - [ext[0], ext[2]], 2)))
                if key not in tiles:
                    x, y = place(w, h)
                    tid = f"toll_{kind}_{len(tiles):02d}"
                    Image.fromarray(np.dstack([col.round().clip(0, 255).astype(np.uint8), np.full((h, w), 255, np.uint8)]), "RGBA").save(OUT_IMG / f"{tid}.png")
                    Image.fromarray(opa).save(OUT_IMG / f"{tid}_o.png")
                    elements.append({"id": tid, "matrix": "roadsigns_speed_limit_tile" if kind == "lower" else "roadsigns_do_not_stop",
                                     "op": "image", "box": [x, y, x + w, y + h], "image": f"working/png/toll_booth/{tid}.png",
                                     "opacity_image": f"working/png/toll_booth/{tid}_o.png",
                                     "uv_override": "UV of the PT-BR s_toll_booth_center(_alt).dae of the mod (board quads re-targeted here); Phase 7 toll booth"})
                    tiles[key] = [x, y, x + w, y + h]
                uv_map.append({"id": f"{Path(mesh).stem}_{lod}_{kind}_board", "from": [round(v) for v in q["rect"]], "to": tiles[key],
                               "at": [q["centroid"].round(4).tolist()], "radius": 0.005})
        for q in others:
            uv_map.append({"id": f"{Path(mesh).stem}_{q['node']}_{kind}_legend", "from": [round(v) for v in q["rect"]], "to": BLANK,
                           "at": [q["centroid"].round(4).tolist()], "radius": 0.005})
    # preview of the two new plates as the booth shows them
json.dump({"_doc": __doc__, "elements": elements, "uv_map": uv_map}, open(HERE / "toll_booth_tiles.json", "w", encoding="utf8"), indent=1, ensure_ascii=False)
for e in elements:
    print(e["id"], e["box"])
print(len(uv_map), "uv entries")
