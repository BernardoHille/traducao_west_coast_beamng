"""Shared primitives: results, reports, configuration, manifest lookup."""
import csv
import datetime as dt
import hashlib
import json
import os
from dataclasses import dataclass, field, asdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CONFIG = os.path.join(HERE, "config")
REPORT_DIR = os.path.join(REPO, "export", "reports", "validation")
IMAGE_DIR = os.path.join(REPORT_DIR, "images")
MANIFEST = os.path.join(REPO, "docs", "inventory", "original_files_manifest.csv")

PASS, WARN, FAIL, SKIP = "PASS", "WARN", "FAIL", "SKIP"
_RANK = {PASS: 0, SKIP: 0, WARN: 1, FAIL: 2}


class ToolError(Exception):
    """Internal error of the validator (exit code 2), never a validation verdict."""


@dataclass
class Check:
    status: str
    name: str
    message: str
    details: dict = field(default_factory=dict)

    def line(self):
        return f"[{self.status}] {self.name}: {self.message}"


@dataclass
class Report:
    title: str
    subject: str = ""
    checks: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    def add(self, status, name, message, **details):
        c = Check(status, name, message, details)
        self.checks.append(c)
        return c

    def extend(self, other):
        self.checks.extend(other.checks)

    @property
    def status(self):
        if not self.checks:
            return SKIP
        worst = max(self.checks, key=lambda c: _RANK[c.status]).status
        if worst == PASS and all(c.status == SKIP for c in self.checks):
            return SKIP
        return worst

    def counts(self):
        out = {PASS: 0, WARN: 0, FAIL: 0, SKIP: 0}
        for c in self.checks:
            out[c.status] += 1
        return out

    def print(self):
        print(f"== {self.title}" + (f" — {self.subject}" if self.subject else ""))
        for c in self.checks:
            print("  " + c.line())
        print(f"  => {self.status} {self.counts()}")

    def to_dict(self):
        return {"title": self.title, "subject": self.subject, "status": self.status, "counts": self.counts(),
                "generated": dt.datetime.now().isoformat(timespec="seconds"),
                "meta": {k: v for k, v in self.meta.items() if k != "_appendix_md"},
                "checks": [asdict(c) for c in self.checks]}

    def to_markdown(self):
        lines = [f"# {self.title}", ""]
        if self.subject:
            lines += [f"**Alvo:** `{self.subject}`  ", ""]
        lines += [f"**Resultado:** `{self.status}` · " + " · ".join(f"{k} {v}" for k, v in self.counts().items()), ""]
        shown = {k: v for k, v in self.meta.items() if not k.startswith("_") and k != "metrics"}
        for k, v in shown.items():
            lines.append(f"- {k}: `{v}`")
        if shown:
            lines.append("")
        lines += ["| Status | Verificação | Mensagem |", "|---|---|---|"]
        for c in self.checks:
            lines.append(f"| {c.status} | {c.name} | {c.message.replace('|', '/')} |")
        if self.meta.get("_appendix_md"):
            lines += ["", self.meta["_appendix_md"]]
        return "\n".join(lines) + "\n"

    def save(self, stem, directory=REPORT_DIR):
        os.makedirs(directory, exist_ok=True)
        base = os.path.join(directory, stem)
        with open(base + ".json", "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
        with open(base + ".md", "w", encoding="utf-8", newline="\n") as f:
            f.write(self.to_markdown())
        return base


def load_config(name):
    path = os.path.join(CONFIG, name)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise ToolError(f"cannot load config {name}: {e}")


def thresholds():
    return {k: v["value"] for k, v in load_config("thresholds.json").items() if not k.startswith("_")}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def texture_stem(path):
    """'…/t_roadsigns_b.color_ptbr.png' -> 't_roadsigns_b.color'."""
    name = os.path.basename(path)
    for ext in (".png", ".dds", ".PNG", ".DDS"):
        if name.endswith(ext):
            name = name[: -len(ext)]
    for suffix in ("_ptbr", "_poc"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def find_original(stem, kind):
    """Return (absolute path, manifest row) of the original DDS/PNG copy in source/originals."""
    cls = {"dds": "original_dds", "png": "original_png"}[kind]
    for row in manifest():
        if row["classification"] == cls and texture_stem(row["filename"]).lower() == stem.lower():
            return os.path.join(REPO, row["copied_to"]), row
    return None, None


def check_original_integrity(report, path, row):
    """SHA-256 of the local original must match the Phase 0 manifest."""
    if not path or not os.path.exists(path):
        report.add(FAIL, "Original integrity", f"original not found locally ({path})")
        return False
    actual = sha256(path)
    if actual != row["sha256"]:
        report.add(FAIL, "Original integrity", f"SHA-256 mismatch for {row['copied_to']} (manifest {row['sha256'][:12]}…, file {actual[:12]}…)")
        return False
    report.add(PASS, "Original integrity", f"SHA-256 matches manifest ({actual[:12]}…)")
    return True


def rel(path):
    try:
        return os.path.relpath(path, REPO).replace("\\", "/")
    except ValueError:
        return path
