"""Ship the rewritten glyph-sign meshes with their engine-compiled .cdae (Phase 6).

    python tools/production/glyph_sync.py dae    # working/glyph_meshes -> mod (only files whose content changed)
    python tools/production/glyph_sync.py cdae   # after the game loaded the level with the mod: copy the .cdae it
                                                 # compiled (user temp) next to each .dae of the mod; shapes not
                                                 # loaded with the level are compiled by spawning a TSStatic (MCP)

Without the .cdae the game compiles the .dae into the user temp cache, which outlives the mod (Phase 5 finding)."""
import filecmp
import json
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "working/glyph_meshes"
MOD = REPO / "mod/traducao_ptbr_wcusa"
INST = Path(r"C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/mods/unpacked/traducao_ptbr_wcusa")
TEMP = Path(r"C:/Users/Desktop/AppData/Local/BeamNG/BeamNG.drive/current/temp")


def sync_dae(force=False):
    n = 0
    for f in SRC.rglob("*.dae"):
        dst = MOD / f.relative_to(SRC)
        if dst.exists() and filecmp.cmp(f, dst, shallow=False) and not force:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, dst)
        stale = dst.with_suffix(".cdae")  # compiled from the previous .dae: install_mod.py would re-stamp it as fresh
        if stale.exists():
            stale.unlink()
        n += 1
        print("dae", dst.relative_to(MOD))
    print(n, "changed")


def sync_cdae():
    sys.path.insert(0, str(REPO / "tools/beamng"))
    m = None
    for f in SRC.rglob("*.dae"):
        rel = f.relative_to(SRC)
        dae, cd_mod, cd_tmp, inst = MOD / rel, MOD / rel.with_suffix(".cdae"), TEMP / rel.with_suffix(".cdae"), INST / rel
        if cd_mod.exists() and cd_mod.stat().st_mtime > dae.stat().st_mtime:
            continue
        if not (inst.exists() and filecmp.cmp(inst, dae, shallow=False)):
            raise SystemExit(f"{rel}: installed copy differs from the mod - run install_mod.py and reload the level first")
        if not cd_tmp.exists() or cd_tmp.stat().st_mtime < inst.stat().st_mtime:
            if m is None:
                from mcp_client import BeamNGMCP
                m = BeamNGMCP()
            shape = "/" + rel.as_posix()
            m.lua(f"local o = createObject('TSStatic') o.shapeName = {json.dumps(shape)} o:setPosition(vec3(0, 0, -500)) "
                  "o:registerObject('ptbr_tmp_compile') o:delete() return 1")
            time.sleep(1)
        if not cd_tmp.exists() or cd_tmp.stat().st_mtime < inst.stat().st_mtime:
            raise SystemExit(f"{rel}: the game did not compile a fresh .cdae")
        shutil.copy(cd_tmp, cd_mod)  # new mtime: newer than the .dae
        print("cdae", cd_mod.relative_to(MOD))


if __name__ == "__main__":
    {"dae": sync_dae, "dae-force": lambda: sync_dae(True), "cdae": sync_cdae}[sys.argv[1]]()
