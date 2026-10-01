"""Install (mirror) mod/traducao_ptbr_wcusa into the BeamNG user folder's mods/unpacked.

Only the mod's own folder is touched: files are copied when their SHA-256 differs and files that no
longer exist in the repo are removed from the installed copy. Nothing else in the user folder and
nothing in the game installation is modified.

    python tools/production/install_mod.py            # mirror
    python tools/production/install_mod.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "mod/traducao_ptbr_wcusa"
DST = Path(r"C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/mods/unpacked/traducao_ptbr_wcusa")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if DST.parent.name != "unpacked" or DST.name != SRC.name:
        raise SystemExit("refusing: unexpected destination")
    src = {p.relative_to(SRC).as_posix(): p for p in SRC.rglob("*") if p.is_file()}
    dst = {p.relative_to(DST).as_posix(): p for p in DST.rglob("*") if p.is_file()} if DST.exists() else {}
    copied, removed = [], []
    for rel, p in sorted(src.items()):
        t = DST / rel
        if rel not in dst or sha(p) != sha(t):
            copied.append(rel)
            if not a.dry_run:
                t.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, t)
    for rel, p in sorted(dst.items()):
        if rel not in src:
            removed.append(rel)
            if not a.dry_run:
                p.unlink()
    if not a.dry_run:
        # a compiled mesh must be newer than its .dae, or the game recompiles it into the user temp
        # cache, which survives the mod being disabled (see docs/production/PHASE5_ROADSIGNS.md)
        import os
        for root in (SRC, DST):
            for cd in root.rglob("*.cdae"):
                dae = cd.with_suffix(".dae")
                if dae.exists() and cd.stat().st_mtime <= dae.stat().st_mtime:
                    t = dae.stat().st_mtime + 60
                    os.utime(cd, (t, t))
        for d in sorted((d for d in DST.rglob("*") if d.is_dir()), key=lambda d: -len(d.parts)):
            if not any(d.iterdir()):
                d.rmdir()
    print(f"copied {len(copied)}: {copied}")
    print(f"removed {len(removed)}: {removed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
