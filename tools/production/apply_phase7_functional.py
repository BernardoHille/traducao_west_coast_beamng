"""Phase 7 functional integration: one deterministic build of every functional override of the mod.

Decisions (reviewed, versioned):
    working/functional/phase7_plan.json      the plan: nothing changes unless an entry here lists it
    working/speed/speed_changes.json         Phase 5 (10/40 km/h roads), reapplied unchanged
    working/functional/speed_changes.json    Phase 7 roads (60/70/50/120) and inert waypoints
    working/functional/radar_changes.json    radars (speed traps)
    working/functional/zone_changes.json     zone speedLimit values (city.sites.json, garageToGarage garages.sites.json)
    working/functional/adas_zones.json       ADAS corridors: new R-19 signs (positions measured by place_signs.py),
                                             research-scenario start patch
    working/functional/fuel_units.json       level info localUnits

Outputs (mod overrides, regenerated from the local game install; gitignored copies of game files):
    levels/west_coast_usa/main/MissionGroup/**/items.level.json   speedLimit edits + new group ptbr_functional_signs
    levels/west_coast_usa/slotTraffic.json                       derived lane limits (Phase 5 method)
    levels/west_coast_usa/city.sites.json, levels/west_coast_usa/info.json
    gameplay/missions/west_coast_usa/garageToGarage/globalinfo/garages.sites.json
    tools/validation/config/sign_regulation.json
    tests/reports/phase7/functional_diff.json / .md               structured diff + verification

    python tools/production/apply_phase7_functional.py               # build + verify
    python tools/production/apply_phase7_functional.py --check       # verify the mod against the game files only
    python tools/production/apply_phase7_functional.py --scenarios   # also patch the ADAS research mods (outside the
                                                                     # repo, current/mods/unpacked; backup kept in the
                                                                     # mod's _archive/)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
import uuid
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import speed_overrides as SO  # noqa: E402

INSTALL = Path(r"C:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive")
USER_MODS = Path(r"C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/mods/unpacked")
FUNC = REPO / "working/functional"
MOD = REPO / "mod/traducao_ptbr_wcusa"
OUT = REPO / "tests/reports/phase7"
LEVEL = "levels/west_coast_usa/"
NS = uuid.uuid5(uuid.NAMESPACE_URL, "traducao_ptbr_wcusa/phase7")   # deterministic persistentIds of the new objects
R19_DIR = "/levels/west_coast_usa/art/shapes/objects/roadsigns_ptbr"


def load(name):
    return json.loads((FUNC / name).read_text(encoding="utf8"))


def rnd(v, n=6):
    r = round(float(v), n)
    return 0.0 if r == 0 else r


def line(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


# ---------------------------------------------------------------- plan
def check_plan(plan, records):
    """Every record points to a plan entry; every object the plan lists is changed exactly as listed."""
    errs = []
    ids = {e["id"]: e for e in plan["entries"]}
    for kind, recs in records.items():
        if kind == "plate" or recs is None:   # plates are matched against the plan entries listing them (below)
            continue
        for r in recs:
            if r.get("plan_id") not in ids:
                errs.append(f"{kind} {r.get('id')}: plan_id {r.get('plan_id')!r} not in the plan")
    listed = {}
    for e in plan["entries"]:
        for o in e["roads"]:
            listed[("obj", o["persistentId"])] = (e["id"], o["to"])
        for o in e["radars"]:
            listed[("obj", o["persistentId"])] = (e["id"], o["to"])
        for o in e["zones"]:
            listed[("zone", o["file"], o["zone"])] = (e["id"], o["to"])
        for o in e["missions"]:
            if "zone" in o:
                listed[("zone", o["file"], o["zone"])] = (e["id"], o["to"])
        for o in e["visual_signs"]:
            listed[("sign", o["id"])] = (e["id"], o["value_kph"])
    got = {}
    for r in records["speed"] + records["radar"]:
        got[("obj", r["pid"])] = (r["plan_id"], r["to"])
    for r in records["zone"]:
        got[("zone", r["file"], r["zone"])] = (r["plan_id"], r["to"])
    for s in records["sign"]:
        got[("sign", s["id"])] = (s["plan_id"], s["value"])
    for e in plan["entries"]:
        for o in e.get("visual_plates", []):
            listed[("plate", o["id"])] = (e["id"], o["value_kmh"])
    for pl in records.get("plate", []):
        got[("plate", pl["id"])] = ("roadsigns_speed_plates", pl["value_kmh"])
    if records.get("plate") is not None:
        got[("plate", "toll_booth")] = ("toll_plaza_40", 40)
    for k in sorted(set(listed) | set(got), key=str):
        if listed.get(k) != got.get(k):
            errs.append(f"plan vs decisions: {k}: plan {listed.get(k)} / decisions {got.get(k)}")
    return errs


# ---------------------------------------------------------------- new sign objects
def yaw_quat(fx, fy):
    """quatFromDir(dir, up) for a horizontal direction (same convention as the game: theta = 90 deg - heading)."""
    th = math.pi / 2 - math.atan2(fy, fx)
    return [0.0, 0.0, math.sin(th / 2), math.cos(th / 2)]


def sign_objects(adas):
    """TSStatic R-19 + pole per sign, mounted like an original West Coast speed sign (adas_zones.json sign_template).
    rotationMatrix rows are the world directions of the local axes: the R-19 face is local -Y, so local +Y = flow."""
    tpl = adas["sign_template"]
    group = tpl["group"]
    objs = [{"name": group, "class": "SimGroup", "persistentId": str(uuid.uuid5(NS, group)), "__parent": "MissionGroup"}]
    lines = []
    reg = []
    for s in adas["signs"]:
        m = s.get("_measured")
        if not m or m.get("ground_z") is None:
            raise SystemExit(f"sign {s['id']}: not measured (python working/functional/place_signs.py)")
        fx, fy = m["flow"]
        n = math.hypot(fx, fy)
        fx, fy = fx / n, fy / n
        x, y = m["xy"]
        g = m["ground_z"]
        shape = f"{R19_DIR}/sign_r19_{s['value']}.dae"
        sign = {"name": f"ptbr_{s['id']}", "class": "TSStatic", "persistentId": str(uuid.uuid5(NS, s["id"])), "__parent": group,
                "position": [rnd(x), rnd(y), rnd(g + tpl["sign_height_m"])], "isRenderEnabled": False,
                "rotationMatrix": [rnd(fy), rnd(-fx), 0, rnd(fx), rnd(fy), 0, 0, 0, 1], "shapeName": shape,
                "useInstanceRenderData": True}
        b = tpl["pole_behind_m"]
        pole = {"name": f"ptbr_{s['id']}_pole", "class": "TSStatic", "persistentId": str(uuid.uuid5(NS, s["id"] + "/pole")),
                "__parent": group, "position": [rnd(x + b * fx), rnd(y + b * fy), rnd(g + tpl["pole_height_m"])], "annotation": "POLE",
                "isRenderEnabled": False, "rotationMatrix": [rnd(-fy), rnd(fx), 0, rnd(fx), rnd(fy), 0, 0, 0, -1],
                "shapeName": tpl["pole_shape"], "useInstanceRenderData": True}
        lines += [line(sign), line(pole)]
        reg.append({"shape": f"sign_r19_{s['value']}", "persistentId": sign["persistentId"], "position": [round(v, 2) for v in sign["position"]],
                    "group": group, "added_by": "phase7", "id": s["id"], "regulated_roads": s["_regulated"]})
    return {"append": {"items.level.json": [line(objs[0])]}, "new": {f"{group}/items.level.json": lines}}, reg


# ---------------------------------------------------------------- zone / info files (whole-file overrides)
def zone_index(doc, name):
    hits = [i for i, z in enumerate(doc.get("zones", [])) if z.get("name") == name and "speedLimit" in z.get("customFields", {}).get("values", {})]
    if len(hits) != 1:
        raise SystemExit(f"zone {name}: {len(hits)} zones with a speedLimit")
    return hits[0]


def edit_zones(raw, changes):
    """Replace customFields.values.speedLimit of the declared zones, byte-minimal: each numeric speedLimit token of the
    file is mapped to its zone by a probe parse, only the declared ones are rewritten."""
    doc = json.loads(raw)
    target = {}
    for c in changes:
        i = zone_index(doc, c["zone"])
        v = doc["zones"][i]["customFields"]["values"]["speedLimit"]
        if abs(v - c["from"]) > 1e-6:
            raise SystemExit(f"zone {c['zone']}: expected {c['from']}, found {v}")
        target[i] = c
    out, pos = [], 0
    for m in re.finditer(r'("speedLimit"\s*:\s*)(-?[0-9][0-9.eE+-]*)', raw):
        probe = json.loads(raw[:m.start(2)] + "-987654.5" + raw[m.end(2):])
        zi = [i for i, z in enumerate(probe.get("zones", [])) if z.get("customFields", {}).get("values", {}).get("speedLimit") == -987654.5]
        if len(zi) == 1 and zi[0] in target:
            out.append(raw[pos:m.start(2)] + repr(float(target[zi[0]]["to"])))
            pos = m.end(2)
    out.append(raw[pos:])
    return "".join(out)


def verify_zones(orig_raw, new_raw, changes):
    a, b = json.loads(orig_raw), json.loads(new_raw)
    errs = []
    for c in changes:
        i = zone_index(a, c["zone"])
        if abs(b["zones"][i]["customFields"]["values"]["speedLimit"] - c["to"]) > 1e-9:
            errs.append(f"{c['zone']}: value {b['zones'][i]['customFields']['values']['speedLimit']} != {c['to']}")
        b["zones"][i]["customFields"]["values"]["speedLimit"] = a["zones"][i]["customFields"]["values"]["speedLimit"]
    if a != b:
        errs.append("differs beyond the declared zone speedLimit values")
    return errs


def edit_info(raw, change):
    # the block and its line break (the file uses CRLF); every other byte is kept
    new, n = re.subn(r'(\r?\n)[ \t]*"' + re.escape(change["remove_key"]) + r'"\s*:\s*\{[^{}]*\},[ \t]*\r?\n', r"\1", raw)
    if n != 1:
        raise SystemExit(f"info.json: {change['remove_key']} block not found exactly once")
    return new


def relaxed_json(text):
    """BeamNG's JSON dialect (trailing commas, // comments) -> Python objects (strings are left untouched)."""
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if ch == "\\":
                out.append(text[i + 1])
                i += 1
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
            out.append(ch)
        elif text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
            continue
        elif ch == ",":
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j < n and text[j] in "}]":
                i += 1
                continue
            out.append(ch)
        else:
            out.append(ch)
        i += 1
    return json.loads("".join(out))


def verify_info(orig_raw, new_raw, change):
    a, b = relaxed_json(orig_raw), relaxed_json(new_raw)
    errs = []
    if a.get(change["remove_key"]) != change["from"]:
        errs.append(f"game value {a.get(change['remove_key'])} != declared {change['from']}")
    a.pop(change["remove_key"], None)
    if change["remove_key"] in b or a != b:
        errs.append("differs beyond the removed key")
    return errs


def game_text(zf, change):
    if change["source"] == "level_zip":
        return zf.read(change["file"]).decode("utf8")
    return (INSTALL / change["file"]).read_text(encoding="utf8")


# ---------------------------------------------------------------- research-scenario patches (outside the repo)
def scenario_text(patch, adas):
    spawns = {s["id"]: s for s in adas.get("spawns", [])}
    reps = []
    for r in patch["replace"]:
        new = r.get("new")
        if new is None:
            m = spawns[r["spawn"]]["_measured"]
            fx, fy = m["flow"]
            q = yaw_quat(fx, fy)
            new = r["new_template"].format(x=f"{m['xy'][0]:.3f}", y=f"{m['xy'][1]:.3f}", z=f"{m['road_z'] + 0.2:.2f}",
                                           fx=f"{fx:.4f}", fy=f"{fy:.4f}", qz=f"{q[2]:.10f}", qw=f"{q[3]:.10f}")
        reps.append((r["old"], new))
    return reps


def apply_scenarios(adas, write):
    res = []
    for p in adas.get("scenario_patches", []):
        path = USER_MODS / p["mod"] / p["file"]
        if not path.exists():
            res.append({"id": p["id"], "file": str(path), "status": "mod not installed"})
            continue
        raw = path.read_bytes().decode("utf8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        new_text, state = text, []
        for old, new in scenario_text(p, adas):
            if new in new_text:
                state.append("already")
            elif new_text.count(old) == 1:
                new_text = new_text.replace(old, new)
                state.append("applied")
            else:
                raise SystemExit(f"{p['id']}: original text not found exactly once in {path}")
        out = new_text.replace("\n", "\r\n") if crlf else new_text
        status = "already applied" if all(s == "already" for s in state) else "applied"
        if write and status == "applied":
            bak = USER_MODS / p["mod"] / "_archive" / (path.name + ".pre_ptbr_phase7")
            bak.parent.mkdir(parents=True, exist_ok=True)
            if not bak.exists():
                shutil.copyfile(path, bak)
            path.write_bytes(out.encode("utf8"))
        elif not write and status == "applied":
            status = "pending (run with --scenarios)"
        res.append({"id": p["id"], "file": str(path), "status": status,
                    "sha256_before": hashlib.sha256(raw.encode("utf8")).hexdigest(),
                    "sha256_after": hashlib.sha256(out.encode("utf8")).hexdigest()})
    return res


# ---------------------------------------------------------------- build / verify
def decisions():
    plan = load("phase7_plan.json")
    p7 = load("speed_changes.json")["changes"]
    radar = load("radar_changes.json")["changes"]
    zones = load("zone_changes.json")["changes"]
    fuel = load("fuel_units.json")["changes"]
    adas = load("adas_zones.json")
    for s in adas["signs"]:
        s["_regulated"] = [{"persistentId": c["pid"], "file": c["file"], "to_mps": float(c["to"]), "category": c["category"]}
                           for c in p7 if c["pid"] in s["regulates"]]
        if len(s["_regulated"]) != len(s["regulates"]):
            raise SystemExit(f"sign {s['id']}: regulates a road without a decision")
    return plan, p7, radar, zones, fuel, adas


def verify_mod_file(rel):
    """For validate.py new: (errors, description) for the Phase 7 files that are not 'game file with edited
    speedLimit lines' (new / appended level files, zone files, level info); None for any other file."""
    plan, p7, radar, zones, fuel, adas = decisions()
    path = MOD / rel
    mg = LEVEL + "main/MissionGroup/"
    zf = zipfile.ZipFile(SO.GAME_ZIP)
    if rel.startswith(mg):
        additions, _ = sign_objects(adas)
        r = rel[len(mg):]
        b = path.read_text(encoding="utf8").split("\n")
        if r in additions["new"]:
            ok = b == list(additions["new"][r]) + [""]
            return ([] if ok else ["differs from the declared new objects"]), f"new file: exactly the {len(additions['new'][r])} declared objects"
        if r in additions["append"]:
            a = zf.read(rel).decode("utf8").split("\n")
            tail = 1 if a[-1] == "" else 0
            exp = a[:len(a) - tail] + list(additions["append"][r]) + [""] * tail
            return ([] if b == exp else ["differs from game file + declared objects"]), \
                f"game file + {len(additions['append'][r])} declared object(s) appended, nothing else"
        return None
    zs = [c for c in zones if c["file"] == rel]
    if zs:
        e = verify_zones(game_text(zf, zs[0]), path.read_text(encoding="utf8"), zs)
        return e, f"only the {len(zs)} declared zone speedLimit values differ"
    fs = [c for c in fuel if c["file"] == rel]
    if fs:
        e = verify_info(game_text(zf, fs[0]), path.read_text(encoding="utf8"), fs[0])
        return e, f"only the key {fs[0]['remove_key']} removed"
    return None


def slot_checks(zf, report):
    """Derived-file checks: no 35 mph value left, Phase 5 lane edits still present, only speedLimit numbers changed."""
    a = zf.read(SO.SLOT).decode("utf8").split("\n")
    b = (SO.MOD_LEVEL / "slotTraffic.json").read_text(encoding="utf8").split("\n")
    errs = []
    if len(a) != len(b):
        return [f"slotTraffic line count {len(a)} -> {len(b)}"]
    changed = 0
    for x, y in zip(a, b):
        if x != y:
            changed += 1
            if not re.fullmatch(r'\s*"speedLimit":\s*[-0-9.eE+]+,?', y) or re.sub(r"[-0-9.eE+]+", "N", x) != re.sub(r"[-0-9.eE+]+", "N", y):
                errs.append(f"slotTraffic: non-speedLimit change: {y.strip()[:60]}")
    left = [(i + 1, v) for i, k, o, v in SO.walk_speed_lines(b) if any(abs(v - m) <= SO.TOL for m in SO.MPH_VALUES)]
    if left:
        errs.append(f"slotTraffic: {len(left)} lanes still hold mph-derived values: {left[:3]}")
    p5 = json.loads(SO.REPORT.read_text(encoding="utf8")) if SO.REPORT.exists() else {}
    lost = [e for e in p5.get("slotTraffic", {}).get("edits", []) if b[e["line"] - 1].strip().rstrip(",").split(":")[-1].strip() != SO.c_num(e["new"])]
    if lost:
        errs.append(f"slotTraffic: {len(lost)} Phase 5 lane edits not present any more: {lost[:2]}")
    report["slotTraffic_checks"] = {"changed_lines": changed, "mph_values_left": len(left),
                                    "phase5_edits_checked": len(p5.get("slotTraffic", {}).get("edits", [])), "phase5_edits_lost": len(lost)}
    return errs


def run(check=False, scenarios=False):
    plan, p7, radar, zones, fuel, adas = decisions()
    plates_path = FUNC / "speed_plates.json"
    plates = json.loads(plates_path.read_text(encoding="utf8"))["plates"] if plates_path.exists() else None
    records = {"speed": p7, "radar": radar, "zone": zones, "sign": adas["signs"], "plate": plates}
    report = {"plan_errors": check_plan(plan, records)}
    if report["plan_errors"]:
        raise SystemExit("plan check failed:\n  " + "\n  ".join(report["plan_errors"]))
    changes = SO.load_changes()
    additions, added_signs = sign_objects(adas)
    zf = zipfile.ZipFile(SO.GAME_ZIP)
    if not check:
        report["level_files"] = SO.build_level_files(changes, zf, additions)
        SO.build_slot(changes, zf, report)
        SO.write_sign_regulation(changes, zf, added_signs)
        for group in sorted({c["file"] for c in zones}):
            cs = [c for c in zones if c["file"] == group]
            dst = MOD / group
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(edit_zones(game_text(zf, cs[0]), cs).encode("utf8"))
        for c in fuel:
            dst = MOD / c["file"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(edit_info(game_text(zf, c), c).encode("utf8"))
    # ---- verification (also the --check mode)
    v = {"level": SO.verify(changes, zf, additions)}
    errs = list(v["level"]["problems"])
    if not v["level"]["ok"]:
        errs.append("level files: " + v["level"]["summary"])
    errs += slot_checks(zf, report)
    for group in sorted({c["file"] for c in zones}):
        cs = [c for c in zones if c["file"] == group]
        e = verify_zones(game_text(zf, cs[0]), (MOD / group).read_text(encoding="utf8"), cs)
        v[group] = e or "OK"
        errs += [f"{group}: {x}" for x in e]
    for c in fuel:
        e = verify_info(game_text(zf, c), (MOD / c["file"]).read_text(encoding="utf8"), c)
        v[c["file"]] = e or "OK"
        errs += [f"{c['file']}: {x}" for x in e]
    report["scenarios"] = apply_scenarios(adas, write=scenarios and not check)
    report["verification"] = v
    report["errors"] = errs
    report["summary"] = summary(changes, p7, radar, zones, fuel, adas, report)
    if not check:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "functional_diff.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
        (OUT / "functional_diff.md").write_text(markdown(report, p7, radar, zones, fuel, adas), encoding="utf8")
    return report


def summary(changes, p7, radar, zones, fuel, adas, report):
    by = {}
    for c in p7 + radar:
        by.setdefault(f"{c['class']} -> {float(c['to']) * 3.6:.0f} km/h", []).append(c["id"])
    st = report.get("slotTraffic", {})
    return {"phase5_records": len(changes) - len(p7) - len(radar), "phase7_object_records": len(p7) + len(radar),
            "by_target": {k: len(v) for k, v in sorted(by.items())}, "zones": len(zones), "fuel": len(fuel),
            "new_signs": len(adas["signs"]), "new_objects": 1 + 2 * len(adas["signs"]),
            "slotTraffic_edited_lines": st.get("edited_lines"), "slotTraffic_equal_untouched": len(st.get("already_equal_untouched", [])),
            "slotTraffic_skipped": len(st.get("skipped_value_mismatch", []))}


def markdown(report, p7, radar, zones, fuel, adas):
    s = report["summary"]
    L = ["# Fase 7 — diff estruturado dos overrides funcionais", "",
         "Gerado por `tools/production/apply_phase7_functional.py`. Cada linha corresponde a uma decisão de `working/functional/`, "
         "ligada a uma entrada de `phase7_plan.json`.", "",
         f"**Verificação:** {'OK' if not report['errors'] else 'FALHA'} — {report['verification']['level']['summary']}.", ""]
    if report["errors"]:
        L += ["**Erros:**", ""] + [f"- {e}" for e in report["errors"]] + [""]
    L += ["## Objetos do nível (só o campo `speedLimit`)", "", "| Plano | Objeto | Classe | Arquivo | De (m/s) | Para (m/s) | km/h |", "|---|---|---|---|---|---|---|"]
    for c in p7 + radar:
        old = c["from"] if c["from"] is not None else f"auto {c.get('old_effective_mps')}"
        L.append(f"| {c['plan_id']} | {c.get('dr') or c.get('name')} `{c['pid'][:8]}` | {c['class']} | `{c['file']}` | {old} | {c['to']} | {float(c['to']) * 3.6:.0f} |")
    L += ["", "## Objetos novos (grupo `ptbr_functional_signs`)", "", "| Placa | Valor | Posição | Regulamenta |", "|---|---|---|---|"]
    for sg in adas["signs"]:
        L.append(f"| {sg['id']} | R-19 {sg['value']} | {sg['_measured']['xy']} | {', '.join(r['persistentId'][:8] for r in sg['_regulated'])} |")
    L += ["", f"Mais 1 `SimGroup` acrescentado ao `MissionGroup/items.level.json` e 1 poste `pole_fence1` por placa ({s['new_objects']} objetos).", "",
          "## Zonas (`customFields.values.speedLimit`)", "", "| Plano | Arquivo | Zona | De | Para |", "|---|---|---|---|---|"]
    for c in zones:
        L.append(f"| {c['plan_id']} | `{c['file']}` | {c['zone']} | {c['from']} | {c['to']} |")
    L += ["", "## Unidades", ""]
    for c in fuel:
        L.append(f"- `{c['file']}`: chave `{c['remove_key']}` removida (era {json.dumps(c['from'])}).")
    st = report.get("slotTraffic", {})
    if st:
        L += ["", "## slotTraffic.json", "",
              f"- linhas editadas: {st['edited_lines']} ({st['edited_road_properties']} faixas, {st['edited_links']} ligações);",
              f"- já iguais ao alvo (não tocadas): {len(st['already_equal_untouched'])}; valor divergente (não tocadas): {len(st['skipped_value_mismatch'])};",
              f"- vias sem faixa casada por geometria: {len(st['unmatched_roads'])}."]
    sc = report.get("slotTraffic_checks", {})
    if sc:
        L.append(f"- valores de mph restantes: {sc['mph_values_left']}; edições da Fase 5 conferidas: {sc['phase5_edits_checked']} (perdidas: {sc['phase5_edits_lost']}).")
    L += ["", "## Cenários de pesquisa (fora do repositório)", ""]
    for r in report["scenarios"]:
        L.append(f"- `{r['id']}`: {r['status']} (`{r['file']}`)")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only verify the existing mod files against the game files")
    ap.add_argument("--scenarios", action="store_true", help="also patch the ADAS research mods (backup in their _archive/)")
    a = ap.parse_args(argv)
    r = run(check=a.check, scenarios=a.scenarios)
    print(json.dumps(r["summary"], indent=1))
    for f in r.get("level_files", []):
        print(f"  {f['file']}: {f.get('edited_objects', 0)} edited, {f.get('appended_objects', f.get('added_objects', 0))} added")
    for s in r["scenarios"]:
        print(f"  scenario {s['id']}: {s['status']}")
    print(f"verification: {'OK' if not r['errors'] else 'FAIL'} {r['verification']['level']['summary']}")
    for e in r["errors"]:
        print("  -", e)
    return 0 if not r["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
