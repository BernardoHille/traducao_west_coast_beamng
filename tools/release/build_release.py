"""Build the public release ZIP of the mod from mod/traducao_ptbr_wcusa, reproducibly.

    python tools/release/build_release.py                 # release build (refuses a dirty Git tree)
    python tools/release/build_release.py --allow-dirty   # local test build (marked as such in the output)

Steps (any failure stops the build, exit code 1):
  1. Git state: HEAD commit; the working tree must be clean for a release build.
  2. Mod tree: tools/validation mod-tree check without FAIL.
  3. Generated level overrides (not versioned, rebuilt from the game install) must match the versioned
     decisions: apply_phase7_functional.py --check and decal_overrides.py --check.
  4. File selection: every file of the mod tree; only runtime extensions are allowed, and forbidden names
     (PSD/XCF, backups, _ptbr/_poc, caches, logs, Thumbs.db, .git, .env, __pycache__ ...) fail the build.
  5. No unneeded originals: each file is compared with the game's own file at the same virtual path
     (content zips and loose gameplay/ of the install); a byte-identical copy fails the build.
  6. Text audit of every text file: no local absolute paths, user names, e-mail addresses or secrets.
  7. Clean staging (release/staging/<name>/), deterministic ZIP (sorted entries, fixed timestamps from
     tools/release/release_config.json, fixed permissions; each .cdae stamped later than its .dae so the
     game uses the shipped compiled mesh instead of recompiling it into the user cache).
  8. SHA-256 of the ZIP (<name>.sha256), manifest with path / size / SHA-256 of every file.
  9. The ZIP is extracted into a brand-new temporary folder and compared with the staging and with the
     mod tree: same files, same hashes, nothing extra.

The ZIP content does not depend on the commit or on the build time, so building again from any commit with
the same mod tree gives the same bytes (same SHA-256), which is how the tagged commit is checked.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).resolve().with_name("release_config.json")
MOD_NAME = "traducao_ptbr_wcusa"
MOD_DIR = REPO / "mod" / MOD_NAME
INFO = MOD_DIR / "mod_info" / MOD_NAME / "info.json"
STAGING_ROOT = REPO / "release" / "staging"
OUTPUT = REPO / "release" / "output"

RUNTIME_EXT = {".dds", ".dae", ".cdae", ".json"}
TEXT_EXT = {".json", ".dae"}
FORBIDDEN = [
    "*.psd", "*.xcf", "*.kra", "*.ora", "*.blend", "*.blend1", "*.blend~", "*.bak", "*.tmp", "*.orig", "*~",
    "*.log", "*.pyc", "*.py", "*.lua.pre_*", "*.svg", "*.png", "*.jpg", "*.exe", "*.zip",
    "thumbs.db", "desktop.ini", ".ds_store", ".gitkeep", ".env", ".env.*",
    "*_ptbr.*", "*_poc.*", "*_old.*", "*_backup.*", "*_copy.*", "*_tmp.*",
]
FORBIDDEN_DIRS = {".git", "__pycache__", "cache", "temp", "_archive", "screenshots", "originals", "reference_ptbr"}
TEXT_PATTERNS = [
    (re.compile(r"[A-Za-z]:[\\/]{1,2}(?:Users|Program Files|Documents)", re.I), "absolute Windows path"),
    (re.compile(r"file:///", re.I), "file URL"),
    (re.compile(r"[\\/](?:Users|home)[\\/][^\\/\s\"<]+", re.I), "user folder path"),
    (re.compile(r"\bDesktop[\\/]", re.I), "Desktop folder path"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "e-mail address"),
    (re.compile(r"(?:api[_-]?key|secret|passw(?:or)?d|token)\s*[\"']?\s*[:=]", re.I), "credential-like field"),
    (re.compile(r"\b(?:ghp|gho|github_pat|sk|xox[abp])_[A-Za-z0-9_]{16,}"), "token-like string"),
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class BuildError(Exception):
    pass


def git(*args) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout.strip()


def step(msg):
    print(f"== {msg}", flush=True)


def check_git(allow_dirty):
    head = git("rev-parse", "HEAD")
    # the build's own output folder does not count: the previous build's records are written there before they are committed
    dirty = git("status", "--porcelain", "--", ".", ":(exclude)release/output")
    if dirty and not allow_dirty:
        raise BuildError("working tree is not clean (commit first, or --allow-dirty for a test build):\n" + dirty)
    print(f"   HEAD {head}{' (dirty tree: TEST BUILD)' if dirty else ''}")
    return head, bool(dirty)


def check_tree():
    sys.path.insert(0, str(REPO / "tools" / "validation"))
    from validate_mod_tree import validate_mod_tree
    rep = validate_mod_tree(str(MOD_DIR))
    fails = [c.line() for c in rep.checks if c.status == "FAIL"]
    if fails:
        raise BuildError("mod tree validation failed:\n" + "\n".join(fails))
    print(f"   mod tree: {len(rep.checks)} checks, 0 FAIL")


def check_generated():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for cmd in (["tools/production/apply_phase7_functional.py", "--check"], ["tools/production/decal_overrides.py", "--check"]):
        r = subprocess.run([sys.executable, *cmd], cwd=REPO, capture_output=True, text=True, env=env, encoding="utf-8")
        last = (r.stdout.strip().splitlines() or [""])[-1]
        if r.returncode != 0:
            raise BuildError(f"{' '.join(cmd)} failed:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        print(f"   {cmd[0]} --check: {last}")


def forbidden_reason(rel: str):
    parts = rel.lower().split("/")
    bad_dir = FORBIDDEN_DIRS.intersection(parts[:-1])
    if bad_dir:
        return f"forbidden folder {sorted(bad_dir)}"
    name = parts[-1]
    for pat in FORBIDDEN:
        if fnmatch.fnmatch(name, pat):
            return f"forbidden name ({pat})"
    if os.path.splitext(name)[1] not in RUNTIME_EXT:
        return "not a runtime file type"
    return None


def collect():
    files = sorted(p.relative_to(MOD_DIR).as_posix() for p in MOD_DIR.rglob("*") if p.is_file())
    bad = [(f, r) for f in files if (r := forbidden_reason(f))]
    if bad:
        raise BuildError("forbidden files in the mod tree:\n" + "\n".join(f"  {f}: {r}" for f, r in bad))
    return files


def game_index(game: Path, wanted: set[str]):
    """lower-case virtual path -> (container, member) for the wanted paths, from the game install."""
    found = {}
    gp = game / "gameplay"
    for w in wanted:
        if w.startswith("gameplay/"):
            p = game / w
            if p.is_file():
                found[w] = (None, p)
    zips = [z for z in sorted((game / "content").rglob("*.zip")) if "vehicles" not in z.relative_to(game / "content").parts]
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            for n in zf.namelist():
                k = n.lower()
                if k in wanted and k not in found:
                    found[k] = (z, n)
    return found


def check_originals(files, game: Path):
    wanted = {f.lower() for f in files if not f.startswith("mod_info/")}
    idx = game_index(game, wanted)
    identical, modified, new = [], [], []
    for f in files:
        if f.startswith("mod_info/"):
            continue
        hit = idx.get(f.lower())
        if hit is None:
            new.append(f)
            continue
        z, member = hit
        if z is None:
            orig = sha256(member)
        else:
            with zipfile.ZipFile(z) as zf:
                orig = sha256_bytes(zf.read(member))
        (identical if orig == sha256(MOD_DIR / f) else modified).append(f)
    if identical:
        raise BuildError("byte-identical copies of game files (must not be shipped):\n" + "\n".join(f"  {f}" for f in identical))
    print(f"   {len(modified)} files override a game file (all modified), {len(new)} new files, 0 identical copies")
    return {"modified": modified, "new": new}


def check_text(files):
    hits = []
    for f in files:
        if os.path.splitext(f)[1].lower() not in TEXT_EXT:
            continue
        t = (MOD_DIR / f).read_text(encoding="utf-8", errors="replace")
        for rx, what in TEXT_PATTERNS:
            m = rx.search(t)
            if m:
                hits.append(f"  {f}: {what}: {m.group(0)[:60]!r}")
    if hits:
        raise BuildError("text audit failed:\n" + "\n".join(hits))
    print(f"   text audit: {sum(os.path.splitext(f)[1].lower() in TEXT_EXT for f in files)} text files, nothing found")


def stage(files, name):
    root = STAGING_ROOT / name
    if root.exists():
        if root.resolve().parent != STAGING_ROOT.resolve():
            raise BuildError(f"refusing to clear unexpected staging path {root}")
        shutil.rmtree(root)
    for f in files:
        t = root / f
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(MOD_DIR / f, t)
    return root


def write_zip(root: Path, files, zpath: Path, stamp: dt.datetime):
    base = stamp.timetuple()[:6]
    later = (stamp + dt.timedelta(minutes=2)).timetuple()[:6]
    tmp = zpath.with_suffix(".zip.part")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in files:  # already sorted
            zi = zipfile.ZipInfo(f, date_time=later if f.lower().endswith(".cdae") else base)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            zi.external_attr = 0
            zf.writestr(zi, (root / f).read_bytes(), compresslevel=9)
    os.replace(tmp, zpath)


def verify_zip(zpath: Path, root: Path, files):
    tmp = Path(tempfile.mkdtemp(prefix="wcusa_release_verify_"))
    try:
        with zipfile.ZipFile(zpath) as zf:
            bad = zf.testzip()
            if bad:
                raise BuildError(f"corrupt ZIP member {bad}")
            zf.extractall(tmp)
        got = sorted(p.relative_to(tmp).as_posix() for p in tmp.rglob("*") if p.is_file())
        if got != files:
            raise BuildError(f"extracted file set differs: extra {sorted(set(got) - set(files))}, missing {sorted(set(files) - set(got))}")
        diff = [f for f in files if not (sha256(tmp / f) == sha256(root / f) == sha256(MOD_DIR / f))]
        if diff:
            raise BuildError(f"extracted files differ from staging/mod tree: {diff}")
        print(f"   extracted into a new temporary folder: {len(got)} files, identical to staging and to the mod tree, nothing extra")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def kind(f):
    ext = os.path.splitext(f)[1].lower()
    if f.startswith("mod_info/"):
        return "metadata"
    if ext == ".json":
        return "materials" if f.endswith("materials.json") else "level/gameplay data"
    return {".dds": "textures (DDS)", ".dae": "meshes (DAE)", ".cdae": "compiled meshes (CDAE)"}[ext]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--allow-dirty", action="store_true", help="test build from a dirty tree (never a release)")
    ap.add_argument("--game", type=Path, default=None, help="BeamNG.drive install folder (default from release_config.json)")
    a = ap.parse_args(argv)
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    game = a.game or Path(cfg["game_install"])
    info = json.loads(INFO.read_text(encoding="utf-8"))
    version = info["version"]
    if version != cfg["version"]:
        raise BuildError(f"info.json version {version} != release_config.json version {cfg['version']}")
    name = f"{MOD_NAME}_v{version}"
    try:
        step("Git"); head, dirty = check_git(a.allow_dirty)
        step("Mod tree"); check_tree()
        step("Generated overrides"); check_generated()
        step("File selection"); files = collect(); print(f"   {len(files)} files, all runtime types, no forbidden names")
        step("Originals"); origin = check_originals(files, game)
        step("Text audit"); check_text(files)
        step("Staging"); root = stage(files, name); print(f"   {root.relative_to(REPO).as_posix()}")
        step("ZIP")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        zpath = OUTPUT / f"{name}.zip"
        write_zip(root, files, zpath, dt.datetime.fromisoformat(cfg["zip_timestamp"]))
        zsha = sha256(zpath)
        (OUTPUT / f"{name}.sha256").write_text(f"{zsha}  {zpath.name}\n", encoding="utf-8", newline="\n")
        rows = [(f, (root / f).stat().st_size, sha256(root / f)) for f in files]
        total = sum(r[1] for r in rows)
        counts = {}
        for f in files:
            counts[kind(f)] = counts.get(kind(f), 0) + 1
        lines = [
            f"# {cfg['title']} {version} - release manifest",
            f"# zip: {zpath.name}",
            f"# zip sha256: {zsha}",
            f"# zip size: {zpath.stat().st_size} bytes",
            f"# files: {len(files)}, uncompressed {total} bytes",
            f"# compatibility: {cfg['beamng_version']}",
            "# columns: sha256  size  path",
        ] + [f"{h}  {s:>10}  {f}" for f, s, h in rows]
        (OUTPUT / f"{name}_manifest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        step("Verify ZIP"); verify_zip(zpath, root, files)
        build = {
            "version": version, "commit": head, "dirty_tree": dirty, "zip": zpath.name, "zip_size": zpath.stat().st_size,
            "zip_sha256": zsha, "files": len(files), "uncompressed_size": total, "by_kind": counts,
            "overrides_game_file": len(origin["modified"]), "new_files": len(origin["new"]),
            "beamng_compatibility": cfg["beamng_version"], "built_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        }
        (OUTPUT / f"{name}_build.json").write_text(json.dumps(build, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    except BuildError as e:
        print(f"BUILD FAILED: {e}", file=sys.stderr)
        return 1
    print("== Result")
    for k, v in build.items():
        print(f"   {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
