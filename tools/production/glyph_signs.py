"""Signs whose words are built in the MESH from glyph quads (Phase 6, glyph signs).

Each letter of such a sign is a small quad (2 triangles, sometimes with side strips) of material
`clutter_commercial` whose UVs point at one cell of an alphabet row of the atlas; the letter shape comes
from the opacity map. This tool reads those quads from a COLLADA file and renders the sign as the game
shows it (front view), so the words can be read and planned; `rewrite` builds a new .dae with the quads
of chosen letters re-targeted / added / removed.

    python tools/production/glyph_signs.py analyze <mesh.dae> [--out preview.png]

Read-only on the game files: meshes are read from source/originals/meshes (extracted copies).
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
import dae_uv  # noqa: E402

NS = dae_uv.NS
import os
ATLAS = Path(os.environ.get("GLYPH_ATLAS", REPO / "source/originals/png/art_shapes/clutter_commercial_b.color.png"))
OPACITY = Path(os.environ.get("GLYPH_OPACITY", REPO / "source/originals/png/art_shapes/clutter_commercial_o.data.png"))
SIZE = (2048, 2048)


def _floats(t):
    return np.array(t.split(), dtype=np.float64) if t and t.strip() else np.zeros(0)


def read_quads(path, material="clutter_commercial", size=None):
    """Connected triangle groups of `material` (letters), in world space (node matrices applied).

    Returns list of dicts: tris (N,3,3 xyz), uv_px (N,3,2), rect (x0,y0,x1,y1 px), centroid, normal, area,
    geometry, prim_index, tri_index (indices of the triangles inside their <triangles> element)."""
    root = dae_uv.load(path)
    mats = dae_uv._node_matrices(root)
    names = dae_uv.material_names(root)
    out = []
    for geom in root.iterfind(".//c:library_geometries/c:geometry", NS):
        gid = geom.get("id")
        inst = mats.get(gid)
        if not inst:
            continue
        w, node = inst[0]
        if node.lower().startswith(("col", "collision")):
            continue
        mesh = geom.find("c:mesh", NS)
        vert = mesh.find("c:vertices", NS)
        pos_src = vert.find("c:input[@semantic='POSITION']", NS).get("source")[1:]
        P = dae_uv._source_array(mesh, pos_src)[:, :3]
        P = P @ w[:3, :3].T + w[:3, 3]
        for pi, prim in enumerate(mesh.findall("c:triangles", NS)):
            if names.get(prim.get("material"), prim.get("material")) != material:
                continue
            inputs = prim.findall("c:input", NS)
            offs = {}
            for i in inputs:
                offs.setdefault(i.get("semantic") + (i.get("set", "") if i.get("semantic") == "TEXCOORD" else ""), int(i.get("offset")))
            stride = max(int(i.get("offset")) for i in inputs) + 1
            voff = next(int(i.get("offset")) for i in inputs if i.get("semantic") == "VERTEX")
            tex = sorted((i for i in inputs if i.get("semantic") == "TEXCOORD"), key=lambda i: int(i.get("set", "0")))
            T = dae_uv._source_array(mesh, tex[0].get("source")[1:])[:, :2]
            toff = int(tex[0].get("offset"))
            idx = np.array(" ".join(p.text for p in prim.findall("c:p", NS)).split(), dtype=np.int64).reshape(-1, 3, stride)
            tris = P[idx[:, :, voff]]
            uvs = T[idx[:, :, toff]]
            # connected components by shared vertex position
            key = {}
            parent = list(range(len(tris)))

            def find(a):
                while parent[a] != a:
                    parent[a] = parent[parent[a]]
                    a = parent[a]
                return a
            for t, tri in enumerate(tris):
                for v, uvv in zip(tri, uvs[t]):
                    # same position AND same UV: adjacent letters share edges in 3D but not in the atlas
                    k = tuple(np.round(v, 4)) + tuple(np.round(uvv, 4))
                    if k in key:
                        ra, rb = find(t), find(key[k])
                        if ra != rb:
                            parent[ra] = rb
                    else:
                        key[k] = t
            groups = {}
            for t in range(len(tris)):
                groups.setdefault(find(t), []).append(t)
            for g in groups.values():
                tr, uv = tris[g], uvs[g]
                px = dae_uv.uv_to_px(uv, size or SIZE)
                cr = np.cross(tr[:, 1] - tr[:, 0], tr[:, 2] - tr[:, 0])
                area = np.linalg.norm(cr, axis=1)
                n = cr.sum(0)
                out.append({"tris": tr, "uv_px": px, "rect": [float(px[..., 0].min()), float(px[..., 1].min()), float(px[..., 0].max()), float(px[..., 1].max())],
                            "centroid": tr.reshape(-1, 3).mean(0), "normal": n / (np.linalg.norm(n) + 1e-12), "area": float(area.sum() / 2),
                            "geometry": gid, "prim_index": pi, "tri_index": g, "node": node,
                            "idx": idx[g], "offs": offs, "stride": stride, "w": w})
    return out


def front_basis(quads):
    """Dominant facing direction (area-weighted) and a right/up basis for a front view (world Z up)."""
    ns = np.array([q["normal"] * q["area"] for q in quads])
    # cluster: take the direction with most area among the quads' normals
    best, bn = -1, None
    for q in quads:
        s = sum(r["area"] for r in quads if r["normal"] @ q["normal"] > 0.9)
        if s > best:
            best, bn = s, q["normal"]
    up = np.array([0.0, 0.0, 1.0])
    if abs(bn @ up) > 0.9:
        up = np.array([0.0, 1.0, 0.0])
    right = np.cross(up, bn)
    right /= np.linalg.norm(right)
    up = np.cross(bn, right)
    return bn, right, up


def render(quads, normal, right, up, scale=400, facing=0.5, atlas=None, opacity=None, base=None):
    """Front-view image of the quads facing `normal` (letters textured from the atlas, cut by opacity).
    Quads may carry their own "atlas"/"opacity" arrays (several materials in one view)."""
    at = atlas if atlas is not None else np.asarray(Image.open(ATLAS).convert("RGB"))
    op = opacity if opacity is not None else np.asarray(Image.open(OPACITY).convert("L"))
    # winding is not consistent in these meshes: the side a quad is seen from is the side where its texture is
    # not mirrored (atlas u to the right, v up), like the game with double-sided letters on a solid board
    sel = []
    for q in quads:
        if facing > 0 and abs(q["normal"] @ normal) <= facing:
            continue
        tri, px = q["tris"][0], q["uv_px"][0]
        M = np.linalg.lstsq(np.c_[px, np.ones(3)], tri, rcond=None)[0]
        if facing <= 0 or np.cross(M[0], -M[1]) @ normal > 0:
            sel.append(q)
    if not sel:
        return None, []
    pts = np.concatenate([q["tris"].reshape(-1, 3) for q in sel])
    o = pts.mean(0)
    xy = lambda p: np.stack([(p - o) @ right, (p - o) @ up], -1)
    allxy = xy(pts)
    lo, hi = allxy.min(0) - 0.05, allxy.max(0) + 0.05
    W, H = int((hi[0] - lo[0]) * scale) + 1, int((hi[1] - lo[1]) * scale) + 1
    img = np.full((H, W, 3), 50, np.uint8)
    zbuf = np.full((H, W), -np.inf)
    labels = []
    order = sel
    for q in order:
        for tri, uv in zip(q["tris"], q["uv_px"]):
            s = (xy(tri) - lo) * scale
            s[:, 1] = H - s[:, 1]
            z = (tri - o) @ normal  # larger = nearer to the viewer
            A = np.c_[s, np.ones(3)]
            if abs(np.linalg.det(A)) < 1e-9:
                continue
            M = np.linalg.solve(A, uv)
            x0, y0 = np.floor(s.min(0)).astype(int)
            x1, y1 = np.ceil(s.max(0)).astype(int)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
            if x1 <= x0 or y1 <= y0:
                continue
            yy, xx = np.mgrid[y0:y1, x0:x1]
            v0, v1 = s[1] - s[0], s[2] - s[0]
            d = v0[0] * v1[1] - v0[1] * v1[0]
            px_, py_ = xx + 0.5 - s[0, 0], yy + 0.5 - s[0, 1]
            a = (px_ * v1[1] - py_ * v1[0]) / d
            b = (v0[0] * py_ - v0[1] * px_) / d
            inside = (a >= -0.01) & (b >= -0.01) & (a + b <= 1.01)
            zz = z[0] + a * (z[1] - z[0]) + b * (z[2] - z[0])
            src = np.stack([xx + 0.5, yy + 0.5, np.ones_like(xx, float)], -1) @ M
            at_q = q.get("atlas", at)
            op_q = q.get("opacity", op)
            sx = np.clip(src[..., 0].astype(int), 0, at_q.shape[1] - 1)
            sy = np.clip(src[..., 1].astype(int), 0, at_q.shape[0] - 1)
            vis = inside & (op_q[sy, sx] >= 64) & (zz > zbuf[y0:y1, x0:x1] + 1e-5)
            reg = img[y0:y1, x0:x1]
            reg[vis] = at_q[sy, sx][vis]
            zr = zbuf[y0:y1, x0:x1]
            zr[vis] = zz[vis]
        c = (xy(q["centroid"][None])[0] - lo) * scale
        labels.append((q, (c[0], H - c[1])))
    return Image.fromarray(img), labels


def analyze(path, out=None, scale=400):
    quads = read_quads(path)
    n, r, u = front_basis(quads)
    img, labels = render(quads, n, r, u, scale)
    if out and img is not None:
        back, _ = render(quads, -n, -r, u, scale)  # the other face (letters are often on both sides)
        W = img.width + (back.width + 10 if back is not None else 0)
        big = Image.new("RGB", (W, max(img.height, back.height if back is not None else 0)), (255, 0, 255))
        big.paste(img, (0, 0))
        if back is not None:
            big.paste(back, (img.width + 10, 0))
        d = ImageDraw.Draw(big)
        for k, (q, (x, y)) in enumerate(labels):
            d.text((x - 4, y + 6), str(k), fill=(255, 0, 255))
        big.save(out)
    return quads, (n, r, u), labels


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("dae")
    a.add_argument("--out")
    a.add_argument("--scale", type=int, default=400)
    li = sub.add_parser("lines")
    li.add_argument("dae")
    args = ap.parse_args(argv)
    if args.cmd == "lines":
        for l in lines_of(read_quads(args.dae)):
            print(f"face {l['face']:+d} {l['font']:3s} {l['text']}")
        return 0
    if args.cmd == "analyze":
        quads, (n, r, u), labels = analyze(args.dae, args.out, args.scale)
        print(f"{len(quads)} groups; front normal {np.round(n, 2)}; facing groups {len(labels)}")
        for k, (q, xy) in enumerate(labels):
            print(k, [int(v) for v in q["rect"]], "tris", len(q["tri_index"]), "area %.3f" % q["area"])
    return 0



# ---------------------------------------------------------------- decoding (which letter each quad shows)
FONTS = json.loads((REPO / "tools/production/glyph_fonts.json").read_text(encoding="utf8"))


_OP = None


def decode(rect):
    """(font, letter) of a quad from its UV rect: the alphabet cell with most ink (opacity) inside the rect."""
    global _OP
    if _OP is None:
        _OP = np.asarray(Image.open(OPACITY).convert("L")) >= 128
    x0, y0, x1, y1 = [int(round(v)) for v in rect]
    best = None
    for fk, f in FONTS.items():
        fy0, fy1 = f["y"]
        ov = min(y1, fy1) - max(y0, fy0)
        if ov < 0.5 * (fy1 - fy0) or (y1 - y0) > 1.6 * (fy1 - fy0):
            continue
        for ch, (a, b) in list(f["letters"].items()) + list(f.get("extra", {}).items()):
            lo, hi = max(a, x0), min(b, x1)
            if hi <= lo:
                continue
            ink_in = _OP[max(y0, fy0):min(y1, fy1), lo:hi].sum()
            ink_all = _OP[fy0:fy1, a:b].sum() + 1
            frac = ink_in / ink_all
            if frac > 0.6 and (best is None or frac > best[0] or (frac == best[0] and (hi - lo) > best[3])):
                best = (frac, fk, ch, hi - lo)
    return (best[1], best[2]) if best else (None, None)


def lines_of(quads):
    """Group the letter quads into text lines per face. A face = side of the sign (+/- front normal).

    Returns [{"face": +1/-1, "font": f, "text": str, "quads": [...] (reading order), "right": v, "up": v}]"""
    n, r, u = front_basis(quads)
    out = []
    letters = []
    for q in quads:
        f, ch = decode(q["rect"])
        if f is None:
            continue
        q["font"], q["char"] = f, ch
        letters.append(q)
    for q in letters:
        # reading direction of this quad in 3D: where the atlas u grows (x px grows)
        tri, px = q["tris"][0], q["uv_px"][0]
        A = np.c_[px, np.ones(3)]
        M = np.linalg.lstsq(A, tri, rcond=None)[0]  # px -> xyz (affine)
        q["dir_u"] = M[0] / (np.linalg.norm(M[0]) + 1e-12)   # +x in atlas
        q["dir_v"] = -M[1] / (np.linalg.norm(M[1]) + 1e-12)  # up on the letter (= -y in atlas)
        q["h3d"] = float(np.linalg.norm(M[1]) * (q["rect"][3] - q["rect"][1]))
        w = np.cross(q["dir_u"], q["dir_v"])
        q["rn"] = w / (np.linalg.norm(w) + 1e-12)  # reading normal: the side the letter is read from
        ref = n if abs(q["rn"] @ n) > 0.3 else np.eye(3)[int(np.argmax(np.abs(q["rn"])))]
        q["face"] = 1 if q["rn"] @ ref > 0 else -1
    for k, q in enumerate(letters):
        q["_k"] = k
    pool = list(letters)
    while pool:
        seed = pool.pop(0)
        line = [seed]
        for q in list(pool):
            if q["rn"] @ seed["rn"] < 0.9 or q["font"] != seed["font"] or q["dir_u"] @ seed["dir_u"] < 0.9:
                continue
            d = q["centroid"] - seed["centroid"]
            perp = seed["dir_v"] - (seed["dir_v"] @ seed["dir_u"]) * seed["dir_u"]  # italic letters: skewed v axis
            perp /= np.linalg.norm(perp) + 1e-12
            if abs(d @ perp) < 0.35 * seed["h3d"] and abs(d @ seed["rn"]) < 0.05:
                line.append(q)
                pool = [p for p in pool if p["_k"] != q["_k"]]
        line.sort(key=lambda q: q["centroid"] @ seed["dir_u"])
        # stacks: quads drawn at the same place (double-sided copies, layers) form one letter
        stacks = []
        for q in line:
            if stacks:
                p0 = stacks[-1][0]
                d = (q["centroid"] - p0["centroid"]) @ seed["dir_u"]
                w = np.ptp(p0["tris"].reshape(-1, 3) @ seed["dir_u"])
                if abs(d) < 0.3 * max(w, 1e-6) and q["char"] == p0["char"]:
                    stacks[-1].append(q)
                    continue
            stacks.append([q])
        # split at large gaps (several signs share one row of a facade)
        segs, cur = [], [stacks[0]]
        for a, b in zip(stacks, stacks[1:]):
            gap = (b[0]["centroid"] - a[0]["centroid"]) @ seed["dir_u"]
            if gap > 2.6 * seed["h3d"]:
                segs.append(cur)
                cur = []
            cur.append(b)
        segs.append(cur)
        for seg in segs:
            txt, prev = "", None
            for st in seg:
                q = st[0]
                if prev is not None:
                    gap = (q["centroid"] - prev["centroid"]) @ seed["dir_u"]
                    w = np.linalg.norm(q["tris"].reshape(-1, 3).max(0) - q["tris"].reshape(-1, 3).min(0))
                    if gap > 1.25 * max(w, seed["h3d"] * 0.6):
                        txt += " "
                txt += q["char"]
                prev = q
            out.append({"face": seed["face"], "font": seed["font"], "text": txt, "quads": [q for st in seg for q in st],
                        "stacks": seg, "right": seed["dir_u"], "up": seed["dir_v"]})
    out.sort(key=lambda l: (l["face"], -(np.mean([q["centroid"] for q in l["quads"]], 0) @ l["up"])))
    return out


if __name__ == "__main__":
    sys.exit(main())


def line_shots(path, out, scale=300, min_len=2):
    """One front-view image per decoded line (its own quads only), stacked with the decoded text."""
    from PIL import ImageDraw as _D
    quads = read_quads(path)
    import glyph_rewrite as R
    main, layers = R.collect(quads)
    main = R.vertical_lines(main)
    tiles = []
    for l in main:
        if len(R.compact(l["text"])) < min_len:
            continue
        q0 = l["quads"][0]
        n = np.cross(q0["dir_u"], q0["dir_v"])
        n /= np.linalg.norm(n)
        img, _ = render(l["quads"], n, q0["dir_u"], q0["dir_v"], scale, facing=0.0)
        if img is None:
            continue
        t = Image.new("RGB", (max(img.width, 300), img.height + 16), (0, 0, 60))
        t.paste(img, (0, 16))
        _D.Draw(t).text((2, 2), f"face {l['face']:+d} {l['font']} [{len(l['quads'])}] {l['text']}", fill=(255, 255, 0))
        s = min(1.0, 1400 / t.width)
        tiles.append(t.resize((int(t.width * s), int(t.height * s))))
    if not tiles:
        return 0
    W = max(t.width for t in tiles)
    H = sum(t.height + 4 for t in tiles)
    S = Image.new("RGB", (W, H), (80, 80, 80))
    y = 0
    for t in tiles:
        S.paste(t, (0, y))
        y += t.height + 4
    S.save(out)
    return len(tiles)
