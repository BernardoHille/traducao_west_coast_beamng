"""Phase 7 block J: the game's AI (speed mode 'legal') drives roads of each class and must respect the navgraph limit.

For each case the player vehicle is teleported to a start point, given the legal navgraph route ahead (same tracer as
place_signs.py) with ai.driveUsingPath + ai.setSpeedMode('legal'), and sampled every 0.25 s: speed, position and the
navgraph limit under the car. Only samples on edges of the case's class count. Writes tests/reports/phase7/ai_test.json.

    python working/functional/ai_test.py [case ...]
"""
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP  # noqa: E402

CASES = {
    "ai40_dr272": {"kmh": 40, "start": [-630.0, 66.0, 103.3], "dir": [0.70, 0.71], "len": 200, "secs": 30,
                   "doc": "DR272, via local (Fase 5, ex-25 mph)"},
    "ai40_toll": {"kmh": 40, "start": [-905.0, -580.0, 106.6], "dir": [0.72, 0.69], "len": 160, "secs": 25,
                  "doc": "Praça de pedágio, faixa DR630 entre as cabines (Fase 7, 40)"},
    "ai50_dr312": {"kmh": 50, "start": [431.2, 701.6, 116.2], "dir": [-0.8025, -0.5967], "len": 900, "secs": 55,
                   "doc": "DR312, zona ADAS 50 a partir do spawn"},
    "ai60_dr1009": {"kmh": 60, "start": [0.0, 1941.0, 86.3], "dir": [0.92, 0.40], "len": 600, "secs": 45,
                    "doc": "DR1009, ilha (ex-35 mph), passa pelo radar 7"},
    "ai60_dr989": {"kmh": 60, "start": [-782.0, 1803.0, 86.3], "dir": [-1.0, 0.0], "len": 360, "secs": 30,
                   "doc": "DR989, ilha (ex-35 mph), passa pelo radar 5"},
    "ai70_dr652": {"kmh": 70, "start": [-428.2, 164.3, 100.4], "dir": [0.366, 0.931], "len": 210, "secs": 22,
                   "doc": "DR652, corredor 70 do Event 01 (novo início)"},
    "ai80_dr282": {"kmh": 80, "start": [209.0, 24.0, 127.3], "dir": [0.0, 1.0], "len": 300, "secs": 30,
                   "doc": "DR282, via de mão dupla automática (80)"},
}
ROUTE_LUA = (HERE / "place_signs.py").read_text(encoding="utf8").split('ROUTE_LUA = r"""')[1].split('"""')[0]
START_LUA = r"""
local v = be:getPlayerVehicle(0)
local dir = vec3(%f, %f, 0):normalized()
local rot = quatFromDir(dir, vec3(0, 0, 1))
spawn.safeTeleport(v, vec3(%f, %f, %f), rot, nil, nil, nil, true)
v:queueLuaCommand("ai.setMode('disabled'); electrics.values.parkingbrake = 0; input.event('parkingbrake', 0, 1); controller.mainController.setStarter(true)")
return 'ok'
"""
DRIVE_LUA = r"""
local v = be:getPlayerVehicle(0)
v:queueLuaCommand([[ai.driveUsingPath({path = %s, driveInLane = 'on', aggression = 0.3, avoidCars = 'off'}); ai.setSpeedMode('legal')]])
return 'ok'
"""
SAMPLE_LUA = r"""
local v = be:getPlayerVehicle(0)
local p = v:getPosition()
local mp = map.getMap()
local a, b, d = map.findClosestRoad(p)
local l = a and ((mp.nodes[a].links[b]) or (mp.nodes[b] and mp.nodes[b].links[a]))
return jsonEncode({p.x, p.y, v:getVelocity():length(), l and l.speedLimit or -1, d or -1, a or '', b or ''})
"""


def lua_list(names):
    return "{" + ",".join(f"'{n}'" for n in names) + "}"


def run_case(m, cid, c):
    route = json.loads(m.lua(ROUTE_LUA % (*c["start"], *c["dir"], c["len"])))
    names = [r["node"] for r in route][1:]  # the first node is behind the car
    m.lua(START_LUA % (*c["dir"], *c["start"]))
    time.sleep(2.5)
    m.lua(DRIVE_LUA % lua_list(names))
    t0 = time.time()
    samples = []
    while time.time() - t0 < c["secs"]:
        s = json.loads(m.lua(SAMPLE_LUA))
        samples.append({"t": round(time.time() - t0, 2), "x": round(s[0], 1), "y": round(s[1], 1), "v_kmh": round(s[2] * 3.6, 2),
                        "limit_kmh": round(s[3] * 3.6, 1), "d": round(s[4], 1), "edge": [s[5], s[6]]})
        time.sleep(0.25)
    m.lua("be:getPlayerVehicle(0):queueLuaCommand(\"ai.setMode('disabled'); input.event('brake', 1, 1)\") return 'ok'")
    on = [s for s in samples if abs(s["limit_kmh"] - c["kmh"]) < 0.5 and s["d"] < 6]
    sp = sorted(s["v_kmh"] for s in on)
    res = {"case": cid, "doc": c["doc"], "limit_kmh": c["kmh"], "route_nodes": names, "samples_total": len(samples),
           "samples_on_class": len(on)}
    if sp:
        p90 = sp[min(len(sp) - 1, int(math.ceil(0.9 * len(sp))) - 1)]
        res.update(max_kmh=sp[-1], p90_kmh=p90, reached_pct=round(100 * sp[-1] / c["kmh"], 1),
                   result="PASS" if sp[-1] <= c["kmh"] * 1.03 + 1.0 and sp[-1] >= 0.8 * c["kmh"] else "FAIL")
    else:
        res["result"] = "NO_SAMPLES"
    res["samples"] = samples
    return res


def main(argv):
    m = BeamNGMCP()
    m.call("toggle_ui", show=False)
    out = REPO / "tests/reports/phase7/ai_test.json"
    prev = json.loads(out.read_text(encoding="utf8")) if out.exists() else {}
    for cid in (argv or list(CASES)):
        r = run_case(m, cid, CASES[cid])
        prev[cid] = r
        print(cid, r["result"], r.get("max_kmh"), r.get("p90_kmh"), f"{r['samples_on_class']}/{r['samples_total']}")
        out.write_text(json.dumps(prev, indent=1, ensure_ascii=False) + "\n", encoding="utf8")


if __name__ == "__main__":
    main(sys.argv[1:])
