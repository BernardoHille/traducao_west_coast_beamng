"""Contact sheet original | PT-BR (and night) for QA review: python tools/beamng/qa_sheet.py <family> [out.jpg] [--ids a b]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]
fam = sys.argv[1]
out = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else REPO / f"working/temporary/qa_{fam}.jpg"
ids = sys.argv[sys.argv.index("--ids") + 1:] if "--ids" in sys.argv else None
d = REPO / "tests/screenshots/phase6" / fam
names = sorted({p.stem.rsplit("_original", 1)[0] for p in list(d.glob("*_original*.png")) + list(d.glob("*_original*.jpg"))})
if ids:
    names = [n for n in names if n in ids]
W, H = 640, 331
rows = []
for n in names:
    for suf in ("", "_night"):
        def pick(stem):
            for ext in (".png", ".jpg"):
                if (d / (stem + ext)).exists():
                    return d / (stem + ext)
            return d / (stem + ".png")
        a, b = pick(f"{n}_original{suf}"), pick(f"{n}_ptbr{suf}")
        if a.exists() or b.exists():
            r = Image.new("RGB", (W * 2 + 4, H + 16), (0, 0, 0))
            for i, p in enumerate((a, b)):
                if p.exists():
                    r.paste(Image.open(p).convert("RGB").resize((W, H)), (i * (W + 4), 16))
            ImageDraw.Draw(r).text((4, 2), n + suf, fill=(255, 255, 0))
            rows.append(r)
sheet = Image.new("RGB", (W * 2 + 4, sum(r.height for r in rows)))
y = 0
for r in rows:
    sheet.paste(r, (0, y)); y += r.height
sheet.save(out, quality=85)
print(out, len(rows))
