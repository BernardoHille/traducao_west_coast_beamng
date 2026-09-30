"""Structural speed consistency: visual sign == road limit == radar == zone (== ADAS for limit-alert systems).

Offline sources (read-only): level zip (explicit road limits, radars, zones), gameplay/ missions,
ADAS mod Lua. Runtime source: a navgraph snapshot of road limits at signs/radars/ADAS spawns,
collected through the BeamNG MCP (`--refresh`) and stored in tools/validation/data/.
Nothing in the game is modified.
"""
import datetime as dt
import glob
import json
import math
import os
import re
import sys
import zipfile

from common import FAIL, PASS, REPO, SKIP, WARN, Report, ToolError, load_config, thresholds

MPH = 1.609344


# ------------------------------------------------------------------ units
def kmh(mps):
    return mps * 3.6


def mps(kmh_value):
    return kmh_value / 3.6


def same_speed(a_mps, b_mps, tol=None):
    tol = thresholds()["speed_mps_tolerance"] if tol is None else tol
    return abs(a_mps - b_mps) <= tol


def is_multiple_of_10(mps_value):
    t = thresholds()
    v = kmh(mps_value)
    step = t["speed_multiple_kmh"]
    return abs(v - round(v / step) * step) <= t["speed_multiple_tolerance_kmh"]


def fmt(mps_value):
    return f"{kmh(mps_value):.1f} km/h ({mps_value:.4g} m/s)"


def point_in_polygon(x, y, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i][0], poly[i][1]
        xj, yj = poly[j][0], poly[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


# ------------------------------------------------------------------ offline data
def _paths():
    r = load_config("speed_rules.json")
    return r, {k: v for k, v in r["paths"].items()}


def load_static():
    rules, p = _paths()
    install, user = p["install_dir"], p["user_dir"]
    zpath = os.path.join(install, p["level_zip"])
    if not os.path.exists(zpath):
        raise ToolError(f"level zip not found: {zpath} (install_dir in config/speed_rules.json)")
    data = {"explicit_roads": [], "radars": [], "zones": [], "mission_zones": [], "arrive": [], "adas": []}
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            if not name.endswith("items.level.json"):
                continue
            for line in z.read(name).decode("utf-8", "replace").splitlines():
                if '"speedLimit"' not in line:
                    continue
                o = json.loads(line)
                v = float(o["speedLimit"])
                rec = {"file": name.split("/MissionGroup/")[-1], "class": o.get("class"), "name": o.get("name") or o.get("internalName"),
                       "persistentId": o.get("persistentId"), "position": o.get("position"), "speed_mps": v}
                if o.get("class") == "BeamNGTrigger":
                    rec["speedTrapType"] = o.get("speedTrapType")
                    data["radars"].append(rec)
                else:
                    data["explicit_roads"].append(rec)
        sites = json.loads(z.read("levels/west_coast_usa/city.sites.json"))
        for zn in sites.get("zones", []):
            vals = zn.get("customFields", {}).get("values", {})
            if "speedLimit" in vals:
                data["zones"].append({"name": zn["name"], "speed_mps": float(vals["speedLimit"]),
                                      "polygon": [v[:2] if isinstance(v, list) else v["pos"][:2] for v in zn.get("vertices", [])],
                                      "source": "city.sites.json"})
    gpath = os.path.join(install, p["garages_sites"])
    if os.path.exists(gpath):
        with open(gpath, encoding="utf-8") as f:
            for zn in json.load(f).get("zones", []):
                vals = zn.get("customFields", {}).get("values", {})
                if "speedLimit" in vals:
                    data["mission_zones"].append({"name": re.sub(r"\.name$", "", zn["name"]), "speed_mps": float(vals["speedLimit"]), "source": "garageToGarage/garages.sites.json"})
    for f in sorted(glob.glob(os.path.join(install, p["arrive_missions_glob"]))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        d = d.get("missionTypeData", d)
        s = json.dumps(d)
        lim = re.search(r'"speedLimit":\s*([0-9.]+)', s)
        act = re.search(r'"maxSpeedActive":\s*(true|false)', s)
        data["arrive"].append({"mission": os.path.basename(os.path.dirname(f)), "speed_mps": float(lim.group(1)) if lim else None,
                               "active": act and act.group(1) == "true"})
    for a in rules["adas"]:
        lua = os.path.join(user, p["mods_unpacked"], a["mod"], a["lua"])
        rec = dict(a, found=os.path.exists(lua))
        if rec["found"]:
            src = open(lua, encoding="utf-8", errors="replace").read()
            if a.get("threshold_var"):
                m = re.search(re.escape(a["threshold_var"]) + r"\s*=\s*([0-9.]+)", src)
                rec["threshold_kmh"] = float(m.group(1)) if m else None
            m = re.search(re.escape(a.get("spawn_var", "playerSpawn")) + r"\s*=\s*vec3\(\s*(-?[0-9.]+)\s*,\s*(-?[0-9.]+)\s*,\s*(-?[0-9.]+)", src)
            rec["spawn"] = [float(m.group(i)) for i in (1, 2, 3)] if m else None
        data["adas"].append(rec)
    return data


# ------------------------------------------------------------------ runtime snapshot (MCP)
SNAPSHOT_LUA = r"""
local pts = jsonDecode(%s)
local m = map.getMap()
local function limitAt(p)
  local n1, n2, dist = map.findClosestRoad(vec3(p[1], p[2], p[3]))
  local e = (n1 and m.nodes[n1] and m.nodes[n1].links[n2]) or (n2 and m.nodes[n2] and m.nodes[n2].links[n1])
  if not e then return nil end
  return {limit = e.speedLimit, node = n1, dist = dist, oneWay = e.oneWay, lanes = e.lanes}
end
local out = {signs = {}, points = {}}
for _, n in ipairs(scenetree.findClassObjects("TSStatic")) do
  local o = scenetree.findObject(n)
  if o then
    local s = (o:getField("shapeName", 0) or "")
    if s:lower():find("sign_speed%%d+%%.dae$") then
      local p = o:getPosition()
      local r = limitAt({p.x, p.y, p.z})
      table.insert(out.signs, {shape = s, pos = {p.x, p.y, p.z}, road = r})
    end
  end
end
for i, p in ipairs(pts) do out.points[i] = {id = p[4], road = limitAt(p)} end
return jsonEncode(out)
"""


def refresh_snapshot(static):
    sys.path.insert(0, os.path.join(REPO, "tools", "beamng"))
    from mcp_client import BeamNGMCP  # noqa: E402
    rules = load_config("speed_rules.json")
    m = BeamNGMCP()
    status = m.call_json("get_status")
    if rules["map"] not in (status.get("level") or ""):
        raise ToolError(f"load {rules['map']} in BeamNG before --refresh (current level: {status.get('level')})")
    pts = [[*r["position"], f"radar:{r['name']}"] for r in static["radars"]]
    pts += [[*a["spawn"], f"adas:{a['id']}"] for a in static["adas"] if a.get("spawn")]
    raw = m.lua(SNAPSHOT_LUA % json.dumps(json.dumps(pts)))
    snap = json.loads(raw)
    snap["meta"] = {"collected": dt.datetime.now().isoformat(timespec="seconds"), "level": status.get("level"),
                    "source": "MCP map.getMap() + map.findClosestRoad, TSStatic sign_speed*.dae"}
    path = os.path.join(REPO, rules["snapshot"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(snap, f, indent=1)
    return snap


def load_snapshot():
    path = os.path.join(REPO, load_config("speed_rules.json")["snapshot"])
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ rules
def validate_speeds(refresh=False, report=None, static=None, snapshot=None):
    rep = report or Report("Speed consistency", "west_coast_usa")
    rules = load_config("speed_rules.json")
    static = static or load_static()
    if refresh:
        snapshot = refresh_snapshot(static)
    snapshot = snapshot if snapshot is not None else load_snapshot()
    rows = []

    # 1. explicit regulatory values must be multiples of 10 km/h
    by_val = {}
    for r in static["explicit_roads"]:
        by_val.setdefault(round(r["speed_mps"], 4), []).append(r)
    bad = {v: rs for v, rs in by_val.items() if not is_multiple_of_10(v)}
    ok = {v: rs for v, rs in by_val.items() if is_multiple_of_10(v)}
    if bad:
        rep.add(FAIL, "Road limits: multiples of 10 km/h",
                f"{sum(len(x) for x in bad.values())} explicit road limits are not multiples of 10: "
                + "; ".join(f"{fmt(v)} ×{len(rs)}" for v, rs in sorted(bad.items())),
                objects=[{"file": r["file"], "persistentId": r["persistentId"], "speed_mps": r["speed_mps"]} for rs in bad.values() for r in rs])
    else:
        rep.add(PASS, "Road limits: multiples of 10 km/h", f"{sum(len(x) for x in ok.values())} explicit limits OK")

    for label, zones in (("Map zones", static["zones"]), ("Mission zones (garageToGarage)", static["mission_zones"])):
        badz = [z for z in zones if not is_multiple_of_10(z["speed_mps"])]
        if not zones:
            rep.add(SKIP, label, "no zone with speedLimit found")
        elif badz:
            rep.add(FAIL, label, "not multiples of 10: " + "; ".join(f"{z['name'].split('.')[-1]} {fmt(z['speed_mps'])}" for z in badz))
        else:
            rep.add(PASS, label, f"{len(zones)} zones OK")

    # 2. radars: regulatory value and radar == road
    for r in static["radars"]:
        tag = r["name"] or r["persistentId"]
        rows_entry = {"location": f"radar {tag} @ {[round(x) for x in r['position'][:2]]}", "sign": "—", "radar": fmt(r["speed_mps"])}
        road = None
        if snapshot:
            road = next((p["road"] for p in snapshot.get("points", []) if p["id"] == f"radar:{r['name']}"), None)
        zone = next((z for z in static["zones"] if point_in_polygon(r["position"][0], r["position"][1], z["polygon"])), None)
        rows_entry["zone"] = f"{zone['name'].split('.')[-1]} {fmt(zone['speed_mps'])}" if zone else "—"
        if not is_multiple_of_10(r["speed_mps"]):
            rep.add(FAIL, f"Radar {tag}: regulatory value", f"{fmt(r['speed_mps'])} is not a multiple of 10 km/h")
        if road is None or road.get("limit") is None:
            rep.add(SKIP, f"Radar {tag} vs road", "no navgraph snapshot (run: validate.py speeds --refresh with the map loaded)")
            rows_entry.update(road="?", result="SKIP")
        else:
            rows_entry["road"] = fmt(road["limit"])
            if same_speed(r["speed_mps"], road["limit"]):
                rep.add(PASS, f"Radar {tag} vs road", f"radar {fmt(r['speed_mps'])} == road")
                rows_entry["result"] = "PASS"
            elif zone and same_speed(r["speed_mps"], zone["speed_mps"]):
                rep.add(PASS, f"Radar {tag} vs road", f"radar {fmt(r['speed_mps'])} matches explicit zone {zone['name']}")
                rows_entry["result"] = "PASS (zone)"
            else:
                rep.add(FAIL, f"Radar {tag} vs road", f"radar {fmt(r['speed_mps'])} ≠ road {fmt(road['limit'])} and no zone regulates the radar value")
                rows_entry["result"] = "FAIL"
        rows.append(rows_entry)

    # 3. visual speed signs vs road
    pat = re.compile(rules["sign_shapes"]["pattern"], re.I)
    unit = rules["sign_shapes"]["current_unit"]
    if not snapshot:
        rep.add(SKIP, "Speed signs vs road", "no navgraph snapshot (run: validate.py speeds --refresh with the map loaded)")
    else:
        groups = {}
        for s in snapshot.get("signs", []):
            mm = pat.search(s["shape"])
            if not mm:
                continue
            val = float(mm.group(1))
            sign_mps = mps(val * MPH) if unit == "mph" else mps(val)
            road = (s.get("road") or {}).get("limit")
            res = "SKIP" if road is None else ("PASS" if same_speed(sign_mps, road) else "FAIL")
            groups.setdefault((val, unit), []).append((s, road, res))
            rows.append({"location": f"{os.path.basename(s['shape'])} @ {[round(x) for x in s['pos'][:2]]}",
                         "sign": f"{val:g} {unit} (= {kmh(sign_mps):.1f} km/h)", "road": fmt(road) if road else "?",
                         "radar": "—", "zone": "—", "result": res})
        for (val, u), items in sorted(groups.items()):
            if u != "km/h":
                rep.add(FAIL, f"Speed sign {val:g} {u}: unit", f"{len(items)} signs show {u}; project rule is km/h (R-19)")
            fails = [i for i in items if i[2] == "FAIL"]
            roads = sorted({round(kmh(i[1]), 1) for i in items if i[1]})
            if fails:
                rep.add(FAIL, f"Speed sign {val:g} {u} vs road", f"{len(fails)}/{len(items)} signs disagree with the road limit next to them (roads: {roads} km/h)")
            else:
                rep.add(PASS, f"Speed sign {val:g} {u} vs road", f"{len(items)} signs agree with the road")

    # 4. ADAS
    for a in static["adas"]:
        name = f"ADAS {a['id']} ({a['classification']})"
        if not a.get("found"):
            rep.add(SKIP, name, "mod not installed")
            continue
        if a["classification"] not in rules["adas_classes_compared_to_road"]:
            rep.add(SKIP, name, f"experimental_speed_range {a.get('range_kmh')} km/h — excluded from sign == road rule by policy")
            rows.append({"location": f"ADAS {a['id']}", "sign": "—", "road": "—", "radar": "—", "zone": "—", "adas": f"range {a.get('range_kmh')} km/h (experimental)", "result": "SKIP"})
            continue
        thr = a.get("threshold_kmh")
        road = None
        if snapshot:
            road = next((p["road"] for p in snapshot.get("points", []) if p["id"] == f"adas:{a['id']}"), None)
        row = {"location": f"ADAS {a['id']} spawn {[round(x) for x in (a.get('spawn') or [])[:2]]}", "sign": "—", "radar": "—", "zone": "—",
               "adas": f"{thr} km/h", "road": fmt(road["limit"]) if road and road.get("limit") else "?"}
        if thr is None:
            rep.add(WARN, name, "threshold constant not found in Lua (config threshold_var)")
            row["result"] = "WARN"
        elif not road or road.get("limit") is None:
            rep.add(SKIP, name, "no navgraph snapshot for the spawn point")
            row["result"] = "SKIP"
        elif same_speed(mps(thr), road["limit"]):
            rep.add(PASS, name, f"threshold {thr} km/h == regulated road at spawn")
            row["result"] = "PASS"
        else:
            rep.add(FAIL, name, f"threshold {thr} km/h ≠ road limit at the scenario start ({fmt(road['limit'])}); limit-alert systems must follow the regulated road")
            row["result"] = "FAIL"
        rows.append(row)

    # 5. arrive missions
    for a in static["arrive"]:
        if a["speed_mps"] is None:
            continue
        rep.add(SKIP if not a["active"] else (PASS if is_multiple_of_10(a["speed_mps"]) else FAIL),
                f"Mission arrive/{a['mission']}", f"speedLimit {fmt(a['speed_mps'])}" + (" (maxSpeedActive=false, inactive)" if not a["active"] else ""))

    if snapshot:
        rep.meta["snapshot"] = snapshot.get("meta", {})
    head = "| Local | Placa | Via | Radar | Zona | ADAS | Resultado |\n|---|---|---|---|---|---|---|\n"
    body = "".join(f"| {r['location']} | {r.get('sign', '—')} | {r.get('road', '—')} | {r.get('radar', '—')} | {r.get('zone', '—')} | {r.get('adas', '—')} | {r.get('result', '')} |\n" for r in rows)
    rep.meta["_appendix_md"] = "## Tabela de consistência\n\n" + head + body
    rep.meta["rows"] = rows
    return rep
