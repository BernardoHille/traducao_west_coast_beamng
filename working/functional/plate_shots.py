"""Phase 7 QA: screenshot of every speed plate of roadsigns.dae (working/functional/speed_plates.json) from the front,
`dist` m along its face normal, slightly raised. Writes JPEGs + a contact sheet to <out_dir>.

    python working/functional/plate_shots.py tests/screenshots/phase7/speed_plates [dist] [state-label]
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP, wait_for_file  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

out = REPO / sys.argv[1]
dist = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
label = sys.argv[3] if len(sys.argv) > 3 else "ptbr"
out.mkdir(parents=True, exist_ok=True)
plates = json.loads((HERE / "speed_plates.json").read_text(encoding="utf8"))["plates"]
m = BeamNGMCP()
m.call("toggle_ui", show=False)
ims = []
for p in plates:
    c, n = p["center"], p["normal"]
    cam = [c[0] + n[0] * dist, c[1] + n[1] * dist, c[2] + 0.6]
    q = json.loads(m.lua(f"local q = quatFromDir((vec3({c[0]},{c[1]},{c[2]}) - vec3({cam[0]},{cam[1]},{cam[2]})):normalized(), vec3(0,0,1)) "
                         "return jsonEncode({q.x,q.y,q.z,q.w})"))
    m.call("set_free_camera", pos=dict(zip("xyz", cam)), rot=dict(zip("xyzw", q)), fov=40)
    time.sleep(1.3)
    src = m.call("screenshot").strip()
    wait_for_file(src)
    im = Image.open(src).convert("RGB")
    im.thumbnail((1280, 1280))
    im.save(out / f"{p['id']}_{label}.jpg", quality=88)
    t = im.copy()
    t.thumbnail((480, 480))
    ImageDraw.Draw(t).rectangle((0, 0, 300, 18), fill=(0, 0, 0))
    ImageDraw.Draw(t).text((4, 3), f"{p['id']} {p['mph']} mph -> {p['value_kmh']} km/h", fill=(255, 255, 0))
    ims.append(t)
w, h = ims[0].size
cols = 4
sheet = Image.new("RGB", (w * cols, h * ((len(ims) + cols - 1) // cols)))
for i, t in enumerate(ims):
    sheet.paste(t, ((i % cols) * w, (i // cols) * h))
sheet.save(out / f"_sheet_{label}.jpg", quality=85)
print(len(ims), "plates ->", out)
