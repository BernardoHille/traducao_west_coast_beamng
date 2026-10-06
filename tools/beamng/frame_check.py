"""Quick framing check of catalog points in the CURRENT game state (no reload): python tools/beamng/frame_check.py id..."""
import json, sys, time, shutil
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/beamng"))
import qa_runner as q
from mcp_client import BeamNGMCP
from PIL import Image
m = BeamNGMCP()
cat = q.catalog()
m.call("set_ui_state", route="play")
q.apply_preset(m, q.preset("day"))
tiles = []
for i in sys.argv[1:]:
    loc = [l for l in cat["locations"] if l["id"] == i][0]
    q.place_camera(m, loc["camera"]); time.sleep(3)
    p = REPO / "working/temporary/frame" / f"{i}.png"
    q.screenshot(m, str(p))
    tiles.append(Image.open(p).convert("RGB").resize((640, 331)))
m.call("toggle_ui", show=True)
s = Image.new("RGB", (1280, 331 * ((len(tiles) + 1) // 2)))
for k, t in enumerate(tiles):
    s.paste(t, ((k % 2) * 640, (k // 2) * 331))
s.save(REPO / "working/temporary/frame/sheet.jpg", quality=85)
print("ok")
