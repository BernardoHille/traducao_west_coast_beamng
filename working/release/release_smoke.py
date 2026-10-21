"""Phase 9: smoke test of the REAL release ZIP in the game (BeamNG MCP), with the development copy removed.

    python working/release/release_smoke.py state on|off       # mods mounted + VFS origin of every file of the manifest
    python working/release/release_smoke.py visual on|off day|night <location id> ...
    python working/release/release_smoke.py functional on|off  # navgraph samples 10-120 km/h, radar triggers, level objects
    python working/release/release_smoke.py radar <radar id> <km/h> ...
    python working/release/release_smoke.py logs <label>       # new game-log lines since the previous call, filtered

"on" = only the release ZIP active; "off" = ZIP deactivated (the game must show its originals). Every state change goes
through another level first (Phase 5 finding). Results: tests/reports/release/release_smoke.json; screenshots:
tests/screenshots/release/<state>/.
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
sys.path.insert(0, str(REPO / "working/functional"))
import qa_runner as Q  # noqa: E402
from mcp_client import BeamNGMCP  # noqa: E402

CFG = json.loads((REPO / "tools/release/release_config.json").read_text(encoding="utf8"))
INFO = json.loads((REPO / "mod/traducao_ptbr_wcusa/mod_info/traducao_ptbr_wcusa/info.json").read_text(encoding="utf8"))
NAME = f"traducao_ptbr_wcusa_v{INFO['version']}"
DEV = "traducao_ptbr_wcusa"
MANIFEST = REPO / "release/output" / f"{NAME}_manifest.txt"
OUT = REPO / "tests/reports/release/release_smoke.json"


def save(section, data):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prev = json.loads(OUT.read_text(encoding="utf8")) if OUT.exists() else {}
    prev[section] = data
    OUT.write_text(json.dumps(prev, indent=1, ensure_ascii=False) + "\n", encoding="utf8")


def catalog():
    cat = Q.catalog()
    cat["mod_name"] = NAME
    for fam in cat["families"].values():
        for chk in fam.get("vfs_checks", []):
            chk["mod_origin_contains"] = f"{NAME}.zip"
    return cat


def mods(m):
    return json.loads(m.lua("local o = {} for k, v in pairs(core_modmanager.getMods()) do o[k] = {active = v.active, path = v.fullpath} end return jsonEncode(o)"))


def reach(m, state):
    ms = mods(m)
    if DEV in ms:
        raise SystemExit(f"development copy still registered: {ms[DEV]} - remove it before testing the ZIP")
    Q.ensure_state(m, catalog(), state == "on", force_reload=True)


def cmd_state(m, state):
    reach(m, state)
    files = [l.split()[2] for l in MANIFEST.read_text(encoding="utf8").splitlines() if l and not l.startswith("#")]
    files = [f for f in files if not f.startswith("mod_info/")]
    res = json.loads(m.lua("local o = {} for _, f in ipairs(jsonDecode(%s)) do o[f] = FS:getFileRealPath('/' .. f) or '' end return jsonEncode(o)"
                           % json.dumps(json.dumps(files))))
    zip_hits = [f for f, r in res.items() if f"{NAME}.zip".lower() in r.lower()]
    # on: every file must come from the ZIP; off: none may (modified files fall back to the game, new ones do not exist)
    bad = [(f, res[f]) for f in files if (f in zip_hits) != (state == "on")]
    samples = {f: res[f] for f in ("assets/materials/signage/roadsigns/t_roadsigns_b.color.dds",
                                   "levels/west_coast_usa/art/shapes/roads/roadsigns.cdae",
                                   "levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr/sign_r19_50.cdae",
                                   "levels/west_coast_usa/main/MissionGroup/DecalRoads/items.level.json",
                                   "levels/west_coast_usa/slotTraffic.json",
                                   "gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json")}
    fi = m.call_json("file_info", path="/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds")
    data = {"mods": mods(m), "files_checked": len(files), "from_release_zip": len(zip_hits), "unexpected": bad,
            "samples_realPath": samples, "file_info_t_roadsigns": fi, "status": Q.status(m),
            "result": "PASS" if not bad else "FAIL"}
    save(f"state_{state}", data)
    print(json.dumps({k: v for k, v in data.items() if k != "mods"}, indent=1, ensure_ascii=False))
    print("active mods:", {k: v["active"] for k, v in data["mods"].items()})


def cmd_visual(m, state, preset, ids):
    cat, pre = catalog(), Q.preset(preset)
    if not Q.level_ready(m, cat["map"]) or Q.mod_active(m, NAME) != (state == "on"):
        reach(m, state)
    Q.apply_preset(m, pre)
    settle = Q.defaults()["settle_seconds_after_camera_move"]
    shots = []
    for lid in ids:
        loc = Q.locations_for(cat, location=lid)[0]
        obj = Q.resolve_object(m, loc["object"])
        Q.place_camera(m, loc["camera"])
        time.sleep(settle)
        dest = REPO / "tests/screenshots/release" / state / f"{lid}_{preset}.png"
        src, size = Q.screenshot(m, str(dest))
        shots.append({"location": lid, "family": loc["family"], "object": obj, "file": dest.relative_to(REPO).as_posix(), "resolution": size})
        print(lid, obj and obj.get("id", obj.get("kind")), dest.relative_to(REPO).as_posix())
    m.call("toggle_ui", show=True)
    prev = json.loads(OUT.read_text(encoding="utf8")).get(f"visual_{state}_{preset}", []) if OUT.exists() else []
    keep = [s for s in prev if s["location"] not in ids]
    save(f"visual_{state}_{preset}", keep + shots)


OBJ_LUA = r"""
local out = {radars = {}}
for i = 2, 7 do local t = scenetree.findObject('speedTrapTrigger' .. i); out.radars['speedTrapTrigger' .. i] = t and t.speedLimit end
local g = scenetree.findObject('ptbr_functional_signs')
out.ptbr_functional_signs = g and g:getCount() or 'absent'
local info = jsonReadFile('/levels/west_coast_usa/info.json')
out.localUnits = info and info.localUnits or 'absent'
return jsonEncode(out)
"""


def cmd_functional(m, state):
    import navgraph_matrix as N
    if not Q.level_ready(m, "west_coast_usa") or Q.mod_active(m, NAME) != (state == "on"):
        reach(m, state)
    res = json.loads(m.lua(N.LUA % json.dumps(json.dumps([[p[2], p[3], p[4]] for p in N.POINTS]))))
    rows = []
    for p, r in zip(N.POINTS, res):
        got = round(r["lim"] * 3.6, 1) if r else None
        rows.append({"expected_with_mod_kmh": p[0], "label": p[1], "edge": [r["a"], r["b"]] if r else None, "navgraph_kmh": got,
                     "match_mod": got is not None and abs(got - p[0]) < 0.5})
    objs = json.loads(m.lua(OBJ_LUA))
    data = {"navgraph": rows, "objects": objs}
    if state == "on":
        # the generator's 15 added objects are the ptbr_functional_signs group + its 14 signs
        data["result"] = "PASS" if all(r["match_mod"] for r in rows) and objs["ptbr_functional_signs"] == 14 \
            and objs["localUnits"] == "absent" else "FAIL"
    save(f"functional_{state}", data)
    for r in rows:
        print(("OK " if r["match_mod"] else "-- "), r["expected_with_mod_kmh"], r["navgraph_kmh"], r["label"])
    print(json.dumps(objs, ensure_ascii=False))


def cmd_radar(m, args):
    import radar_test as R
    if Q.mod_active(m, NAME) is not True:
        raise SystemExit("release ZIP not active")
    m.lua(R.HOOK_LUA)
    out = []
    try:
        rid = int(args[0])
        for kmh in [int(a) for a in args[1:]]:
            r = R.run(m, rid, kmh)
            out.append(r)
            print(f"radar {rid} ({r['limit_kmh']}, fires > {r['trigger_above_kmh']}): target {kmh} at radar {r['speed_at_radar_kmh']} "
                  f"-> triggered {r['triggered']} (expected {r['expected_trigger']}) {r['result']}")
    finally:
        m.lua(R.UNHOOK_LUA)
    prev = json.loads(OUT.read_text(encoding="utf8")).get("radar", []) if OUT.exists() else []
    save("radar", prev + out)


PAT = re.compile(r"mod|dds|material|mesh|cdae|dae|json|missing|unable to load|invalid|not found|failed|error", re.I)


def cmd_logs(m, label):
    text = m.call("get_logs")
    lines = [l.strip() for l in text.splitlines() if re.match(r"\s*[\d.]+\|[EW]\|", l)]
    rel = [l[:300] for l in lines if PAT.search(l)]
    ours = [l for l in rel if re.search(r"traducao|ptbr|roadsigns|r19|west_coast_usa", l, re.I)]
    data = {"error_warning_lines": len(lines), "filtered_lines": rel, "lines_naming_mod_or_its_paths": ours}
    save(f"logs_{label}", data)
    print(f"{len(lines)} E/W lines, {len(rel)} after filter, {len(ours)} naming the mod or its paths")
    for l in rel[:60]:
        print("  ", l)


def main(argv):
    m = BeamNGMCP()
    cmd = argv[0]
    if cmd == "state":
        cmd_state(m, argv[1])
    elif cmd == "visual":
        cmd_visual(m, argv[1], argv[2], argv[3:])
    elif cmd == "functional":
        cmd_functional(m, argv[1])
    elif cmd == "radar":
        cmd_radar(m, argv[1:])
    elif cmd == "logs":
        cmd_logs(m, argv[1])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
