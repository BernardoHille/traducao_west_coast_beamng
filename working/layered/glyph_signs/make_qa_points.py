"""QA points for the glyph-built signs: one camera per translated line (first instance of the mesh in the
level, face read from the front), computed from the game's TSStatic transforms (MCP must be running).

Writes qa_points.json (kind "pose") for tools/beamng/catalog_add.py."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools/production"))
sys.path.insert(0, str(REPO / "tools/beamng"))
import glyph_signs as G  # noqa: E402
import glyph_rewrite as R  # noqa: E402
import catalog_add as CA  # noqa: E402
from mcp_client import BeamNGMCP  # noqa: E402

spec = json.loads((HERE / "spec.json").read_text(encoding="utf8"))
m = BeamNGMCP()
MOD = "mods" + chr(92) + "unpacked" + chr(92) + "traducao_ptbr_wcusa"
points, vfs = [], []
FOV = 45
# framing fixes after the first in-game review (camera behind the gantry / too far from small labels)
OVERRIDE = {"gl_roadsigns_rs_carpools": {"side": -1}, "gl_roadsigns_rs_per_vehicle": {"side": -1},
            "gl_dragstrip_tree_alder": {"dist": 1.0}, "gl_dragStrip_irSensorBox": {"dist": 0.9}, "gl_s_busstop_wcu": {"dist": 1.3},
            "gl_bld_shops_001_pack": {"side": -1}}
for name, s in spec["signs"].items():
    src = REPO / s["src"]
    quads = G.read_quads(src)
    main, _ = R.collect(quads) if quads else ([], [])
    main = R.vertical_lines(main) if main else []
    shape = "/" + s["install"] + "/" + src.name
    objs = CA.game_instances(m, shape)
    if not objs:
        print("NO INSTANCE", shape)
        continue
    vfs.append({"path": shape, "mod_origin_contains": MOD, "original_origin_contains": ".zip"})
    seen = set()
    o = objs[0]
    rot = np.array([o["c0"], o["c1"], o["c2"]], float).T
    sc = np.array(o["scale"], float)

    def add_point(pid, qsel, expected, desc):
        pts = np.concatenate([q["tris"].reshape(-1, 3) for q in qsel])
        L = float(np.linalg.norm(np.ptp(pts, 0) * sc))
        target = np.array(o["pos"], float) + rot @ (pts.mean(0) * sc)
        q0 = qsel[0]
        M = R.affine(q0)
        rn = np.cross(M[0], -M[1])
        rn = rot @ (rn / np.linalg.norm(rn))
        rn /= np.linalg.norm(rn)
        dist = max(2.0, (L + 0.5) / 0.7 / (2 * np.tan(np.radians(FOV / 2))))
        ov = next((v for k, v in OVERRIDE.items() if pid.startswith(k)), {})
        rn = rn * ov.get("side", 1)
        dist = ov.get("dist", dist)
        cam = target + rn * dist + np.array([0, 0, ov.get("dz", 0.0)])
        points.append({"id": pid, "kind": "pose", "pos": cam.round(3).tolist(), "look": target.round(3).tolist(), "fov": FOV,
                       "object": {"shape": shape, "position": [round(v, 3) for v in o["pos"]], "match_tolerance_m": 1.0},
                       "expected": [expected], "description": desc, "lighting": ["day"]})

    for sl in s["lines"]:
        if sl.get("custom") == "uv_map":
            mp = json.loads((REPO / sl["map_file"]).read_text(encoding="utf8"))["uv_map"]
            mq = G.read_quads(src, sl["material"], tuple(sl["size"]))
            done = []
            for e in mp:
                if e["id"] == "rs_miles_blank":
                    continue
                for q in mq:
                    if max(abs(a - b) for a, b in zip(q["rect"], e["from"])) <= 1.5 and not any(np.linalg.norm(q["centroid"] - d) < 3 for d in done):
                        done.append(q["centroid"])
                        near = [r for r in mq if np.linalg.norm(r["centroid"] - q["centroid"]) < 2.0]
                        add_point(f"gl_roadsigns_{e['id']}_{len(done)}", near, e["id"], f"roadsigns.dae: tile {e['id']} (re-targeted)")
            continue
        if sl.get("custom") == "dealer_word":
            mq = G.read_quads(src, "m_billboardsigns_dealers", (2048, 1024))
            add_point(f"gl_{name}_mapa", mq[:3], "MAPA / INFO", f"{name}: MAP -> MAPA")
            continue
        if sl.get("custom") == "currency":
            continue
        key = R.compact(sl["old"])
        if sl.get("custom") == "clearance":
            key = "FT"
        hits = [l for l in main if R.compact(l["text"]) == key]
        for l in hits[:1] if key not in seen else []:
            seen.add(key)
            pts = np.concatenate([q["tris"].reshape(-1, 3) for q in l["quads"]])
            c_local = pts.mean(0)
            ext = np.ptp(pts, 0)
            L = float(np.linalg.norm(ext * sc))
            target = np.array(o["pos"], float) + rot @ (c_local * sc)
            rn = rot @ l["quads"][0]["rn"]
            rn /= np.linalg.norm(rn)
            dist = max(2.0, (L + 0.5) / 0.7 / (2 * np.tan(np.radians(FOV / 2))))
            pid0 = f"gl_{name.replace('s_', '', 1)[:24]}_{key.lower()[:14]}"
            ov = next((v for k, v in OVERRIDE.items() if pid0.startswith(k)), {})
            rn = rn * ov.get("side", 1)
            dist = ov.get("dist", dist)
            cam = target + rn * dist + np.array([0, 0, ov.get("dz", 0.0)])
            cam[2] = max(cam[2], target[2] - 0.5)
            pid = f"gl_{name.replace('s_', '', 1)[:24]}_{key.lower()[:14]}"
            points.append({"id": pid, "kind": "pose", "pos": cam.round(3).tolist(), "look": target.round(3).tolist(), "fov": FOV,
                           "object": {"shape": shape, "position": [round(v, 3) for v in o["pos"]], "match_tolerance_m": 1.0},
                           "expected": [sl["new"] + (" m" if sl.get("custom") else "")],
                           "description": f"{name}: {sl['old']} -> {sl['new']} ({len(objs)} instance(s) in the level)",
                           "lighting": ["day"]})
json.dump({"family": "glyph_signs", "family_entry": {"material": "clutter_commercial", "vfs_checks": vfs}, "points": points},
          open(HERE / "qa_points.json", "w", encoding="utf8"), indent=1, ensure_ascii=False)
print(len(points), "points")
