"""Offline preview of composed road signs (what the player sees), without the game.

Several West Coast signs are *composed by UV*: a panel quad plus glyph/word quads
floating a few millimetres in front of it (street names, EXIT/NEXT, TOLL, digits…).
The glyph shape comes from the opacity map, the tint from the vertex colour.
This tool groups the triangles of a mesh into sign faces, projects each face onto its
plane and rasterizes it with an atlas (base colour × vertex colour, alpha-tested by the
opacity map), so an atlas edit can be reviewed in its real composition.

    python tools/production/render_signs.py <mesh.dae> --color <b.color.png> --opacity <o.data.png> --out <dir>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import dae_uv  # noqa: E402

PX_PER_M = 220          # preview resolution
ALPHA_REF = 128         # material `roadsigns`: alphaTest true, alphaRef 128


def collect(path, material="roadsigns"):
    tris = []
    for prim in dae_uv.primitives(dae_uv.load(path)):
        if prim["material"] != material or prim["uvs"] is None:
            continue
        cols = prim["colors"] if prim["colors"] is not None else np.ones_like(prim["positions"])
        for p, uv, c in zip(prim["positions"], prim["uvs"], cols):
            n = np.cross(p[1] - p[0], p[2] - p[0])
            a = np.linalg.norm(n)
            if a < 1e-9:
                continue
            tris.append({"p": p, "uv": uv, "c": c, "n": n / a})
    return tris


def group_faces(tris, dist=0.6):
    """Single-linkage clustering of triangles facing the same way and close to each other."""
    n = len(tris)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    cent = np.array([t["p"].mean(0) for t in tris])
    norm = np.array([t["n"] for t in tris])
    lo = np.array([t["p"].min(0) for t in tris]) - dist
    hi = np.array([t["p"].max(0) for t in tris]) + dist
    order = np.argsort(cent[:, 0])
    for ii, i in enumerate(order):
        for j in order[ii + 1:]:
            if lo[j, 0] > hi[i, 0]:
                break
            if np.dot(norm[i], norm[j]) < 0.95:
                continue
            if np.all(lo[j] <= hi[i]) and np.all(lo[i] <= hi[j]):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [[tris[i] for i in g] for g in groups.values()]


def render_face(face, color, opacity, px_per_m=PX_PER_M):
    nrm = np.mean([t["n"] for t in face], axis=0)
    nrm /= np.linalg.norm(nrm)
    up = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(up, nrm)) > 0.9:
        up = np.array([0.0, 1.0, 0.0])
    right = np.cross(up, nrm)   # viewer looks along -normal
    right /= np.linalg.norm(right)
    upv = np.cross(nrm, right)
    pts = np.concatenate([t["p"] for t in face])
    x = pts @ right
    y = pts @ upv
    x0, y0 = x.min(), y.max()
    w = int(np.ceil((x.max() - x0) * px_per_m)) + 2
    h = int(np.ceil((y0 - y.min()) * px_per_m)) + 2
    if w * h > 6_000_000 or w < 4 or h < 4:
        return None
    out = np.zeros((h, w, 3), np.float32) + np.array([40, 44, 52], np.float32)
    depth = np.full((h, w), -1e9, np.float32)
    ch, cw = color.shape[:2]
    for t in face:
        sx = (t["p"] @ right - x0) * px_per_m + 1
        sy = (y0 - t["p"] @ upv) * px_per_m + 1
        dz = t["p"] @ nrm
        bx0, bx1 = int(max(np.floor(sx.min()), 0)), int(min(np.ceil(sx.max()), w - 1))
        by0, by1 = int(max(np.floor(sy.min()), 0)), int(min(np.ceil(sy.max()), h - 1))
        if bx1 < bx0 or by1 < by0:
            continue
        yy, xx = np.mgrid[by0:by1 + 1, bx0:bx1 + 1] + 0.5
        den = (sy[1] - sy[2]) * (sx[0] - sx[2]) + (sx[2] - sx[1]) * (sy[0] - sy[2])
        if abs(den) < 1e-9:
            continue
        l0 = ((sy[1] - sy[2]) * (xx - sx[2]) + (sx[2] - sx[1]) * (yy - sy[2])) / den
        l1 = ((sy[2] - sy[0]) * (xx - sx[2]) + (sx[0] - sx[2]) * (yy - sy[2])) / den
        l2 = 1 - l0 - l1
        inside = (l0 >= -1e-4) & (l1 >= -1e-4) & (l2 >= -1e-4)
        if not inside.any():
            continue
        uv = t["uv"]
        u = l0 * uv[0, 0] + l1 * uv[1, 0] + l2 * uv[2, 0]
        v = l0 * uv[0, 1] + l1 * uv[1, 1] + l2 * uv[2, 1]
        u -= np.floor(uv[:, 0].min())
        v -= np.floor(uv[:, 1].min())
        tx = np.clip((u * cw).astype(int), 0, cw - 1)
        ty = np.clip(((1 - v) * ch).astype(int), 0, ch - 1)
        a = opacity[ty, tx]
        z = l0 * dz[0] + l1 * dz[1] + l2 * dz[2]
        sub = depth[by0:by1 + 1, bx0:bx1 + 1]
        ok = inside & (a >= ALPHA_REF) & (z >= sub - 1e-5)
        vc = (l0[..., None] * t["c"][0] + l1[..., None] * t["c"][1] + l2[..., None] * t["c"][2])
        rgb = color[ty, tx, :3].astype(np.float32) * vc
        o = out[by0:by1 + 1, bx0:bx1 + 1]
        o[ok] = rgb[ok]
        sub[ok] = z[ok]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8)), (float(pts[:, 0].mean()), float(pts[:, 1].mean()), float(pts[:, 2].mean()))


def contact_sheet(images, cols=6, cell=(360, 260)):
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell[0], rows * cell[1]), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(images):
        im = im.copy()
        im.thumbnail((cell[0] - 8, cell[1] - 22))
        x, y = (i % cols) * cell[0] + 4, (i // cols) * cell[1] + 4
        sheet.paste(im, (x, y))
        d.text((x, y + cell[1] - 18), label, fill=(230, 230, 230))
    return sheet


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dae", nargs="+")
    ap.add_argument("--color", required=True)
    ap.add_argument("--opacity", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-area", type=float, default=0.05, help="skip faces smaller than this (m²)")
    a = ap.parse_args(argv)
    color = np.array(Image.open(a.color).convert("RGB"))
    opacity = np.array(Image.open(a.opacity).convert("RGBA"))[..., 0]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for dae in a.dae:
        faces = group_faces(collect(dae))
        imgs = []
        for k, face in enumerate(sorted(faces, key=lambda f: tuple(np.round(f[0]["p"].mean(0), 1)))):
            area = sum(0.5 * np.linalg.norm(np.cross(t["p"][1] - t["p"][0], t["p"][2] - t["p"][0])) for t in face)
            if area < a.min_area:
                continue
            r = render_face(face, color, opacity)
            if r is None:
                continue
            im, c = r
            name = f"{Path(dae).stem}_{k:03d}"
            im.save(out / f"{name}.png")
            imgs.append((f"{name} ({c[0]:.0f},{c[1]:.0f},{c[2]:.0f})", im))
        if imgs:
            contact_sheet(imgs).save(out / f"{Path(dae).stem}_sheet.png")
        print(f"{dae}: {len(imgs)} faces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
