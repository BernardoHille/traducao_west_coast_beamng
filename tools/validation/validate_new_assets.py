"""new_asset_spec validation: assets without a game original (Phase 5 R-19) + functional level overrides.

Textures are checked against the declared spec (no original to compare with), materials must point to
textures shipped by the mod and may not redefine game materials, meshes must keep the original
structure (only materials/UVs may change) and ship an up-to-date compiled .cdae, and every overridden
level file may differ from the game file only in declared speedLimit values.
"""
import fnmatch
import json
import os
import re
import sys
import zipfile

import numpy as np
from PIL import Image

import dds_parser
from common import FAIL, PASS, REPO, SKIP, WARN, Report, load_config, rel

MOD_NAME = "traducao_ptbr_wcusa"
MOD_DIR = os.path.join(REPO, "mod", MOD_NAME)


def _png(path):
    return np.asarray(Image.open(path).convert("RGBA"))


def check_texture(rep, fam, t):
    path = os.path.join(MOD_DIR, fam["dir"], t["file"])
    name = f"{t['file']}"
    if not os.path.exists(path):
        rep.add(FAIL, f"{name}: present", f"missing in the mod: {fam['dir']}/{t['file']}")
        return
    try:
        info = dds_parser.parse(path)
    except dds_parser.DDSError as e:
        rep.add(FAIL, f"{name}: DDS header", str(e))
        return
    problems = []
    if (info["width"], info["height"]) != (t["width"], t["height"]):
        problems.append(f"resolution {info['width']}x{info['height']} != {t['width']}x{t['height']}")
    if info["format"] != t["format"]:
        problems.append(f"format {info['format']} != {t['format']}")
    if t["srgb"] and info["srgb"] is not True:
        problems.append("colour map must be sRGB")
    if not t["srgb"] and info["srgb"] is True:
        problems.append("data map must be linear")
    if t.get("mips") == "full" and info["mip_count"] != info["full_mip_count"]:
        problems.append(f"mipmaps {info['mip_count']} != full chain {info['full_mip_count']}")
    if info["file_size"] != info["expected_size"]:
        problems.append(f"file size {info['file_size']} != {info['expected_size']}")
    if t.get("alpha_modes") and info.get("alpha_mode") and info["alpha_mode"] not in t["alpha_modes"]:
        problems.append(f"alpha mode {info['alpha_mode']}")
    rep.add(FAIL if problems else PASS, f"{name}: spec", "; ".join(problems) if problems else dds_parser.describe(info))
    src = os.path.join(REPO, t.get("source_png", ""))
    if t.get("source_png") and os.path.exists(src):
        a = _png(src)
        if a.shape[1] != t["width"] or a.shape[0] != t["height"]:
            rep.add(FAIL, f"{name}: source PNG", f"{a.shape[1]}x{a.shape[0]} != spec")
        if "disc" in t:
            d, m = t["disc"], a[..., 0].astype(float)
            corners = [m[0, 0], m[0, -1], m[-1, 0], m[-1, -1], m[0, m.shape[1] // 2], m[-1, m.shape[1] // 2]]
            cov = float((m >= 128).mean())
            probs = []
            if max(corners) > d["corners_max"]:
                probs.append(f"corners/top/bottom not transparent ({max(corners):.0f})")
            if m[m.shape[0] // 2, m.shape[1] // 2] < d["center_min"]:
                probs.append("centre not opaque")
            if not d["coverage_range"][0] <= cov <= d["coverage_range"][1]:
                probs.append(f"coverage {cov:.3f} outside {d['coverage_range']}")
            rep.add(FAIL if probs else PASS, f"{name}: disc mask", "; ".join(probs) if probs else
                    f"corners transparent, centre opaque, coverage {cov:.3f} (alphaTest 128)")
    elif t.get("source_png"):
        rep.add(WARN, f"{name}: source PNG", f"master render not found ({t['source_png']}); run working/layered/r19/build_r19.py")


def check_halo(rep, fam):
    h = fam.get("halo_check")
    if not h:
        return
    tex = {t["file"]: t for t in fam["textures"]}
    mpath = os.path.join(REPO, tex[h["opacity"]]["source_png"])
    if not os.path.exists(mpath):
        rep.add(SKIP, "Edge halo", "opacity master not rendered")
        return
    m = _png(mpath)[..., 0].astype(int)
    edge = (m >= 16) & (m <= 240)
    for f in h["color"]:
        c = _png(os.path.join(REPO, tex[f]["source_png"]))[..., :3].astype(float)
        dist = np.linalg.norm(c[edge] - np.array(h["border_rgb"], float), axis=1)
        bad = int((dist > h["max_distance"]).sum())
        rep.add(FAIL if bad else PASS, f"{f}: edge halo", f"{bad} of {int(edge.sum())} edge pixels far from the border colour"
                if bad else f"{int(edge.sum())} edge pixels carry the border colour (no halo)")


def check_materials(rep, fam):
    path = os.path.join(MOD_DIR, fam["dir"], fam["materials_file"])
    if not os.path.exists(path):
        rep.add(FAIL, "Materials file", f"missing: {fam['dir']}/{fam['materials_file']}")
        return
    try:
        with open(path, encoding="utf-8") as fh:
            mats = json.load(fh)
    except json.JSONDecodeError as e:
        rep.add(FAIL, "Materials file", f"invalid JSON: {e}")
        return
    bad_names = [n for n in mats if n in fam["forbidden_material_names"]]
    rep.add(FAIL if bad_names else PASS, "Materials: no game material redefined",
            f"redefines {bad_names}" if bad_names else f"{len(mats)} own materials, none named {fam['forbidden_material_names']}")
    for name, want in fam["materials"].items():
        m = mats.get(name)
        if not m:
            rep.add(FAIL, f"Material {name}", "not defined")
            continue
        st = (m.get("Stages") or [{}])[0]
        probs = []
        if m.get("name") != name or m.get("mapTo") != name:
            probs.append("name/mapTo mismatch")
        for key in ("baseColorMap", "opacityMap"):
            if key in want:
                v = st.get(key, "")
                if not v.endswith("/" + want[key]):
                    probs.append(f"{key} {v} != .../{want[key]}")
                elif not os.path.exists(os.path.join(MOD_DIR, v.lstrip("/"))):
                    probs.append(f"{key} {v} not shipped in the mod")
        if bool(m.get("alphaTest")) != want["alphaTest"] or int(m.get("alphaRef", -1)) != want["alphaRef"]:
            probs.append(f"alphaTest/alphaRef {m.get('alphaTest')}/{m.get('alphaRef')}")
        rep.add(FAIL if probs else PASS, f"Material {name}", "; ".join(probs) if probs else
                f"baseColor {os.path.basename(st.get('baseColorMap', ''))} · opacity {os.path.basename(st.get('opacityMap', ''))} · alphaTest {m.get('alphaRef')}")


def check_meshes(rep, fam):
    sys.path.insert(0, os.path.join(REPO, "tools", "production"))
    import r19_mesh  # noqa: E402
    from pathlib import Path
    for me in fam["meshes"]:
        new, orig = os.path.join(MOD_DIR, me["file"]), os.path.join(REPO, me["original"])
        label = os.path.basename(me["file"])
        if not os.path.exists(new):
            rep.add(FAIL, f"{label}: present", "missing in the mod")
            continue
        if not os.path.exists(orig):
            rep.add(SKIP, f"{label}: structure", f"original not extracted ({me['original']})")
        else:
            cmp = r19_mesh.compare(Path(orig), Path(new))
            allowed = {"triangles_per_material", "materials"}
            diff = [r["check"] for r in cmp["rows"] if not r["same"] and r["check"] not in allowed]
            rep.add(FAIL if diff else PASS, f"{label}: structure vs original",
                    f"changed: {diff}" if diff else "geometry, normals, vertex colours, triangle lists, node transforms and bounding box identical; only materials/UVs differ")
            mats = next(r["new"] for r in cmp["rows"] if r["check"] == "materials")
            rep.add(PASS if sorted(mats) == sorted(me["materials"]) else FAIL, f"{label}: materials", f"{mats}")
        cd = os.path.join(MOD_DIR, me["cdae"])
        if not os.path.exists(cd):
            rep.add(FAIL, f"{label}: compiled .cdae", "missing: the game would compile it into the user temp cache, which outlives the mod "
                                                       "(mod disabled -> stale R-19 shape); ship the engine-compiled .cdae")
        elif os.path.getmtime(cd) < os.path.getmtime(new):
            rep.add(FAIL, f"{label}: compiled .cdae", ".cdae older than .dae: the game would recompile into the user temp cache "
                                                       "(run tools/production/install_mod.py, which re-stamps it, or recompile)")
        else:
            rep.add(PASS, f"{label}: compiled .cdae", "present and newer than the .dae (no recompilation, no temp cache)")


def check_functional(rep, spec):
    pats = spec["functional_files"]["patterns"]
    files = []
    for root, _, names in os.walk(MOD_DIR):
        for n in names:
            r = os.path.relpath(os.path.join(root, n), MOD_DIR).replace("\\", "/")
            if any(fnmatch.fnmatch(r, p) for p in pats):
                files.append(r)
    if not files:
        rep.add(SKIP, "Functional overrides", "none in the mod")
        return
    rules = load_config("speed_rules.json")
    zpath = os.path.join(rules["paths"]["install_dir"], rules["paths"]["level_zip"])
    if not os.path.exists(zpath):
        rep.add(SKIP, "Functional overrides", "game zip not found")
        return
    inst_path = os.path.join(REPO, "working", "speed", "sign_instances.json")
    shapes = {}
    if os.path.exists(inst_path):
        with open(inst_path, encoding="utf-8") as fh:
            shapes = {i["persistentId"] if "persistentId" in i else i["pid"]: i["to"] for i in json.load(fh)["instances"]}
    total = 0
    with zipfile.ZipFile(zpath) as z:
        for f in sorted(files):
            if f.endswith("main.decals.json"):  # Phase 6: pavement phrases (instances deleted / rectIdx changed)
                sys.path.insert(0, os.path.join(REPO, "tools", "production"))
                import decal_overrides
                with open(decal_overrides.DECISIONS, encoding="utf-8") as fh:
                    dec = json.load(fh)
                with open(os.path.join(MOD_DIR, f), encoding="utf-8") as fh:
                    errs = decal_overrides.verify(fh.read(), dec)
                rep.add(FAIL if errs else PASS, f"Override {f}", "; ".join(errs) if errs else
                        f"only the declared decal instances differ ({len(dec['delete'])} deleted, "
                        f"{len(dec['set_rectIdx'])} rectIdx changed)")
                continue
            a = z.read(f).decode("utf-8").split("\n")
            with open(os.path.join(MOD_DIR, f), encoding="utf-8") as fh:
                b = fh.read().split("\n")
            if len(a) != len(b):
                rep.add(FAIL, f"Override {f}", f"line count {len(a)} -> {len(b)}")
                continue
            bad, n = [], 0
            for x, y in zip(a, b):
                if x == y:
                    continue
                n += 1
                if f.endswith("slotTraffic.json"):
                    if not re.fullmatch(r'\s*"speedLimit":\s*[-0-9.eE+]+,?', y) or re.sub(r"[-0-9.eE+]+", "N", x) != re.sub(r"[-0-9.eE+]+", "N", y):
                        bad.append(y.strip()[:60])
                else:
                    ox, oy = json.loads(x), json.loads(y)
                    pid = oy.get("persistentId")
                    if pid in shapes and oy.get("shapeName") == shapes[pid]:
                        ox.pop("shapeName", None)
                        oy.pop("shapeName", None)
                    ox.pop("speedLimit", None)
                    oy.pop("speedLimit", None)
                    if ox != oy:
                        bad.append(pid)
            total += n
            rep.add(FAIL if bad else PASS, f"Override {f}", f"{len(bad)} lines change more than speedLimit: {bad[:3]}" if bad
                    else f"{n} line(s) differ from the game file, only in speedLimit / declared shapeName")
    rep.meta["functional_changed_lines"] = total


def validate_new_assets(report=None):
    rep = report or Report("New assets (new_asset_spec)", rel(MOD_DIR))
    spec = load_config("new_assets.json")
    for fname, fam in spec["families"].items():
        for t in fam["textures"]:
            check_texture(rep, fam, t)
        check_halo(rep, fam)
        check_materials(rep, fam)
        check_meshes(rep, fam)
    check_functional(rep, spec)
    return rep


def declared_paths():
    """Mod-relative paths (lower case) declared by new_assets.json: textures, materials, meshes, cdae."""
    spec = load_config("new_assets.json")
    out = set()
    for fam in spec["families"].values():
        for t in fam["textures"]:
            out.add(f"{fam['dir']}/{t['file']}".lower())
        out.add(f"{fam['dir']}/{fam['materials_file']}".lower())
        for me in fam["meshes"]:
            out.add(me["file"].lower())
            out.add(me["cdae"].lower())
    return out, spec["functional_files"]["patterns"]
