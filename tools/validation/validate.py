"""Asset validation pipeline — single entry point.

  python tools/validation/validate.py texture <png> [--original <png>] [--no-heatmap]
  python tools/validation/validate.py dds <dds> [--original <dds>]
  python tools/validation/validate.py family <family> [--source mod|reference] [--dir DIR] [--shape-changed true|false]
  python tools/validation/validate.py mod [--installed]
  python tools/validation/validate.py speeds [--refresh]
  python tools/validation/validate.py selftest           # originals vs themselves + PoC DDS metadata
  python tools/validation/validate.py regression         # legacy PT-BR images must be caught
  python tools/validation/validate.py all [--refresh]

Statuses: PASS / WARN / FAIL / SKIP. Exit code: 0 = no FAIL, 1 = at least one FAIL, 2 = internal tool error.
Reports: export/reports/validation/<name>.md + .json (heatmaps in images/).
"""
import argparse
import glob
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import FAIL, PASS, REPO, SKIP, WARN, Report, ToolError, load_config, manifest, rel  # noqa: E402
from validate_dds import validate_dds  # noqa: E402
from validate_family import validate_family  # noqa: E402
from validate_mod_tree import MOD_DIR, validate_mod_tree  # noqa: E402
from validate_speed_consistency import validate_speeds  # noqa: E402
from validate_texture import validate_png  # noqa: E402

INSTALLED = "C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/mods/unpacked/traducao_ptbr_wcusa"


def _abs(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def _finish(rep, stem, quiet=False):
    if not quiet:
        rep.print()
    base = rep.save(stem)
    if not quiet:
        print(f"  report: {rel(base)}.md / .json")
    return rep


def cmd_texture(a):
    return _finish(validate_png(_abs(a.file), _abs(a.original) if a.original else None, heatmap=not a.no_heatmap), os.path.basename(a.file))


def cmd_dds(a):
    return _finish(validate_dds(_abs(a.file), _abs(a.original) if a.original else None), os.path.basename(a.file))


def cmd_family(a):
    sc = None if a.shape_changed is None else a.shape_changed == "true"
    return _finish(validate_family(a.family, a.source, _abs(a.dir) if a.dir else None, sc), f"family_{a.family}_{a.source}")


def mod_report(installed=True):
    rep = validate_mod_tree(MOD_DIR, INSTALLED if installed else None)
    fam_rep = Report("Mod families")
    delivered = set()
    for root, _, files in os.walk(MOD_DIR):
        for f in files:
            delivered.add(f.lower())
    for name, fam in load_config("texture_families.json")["families"].items():
        if any(m["file"].lower() in delivered for m in fam["maps"].values()):
            r = validate_family(name, "mod")
            for c in r.checks:
                fam_rep.add(c.status, f"{name}: {c.name}", c.message)
    rep.extend(fam_rep)
    return rep


def cmd_mod(a):
    return _finish(mod_report(a.installed), "mod_tree")


def cmd_speeds(a):
    return _finish(validate_speeds(refresh=a.refresh), "speed_consistency")


def selftest(quiet=False):
    rep = Report("Self-test: originals vs themselves + PoC DDS")
    for row in manifest():
        path = os.path.join(REPO, row["copied_to"])
        if row["classification"] == "original_dds":
            r = validate_dds(path, path)
        elif row["classification"] == "original_png":
            r = validate_png(path, path, heatmap=False)
        else:
            continue
        st = r.status
        bad = [c for c in r.checks if c.status in (FAIL, WARN)]
        rep.add(PASS if st in (PASS, SKIP) else FAIL, f"original {row['filename']}",
                "identical to itself" if not bad else "; ".join(c.line() for c in bad))
    for poc in ("export/dds/poc/t_roadsigns_b.color.dds", "mod/traducao_ptbr_wcusa/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds"):
        r = validate_dds(_abs(poc))
        bad = [c for c in r.checks if c.status in (FAIL, WARN)]
        rep.add(PASS if not bad else FAIL, f"PoC DDS metadata {poc}",
                "; ".join(f"{c.name}: {c.message}" for c in r.checks if c.name in ("Resolution", "DDS format", "Colour space", "Mipmaps", "DX10 alpha mode"))
                if not bad else "; ".join(c.line() for c in bad))
    return _finish(rep, "selftest", quiet)


def regression(quiet=False):
    rep = Report("Regression: legacy PT-BR images (negative dataset)")
    rows = []
    for case in load_config("regression_expectations.json")["cases"]:
        if case["kind"] == "texture":
            r = validate_png(_abs(case["file"]))
            _finish(r, "regression_" + case["id"], quiet=True)
        else:
            r = validate_family(case["family"], case["source"])
            _finish(r, "regression_" + case["id"], quiet=True)
        failed = {c.name for c in r.checks if c.status == FAIL}
        missing = [n for n in case["expect_fail"] if n not in failed]
        want = case.get("expect_status")
        ok = not missing and (want is None or r.status == want)
        detail = f"got {r.status}; FAIL checks: {sorted(failed) or 'none'}"
        rep.add(PASS if ok else FAIL, f"{case['id']}", ("detected as expected — " if ok else f"NOT detected: {missing} — ") + detail)
        rows.append({"case": case["id"], "expected": case["expect_fail"] or want, "obtained": r.status, "fail_checks": sorted(failed), "ok": ok})
    rep.meta["cases"] = rows
    return _finish(rep, "regression", quiet)


def cmd_all(a):
    summary = Report("Validation — full run")
    parts = [("Texture infrastructure (self-test)", selftest(quiet=True)),
             ("Regression (legacy images caught)", regression(quiet=True)),
             ("Mod tree + families", mod_report(True)),
             ("Current map speed consistency", validate_speeds(refresh=a.refresh))]
    _finish(parts[2][1], "mod_tree", quiet=True)
    _finish(parts[3][1], "speed_consistency", quiet=True)
    for label, r in parts:
        c = r.counts()
        summary.add(r.status, label, f"PASS {c['PASS']} · WARN {c['WARN']} · FAIL {c['FAIL']} · SKIP {c['SKIP']}")
    summary.print()
    for label, r in parts:
        for c in r.checks:
            if c.status == FAIL:
                print(f"    {label}: {c.line()}")
    summary.save("summary")
    return summary


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="validate.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("texture", help="PNG vs original: resolution, alpha, pixel diff, allowed regions, heatmaps")
    p.add_argument("file"); p.add_argument("--original"); p.add_argument("--no-heatmap", action="store_true")
    p = sp.add_parser("dds", help="DDS header vs original: format, sRGB/linear, mipmaps, size")
    p.add_argument("file"); p.add_argument("--original")
    p = sp.add_parser("family", help="maps delivered for a family + shape_changed rule")
    p.add_argument("family"); p.add_argument("--source", default="mod", choices=["mod", "reference", "dir"])
    p.add_argument("--dir"); p.add_argument("--shape-changed", choices=["true", "false"])
    p = sp.add_parser("mod", help="mod tree: names, virtual paths, stray files, mod_info, families")
    p.add_argument("--installed", action="store_true", help="also compare with the copy in the BeamNG user folder")
    p = sp.add_parser("speeds", help="sign == road == radar == zone == ADAS (limit alert)")
    p.add_argument("--refresh", action="store_true", help="collect a new navgraph snapshot via MCP (map must be loaded)")
    sp.add_parser("selftest", help="originals vs themselves + PoC DDS metadata (must PASS)")
    sp.add_parser("regression", help="legacy PT-BR images (must be caught)")
    p = sp.add_parser("all", help="selftest + regression + mod + speeds + summary")
    p.add_argument("--refresh", action="store_true")
    a = ap.parse_args(argv)
    try:
        rep = {"texture": cmd_texture, "dds": cmd_dds, "family": cmd_family, "mod": cmd_mod, "speeds": cmd_speeds,
               "selftest": lambda _: selftest(), "regression": lambda _: regression(), "all": cmd_all}[a.cmd](a)
    except ToolError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 2
    except Exception:
        traceback.print_exc()
        return 2
    return 1 if rep.status == FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
