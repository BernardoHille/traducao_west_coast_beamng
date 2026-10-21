"""Unit tests for the release packaging (tools/release/build_release.py). Synthetic data only."""
import datetime as dt
import hashlib
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "release"))
import build_release as B  # noqa: E402


class TestForbidden(unittest.TestCase):
    def test_runtime_files_pass(self):
        for f in ("assets/materials/signage/roadsigns/t_roadsigns_b.color.dds",
                  "levels/west_coast_usa/art/shapes/roads/roadsigns.cdae",
                  "levels/west_coast_usa/main/MissionGroup/items.level.json",
                  "mod_info/traducao_ptbr_wcusa/info.json"):
            self.assertIsNone(B.forbidden_reason(f), f)

    def test_dev_files_fail(self):
        for f in ("a/b/master.psd", "a/b/x.xcf", "a/t_roadsigns_b.color_ptbr.dds", "a/t_poc.dds", "a/x.bak", "a/x.tmp",
                  "a/Thumbs.db", "a/desktop.ini", ".env", "a/.env.local", "a/__pycache__/x.json", ".git/config",
                  "a/temp/x.cdae", "a/cache/x.dds", "a/_archive/info.json", "a/shot.png", "a/tool.py", "a/r19.svg", "a/x.log"):
            self.assertIsNotNone(B.forbidden_reason(f), f)


class TestZip(unittest.TestCase):
    def _build(self, root, out):
        files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
        B.write_zip(root, files, out, dt.datetime(2026, 10, 21))
        return files

    def test_deterministic_and_cdae_newer(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            root = t / "s"
            for rel, data in (("b/shape.dae", b"<dae/>"), ("b/shape.cdae", b"\x00\x01"), ("a/x.json", b"{}")):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_bytes(data)
            files = self._build(root, t / "1.zip")
            os.utime(root / "a/x.json", (1, 1))      # file-system times must not leak into the ZIP
            self._build(root, t / "2.zip")
            h = [hashlib.sha256((t / n).read_bytes()).hexdigest() for n in ("1.zip", "2.zip")]
            self.assertEqual(h[0], h[1])
            with zipfile.ZipFile(t / "1.zip") as zf:
                self.assertEqual(zf.namelist(), files)       # sorted entries, no directory entries
                stamp = {i.filename: i.date_time for i in zf.infolist()}
            self.assertGreater(stamp["b/shape.cdae"], stamp["b/shape.dae"])
            self.assertEqual(stamp["a/x.json"], stamp["b/shape.dae"])


class TestTextAudit(unittest.TestCase):
    def test_patterns(self):
        bad = ["C:\\Users\\someone\\x.png", "file:///D:/art/x.png", "/home/user/x", "me@example.com", "\"token\": \"abc\""]
        good = ["levels/west_coast_usa/art/shapes/x.dae", "\"speedLimit\": 16.6667", "Bernardo Hille"]
        hit = lambda s: any(rx.search(s) for rx, _ in B.TEXT_PATTERNS)
        for s in bad:
            self.assertTrue(hit(s), s)
        for s in good:
            self.assertFalse(hit(s), s)


if __name__ == "__main__":
    unittest.main()
