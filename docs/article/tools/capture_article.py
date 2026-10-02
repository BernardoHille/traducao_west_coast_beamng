"""Fase 5.5 - capturas reais para o artigo (BeamNG MCP).

Estados:  original (mod OFF) -> poc (copia instalada com o DDS do PoC da Fase 1 e sem o _o.data novo)
          -> restaura copia instalada (install_mod.py) -> ptbr (mod ON, estado commitado).
Cada troca de estado passa por smallgrid (qa_runner.ensure_state). Raw PNG vai para docs/article/figures/raw/.
Uso: python docs/article/tools/capture_article.py original|poc|ptbr|ptbr_extra
"""
import json, os, shutil, sys, time, subprocess
REPO = r"C:\Users\Desktop\Desktop\traducao_west_coast_beamng"
sys.path.insert(0, os.path.join(REPO, "tools", "beamng"))
import qa_runner as q
from mcp_client import BeamNGMCP

RAW = os.path.join(REPO, "docs", "article", "figures", "raw")
LOG = os.path.join(RAW, "capture_log.json")
USER_MOD = r"C:\Users\Desktop\AppData\Local\BeamNG\BeamNG.drive\current\mods\unpacked\traducao_ptbr_wcusa"
ATLAS_DIR = os.path.join(USER_MOD, "assets", "materials", "signage", "roadsigns")

# custom (non-catalog) poses: camera position + look-at target, fov
CUSTOM = {
    # top-down overview of downtown/Chinatown, north up
    "aerial_downtown": {"pos": [-420.0, 330.0, 760.0], "dir": [0, 0, -1], "up": [0, 1, 0], "fov": 50},
    # oblique context of the Chinatown QA point (sign + QA camera both visible)
    "qa_context_chinatown": {"pos": [-697.0, 528.0, 136.0], "look": [-711.5, 551.5, 121.5], "fov": 50},
    # side view of the same QA point: QA camera and sign separated on screen (added after the first run)
    # first attempt (-700.4, 559.8, 128) looked from inside a building: capture discarded, replaced by top-down
    "qa_context_top": {"pos": [-711.7, 551.6, 139.0], "dir": [0, 0, -1], "up": [-0.59, 0.81, 0], "fov": 50},
    # road markings, near top-down
    "decal_bus_only_top": {"pos": [-445.7, 499.0, 118.0], "dir": [0, 0, -1], "up": [-0.707, -0.707, 0], "fov": 50},
    "decal_keep_clear_top": {"pos": [-335.4, 477.9, 108.0], "dir": [0, 0, -1], "up": [-0.707, 0.707, 0], "fov": 50},
    "decal_stop_chinatown_oblique": {"pos": [-703.0, 539.0, 128.0], "look": [-712.4, 550.0, 120.5], "fov": 50},
}
CATALOG_POINTS = ["roadsigns_chinatown_stop", "roadsigns_downtown_yield", "r19_40_hill", "r19_10_downtown_parking"]

PLAN = {
    "original": CATALOG_POINTS + list(CUSTOM),
    "poc": ["roadsigns_chinatown_stop", "roadsigns_downtown_yield"],
    "ptbr": CATALOG_POINTS + ["aerial_downtown", "decal_bus_only_top", "decal_stop_chinatown_oblique"],
    "ptbr_extra": ["qa_context_top"],
}


def quat_for(m, cam):
    if "look" in cam:
        d = [cam["look"][i] - cam["pos"][i] for i in range(3)]
        code = f"local q=quatFromDir(vec3({d[0]},{d[1]},{d[2]}):normalized(), vec3(0,0,1)) return jsonEncode({{x=q.x,y=q.y,z=q.z,w=q.w}})"
    else:
        d, u = cam["dir"], cam["up"]
        code = f"local q=quatFromDir(vec3({d[0]},{d[1]},{d[2]}):normalized(), vec3({u[0]},{u[1]},{u[2]}):normalized()) return jsonEncode({{x=q.x,y=q.y,z=q.z,w=q.w}})"
    return json.loads(m.lua(code))


def shoot(m, name, state, log):
    cat = q.catalog()
    if name in CUSTOM:
        cam = CUSTOM[name]
        rot = quat_for(m, cam)
        m.call("set_free_camera", pos=dict(zip("xyz", cam["pos"])), rot=rot, fov=cam["fov"])
        settle = 8 if name.startswith("aerial") else 5
    else:
        loc = [l for l in cat["locations"] if l["id"] == name][0]
        q.place_camera(m, loc["camera"])
        settle = 5
    time.sleep(settle)
    dest = os.path.join(RAW, f"{name}__{state}.png")
    if os.path.exists(dest):
        raise SystemExit(f"refusing to overwrite raw evidence {dest}")
    src, size = q.screenshot(m, dest)
    camst = m.call_json("get_camera_state")
    log.append({"file": os.path.relpath(dest, REPO).replace("\\", "/"), "name": name, "state": state,
                "taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "source": src, "resolution": size,
                "camera": camst, "mod_active": q.mod_active(m, cat["mod_name"]),
                "vfs_b_color": m.call_json("file_info", path="/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds").get("realPath"),
                "vfs_o_data": m.call_json("file_info", path="/assets/materials/signage/roadsigns/t_roadsigns_o.data.dds").get("realPath")})
    q.log(f"{name} [{state}] -> {dest} {size}")


def prepare_poc():
    """Temporary PoC state in the INSTALLED copy only (repo untouched): Phase 1 DDS, original mask."""
    shutil.copyfile(os.path.join(REPO, "export", "dds", "poc", "t_roadsigns_b.color.dds"),
                    os.path.join(ATLAS_DIR, "t_roadsigns_b.color.dds"))
    os.remove(os.path.join(ATLAS_DIR, "t_roadsigns_o.data.dds"))


def restore_installed():
    subprocess.check_call([sys.executable, os.path.join(REPO, "tools", "production", "install_mod.py")])


def main():
    state = sys.argv[1]
    os.makedirs(RAW, exist_ok=True)
    log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else []
    m = BeamNGMCP()
    cat, pre = q.catalog(), q.preset("day")
    if state == "poc":
        prepare_poc()
    try:
        if state != "ptbr_extra":  # extra shots reuse the already flushed ptbr session
            q.ensure_state(m, cat, enable_mod=(state != "original"), force_reload=True)
        state_tag = "ptbr" if state == "ptbr_extra" else state
        m.call("set_ui_state", route="play")
        q.apply_preset(m, pre)
        for name in PLAN[state]:
            shoot(m, name, state_tag, log)
    finally:
        if state == "poc":
            restore_installed()
            q.log("installed copy restored (install_mod.py)")
        m.call("toggle_ui", show=True)
        json.dump(log, open(LOG, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
