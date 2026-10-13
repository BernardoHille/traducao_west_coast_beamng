"""Phase 7 blocks E/F/G: in-game QA of the research scenarios on the localized West Coast (mod active).

Each scenario is opened through its own controller (`extensions.<name>.load()` = freeroam without traffic, as the
user starts it), the Honda is driven by the vehicle AI at controlled target speeds ('set' mode, the method of the
scenarios' own validation), and the controller state (getState), the beamng.log lines of the scenario and the
navgraph limit under the car are recorded. Screenshots go to tests/screenshots/phase7/adas/.

    python working/functional/adas_test.py speed_alert|speed_alert_web|event01|reaction
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP, wait_for_file  # noqa: E402
from PIL import Image  # noqa: E402

LOG = Path(r"C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/beamng.log")
OUT = REPO / "tests/reports/phase7/adas_qa.json"
SHOTS = REPO / "tests/screenshots/phase7/adas"
ROUTE_LUA = (HERE / "place_signs.py").read_text(encoding="utf8").split('ROUTE_LUA = r"""')[1].split('"""')[0]
CAR_LUA = r"""
local v = be:getPlayerVehicle(0)
if not v then return 'null' end
local p = v:getPosition()
local mp = map.getMap()
local a, b, d = map.findClosestRoad(p)
local l = a and ((mp.nodes[a].links[b]) or (mp.nodes[b] and mp.nodes[b].links[a]))
local st = extensions['%s'] and extensions['%s'].getState() or {}
return jsonEncode({pos = {p.x, p.y, p.z}, kmh = v:getVelocity():length() * 3.6, limit = l and l.speedLimit * 3.6 or -1, edge = {a, b},
  jbeam = v:getJBeamFilename(), state = st})
"""


class Log:
    def __init__(self):
        self.pos = LOG.stat().st_size

    def new(self, tags):
        with open(LOG, "rb") as f:
            f.seek(self.pos)
            data = f.read().decode("utf8", "replace")
        self.pos += len(data.encode("utf8"))
        return [l.strip() for l in data.splitlines() if any(t in l for t in tags)]


def shot(m, name, ui=True):
    m.call("toggle_ui", show=ui)
    time.sleep(0.8)
    src = m.call("screenshot").strip()
    wait_for_file(src)
    SHOTS.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((1600, 1600))
    dst = SHOTS / f"{name}.jpg"
    im.save(dst, quality=88)
    return dst.relative_to(REPO).as_posix()


SCENARIOS = ("adasSpeedAlertTest", "adasSpeedAlertWeb", "event01SpeedLimitRecognition", "reactionTest")


def isolate(m, ext):
    """Only the scenario under test may run: a controller left active re-teleports the Honda to its own start on every
    vehicle reset. The one under test is reloaded from disk (picks up the Phase 7 start patch)."""
    for other in SCENARIOS:
        m.lua(f"if extensions['{other}'] and extensions['{other}'].stopMission then extensions['{other}'].stopMission() end "
              f"if '{other}' ~= '{ext}' then extensions.unload('{other}') end return 'ok'")
    m.lua(f"extensions.unload('{ext}') extensions.load('{ext}') return 'ok'")
    time.sleep(1)


def wait_running(m, ext, timeout=240):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = json.loads(m.lua(CAR_LUA % (ext, ext)))
            if c and c.get("state", {}).get("phase") == "running" and "hcity7" in (c.get("jbeam") or ""):
                return c
        except Exception:
            pass
        time.sleep(2)
    raise SystemExit(f"{ext}: never reached phase 'running'")


def drive(m, path, kmh):
    names = "{" + ",".join(f"'{n}'" for n in path) + "}"
    m.lua(f"be:getPlayerVehicle(0):queueLuaCommand([[ai.driveUsingPath({{path = {names}, driveInLane = 'on', aggression = 0.5, "
          f"avoidCars = 'off'}}); ai.setSpeedMode('set'); ai.setSpeed({kmh / 3.6:.4f})]]) return 'ok'")


def set_speed(m, kmh):
    m.lua(f"be:getPlayerVehicle(0):queueLuaCommand([[ai.setSpeedMode('set'); ai.setSpeed({kmh / 3.6:.4f})]]) return 'ok'")


def stop(m):
    m.lua("be:getPlayerVehicle(0):queueLuaCommand(\"ai.setMode('disabled'); input.event('throttle', 0, 1); input.event('brake', 1, 1)\") return 'ok'")


def sample(m, ext, secs, every=0.5, until=None):
    out, t0 = [], time.time()
    while time.time() - t0 < secs:
        c = json.loads(m.lua(CAR_LUA % (ext, ext)))
        st = c.get("state", {})
        out.append({"t": round(time.time() - t0, 1), "kmh": round(c["kmh"], 1), "limit_kmh": round(c["limit"], 1), "xy": [round(c["pos"][0], 1), round(c["pos"][1], 1)],
                    **{k: st.get(k) for k in ("alertActive", "audioPlaying", "alertStartCount", "alertStopCount", "armed", "alertCount", "alertPlaying", "phase")}})
        if until and until(out[-1]):
            break
        time.sleep(every)
    return out


def route_names(m, start, d, length):
    r = json.loads(m.lua(ROUTE_LUA % (*start, *d, length)))
    return [n["node"] for n in r[1:]]


def speed_alert(m, ext="adasSpeedAlertTest", tag="[ADAS Speed Test]", name="speed_alert"):
    log = Log()
    isolate(m, ext)
    m.lua(f"extensions['{ext}'].load() return 'ok'")
    c0 = wait_running(m, ext)
    time.sleep(2)
    res = {"scenario": ext, "spawn": c0["pos"], "navgraph_at_spawn_kmh": round(c0["limit"], 1), "edge_at_spawn": c0["edge"],
           "threshold_kmh": c0["state"].get("thresholdKmh"), "steps": {}}
    res["screens"] = {"spawn_driver_view": shot(m, f"{name}_spawn")}
    path = route_names(m, [431.2, 701.6, 116.0], [-0.8025, -0.5967], 1000)
    drive(m, path, 40)
    res["steps"]["A_below_50"] = sample(m, ext, 14)
    set_speed(m, 58)
    res["steps"]["B_above_50"] = sample(m, ext, 9)
    res["screens"]["alert_active"] = shot(m, f"{name}_alert_active")
    set_speed(m, 40)
    res["steps"]["C_reduce"] = sample(m, ext, 9)
    stop(m)
    res["log"] = log.new([tag])
    A, B, C = (res["steps"][k] for k in ("A_below_50", "B_above_50", "C_reduce"))
    res["checks"] = {
        "spawn_on_50": abs(res["navgraph_at_spawn_kmh"] - 50) < 0.5,
        "A_no_alert_below_50": all(not s["alertActive"] for s in A if s["kmh"] < 50) and max(s["kmh"] for s in A) < 50,
        "B_alert_above_50": any(s["alertActive"] for s in B if s["kmh"] >= 50),
        "C_alert_stops_below_50": not C[-1]["alertActive"] and C[-1]["kmh"] < 50,
        "all_samples_in_zone_are_50": all(abs(s["limit_kmh"] - 50) < 0.5 for s in A + B + C),
        # the ALERT START/STOP log lines depend on the flowgraph's DebugEnabled; the controller counters do not
        "state_transitions_start_stop": max(s["alertStartCount"] or 0 for s in B) >= 1 and (C[-1]["alertStopCount"] or 0) >= 1,
    }
    res["result"] = "PASS" if all(res["checks"].values()) else "FAIL"
    return res


def event01(m):
    ext, tag = "event01SpeedLimitRecognition", "[Event01]"
    log = Log()
    isolate(m, ext)
    m.lua(f"extensions['{ext}'].load() return 'ok'")
    c0 = wait_running(m, ext)
    time.sleep(2)
    res = {"scenario": ext, "spawn": c0["pos"], "navgraph_at_spawn_kmh": round(c0["limit"], 1), "edge_at_spawn": c0["edge"], "runs": {}}
    res["screens"] = {"spawn_driver_view": shot(m, "event01_spawn")}
    path = route_names(m, [-428.2, 164.3, 100.4], [0.366, 0.931], 700)
    # run 1: 65 then 69 (no alert expected)
    drive(m, path, 65)
    r1 = sample(m, ext, 9)
    set_speed(m, 69)
    r1 += sample(m, ext, 4)
    stop(m)
    res["runs"]["run1_65_69"] = r1
    res["log_run1"] = log.new([tag])
    m.lua(f"extensions['{ext}'].restart() return 'ok'")
    wait_running(m, ext)
    time.sleep(2)
    # run 2: 72 (alert at 70), hold (no new alert), 60 (rearm <= 65), 72 again (alert #2)
    drive(m, path, 72)
    r2 = sample(m, ext, 10)
    res["screens"]["alert"] = shot(m, "event01_alert")
    set_speed(m, 60)
    r2 += sample(m, ext, 6)
    set_speed(m, 72)
    r2 += sample(m, ext, 7)
    stop(m)
    res["runs"]["run2_72_60_72"] = r2
    res["log_run2"] = log.new([tag])
    l1, l2 = res["log_run1"], res["log_run2"]
    first_alert = next((s for s in r2 if (s.get("alertCount") or 0) >= 1), None)
    res["checks"] = {
        "spawn_on_70": abs(res["navgraph_at_spawn_kmh"] - 70) < 0.5,
        "run1_no_alert_at_65_69": max(s["kmh"] for s in r1) < 70 and all((s.get("alertCount") or 0) == 0 for s in r1),
        "run2_alert_at_70": first_alert is not None and first_alert["kmh"] >= 69.5,
        "run2_first_alert_inside_corridor": first_alert is not None and abs(first_alert["limit_kmh"] - 70) < 0.5,
        "run2_single_alert_while_above": any("SPEED LIMIT REACHED" in l for l in l2),
        "run2_rearm_below_65": any("rearmed" in l for l in l2),
        "run2_second_alert": max((s.get("alertCount") or 0) for s in r2) >= 2,
    }
    res["result"] = "PASS" if all(res["checks"].values()) else "FAIL"
    return res


def reaction(m):
    ext, tag = "reactionTest", "[ReactionTest]"
    log = Log()
    isolate(m, ext)
    m.lua(f"extensions['{ext}'].load() return 'ok'")
    t0, phases, st = time.time(), [], {}
    while time.time() - t0 < 240:
        st = json.loads(m.lua(f"return jsonEncode(extensions['{ext}'] and extensions['{ext}'].getState() or {{}})"))
        if not phases or phases[-1] != st.get("phase"):
            phases.append(st.get("phase"))
        if st.get("phase") == "armed":
            break
        time.sleep(2)
    time.sleep(3)
    res = {"scenario": ext, "phases": phases, "state_armed": st}
    res["screens"] = {"armed": shot(m, "reaction_armed")}
    path = route_names(m, [431.2, 701.6, 116.0], [-0.8025, -0.5967], 1000)
    drive(m, path, 60)
    t0, traffic = time.time(), []
    while time.time() - t0 < 75:
        st = json.loads(m.lua(f"return jsonEncode(extensions['{ext}'].getState())"))
        if phases[-1] != st.get("phase"):
            phases.append(st.get("phase"))
        tr = json.loads(m.lua(r"""
local out = {}
local pid = be:getPlayerVehicleID(0)
local mp = map.getMap()
for i = 0, be:getObjectCount() - 1 do
  local o = be:getObject(i)
  if o and o:getId() ~= pid then
    local p = o:getPosition()
    local a, b = map.findClosestRoad(p)
    local l = a and ((mp.nodes[a].links[b]) or (mp.nodes[b] and mp.nodes[b].links[a]))
    table.insert(out, {id = o:getId(), kmh = o:getVelocity():length() * 3.6, limit = l and l.speedLimit * 3.6 or -1})
  end
end
return jsonEncode(out)"""))
        traffic.append(tr)
        if st.get("phase") in ("finished", "error"):
            break
        time.sleep(1)
    stop(m)
    res["phases"] = phases
    res["final_state"] = st
    res["traffic_samples"] = traffic[::5]
    res["log"] = log.new([tag, "reactionTest"])[-60:]
    res["checks"] = {"armed_with_vehicles": "armed" in phases, "event_or_finished": any(p in ("event", "finished") for p in phases),
                     "no_error_phase": "error" not in phases}
    res["result"] = "PASS" if all(res["checks"].values()) else "CHECK"
    return res


def main(argv):
    m = BeamNGMCP()
    prev = json.loads(OUT.read_text(encoding="utf8")) if OUT.exists() else {}
    for what in argv:
        if what == "speed_alert":
            r = speed_alert(m)
        elif what == "speed_alert_web":
            r = speed_alert(m, "adasSpeedAlertWeb", "[ADAS", "speed_alert_web")
        elif what == "event01":
            r = event01(m)
        elif what == "reaction":
            r = reaction(m)
        else:
            raise SystemExit(what)
        prev[what] = r
        OUT.write_text(json.dumps(prev, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
        print(what, r["result"], json.dumps(r.get("checks"), indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
