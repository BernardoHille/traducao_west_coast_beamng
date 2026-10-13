"""Phase 7 QA: driver's-eye screenshot of every new R-19 sign (and of the Event 01 start) from the road it regulates.
Camera on the road axis, `back` m before the sign along the flow, 1.4 m above the road; looks at the sign.

    python working/functional/sign_shots.py <out_dir> [back_m]
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools/beamng"))
from mcp_client import BeamNGMCP, wait_for_file  # noqa: E402
from PIL import Image  # noqa: E402

out = Path(sys.argv[1])
back = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
out.mkdir(parents=True, exist_ok=True)
cfg = json.loads((HERE / "adas_zones.json").read_text(encoding="utf8"))
m = BeamNGMCP()
m.call("toggle_ui", show=False)
shots = []
for s in cfg["signs"]:
    mm = s["_measured"]
    fx, fy = mm["flow"]
    rp = mm["road_point"]
    cam = [rp[0] - fx * back, rp[1] - fy * back, mm["road_z"] + 1.4]
    tgt = [mm["xy"][0], mm["xy"][1], mm["ground_z"] + 2.2]
    q = json.loads(m.lua(f"local q = quatFromDir((vec3({tgt[0]},{tgt[1]},{tgt[2]}) - vec3({cam[0]},{cam[1]},{cam[2]})):normalized(), vec3(0,0,1)) "
                         "return jsonEncode({q.x,q.y,q.z,q.w})"))
    m.call("set_free_camera", pos=dict(zip("xyz", cam)), rot=dict(zip("xyzw", q)), fov=45)
    time.sleep(1.5)
    src = m.call("screenshot").strip()
    wait_for_file(src)
    im = Image.open(src).convert("RGB")
    im.thumbnail((1600, 1600))
    dst = out / f"{s['id']}.jpg"
    im.save(dst, quality=88)
    shots.append({"id": s["id"], "value": s["value"], "camera": [round(v, 2) for v in cam], "target": [round(v, 2) for v in tgt], "file": dst.name})
    print(dst)
(out / "shots.json").write_text(json.dumps(shots, indent=1) + "\n", encoding="utf8")
