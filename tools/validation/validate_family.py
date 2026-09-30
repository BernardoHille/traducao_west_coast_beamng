"""Family validation: which maps of a texture family are delivered, and whether a shape change
brought the auxiliary maps it requires (opacity / emissive / normal / AO …)."""
import os

from common import FAIL, PASS, REPO, SKIP, WARN, Report, load_config, texture_stem

MOD_DIR = os.path.join(REPO, "mod", "traducao_ptbr_wcusa")
REFERENCE_DIR = os.path.join(REPO, "source", "reference_ptbr")


def families():
    return load_config("texture_families.json")["families"]


def family_of(stem):
    for name, fam in families().items():
        for role, m in fam["maps"].items():
            if texture_stem(m["file"]).lower() == stem.lower():
                return name, role
    return None, None


def delivered_from_dir(directory):
    """Map texture stem -> file path for every DDS/PNG under a directory tree."""
    out = {}
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith((".dds", ".png")):
                out.setdefault(texture_stem(f).lower(), os.path.join(root, f))
    return out


def modification(name, source):
    mods = load_config("modifications.json")
    return mods.get(source, {}).get(name, {})


def validate_family(name, source="mod", directory=None, shape_changed=None, report=None):
    fams = families()
    rep = report or Report("Family validation", f"{name} ({source})")
    if name not in fams:
        rep.add(FAIL, "Family", f"unknown family '{name}' (see config/texture_families.json)")
        return rep
    fam = fams[name]
    directory = directory or {"mod": MOD_DIR, "reference": REFERENCE_DIR}.get(source)
    if not directory or not os.path.isdir(directory):
        rep.add(FAIL, "Source", f"directory not found for source '{source}'")
        return rep
    delivered = delivered_from_dir(directory)
    present = {role: delivered.get(texture_stem(m["file"]).lower()) for role, m in fam["maps"].items()}
    present = {r: p for r, p in present.items() if p}
    rep.meta.update(scope=fam["scope"], wcusa_usage=fam["wcusa_usage"], delivered={r: os.path.relpath(p, REPO).replace("\\", "/") for r, p in present.items()})
    if not present:
        rep.add(SKIP, "Delivered maps", "no map of this family in the source")
        return rep

    for role, m in fam["maps"].items():
        label = f"{role} ({m['file']})"
        if role in present:
            rep.add(PASS, label, "delivered")
        elif m["required"]:
            rep.add(FAIL, label, "required map missing from the package")
        else:
            rep.add(PASS, label, "not delivered — original stays in use")

    decl = modification(name, source)
    if shape_changed is None:
        shape_changed = decl.get("shape_changed")
    req = fam.get("requires_on_shape_change", [])
    if shape_changed is None:
        rep.add(WARN, "shape_changed", "modification does not declare shape_changed (config/modifications.json); auxiliary-map rule not evaluated")
    elif shape_changed:
        missing = [r for r in req if r not in present]
        if not req:
            rep.add(PASS, "shape_changed", "declared true; family has no shape-dependent auxiliary map")
        elif missing:
            rep.add(FAIL, "shape_changed", "shape changed but these maps were not updated: " + ", ".join(f"{r} ({fam['maps'][r]['file']})" for r in missing))
        else:
            rep.add(PASS, "shape_changed", "all shape-dependent maps delivered: " + ", ".join(req))
    else:
        rep.add(PASS, "shape_changed", "declared false (only colours/text inside the original silhouette)")
    if fam.get("notes"):
        rep.meta["notes"] = fam["notes"]
    return rep
