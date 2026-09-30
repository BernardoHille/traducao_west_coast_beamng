"""Visual QA runner for the PT-BR West Coast USA translation mod.

Talks to the BeamNG in-game MCP server (http://127.0.0.1:29292/mcp) and drives the
procedure documented in tools/beamng/QA_PROTOCOL.md:

    load map -> known state -> mod ON/OFF (+ level reload) -> VFS origin check ->
    preset (time of day, UI hidden) -> camera pose -> screenshot -> copy -> log scan -> run report

Usage (from the repository root, BeamNG running with the MCP server enabled):

    python tools/beamng/qa_runner.py status
    python tools/beamng/qa_runner.py capture --family t_roadsigns --state original --preset day
    python tools/beamng/qa_runner.py capture --location roadsigns_chinatown_stop --state poc --preset night
    python tools/beamng/qa_runner.py repro --location roadsigns_chinatown_stop --preset day
    python tools/beamng/qa_runner.py frame --location roadsigns_chinatown_stop       # candidate pose, not saved
    python tools/beamng/qa_runner.py save-camera --location roadsigns_chinatown_stop  # store the live camera pose
    python tools/beamng/qa_runner.py mod --enable | --disable                         # + level reload

States: 'original' = translation mod disabled (baseline); any other state (poc, ptbr, ...) = mod enabled.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import BeamNGMCP, MCPError, wait_for_file  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CATALOG = os.path.join(REPO, "tests", "qa_locations.json")
PRESETS = os.path.join(REPO, "tests", "presets")

LOG_PATTERNS = re.compile(
    r"missing|not found|failed to load|could not load|unable to (load|mount|find)|invalid|"
    r"duplicat|\.dds|texture|NO-MATERIAL", re.I)


# ---------------------------------------------------------------- helpers
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def log(msg):
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


def catalog():
    return load_json(CATALOG)


def preset(name):
    return load_json(os.path.join(PRESETS, f"{name}.json"))


def defaults():
    return load_json(os.path.join(PRESETS, "camera_defaults.json"))


def locations_for(cat, family=None, location=None):
    locs = cat["locations"]
    if location:
        locs = [l for l in locs if l["id"] == location]
    elif family:
        locs = [l for l in locs if l["family"] == family]
    if not locs:
        sys.exit(f"no location matches family={family} location={location}")
    return locs


# ---------------------------------------------------------------- game state
def status(m):
    return m.call_json("get_status")


def mod_active(m, mod_name):
    return m.lua(f'local x=core_modmanager.getMods()["{mod_name}"] return tostring(x and x.active)') == "true"


def level_ready(m, map_name):
    try:
        s = status(m)
    except Exception:
        return False
    return map_name in (s.get("level") or "") and (s.get("vehicleCount") or 0) >= 1


def load_level(m, map_name):
    d = defaults()["level_load"]
    log(f"loading level {map_name} ...")
    m.call("load_level", name=map_name)
    time.sleep(d["initial_wait_seconds"])
    deadline = time.time() + d["timeout_seconds"]
    ok_streak = 0
    while time.time() < deadline:
        ok_streak = ok_streak + 1 if level_ready(m, map_name) else 0
        if ok_streak >= 2:
            time.sleep(d["settle_seconds_after_ready"])
            log("level ready")
            return
        time.sleep(d["poll_interval_seconds"])
    raise TimeoutError(f"level {map_name} did not become ready")


def set_mod(m, mod_name, enable):
    """enable_translation_mod / disable_translation_mod. Returns True if the state changed."""
    if mod_active(m, mod_name) == enable:
        return False
    fn = "activateMod" if enable else "deactivateMod"
    m.lua(f'core_modmanager.{fn}("{mod_name}") return "ok"')
    time.sleep(3)
    if mod_active(m, mod_name) != enable:
        raise MCPError(f"mod {mod_name} did not switch to active={enable}")
    log(f"mod {mod_name} -> {'enabled' if enable else 'disabled'}")
    return True


def ensure_state(m, cat, enable_mod, force_reload=False):
    """Known state: map loaded AFTER the mod reached the wanted state (textures are cached per load)."""
    changed = set_mod(m, cat["mod_name"], enable_mod)
    if changed or force_reload or not level_ready(m, cat["map"]):
        load_level(m, cat["map"])


def vfs_checks(m, cat, family, enable_mod):
    results = []
    for chk in cat["families"].get(family, {}).get("vfs_checks", []):
        info = m.call_json("file_info", path=chk["path"])
        real = info.get("realPath", "")
        expect = chk["mod_origin_contains"] if enable_mod else chk["original_origin_contains"]
        ok = bool(info.get("exists")) and expect.lower() in real.lower()
        results.append({"path": chk["path"], "realPath": real, "expected_contains": expect, "ok": ok})
        log(f"VFS {'OK ' if ok else 'BAD'} {chk['path']} -> {real}")
    return results


def apply_preset(m, pre):
    tod = pre["time_of_day"]
    m.call("set_time_of_day", time=tod["time"], play=tod.get("play", False))
    env = pre.get("environment")
    if env:  # e.g. windSpeed=0 freezes cloud drift (no dedicated MCP tool; core_environment via run_lua)
        fields = ", ".join(f"{k}={json.dumps(v)}" for k, v in env.items())
        m.lua(f"core_environment.setState({{{fields}}}) return 'ok'")
    m.call("toggle_ui", show=bool(defaults()["ui_visible"]))


def resolve_object(m, obj):
    """Object ids change on every level load: resolve by shape + position."""
    x, y, z = obj["position"]
    code = f"""
local best, bestd = nil, 1e9
local want = {json.dumps(obj["shape"].lower())}
for _, n in ipairs(scenetree.findClassObjects("TSStatic")) do
  local o = scenetree.findObject(n)
  if o and (o:getField("shapeName", 0) or ""):lower() == want then
    local d = (vec3(o:getPosition()) - vec3({x}, {y}, {z})):length()
    if d < bestd then best, bestd = o, d end
  end
end
if not best or bestd > {obj.get("match_tolerance_m", 1.0)} then return "null" end
local ok, mats = pcall(function() return best:getMaterialNames() end)
return jsonEncode({{id = best:getID(), dist = bestd, materials = ok and mats or {{}}}})
"""
    return json.loads(m.lua(code))


def place_camera(m, cam):
    p, r = cam["position"], cam["rotation"]
    m.call("set_free_camera", pos={"x": p[0], "y": p[1], "z": p[2]},
           rot={"x": r[0], "y": r[1], "z": r[2], "w": r[3]}, fov=cam["fov"])


def screenshot(m, dest):
    src = m.call("screenshot").strip()
    wait_for_file(src)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(src, dest)
    from PIL import Image
    with Image.open(dest) as im:
        size = list(im.size)
    return src, size


def scan_logs(text, extra_terms):
    terms = re.compile("|".join(re.escape(t) for t in extra_terms), re.I) if extra_terms else None
    rel, counts = [], {}
    for line in text.splitlines():
        mm = re.match(r"\s*[\d.]+\|([EW])\|([^|]+)\|(.*)", line)
        if not mm:
            continue
        lvl, src, msg = mm.groups()
        key = f"{lvl} {re.sub(r':[0-9]+$', '', src.strip())}"  # drop per-load vehicle ids (controller.init:<id>)
        counts[key] = counts.get(key, 0) + 1
        if (terms and terms.search(line)) or LOG_PATTERNS.search(msg):
            rel.append(line.strip()[:300])
    return {"error_warning_counts": counts, "relevant_lines": rel}


def dest_path(loc, state, pre):
    sub = "baseline" if state == "original" else "current"
    return os.path.join(REPO, "tests", "screenshots", sub, loc["family"],
                        f'{loc["id"]}_{state}{pre.get("filename_suffix", "")}.png')


# ---------------------------------------------------------------- commands
def cmd_status(m, a):
    cat = catalog()
    print(json.dumps({"status": status(m), "mod_active": mod_active(m, cat["mod_name"]),
                      "time_of_day": m.call_json("get_time_of_day"),
                      "camera": m.call_json("get_camera_state")}, indent=2))


def cmd_mod(m, a):
    cat = catalog()
    ensure_state(m, cat, enable_mod=a.enable, force_reload=a.reload)
    for fam in cat["families"]:
        vfs_checks(m, cat, fam, a.enable)


def cmd_capture(m, a):
    cat, pre = catalog(), preset(a.preset)
    locs = locations_for(cat, a.family, a.location)
    enable = a.state != "original"
    m.call("get_logs", lines=1)  # log marker: next call returns only new lines
    # A level loaded before the last mod toggle can hold stale textures and the runner cannot
    # tell, so a capture run reloads by default.
    ensure_state(m, cat, enable_mod=enable, force_reload=not a.no_reload)
    families = sorted({l["family"] for l in locs})
    run = {"started": dt.datetime.now().isoformat(timespec="seconds"), "map": cat["map"], "state": a.state,
           "preset": a.preset, "mod_active": mod_active(m, cat["mod_name"]),
           "vfs": {f: vfs_checks(m, cat, f, enable) for f in families}, "captures": []}
    apply_preset(m, pre)
    settle = defaults()["settle_seconds_after_camera_move"]
    for loc in locs:
        obj = resolve_object(m, loc["object"])
        place_camera(m, loc["camera"])
        time.sleep(settle)
        dest = dest_path(loc, a.state, pre)
        src, size = screenshot(m, dest)
        cam = m.call_json("get_camera_state")
        exp = defaults()["screenshot"]["expected_resolution"]
        entry = {"location": loc["id"], "object": obj, "file": os.path.relpath(dest, REPO).replace("\\", "/"),
                 "source": src, "resolution": size, "resolution_ok": size == exp, "camera_after": cam}
        run["captures"].append(entry)
        log(f"{loc['id']}: object={obj and obj['id']} -> {entry['file']} {size}")
    if a.restore_ui:
        m.call("toggle_ui", show=True)
    run["logs"] = scan_logs(m.call("get_logs"), families + [cat["mod_name"]])
    run["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    out = os.path.join(REPO, "tests", "reports", "runs",
                       f"{dt.datetime.now():%Y%m%d_%H%M%S}_{a.family or a.location}_{a.state}_{a.preset}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_json(out, run)
    bad = [v for f in run["vfs"].values() for v in f if not v["ok"]]
    log(f"run report: {os.path.relpath(out, REPO)} | VFS problems: {len(bad)} | "
        f"relevant log lines: {len(run['logs']['relevant_lines'])}")


def cmd_repro(m, a):
    """A -> A2 (no move, noise floor) -> move away -> restore -> B. Compares A/B against A/A2."""
    import numpy as np
    from PIL import Image
    cat, pre = catalog(), preset(a.preset)
    loc = locations_for(cat, location=a.location)[0]
    if not level_ready(m, cat["map"]):
        load_level(m, cat["map"])
    apply_preset(m, pre)
    tmp = os.path.join(REPO, "working", "temporary", "qa_repro")
    settle = defaults()["settle_seconds_after_camera_move"]
    shots = {}
    place_camera(m, loc["camera"]); time.sleep(settle)
    shots["A"] = screenshot(m, os.path.join(tmp, f"{loc['id']}_A.png"))[0]
    shots["A2"] = screenshot(m, os.path.join(tmp, f"{loc['id']}_A2.png"))[0]
    p = loc["camera"]["position"]
    m.call("set_free_camera", pos={"x": p[0] + 40, "y": p[1] - 25, "z": p[2] + 15},
           rot={"x": 0, "y": 0, "z": 0.7071, "w": 0.7071}, fov=90)
    time.sleep(settle)
    place_camera(m, loc["camera"]); time.sleep(settle)
    shots["B"] = screenshot(m, os.path.join(tmp, f"{loc['id']}_B.png"))[0]
    if a.restore_ui:
        m.call("toggle_ui", show=True)

    def arr(k):
        return np.asarray(Image.open(os.path.join(tmp, f"{loc['id']}_{k}.png")).convert("RGB")).astype(np.int16)

    A, A2, B = arr("A"), arr("A2"), arr("B")

    def metrics(x, y):
        d = np.abs(x - y)
        mse = float((d.astype(np.float64) ** 2).mean())
        h, w, _ = d.shape
        c = d[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
        return {"mean_abs": round(float(d.mean()), 3), "psnr_db": round(10 * np.log10(255 ** 2 / mse), 2) if mse else 99.0,
                "pct_pixels_diff_gt_16": round(float((d.max(axis=2) > 16).mean() * 100), 3),
                "center_mean_abs": round(float(c.mean()), 3)}

    res = {"location": loc["id"], "preset": a.preset, "noise_floor_A_vs_A2": metrics(A, A2),
           "restored_A_vs_B": metrics(A, B), "files": shots,
           "date": dt.datetime.now().isoformat(timespec="seconds")}
    out = os.path.join(REPO, "tests", "reports", "runs", f"{dt.datetime.now():%Y%m%d_%H%M%S}_repro_{loc['id']}_{a.preset}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    save_json(out, res)
    print(json.dumps(res, indent=2))


def cmd_frame(m, a):
    """Place a CANDIDATE camera facing the object (not saved). Inspect, then use save-camera."""
    cat = catalog()
    loc = locations_for(cat, location=a.location)[0]
    obj = resolve_object(m, loc["object"])
    if not obj:
        sys.exit("object not found in the loaded level")
    side = {"+fwd": 1, "-fwd": -1}[a.side]
    code = f"""
local o = scenetree.findObjectById({obj['id']})
local b = o:getWorldBox()
local c = vec3((b.minExtents.x+b.maxExtents.x)/2, (b.minExtents.y+b.maxExtents.y)/2, (b.minExtents.z+b.maxExtents.z)/2)
local f = vec3(o:getTransform():getColumn(1)); f.z = 0; f = f:normalized()
local cam = c + f * ({side} * {a.distance}) + vec3(0, 0, {a.dz})
local q = quatFromDir((c - cam):normalized(), vec3(0, 0, 1))
return jsonEncode({{pos = {{x = cam.x, y = cam.y, z = cam.z}}, rot = {{x = q.x, y = q.y, z = q.z, w = q.w}}}})
"""
    pose = json.loads(m.lua(code))
    m.call("set_free_camera", pos=pose["pos"], rot=pose["rot"], fov=defaults()["fov"])
    print(json.dumps(pose))


def cmd_save_camera(m, a):
    cat = catalog()
    cam = m.call_json("get_camera_state")
    if cam.get("mode") != "free":
        sys.exit(f"camera mode is {cam.get('mode')}, expected free")
    for loc in cat["locations"]:
        if loc["id"] == a.location:
            r = cam["rot"]
            loc["camera"] = {"position": [round(cam["pos"][k], 4) for k in "xyz"],
                             "rotation": [round(r[k], 6) for k in "xyzw"], "fov": cam["fov"],
                             "captured": dt.datetime.now().isoformat(timespec="seconds"),
                             "source": "get_camera_state"}
            save_json(CATALOG, cat)
            print(json.dumps(loc["camera"]))
            return
    sys.exit(f"unknown location {a.location}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://127.0.0.1:29292/mcp")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status")
    p = sp.add_parser("mod"); g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--enable", action="store_true"); g.add_argument("--disable", action="store_true")
    p.add_argument("--reload", action="store_true", help="reload the level even if the state did not change")
    for name in ("capture", "repro"):
        p = sp.add_parser(name)
        if name == "capture":
            g = p.add_mutually_exclusive_group(required=True)
            g.add_argument("--family"); g.add_argument("--location")
            p.add_argument("--state", required=True, help="original | poc | ptbr | ...")
            p.add_argument("--no-reload", action="store_true",
                           help="skip the start-of-run level reload (only if the level was loaded after the last mod toggle)")
        else:
            p.add_argument("--location", required=True)
        p.add_argument("--preset", default="day", choices=["day", "night"])
        p.add_argument("--no-restore-ui", dest="restore_ui", action="store_false")
    p = sp.add_parser("frame"); p.add_argument("--location", required=True)
    p.add_argument("--side", default="-fwd", choices=["+fwd", "-fwd"])
    p.add_argument("--distance", type=float, default=3.5); p.add_argument("--dz", type=float, default=-0.2)
    p = sp.add_parser("save-camera"); p.add_argument("--location", required=True)
    a = ap.parse_args()
    if a.cmd == "mod":
        a.enable = bool(a.enable)
    m = BeamNGMCP(a.url)
    {"status": cmd_status, "mod": cmd_mod, "capture": cmd_capture, "repro": cmd_repro,
     "frame": cmd_frame, "save-camera": cmd_save_camera}[a.cmd](m, a)


if __name__ == "__main__":
    main()
