"""PT-BR words of the pavement-marking atlas `t_decal_roadmarkings` (Phase 6, 6A) - deterministic master.

The atlas is a 4x4 grid of square cells (managedDecalData.json: texRows/texCols 4); each decal shows ONE
cell. A word is defined by FOUR maps that must agree (audit section 4.1):

  _o.data     (512)   opacity: letter shape x paint wear  -> decides what is drawn
  _b.color    (1024)  paint colour/texture inside the letters
  _nm.normal  (1024)  BC5 relief: raised paint edges + crack texture
  _ao.data    (2048)  dark rim around the letters + specks
  _r.data / _m.data   roughness / metallic: noise not tied to the letters -> left untouched

For every edited cell and every map the script:
  1. measures the ORIGINAL word: mask M0 (opacity >= 0.5) at the map's resolution, signed distance to
     its edge, and the map's mean profile as a function of that distance (normal: projected on the
     edge direction) -> how the paint edge looks in this map;
  2. builds a "paint field" by copying the original letter interior (eroded M0) and filling the rest of
     the cell with shifted copies of the same interior -> real paint texture, no synthesis;
  3. renders the new word (system font) and recomposes: profile(new distance) + texture deviation of
     the paint field inside the new letters.  Outside the edited cells nothing changes.

    python working/layered/t_decal_roadmarkings/build_roadmarkings.py build
    python working/layered/t_decal_roadmarkings/build_roadmarkings.py preview
    python working/layered/t_decal_roadmarkings/build_roadmarkings.py build layout_decalroad.json   # copy in assets/materials/decalroad
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
import compose as C  # noqa: E402

LAYOUT_NAME = sys.argv[2] if len(sys.argv) > 2 else "layout.json"
LAYOUT = json.loads((HERE / LAYOUT_NAME).read_text(encoding="utf8"))
R = {"o": 6, "b": 8, "nm": 10, "ao": 16}  # profile half-width (px at each map's resolution)


def load():
    maps = {}
    for key, m in LAYOUT["maps"].items():
        p = REPO / m["original"]
        C.check_original(p)
        maps[key] = np.array(Image.open(p).convert("RGBA"))
    return maps


def cell_box(idx, size):
    r, c = divmod(idx, 4)
    s = size // 4
    return c * s, r * s, (c + 1) * s, (r + 1) * s


def signed_distance(mask, rmax):
    """City-block-ish signed distance (negative inside), clipped to +-rmax."""
    d = np.full(mask.shape, float(rmax))
    cur = mask.copy()
    d[mask] = -float(rmax)
    out_ring = mask.copy()
    for k in range(1, rmax + 1):  # outside: distance to the letters
        nxt = C.dilate(out_ring, 1)
        d[nxt & ~out_ring] = k - 0.5
        out_ring = nxt
    inner = ~mask
    for k in range(1, rmax + 1):  # inside: distance to the background
        nxt = C.dilate(inner, 1)
        d[nxt & ~inner] = -(k - 0.5)
        inner = nxt
    return d


def grad_dir(cov):
    g = C.box_blur(cov[..., None], 2)[..., 0]
    gy, gx = np.gradient(g)
    n = np.hypot(gx, gy) + 1e-6
    return -gx / n, -gy / n  # pointing outwards


def paint_field(values, mask, rng):
    """Original letter interior copied over the whole cell (shifted copies fill the gaps)."""
    inner = mask & ~C.dilate(~mask, 3)
    out = values.astype(np.float64).copy()
    have = inner.copy()
    H, W = mask.shape
    shifts = [(dy, dx) for r in range(4, max(H, W), 6) for dy, dx in ((0, r), (r, 0), (0, -r), (-r, 0), (r, r), (-r, -r), (r, -r), (-r, r))]
    for dy, dx in shifts:
        if have.all():
            break
        src_ok = np.roll(np.roll(inner, dy, 0), dx, 1)
        take = src_ok & ~have
        if take.any():
            out[take] = np.roll(np.roll(values, dy, 0), dx, 1)[take]
            have |= take
    if not have.all():
        out[~have] = values[inner].mean(0)
    return out


def profile(values, d, rmax, inside_mask):
    """Mean of `values` per signed-distance bin (-rmax..rmax)."""
    bins = np.round(d * 2) / 2
    prof = {}
    for b in np.unique(bins):
        sel = bins == b
        if sel.sum() > 10:
            prof[float(b)] = values[sel].mean(0)
    return prof


def apply_profile(prof, d):
    keys = np.array(sorted(prof))
    vals = np.array([prof[k] for k in keys])
    b = np.clip(np.round(d * 2) / 2, keys.min(), keys.max())
    idx = np.searchsorted(keys, b)
    idx = np.clip(idx, 0, len(keys) - 1)
    return vals[idx]


def word_cov(word, spec, box, size):
    sp = dict(spec)
    return C.render_line(word, sp, box, (size, size))


def build():
    maps = load()
    orig = {k: v.copy() for k, v in maps.items()}
    rng = np.random.default_rng(LAYOUT.get("seed", 20261005))
    style = LAYOUT["style"]
    log = []
    for cell in LAYOUT["cells"]:
        idx, word = cell["slot"], cell["text"]
        # word box in the 1024 colour grid: original ink box of the opacity map (scaled), accents above
        o = orig["o"][..., 0].astype(float) / 255
        ox0, oy0, ox1, oy1 = cell_box(idx, o.shape[0])
        m0 = o[oy0:oy1, ox0:ox1] > 0.15
        ys, xs = np.nonzero(m0)
        k = 1024 / o.shape[0]
        ink = [ox0 + xs.min(), oy0 + ys.min(), ox0 + xs.max() + 1, oy0 + ys.max() + 1]
        cx0, cy0, cx1, cy1 = cell_box(idx, 1024)
        bx0 = int(round(ink[0] * k)) if not cell.get("full_width") else cx0 + cell.get("margin", 10)
        bx1 = int(round(ink[2] * k)) if not cell.get("full_width") else cx1 - cell.get("margin", 10)
        by0, by1 = int(round(ink[1] * k)), int(round(ink[3] * k))
        if "x_range" in cell:  # explicit horizontal extent (1024 grid), e.g. to keep the gap of a side-by-side pair
            bx0, bx1 = cell["x_range"]
        acc = int(round((by1 - by0) * cell.get("accent_room", 0.0)))
        box = [bx0, by0 + acc, bx1, by1]
        spec = dict(style)
        spec.update(cell.get("style", {}))
        spec["stretch"] = cell.get("stretch", False)
        rec = {"slot": idx, "text": word, "cap_box_1024": box}
        for key, m in maps.items():
            if key not in R:
                continue
            size = m.shape[0]
            s = size / 1024
            X0, Y0, X1, Y1 = cell_box(idx, size)
            sl = (slice(Y0, Y1), slice(X0, X1))
            bb = [int(round(v * s)) for v in box]
            new = word_cov(word, spec, bb, size)[sl]
            o_old = np.asarray(Image.fromarray(orig["o"][..., 0]).resize((size, size), Image.LANCZOS), float)[sl] / 255
            m_old = o_old > 0.15
            m_new = new > 0.5
            vals = orig[key][sl][..., :3].astype(np.float64)
            rmax = max(2, int(round(R[key])))
            d_old, d_new = signed_distance(m_old, rmax), signed_distance(m_new, rmax)
            field = paint_field(vals, m_old, rng)
            if key == "o":
                # opacity: wear of the paint (field) x new letter coverage; level of the original letters kept
                out = field[..., 0] * new
                res = np.repeat(out[..., None], 3, -1)
            elif key == "b":
                bg = np.median(vals[~C.dilate(m_old, 4)], 0)
                res = np.where(C.dilate(m_new, 3)[..., None], field, bg)
            elif key == "ao":
                prof = profile(vals, d_old, rmax, m_old)
                base = apply_profile(prof, d_new)
                inner_mean = vals[d_old <= -rmax + 0.5].mean(0) if (d_old <= -rmax + 0.5).any() else vals[m_old].mean(0)
                res = base + np.where((d_new < -1)[..., None], field - inner_mean, 0)
            else:  # nm: BC5 x/y in R/G; relief projected on the edge direction
                gx_o, gy_o = grad_dir(o_old)
                dx, dy = vals[..., 0] - 127.5, vals[..., 1] - 127.5
                proj = dx * gx_o + dy * gy_o
                prof = profile(proj[..., None], d_old, rmax, m_old)
                p_new = apply_profile(prof, d_new)[..., 0]
                gx_n, gy_n = grad_dir(new)
                fx, fy = field[..., 0] - 127.5, field[..., 1] - 127.5
                inner = (d_new < -2)
                res = vals.copy()
                res[..., 0] = 127.5 + p_new * gx_n + np.where(inner, fx, 0)
                res[..., 1] = 127.5 + p_new * gy_n + np.where(inner, fy, 0)
                res[..., 2] = vals[..., 2]
            maps[key][sl][..., :3] = np.clip(np.round(res), 0, 255).astype(np.uint8)
            rec[f"{key}_pixels_changed"] = int((np.abs(maps[key][sl][..., :3].astype(int) - orig[key][sl][..., :3].astype(int)).max(-1) > 0).sum())
        log.append(rec)
    for key, m in LAYOUT["maps"].items():
        if m.get("out"):
            out = REPO / m["out"]
            out.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(maps[key], "RGBA").save(out)
    (HERE / ("build_log.json" if LAYOUT_NAME == "layout.json" else "build_log_" + LAYOUT_NAME)).write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    print(json.dumps(log, ensure_ascii=False))


def preview():
    """What a decal shows: colour where opacity >= alphaRef 8, over asphalt grey; original vs PT-BR."""
    out_dir = REPO / "working/temporary/t_decal_roadmarkings"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for state in ("original", "out"):
        mp = {k: np.array(Image.open(REPO / (m["original"] if state == "original" else (m.get("out") or m["original"]))).convert("RGBA"))
              for k, m in LAYOUT["maps"].items()}
        col = mp["b"][..., :3].astype(float)
        op = np.asarray(Image.fromarray(mp["o"][..., 0]).resize((1024, 1024), Image.LANCZOS), float) / 255
        ao = np.asarray(Image.fromarray(mp["ao"][..., 0]).resize((1024, 1024), Image.LANCZOS), float) / 255
        asphalt = np.full_like(col, 70.0)
        img = asphalt * (1 - op[..., None]) + col * ao[..., None] * op[..., None]
        tiles = []
        for cell in LAYOUT["cells"]:
            x0, y0, x1, y1 = cell_box(cell["slot"], 1024)
            t = Image.fromarray(img[y0:y1, x0:x1].astype(np.uint8))
            nm = mp["nm"][y0:y1, x0:x1, :3].copy()
            nm[..., 2] = 255
            tiles.append(np.concatenate([np.asarray(t), nm], 0))
        rows.append(np.concatenate(tiles, 1))
    Image.fromarray(np.concatenate(rows, 0)).save(out_dir / "preview.png")
    print(out_dir / "preview.png")


if __name__ == "__main__":
    {"build": build, "preview": preview}[sys.argv[1]]()
