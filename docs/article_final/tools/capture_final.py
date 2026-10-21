"""Final article (v1.0.0): real captures in the game through the BeamNG MCP, with ONLY the release ZIP installed.

States:  on  = traducao_ptbr_wcusa_v1.0.0 (the release ZIP) active, development copy not registered
         off = the same ZIP deactivated (game originals)
Every state change goes through smallgrid (qa_runner.ensure_state, Phase 5 cache finding).
Raw captures go to docs/article_final/figures/raw/ and are never overwritten; every shot is logged with the
camera, the active mods and the VFS origin of a representative file (capture_log.json).

    python docs/article_final/tools/capture_final.py on|off [day|night]
    python docs/article_final/tools/capture_final.py navgraph on|off     # dump of the navgraph edges (positions + km/h)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ART, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "beamng"))
import qa_runner as q  # noqa: E402
from mcp_client import BeamNGMCP  # noqa: E402

RAW = os.path.join(ART, "figures", "raw")
LOG = os.path.join(RAW, "capture_log.json")
ZIP_MOD = "traducao_ptbr_wcusa_v1.0.0"
DEV_MOD = "traducao_ptbr_wcusa"

# custom poses (camera position + look-at target or direction/up), vertical FOV in degrees.
# The first four are the poses of the first article (docs/article/tools/capture_article.py) so the 1.0.0 state can be
# compared with the Phase 5 snapshot at the same camera.
CUSTOM = {
    "decal_stop_chinatown_oblique": {"pos": [-703.0, 539.0, 128.0], "look": [-712.4, 550.0, 120.5], "fov": 50},
    "aerial_downtown": {"pos": [-420.0, 330.0, 760.0], "dir": [0, 0, -1], "up": [0, 1, 0], "fov": 50},
    "decal_bus_only_top": {"pos": [-445.7, 499.0, 118.0], "dir": [0, 0, -1], "up": [-0.707, -0.707, 0], "fov": 50},
    "decal_keep_clear_top": {"pos": [-335.4, 477.9, 108.0], "dir": [0, 0, -1], "up": [-0.707, 0.707, 0], "fov": 50},
    # new for the final article: the Chinatown intersection from the driver's height, further back (opening figure)
    "chinatown_street": {"pos": [-694.0, 529.0, 122.6], "look": [-712.4, 550.0, 121.2], "fov": 55},  # not used: sign out of frame
    # opening figure candidates: driver height, before the painted PARE, looking at the intersection
    "chinatown_driver_a": {"pos": [-699.5, 534.5, 122.4], "look": [-712.4, 550.0, 121.0], "fov": 55},
    "chinatown_driver_b": {"pos": [-697.0, 531.5, 123.0], "look": [-711.0, 549.0, 120.8], "fov": 60},
}
CATALOG = ["roadsigns_chinatown_stop", "roadsigns_downtown_yield", "r19_40_hill"]
PLAN = {
    ("on", "day"): ["chinatown_street", "decal_stop_chinatown_oblique", "aerial_downtown", "decal_bus_only_top",
                    "decal_keep_clear_top"] + CATALOG,
    ("on", "night"): ["chinatown_driver_a", "decal_stop_chinatown_oblique"],
    ("on", "opening"): ["chinatown_driver_a", "chinatown_driver_b"],
    ("off", "day"): ["chinatown_driver_a", "decal_stop_chinatown_oblique", "decal_keep_clear_top"] + CATALOG,
}


def catalog():
    cat = q.catalog()
    cat["mod_name"] = ZIP_MOD
    return cat


def mods(m):
    return json.loads(m.lua("local o = {} for k, v in pairs(core_modmanager.getMods()) do o[k] = v.active end return jsonEncode(o)"))


def quat_for(m, cam):
    if "look" in cam:
        d = [cam["look"][i] - cam["pos"][i] for i in range(3)]
        up = [0, 0, 1]
    else:
        d, up = cam["dir"], cam["up"]
    code = (f"local q=quatFromDir(vec3({d[0]},{d[1]},{d[2]}):normalized(), vec3({up[0]},{up[1]},{up[2]}):normalized()) "
            "return jsonEncode({x=q.x,y=q.y,z=q.z,w=q.w})")
    return json.loads(m.lua(code))


def screenshot(m, dest):
    """qa_runner.screenshot with a longer wait: with the game window in the background a shot took ~22 s (21/10/2026)."""
    import shutil
    from mcp_client import wait_for_file
    from PIL import Image
    src = m.call("screenshot").strip()
    wait_for_file(src, timeout=120)
    shutil.copyfile(src, dest)
    with Image.open(dest) as im:
        return src, list(im.size)


def shoot(m, name, state, preset, log):
    cat = catalog()
    if name in CUSTOM:
        cam = CUSTOM[name]
        m.call("set_free_camera", pos=dict(zip("xyz", cam["pos"])), rot=quat_for(m, cam), fov=cam["fov"])
        settle = 8 if name.startswith("aerial") else 5
    else:
        loc = [l for l in cat["locations"] if l["id"] == name][0]
        q.place_camera(m, loc["camera"])
        settle = 5
    time.sleep(settle)
    dest = os.path.join(RAW, f"{name}__{state}_{preset}.png")
    if os.path.exists(dest):
        raise SystemExit(f"refusing to overwrite raw evidence {dest}")
    src, size = screenshot(m, dest)
    log.append({"file": os.path.relpath(dest, REPO).replace("\\", "/"), "name": name, "state": state, "preset": preset,
                "taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "resolution": size, "camera": m.call_json("get_camera_state"),
                "active_mods": {k: v for k, v in mods(m).items() if v},
                "vfs_t_roadsigns_b_color": m.call_json("file_info", path="/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds").get("realPath"),
                "vfs_decal_items": m.call_json("file_info", path="/levels/west_coast_usa/main.decals.json").get("realPath")})
    q.log(f"{name} [{state} {preset}] -> {dest} {size}")


NAV_LUA = r"""
local mp = map.getMap()
local out = {}
for a, n in pairs(mp.nodes) do
  for b, l in pairs(n.links) do
    local nb = mp.nodes[b]
    if nb then
      out[#out + 1] = {math.floor(n.pos.x * 10 + 0.5) / 10, math.floor(n.pos.y * 10 + 0.5) / 10,
                       math.floor(nb.pos.x * 10 + 0.5) / 10, math.floor(nb.pos.y * 10 + 0.5) / 10,
                       math.floor(l.speedLimit * 36 + 0.5) / 10, l.drivability or 1, a, b}
    end
  end
end
return jsonEncode(out)
"""


def dump_navgraph(m, state):
    dest = os.path.join(RAW, f"navgraph_edges__{state}.json")
    if os.path.exists(dest):
        raise SystemExit(f"refusing to overwrite raw evidence {dest}")
    edges = json.loads(m.lua(NAV_LUA))
    meta = {"state": state, "taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "active_mods": {k: v for k, v in mods(m).items() if v},
            "columns": ["x1", "y1", "x2", "y2", "speed_kmh", "drivability", "node_a", "node_b"], "edges": len(edges)}
    json.dump({"meta": meta, "edges": edges}, open(dest, "w", encoding="utf-8"))
    q.log(f"navgraph {state}: {len(edges)} edges -> {dest}")


def main():
    os.makedirs(RAW, exist_ok=True)
    log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else []
    m = BeamNGMCP()
    if DEV_MOD in mods(m):
        raise SystemExit("development copy registered: remove it so that only the release ZIP is tested")
    if sys.argv[1] == "navgraph":
        state = sys.argv[2]
        if q.mod_active(m, ZIP_MOD) != (state == "on") or not q.level_ready(m, "west_coast_usa"):
            q.ensure_state(m, catalog(), enable_mod=(state == "on"), force_reload=True)
        dump_navgraph(m, state)
        return
    state, preset = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "day")
    try:
        if q.mod_active(m, ZIP_MOD) != (state == "on") or not q.level_ready(m, "west_coast_usa"):
            q.ensure_state(m, catalog(), enable_mod=(state == "on"), force_reload=True)
        m.call("set_ui_state", route="play")
        q.apply_preset(m, q.preset("day" if preset == "opening" else preset))
        for name in PLAN[(state, preset)]:
            shoot(m, name, state, preset, log)
    finally:
        m.call("toggle_ui", show=True)
        json.dump(log, open(LOG, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
