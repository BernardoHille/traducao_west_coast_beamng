"""Read-only COLLADA (.dae) inspector used to confirm atlas regions.

For every <triangles>/<polylist> bound to a material, collect the UV triangles and
rasterize them onto the texture grid, so an atlas region is backed by the real UV
footprint of the meshes that sample it (not by eyeballing the image).

    python tools/production/dae_uv.py footprint <dae...> --material roadsigns --size 2048 1024
    python tools/production/dae_uv.py summary <dae>
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

NS = {"c": "http://www.collada.org/2005/11/COLLADASchema"}


def _floats(text: str) -> list[float]:
    return [float(t) for t in text.split()] if text else []


def load(path: str | Path) -> ET.Element:
    return ET.fromstring(Path(path).read_bytes())


def material_names(root: ET.Element) -> dict[str, str]:
    """symbol/id -> engine material name (the `name` attribute, which BeamNG maps)."""
    out = {}
    for m in root.iterfind(".//c:library_materials/c:material", NS):
        mid = m.get("id")
        out[mid] = m.get("name") or mid.removesuffix("-material")
    return out


def _source_array(mesh: ET.Element, src_id: str) -> np.ndarray:
    src = mesh.find(f"c:source[@id='{src_id}']", NS)
    arr = _floats(src.find("c:float_array", NS).text)
    stride = int(src.find(".//c:accessor", NS).get("stride", "1"))
    return np.array(arr, dtype=np.float64).reshape(-1, stride)


def primitives(root: ET.Element):
    """Yield dicts: geometry, material (engine name), positions (N,3,3), uvs (N,3,2) per triangle."""
    names = material_names(root)
    for geom in root.iterfind(".//c:library_geometries/c:geometry", NS):
        mesh = geom.find("c:mesh", NS)
        if mesh is None:
            continue
        vert = mesh.find("c:vertices", NS)
        pos_src = vert.find("c:input[@semantic='POSITION']", NS).get("source")[1:]
        positions = _source_array(mesh, pos_src)
        for prim in list(mesh):
            tag = prim.tag.split("}")[1]
            if tag not in ("triangles", "polylist"):
                continue
            inputs = prim.findall("c:input", NS)
            stride = max(int(i.get("offset")) for i in inputs) + 1
            voff = next(int(i.get("offset")) for i in inputs if i.get("semantic") == "VERTEX")
            tex = sorted((i for i in inputs if i.get("semantic") == "TEXCOORD"), key=lambda i: int(i.get("set", "0")))
            uvs = _source_array(mesh, tex[0].get("source")[1:]) if tex else None
            toff = int(tex[0].get("offset")) if tex else 0
            col = next((i for i in inputs if i.get("semantic") == "COLOR"), None)
            colors = _source_array(mesh, col.get("source")[1:]) if col is not None else None
            coff = int(col.get("offset")) if col is not None else 0
            idx = np.array(_floats(" ".join(p.text or "" for p in prim.findall("c:p", NS))), dtype=np.int64)
            idx = idx.reshape(-1, stride)
            if tag == "triangles":
                tri = idx.reshape(-1, 3, stride)
            else:  # polylist -> fan triangulation
                vcount = [int(v) for v in prim.find("c:vcount", NS).text.split()]
                tris, k = [], 0
                for n in vcount:
                    poly = idx[k:k + n]
                    tris.extend([poly[0], poly[j], poly[j + 1]] for j in range(1, n - 1))
                    k += n
                tri = np.array(tris).reshape(-1, 3, stride)
            yield {
                "geometry": geom.get("name") or geom.get("id"),
                "material": names.get(prim.get("material"), prim.get("material")),
                "positions": positions[tri[:, :, voff]][:, :, :3],
                "uvs": uvs[tri[:, :, toff]][:, :, :2] if uvs is not None else None,
                "colors": colors[tri[:, :, coff]][:, :, :3] if colors is not None else None,
            }


def _raster_tri(mask: np.ndarray, p: np.ndarray) -> None:
    h, w = mask.shape
    x0, y0 = np.floor(p.min(0)).astype(int)
    x1, y1 = np.ceil(p.max(0)).astype(int)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, w - 1), min(y1, h - 1)
    if x1 < x0 or y1 < y0:
        return
    ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
    px, py = xs + 0.5, ys + 0.5
    (ax, ay), (bx, by), (cx, cy) = p

    def edge(ex0, ey0, ex1, ey1):
        return (ex1 - ex0) * (py - ey0) - (ey1 - ey0) * (px - ex0)

    e0, e1, e2 = edge(ax, ay, bx, by), edge(bx, by, cx, cy), edge(cx, cy, ax, ay)
    inside = ((e0 >= 0) & (e1 >= 0) & (e2 >= 0)) | ((e0 <= 0) & (e1 <= 0) & (e2 <= 0))
    mask[y0:y1 + 1, x0:x1 + 1] |= inside


def uv_to_px(uv: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    """UV (N,3,2) -> atlas pixels. Triangles are shifted into the 0..1 tile (atlas tiles never wrap)."""
    w, h = size
    u = uv[..., 0] - np.floor(uv[..., 0].min(axis=-1, keepdims=True))
    v = uv[..., 1] - np.floor(uv[..., 1].min(axis=-1, keepdims=True))
    return np.stack([u * w, (1.0 - v) * h], axis=-1)


def footprint(paths, material: str, size=(2048, 1024)) -> tuple[np.ndarray, list[dict]]:
    """Union mask of UV triangles (pixels) + one record per triangle."""
    w, h = size
    mask = np.zeros((h, w), dtype=bool)
    items = []
    for path in paths:
        for prim in primitives(load(path)):
            if prim["material"] != material or prim["uvs"] is None:
                continue
            for t in uv_to_px(prim["uvs"], size):
                area = abs((t[1, 0] - t[0, 0]) * (t[2, 1] - t[0, 1]) - (t[2, 0] - t[0, 0]) * (t[1, 1] - t[0, 1]))
                if area < 1e-6:
                    continue
                _raster_tri(mask, t)
                items.append({"file": Path(path).name, "geometry": prim["geometry"],
                              "bbox_px": [float(t[:, 0].min()), float(t[:, 1].min()),
                                          float(t[:, 0].max()), float(t[:, 1].max())]})
    return mask, items


def summary(path) -> dict:
    root = load(path)
    out = {"file": str(path), "primitives": [], "nodes": []}
    for prim in primitives(root):
        pos = prim["positions"].reshape(-1, 3)
        entry = {"geometry": prim["geometry"], "material": prim["material"], "triangles": int(len(prim["positions"])),
                 "bbox_min": pos.min(0).round(6).tolist(), "bbox_max": pos.max(0).round(6).tolist()}
        if prim["uvs"] is not None:
            uv = prim["uvs"].reshape(-1, 2)
            entry["uv_min"] = uv.min(0).round(6).tolist()
            entry["uv_max"] = uv.max(0).round(6).tolist()
        out["primitives"].append(entry)
    for node in root.iter(f"{{{NS['c']}}}node"):
        m = node.find("c:matrix", NS)
        out["nodes"].append({"name": node.get("name"), "matrix": _floats(m.text) if m is not None else None})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("footprint")
    f.add_argument("dae", nargs="+")
    f.add_argument("--material", default="roadsigns")
    f.add_argument("--size", nargs=2, type=int, default=[2048, 1024])
    f.add_argument("--png", help="write the union mask as PNG")
    s = sub.add_parser("summary")
    s.add_argument("dae")
    a = ap.parse_args(argv)
    if a.cmd == "summary":
        print(json.dumps(summary(a.dae), indent=2))
        return 0
    mask, items = footprint(a.dae, a.material, tuple(a.size))
    ys, xs = np.nonzero(mask)
    print(json.dumps({"pixels": int(mask.sum()),
                      "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                      "triangles": len(items)}, indent=2))
    if a.png:
        from PIL import Image
        Image.fromarray((mask * 255).astype(np.uint8)).save(a.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
