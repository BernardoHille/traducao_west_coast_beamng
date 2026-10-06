"""Rewrite the words of glyph-built signs (Phase 6): new letter quads in the plane of the old ones.

A sign line (e.g. MOTEL) is a row of letter quads of material clutter_commercial, each pointing at one cell
of an alphabet row of the atlas (see glyph_signs.py). For each line to translate, on every face of the sign:

  * the old quads are deleted (all layers: fill, outline layer `E` behind `F`, the two `&` layers);
  * the new text is laid out in the line's own frame (atlas px units along the old letters): same cell
    padding and letter gap as the original, centred on the old line (or left/right aligned), condensed in X
    when longer than the old span (and shrunk uniformly below 70 % condensing);
  * accented letters = base letter + an accent quad pointing at an accent cell drawn in a free part of the
    atlas (`accents` in the spec, drawn by compose.py op `accent`);
  * vertices reuse the normal / colour / lightmap values of the quads they replace; the rest of the mesh is
    untouched (other materials, nodes, LOD and collision byte-identical).

    python tools/production/glyph_rewrite.py build working/layered/glyph_signs/spec.json [--only s_motel_sign]

Inputs are the extracted originals (source/originals/meshes/phase6); outputs go to the spec's out_dir.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
import glyph_signs as G  # noqa: E402

ACCENT_OF = {"́": "acute", "̂": "circ", "̃": "tilde", "̧": "cedil"}


def split_char(ch):
    """'Ã' -> ('A', 'tilde'); 'Ç' -> ('C', 'cedil'); 'A' -> ('A', None)."""
    d = unicodedata.normalize("NFD", ch)
    base = d[0]
    acc = None
    for m in d[1:]:
        acc = ACCENT_OF.get(m, acc)
    return base, acc


def compact(s):
    return re.sub(r"\s+", "", s)


# ---------------------------------------------------------------- frames
def affine(q):
    """px -> xyz affine map of a quad: P = x*M[0] + y*M[1] + M[2]."""
    px = q["uv_px"].reshape(-1, 2)
    P = q["tris"].reshape(-1, 3)
    A = np.c_[px, np.ones(len(px))]
    return np.linalg.lstsq(A, P, rcond=None)[0]


class Frame:
    def __init__(self, q):
        M = affine(q)
        self.O, self.R, self.D = M[2], M[0], M[1]
        n = np.cross(self.R, self.D)
        self.n = n / np.linalg.norm(n)
        self.B = np.c_[self.R, self.D]

    def xyd(self, P):
        P = np.atleast_2d(P) - self.O
        XY = np.linalg.lstsq(self.B, P.T, rcond=None)[0].T
        depth = (P - XY @ self.B.T) @ self.n
        return XY, depth

    def world(self, X, Y, depth=0.0):
        return self.O + self.R * X + self.D * Y + self.n * depth


def quad_box(fr, q):
    """X range / Y range / depth of a quad's cell rect in the frame."""
    M = affine(q)
    x0, y0, x1, y1 = q["rect"]
    pts = np.array([x0 * M[0] + y0 * M[1] + M[2], x1 * M[0] + y1 * M[1] + M[2]])
    XY, d = fr.xyd(np.r_[pts, q["tris"].reshape(-1, 3)])
    return {"Xa": XY[0, 0], "Xb": XY[1, 0], "Ya": XY[0, 1], "Yb": XY[1, 1], "depth": float(np.median(d[2:]))}


# ---------------------------------------------------------------- planning
def collect(quads):
    """Lines (main fonts) + layer quads (E outline, SYM &) per face, using glyph_signs decoding."""
    lines = G.lines_of(quads)
    punct = lambda l: len(l.get("stacks") or l["quads"]) == 1 and not l["text"].isalnum()
    main = [l for l in lines if l["font"] not in ("E", "SYM") and not punct(l)]
    layers = [q for l in lines if l["font"] in ("E", "SYM") or punct(l) for q in l["quads"]]
    return main, layers


def vertical_lines(main):
    """Merge single-letter lines stacked vertically (same face/font/column) into vertical lines."""
    nst = lambda l: len(l.get("stacks") or [[q] for q in l["quads"]])
    singles = [l for l in main if nst(l) == 1]
    rest = [l for l in main if nst(l) > 1]
    used = set()
    out = []
    for i, a in enumerate(singles):
        if i in used:
            continue
        qa = a["quads"][0]
        col = [i]
        for j, b in enumerate(singles):
            if j <= i or j in used or b["quads"][0]["rn"] @ qa["rn"] < 0.9 or b["font"] != a["font"]:
                continue
            qb = b["quads"][0]
            d = qb["centroid"] - qa["centroid"]
            if abs(d @ qa["dir_u"]) < 0.3 * qa["h3d"] and abs(d @ np.cross(qa["dir_u"], qa["dir_v"])) < 0.05:
                col.append(j)
        if len(col) > 1:
            used.update(col)
            sts = [(singles[k].get("stacks") or [singles[k]["quads"]])[0] for k in col]
            sts.sort(key=lambda st: -(st[0]["centroid"] @ qa["dir_v"]))
            out.append({"face": a["face"], "font": a["font"], "text": "".join(st[0]["char"] for st in sts),
                        "quads": [q for st in sts for q in st], "stacks": sts,
                        "right": a["right"], "up": a["up"], "vertical": True})
    return rest + out + [l for k, l in enumerate(singles) if k not in used]


def plan_line(line, layers, new_text, opt, accents):
    """New quads for one line on one face. Returns (deleted quads, new quads)."""
    font = line["font"]
    F = G.FONTS[font]
    stacks_in = line.get("stacks") or [[q] for q in line["quads"]]
    qs = [st[0] for st in stacks_in]
    big = max(stacks_in, key=len)

    def single(q):  # some designers put two letters in one quad ("ST"): not a reference for frame or padding
        a_, b_ = F["letters"].get(q["char"], (0, 1e9))
        return (q["rect"][2] - q["rect"][0]) <= 1.6 * (b_ - a_) + 6
    ref_q = next((q for q in qs if single(q)), qs[0])
    fr = Frame(ref_q)
    ref_box = quad_box(fr, big[0])
    dups = [{"src": q, "depth": quad_box(fr, q)["depth"] - ref_box["depth"]} for q in big[1:]]
    vertical = line.get("vertical", False)
    # companion layers of this line
    boxes = [quad_box(fr, q) for q in qs]
    Ymin = min(min(b["Ya"], b["Yb"]) for b in boxes)
    Ymax = max(max(b["Ya"], b["Yb"]) for b in boxes)
    hcell = Ymax - Ymin
    e_layers, amp = [], []
    for q in layers:
        if q["rn"] @ line["quads"][0]["rn"] < 0.9 or q.get("_used"):
            continue
        b = quad_box(fr, q)
        if abs(b["depth"]) > 0.08:
            continue
        yc = (b["Ya"] + b["Yb"]) / 2
        if q["font"] == "E":
            for qb, bb in zip(qs, boxes):
                if abs((b["Xa"] + b["Xb"]) / 2 - (bb["Xa"] + bb["Xb"]) / 2) < 6 and abs(yc - (bb["Ya"] + bb["Yb"]) / 2) < 0.4 * hcell:
                    e_layers.append((q, b, qb, bb))
                    q["_used"] = True
                    break
        elif (q["font"] == "SYM" or not q["char"].isalnum()) and Ymin - 0.3 * hcell < yc < Ymax + 0.3 * hcell and not vertical:
            xs = [x for bb in boxes for x in (bb["Xa"], bb["Xb"])]
            if min(xs) - 3 * hcell < b["Xa"] < max(xs) + 3 * hcell:
                amp.append((q, b))
                q["_used"] = True
    deleted = list(line["quads"]) + [e[0] for e in e_layers] + [a[0] for a in amp]
    # E layer template (offset of the outline layer relative to its fill letter)
    e_tpl = None
    if e_layers:
        dY = np.median([b["Ya"] - q["rect"][1] for q, b, _, _ in e_layers])
        dd = np.median([b["depth"] - bb["depth"] for _, b, _, bb in e_layers])
        e_tpl = {"dY": float(dY), "depth": float(dd), "src": e_layers[0][0]}
    # & template
    sym_tpl = {}
    for chs in {q["char"] for q, _ in amp}:
        grp = [(q, b) for q, b in amp if q["char"] == chs]
        x_first = min(b["Xa"] for _, b in grp)  # several separators of the same kind: template = the first one
        grp = [(q, b) for q, b in grp if b["Xa"] < x_first + 0.5 * (b["Xb"] - b["Xa"]) + 1]
        Xs = min(b["Xa"] for _, b in grp)
        sym_tpl[chs] = {"left": Xs, "width": max(b["Xb"] for _, b in grp) - Xs,
                        "layers": [{"q": q, "rect": q["rect"], "dXa": b["Xa"] - Xs, "dXb": b["Xb"] - Xs, "Ya": b["Ya"], "Yb": b["Yb"],
                                    "depth": b["depth"]} for q, b in grp]}
    # original stacks in reading order (letters + symbols)
    stacks = [(b["Xa"], b["Xb"]) for b in boxes] + [(b_["Xa"], b_["Xb"]) for _, b_ in amp]
    # cell padding of the designer's quads vs the run cells
    pl = np.median([q["rect"][0] - F["letters"][q["char"]][0] for q in qs if q["char"] in F["letters"] and single(q)] or [-1])
    pr = np.median([q["rect"][2] - F["letters"][q["char"]][1] for q in qs if q["char"] in F["letters"] and single(q)] or [2])
    cy0 = float(np.median([q["rect"][1] for q in qs]))
    cy1 = float(np.median([q["rect"][3] for q in qs]))
    main_depth = float(np.median([b["depth"] for b in boxes]))
    Ya_line = float(np.median([b["Ya"] for b in boxes]))  # Y of cell top in the frame
    dYmain = Ya_line - cy0  # frame Y = atlas y + dYmain

    runs = sorted(list(F["letters"].values()) + list(F.get("extra", {}).values()))

    def cell(ch):
        a, b = F["letters"][ch]
        prev_end = max([r[1] for r in runs if r[1] <= a] or [a - 40])
        next_start = min([r[0] for r in runs if r[0] >= b] or [b + 40])
        # padding of the original quads, but never past the middle of the gap to the neighbouring glyph
        return max(a + pl, (prev_end + a) / 2), cy0, min(b + pr, (b + next_start) / 2), cy1

    toks = list(new_text)
    if not vertical:
        st = sorted(stacks)
        gaps = [st[i + 1][0] - st[i][1] for i in range(len(st) - 1)]
        letter_gaps = [g for g in gaps if g < 0.35 * hcell]
        word_gaps = [g for g in gaps if g >= 0.35 * hcell]
        g_letter = float(np.median(letter_gaps)) if letter_gaps else 0.0
        g_space = float(np.median(word_gaps)) if word_gaps else 0.33 * hcell
        widths = []
        for t in toks:
            if t == " ":
                widths.append(None)
            elif t in sym_tpl:
                widths.append(sym_tpl[t]["width"])
            elif t == "-":
                hb = accents[f"{font}:hyphen"]["box"]
                widths.append(1.6 * (hb[2] - hb[0]))
            else:
                c = cell(split_char(t)[0])
                widths.append(c[2] - c[0])
        total, prev = 0.0, None
        for w in widths:
            if w is None:
                total += g_space - g_letter if prev is not None else 0
            else:
                total += (g_letter if prev is not None else 0) + w
            prev = w
        Xmin, Xmax = min(s[0] for s in stacks), max(s[1] for s in stacks)
        span = (Xmax - Xmin) * opt.get("span", 1.0)
        sx = min(1.0, span / total) if total > 0 else 1.0
        kmin = opt.get("kmin", 0.7)
        sy = 1.0 if sx >= kmin else sx / kmin
        align = opt.get("align", "center")
        width = total * sx
        Xc = (Xmin + Xmax) / 2 + opt.get("dx", 0.0)
        X0 = Xmin if align == "left" else (Xmax - width if align == "right" else Xc - width / 2)
        Yc = (Ymin + Ymax) / 2
        place = []  # (token, Xa, Xb)
        x, prev = X0, None
        for t, w in zip(toks, widths):
            if w is None:
                x += (g_space - g_letter) * sx
                prev = None
                continue
            if prev is not None:
                x += g_letter * sx
            place.append((t, x, x + w * sx))
            x += w * sx
            prev = t
        mapY = lambda y: Yc + (y + dYmain - Yc) * sy
        mapYf = lambda Y: Yc + (Y - Yc) * sy
    else:
        # vertical: letters stacked down the column, uniform scale
        st = sorted([(b["Ya"], b["Yb"]) for b in boxes])
        gaps = [st[i + 1][0] - st[i][1] for i in range(len(st) - 1)]
        g_letter = float(np.median(gaps)) if gaps else 0.0
        hs = [cy1 - cy0 if t != " " else opt.get("vspace", 0.75) * (cy1 - cy0) for t in toks]
        total = sum(hs) + g_letter * (len(toks) - 1)
        spanY = max(s[1] for s in st) - min(s[0] for s in st)
        s = min(1.0, spanY / total)
        Xcol = float(np.median([(b["Xa"] + b["Xb"]) / 2 for b in boxes]))
        Y0 = (min(s_[0] for s_ in st) + max(s_[1] for s_ in st)) / 2 - total * s / 2
        place = []
        y = Y0
        for t, h in zip(toks, hs):
            if t != " ":
                c = cell(split_char(t)[0])
                w = (c[2] - c[0]) * s
                place.append((t, Xcol - w / 2, Xcol + w / 2, y, y + h * s))
            y += (h + g_letter) * s
        sx = sy = s
    # ---------------------------------------------------------------- emit quads
    new = []

    def emit(Xa, Xb, Ya, Yb, rect, depth, src):
        new.append({"frame": fr, "Xa": Xa, "Xb": Xb, "Ya": Ya, "Yb": Yb, "rect": rect, "depth": depth, "src": src})

    for p in place:
        t = p[0]
        if t in sym_tpl:
            for L in sym_tpl[t]["layers"]:
                if vertical:
                    raise SystemExit("& in a vertical line")
                emit(p[1] + L["dXa"] * sx, p[1] + L["dXb"] * sx, mapYf(L["Ya"]), mapYf(L["Yb"]), L["rect"], L["depth"], L["q"])
            continue
        if t == "-":
            A = accents[f"{font}:hyphen"]
            hb = A["box"]
            hw, hh = (hb[2] - hb[0]) * sx, (hb[3] - hb[1]) * sy
            xm = (p[1] + p[2]) / 2
            ym = mapY((A["ink_top"] + A["ink_bottom"]) / 2)
            emit(xm - hw / 2, xm + hw / 2, ym - hh / 2, ym + hh / 2, hb, main_depth, qs[0])
            for dl in dups:
                emit(xm - hw / 2, xm + hw / 2, ym - hh / 2, ym + hh / 2, hb, main_depth + dl["depth"], dl["src"])
            continue
        base, acc = split_char(t)
        c = cell(base)
        if vertical:
            Xa, Xb, Ya, Yb = p[1], p[2], p[3], p[4]
            ty = lambda y: Ya + (y - c[1]) * sy
        else:
            Xa, Xb = p[1], p[2]
            Ya, Yb = mapY(c[1]), mapY(c[3])
            ty = mapY
        if e_tpl is not None:
            ec = (c[0], c[1] - (G.FONTS["E"].get("dy_to_main", 91)), c[2], c[3] - (G.FONTS["E"].get("dy_to_main", 91)))
            emit(Xa, Xb, Ya, Yb, ec, main_depth + e_tpl["depth"], e_tpl["src"])
        emit(Xa, Xb, Ya, Yb, c, main_depth, qs[0])
        for dl in dups:
            emit(Xa, Xb, Ya, Yb, c, main_depth + dl["depth"], dl["src"])
        if acc:
            A = accents.get(f"{font}:{acc}")
            if A is None:
                raise SystemExit(f"no accent cell for {font}:{acc}")
            ax0, ay0, ax1, ay1 = A["box"]
            aw, ah = (ax1 - ax0) * sx, (ay1 - ay0) * sy
            xc = (Xa + Xb) / 2 + A.get("dx", 0) * (Xb - Xa)
            if acc == "cedil":
                top = ty(A["ink_bottom"]) - A.get("overlap", 1) * sy
                Ybox = (top, top + ah)
            else:
                bot = ty(A["ink_top"]) - A.get("gap", 3) * sy
                Ybox = (bot - ah, bot)
            if e_tpl is not None and f"E:{acc}" in accents:
                E2 = accents[f"E:{acc}"]
                ew, eh = (E2["box"][2] - E2["box"][0]) * sx, (E2["box"][3] - E2["box"][1]) * sy
                ym = (Ybox[0] + Ybox[1]) / 2
                emit(xc - ew / 2, xc + ew / 2, ym - eh / 2, ym + eh / 2, E2["box"], main_depth + e_tpl["depth"], e_tpl["src"])
            emit(xc - aw / 2, xc + aw / 2, Ybox[0], Ybox[1], A["box"], main_depth, qs[0])
            for dl in dups:
                emit(xc - aw / 2, xc + aw / 2, Ybox[0], Ybox[1], A["box"], main_depth + dl["depth"], dl["src"])
    return deleted, new, {"sx": round(float(sx), 3), "sy": round(float(sy), 3)}


RS_DIGITS = {"1": (359, 375), "2": (403, 435), "3": (458, 491), "4": (511, 549), "5": (572, 604), "6": (627, 661),
             "7": (681, 712), "8": (734, 768), "9": (790, 824), "0": (848, 882)}  # t_roadsigns digit row (y 11..74)


def rs_cell(d):
    a, b = RS_DIGITS[d]
    c = (a + b) / 2
    return (c - 26, 11, c + 26, 74)


def plan_clearance(path, quads, main, value, accents):
    """'MAX CLEARANCE  13 FT 1 IN' panels: digits of material roadsigns + FT/IN of clutter -> metric 'd,d m'.

    For every FT label: the roadsigns digit quads beside it (same plane) are re-targeted to the new digits, a
    comma (clutter cell) is added between them, FT becomes a lowercase 'm' on the baseline, and the inch part
    (digit + IN) is removed."""
    rq = G.read_quads(path, "roadsigns", (2048, 1024))
    deleted, new, rep = [], [], []
    a, b = value.split(",")
    LC = G.FONTS["LC"]
    for ft in [l for l in main if l["text"] == "FT"]:
        q_ft = ft["quads"][0]
        fr = Frame(q_ft)
        c = np.mean([q["centroid"] for q in ft["quads"]], 0)
        digs = []
        for q in rq:
            x0_, y0_, x1_, y1_ = q["rect"]
            if not (y0_ > 0 and y1_ < 90 and 320 < (x0_ + x1_) / 2 < 900):
                continue  # only the digit row of t_roadsigns
            if np.linalg.norm(q["centroid"] - c) < 1.5 and abs((q["centroid"] - q_ft["centroid"]) @ fr.n) < 0.05:
                bx = quad_box(fr, q)
                digs.append((bx["Xa"], q, bx))
        ins = [l for l in main if l["text"] == "IN" and np.linalg.norm(np.mean([q["centroid"] for q in l["quads"]], 0) - c) < 1.5]
        digs.sort(key=lambda t: t[0])
        fx = quad_box(fr, q_ft)["Xa"]
        left = [d for d in digs if d[0] < fx]
        right = [d for d in digs if d[0] > fx]
        if len(left) != 2 or not ins:
            raise SystemExit(f"clearance panel at {np.round(c, 1)}: digits {len(left)}+{len(right)}, IN {len(ins)}")
        (_, q1, b1), (_, q2, b2) = left
        h = b1["Yb"] - b1["Ya"]
        w = b1["Xb"] - b1["Xa"]
        com = accents["R1:comma"]
        cw = 0.32 * w
        # digit 1 in place, comma, digit 2 shifted right by the comma width
        new.append({"frame": fr, "Xa": b1["Xa"], "Xb": b1["Xb"], "Ya": b1["Ya"], "Yb": b1["Yb"], "rect": rs_cell(a), "depth": b1["depth"],
                    "src": q1, "size": (2048, 1024)})
        cx = b1["Xb"] - 0.12 * w
        new.append({"frame": fr, "Xa": cx, "Xb": cx + cw, "Ya": b1["Yb"] - 0.30 * h, "Yb": b1["Yb"] + 0.05 * h, "rect": com["box"],
                    "depth": b1["depth"], "src": q_ft})
        x2 = b2["Xa"] + cw * 0.6
        new.append({"frame": fr, "Xa": x2, "Xb": x2 + w, "Ya": b2["Ya"], "Yb": b2["Yb"], "rect": rs_cell(b), "depth": b2["depth"],
                    "src": q2, "size": (2048, 1024)})
        # 'm' on the baseline of the digits (x-height ~ 0.45 of the digit height)
        ma, mb = LC["letters"]["m"]
        mrect = (ma - 2, 86, mb + 2, 110)
        mh = 0.42 * (b1["Yb"] - b1["Ya"]) * 0.78
        mw = mh * (mrect[2] - mrect[0]) / (mrect[3] - mrect[1])
        xm = x2 + w + 0.08 * w
        new.append({"frame": fr, "Xa": xm, "Xb": xm + mw, "Ya": b1["Yb"] - 0.10 * h - mh, "Yb": b1["Yb"] - 0.10 * h, "rect": mrect,
                    "depth": quad_box(fr, q_ft)["depth"], "src": q_ft})
        deleted += list(ft["quads"]) + [q1, q2] + [d[1] for d in right] + [q for l in ins for q in l["quads"]]
        rep.append({"face": ft["face"], "old": "13 FT 1 IN", "new": f"{value} m"})
    return deleted, new, rep


DOLLAR = (1732, 0, 1795, 92)  # big '$' cell of the clutter atlas (prices on posters and signs)


def plan_currency(quads):
    """'$' -> 'R$' (rule: R$ without exchange conversion). Each $ quad is split in place: a bold 'R' (R1 font) in the
    left 42 % of its footprint and the '$' squeezed into the rest; height of the R = 62 % of the $ cell, centred."""
    deleted, new = [], []
    Rc = G.FONTS["R1"]["letters"]["R"]
    for q in quads:
        if max(abs(v - d) for v, d in zip(q["rect"], DOLLAR)) > 1.5:
            continue
        fr = Frame(q)
        b = quad_box(fr, q)
        Xa, Xb, Ya, Yb = b["Xa"], b["Xb"], b["Ya"], b["Yb"]
        w, h = Xb - Xa, Yb - Ya
        xr = Xa + 0.42 * w
        rh = 0.62 * h
        ym = (Ya + Yb) / 2 + 0.04 * h
        new.append({"frame": fr, "Xa": Xa + 0.02 * w, "Xb": xr, "Ya": ym - rh / 2, "Yb": ym + rh / 2,
                    "rect": (Rc[0] - 1, 44, Rc[1] + 1, 72), "depth": b["depth"], "src": q})
        new.append({"frame": fr, "Xa": xr - 0.04 * w, "Xb": Xb, "Ya": Ya, "Yb": Yb, "rect": DOLLAR, "depth": b["depth"], "src": q})
        deleted.append(q)
    return deleted, new


DEALER_CELLS = {"A": (3, 64), "F": (322, 371), "I": (510, 542), "M": (718, 785), "N": (799, 852), "O": (865, 921), "P": (933, 986)}
DEALER_Y = (769, 830)  # glyph row of t_billboardsigns_dealers used by the bus shelters (MAP / INFO)


def plan_dealer_word(path, old, new_text):
    """Words of the bus shelters built from glyphs of material m_billboardsigns_dealers (atlas 2048x1024)."""
    qs = G.read_quads(path, "m_billboardsigns_dealers", (2048, 1024))
    for q in qs:
        cx = (q["rect"][0] + q["rect"][2]) / 2
        q["ch"] = next((ch for ch, (a, b) in DEALER_CELLS.items() if a <= cx <= b), "?")
        M = affine(q)
        rn = np.cross(M[0], -M[1])
        q["rn2"] = rn / np.linalg.norm(rn)
    deleted, new, rep = [], [], []
    used = set()
    for i, q in enumerate(qs):
        if i in used:
            continue
        grp = [j for j, r in enumerate(qs) if j not in used and r["rn2"] @ q["rn2"] > 0.9 and abs(r["centroid"][2] - q["centroid"][2]) < 0.05
               and np.linalg.norm(r["centroid"] - q["centroid"]) < 0.5]
        fr = Frame(qs[grp[0]])
        grp.sort(key=lambda j: quad_box(fr, qs[j])["Xa"])
        word = "".join(qs[j]["ch"] for j in grp)
        if word != old:
            continue
        used.update(grp)
        boxes = [quad_box(fr, qs[j]) for j in grp]
        Xmin, Xmax = boxes[0]["Xa"], boxes[-1]["Xb"]
        gaps = [boxes[k + 1]["Xa"] - boxes[k]["Xb"] for k in range(len(boxes) - 1)]
        g = float(np.median(gaps)) if gaps else 0.0
        pad = float(np.median([qs[j]["rect"][2] - qs[j]["rect"][0] - (DEALER_CELLS[qs[j]["ch"]][1] - DEALER_CELLS[qs[j]["ch"]][0]) for j in grp]))
        ws = [DEALER_CELLS[c][1] - DEALER_CELLS[c][0] + pad for c in new_text]
        total = sum(ws) + g * (len(ws) - 1)
        sx = min(1.0, (Xmax - Xmin) / total)
        sy = 1.0 if sx >= 0.7 else sx / 0.7
        Ya, Yb = boxes[0]["Ya"], boxes[0]["Yb"]
        Yc = (Ya + Yb) / 2
        x = (Xmin + Xmax) / 2 - total * sx / 2
        src = qs[grp[0]]
        for c, w in zip(new_text, ws):
            a, b = DEALER_CELLS[c]
            new.append({"frame": fr, "Xa": x, "Xb": x + w * sx, "Ya": Yc + (Ya - Yc) * sy, "Yb": Yc + (Yb - Yc) * sy,
                        "rect": (a - pad / 2, src["rect"][1], b + pad / 2, src["rect"][3]), "depth": boxes[0]["depth"], "src": src,
                        "size": (2048, 1024)})
            x += (w + g) * sx
        deleted += [qs[j] for j in grp]
        rep.append({"face": 0, "old": old, "new": new_text, "sx": round(sx, 3), "sy": round(sy, 3)})
    return deleted, new, rep


def plan_uv_map(path, material, size, mapping):
    """Re-target quads of `material` whose UV rect matches a 'from' rect (±1.5 px) to the 'to' rect (same size);
    geometry unchanged (the quad is rebuilt on its own frame)."""
    qs = G.read_quads(path, material, tuple(size))
    deleted, new, rep = [], [], {}
    for q in qs:
        for m in mapping:
            if max(abs(a - b) for a, b in zip(q["rect"], m["from"])) <= 1.5:
                fr = Frame(q)
                b = quad_box(fr, q)
                new.append({"frame": fr, "Xa": b["Xa"], "Xb": b["Xb"], "Ya": b["Ya"], "Yb": b["Yb"], "rect": tuple(m["to"]),
                            "depth": b["depth"], "src": q, "size": tuple(size)})
                deleted.append(q)
                rep[m["id"]] = rep.get(m["id"], 0) + 1
                break
    return deleted, new, [{"face": 0, "old": k, "new": f"{v} quads"} for k, v in rep.items()]


def plan_sign(quads, spec_lines, accents, path=None):
    main, layers = collect(quads) if quads else ([], [])
    main = vertical_lines(main) if main else []
    deleted, new, report = [], [], []
    def edges(l):
        R = l["right"]
        pts = np.concatenate([q["tris"].reshape(-1, 3) for q in l["quads"]]) @ R
        return pts.min(), pts.max(), l["quads"][0]["h3d"]

    def auto_align(l):
        same = [m for m in main if m["face"] == l["face"] and m is not l and not m.get("vertical") and m["right"] @ l["right"] > 0.95
                and m["font"] == l["font"]]
        if not same:
            return "center"
        a0, a1, h = edges(l)
        L = [abs(edges(m)[0] - a0) < 0.15 * h for m in same]
        R_ = [abs(edges(m)[1] - a1) < 0.15 * h for m in same]
        C = [abs((edges(m)[0] + edges(m)[1]) / 2 - (a0 + a1) / 2) < 0.15 * h for m in same]
        if any(C):
            return "center"
        if any(L):
            return "left"
        if any(R_):
            return "right"
        return "center"
    for sl in spec_lines:
        if sl.get("custom") == "uv_map":
            mp = json.loads((REPO / sl["map_file"]).read_text(encoding="utf8"))["uv_map"]
            d, n, r = plan_uv_map(path, sl["material"], sl["size"], mp)
            deleted += d; new += n; report += r
            continue
        if sl.get("custom") == "dealer_word":
            d, n, r = plan_dealer_word(path, sl["old"], sl["new"])
            deleted += d; new += n; report += r
            continue
        if sl.get("custom") == "currency":
            d, n = plan_currency(quads)
            deleted += d; new += n
            report.append({"face": 0, "old": "$", "new": f"R$ ({len(d)} quads)"})
            continue
        if sl.get("custom") == "clearance":
            d, n, r = plan_clearance(path, quads, main, sl["new"], accents)
            deleted += d; new += n; report += r
            continue
        hits = [l for l in main if compact(l["text"]) == compact(sl["old"]) and (sl.get("face") in (None, l["face"]))]
        if not hits:
            raise SystemExit(f"line {sl['old']!r} not found; lines: {[l['text'] for l in main]}")
        for l in hits:
            opt = dict(sl)
            if opt.get("align", "auto") == "auto":
                opt["align"] = auto_align(l)
            # orphans: single letters of the same word that decoded on the other face (flipped quads) - deleted with it
            fr = Frame(l["quads"][0])
            bx = [quad_box(fr, q) for q in l["quads"]]
            X0, X1 = min(b["Xa"] for b in bx), max(b["Xb"] for b in bx)
            Y0, Y1 = min(b["Ya"] for b in bx), max(b["Yb"] for b in bx)
            for m in main:
                if m is l or m.get("vertical") or len(m.get("stacks") or m["quads"]) != 1 or m["font"] != l["font"] or m.get("_absorbed"):
                    continue
                if opt.get("orphans", True) is False:
                    break
                ob = [quad_box(fr, q) for q in m["quads"]]
                xc = np.mean([(b["Xa"] + b["Xb"]) / 2 for b in ob]); yc = np.mean([(b["Ya"] + b["Yb"]) / 2 for b in ob])
                if X0 <= xc <= X1 and Y0 <= yc <= Y1 and all(abs(b["depth"]) < 0.05 for b in ob):
                    m["_absorbed"] = True
                    deleted += list(m["quads"])
                    report.append({"face": m["face"], "old": m["text"], "new": "(absorbed into " + l["text"] + ")"})
            d, n, r = plan_line(l, layers, sl["new"], opt, accents)
            r["align"] = opt["align"]
            deleted += d
            new += n
            report.append({"face": l["face"], "old": l["text"], "new": sl["new"], **r})
    return deleted, new, report


# ---------------------------------------------------------------- COLLADA text surgery
def _array(block, src_id):
    m = re.search(r'(<float_array id="' + re.escape(src_id) + r'-array" count=")(\d+)(">)([^<]*)(</float_array>)', block)
    return m


def write(src_text, quads, deleted, new):
    """Return the new COLLADA text: deleted triangles removed, new quads appended (per geometry/<triangles>)."""
    by_prim = {}
    for q in deleted:
        by_prim.setdefault((q["geometry"], q["prim_index"]), {"del": set(), "new": [], "tpl": q})["del"].update(q["tri_index"])
    for nq in new:
        q = nq["src"]
        by_prim.setdefault((q["geometry"], q["prim_index"]), {"del": set(), "new": [], "tpl": q})["new"].append(nq)
    text = src_text
    for gid in sorted({k[0] for k in by_prim}):
        gs = text.index(f'<geometry id="{gid}"')
        ge = text.index("</geometry>", gs) + len("</geometry>")
        block = text[gs:ge]
        pos_src = re.search(r'<input semantic="POSITION" source="#([^"]+)"', block).group(1)
        m_pos = _array(block, pos_src)
        pos = [float(v) for v in m_pos.group(4).split()]
        tri_iter = list(re.finditer(r'<triangles material="([^"]+)" count="(\d+)">(.*?)</triangles>', block, re.S))
        uv_srcs = None
        edits = []  # (span, replacement) inside block for <triangles>
        uv_add = {}
        for (g, pi), job in sorted(by_prim.items()):
            if g != gid:
                continue
            tm = tri_iter[pi]
            body = tm.group(3)
            inputs = re.findall(r'<input semantic="(\w+)" source="#([^"]+)" offset="(\d+)"(?: set="(\d+)")?/>', body)
            stride = max(int(o) for _, _, o, _ in inputs) + 1
            off = {}
            tex_srcs = []
            for sem, src, o, st in inputs:
                if sem == "TEXCOORD":
                    tex_srcs.append(src)
                    off["TEXCOORD"] = int(o)
                else:
                    off[sem] = int(o)
            if uv_srcs is None:
                uv_srcs = tex_srcs
                for s_ in uv_srcs:
                    am = _array(block, s_)
                    uv_add[s_] = [float(v) for v in am.group(4).split()]
            p = np.array(re.search(r"<p>([^<]*)</p>", body).group(1).split(), dtype=np.int64).reshape(-1, 3, stride)
            keep = np.ones(len(p), bool)
            keep[sorted(job["del"])] = False
            p = p[keep]
            w = job["tpl"]["w"]
            winv = np.linalg.inv(w[:3, :3])
            add = []
            for nq in job["new"]:
                fr = nq["frame"]
                tpl = nq["src"]["idx"][0][0]  # first corner of the replaced quad: normal / colour / other inputs
                x0, y0, x1, y1 = nq["rect"]
                corners = {"TL": (nq["Xa"], nq["Ya"], x0, y0), "BL": (nq["Xa"], nq["Yb"], x0, y1),
                           "BR": (nq["Xb"], nq["Yb"], x1, y1), "TR": (nq["Xb"], nq["Ya"], x1, y0)}
                vid = {}
                for k, (X, Y, ux, uy) in corners.items():
                    P = fr.world(X, Y, nq["depth"])
                    L = winv @ (P - w[:3, 3])
                    vid[k] = len(pos) // 3
                    pos.extend(L.tolist())
                    tid = len(uv_add[uv_srcs[0]]) // 2
                    aw_, ah_ = nq.get("size", (2048, 2048))
                    uv_add[uv_srcs[0]].extend([ux / aw_, 1.0 - uy / ah_])
                    for s_ in uv_srcs[1:]:
                        src_uv = uv_add[s_]
                        t0 = int(tpl[off["TEXCOORD"]])
                        uv_add[s_].extend(src_uv[2 * t0:2 * t0 + 2])
                    vid[k] = (vid[k], tid)
                # winding like the replaced quad
                ref = nq["src"]["tris"][0]
                ref_s = np.cross(ref[1] - ref[0], ref[2] - ref[0]) @ fr.n
                a_ = fr.world(nq["Xa"], nq["Ya"]); b_ = fr.world(nq["Xa"], nq["Yb"]); c_ = fr.world(nq["Xb"], nq["Yb"])
                order = (("TL", "BL", "BR"), ("TL", "BR", "TR"))
                if np.sign(np.cross(b_ - a_, c_ - a_) @ fr.n) != np.sign(ref_s):
                    order = (("TL", "BR", "BL"), ("TL", "TR", "BR"))
                for tri in order:
                    rec = []
                    for k in tri:
                        c = np.array(tpl).copy()
                        c[off["VERTEX"]] = vid[k][0]
                        c[off["TEXCOORD"]] = vid[k][1]
                        rec.append(c)
                    add.append(rec)
            if add:
                p = np.concatenate([p, np.array(add, dtype=np.int64)]) if len(p) else np.array(add, dtype=np.int64)
            new_body = re.sub(r"<p>[^<]*</p>", "<p>" + " ".join(map(str, p.reshape(-1).tolist())) + "</p>", body)
            edits.append((tm.span(), f'<triangles material="{tm.group(1)}" count="{len(p)}">{new_body}</triangles>'))
        for span, rep in sorted(edits, reverse=True):
            block = block[:span[0]] + rep + block[span[1]:]

        def put(block, src_id, vals, stride_):
            m = _array(block, src_id)
            txt = " ".join(f"{v:.7g}" for v in vals)
            block = block[:m.start()] + f'{m.group(1)}{len(vals)}{m.group(3)}{txt}{m.group(5)}' + block[m.end():]
            block = re.sub(r'(<accessor source="#' + re.escape(src_id) + r'-array" count=")(\d+)(")',
                           lambda mm: f"{mm.group(1)}{len(vals) // stride_}{mm.group(3)}", block)
            return block
        block = put(block, pos_src, pos, 3)
        for s_, vals in (uv_add or {}).items():
            block = put(block, s_, vals, 2)
        text = text[:gs] + block + text[ge:]
    return text


def build(spec_path, only=None):
    spec = json.loads(Path(spec_path).read_text(encoding="utf8"))
    accents = spec.get("accents", {})
    if spec.get("accents_file"):
        accents = json.loads((REPO / spec["accents_file"]).read_text(encoding="utf8"))
    out_dir = REPO / spec["out_dir"]
    reports = {}
    for name, s in spec["signs"].items():
        if only and name not in only:
            continue
        src = REPO / s["src"]
        quads = G.read_quads(src)
        deleted, new, rep = plan_sign(quads, s["lines"], accents, src)
        text = write(src.read_text(encoding="utf8"), quads, deleted, new)
        dst = out_dir / s["install"] / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf8", newline="\n")
        reports[name] = {"deleted_quads": len(deleted), "new_quads": len(new), "lines": rep, "out": str(dst.relative_to(REPO))}
        print(name, len(deleted), "->", len(new), [(r["face"], r["new"], r.get("sx"), r.get("sy")) for r in rep])
    return reports


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("spec")
    b.add_argument("--only", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        rep = build(a.spec, a.only)
        out = Path(a.spec).parent / "build_report.json"
        old = json.loads(out.read_text(encoding="utf8")) if out.exists() and a.only else {}
        old.update(rep)
        out.write_text(json.dumps(old, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
