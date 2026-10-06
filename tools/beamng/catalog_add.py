"""Add Phase 6 QA points to tests/qa_locations.json with camera poses computed from game data.

    python tools/beamng/catalog_add.py <points.json>

points.json: {"family": ..., "family_entry": {...vfs_checks...}, "points": [...]}
Point kinds:
  decal:   {"id", "kind": "decal", "decal_set", "indices": [instance indices of the phrase], "view": "top"|"oblique",
            "expected": [...], "description"}
           pose from main.decals.json: text up = tangent x normal (Phase 6 calibration), camera above the
           phrase looking down with the text upright ("top"), or behind it at driver height ("oblique").
  static:  {"id", "kind": "static", "shape", "position", "local_target": [x,y,z] (mesh local), "local_normal",
            "distance", "fov", "expected", "description"}
           pose from the TSStatic transform (rotationMatrix column-major, Phase 5) and a point/normal of the
           mesh face that shows the edited atlas region.
  pose:    {"id", "kind": "pose", "pos", "look" or "dir"+"up", "fov", ...} explicit camera.
The camera quaternion is computed in the game (quatFromDir) - the MCP server must be running.
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP  # noqa: E402

CATALOG = REPO / "tests/qa_locations.json"
LEVEL_ZIP = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/west_coast_usa.zip")


def quat(m, d, up=(0, 0, 1)):
    code = (f"local q=quatFromDir(vec3({d[0]},{d[1]},{d[2]}):normalized(), vec3({up[0]},{up[1]},{up[2]}):normalized()) "
            "return jsonEncode({q.x,q.y,q.z,q.w})")
    return [round(v, 6) for v in json.loads(m.lua(code))]


def decal_pose(inst, p):
    pos = np.array([i[3:6] for i in inst])
    c = pos.mean(0)
    n = np.array(inst[0][6:9])
    t = np.array(inst[0][9:12])
    up = np.cross(t, n)
    up /= np.linalg.norm(up)
    size = max(i[1] for i in inst)
    span = float(np.ptp(pos, 0).max()) if len(pos) > 1 else 0.0
    if p.get("view", "top") == "top":
        h = p.get("height", 1.15 * (size + span) / np.tan(np.radians(p.get("fov", 50) / 2)) / 2 + 1.0)
        cam = c + n * h
        return cam, -n, up, size
    first = pos[0]
    dist = p.get("distance", 1.8 * size + 2.5)
    cam = first - up * dist + n * p.get("eye", 1.4)
    return cam, c - cam, n, size


def game_instances(m, shape):
    """World transforms of every TSStatic using `shape` in the loaded level (prefab children included)."""
    code = f"""
local out = {{}}
local want = {json.dumps(shape.lower())}
for _, n in ipairs(scenetree.findClassObjects("TSStatic")) do
  local o = scenetree.findObject(n)
  if o and (o:getField("shapeName", 0) or ""):lower() == want then
    local t = o:getTransform()
    local p, c0, c1, c2 = o:getPosition(), t:getColumn(0), t:getColumn(1), t:getColumn(2)
    local sc = o:getScale()
    table.insert(out, {{pos = {{p.x, p.y, p.z}}, c0 = {{c0.x, c0.y, c0.z}}, c1 = {{c1.x, c1.y, c1.z}}, c2 = {{c2.x, c2.y, c2.z}}, scale = {{sc.x, sc.y, sc.z}}}})
  end
end
return jsonEncode(out)"""
    res = json.loads(m.lua(code))
    return sorted(res, key=lambda r: (round(r["pos"][0], 1), round(r["pos"][1], 1), round(r["pos"][2], 1)))


def uv_pose(m, p):
    """Camera in front of the face that shows atlas `region` of `mesh` on instance `instance` (game order)."""
    sys.path.insert(0, str(REPO / "tools/production"))
    import asset_usage
    import dae_uv
    key = p["mesh"]
    local = asset_usage.extract([key], REPO / "source/originals/meshes/phase6")[0]
    f = dae_uv.region_point(local, p["material"], tuple(p["size"]), p["region"]) if p.get("locate") == "point"         else dae_uv.region_faces(local, p["material"], tuple(p["size"]), p["region"])
    if not f and p.get("locate") != "point":
        f = dae_uv.region_point(local, p["material"], tuple(p["size"]), p["region"])
    if not f:
        raise SystemExit(f"{p['id']}: no face of {key} shows region {p['region']}")
    shape = "/" + key.split("::", 1)[1]
    objs = game_instances(m, shape)
    if not objs:
        raise SystemExit(f"{p['id']}: no TSStatic with {shape} in the loaded level")
    o = objs[p.get("instance", 0) % len(objs)]
    rot = np.array([o["c0"], o["c1"], o["c2"]], float).T
    sc = np.array(o["scale"], float)
    c_local = np.array(p.get("local_target", f["centroid"]), float)
    n_local = np.array(p.get("local_normal", f["normal"]), float)
    target = np.array(o["pos"], float) + rot @ (c_local * sc)
    normal = rot @ (n_local / np.where(sc == 0, 1, sc)) * p.get("side", 1)
    if p.get("horizontal"):
        normal[2] = 0.0
    normal /= np.linalg.norm(normal)
    dist = p.get("distance", 2.0)
    if dist == "auto":  # frame the face: its largest extent fills ~60 % of the vertical field of view
        ext = float(max(f["extent"]) * max(sc))
        dist = max(0.8, ext / 0.6 / (2 * np.tan(np.radians(p.get("fov", 50) / 2))))
    cam = target + normal * dist + np.array([0, 0, p.get("dz", 0.0)])
    return cam, target - cam, (0, 0, 1), o, f, len(objs)


def static_pose(p):
    rot = np.array(p["rotationMatrix"]).reshape(3, 3).T  # column-major in items.level.json
    sc = np.array(p.get("scale", [1, 1, 1]))
    target = np.array(p["position"]) + rot @ (np.array(p["local_target"]) * sc)
    normal = rot @ np.array(p["local_normal"])
    normal /= np.linalg.norm(normal)
    cam = target + normal * p.get("distance", 4.0) + np.array([0, 0, p.get("dz", 0.0)])
    return cam, target - cam, (0, 0, 1)


def main(argv=None) -> int:
    spec = json.loads(Path((argv or sys.argv[1:])[0]).read_text(encoding="utf8"))
    m = BeamNGMCP()
    cat = json.loads(CATALOG.read_text(encoding="utf8"))
    fam = spec["family"]
    if spec.get("family_entry"):
        cat["families"][fam] = spec["family_entry"]
    decals = None
    ids = {l["id"] for l in cat["locations"]}
    for p in spec["points"]:
        if p["id"] in ids:
            cat["locations"] = [l for l in cat["locations"] if l["id"] != p["id"]]
        loc = {"id": p["id"], "family": fam, "description": p.get("description", ""), "expected_elements": p.get("expected", []),
               "lighting": p.get("lighting", ["day"]), "added": "phase6"}
        if p["kind"] == "decal":
            if decals is None:
                decals = json.loads(zipfile.ZipFile(LEVEL_ZIP).read("levels/west_coast_usa/main.decals.json"))["instances"]
            inst = [decals[p["decal_set"]][i] for i in p["indices"]]
            cam, d, up, size = decal_pose(inst, p)
            loc["object"] = {"kind": "decal", "decal_set": p["decal_set"], "indices": p["indices"],
                             "uid": [i[12] for i in inst], "rectIdx": [i[0] for i in inst], "position": [round(v, 3) for v in inst[0][3:6]],
                             "size": [round(i[1], 3) for i in inst]}
        elif p["kind"] == "uv":
            cam, d, up, o, f, n_inst = uv_pose(m, p)
            loc["object"] = {"shape": "/" + p["mesh"].split("::", 1)[1], "position": [round(v, 3) for v in o["pos"]],
                             "match_tolerance_m": 1.0, "atlas_region": p["region"], "face_triangles": f["triangles"],
                             "instances_in_level": n_inst}
        elif p["kind"] == "static":
            cam, d, up = static_pose(p)
            loc["object"] = {"shape": p["shape"], "position": p["position"], "match_tolerance_m": 1.0}
        else:
            cam = np.array(p["pos"], float)
            d = np.array(p["look"]) - cam if "look" in p else np.array(p["dir"], float)
            up = p.get("up", (0, 0, 1))
            if p.get("object"):
                loc["object"] = p["object"]
        loc["camera"] = {"position": [round(float(v), 4) for v in cam], "rotation": quat(m, d, up),
                         "fov": p.get("fov", 50), "source": f"tools/beamng/catalog_add.py ({p['kind']})"}
        cat["locations"].append(loc)
        print(f"{p['id']}: cam {loc['camera']['position']}")
    CATALOG.write_text(json.dumps(cat, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
