"""Convert QA PNG captures under tests/screenshots/<dir> to JPEG q92 (Phase 5 convention) and fix run reports.

    python tools/beamng/shots_to_jpeg.py phase6
"""
import json
import sys
from pathlib import Path
from PIL import Image
REPO = Path(__file__).resolve().parents[2]
sub = sys.argv[1]
n = 0
for p in (REPO / "tests/screenshots" / sub).rglob("*.png"):
    Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=92)
    p.unlink()
    n += 1
for r in (REPO / "tests/reports" / sub / "runs").glob("*.json"):
    t = r.read_text(encoding="utf8")
    t2 = t.replace(".png\"", ".jpg\"")
    if t2 != t:
        r.write_text(t2, encoding="utf8")
print(f"{n} PNG -> JPEG")
