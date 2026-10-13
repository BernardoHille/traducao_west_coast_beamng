"""Phase 7 block J: speed-camera (speed trap) tests with the game's own trigger logic and tolerance.

The player car gets a flying start 45 m before each radar (teleport + initial velocity along the enforced direction)
and the AI holds a constant speed ('set' mode) through the trigger. extensions.hook is wrapped for the run to record
'onSpeedTrapTriggered' (fired by lua/ge/extensions/gameplay/speedTraps.lua when speed > limit + 10 %).
The game camera follows the car (the trap ignores cars more than 100 m from the camera). Writes
tests/reports/phase7/radar_test.json.

    python working/functional/radar_test.py [radar ...]
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP  # noqa: E402

RADARS = {  # trigger centre (z: road height hint), enforced direction (trigger y axis, measured), Phase 7 limit
    2: {"pos": [-416.1, 197.7], "z": 100.5, "flow": [0.42, 0.91], "kmh": 70},
    3: {"pos": [-305.4, 325.2], "z": 101.5, "flow": [-0.86, -0.51], "kmh": 60},
    4: {"pos": [-423.7, 672.8], "z": 75.0, "flow": [0.76, -0.65], "kmh": 100,
        "speeds": [95, 105, 125]},  # junction ramp: the AI slows ~6 km/h in the curve before the trigger
    5: {"pos": [-1001.7, 1902.1], "z": 90.5, "flow": [-0.96, 0.27], "kmh": 60, "back": 25,
        "speeds": [55, 65, 80]},  # curve: the AI slows before the trigger
    6: {"pos": [414.3, 1646.2], "z": 74.5, "flow": [0.01, 1.0], "kmh": 60,
        # dock gate: many parallel booth lanes; the lane through the trigger is given explicitly
        "path": ["DR1213_2", "DR1213_3", "DR1213_4", "DR1253_5", "DR1294_1"]},
    7: {"pos": [393.0, 1848.0], "z": 74.5, "flow": [0.25, -0.97], "kmh": 60, "back": 25},
}
SPEEDS = {60: [55, 65, 70], 70: [65, 75, 80], 100: [95, 105, 115]}
ROUTE_LUA = (HERE / "place_signs.py").read_text(encoding="utf8").split('ROUTE_LUA = r"""')[1].split('"""')[0]
HOOK_LUA = r"""
-- freeroam loads gameplay_speedTraps as a preset extension; a level loaded through the MCP is not in freeroam mode
if not gameplay_speedTraps then extensions.load('gameplay_speedTraps') end
if not _G.__ptbrHookOrig then
  _G.__ptbrHookOrig = extensions.hook
  extensions.hook = function(name, ...)
    if name == 'onSpeedTrapTriggered' then
      local d, s, o = ...
      table.insert(_G.__ptbrTraps, {trigger = d and d.triggerName, limit = d and d.speedLimit, speed = s, over = o, t = os.clock()})
    end
    return _G.__ptbrHookOrig(name, ...)
  end
end
_G.__ptbrTraps = {}
return 'ok'
"""
UNHOOK_LUA = "if _G.__ptbrHookOrig then extensions.hook = _G.__ptbrHookOrig; _G.__ptbrHookOrig = nil end return 'ok'"
START_LUA = r"""
local v = be:getPlayerVehicle(0)
local p = vec3(%f, %f, 0)
-- height from the navgraph edge under the point (a ray from above would hit overpasses)
local mp = map.getMap()
local a, b = map.findClosestRoad(vec3(p.x, p.y, %f))
local na, nb = mp.nodes[a].pos, mp.nodes[b].pos
local ab = nb - na
local t = math.max(0, math.min(1, (p - na):dot(ab) / ab:dot(ab)))
p.z = na.z + ab.z * t + 0.5
local dir = vec3(%f, %f, 0):normalized()
spawn.safeTeleport(v, p, quatFromDir(dir, vec3(0, 0, 1)), nil, nil, nil, true)
v:queueLuaCommand("ai.setMode('disabled')")
commands.setGameCamera()
return jsonEncode({p.x, p.y, p.z})
"""
GO_LUA = r"""
local v = be:getPlayerVehicle(0)
local dir = vec3(%f, %f, 0):normalized() * %f
v:applyClusterVelocityScaleAdd(v:getRefNodeId(), 1, dir.x, dir.y, dir.z)
v:queueLuaCommand([[ai.driveUsingPath({path = %s, driveInLane = 'on', aggression = 0.6, avoidCars = 'off'}); ai.setSpeedMode('set'); ai.setSpeed(%f)]])
_G.__ptbrTraps = {}
return 'ok'
"""
POLL_LUA = r"""
local v = be:getPlayerVehicle(0)
local p = v:getPosition()
return jsonEncode({p.x, p.y, v:getVelocity():length(), _G.__ptbrTraps or {}})
"""


def run(m, rid, kmh):
    r = RADARS[rid]
    fx, fy = r["flow"]
    back = r.get("back", 45)
    sx, sy = r["pos"][0] - fx * back, r["pos"][1] - fy * back
    m.lua(START_LUA % (sx, sy, r["z"], fx, fy))
    time.sleep(2.0)
    route = json.loads(m.lua(ROUTE_LUA % (sx, sy, r["z"], fx, fy, 120)))
    nodes = r.get("path") or [n["node"] for n in route[1:]]
    names = "{" + ",".join(f"'{n}'" for n in nodes) + "}"
    m.lua(GO_LUA % (fx, fy, kmh / 3.6, names, kmh / 3.6))
    t0, speeds, traps, passed = time.time(), [], [], False
    while time.time() - t0 < 9:
        x, y, v, tr = json.loads(m.lua(POLL_LUA))
        along = (x - r["pos"][0]) * fx + (y - r["pos"][1]) * fy
        if -12 < along < 12:
            speeds.append(round(v * 3.6, 1))
        traps = tr or traps
        if along > 25:
            passed = True
            break
        time.sleep(0.1)
    m.lua("be:getPlayerVehicle(0):queueLuaCommand(\"ai.setMode('disabled'); input.event('brake', 1, 1)\") return 'ok'")
    mine = [t for t in traps if t["trigger"] == f"speedTrapTrigger{rid}"]
    threshold = r["kmh"] * 1.1
    v_at = speeds[len(speeds) // 2] if speeds else None
    expect = v_at is not None and v_at > threshold
    res = {"radar": rid, "limit_kmh": r["kmh"], "trigger_above_kmh": round(threshold, 1), "target_kmh": kmh,
           "speed_at_radar_kmh": v_at, "speeds_in_box": speeds, "passed": passed, "triggered": bool(mine),
           "trap_events": mine, "expected_trigger": expect}
    res["result"] = "PASS" if passed and speeds and bool(mine) == expect else "CHECK"
    return res


def main(argv):
    m = BeamNGMCP()
    out = REPO / "tests/reports/phase7/radar_test.json"
    prev = json.loads(out.read_text(encoding="utf8")) if out.exists() else {}
    m.lua(HOOK_LUA)
    try:
        for rid in [int(a) for a in argv] or list(RADARS):
            for kmh in RADARS[rid].get("speeds") or SPEEDS[RADARS[rid]["kmh"]]:
                r = run(m, rid, kmh)
                prev[f"radar{rid}_{kmh}"] = r
                print(f"radar {rid} ({r['limit_kmh']}, fires > {r['trigger_above_kmh']}): target {kmh} at radar {r['speed_at_radar_kmh']} "
                      f"-> triggered {r['triggered']} (expected {r['expected_trigger']}) {r['result']}")
                out.write_text(json.dumps(prev, indent=1) + "\n", encoding="utf8")
    finally:
        m.lua(UNHOOK_LUA)


if __name__ == "__main__":
    main(sys.argv[1:])
