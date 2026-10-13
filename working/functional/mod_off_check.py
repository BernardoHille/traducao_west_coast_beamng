"""Phase 7 block J: MOD OFF / ON check of every functional override.

State change goes through another level first (Phase 5 finding: reloading the same level keeps cached level data).
Reads, in the game: navgraph limits on the changed roads, radar trigger values, the zone/info files as the VFS resolves
them, the ptbr_functional_signs group, and screenshots the Event 01 corridor entry (R-19 70 present / absent).

    python working/functional/mod_off_check.py off|on
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
sys.path.insert(0, str(HERE))
import qa_runner as Q  # noqa: E402
from mcp_client import BeamNGMCP  # noqa: E402
import adas_test as A  # noqa: E402

PROBE = r"""
local mp = map.getMap()
local function lim(a, b) local n = mp.nodes[a]; local l = n and (n.links[b] or (mp.nodes[b] and mp.nodes[b].links[a])); return l and math.floor(l.speedLimit * 36 + 0.5) / 10 end
local out = {roads = {
  DR652_event01 = lim('DR652_5', 'DR652_6'), DR666 = lim('DR666_4', 'DR666_5'), DR571 = lim('DR571_5', 'DR655_1'),
  DR312_adas = lim('DR253_6', 'DR312_9'), DR989 = lim('DR989_14', 'autojunction_711'), DR1009 = lim('DR1009_26', 'DR1009_27'),
  junction1 = lim('junction1_wp25', 'junction1_wp19'), DR272_phase5 = lim('DR766_4', 'DR272_5')}}
out.radars = {}
for i = 2, 7 do local t = scenetree.findObject('speedTrapTrigger' .. i); out.radars['speedTrapTrigger' .. i] = t and t.speedLimit end
local g = scenetree.findObject('ptbr_functional_signs')
out.signs_group = g and g:getCount() or 'absent'
local files = {'/levels/west_coast_usa/city.sites.json', '/levels/west_coast_usa/info.json',
  '/gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json', '/levels/west_coast_usa/slotTraffic.json'}
out.vfs = {}
for _, f in ipairs(files) do out.vfs[f] = FS:getFileRealPath(f) end
local info = jsonReadFile('/levels/west_coast_usa/info.json')
out.localUnits = info and info.localUnits or 'absent'
local c = jsonReadFile('/levels/west_coast_usa/city.sites.json')
out.city_zones = {}
for _, zn in ipairs(c and c.zones or {}) do local v = zn.customFields and zn.customFields.values if v and v.speedLimit then out.city_zones[zn.name] = v.speedLimit end end
return jsonEncode(out)
"""


def main(state):
    m = BeamNGMCP()
    for e in A.SCENARIOS:
        m.lua(f"if extensions['{e}'] and extensions['{e}'].stopMission then extensions['{e}'].stopMission() end return 'ok'")
    cat = Q.catalog()
    Q.ensure_state(m, cat, state == "on", force_reload=True)
    time.sleep(3)
    r = json.loads(m.lua(PROBE))
    m.call("toggle_ui", show=False)
    sign = next(s for s in json.loads((HERE / "adas_zones.json").read_text(encoding="utf8"))["signs"] if s["id"] == "r19_70_entry_right")
    mm = sign["_measured"]
    fx, fy = mm["flow"]
    cam = [mm["road_point"][0] - fx * 12, mm["road_point"][1] - fy * 12, mm["road_z"] + 1.4]
    tgt = [mm["xy"][0], mm["xy"][1], mm["ground_z"] + 2.2]
    q = json.loads(m.lua(f"local q = quatFromDir((vec3({tgt[0]},{tgt[1]},{tgt[2]}) - vec3({cam[0]},{cam[1]},{cam[2]})):normalized(), vec3(0,0,1)) return jsonEncode({{q.x,q.y,q.z,q.w}})"))
    m.call("set_free_camera", pos=dict(zip("xyz", cam)), rot=dict(zip("xyzw", q)), fov=45)
    time.sleep(2)
    r["screenshot"] = A.shot(m, f"mod_{state}_event01_entry", ui=False)
    out = REPO / "tests/reports/phase7/mod_off_on.json"
    prev = json.loads(out.read_text(encoding="utf8")) if out.exists() else {}
    prev[f"mod_{state}"] = r
    out.write_text(json.dumps(prev, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
    print(json.dumps(r, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
