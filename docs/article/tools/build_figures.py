"""Fase 5.5 - gera as figuras do artigo a partir de evidencias reais.

Entradas (nunca alteradas):
  docs/article/figures/raw/*.png          capturas MCP desta fase (capture_article.py)
  tests/screenshots/poc|phase5/...        capturas das Fases 1 e 5
  source/originals/png, source/reference_ptbr, working/png   texturas
  export/reports/validation/images/*      heatmaps gerados por tools/validation/validate.py texture
  tools/validation/config/allowed_regions.json, docs/article/tools/annotation_points.json
Saidas: docs/article/figures/{aerial,comparisons,textures,validation,pipeline,final}/
Somente recorte, composicao lado a lado, caixas, setas e rotulos (Pillow). Sem edicao generativa.
Uso: python docs/article/tools/build_figures.py
"""
import json
import math
import os
import zipfile
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ART = os.path.join(REPO, "docs", "article")
RAW = os.path.join(ART, "figures", "raw")
FIG = os.path.join(ART, "figures")
GAME_LEVEL_ZIP = r"C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive\content\levels\west_coast_usa.zip"
FONTS = r"C:\Windows\Fonts"

INK = (28, 32, 38)
MUTED = (96, 104, 114)
WHITE = (255, 255, 255)
RED = (214, 40, 40)
BLUE = (29, 99, 196)
ORANGE = (230, 120, 20)
GREEN = (20, 140, 70)
PURPLE = (120, 60, 170)
CYAN = (0, 200, 220)


def font(size, bold=False):
    for name in (("segoeuib.ttf" if bold else "segoeui.ttf"), ("arialbd.ttf" if bold else "arial.ttf")):
        p = os.path.join(FONTS, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def p(*parts):
    return os.path.join(REPO, *parts)


def raw(name):
    return Image.open(os.path.join(RAW, name)).convert("RGB")


def save(img, sub, name, quality=92):
    os.makedirs(os.path.join(FIG, sub), exist_ok=True)
    path = os.path.join(FIG, sub, name)
    if name.endswith(".jpg"):
        img.convert("RGB").save(path, quality=quality, optimize=True)
    else:
        img.save(path, optimize=True)
    print(f"{os.path.relpath(path, REPO)}  {img.size[0]}x{img.size[1]}  {os.path.getsize(path) / 1e6:.2f} MB")
    return path


def titled(img, letter, title, bar=58, size=26):
    """Panel with a title bar above the image: [A] title."""
    out = Image.new("RGB", (img.width, img.height + bar), WHITE)
    out.paste(img, (0, bar))
    d = ImageDraw.Draw(out)
    x = 0
    if letter:
        d.rectangle([0, 8, 42, bar - 8], fill=INK)
        tw = d.textlength(letter, font=font(size, True))
        d.text(((42 - tw) / 2, (bar - size) / 2 - 3), letter, fill=WHITE, font=font(size, True))
        x = 54
    n = title.count("\n") + 1
    d.multiline_text((x, (bar - n * (size + 4)) / 2 - 2), title, fill=INK, font=font(size, True), spacing=4)
    return out


def row(panels, gap=18, bg=WHITE, valign="top"):
    h = max(pn.height for pn in panels)
    w = sum(pn.width for pn in panels) + gap * (len(panels) - 1)
    out = Image.new("RGB", (w, h), bg)
    x = 0
    for pn in panels:
        out.paste(pn, (x, 0 if valign == "top" else (h - pn.height) // 2))
        x += pn.width + gap
    return out


def col(panels, gap=18, bg=WHITE):
    w = max(pn.width for pn in panels)
    h = sum(pn.height for pn in panels) + gap * (len(panels) - 1)
    out = Image.new("RGB", (w, h), bg)
    y = 0
    for pn in panels:
        out.paste(pn, (0, y))
        y += pn.height + gap
    return out


def pad(img, m=24, bg=WHITE):
    out = Image.new("RGB", (img.width + 2 * m, img.height + 2 * m), bg)
    out.paste(img, (m, m))
    return out


def label_box(d, xy, text, fg=WHITE, bg=INK, size=24, anchor="lt", padding=8):
    f = font(size, True)
    lines = text.split("\n")
    w = max(d.textlength(t, font=f) for t in lines) + 2 * padding
    h = len(lines) * (size + 6) + 2 * padding - 6
    x, y = xy
    if "r" in anchor:
        x -= w
    if "b" in anchor:
        y -= h
    if "m" in anchor:
        x -= w / 2
    d.rectangle([x, y, x + w, y + h], fill=bg)
    for i, t in enumerate(lines):
        d.text((x + padding, y + padding + i * (size + 6) - 2), t, fill=fg, font=f)
    return (x, y, x + w, y + h)


def ring(d, xy, r, color, width=5, number=None, size=26):
    x, y = xy
    d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], outline=WHITE, width=width + 4)
    d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=width)
    if number is not None:
        f = font(size, True)
        d.ellipse([x + r * 0.55, y - r * 1.75, x + r * 0.55 + 38, y - r * 1.75 + 38], fill=color, outline=WHITE, width=3)
        tw = d.textlength(str(number), font=f)
        d.text((x + r * 0.55 + 19 - tw / 2, y - r * 1.75 + 2), str(number), fill=WHITE, font=f)


def arrow(d, a, b, color, width=5, head=18):
    d.line([a, b], fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (-1, 1):
        d.line([b, (b[0] - head * math.cos(ang + s * 0.45), b[1] - head * math.sin(ang + s * 0.45))], fill=color, width=width)


def checker(size, s=16):
    w, h = size
    a = (np.indices((h, w)) // s).sum(0) % 2
    v = np.where(a, 205, 240).astype(np.uint8)
    return Image.fromarray(np.dstack([v, v, v]))


def on_gray(img_rgba, g=128):
    bg = Image.new("RGB", img_rgba.size, (g, g, g))
    bg.paste(img_rgba.convert("RGB"), mask=img_rgba.split()[3])
    return bg


ANCH = json.load(open(os.path.join(ART, "tools", "annotation_points.json"), encoding="utf-8"))


# ------------------------------------------------------------------ Fig. 1 - aerial
def fig_aerial():
    base = raw("aerial_downtown__original.png")
    img = base.copy()
    d = ImageDraw.Draw(img)
    a = ANCH["aerial_downtown"]
    marks = [(1, a["stop_chinatown"], RED), (2, a["bus_only"], ORANGE), (3, a["keep_clear"], ORANGE),
             (4, a["speed25_hill"], BLUE), (5, a["yield_downtown"], RED)]
    for n, xy, c in marks:
        ring(d, xy, 24, c, number=n)
    # off-frame R-19 10 (parking) just south of the frame
    x = a["speed5_parking_projected_offframe"][0]
    arrow(d, (x, 900), (x, 985), BLUE, width=6)
    f = font(26, True)
    d.ellipse([x + 14, 905, x + 52, 943], fill=BLUE, outline=WHITE, width=3)
    d.text((x + 33 - d.textlength("6", font=f) / 2, 907), "6", fill=WHITE, font=f)
    # north arrow + scale (100 m at ground z~120 m: depth ~640 m, focal 1064.8 px -> 0.601 m/px)
    arrow(d, (1840, 150), (1840, 60), WHITE, width=7, head=22)
    d.text((1828, 152), "N", fill=WHITE, font=font(30, True))
    px100 = 100 / 0.601
    d.rectangle([60, 930, 60 + px100, 944], fill=WHITE, outline=INK, width=2)
    d.text((60, 890), "≈ 100 m", fill=WHITE, font=font(26, True))
    legend = Image.new("RGB", (560, img.height), WHITE)
    ld = ImageDraw.Draw(legend)
    ld.text((24, 22), "Pontos usados no artigo", fill=INK, font=font(30, True))
    items = [
        (1, RED, "STOP → PARE (R-1)", "Chinatown · ponto de QA da Fase 1"),
        (2, ORANGE, "BUS ONLY no pavimento", "decalques de palavra (família\nt_decal_roadmarkings, não produzida)"),
        (3, ORANGE, "KEEP CLEAR no pavimento", "idem"),
        (4, BLUE, "SPEED LIMIT 25 → R-19 40", "colina · ponto da Fase 2"),
        (5, RED, "YIELD → R-2 sem legenda", "ponto roadsigns_downtown_yield"),
        (6, BLUE, "SPEED LIMIT 5 → R-19 10", "estacionamento logo ao sul do\nlimite do quadro (≈ 11 m)"),
    ]
    y = 86
    for n, c, t1, t2 in items:
        ld.ellipse([24, y, 62, y + 38], fill=c)
        ld.text((43 - ld.textlength(str(n), font=font(24, True)) / 2, y + 3), str(n), fill=WHITE, font=font(24, True))
        ld.text((78, y - 2), t1, fill=INK, font=font(25, True))
        ld.multiline_text((78, y + 32), t2, fill=MUTED, font=font(21), spacing=4)
        y += 120 if "\n" in t2 else 98
    ld.multiline_text((24, y + 6), "Câmera livre a 760 m de altitude,\nFOV vertical 50°, norte para cima.\n"
                      "Marcadores projetados das coordenadas\ndo mapa e conferidos com esferas de\n"
                      "depuração no jogo (erro ≤ 6 px).\nMod desligado (mapa original).",
                      fill=MUTED, font=font(20), spacing=5)
    return save(row([img, legend], gap=0), "aerial", "fig_01_wcusa_aerial_annotated.jpg")


# ------------------------------------------------------------------ Fig. 2 - validator heatmaps
def fig_heatmaps():
    a = Image.open(p("export", "reports", "validation", "images", "t_roadsigns_b.color_ptbr_diff.png")).convert("RGB")
    b = Image.open(p("export", "reports", "validation", "images", "t_roadsigns_b.color_diff.png")).convert("RGB")
    w = 1400
    a, b = (im.resize((w, w // 2), Image.LANCZOS) for im in (a, b))
    pa = titled(a, "A", "Referência PT-BR antiga: 59,88 % dos pixels fora das 44 regiões autorizadas mudaram (FAIL)")
    pb = titled(b, "B", "Atlas da Fase 5: 0 px fora das regiões; 188.445 px dentro de 44 regiões (PASS)")
    return save(pad(col([pa, pb], gap=28)), "validation", "fig_02_heatmap_t_roadsigns_legacy_vs_phase5.jpg", 90)


# ------------------------------------------------------------------ Fig. 3 - atlas with real regions
SHARED = [  # from docs/production/t_roadsigns_plan.md (UV inventory of the instanced meshes)
    ("algarismos 0–9 (compartilhados)", (340, 0, 900, 84)),
    ("SPEED LIMIT", (229, 284, 363, 381)),
    ("MPH", (256, 244, 352, 279)),
    ("ONLY", (352, 141, 440, 186)),
    ("CARPOOLS", (1409, 0, 1742, 88)),
    ("PER VEHICLE", (685, 72, 876, 116)),
    ("¼ ½ ¾", (340, 84, 520, 143)),
    ("MILES", (638, 116, 780, 153)),
    ("painel branco R-19", (370, 189, 516, 381)),
]


def region_color(rid):
    if rid in ("stop_r1", "yield_r2", "do_not_enter_r3", "wrong_way"):
        return RED
    if rid.startswith("g_"):
        return PURPLE
    if rid.startswith("n_"):
        return GREEN
    return BLUE


def dashed_rect(d, box, color, width=4, dash=12):
    x0, y0, x1, y1 = box
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        L = math.dist(a, b)
        n = max(1, int(L // (2 * dash)))
        for i in range(n):
            t0, t1 = (2 * i) / (2 * n), (2 * i + 1) / (2 * n)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=color, width=width)


def fig_atlas():
    atlas = on_gray(Image.open(p("source", "originals", "png", "t_roadsigns_b.color.png")).convert("RGBA"), 70)
    d = ImageDraw.Draw(atlas)
    regs = json.load(open(p("tools", "validation", "config", "allowed_regions.json"), encoding="utf-8"))["t_roadsigns_b.color"]["regions"]
    for r in regs:
        d.rectangle([r["x"], r["y"], r["x"] + r["width"] - 1, r["y"] + r["height"] - 1], outline=region_color(r["id"]), width=4)
    for name, box in SHARED:
        dashed_rect(d, box, ORANGE, width=4)
    tags = {"stop_r1": "R-1 STOP", "yield_r2": "R-2 YIELD", "do_not_enter_r3": "R-3", "speed_camera": "câmera vel.",
            "red_light_camera": "câmera sinal", "danger_header": "PERIGO"}
    for r in regs:
        if r["id"] in tags:
            label_box(d, (r["x"] + 2, r["y"] + r["height"] + 2), tags[r["id"]], size=20, padding=4, bg=region_color(r["id"]))
    label_box(d, (342, 86 + 60), "algarismos / frações", size=20, padding=4, bg=ORANGE)
    label_box(d, (230, 383), "SPEED LIMIT", size=20, padding=4, bg=ORANGE)
    leg = Image.new("RGB", (atlas.width, 150), WHITE)
    ld = ImageDraw.Draw(leg)
    entries = [(RED, "solid", "Regulamentação: PARE, R-2, R-3, CONTRAMÃO (4)"),
               (BLUE, "solid", "Painéis, perigo e fiscalização (12)"),
               (PURPLE, "solid", "Palavras recortadas pela opacidade (14)"),
               (GREEN, "solid", "Nomes de vias e destinos (14)"),
               (ORANGE, "dash", "Glifos/painéis compartilhados — preservados")]
    x, y = 24, 22
    for i, (c, style, t) in enumerate(entries):
        if style == "solid":
            ld.rectangle([x, y + 4, x + 44, y + 30], outline=c, width=5)
        else:
            dashed_rect(ld, (x, y + 4, x + 44, y + 30), c, width=5, dash=7)
        ld.text((x + 58, y), t, fill=INK, font=font(26, True))
        if i == 2:
            x, y = 1040, 22
        else:
            y += 42
    return save(col([atlas, leg], gap=0), "textures", "fig_03_atlas_roadsigns_regions.jpg", 90)


# ------------------------------------------------------------------ Fig. 4 - STOP region pixel zoom
def fig_stop_zoom():
    box = (1134, 201, 1320, 387)  # 186 x 186 around stop_r1 (1164, 231, 126 x 127)
    srcs = [("A", "Original do jogo", p("source", "originals", "png", "t_roadsigns_b.color.png")),
            ("B", "Referência antiga (PoC)", p("source", "reference_ptbr", "t_roadsigns_b.color_ptbr.png")),
            ("C", "Reconstrução da Fase 5", p("working", "png", "t_roadsigns_b.color.png"))]
    k = 3
    panels = []
    for letter, title, path in srcs:
        crop = on_gray(Image.open(path).convert("RGBA").crop(box), 128).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.NEAREST)
        d = ImageDraw.Draw(crop)
        ux0, uy0 = (1164 - box[0]) * k, (231 - box[1]) * k
        d.rectangle([ux0, uy0, ux0 + 126 * k - 1, uy0 + 127 * k - 1], outline=CYAN, width=4)
        panels.append(titled(crop, letter, title, size=24))
    note = Image.new("RGB", (row(panels).width, 70), WHITE)
    ImageDraw.Draw(note).text((4, 18), "Contorno ciano: região UV que sign_stop.dae (52 instâncias) e roadsigns.dae amostram, "
                              "x 1164–1290, y 231–358 px. Ampliação 3× sem interpolação.", fill=MUTED, font=font(22))
    return save(pad(col([row(panels), note], gap=6)), "textures", "fig_04_stop_uv_region_zoom.png")


# ------------------------------------------------------------------ in-game comparisons
def crops(names, box):
    return [raw(n).crop(box) for n in names]


def fig_stop_ingame():
    box = (590, 280, 1330, 920)
    a, b, c = crops(["roadsigns_chinatown_stop__original.png", "roadsigns_chinatown_stop__poc.png",
                     "roadsigns_chinatown_stop__ptbr.png"], box)
    panels = [titled(a, "A", "Original (mod desligado)"), titled(b, "B", "PoC da Fase 1 (referência antiga)"),
              titled(c, "C", "Fase 5 (atlas reconstruído)")]
    return save(pad(row(panels)), "comparisons", "fig_05_stop_chinatown_A_B_C.jpg")


def fig_yield_ingame():
    box = (620, 170, 1300, 790)
    a, b, c = crops(["roadsigns_downtown_yield__original.png", "roadsigns_downtown_yield__poc.png",
                     "roadsigns_downtown_yield__ptbr.png"], box)
    panels = [titled(a, "A", "Original: YIELD"), titled(b, "B", "Referência antiga: texto no triângulo"),
              titled(c, "C", "Fase 5: R-2 sem legenda")]
    return save(pad(row(panels)), "comparisons", "fig_16_yield_r2_A_B_C.jpg")


def fig_r19_ingame():
    hb, pb = (680, 0, 1240, 993), (674, 0, 1234, 993)
    a, b = crops(["r19_40_hill__original.png", "r19_40_hill__ptbr.png"], hb)
    c, d = crops(["r19_10_downtown_parking__original.png", "r19_10_downtown_parking__ptbr.png"], pb)
    panels = [titled(a, "A", "25 mph (original)"), titled(b, "B", "R-19 40 km/h"),
              titled(c, "C", "5 mph (original)"), titled(d, "D", "R-19 10 km/h")]
    return save(pad(row(panels)), "comparisons", "fig_19_r19_40_and_10_ingame.jpg")


def fig_poc_onoff():
    box = (600, 290, 1380, 930)
    names = ["roadsigns_mod_on.png", "roadsigns_mod_off.png", "roadsigns_mod_on_again.png"]
    ims = [Image.open(p("tests", "screenshots", "poc", n)).convert("RGB").crop(box) for n in names]
    panels = [titled(ims[0], "A", "Mod ativo"), titled(ims[1], "B", "Mod desativado + recarga"),
              titled(ims[2], "C", "Mod reativado + recarga")]
    return save(pad(row(panels)), "comparisons", "fig_07_poc_override_on_off_on.jpg")


def fig_gantry():
    box = (400, 360, 1580, 640)
    a = Image.open(p("tests", "screenshots", "phase5", "t_roadsigns", "roadsigns_toll_plaza_original.jpg")).convert("RGB").crop(box)
    b = Image.open(p("tests", "screenshots", "phase5", "t_roadsigns", "roadsigns_toll_plaza_ptbr.jpg")).convert("RGB").crop(box)
    return save(pad(col([titled(a, "A", "Original"), titled(b, "B", "Fase 5 (CARPOOLS ONLY e ½ MILE seguem em inglês: glifos compartilhados)")])),
                "comparisons", "fig_20_gantry_toll_plaza.jpg")


# ------------------------------------------------------------------ Fig. 8 - alpha
def alpha_stats(img):
    a = np.asarray(img.split()[3])
    return 100 * (a == 0).mean(), 100 * ((a > 0) & (a < 255)).mean()


def fig_alpha():
    pairs = [("eca_roadsigns_d", p("source", "originals", "png", "eca_roadsigns_d.png"), p("source", "reference_ptbr", "eca_roadsigns_d_ptbr.png"), 640),
             ("t_billboardsigns_dealers_b", p("source", "originals", "png", "t_billboardsigns_dealers_b.color.png"),
              p("source", "reference_ptbr", "t_billboardsigns_dealers_b.color_ptbr.png"), 640)]
    rows_ = []
    letters = iter("ABCD")
    for name, o, r, w in pairs:
        cells = []
        for kind, path in (("original", o), ("referência antiga", r)):
            im = Image.open(path).convert("RGBA")
            t, s = alpha_stats(im)
            al = im.split()[3].convert("RGB")
            al = al.resize((w, int(w * al.height / al.width)), Image.LANCZOS)
            ImageDraw.Draw(al).rectangle([0, 0, al.width - 1, al.height - 1], outline=(150, 150, 150), width=2)
            fmt = lambda v: f"{v:.1f}".replace(".", ",")
            cells.append(titled(al, next(letters), f"{name} · {kind}\n{fmt(t)} % alfa 0 · {fmt(s)} % semitransparente",
                                size=20, bar=72))
        rows_.append(row(cells))
    note = Image.new("RGB", (rows_[0].width, 60), WHITE)
    ImageDraw.Draw(note).text((4, 14), "Canal alfa em tons de cinza: preto = transparente (0), branco = opaco (255).",
                              fill=MUTED, font=font(22))
    return save(pad(col(rows_ + [note], gap=14)), "textures", "fig_08_alpha_loss_legacy.png")


# ------------------------------------------------------------------ Fig. 9 - road marking atlas slots
RM_WORDS = {0: ("seta esquerda", "—"), 1: ("seta direita", "—"), 2: ("seta reta", "—"), 3: ("STOP", "PARE"), 4: ("losango", "—"),
            5: ("ONLY", "needs_context"), 6: ("BUS", "ÔNIBUS"), 7: ("KEEP", "NÃO"), 8: ("CLEAR", "BLOQUEIE"), 9: ("NO", "SEM"),
            10: ("LEFT", "não usado"), 11: ("TURN", "não usado"), 12: ("(vazio)", "—"), 13: ("moldura", "—"), 14: ("EXIT", "SAÍDA"),
            15: ("grelha", "—")}


def fig_roadmarkings_atlas():
    z = zipfile.ZipFile(GAME_LEVEL_ZIP)
    inst = json.loads(z.read("levels/west_coast_usa/main.decals.json"))["instances"]["decal_roadmarkings1"]
    cnt = Counter(r[0] for r in inst)
    atlas = on_gray(Image.open(p("source", "originals", "png", "t_decal_roadmarkings_b.color.png")).convert("RGBA"), 120)
    cell, strip = 256, 74
    out = Image.new("RGB", (4 * cell, 4 * (cell + strip)), WHITE)
    d = ImageDraw.Draw(out)
    for i in range(16):
        r, c = divmod(i, 4)
        tile = atlas.crop((c * cell, r * cell, (c + 1) * cell, (r + 1) * cell))
        x, y = c * cell, r * (cell + strip)
        out.paste(tile, (x, y))
        d.rectangle([x, y, x + cell - 1, y + cell - 1], outline=WHITE, width=2)
        word, pt = RM_WORDS[i]
        text_word = word in ("STOP", "ONLY", "BUS", "KEEP", "CLEAR", "NO", "LEFT", "TURN", "EXIT")
        bg = (255, 244, 230) if text_word else (245, 246, 248)
        d.rectangle([x, y + cell, x + cell - 1, y + cell + strip - 1], fill=bg)
        d.text((x + 8, y + cell + 4), f"rectIdx {i} · {word}", fill=INK, font=font(19, True))
        d.text((x + 8, y + cell + 36), f"{cnt.get(i, 0)} inst. → {pt}", fill=ORANGE if text_word else MUTED, font=font(19, True))
    return save(pad(out), "textures", "fig_09_roadmarkings_atlas_slots.png")


# ------------------------------------------------------------------ Fig. 10 - road markings from above
def fig_roadmarkings_top():
    a = raw("decal_bus_only_top__original.png")
    da = ImageDraw.Draw(a)
    bus = ANCH["decal_bus_only_top"]["bus"][:2]
    only = (820, 380)  # sphere hidden under the surface: placed on the visible word
    for xy, t in ((bus, "decal rectIdx 6 · BUS"), (only, "decal rectIdx 5 · ONLY")):
        ring(da, xy, 70, ORANGE, width=6)
        label_box(da, (xy[0] + 80, xy[1] - 20), t, bg=ORANGE, size=26)
    label_box(da, (590, 880), "2 decalques independentes · 7,4 m entre centros", size=24)
    a = a.crop((540, 120, 1500, 960))
    b = raw("decal_keep_clear_top__original.png")
    db = ImageDraw.Draw(b)
    keep = (760, 690)
    clear = ANCH["decal_keep_clear_top"]["clear"][:2]
    for xy, t, anc, dx in ((keep, "decal rectIdx 7 · KEEP", "lt", 90), (clear, "decal rectIdx 8 · CLEAR", "rt", -90)):
        ring(db, xy, 80, ORANGE, width=6)
        label_box(db, (xy[0] + dx, xy[1] - 20), t, bg=ORANGE, size=26, anchor=anc)
    label_box(db, (520, 900), "2 decalques independentes · 11,4 m entre centros", size=24)
    b = b.crop((480, 140, 1440, 980))
    return save(pad(row([titled(a, "A", "BUS ONLY (faixa de ônibus)"), titled(b, "B", "KEEP CLEAR (cruzamento)")])),
                "aerial", "fig_10_roadmarkings_top_view.jpg")


# ------------------------------------------------------------------ Fig. 12 - QA point
def fig_qa_point():
    img = raw("qa_context_top__ptbr.png")
    d = ImageDraw.Draw(img)
    c = ANCH["qa_context_top"]
    sign, cam = c["sign"][:2], c["qacam"][:2]
    ang = math.atan2(sign[1] - cam[1], sign[0] - cam[0])
    for s in (-1, 1):  # field-of-view wedge (50 deg vertical ~ 86 deg horizontal at 1920x993)
        e = (cam[0] + 230 * math.cos(ang + s * math.radians(43)), cam[1] + 230 * math.sin(ang + s * math.radians(43)))
        d.line([cam, e], fill=CYAN, width=4)
    arrow(d, cam, (sign[0] + (cam[0] - sign[0]) * 0.18, sign[1] + (cam[1] - sign[1]) * 0.18), CYAN, width=5)
    ring(d, cam, 20, CYAN, width=6)
    ring(d, sign, 26, RED, width=6)
    label_box(d, (sign[0] + 50, sign[1] - 60), "placa sign_stop.dae\n(−712,667; 552,899; 122,435)", anchor="lb", bg=RED, size=24)
    label_box(d, (cam[0] + 40, cam[1] + 10), "câmera do ponto roadsigns_chinatown_stop\npos (−710,782; 550,313; 122,835)\n"
              "quat (0,0074; 0,0024; −0,3099; 0,9507) · FOV 50°\ndistância à placa ≈ 3,2 m", bg=(0, 120, 140), size=24)
    inset = raw("roadsigns_chinatown_stop__ptbr.png").resize((576, 298), Image.LANCZOS)
    inset = titled(inset, "", "Quadro capturado nesse ponto", bar=44, size=22)
    img.paste(Image.new("RGB", (inset.width + 8, inset.height + 8), WHITE), (16, 16))
    img.paste(inset, (20, 20))
    return save(img, "final", "fig_12_qa_point_chinatown_top.jpg")


# ------------------------------------------------------------------ Fig. 17/18 - R-19 asset, port side effect
def fig_r19_asset():
    col40 = Image.open(p("working", "png", "r19", "t_r19_40_b.color.png")).convert("RGB")
    col10 = Image.open(p("working", "png", "r19", "t_r19_10_b.color.png")).convert("RGB")
    mask = Image.open(p("working", "png", "r19", "t_r19_o.data.png")).convert("L")
    w, h = 300, 600

    def comp(c):
        bg = checker(c.size)
        bg.paste(c, mask=mask.point(lambda v: 255 if v >= 128 else 0))  # alphaTest 128, as the material
        return bg.resize((w, h), Image.LANCZOS)

    panels = [titled(col40.resize((w, h), Image.LANCZOS), "A", "cor (40)", size=22, bar=48),
              titled(mask.convert("RGB").resize((w, h), Image.LANCZOS), "B", "opacidade", size=22, bar=48),
              titled(comp(col40), "C", "40 recortado", size=22, bar=48),
              titled(comp(col10), "D", "10 recortado", size=22, bar=48)]
    note = Image.new("RGB", (row(panels).width, 92), WHITE)
    ImageDraw.Draw(note).multiline_text((4, 10), "Texturas 512×1024 do painel 0,7317 × 1 m (UV 0–1). Disco D = 0,99 × largura; orla = 0,10 D;\n"
                                        "algarismos = 0,40 D; recorte por alphaTest 128 (xadrez = transparente).",
                                        fill=MUTED, font=font(21), spacing=6)
    return save(pad(col([row(panels), note], gap=6)), "textures", "fig_17_r19_texture_and_mask.png")


def fig_port_bay():
    a = Image.open(p("tests", "screenshots", "phase5", "roadsigns_ptbr_r19", "port_bay_plate_side_effect_original_vs_inplace_override.jpg")).convert("RGB")
    b = Image.open(p("tests", "screenshots", "phase5", "roadsigns_ptbr_r19", "port_bay_plate_after_fix_original_vs_mod.jpg")).convert("RGB")
    return save(pad(col([titled(a, "A", "Substituição de sign_speed5.dae no mesmo caminho (original | mod)", size=22, bar=48),
                         titled(b, "B", "Após a correção: mesh novo só nas 7 placas (original | mod)", size=22, bar=48)])),
                "validation", "fig_18_port_bay_plate_side_effect.jpg")


def fig_pavement_state():
    img = raw("decal_stop_chinatown_oblique__ptbr.png")
    d = ImageDraw.Draw(img)
    c = ANCH["decal_stop_chinatown_oblique"]
    ring(d, c["sign"][:2], 40, RED, width=6)
    label_box(d, (c["sign"][0] + 55, c["sign"][1] - 30), "placa: PARE\n(t_roadsigns, Fase 5)", bg=RED, size=26)
    ring(d, c["decal"][:2], 95, ORANGE, width=6)
    label_box(d, (c["decal"][0] + 110, c["decal"][1] - 10), "pavimento: STOP\n(t_decal_roadmarkings,\nainda não produzida)", bg=ORANGE, size=26)
    return save(img, "final", "fig_21_pare_sign_with_stop_pavement.jpg")


# ------------------------------------------------------------------ SVG diagrams
SVG_HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            'font-family="Segoe UI, Arial, sans-serif"><rect width="100%" height="100%" fill="#ffffff"/>'
            '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#1c2026"/></marker></defs>')


def box_svg(x, y, w, h, title, sub="", fill="#eef3fb", stroke="#1d63c4", tsize=17):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    ty = y + (h / 2 + 6 if not sub else h / 2 - 4)
    s += f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" font-size="{tsize}" font-weight="700" fill="#1c2026">{title}</text>'
    for i, line in enumerate(sub.split("\n") if sub else []):
        s += f'<text x="{x + w / 2}" y="{y + h / 2 + 18 + i * 17}" text-anchor="middle" font-size="13" fill="#4c5560">{line}</text>'
    return s


def line_svg(x1, y1, x2, y2, dash=False):
    da = ' stroke-dasharray="6,5"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1c2026" stroke-width="2"{da} marker-end="url(#ah)"/>'


def write_svg(sub, name, body, w, h):
    os.makedirs(os.path.join(FIG, sub), exist_ok=True)
    path = os.path.join(FIG, sub, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(SVG_HEAD.format(w=w, h=h) + body + "</svg>\n")
    print(f"{os.path.relpath(path, REPO)}  svg")
    return path


def fig_vfs():
    b = ""
    b += box_svg(250, 20, 420, 70, "BeamNG solicita o caminho virtual", "/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds", "#f3f4f6", "#1c2026")
    b += box_svg(250, 130, 420, 60, "Sistema de arquivos virtual (VFS)", "monta zips do jogo + pastas de mods; mod ativo tem precedência", "#fff7e8", "#e67814")
    b += line_svg(460, 90, 460, 128)
    b += line_svg(400, 190, 210, 240)
    b += line_svg(520, 190, 710, 240)
    b += box_svg(20, 240, 400, 110, "MOD ATIVO", "current/mods/unpacked/traducao_ptbr_wcusa/\nassets/materials/signage/roadsigns/\nt_roadsigns_b.color.dds  →  PARE", "#eaf6ee", "#148c46")
    b += box_svg(500, 240, 400, 110, "MOD INATIVO", "content/assets/materials/signage.zip\n(instalação do jogo, somente leitura)\nt_roadsigns_b.color.dds  →  STOP", "#fbeaea", "#d62828")
    b += ('<text x="460" y="390" text-anchor="middle" font-size="14" fill="#4c5560">Mesmo nome, mesmo caminho, mesmo formato: o material '
          '<tspan font-weight="700">roadsigns</tspan> não muda; só a origem do arquivo muda (MCP file_info → realPath).</text>')
    return write_svg("pipeline", "fig_06_vfs_override.svg", b, 920, 410)


def fig_qa_pipeline():
    steps = [("Asset original", "SHA-256 do manifesto"), ("Edição", "master determinístico"), ("Validação PNG", "validate.py texture"),
             ("Conversão DDS", "texconv, formato original"), ("Validação DDS", "dds / family / new"), ("Montagem do mod", "install_mod.py + mod --installed"),
             ("BeamNG via MCP", "smallgrid → mapa, preset"), ("Screenshot", "pose de câmera fixa"), ("Comparação", "original × PT-BR + revisão humana")]
    b, x, y = "", 20, 30
    w, h, gx, gy = 250, 78, 40, 52
    for i, (t, s) in enumerate(steps):
        r, c = divmod(i, 3)
        cx = x + (c if r % 2 == 0 else 2 - c) * (w + gx)
        cy = y + r * (h + gy)
        fill = "#eef3fb" if i < 6 else "#eaf6ee"
        b += box_svg(cx, cy, w, h, f"{i + 1}. {t}", s, fill, "#1d63c4" if i < 6 else "#148c46")
        if i < len(steps) - 1:
            r2, c2 = divmod(i + 1, 3)
            nx = x + (c2 if r2 % 2 == 0 else 2 - c2) * (w + gx)
            ny = y + r2 * (h + gy)
            if r2 == r:
                b += line_svg(cx + w if nx > cx else cx, cy + h / 2, nx if nx > cx else nx + w, ny + h / 2)
            else:
                b += line_svg(cx + w / 2, cy + h, nx + w / 2, ny)
    b += ('<text x="20" y="425" font-size="13" fill="#4c5560">Azul: etapas offline (repositório). Verde: etapas no jogo, '
          'automatizadas pelo MCP do BeamNG. Um passo só avança com zero FAIL.</text>')
    return write_svg("pipeline", "fig_11_qa_pipeline.svg", b, 900, 440)


def fig_speed_conversion():
    b = ""
    items = [("25 mph", "valor da placa original", "#f3f4f6", "#1c2026"),
             ("40,23 km/h", "× 1,609344 (conversão exata)", "#fff7e8", "#e67814"),
             ("40 km/h", "múltiplo de 10 (MBST-I p.35)", "#eaf6ee", "#148c46"),
             ("11,1111 m/s", "÷ 3,6 (valor gravado no mapa)", "#eef3fb", "#1d63c4")]
    for i, (t, s, f, st) in enumerate(items):
        x = 20 + i * 235
        b += box_svg(x, 40, 195, 90, t, s, f, st, tsize=22)
        if i < 3:
            b += line_svg(x + 195, 85, x + 233, 85)
    b += '<text x="20" y="24" font-size="15" font-weight="700" fill="#1c2026">Placa (jogador)</text>'
    b += '<text x="725" y="24" font-size="15" font-weight="700" fill="#1c2026">Lógica (IA / tráfego)</text>'
    rows = [("5 mph", "8,05", "10", "2,7778"), ("15 mph", "24,14", "20", "5,5556"), ("25 mph", "40,23", "40", "11,1111"),
            ("30 mph", "48,28", "50", "13,8889"), ("35 mph", "56,33", "60", "16,6667"), ("50 mph", "80,47", "80", "22,2222")]
    y0 = 170
    heads = ["Original", "Matemático (km/h)", "Placa PT-BR (km/h)", "Armazenado (m/s)"]
    for j, hd in enumerate(heads):
        b += f'<text x="{20 + j * 235 + 97}" y="{y0}" text-anchor="middle" font-size="14" font-weight="700" fill="#1c2026">{hd}</text>'
    for i, r in enumerate(rows):
        y = y0 + 26 + i * 24
        if i % 2 == 0:
            b += f'<rect x="20" y="{y - 17}" width="900" height="24" fill="#f6f7f9"/>'
        for j, v in enumerate(r):
            weight = "700" if j == 2 else "400"
            b += f'<text x="{20 + j * 235 + 97}" y="{y}" text-anchor="middle" font-size="14" font-weight="{weight}" fill="#1c2026">{v}</text>'
    b += ('<text x="20" y="360" font-size="13" fill="#4c5560">Implementados na Fase 5: 5 → 10 e 25 → 40 km/h. As demais linhas são a regra '
          'definida (LOCALIZATION_RULES.md §2), ainda sem alteração no mapa.</text>')
    return write_svg("pipeline", "fig_13_speed_conversion.svg", b, 940, 375)


def fig_speed_distribution():
    data = [(30, 3292, "auto"), (40.2, 200, "mph"), (41.4, 1, "mph"), (43.2, 58, "mph"), (50, 674, "auto"), (56.3, 96, "mph"),
            (60, 2579, "auto"), (80, 906, "auto"), (100, 1049, "auto"), (120, 482, "auto")]
    W, H, x0, y0, bw = 900, 380, 70, 320, 66
    mx = 3400
    b = '<text x="20" y="26" font-size="15" font-weight="700" fill="#1c2026">Arestas do navgraph por limite (West Coast original, 9.337 arestas)</text>'
    for t in (0, 1000, 2000, 3000):
        y = y0 - t / mx * 260
        b += f'<line x1="{x0}" y1="{y}" x2="{W - 20}" y2="{y}" stroke="#e3e6ea"/>'
        b += f'<text x="{x0 - 8}" y="{y + 4}" text-anchor="end" font-size="12" fill="#4c5560">{t:,}</text>'.replace(",", ".")
    for i, (v, n, kind) in enumerate(data):
        x = x0 + 12 + i * (bw + 16)
        hgt = max(2, n / mx * 260)
        fill = "#1d63c4" if kind == "auto" else "#e67814"
        b += f'<rect x="{x}" y="{y0 - hgt}" width="{bw}" height="{hgt}" fill="{fill}"/>'
        b += f'<text x="{x + bw / 2}" y="{y0 - hgt - 6}" text-anchor="middle" font-size="12" fill="#1c2026">{n:,}</text>'.replace(",", ".")
        b += f'<text x="{x + bw / 2}" y="{y0 + 18}" text-anchor="middle" font-size="13" fill="#1c2026">{str(v).replace(".", ",")}</text>'
    b += f'<text x="{x0 + 360}" y="{y0 + 44}" text-anchor="middle" font-size="13" fill="#4c5560">km/h</text>'
    b += '<rect x="560" y="44" width="14" height="14" fill="#1d63c4"/><text x="580" y="56" font-size="13" fill="#1c2026">automático (lista métrica do motor)</text>'
    b += '<rect x="560" y="66" width="14" height="14" fill="#e67814"/><text x="580" y="78" font-size="13" fill="#1c2026">explícito herdado de mph (355 arestas)</text>'
    return write_svg("validation", "fig_14_navgraph_speed_distribution.svg", b, W, H)


def fig_sign_logic():
    b = ""
    chain = [("R-19 40 (placa)", "mesh + material próprios"), ("DecalRoad.speedLimit", "\"11.1111\" (m/s, texto)"),
             ("navgraph", "map.getMap(): links[].speedLimit"), ("IA · tráfego · polícia", "set_ai speedMode legal; infrações")]
    for i, (t, s) in enumerate(chain):
        y = 20 + i * 100
        b += box_svg(40, y, 330, 70, t, s, "#eef3fb", "#1d63c4")
        if i < 3:
            b += line_svg(205, y + 70, 205, y + 98)
    b += box_svg(470, 120, 350, 70, "slotTraffic.json", "cópia derivada (faixas + ligações, m/s)", "#fff7e8", "#e67814")
    b += line_svg(370, 155, 468, 155)
    b += box_svg(470, 240, 350, 70, "Radares · zonas · missões", "valores próprios (m/s) — fora da Fase 5", "#f3f4f6", "#8a9099")
    b += box_svg(470, 340, 350, 70, "ADAS (mods de pesquisa)", "limiar fixo em km/h, não lê o mapa", "#f3f4f6", "#8a9099")
    b += line_svg(370, 255, 468, 275, dash=True)
    b += line_svg(370, 355, 468, 375, dash=True)
    b += ('<text x="40" y="440" font-size="13" fill="#4c5560">Linha cheia: alterado e verificado na Fase 5 (navgraph 13/13, IA 40,4 km/h máx.). '
          'Tracejado: deve convergir, ainda não alterado.</text>')
    return write_svg("pipeline", "fig_15_sign_to_logic.svg", b, 860, 455)


if __name__ == "__main__":
    for fn in (fig_aerial, fig_heatmaps, fig_atlas, fig_stop_zoom, fig_stop_ingame, fig_vfs, fig_poc_onoff, fig_alpha,
               fig_roadmarkings_atlas, fig_roadmarkings_top, fig_qa_pipeline, fig_qa_point, fig_speed_conversion,
               fig_speed_distribution, fig_sign_logic, fig_yield_ingame, fig_r19_asset, fig_port_bay, fig_r19_ingame,
               fig_gantry, fig_pavement_state):
        fn()
