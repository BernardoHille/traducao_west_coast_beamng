"""Mod tree validation: exact names and virtual paths, no stray/temporary files, valid mod_info."""
import collections
import json
import os
import re

from common import FAIL, PASS, REPO, SKIP, WARN, Report, load_config, rel, sha256, texture_stem

MOD_NAME = "traducao_ptbr_wcusa"
MOD_DIR = os.path.join(REPO, "mod", MOD_NAME)
FORBIDDEN_NAME = re.compile(r"(_ptbr|_poc|_old|_backup|_copy|_tmp|~$|\.bak$|\.tmp$|\.orig$)", re.I)
JUNK = {"thumbs.db", "desktop.ini", ".ds_store", ".gitkeep"}
LAYERED = (".psd", ".xcf", ".kra", ".ora", ".blend", ".blend1")
MOD_INFO_FIELDS = ("name", "author", "version", "description")


def expected_paths():
    """Virtual path (lower-case) -> (family, role) for every known map, incl. extra paths."""
    out = {}
    for fam_name, fam in load_config("texture_families.json")["families"].items():
        for role, m in fam["maps"].items():
            paths = [m["path"]] + fam.get("extra_paths", {}).get(role, [])
            for p in paths:
                out[f"{p}/{m['file']}".lower()] = (fam_name, role)
    return out


def validate_mod_tree(mod_dir=MOD_DIR, installed_dir=None, report=None):
    rep = report or Report("Mod tree validation", rel(mod_dir))
    if not os.path.isdir(mod_dir):
        rep.add(FAIL, "Mod directory", f"not found: {mod_dir}")
        return rep
    known = expected_paths()
    from validate_new_assets import declared_paths
    import fnmatch
    declared, functional = declared_paths()
    files = []
    for root, dirs, names in os.walk(mod_dir):
        for n in names:
            files.append(os.path.relpath(os.path.join(root, n), mod_dir).replace("\\", "/"))

    info_path = f"mod_info/{os.path.basename(mod_dir)}/info.json"
    if info_path in files:
        try:
            with open(os.path.join(mod_dir, info_path), encoding="utf-8") as f:
                info = json.load(f)
            missing = [k for k in MOD_INFO_FIELDS if not info.get(k)]
            rep.add(FAIL if missing else PASS, "mod_info", f"missing fields: {missing}" if missing else f"{info['name']} {info['version']}")
        except (OSError, json.JSONDecodeError) as e:
            rep.add(FAIL, "mod_info", f"invalid JSON: {e}")
    else:
        rep.add(FAIL, "mod_info", f"{info_path} not found")

    lower = collections.Counter(f.lower() for f in files)
    dup_case = [f for f, n in lower.items() if n > 1]
    rep.add(FAIL if dup_case else PASS, "Case-insensitive duplicates", ", ".join(dup_case) if dup_case else "none")
    by_name = collections.defaultdict(list)
    for f in files:
        by_name[os.path.basename(f).lower()].append(f)

    n_assets = 0
    for f in sorted(files):
        base = os.path.basename(f)
        if f == info_path:
            continue
        if base.lower() in JUNK or f.lower().endswith(LAYERED):
            rep.add(FAIL, "Stray file", f"{f} must not be shipped in the mod")
            continue
        if FORBIDDEN_NAME.search(os.path.splitext(base)[0]) or FORBIDDEN_NAME.search(base):
            rep.add(FAIL, "File name", f"{f}: forbidden suffix (e.g. _ptbr/_poc/backup). Use the exact game name: {texture_stem(base)}{os.path.splitext(base)[1]}")
            continue
        ext = os.path.splitext(base)[1].lower()
        if f.lower() in declared:
            n_assets += ext in (".dds", ".png")
            rep.add(PASS, "Declared new asset", f"{f} (config/new_assets.json; checked by validate.py new)")
            continue
        if any(fnmatch.fnmatch(f, pat) for pat in functional):
            rep.add(PASS, "Declared functional override", f"{f} (speedLimit-only override; checked by validate.py new)")
            continue
        if ext in (".dds", ".png"):
            n_assets += 1
            key = f.lower()
            if key in known:
                fam, role = known[key]
                rep.add(PASS, "Asset path", f"{f} → {fam}/{role}")
                if ext == ".png":
                    rep.add(WARN, "Asset format", f"{f}: PNG in the mod; project rule is DDS in the original format")
            else:
                hint = [p for p in known if p.endswith("/" + base.lower())]
                rep.add(FAIL, "Asset path", f"{f} is not a known virtual path" + (f" (expected {hint[0]})" if hint else ""))
        elif ext in (".json", ".dae", ".cdae", ".lua"):
            rep.add(WARN, "Non-texture file", f"{f}: allowed only for planned functional work (materials, meshes, level data) — review")
        else:
            rep.add(FAIL, "Unexpected file", f)
    if n_assets == 0:
        rep.add(SKIP, "Asset path", "no texture assets in the mod")
    dup_names = {n: p for n, p in by_name.items() if len(p) > 1 and n.endswith((".dds", ".png"))}
    for n, p in dup_names.items():
        fams = {known.get(x.lower(), ("?",))[0] for x in p}
        rep.add(WARN if len(fams) == 1 and "?" not in fams else FAIL, "Duplicate file name", f"{n} at {p}")

    if installed_dir:
        if not os.path.isdir(installed_dir):
            rep.add(SKIP, "Installed copy", f"not installed at {installed_dir}")
        else:
            diffs = []
            for f in files:
                a, b = os.path.join(mod_dir, f), os.path.join(installed_dir, f)
                if not os.path.exists(b) or sha256(a) != sha256(b):
                    diffs.append(f)
            extra = []
            for root, _, names in os.walk(installed_dir):
                for n in names:
                    r = os.path.relpath(os.path.join(root, n), installed_dir).replace("\\", "/")
                    if r not in files:
                        extra.append(r)
            if diffs or extra:
                rep.add(WARN, "Installed copy", f"differs from repo: changed/missing {diffs}, extra {extra}")
            else:
                rep.add(PASS, "Installed copy", f"identical to repo ({len(files)} files)")
    return rep
