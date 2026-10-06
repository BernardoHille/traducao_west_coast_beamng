"""Deterministic PT-BR composition of a texture family from its ORIGINAL maps (Phase 6 engine).

Generalises the Phase 5 `t_roadsigns` master (working/layered/t_roadsigns/build_t_roadsigns.py) to any
family: every map is loaded from source/originals (SHA-256 checked against the manifest), only the
boxes listed in the family layout are edited, every other pixel is copied untouched, and the result
is written to working/png/<variant>/<name>.png.

    python tools/production/compose.py working/layered/<family>/layout.json build
    python tools/production/compose.py working/layered/<family>/layout.json preview   # before/after crops
    python tools/production/compose.py working/layered/<family>/layout.json regions   # UV evidence -> allowed_regions.json
    python tools/production/compose.py working/layered/<family>/layout.json grid --map color --box x0 y0 x1 y1

Layout (JSON):
  family, maps {role: {"original": "<png in source/originals>", "out": "<png in working/png>"}},
  materials [...] (UV evidence), uv_min_coverage, seed, elements [...]
Element ops:
  panel  painted legend on an opaque area: detect the old legend, fill it from the surrounding
         background, draw the new text (lines with explicit cap boxes, or an auto-wrapped block)
  glyph  letters cut by an opacity map: rewrite the mask and paint the base colour under the letters
  fill   repaint boxes with the background (removing a word without replacement)
  copy   copy pixels from another box of the ORIGINAL (re-use an existing glyph/pictogram)
No generative step: text is rendered with Windows system fonts over the original pixels.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
FONT_DIR = Path("C:/Windows/Fonts")
FONTS = {
    "bahnschrift": "bahnschrift.ttf", "arial": "arial.ttf", "arial_bold": "arialbd.ttf", "arial_black": "ariblk.ttf",
    "arial_narrow": "ARIALN.TTF", "arial_narrow_bold": "ARIALNB.TTF", "impact": "impact.ttf", "stencil": "STENCIL.TTF",
    "franklin_heavy": "FRAHV.TTF", "franklin_demi": "FRADM.TTF", "franklin_demi_cond": "FRADMCN.TTF",
    "franklin_medium": "framd.ttf", "franklin_medium_cond": "FRAMDCN.TTF", "franklin_book": "FRABK.TTF",
    "agency_bold": "AGENCYB.TTF", "agency": "AGENCYR.TTF", "tahoma": "tahoma.ttf", "tahoma_bold": "tahomabd.ttf",
    "verdana": "verdana.ttf", "verdana_bold": "verdanab.ttf", "segoe": "segoeui.ttf", "segoe_bold": "segoeuib.ttf",
    "segoe_semibold": "seguisb.ttf", "segoe_black": "seguibl.ttf", "trebuchet": "trebuc.ttf", "trebuchet_bold": "trebucbd.ttf",
    "georgia": "georgia.ttf", "georgia_bold": "georgiab.ttf", "times": "times.ttf", "times_bold": "timesbd.ttf",
    "rockwell": "ROCK.TTF", "rockwell_bold": "ROCKB.TTF", "rockwell_xbold": "ROCKEB.TTF", "gill": "GIL_____.TTF",
    "gill_bold": "GILB____.TTF", "gill_ultra": "GILSANUB.TTF", "gill_cond": "GILC____.TTF", "twcen": "TCM_____.TTF",
    "twcen_bold": "TCB_____.TTF", "twcen_cond_bold": "TCCB____.TTF", "twcen_cond_xbold": "TCCEB.TTF",
    "eras_bold": "ERASBD.TTF", "berlin_bold": "BRLNSB.TTF", "cooper_black": "COOPBL.TTF", "calibri": "calibri.ttf",
    "calibri_bold": "calibrib.ttf", "swiss_cond_black": "swissck.ttf", "swiss_cond_bold": "swisscb.ttf",
    "comic_bold": "comicbd.ttf", "ink_free": "Inkfree.ttf", "segoe_script_bold": "segoescb.ttf",
}
VARIABLE = {"bahnschrift"}
SS = 4
NAMED = {
    "white": lambda a: (a[..., 0] > 175) & (a[..., 1] > 175) & (a[..., 2] > 175),
    "red": lambda a: (a[..., 0] > 120) & (a[..., 0] > a[..., 1] + 50) & (a[..., 0] > a[..., 2] + 50),
    "black": lambda a: (a.max(-1) < 110),
    "dark": lambda a: (a.max(-1) < 140),
    "green": lambda a: (a[..., 1] > a[..., 0] + 20) & (a[..., 1] > 60) & (a[..., 0] < 150),
    "yellow": lambda a: (a[..., 0] > 160) & (a[..., 1] > 130) & (a[..., 2] < 110),
    "blue": lambda a: (a[..., 2] > a[..., 0] + 40) & (a[..., 2] > 90),
    # neon tubes and their glow over a dark grey wall: saturated or bright pixels
    "neon": lambda a: ((a.max(-1) - a.min(-1)) > 38) | (a.max(-1) > 105),
    "neon_red": lambda a: (a[..., 0] > a[..., 1] + 35) & (a[..., 0] > a[..., 2] + 25) & (a[..., 0] > 70),
}


# ---------------------------------------------------------------- io
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_rows():
    with open(REPO / "docs/inventory/original_files_manifest.csv", encoding="utf8") as f:
        return list(csv.DictReader(f))


def check_original(path: Path):
    rel = path.relative_to(REPO).as_posix()
    rows = [r for r in manifest_rows() if r["copied_to"].replace("\\", "/") == rel]
    if not rows:
        raise SystemExit(f"{rel}: not registered in the manifest")
    if sha256(path) != rows[0]["sha256"]:
        raise SystemExit(f"{rel}: SHA-256 mismatch with the manifest - stop and investigate")


class Family:
    def __init__(self, layout_path: Path):
        self.path = layout_path
        self.layout = json.loads(layout_path.read_text(encoding="utf8"))
        self.maps, self.orig = {}, {}
        for role, m in self.layout["maps"].items():
            p = REPO / m["original"]
            check_original(p)
            arr = np.array(Image.open(p).convert("RGBA"))
            self.orig[role] = arr.copy()
            self.maps[role] = arr
        base = self.layout.get("base_map", "color")
        self.base_shape = self.maps[base].shape[:2]
        self.rng = np.random.default_rng(self.layout.get("seed", 20261003))

    def scale(self, role, box):
        """Box in base-map pixels -> box in `role` pixels (maps may have other resolutions)."""
        H, W = self.maps[role].shape[:2]
        bh, bw = self.base_shape
        sx, sy = W / bw, H / bh
        x0, y0, x1, y1 = box
        return [int(round(x0 * sx)), int(round(y0 * sy)), int(round(x1 * sx)), int(round(y1 * sy))]

    def save(self):
        for role, m in self.layout["maps"].items():
            if m.get("out"):
                out = REPO / m["out"]
                out.parent.mkdir(parents=True, exist_ok=True)
                arr = self.maps[role]
                mode = m.get("mode", "RGBA")
                img = Image.fromarray(arr, "RGBA")
                if mode == "L":
                    img = img.getchannel("R")
                elif mode == "RGB":
                    img = img.convert("RGB")
                img.save(out, optimize=False)


# ---------------------------------------------------------------- helpers
def box_slices(b):
    x0, y0, x1, y1 = b
    return slice(y0, y1), slice(x0, x1)


def dilate(m: np.ndarray, r: int) -> np.ndarray:
    if r <= 0:
        return m.copy()
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dy * dy + dx * dx <= r * r:
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def box_blur(img: np.ndarray, r: int) -> np.ndarray:
    k = 2 * r + 1
    pad = np.pad(img, ((r, r), (r, r)) + ((0, 0),) * (img.ndim - 2), mode="edge").astype(np.float64)
    c = pad.cumsum(0).cumsum(1)
    c = np.pad(c, ((1, 0), (1, 0)) + ((0, 0),) * (img.ndim - 2))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def inpaint(rgb: np.ndarray, hole: np.ndarray, rng, iters: int = 400, grain: float = 0.8) -> np.ndarray:
    """Diffusion fill of `hole` from its surroundings, re-grained with residuals of the known pixels."""
    out = rgb.astype(np.float64).copy()
    known = ~hole
    if not known.any() or not hole.any():
        return rgb.astype(np.float64)
    out[hole] = out[known].mean(0)
    for _ in range(iters):
        acc = np.zeros_like(out)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            acc += np.roll(np.roll(out, dy, 0), dx, 1)
        out[hole] = (acc / 4.0)[hole]
    if grain:
        base = rgb.astype(np.float64)
        clean = known & ~dilate(hole, 3)
        resid = (base - box_blur(base, 2))[clean]
        if len(resid):
            resid = np.clip(resid, -10, 10) * grain
            out[hole] += resid[rng.integers(0, len(resid), hole.sum())]
    return out.clip(0, 255)


def grain_color(src: np.ndarray, sel: np.ndarray, rng, n: int, amount: float = 0.6) -> np.ndarray:
    pix = src[sel].astype(np.float64)
    if len(pix) == 0:
        return np.zeros((n, src.shape[-1]))
    med = np.median(pix, 0)
    if len(pix) < 4 or amount == 0:
        return np.tile(med, (n, 1))
    resid = np.clip(pix - pix.mean(0), -25, 25) * amount
    return med + resid[rng.integers(0, len(pix), n)]


def legend_mask(rgb: np.ndarray, spec) -> np.ndarray:
    a = rgb.astype(int)
    if isinstance(spec, str):
        return NAMED[spec](a)
    if "rgbs" in spec:  # several colours (e.g. fill + outline of a display text)
        m = np.zeros(a.shape[:-1], bool)
        for c in spec["rgbs"]:
            m |= np.linalg.norm(a - np.array(c, float), axis=-1) < spec.get("tol", 60)
        return m
    ref = np.array(spec["rgb"], float)
    return np.linalg.norm(a - ref, axis=-1) < spec.get("tol", 60)


# ---------------------------------------------------------------- text
def font(spec: dict, size: int) -> ImageFont.FreeTypeFont:
    name = spec.get("font", "bahnschrift")
    f = ImageFont.truetype(str(FONT_DIR / FONTS[name]), max(1, size))
    if name in VARIABLE:
        try:
            f.set_variation_by_axes([spec.get("wght", 600), spec.get("wdth", 100)])
        except OSError:
            pass
    return f


def cap_height(spec, size):
    b = font(spec, size).getbbox(spec.get("cap_ref", "H"))
    return b[3] - b[1]


def text_width(text, spec, cap_px):
    """Advance width of `text` when the capital height is cap_px (no squeeze)."""
    ref = 200
    s = ref * cap_px / max(1, cap_height(spec, ref))
    f = font(spec, int(round(s * SS)))
    tr = spec.get("tracking", 0) * SS * max(0, len(text) - 1)
    return (f.getlength(text) + tr) / SS


def render_line(text: str, spec: dict, box, shape) -> np.ndarray:
    """Coverage (0..1, full map size) of `text` with capital height = box height.

    Narrows the Bahnschrift width axis (down to min_wdth) before squeezing horizontally (max_squeeze)."""
    spec = dict(spec)
    if spec.get("font", "bahnschrift") in VARIABLE:
        while True:
            w = text_width(text, spec, box[3] - box[1])
            if w <= (box[2] - box[0]) or spec.get("wdth", 100) <= spec.get("min_wdth", 75):
                break
            spec["wdth"] = max(spec.get("min_wdth", 75), spec.get("wdth", 100) - 5)
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    cap_px = bh
    ref = 200
    size = int(round(ref * cap_px * SS / max(1, cap_height(spec, ref))))
    f = font(spec, size)
    tb = f.getbbox(spec.get("cap_ref", "H"))
    pad_top = int(bh * SS * 0.7) + 2 * SS
    H = bh * SS + 2 * pad_top
    tracking = spec.get("tracking", 0) * SS
    W = int(f.getlength(text) + tracking * len(text)) + 16 * SS
    canvas = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(canvas)
    x, by = 8 * SS, pad_top - tb[1]
    if tracking:
        for ch in text:
            d.text((x, by), ch, font=f, fill=255)
            x += f.getlength(ch) + tracking
    else:
        d.text((x, by), text, font=f, fill=255)
    arr = np.array(canvas)
    if spec.get("italic_shear"):
        img = Image.fromarray(arr)
        sh = spec["italic_shear"]
        arr = np.array(img.transform(img.size, Image.AFFINE, (1, sh, -sh * H / 2, 0, 1, 0), Image.BICUBIC))
    cols = np.nonzero(arr.max(0) > 0)[0]
    if len(cols) == 0:
        return np.zeros(shape)
    arr = arr[:, cols.min():cols.max() + 1]
    ink_w = arr.shape[1]
    target = min(ink_w, bw * SS)
    if spec.get("stretch"):
        target = bw * SS
    max_sq = spec.get("max_squeeze", 1.0)  # 1.0 = squeeze allowed down to any width
    if ink_w > bw * SS and max_sq < 1.0 and target / ink_w < max_sq:
        raise SystemExit(f"text {text!r} does not fit {box} (needs {ink_w / SS:.0f}px)")
    img = Image.fromarray(arr).resize((max(1, int(round(target / SS))), H // SS), Image.LANCZOS)
    cov = np.asarray(img, dtype=np.float64) / 255.0
    full = np.zeros(shape)
    w = cov.shape[1]
    align = spec.get("align", "center")
    px = x0 if align == "left" else (x1 - w if align == "right" else x0 + (bw - w) // 2)
    py = y0 - pad_top // SS
    Hs, Ws = shape
    ys0, xs0 = max(py, 0), max(px, 0)
    ys1, xs1 = min(py + cov.shape[0], Hs), min(px + w, Ws)
    if ys1 > ys0 and xs1 > xs0:
        full[ys0:ys1, xs0:xs1] = cov[ys0 - py:ys1 - py, xs0 - px:xs1 - px]
    return full


def wrap_options(text: str, max_lines: int):
    words = text.split()
    if "\n" in text:
        yield [l.strip() for l in text.split("\n")]
        return
    from itertools import combinations
    for n in range(1, min(max_lines, len(words)) + 1):
        for cuts in combinations(range(1, len(words)), n - 1):
            idx = (0,) + cuts + (len(words),)
            yield [" ".join(words[idx[i]:idx[i + 1]]) for i in range(n)]


def block_lines(block: dict, style: dict):
    """Auto layout of a text block in `box`: picks the wrapping that gives the largest capital height."""
    x0, y0, x1, y1 = block["box"]
    bw, bh = x1 - x0, y1 - y0
    lead = block.get("leading", 1.45)
    max_cap = block.get("max_cap", bh)
    best = None
    for lines in wrap_options(block["text"], block.get("max_lines", 4)):
        n = len(lines)
        cap = min(max_cap, bh / (n + (n - 1) * (lead - 1)))
        spec = dict(style)
        if spec.get("font", "bahnschrift") in VARIABLE:
            spec["wdth"] = spec.get("min_wdth", 75)
        widest = max(text_width(l, spec, cap) for l in lines)
        if widest > bw:
            cap *= bw / widest
        score = (round(cap, 1), -n)
        if best is None or score > best[0]:
            best = (score, lines, cap)
    _, lines, cap = best
    cap = int(np.floor(cap))
    n = len(lines)
    total = cap * n + (lead - 1) * cap * (n - 1)
    valign = block.get("valign", "middle")
    ty = y0 if valign == "top" else (y1 - total if valign == "bottom" else y0 + (bh - total) / 2)
    out = []
    for i, l in enumerate(lines):
        ly = int(round(ty + i * cap * lead))
        out.append({"text": l, "box": [x0, ly, x1, ly + cap]})
    return out


def bend_to_arc(cov, box, arc):
    """Wraps a straight line (rendered in `box`) around a circle: arc = {cx, cy, r, deg}. `r` is the radius of the
    box bottom (baseline), `deg` the image angle (y down) of the line centre; box width = arc length at `r`.
    Bottom-of-circle text (deg ~90) keeps the letter tops toward the centre and reads left to right."""
    x0, y0, x1, y1 = box
    cx, cy, r, dc = arc["cx"], arc["cy"], arc["r"], np.radians(arc.get("deg", 90))
    yy, xx = np.mgrid[0:cov.shape[0], 0:cov.shape[1]]
    rho = np.hypot(xx - cx, yy - cy)
    th = np.arctan2(yy - cy, xx - cx)
    dth = (th - dc + np.pi) % (2 * np.pi) - np.pi
    us = (x0 + x1) / 2 - dth * r                       # source column (bottom text: angle grows to the left)
    vs = y1 - (r - rho)                                # source row: baseline at radius r, tops toward the centre
    ok = (us >= x0 - 2) & (us <= x1 + 1) & (vs >= y0 - (y1 - y0)) & (vs <= y1 + (y1 - y0)) & (np.abs(dth) < np.pi / 2)
    out = np.zeros_like(cov)
    u, v = us[ok], vs[ok]
    u0, v0 = np.floor(u).astype(int), np.floor(v).astype(int)
    fu, fv = u - u0, v - v0
    H, W = cov.shape
    def at(a, b):
        return cov[np.clip(b, 0, H - 1), np.clip(a, 0, W - 1)]
    out[ok] = (at(u0, v0) * (1 - fu) * (1 - fv) + at(u0 + 1, v0) * fu * (1 - fv) + at(u0, v0 + 1) * (1 - fu) * fv
               + at(u0 + 1, v0 + 1) * fu * fv)
    return out


def text_coverage(el, shape):
    style = dict(el.get("style", {}))
    lines = list(el.get("lines", []))
    for b in el.get("blocks", []):
        st = dict(style)
        st.update(b.get("style", {}))
        for l in block_lines(b, st):
            l["style"] = b.get("style", {})
            lines.append(l)
    cov = np.zeros(shape)
    for line in lines:
        spec = dict(style)
        spec.update(line.get("style", {}))
        lc = render_line(line["text"], spec, line["box"], shape)
        if line.get("arc"):
            lc = bend_to_arc(lc, line["box"], line["arc"])
        cov = np.maximum(cov, lc)
    el["_lines"] = [{"text": l["text"], "box": l["box"]} for l in lines]
    if el.get("rotate"):  # lines are laid out unrotated around `pivot`, then rotated (degrees, counter-clockwise)
        r = el["rotate"]
        img = Image.fromarray((cov * 255).astype(np.uint8))
        img = img.rotate(r["deg"], resample=Image.BICUBIC, center=tuple(r["pivot"]))
        cov = np.asarray(img, dtype=np.float64) / 255.0
    return cov


def stroke_of(cov, px):
    """Coverage of an outline of `px` pixels around `cov` (approximate distance dilation)."""
    if px <= 0:
        return np.zeros_like(cov)
    out = cov.copy()
    r = int(np.ceil(px))
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dy * dy + dx * dx <= px * px:
                out = np.maximum(out, np.roll(np.roll(cov, dy, 0), dx, 1))
    return out


# ---------------------------------------------------------------- ops
def grow_box(rgb, el, box):
    """Erase box grown to the whole letters it touches: connected legend components seeded inside `box`,
    limited to the element box (so a slightly short erase box still removes complete letters)."""
    if el.get("no_grow"):
        return box
    ex = el["box"]
    sy, sx = box_slices(ex)
    pix = rgb[sy, sx]
    spec = el.get("legend", "auto")
    full = legend_mask(pix, spec) if spec != "auto" else None
    if full is None:
        return box
    seed = np.zeros_like(full)
    bx0, by0, bx1, by1 = box[0] - ex[0], box[1] - ex[1], box[2] - ex[0], box[3] - ex[1]
    seed[max(by0, 0):by1, max(bx0, 0):bx1] = full[max(by0, 0):by1, max(bx0, 0):bx1]
    for _ in range(el.get("grow_iters", 12)):
        nxt = dilate(seed, 1) & full
        if nxt.sum() == seed.sum():
            break
        seed = nxt
    ys, xs = np.nonzero(seed)
    if not len(xs):
        return box
    return [min(box[0], ex[0] + xs.min() - 1), min(box[1], ex[1] + ys.min() - 1),
            max(box[2], ex[0] + xs.max() + 2), max(box[3], ex[1] + ys.max() + 2)]


def detect_legend(rgb, el, box):
    """Old legend pixels inside `box`: named/explicit colour, or 'auto' = far from the box's dominant colour."""
    sy, sx = box_slices(box)
    pix = rgb[sy, sx].astype(np.float64)
    spec = el.get("legend", "auto")
    if spec == "auto":
        bg = np.median(np.concatenate([pix[0], pix[-1], pix[:, 0], pix[:, -1]]), 0)
        dist = np.linalg.norm(pix - bg, axis=-1)
        strict = dist > el.get("legend_tol", 60)
    else:
        strict = legend_mask(pix, spec)
    near = dilate(strict, 2)
    lref = np.median(pix[strict], 0) if strict.any() else pix.mean(0)
    bref = np.median(pix[~near], 0) if (~near).any() else 255 - lref
    dl = np.linalg.norm(pix - lref, axis=-1)
    db = np.linalg.norm(pix - bref, axis=-1)
    hole = ((dl < db * 1.25) | (db > el.get("bg_tol", 18))) & dilate(strict, 3)
    return strict, hole


def op_panel(fam: Family, el):
    role = el.get("map", "color")
    img = fam.maps[role]
    rgb = img[..., :3]
    shape = rgb.shape[:2]
    rng = fam.rng
    hole = np.zeros(shape, bool)
    legend_sel = np.zeros(shape, bool)
    poly = None
    if el.get("erase_rot"):  # rotated labels: [cx, cy, length, height, deg] -> polygon limiting the erase
        poly_img = Image.new("L", (shape[1], shape[0]), 0)
        dr = ImageDraw.Draw(poly_img)
        boxes = []
        for cx, cy, ln, hh, deg in el["erase_rot"]:
            a = np.radians(deg)
            ux, uy = np.cos(a), -np.sin(a)          # reading direction (image y down)
            vx, vy = -uy, ux
            pts = [(cx + sx * ux * ln / 2 + sy * vx * hh / 2, cy + sx * uy * ln / 2 + sy * vy * hh / 2)
                   for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            dr.polygon(pts, fill=255)
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            boxes.append([int(min(xs)) - 1, int(min(ys)) - 1, int(max(xs)) + 2, int(max(ys)) + 2])
        poly = np.asarray(poly_img) > 0
        el["erase"] = list(el.get("erase", [])) + boxes
    if el.get("erase_ring"):  # curved labels: [cx, cy, r_in, r_out, deg0, deg1] (image angles, y down) limit the erase
        yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
        ring = np.zeros(shape, bool)
        for cx, cy, r0, r1, a0, a1 in el["erase_ring"]:
            rho = np.hypot(xx - cx, yy - cy)
            th = np.degrees(np.arctan2(yy - cy, xx - cx))
            ring |= (rho >= r0) & (rho <= r1) & (th >= a0) & (th <= a1)
            el["erase"] = list(el.get("erase", [])) + [[int(cx - r1) - 1, int(cy - r1) - 1, int(cx + r1) + 2, int(cy + r1) + 2]]
        poly = ring if poly is None else (poly | ring)
    el["erase"] = [grow_box(rgb, el, b) for b in el.get("erase", [])]
    for b in el.get("erase", []):
        sy, sx = box_slices(b)
        strict, h = detect_legend(rgb, el, b)
        hole[sy, sx] |= h
        legend_sel[sy, sx] |= strict
    keep = np.zeros(shape, bool)
    for b in el.get("keep", []):
        keep[box_slices(b)] = True
    if el.get("keep_legend"):  # pixels of another colour that must survive (e.g. the blue hanger of a red neon)
        kb = np.zeros(shape, bool)
        kb[box_slices(el["box"])] = True
        keep |= dilate(legend_mask(rgb, el["keep_legend"]) & kb, 1)
    ebox = np.zeros(shape, bool)
    for b in el.get("erase", []):
        ebox[box_slices(b)] = True
    if poly is not None:
        ebox &= dilate(poly, 1)
    hole = dilate(hole, el.get("erase_dilate", 1)) & ~keep & ebox
    flat = np.zeros(shape, bool)
    for b in el.get("fill_boxes", []):
        flat[box_slices(b)] = True
    hole &= ~flat
    sy, sx = box_slices(el["box"])
    crop = rgb[sy, sx].copy()
    hole_c = hole[sy, sx]
    if hole_c.any():
        src = crop.copy()
        if "bg_from" in el:
            by, bx = box_slices(el["bg_from"])
            src[hole_c] = np.median(rgb[by, bx].reshape(-1, 3), 0)
        if el.get("fill") == "texture":  # low frequency by diffusion + high-frequency texture tiled from a clean sample
            low = inpaint(src, hole_c, rng, iters=el.get("inpaint_iters", 300), grain=0)
            tx0, ty0, tx1, ty1 = el["texture_from"]
            samp = rgb[ty0:ty1, tx0:tx1].astype(np.float64)
            hf = samp - box_blur(samp, 3)
            H, W = hole_c.shape
            reps = (H // hf.shape[0] + 2, W // hf.shape[1] + 2, 1)
            tile = np.tile(np.concatenate([hf, hf[:, ::-1]], 1), (reps[0], reps[1] // 2 + 1, 1))[:H, :W]
            out = low + tile
            crop = np.where(hole_c[..., None], out, crop).clip(0, 255).astype(np.uint8)
        elif el.get("fill") == "solid":
            col = el.get("bg_color") or np.median(crop[~dilate(hole_c, 2)].reshape(-1, 3), 0)
            crop[hole_c] = np.array(col, float)
            crop = crop.astype(np.uint8)
        else:
            crop = inpaint(src, hole_c, rng, iters=el.get("inpaint_iters", 300), grain=el.get("grain", 0.8)).astype(np.uint8)
    flat_c = flat[sy, sx]
    if flat_c.any():
        if "bg_color" in el:
            crop[flat_c] = np.array(el["bg_color"], np.uint8)
        else:
            by, bx = box_slices(el["bg_from"])
            bg = np.zeros(shape, bool)
            bg[by, bx] = True
            crop[flat_c] = grain_color(rgb, bg, rng, flat_c.sum(), el.get("grain_amount", 0.6)).clip(0, 255).astype(np.uint8)
    lsel = legend_sel & ~dilate(~legend_sel, 1)
    if "legend_from" in el:
        m = np.zeros(shape, bool)
        by, bx = box_slices(el["legend_from"])
        m[by, bx] = legend_mask(rgb[by, bx], el["legend"]) if el.get("legend", "auto") != "auto" else True
        lsel = m & ~dilate(~m, 1)
    cov = text_coverage(el, shape)
    cov_c = cov[sy, sx]
    st = el.get("style", {})
    if st.get("stroke"):  # outline under the fill
        s = st["stroke"]
        sc = stroke_of(cov, s["px"])[sy, sx]
        ink = sc > 0.02
        col = np.array(s["color"], float)
        a = sc[ink][:, None]
        crop[ink] = (crop[ink] * (1 - a) + col * a).clip(0, 255).astype(np.uint8)
    if st.get("glow"):  # neon: soft halo of the text colour around the tube
        g = st["glow"]
        r = max(1, int(g["px"]))
        halo = box_blur(stroke_of(cov, max(1, r // 2))[..., None], r)[..., 0][sy, sx] * g.get("alpha", 0.8)
        ink_h = halo > 0.02
        col = np.array(g.get("color", el.get("color", [255, 255, 255])), float)
        a_h = np.clip(halo[ink_h], 0, 1)[:, None]
        crop[ink_h] = (crop[ink_h] * (1 - a_h) + col * a_h).clip(0, 255).astype(np.uint8)
    if st.get("shadow"):
        s = st["shadow"]
        sh = np.roll(np.roll(cov, s["dy"], 0), s["dx"], 1)[sy, sx]
        ink = sh > 0.02
        a = sh[ink][:, None] * s.get("alpha", 1.0)
        crop[ink] = (crop[ink] * (1 - a) + np.array(s["color"], float) * a).clip(0, 255).astype(np.uint8)
    ink = cov_c > 0.02
    if ink.any():
        if "color" in el:
            lc = np.tile(np.array(el["color"], np.float64), (ink.sum(), 1))
            if el.get("color_grain"):
                lc = lc + grain_color(rgb, lsel, rng, ink.sum(), 0.6) - np.median(rgb[lsel].astype(float), 0) if lsel.any() else lc
        else:
            lc = grain_color(rgb, lsel, rng, ink.sum())
        a = cov_c[ink][:, None]
        c = crop[ink].astype(np.float64)
        crop[ink] = (c * (1 - a) + lc * a).clip(0, 255).astype(np.uint8)
    rgb[sy, sx] = crop
    # alpha: unchanged unless the element asks to rebuild it from the new text (cut-out legends)
    for aux_role, how in el.get("aux", {}).items():
        aux_apply(fam, aux_role, how, el, cov, hole, legend_sel)


def signed_distance(mask, rmax):
    """Signed distance to the edge of `mask` (negative inside), in pixels, clipped to +-rmax."""
    d = np.full(mask.shape, float(rmax))
    d[mask] = -float(rmax)
    ring = mask.copy()
    for k in range(1, rmax + 1):
        nxt = dilate(ring, 1)
        d[nxt & ~ring] = k - 0.5
        ring = nxt
    inner = ~mask
    for k in range(1, rmax + 1):
        nxt = dilate(inner, 1)
        d[nxt & ~inner] = -(k - 0.5)
        inner = nxt
    return d


def edge_dir(cov):
    g = box_blur(cov[..., None].astype(float), 2)[..., 0]
    gy, gx = np.gradient(g)
    n = np.hypot(gx, gy) + 1e-6
    return -gx / n, -gy / n


def edge_profile(vals, base, d_old, d_new, rmax, normal=False, g_old=None, g_new=None):
    """Relief of the old letters (vals - base) as a function of the distance to their edge, re-applied
    along the edge of the new letters. Normal maps: relief projected on the outward edge direction."""
    delta = vals - base
    if normal:
        proj = delta[..., 0] * g_old[0] + delta[..., 1] * g_old[1]
        src = proj[..., None]
    else:
        src = delta
    bins = np.round(np.clip(d_old, -rmax, rmax) * 2) / 2
    keys = np.unique(bins)
    prof = np.array([src[bins == k].mean(0) if (bins == k).sum() > 5 else np.zeros(src.shape[-1]) for k in keys])
    b_new = np.round(np.clip(d_new, -rmax, rmax) * 2) / 2
    idx = np.clip(np.searchsorted(keys, b_new), 0, len(keys) - 1)
    add = prof[idx]
    out = base.copy()
    if normal:
        out[..., 0] += add[..., 0] * g_new[0]
        out[..., 1] += add[..., 0] * g_new[1]
    else:
        out += add
    return out


def aux_apply(fam, role, how, el, cov_base, hole_base, legend_base=None):
    """Keep an auxiliary map in step with an edited legend (opacity cut-outs, normal/AO flattening)."""
    arr = fam.maps[role]
    H, W = arr.shape[:2]
    bh, bw = fam.base_shape
    cov = np.asarray(Image.fromarray((cov_base * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS), float) / 255.0
    hole = np.asarray(Image.fromarray(hole_base.astype(np.uint8) * 255).resize((W, H), Image.NEAREST)) > 0
    sy, sx = box_slices(fam.scale(role, el["box"]))
    if how == "mask_from_text":       # opacity = new letters (alpha channel stays as original)
        v = (cov[sy, sx] * 255).round().astype(np.uint8)
        for ch in range(3):
            arr[sy, sx, ch] = v
    elif how == "flatten_hole":       # normal/AO/roughness: remove the old letter relief where the legend was erased
        crop = arr[sy, sx, :3].copy()
        h = dilate(hole[sy, sx], 1)
        arr[sy, sx, :3] = inpaint(crop, h, fam.rng, iters=200, grain=0.5).astype(np.uint8)
    elif how in ("edge_profile", "edge_profile_normal"):  # letters embossed in normal/AO/roughness maps
        leg = np.asarray(Image.fromarray(legend_base.astype(np.uint8) * 255).resize((W, H), Image.NEAREST)) > 0
        rmax = max(2, int(round(el.get("relief_px", 5) * W / fam.base_shape[1])))
        old = leg[sy, sx]
        new = cov[sy, sx] > 0.5
        vals = arr[sy, sx, :3].astype(np.float64)
        base = inpaint(vals, dilate(old | new, rmax), fam.rng, iters=250, grain=0.6)
        d_old, d_new = signed_distance(old, rmax), signed_distance(new, rmax)
        if how == "edge_profile_normal":
            res = edge_profile(vals, base, d_old, d_new, rmax, True, edge_dir(old.astype(float)), edge_dir(cov[sy, sx]))
        else:
            res = edge_profile(vals, base, d_old, d_new, rmax)
        arr[sy, sx, :3] = np.clip(np.round(res), 0, 255).astype(np.uint8)
    elif how == "gradient_normal":  # small printed text embossed in a normal map: relief = k * gradient(text coverage)
        leg = np.asarray(Image.fromarray(legend_base.astype(np.uint8) * 255).resize((W, H), Image.NEAREST)) > 0
        r = max(1, int(round(el.get("relief_px", 2) * W / fam.base_shape[1])))
        old = leg[sy, sx].astype(float)
        newc = cov[sy, sx]
        vals = arr[sy, sx, :3].astype(np.float64)
        base = inpaint(vals, dilate(old > 0, r + 1), fam.rng, iters=200, grain=0.6)
        blur = lambda c: box_blur(c[..., None], 1)[..., 0]
        gy_o, gx_o = np.gradient(blur(old))
        gy_n, gx_n = np.gradient(blur(newc))
        dx, dy = vals[..., 0] - base[..., 0], vals[..., 1] - base[..., 1]
        num = (dx * gx_o + dy * gy_o).sum()
        den = (gx_o ** 2 + gy_o ** 2).sum() + 1e-9
        k = num / den * el.get("relief_gain", 1.0)  # least-squares amplitude (and sign) of the old relief
        out = base.copy()
        out[..., 0] += k * gx_n
        out[..., 1] += k * gy_n
        el.setdefault("_relief_k", {})[role] = round(float(k), 2)
        arr[sy, sx, :3] = np.clip(np.round(out), 0, 255).astype(np.uint8)
    elif how == "keep":
        pass
    else:
        raise SystemExit(f"unknown aux rule {how}")


def op_glyph(fam: Family, el):
    """Letters cut by the opacity map: rewrite the mask and paint the letter colour under it (+bleed)."""
    orole, crole = el.get("opacity_map", "opacity"), el.get("map", "color")
    op_img, col = fam.maps[orole], fam.maps[crole]
    shape_c = col.shape[:2]
    cov = text_coverage(el, shape_c)
    sy, sx = box_slices(el["box"])
    old = np.asarray(Image.fromarray(fam.orig[orole][..., 0]).resize(shape_c[::-1], Image.NEAREST))[sy, sx] > 128
    letter_sel = np.zeros(shape_c, bool)
    letter_sel[sy, sx] = old
    # opacity at its own resolution
    H, W = op_img.shape[:2]
    cov_o = np.asarray(Image.fromarray((cov * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS), float) / 255.0
    oy, ox = box_slices(fam.scale(orole, el["box"]))
    base = el.get("mask_base", 0)
    newmask = np.maximum(base, cov_o[oy, ox] * 255).round().astype(np.uint8)
    for ch in range(3):
        op_img[oy, ox, ch] = newmask
    ink = dilate(cov[sy, sx] > 0.02, el.get("bleed", 3))
    rgb = col[..., :3]
    lc = grain_color(rgb, letter_sel, fam.rng, ink.sum()) if "color" not in el else np.tile(np.array(el["color"], float), (ink.sum(), 1))
    crop = rgb[sy, sx].copy()
    crop[ink] = lc.clip(0, 255).astype(np.uint8)
    rgb[sy, sx] = crop


def op_fill(fam: Family, el):
    role = el.get("map", "color")
    rgb = fam.maps[role][..., :3]
    for b in el["boxes"]:
        sy, sx = box_slices(b)
        if "bg_color" in el:
            rgb[sy, sx] = np.array(el["bg_color"], np.uint8)
        else:
            by, bx = box_slices(el["bg_from"])
            bg = np.zeros(rgb.shape[:2], bool)
            bg[by, bx] = True
            n = (b[2] - b[0]) * (b[3] - b[1])
            rgb[sy, sx] = grain_color(rgb, bg, fam.rng, n).reshape(b[3] - b[1], b[2] - b[0], 3).clip(0, 255).astype(np.uint8)


def op_copy(fam: Family, el):
    for role in el.get("maps", ["color"]):
        src = fam.scale(role, el["src"])
        dst = fam.scale(role, el["dst"])
        sy, sx = box_slices(src)
        patch = fam.orig[role][sy, sx].copy()
        dw, dh = dst[2] - dst[0], dst[3] - dst[1]
        if patch.shape[1] != dw or patch.shape[0] != dh:
            patch = np.array(Image.fromarray(patch).resize((dw, dh), Image.LANCZOS))
        fam.maps[role][box_slices(dst)] = patch


OPS = {"panel": op_panel, "glyph": op_glyph, "fill": op_fill, "copy": op_copy}


# ---------------------------------------------------------------- commands
def cmd_build(fam: Family, only=None):
    done = []
    for el in fam.layout["elements"]:
        if only and el["id"] not in only:
            continue
        if el.get("op", "panel") in OPS:
            OPS[el.get("op", "panel")](fam, el)
            done.append(el["id"])
    fam.save()
    lines = {el["id"]: el.get("_lines") for el in fam.layout["elements"] if el.get("_lines")}
    (fam.path.parent / "rendered_lines.json").write_text(json.dumps(lines, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    print(f"{fam.layout['family']}: {len(done)} elements -> " + ", ".join(m["out"] for m in fam.layout["maps"].values() if m.get("out")))


def element_boxes(el):
    if "box" in el:
        return [el["box"]]
    if el.get("op") == "fill":
        return el["boxes"]
    if el.get("op") == "copy":
        return [el["dst"]]
    return []


def cmd_preview(fam: Family, out_dir: Path, only=None, scale=2):
    out_dir.mkdir(parents=True, exist_ok=True)
    roles = [r for r, m in fam.layout["maps"].items() if m.get("out")]
    built = {r: np.array(Image.open(REPO / fam.layout["maps"][r]["out"]).convert("RGBA")) for r in roles}
    n = 0
    for el in fam.layout["elements"]:
        if only and el["id"] not in only:
            continue
        for b in element_boxes(el):
            tiles = []
            for r in roles:
                bb = fam.scale(r, b)
                m = 4
                H, W = built[r].shape[:2]
                bx = (max(bb[0] - m, 0), max(bb[1] - m, 0), min(bb[2] + m, W), min(bb[3] + m, H))
                a = Image.fromarray(fam.orig[r]).crop(bx).convert("RGB")
                c = Image.fromarray(built[r]).crop(bx).convert("RGB")
                if np.array_equal(np.asarray(a), np.asarray(c)) and r != "color":
                    continue
                s = scale if max(a.size) < 600 else 1
                w, h = a.width * s, a.height * s
                t = Image.new("RGB", (w * 2 + 6, h + 14), (0, 0, 0))
                t.paste(a.resize((w, h), Image.NEAREST), (0, 14))
                t.paste(c.resize((w, h), Image.NEAREST), (w + 6, 14))
                ImageDraw.Draw(t).text((2, 1), f"{el['id']} [{r}]", fill=(255, 255, 0))
                tiles.append(t)
            if tiles:
                W = max(t.width for t in tiles)
                sheet = Image.new("RGB", (W, sum(t.height for t in tiles)), (0, 0, 0))
                y = 0
                for t in tiles:
                    sheet.paste(t, (0, y))
                    y += t.height
                sheet.save(out_dir / f"{el['id']}.png")
                n += 1
    print(f"{n} previews -> {out_dir}")


def cmd_grid(fam: Family, role, box, out: Path, step=None, scale=None):
    """Crop of the ORIGINAL with a pixel grid, to read coordinates when authoring the layout."""
    x0, y0, x1, y1 = box
    a = Image.fromarray(fam.orig[role]).crop((x0, y0, x1, y1))
    bg = Image.new("RGBA", a.size, (90, 90, 90, 255))
    bg.alpha_composite(a)
    w, h = a.size
    s = scale or max(1, int(1200 / max(w, h)))
    im = bg.convert("RGB").resize((w * s, h * s), Image.NEAREST)
    d = ImageDraw.Draw(im)
    step = step or max(10, int(round(max(w, h) / 12 / 10)) * 10)
    for gx in range((x0 // step + 1) * step, x1, step):
        X = (gx - x0) * s
        d.line([(X, 0), (X, im.height)], fill=(0, 255, 255), width=1)
        d.text((X + 2, 2), str(gx), fill=(255, 255, 0))
    for gy in range((y0 // step + 1) * step, y1, step):
        Y = (gy - y0) * s
        d.line([(0, Y), (im.width, Y)], fill=(0, 255, 255), width=1)
        d.text((2, Y + 2), str(gy), fill=(255, 255, 0))
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print(out)


def cmd_regions(fam: Family):
    """UV evidence: instanced West Coast meshes whose UV footprint covers each edited box."""
    sys.path.insert(0, str(REPO / "tools/production"))
    import asset_usage
    import dae_uv
    lay = fam.layout
    mats = lay["materials"]
    tex = lay.get("usage_texture") or Path(lay["maps"][lay.get("base_map", "color")]["original"]).stem
    use = asset_usage.usage([tex])[tex]
    dest = REPO / "source/originals/meshes/phase6"
    keys = list(use["instanced_meshes"])
    paths = asset_usage.extract(keys, dest)
    H, W = fam.base_shape
    foot = {}
    for k, p in zip(keys, paths):
        try:
            mask, items = dae_uv.footprint([p], mats, (W, H))
        except Exception as e:  # noqa: BLE001 - malformed meshes are reported, not fatal
            print("skip", k, e)
            continue
        if items:
            foot[k] = (use["instanced_meshes"][k]["wcusa_instances"], mask)
    thr = lay.get("uv_min_coverage", 0.4)
    out = {"_doc": "Generated by tools/production/compose.py regions: instanced West Coast meshes whose UV footprint "
                   f"(materials {mats}) covers each edited box (coverage >= {thr}).", "elements": []}
    regs, missing = {}, []
    for el in lay["elements"]:
        for i, b in enumerate(element_boxes(el)):
            x0, y0, x1, y1 = b
            meshes = {}
            for k, (inst, mask) in foot.items():
                c = float(mask[y0:y1, x0:x1].mean())
                if c >= thr:
                    meshes[k.split("::")[1].rsplit("/", 1)[-1]] = {"instances": inst, "coverage": round(c, 3)}
            rid = el["id"] if i == 0 else f"{el['id']}_{i}"
            out["elements"].append({"id": rid, "box": b, "meshes": meshes})
            if not meshes and not el.get("evidence"):
                missing.append(rid)
                continue
            src = ("UV of " + ", ".join(f"{m} ({v['instances']} inst.)" for m, v in sorted(meshes.items())[:6])
                   + (" …" if len(meshes) > 6 else "")) if meshes else el["evidence"]
            for role in lay.get("region_maps", ["color"]):
                bb = fam.scale(role, b)
                regs.setdefault(role, []).append({"id": rid, "x": bb[0], "y": bb[1], "width": bb[2] - bb[0],
                                                  "height": bb[3] - bb[1], "source": src + "; Phase 6"})
    (fam.path.parent / "regions.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf8")
    if missing:
        print("NO UV EVIDENCE (not registered):", missing)
    allowed_p = REPO / "tools/validation/config/allowed_regions.json"
    allowed = json.loads(allowed_p.read_text(encoding="utf8"))
    for role, rs in regs.items():
        key = Path(lay["maps"][role]["original"]).stem
        H2, W2 = fam.maps[role].shape[:2]
        allowed[key] = {"size": [W2, H2], "regions": rs}
    allowed_p.write_text(json.dumps(allowed, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
    print(f"regions: {sum(len(v) for v in regs.values())} registered, {len(missing)} without evidence")
    return missing


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("layout")
    ap.add_argument("cmd", choices=["build", "preview", "regions", "grid"])
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--map", default="color")
    ap.add_argument("--box", nargs=4, type=int)
    ap.add_argument("--step", type=int)
    ap.add_argument("--scale", type=int)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    fam = Family(Path(a.layout).resolve())
    tmp = REPO / "working/temporary" / fam.layout["family"]
    if a.cmd == "build":
        cmd_build(fam, a.only)
    elif a.cmd == "preview":
        cmd_preview(fam, Path(a.out) if a.out else tmp / "preview", a.only)
    elif a.cmd == "regions":
        return 1 if cmd_regions(fam) else 0
    else:
        cmd_grid(fam, a.map, a.box, Path(a.out) if a.out else tmp / f"grid_{a.map}_{'_'.join(map(str, a.box))}.png", a.step, a.scale)
    return 0


if __name__ == "__main__":
    sys.exit(main())
