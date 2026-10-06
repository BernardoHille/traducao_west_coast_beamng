"""One QA cycle of Phase 6: install -> verify installed copy -> original captures -> PT-BR captures -> JPEG.

    python tools/beamng/qa_cycle.py --families eca_genericsigns t_billboards [--states original ptbr]

For each state the level is reloaded once through smallgrid (qa_runner.ensure_state); every location of the
listed families is captured with the day preset, locations whose catalog entry lists "night" also at night,
and in the PT-BR state the Phase 5 sanity points (PARE, R-2, R-19 40) are captured too.
Refuses to run when the installed mod copy differs from the repository (stale QA).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
SANITY = ["roadsigns_chinatown_stop", "roadsigns_downtown_yield", "r19_40_hill"]


def run(args):
    r = subprocess.run([PY] + args, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    lines = [l for l in (r.stdout + r.stderr).splitlines() if any(k in l for k in ("VFS BAD", "run report", "Error", "Traceback", "FAIL"))]
    for l in lines:
        print("   ", l)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(f"failed: {' '.join(args)}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--families", nargs="+", required=True)
    ap.add_argument("--states", nargs="+", default=["original", "ptbr"])
    ap.add_argument("--no-sanity", action="store_true")
    a = ap.parse_args(argv)
    run(["tools/production/install_mod.py"])
    r = subprocess.run([PY, "tools/validation/validate.py", "mod", "--installed"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if "Installed copy: identical" not in r.stdout:
        raise SystemExit("installed mod copy differs from the repository - refusing to capture")
    sys.path.insert(0, str(REPO / "tools/beamng"))
    import qa_runner as q
    cat = q.catalog()
    for state in a.states:
        print(f"== {state}")
        first = True
        for fam in a.families:
            args = ["tools/beamng/qa_runner.py", "capture", "--family", fam, "--state", state, "--preset", "day", "--out-dir", "phase6"]
            if not first:
                args.append("--no-reload")
            run(args)
            first = False
        nights = [l["id"] for l in cat["locations"] if l["family"] in a.families and "night" in l.get("lighting", [])]
        for lid in nights:
            run(["tools/beamng/qa_runner.py", "capture", "--location", lid, "--state", state, "--preset", "night", "--out-dir", "phase6", "--no-reload"])
        if state != "original" and not a.no_sanity:
            for lid in SANITY:
                run(["tools/beamng/qa_runner.py", "capture", "--location", lid, "--state", state, "--preset", "day", "--out-dir", "phase6", "--no-reload"])
    run(["tools/beamng/shots_to_jpeg.py", "phase6"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
