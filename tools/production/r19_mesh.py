"""Build the PT-BR R-19 replacement of `sign_speed5.dae` / `sign_speed25.dae` (and compare meshes).

Only materials and UVs change; positions, normals, vertex colours, triangle list, node
transforms (pivot/scale/orientation) and therefore the bounding box stay byte-identical.

  front panel quad      roadsigns          -> roadsigns_ptbr_r19_<v>, UV = 0..1 over the panel
                                              (same orientation as the atlas board it replaces)
  overlay quads         roadsigns          -> roadsigns_ptbr_r19_<v>, UV collapsed on a transparent
  (SPEED LIMIT, digits)                       texel: kept (invisible) so topology/bbox are unchanged
  back quad             metal_galvanized   -> roadsigns_ptbr_r19_back (galvanized maps + disc opacity;
                                              the original material is doubleSided, so an uncut back
                                              would show its rectangle corners around the disc)

    python tools/production/r19_mesh.py build <original.dae> <out.dae> --value 40
    python tools/production/r19_mesh.py compare <original.dae> <new.dae>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dae_uv  # noqa: E402

TRANSPARENT_UV = (0.01, 0.99)   # top-left corner of the R-19 texture: outside the disc (opacity 0)


def _uv_array(text: str):
    m = re.search(r'(<float_array id="[^"]*-mesh-map-0-array" count=")(\d+)(">)([^<]*)(</float_array>)', text)
    vals = np.array([float(v) for v in m.group(4).split()]).reshape(-1, 2)
    return m, vals


def _groups(text: str):
    """[(material_symbol, [(vertex, uv_index), ...])] for each <triangles> block."""
    out = []
    for m in re.finditer(r'<triangles material="([^"]+)" count="(\d+)">(.*?)</triangles>', text, re.S):
        body = m.group(3)
        offs = {i.group(1): int(i.group(2)) for i in re.finditer(r'semantic="(\w+)"[^>]*offset="(\d+)"', body)}
        stride = max(offs.values()) + 1
        p = [int(v) for v in re.search(r"<p>([^<]*)</p>", body).group(1).split()]
        corners = [(p[i + offs["VERTEX"]], p[i + offs["TEXCOORD"]]) for i in range(0, len(p), stride)]
        out.append((m.group(1), corners))
    return out


def build(src: Path, dst: Path, value: int) -> dict:
    text = src.read_text(encoding="utf8")
    pos_m = re.search(r'-mesh-positions-array" count="\d+">([^<]*)<', text)
    pos = np.array([float(v) for v in pos_m.group(1).split()]).reshape(-1, 3)
    uv_m, uv = _uv_array(text)
    new_uv = uv.copy()
    groups = _groups(text)
    front, back = f"roadsigns_ptbr_r19_{value}", "roadsigns_ptbr_r19_back"
    info = {"front_quad_uv_indices": [], "overlay_uv_indices": [], "back_uv_indices": []}
    for sym, corners in groups:
        if sym == "roadsigns-material":
            # the panel = the corners whose vertices span the full panel (largest area)
            verts = sorted({v for v, _ in corners})
            ys = {v: pos[v][1] for v in verts}
            panel_y = max(ys.values())            # panel sits behind the overlays (overlays are closer to the viewer)
            panel = [(v, t) for v, t in corners if abs(pos[v][1] - panel_y) < 1e-6]
            others = [(v, t) for v, t in corners if abs(pos[v][1] - panel_y) >= 1e-6]
            # The blank white board is symmetric, so its own UV orientation is not trustworthy (it is in
            # fact rotated 180 deg). Take the orientation from the text overlays (SPEED LIMIT tile,
            # digits), which read correctly in game: sign of du/dx and dv/dz.
            # per overlay triangle: affine map (x, z) -> (u, v); majority vote on the diagonal signs
            votes = []
            for i in range(0, len(others), 3):
                tri = others[i:i + 3]
                X = np.array([[pos[v][0], pos[v][2], 1.0] for v, _ in tri])
                U = np.array([uv[t] for _, t in tri])
                if abs(np.linalg.det(X)) < 1e-9:
                    continue
                A = np.linalg.solve(X, U)          # rows: d/dx, d/dz, offset
                votes.append((np.sign(A[0, 0]), np.sign(A[1, 1])))
            su = np.sign(sum(v[0] for v in votes))
            sv = np.sign(sum(v[1] for v in votes))
            pv = np.array([pos[v] for v, _ in panel])
            x0, x1 = pv[:, 0].min(), pv[:, 0].max()
            z0, z1 = pv[:, 2].min(), pv[:, 2].max()
            for v, t in panel:
                u = (pos[v][0] - x0) / (x1 - x0)
                w = (pos[v][2] - z0) / (z1 - z0)
                new_uv[t] = (u if su > 0 else 1 - u, w if sv > 0 else 1 - w)
                info["front_quad_uv_indices"].append(t)
            info["orientation_from_overlays"] = {"du_dx": int(su), "dv_dz": int(sv)}
            for _, t in others:
                new_uv[t] = TRANSPARENT_UV
                info["overlay_uv_indices"].append(t)
        elif sym == "metal_galvanized-material":
            vs = np.array([pos[v] for v, _ in corners])
            x0, x1 = vs[:, 0].min(), vs[:, 0].max()
            z0, z1 = vs[:, 2].min(), vs[:, 2].max()
            for v, t in corners:
                new_uv[t] = ((pos[v][0] - x0) / (x1 - x0), (pos[v][2] - z0) / (z1 - z0))
                info["back_uv_indices"].append(t)
    fmt = " ".join(f"{a:.7g} {b:.7g}" for a, b in new_uv)
    text = text[:uv_m.start(4)] + fmt + text[uv_m.end(4):]
    # materials: rename ids/names/symbols (effects are irrelevant to BeamNG and left as they are)
    text = text.replace('id="roadsigns-material" name="roadsigns"', f'id="{front}-material" name="{front}"')
    text = text.replace('id="metal_galvanized-material" name="metal_galvanized"', f'id="{back}-material" name="{back}"')
    text = text.replace('"roadsigns-material"', f'"{front}-material"').replace('"#roadsigns-material"', f'"#{front}-material"')
    text = text.replace('"metal_galvanized-material"', f'"{back}-material"').replace('"#metal_galvanized-material"', f'"#{back}-material"')
    text = text.replace("<authoring_tool>", f"<authoring_tool>traducao_ptbr_wcusa r19_mesh.py (R-19 {value} km/h) from ")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf8", newline="\n")
    return info


def structure(path: Path) -> dict:
    root = dae_uv.load(path)
    prims = list(dae_uv.primitives(root))
    pos = np.concatenate([p["positions"].reshape(-1, 3) for p in prims])
    text = path.read_text(encoding="utf8")
    pos_m = re.search(r'-mesh-positions-array" count="\d+">([^<]*)<', text)
    allpos = np.array([float(v) for v in pos_m.group(1).split()]).reshape(-1, 3)
    return {
        "geometries": len(root.findall(".//c:library_geometries/c:geometry", dae_uv.NS)),
        "triangles_total": int(sum(len(p["positions"]) for p in prims)),
        "triangles_per_material": {p["material"]: int(len(p["positions"])) for p in prims},
        "vertices": int(len(allpos)),
        "bbox_min": allpos.min(0).round(6).tolist(),
        "bbox_max": allpos.max(0).round(6).tolist(),
        "bbox_used_min": pos.min(0).round(6).tolist(),
        "bbox_used_max": pos.max(0).round(6).tolist(),
        "nodes": {n["name"]: n["matrix"] for n in dae_uv.summary(path)["nodes"]},
        "positions_sha": __import__("hashlib").sha256(pos_m.group(1).encode()).hexdigest()[:16],
        "normals_sha": __import__("hashlib").sha256(
            re.search(r'-mesh-normals-array" count="\d+">([^<]*)<', text).group(1).encode()).hexdigest()[:16],
        "colors_sha": __import__("hashlib").sha256(
            (re.search(r'-colors-Col-array" count="\d+">([^<]*)<', text) or re.search("", "")).group(0).encode()
        ).hexdigest()[:16],
        "p_lists_sha": __import__("hashlib").sha256(" ".join(re.findall(r"<p>([^<]*)</p>", text)).encode()).hexdigest()[:16],
        "materials": sorted(dae_uv.material_names(root).values()),
    }


def compare(a: Path, b: Path) -> dict:
    sa, sb = structure(a), structure(b)
    rows = []
    for k in ["geometries", "triangles_total", "vertices", "bbox_min", "bbox_max", "bbox_used_min", "bbox_used_max",
              "nodes", "positions_sha", "normals_sha", "colors_sha", "p_lists_sha", "triangles_per_material", "materials"]:
        rows.append({"check": k, "original": sa[k], "new": sb[k], "same": sa[k] == sb[k]})
    return {"original": str(a), "new": str(b), "rows": rows}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("src")
    b.add_argument("dst")
    b.add_argument("--value", type=int, required=True)
    c = sub.add_parser("compare")
    c.add_argument("a")
    c.add_argument("b")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        print(json.dumps(build(Path(a.src), Path(a.dst), a.value)))
    else:
        r = compare(Path(a.a), Path(a.b))
        for row in r["rows"]:
            print(f"{'SAME' if row['same'] else 'DIFF':4s} {row['check']}: {row['original']} -> {row['new']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
