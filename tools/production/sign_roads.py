"""Relate speed-limit signs to the drivable roads they regulate (read-only, level zip).

For every TSStatic whose shape matches --shape, list the nearest drivable DecalRoads with the distance,
the road direction at the closest point, the angle between the sign's facing and the road, the road's
explicit speedLimit (if any), length and file. The facing test matters: a sign regulates traffic that
SEES it, i.e. traffic moving against the sign's face normal.

    python tools/production/sign_roads.py --shape sign_speed25 --out working/speed/sign25_roads.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import zipfile
from pathlib import Path

import numpy as np

GAME = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive")
LEVEL_ZIP = GAME / "content/levels/west_coast_usa.zip"


def load_level_objects(zip_path=LEVEL_ZIP):
    roads, statics = [], []
    with zipfile.ZipFile(zip_path) as zf:
        for n in zf.namelist():
            if not n.endswith("items.level.json"):
                continue
            for i, line in enumerate(zf.read(n).decode("utf8", "replace").splitlines()):
                if not line.strip():
                    continue
                try:
                    j = json.loads(line)
                except json.JSONDecodeError:
                    continue
                c = j.get("class")
                if c == "DecalRoad" and j.get("nodes"):
                    j["_file"], j["_line"] = n, i + 1
                    roads.append(j)
                elif c == "TSStatic":
                    j["_file"], j["_line"] = n, i + 1
                    statics.append(j)
    return roads, statics


def drivable(road) -> bool:
    return float(road.get("drivability", -1)) > 0  # engine default is not drivable (map.lua: road.drivability > 0)


def polyline(road):
    return np.array([[p[0], p[1], p[2]] for p in road["nodes"]], float)


def length(pts):
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


def closest(pts, p):
    best = (1e18, 0, None)
    for k in range(len(pts) - 1):
        a, b = pts[k], pts[k + 1]
        ab = b - a
        t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-9), 0, 1)
        q = a + t * ab
        d = np.linalg.norm((p - q)[:2])
        if d < best[0]:
            best = (d, k, ab / max(np.linalg.norm(ab), 1e-9))
    return best


def facing(static):
    """Sign face normal in world XY. The speed sign meshes face -Y locally (panel normal 0,-1,0)."""
    rot = static.get("rotationMatrix")
    if rot:
        # level JSON stores the matrix column by column (matches TSStatic:getTransform():getColumn(i))
        R = np.array(rot, float).reshape(3, 3).T
        n = R @ np.array([0.0, -1.0, 0.0])
    else:
        n = np.array([0.0, -1.0, 0.0])
    n = n[:2]
    return n / max(np.linalg.norm(n), 1e-9)


def analyse(shape: str, radius=40.0, top=4):
    roads, statics = load_level_objects()
    roads = [r for r in roads if drivable(r)]
    polys = [(r, polyline(r)) for r in roads]
    out = []
    for s in statics:
        if not s.get("shapeName", "").lower().endswith(f"/{shape.lower()}.dae"):
            continue
        p = np.array(s["position"], float)
        f = facing(s)
        cands = []
        for r, pts in polys:
            if np.min(np.linalg.norm(pts[:, :2] - p[:2], axis=1)) > radius + 200:
                continue
            d, k, dirv = closest(pts, p)
            if d > radius:
                continue
            dxy = dirv[:2] / max(np.linalg.norm(dirv[:2]), 1e-9)
            ang = math.degrees(math.acos(np.clip(abs(np.dot(dxy, f)), 0, 1)))
            # who reads the face: traffic moving against the face normal. One-way roads run first->last node.
            dot = float(np.dot(dxy, f))
            seen_by = ("node order" if dot < 0 else "reverse") if r.get("oneWay") else "both directions"
            if r.get("oneWay") and dot >= 0:
                seen_by = "not seen (one-way traffic passes behind the face)"
            cands.append({"road": r.get("name") or r.get("persistentId"), "pid": r.get("persistentId"),
                          "dist_m": round(float(d), 2), "angle_face_vs_road_deg": round(ang, 1),
                          "speedLimit": r.get("speedLimit"), "len_m": round(length(pts), 1), "seen_by": seen_by,
                          "oneWay": r.get("oneWay", False), "lanes": [r.get("lanesLeft"), r.get("lanesRight")],
                          "file": r["_file"].split("main/MissionGroup/")[-1], "line": r["_line"]})
        cands.sort(key=lambda c: c["dist_m"])
        out.append({"sign_pos": [round(v, 2) for v in p.tolist()], "sign_file": s["_file"].split("main/MissionGroup/")[-1],
                    "facing_xy": [round(v, 3) for v in f.tolist()], "roads": cands[:top]})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shape", required=True)
    ap.add_argument("--radius", type=float, default=40.0)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    res = analyse(a.shape, a.radius)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf8")
    for s in res:
        print(s["sign_pos"], s["sign_file"])
        for c in s["roads"]:
            print(f"    {c['road'][:8]} d={c['dist_m']:6.2f} ang={c['angle_face_vs_road_deg']:5.1f} sl={c['speedLimit']} len={c['len_m']} ow={c['oneWay']} seen={c['seen_by']} {c['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
