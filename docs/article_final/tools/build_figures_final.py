"""Final article (v1.0.0): builds every figure from real evidence.

Inputs (never modified):
  docs/article_final/figures/raw/*        captures of the final article (capture_final.py, release ZIP only) + navgraph dumps
  docs/article/figures/**                 figures and raw captures of the first article (Phase 5.5 snapshot), reused with
                                          provenance recorded in FIGURE_INDEX_FINAL.md
  tests/screenshots/{phase6,phase7,release}/...   QA captures of Phases 6, 7 and 9 (catalog cameras)
  tests/reports/phase7/radar_test.json, tests/reports/release/release_smoke.json
  source/originals/png, working/png, mod/traducao_ptbr_wcusa (meshes)
Outputs: docs/article_final/figures/{comparisons,textures,functional,validation,qa,release,diagrams,final}/
Only crops, side-by-side composition, labels, arrows and charts drawn from data (Pillow / hand-written SVG). No generative
editing. Captures of 1920x1080 and 1920x993 with the same vertical FOV are brought to a common 1765x993 frame
(the 1080 image is scaled by 993/1080, the 993 image is centre-cropped), so the same camera gives the same framing.

    python docs/article_final/tools/build_figures_final.py [name ...]
"""
import json
import math
import os
import shutil
import sys
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ART, "..", ".."))
RAW = os.path.join(ART, "figures", "raw")
FIG = os.path.join(ART, "figures")
OLD = os.path.join(REPO, "docs", "article", "figures")
SHOTS = os.path.join(REPO, "tests", "screenshots")
FONTS = r"C:\Windows\Fonts"

INK = (28, 32, 38)
MUTED = (96, 104, 114)
WHITE = (255, 255, 255)
RED = (214, 40, 40)
BLUE = (29, 99, 196)
ORANGE = (230, 120, 20)
GREEN = (20, 140, 70)
CYAN = (0, 200, 220)


def font(size, bold=False):
    for name in (("segoeuib.ttf" if bold else "segoeui.ttf"), ("arialbd.ttf" if bold else "arial.ttf")):
        p = os.path.join(FONTS, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def p(*parts):
    return os.path.join(REPO, *parts)


def load(path):
    return Image.open(path).convert("RGB")


def common(img):
    """1920x1080 and 1920x993 captures (vertical FOV fixed) -> the same 1765x993 field of view."""
    if img.height == 1080:
        return img.resize((round(1920 * 993 / 1080), 993), Image.LANCZOS)
    if img.height == 993:
        x0 = (1920 - 1765) // 2
        return img.crop((x0, 0, x0 + 1765, 993))
    return img


def raw(name):
    return load(os.path.join(RAW, name))


def shot(*parts):
    return load(os.path.join(SHOTS, *parts))


def save(img, sub, name, quality=90):
    os.makedirs(os.path.join(FIG, sub), exist_ok=True)
    path = os.path.join(FIG, sub, name)
    if name.endswith(".jpg"):
        img.convert("RGB").save(path, quality=quality, optimize=True)
    else:
        img.save(path, optimize=True)
    print(f"{os.path.relpath(path, REPO)}  {img.size[0]}x{img.size[1]}  {os.path.getsize(path) / 1e6:.2f} MB")
    return path


def reuse(src_rel, sub, name):
    """Copy a figure of the first article unchanged (historical fact; provenance in FIGURE_INDEX_FINAL.md)."""
    os.makedirs(os.path.join(FIG, sub), exist_ok=True)
    dst = os.path.join(FIG, sub, name)
    shutil.copyfile(os.path.join(OLD, src_rel), dst)
    print(f"{os.path.relpath(dst, REPO)}  (reused docs/article/figures/{src_rel})")
    return dst


def titled(img, letter, title, bar=58, size=26):
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


def row(panels, gap=18, bg=WHITE):
    h = max(pn.height for pn in panels)
    w = sum(pn.width for pn in panels) + gap * (len(panels) - 1)
    out = Image.new("RGB", (w, h), bg)
    x = 0
    for pn in panels:
        out.paste(pn, (x, 0))
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


def fit(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


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


def arrow(d, a, b, color, width=5, head=18):
    d.line([a, b], fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (-1, 1):
        d.line([b, (b[0] - head * math.cos(ang + s * 0.45), b[1] - head * math.sin(ang + s * 0.45))], fill=color, width=width)


def note(width, text, size=21):
    img = Image.new("RGB", (width, size * 2 + 14), WHITE)
    ImageDraw.Draw(img).text((4, 8), text, fill=MUTED, font=font(size))
    return img


# ===================================================================== reused figures of the first article
def fig_reused():
    reuse("validation/fig_02_heatmap_t_roadsigns_legacy_vs_phase5.jpg", "validation", "heatmap_legacy_vs_phase5.jpg")
    reuse("textures/fig_04_stop_uv_region_zoom.png", "textures", "stop_uv_region_zoom.png")
    reuse("textures/fig_08_alpha_loss_legacy.png", "textures", "alpha_loss_legacy.png")
    reuse("comparisons/fig_07_poc_override_on_off_on.jpg", "comparisons", "poc_override_on_off_on.jpg")
    reuse("textures/fig_09_roadmarkings_atlas_slots.png", "textures", "roadmarkings_atlas_slots.png")
    reuse("textures/fig_17_r19_texture_and_mask.png", "textures", "r19_texture_and_mask.png")
    reuse("validation/fig_18_port_bay_plate_side_effect.jpg", "validation", "port_bay_plate_side_effect.jpg")


# ===================================================================== opening
def fig_opening():
    img = common(raw("chinatown_driver_a__on_opening.png"))
    d = ImageDraw.Draw(img)
    s = 993 / 1080
    sign, paint = (1034 * s, 464 * s), (896 * s, 598 * s)
    arrow(d, (sign[0] + 150, sign[1] - 120), (sign[0] + 22, sign[1] - 18), RED)
    label_box(d, (sign[0] + 150, sign[1] - 190), "R-1 PARE", bg=RED, size=30)
    arrow(d, (paint[0] - 250, paint[1] + 120), (paint[0] - 60, paint[1] + 12), BLUE)
    label_box(d, (paint[0] - 520, paint[1] + 110), "PARE no pavimento", bg=BLUE, size=30)
    return save(img, "final", "opening_chinatown_v100.jpg")


def fig_day_night_opening():
    a = common(raw("chinatown_driver_a__on_opening.png"))
    b = common(raw("chinatown_driver_a__on_night.png"))
    box = (430, 200, 1450, 760)
    return save(pad(row([titled(a.crop(box), "A", "1.0.0, dia"), titled(b.crop(box), "B", "1.0.0, noite")])),
                "final", "chinatown_day_night_v100.jpg")


# ===================================================================== in-game comparisons
def fig_stop_original_poc_v100():
    old = lambda n: common(load(os.path.join(OLD, "raw", n)))
    box = (513, 280, 1253, 920)
    a = common(raw("roadsigns_chinatown_stop__off_day.png")).crop(box)
    b = old("roadsigns_chinatown_stop__poc.png").crop(box)
    c = common(raw("roadsigns_chinatown_stop__on_day.png")).crop(box)
    return save(pad(row([titled(a, "A", "Original (ZIP desativado)"), titled(b, "B", "PoC da Fase 1 (30/09)"),
                         titled(c, "C", "Versão 1.0.0 (só o ZIP)")])), "comparisons", "stop_original_poc_v100.jpg")


def fig_r2():
    old = lambda n: common(load(os.path.join(OLD, "raw", n)))
    box = (543, 170, 1223, 790)
    a = common(raw("roadsigns_downtown_yield__off_day.png")).crop(box)
    b = old("roadsigns_downtown_yield__poc.png").crop(box)
    c = common(raw("roadsigns_downtown_yield__on_day.png")).crop(box)
    return save(pad(row([titled(a, "A", "Original: YIELD"), titled(b, "B", "Referência antiga (descartada)"),
                         titled(c, "C", "1.0.0: R-2 sem legenda")])), "comparisons", "r2_original_legacy_v100.jpg")


def fig_roadmarkings_ingame():
    k_off = common(raw("decal_keep_clear_top__off_day.png"))
    k_on = common(raw("decal_keep_clear_top__on_day.png"))
    b_off = common(load(os.path.join(OLD, "raw", "decal_bus_only_top__original.png")))
    b_on = common(raw("decal_bus_only_top__on_day.png"))
    s_off = common(raw("decal_stop_chinatown_oblique__off_day.png"))
    s_on = common(raw("decal_stop_chinatown_oblique__on_day.png"))
    w = 760
    rows = [
        row([titled(fit(k_off, w), "A", "KEEP CLEAR (original)"), titled(fit(k_on, w), "B", "NÃO BLOQUEIE (1.0.0)")]),
        row([titled(fit(b_off, w), "C", "BUS ONLY (original, 02/10)"), titled(fit(b_on, w), "D", "ÔNIBUS (1.0.0)")]),
        row([titled(fit(s_off, w), "E", "STOP (original)"), titled(fit(s_on, w), "F", "PARE (1.0.0)")]),
    ]
    return save(pad(col(rows)), "comparisons", "roadmarkings_ingame_original_v100.jpg")


def fig_roadmarkings_opacity():
    o = Image.open(p("source", "originals", "png", "decalroad", "t_decal_roadmarkings_o.data.png")).convert("L") \
        if os.path.exists(p("source", "originals", "png", "decalroad", "t_decal_roadmarkings_o.data.png")) else None
    if o is None:
        cands = [os.path.join(dp, f) for dp, _, fs in os.walk(p("source", "originals", "png")) for f in fs
                 if f == "t_decal_roadmarkings_o.data.png"]
        o = Image.open(sorted(cands)[0]).convert("L")
    n = Image.open(p("working", "png", "t_decal_roadmarkings_o.data.png")).convert("L")
    if o.size != n.size:
        o = o.resize(n.size, Image.LANCZOS)
    s = 640
    a, b = o.resize((s, s), Image.LANCZOS).convert("RGB"), n.resize((s, s), Image.LANCZOS).convert("RGB")
    for img in (a, b):
        d = ImageDraw.Draw(img)
        for i in range(1, 4):
            d.line([(i * s / 4, 0), (i * s / 4, s)], fill=(0, 160, 220), width=2)
            d.line([(0, i * s / 4), (s, i * s / 4)], fill=(0, 160, 220), width=2)
    return save(pad(row([titled(a, "A", "_o.data original (opacidade)"), titled(b, "B", "_o.data 1.0.0")])),
                "textures", "roadmarkings_opacity_original_v100.png")


def fig_r19_values():
    tiles = []
    for v in (10, 40, 50, 70, 120):
        t = Image.open(p("working", "png", "r19", f"t_r19_{v}_b.color.png")).convert("RGB")
        # the panel is 0.7317 x 1 m on a 512 x 1024 texture: texels are not square. Crop around the disc centre
        # (white field measured at x 54-457, y 215-808) and rescale to the physical aspect so the disc is round.
        kx = (0.7317 / 512) / (1 / 1024)
        half = t.width * kx / 2
        cy = (215 + 808) / 2
        t = t.crop((0, int(cy - half), t.width, int(cy + half))).resize((round(t.width * kx), round(2 * half)), Image.LANCZOS)
        tiles.append(titled(t.resize((260, 260), Image.LANCZOS), "", f"R-19 {v}", bar=44, size=24))
    return save(pad(row(tiles)), "textures", "r19_values_10_to_120.png")


def fig_speed_limit_to_r19():
    box = (590, 0, 1110, 993)
    a = common(raw("r19_40_hill__off_day.png")).crop(box)
    b = common(raw("r19_40_hill__on_day.png")).crop(box)
    sp = lambda n: shot("phase7", "speed_plates", n)
    c, d = sp("reg_02_original.jpg"), sp("reg_02_ptbr.jpg")
    e, f = sp("adv_00_original.jpg"), sp("adv_00_ptbr.jpg")
    h = a.height
    sq = lambda im: fit(im.crop(((im.width - im.height) // 2, 0, (im.width + im.height) // 2, im.height)), h // 2 - 40)
    top = row([titled(a, "A", "STOP + SPEED LIMIT 25"), titled(b, "B", "PARE + R-19 40")])
    side = col([row([titled(sq(c), "C", "70 mph (embutida)"), titled(sq(d), "D", "R-19 = via (120)")]),
                row([titled(sq(e), "E", "advertência MPH"), titled(sq(f), "F", "advertência km/h")])])
    return save(pad(row([top, side])), "comparisons", "speed_limit_to_r19.jpg")


def fig_toll_booth():
    a = shot("phase7", "toll_booth", "toll_booth_close_original.jpg")
    b = shot("phase7", "toll_booth", "toll_booth_close_ptbr.jpg")
    return save(pad(row([titled(fit(a, 900), "A", "DO NOT STOP / SPEED LIMIT 25"), titled(fit(b, 900), "B", "NÃO PARE / R-19 40")])),
                "functional", "toll_booth_original_v100.jpg")


def pair_release(phase6_family, loc, title_a, title_b, night=False, box=None, width=860):
    a = common(shot("phase6", phase6_family, f"{loc}_original{'_night' if night else ''}.jpg"))
    b = common(shot("release", "on", f"{loc}_{'night' if night else 'day'}.jpg"))
    if box:
        a, b = a.crop(box), b.crop(box)
    return [titled(fit(a, width), "", title_a), titled(fit(b, width), "", title_b)]


def lettered(panels, start="A"):
    out = []
    for i, pn in enumerate(panels):
        d = ImageDraw.Draw(pn)
        d.rectangle([0, 8, 42, 50], fill=INK)
        L = chr(ord(start) + i)
        tw = d.textlength(L, font=font(26, True))
        d.text(((42 - tw) / 2, 13), L, fill=WHITE, font=font(26, True))
        out.append(pn)
    return out


def shift_titles(panels):
    """titled(..., '', title) leaves the title at x=0; move it right of the letter box."""
    out = []
    for pn in panels:
        img = Image.new("RGB", pn.size, WHITE)
        img.paste(pn.crop((0, 58, pn.width, pn.height)), (0, 58))
        top = pn.crop((0, 0, pn.width - 54, 58))
        img.paste(top, (54, 0))
        out.append(img)
    return lettered(out)


def fig_fuel_day_night():
    a = common(shot("phase6", "eca_genericsigns", "gs_octane_pump_original.jpg"))
    b = common(shot("release", "on", "gs_octane_pump_day.jpg"))
    c = common(shot("release", "on", "gs_octane_pump_night.jpg"))
    box = (380, 0, 1385, 993)
    ps = [titled(fit(x.crop(box), 620), "", t) for x, t in ((a, "Original"), (b, "1.0.0, dia"), (c, "1.0.0, noite"))]
    return save(pad(row(shift_titles(ps))), "comparisons", "fuel_pump_original_day_night.jpg")


def fig_billboard():
    a = common(shot("phase6", "t_billboards", "bb_turbo_burger_original.jpg"))
    b = common(shot("release", "on", "bb_turbo_burger_day.jpg"))
    c = common(shot("release", "on", "bb_turbo_burger_night.jpg"))
    ps = [titled(fit(x, 620), "", t) for x, t in ((a, "Original"), (b, "1.0.0, dia"), (c, "1.0.0, noite"))]
    return save(pad(row(shift_titles(ps))), "comparisons", "billboard_turbo_burger.jpg")


def fig_industry():
    ps = []
    for fam, loc, t1, t2 in (("ind_industrial_signs", "ind_in_flam_no", "Original", "1.0.0"),
                             ("t_spearleaf_refinery_logo", "t_spea_refinery", "Original", "1.0.0"),
                             ("t_steel_factory_brand", "t_stee_steel_descriptor", "Original", "1.0.0")):
        ps += pair_release(fam, loc, t1, t2, width=620)
    ps = shift_titles(ps)
    img = col([row(ps[i:i + 2]) for i in range(0, 6, 2)])
    return save(pad(img), "comparisons", "industry_original_v100.jpg")


def fig_transport():
    a, b = pair_release("t_bus_routes_wca", "bus_map_shelter", "Original", "1.0.0", width=700)
    c = common(shot("phase6", "glyph_signs", "gl_s_busstop_wcu_mapa_original.jpg"))
    d = common(shot("phase6", "glyph_signs", "gl_s_busstop_wcu_mapa_ptbr.jpg"))
    ps = shift_titles([a, b, titled(fit(c, 700), "", "MAP (glifos, original)"), titled(fit(d, 700), "", "MAPA (glifos, Fase 6)")])
    return save(pad(col([row(ps[:2]), row(ps[2:])])), "comparisons", "transport_bus_map.jpg")


def fig_commercial():
    a = common(shot("phase6", "clutter_commercial", "cc_neon_nails_original_night.jpg"))
    b = common(shot("release", "on", "cc_neon_nails_night.jpg"))
    c = common(shot("phase6", "clutter_commercial", "cc_lemon_original.jpg"))
    d = common(shot("phase6", "clutter_commercial", "cc_lemon_ptbr.jpg"))
    ps = shift_titles([titled(fit(a, 700), "", "Néon original (noite)"), titled(fit(b, 700), "", "1.0.0 (noite)"),
                       titled(fit(c, 700), "", "GOT A LEMON? (original)"), titled(fit(d, 700), "", "TEM UMA BOMBA? (Fase 6)")])
    return save(pad(col([row(ps[:2]), row(ps[2:])])), "comparisons", "commercial_neon_lemon.jpg")


def fig_glyph_examples():
    pairs = [("gl_motel_sign_motel", "MOTEL → POUSADA"), ("gl_food_mart_sign_001_delifoodmart", "DELI & FOOD MART → LANCHES & MERCADO"),
             ("gl_roadsigns_rs_frac_half_0_9", "½ MILE → 800 m (pórtico)")]
    rows = []
    for loc, t in pairs:
        a = common(shot("phase6", "glyph_signs", f"{loc}_original.jpg"))
        b = common(shot("phase6", "glyph_signs", f"{loc}_ptbr.jpg"))
        rows.append(row([titled(fit(a, 620), "", "Original"), titled(fit(b, 620), "", t)]))
    flat = shift_titles([pn for r in rows for pn in (r.crop((0, 0, 620, r.height)), r.crop((638, 0, r.width, r.height)))])
    return save(pad(col([row(flat[i:i + 2]) for i in range(0, len(flat), 2)])), "comparisons", "glyph_signs_examples.jpg")


def fig_glyph_explained():
    sys.path.insert(0, p("tools", "production"))
    import glyph_signs as G
    orig = p("source", "originals", "meshes", "phase6", "west_coast_usa", "levels", "west_coast_usa", "art", "shapes",
             "buildings", "s_motel_sign.dae")
    new = p("mod", "traducao_ptbr_wcusa", "levels", "west_coast_usa", "art", "shapes", "buildings", "s_motel_sign.dae")
    at_o = np.asarray(Image.open(p("source", "originals", "png", "art_shapes", "clutter_commercial_b.color.png")).convert("RGB"))
    op_o = np.asarray(Image.open(p("source", "originals", "png", "art_shapes", "clutter_commercial_o.data.png")).convert("L"))
    at_n = np.asarray(Image.open(p("working", "png", "art_shapes", "clutter_commercial_b.color.png")).convert("RGB"))
    op_n = np.asarray(Image.open(p("working", "png", "art_shapes", "clutter_commercial_o.data.png")).convert("L"))
    qo = G.read_quads(orig)
    qn = G.read_quads(new)
    n, r, u = G.front_basis(qo)
    img_o, _ = G.render(qo, n, r, u, scale=300, atlas=at_o, opacity=op_o)
    img_n, _ = G.render(qn, n, r, u, scale=300, atlas=at_n, opacity=op_n)
    # atlas cells sampled by the quads of the original sign: union box of their UV rects
    rects = np.array([q["rect"] for q in qo])
    x0, y0 = rects[:, 0].min() - 20, rects[:, 1].min() - 20
    x1, y1 = rects[:, 2].max() + 20, rects[:, 3].max() + 20
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    crop = Image.fromarray(at_o).crop((x0, y0, int(x1), int(y1)))
    opc = Image.fromarray(op_o).crop((x0, y0, int(x1), int(y1)))
    bg = Image.new("RGB", crop.size, (60, 64, 70))
    bg.paste(crop, mask=opc)
    d = ImageDraw.Draw(bg)
    for q in qo:
        a, b, c, e = q["rect"]
        d.rectangle([a - x0, b - y0, c - x0, e - y0], outline=CYAN, width=2)
    k = min(3.0, 700 / max(bg.size))
    bg = bg.resize((int(bg.width * k), int(bg.height * k)), Image.NEAREST)
    H = 420
    pa = titled(fit(bg, int(bg.width * H / bg.height)) if bg.height > H else bg, "A", "Atlas clutter_commercial: células usadas pela placa")
    pb = titled(img_o.resize((int(img_o.width * H / img_o.height), H)), "B", f"Original ({len(qo)} quads)")
    pc = titled(img_n.resize((int(img_n.width * H / img_n.height), H)), "C", f"1.0.0 ({len(qn)} quads)")
    return save(pad(col([pa, row([pb, pc])])), "textures", "glyph_sign_motel_explained.png")


def fig_adas():
    # The release smoke screenshots of the ADAS scenario (tests/screenshots/release/on/adas/) show the game main menu over the
    # scene and are not used; the functional result of that run came from the controller counters. Phase 7 captures are used.
    a = shot("phase7", "adas", "speed_alert_spawn.jpg")
    b = shot("release", "on", "signs", "r19_50_spawn_left.jpg")
    c = shot("phase7", "adas", "mod_off_event01_entry.jpg")
    e = shot("phase7", "adas", "mod_on_event01_entry.jpg")
    w = 780
    ps = shift_titles([titled(fit(a, w), "", "Speed Alert: visão do participante no início"),
                       titled(fit(b, w), "", "R-19 50 no início da zona (ZIP 1.0.0)"),
                       titled(fit(c, w), "", "Event 01: entrada do corredor, mod desligado"),
                       titled(fit(e, w), "", "Event 01: entrada do corredor, R-19 70")])
    return save(pad(col([row(ps[:2]), row(ps[2:])])), "functional", "adas_speed_alert_event01.jpg")


def fig_mod_off():
    pairs = [("chinatown_driver_a", (430, 200, 1450, 760)), ("r19_40_hill", (590, 0, 1110, 993)), ("decal_keep_clear_top", None)]
    cols_ = []
    for name, box in pairs:
        a = common(raw(f"{name}__off_day.png"))
        b = common(raw(f"{name}__on_{'opening' if name == 'chinatown_driver_a' else 'day'}.png"))
        if box:
            a, b = a.crop(box), b.crop(box)
        h = 360
        cols_.append(col([titled(fit(a, int(a.width * h / a.height)), "", "ZIP desativado"),
                          titled(fit(b, int(b.width * h / b.height)), "", "ZIP ativo")]))
    img = row(cols_)
    return save(pad(img), "release", "mod_off_on_reversibility.jpg")


# ===================================================================== data figures (navgraph)
CLASS_COLORS = {10: (120, 40, 160), 30: (190, 196, 204), 40: (30, 120, 220), 50: (20, 170, 160), 60: (40, 160, 60),
                70: (240, 170, 0), 80: (240, 110, 20), 100: (210, 40, 40), 120: (120, 20, 30)}


def nav(state):
    return json.load(open(os.path.join(RAW, f"navgraph_edges__{state}.json"), encoding="utf-8"))["edges"]


def fig_speed_map():
    edges = nav("on")
    off = {}
    for e in nav("off"):
        off[tuple(sorted([(round(e[0]), round(e[1])), (round(e[2]), round(e[3]))]))] = e[4]
    xs = [v for e in edges for v in (e[0], e[2])]
    ys = [v for e in edges for v in (e[1], e[3])]
    lo_x, hi_x, lo_y, hi_y = min(xs) - 40, max(xs) + 40, min(ys) - 40, max(ys) + 40
    S = 2600 / max(hi_x - lo_x, hi_y - lo_y)
    W, H = int((hi_x - lo_x) * S), int((hi_y - lo_y) * S)
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    tp = lambda x, y: ((x - lo_x) * S, (hi_y - y) * S)
    order = sorted(edges, key=lambda e: (e[4] != 30, e[4]))
    for e in order:
        v = e[4]
        k = min(CLASS_COLORS, key=lambda c: abs(c - v))
        key = tuple(sorted([(round(e[0]), round(e[1])), (round(e[2]), round(e[3]))]))
        changed = key in off and abs(off[key] - v) > 0.05
        width = 7 if changed else (2 if v == 30 else 3)
        d.line([tp(e[0], e[1]), tp(e[2], e[3])], fill=CLASS_COLORS[k], width=width)
    # representative points (navgraph matrix of Phase 7, re-read on the release ZIP in Phase 9)
    sys.path.insert(0, p("working", "functional"))
    import navgraph_matrix as N
    seen = set()
    for kmh, label, x, y, *_ in N.POINTS:
        if kmh in seen:
            continue
        seen.add(kmh)
        cx, cy = tp(x, y)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=INK, width=5, fill=WHITE)
        label_box(d, (cx + 22, cy - 18), f"{kmh}", bg=CLASS_COLORS[kmh] if kmh not in (30,) else MUTED, size=34)
    # legend
    lx, ly = 40, 40
    d.rectangle([lx - 16, ly - 16, lx + 470, ly + 46 * (len(CLASS_COLORS) + 2) + 10], fill=WHITE, outline=INK, width=2)
    d.text((lx, ly), "Limite no navgraph (km/h), 1.0.0", fill=INK, font=font(30, True))
    for i, (k, c) in enumerate(CLASS_COLORS.items()):
        y = ly + 50 + i * 46
        d.line([(lx, y + 18), (lx + 70, y + 18)], fill=c, width=10)
        d.text((lx + 90, y), f"{k}" + (" (automático do jogo)" if k == 30 else ""), fill=INK, font=font(28))
    y = ly + 50 + len(CLASS_COLORS) * 46
    d.line([(lx, y + 18), (lx + 70, y + 18)], fill=INK, width=7)
    d.text((lx + 90, y), "traço grosso: valor mudou com o mod", fill=INK, font=font(26))
    img = img.resize((W // 2, H // 2), Image.LANCZOS)
    return save(img, "functional", "speed_map_navgraph_v100.png")


def svg_head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            'font-family="Segoe UI, Arial, sans-serif"><rect width="100%" height="100%" fill="#ffffff"/>'
            '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#1c2026"/></marker></defs>')


def write_svg(sub, name, body, w, h):
    os.makedirs(os.path.join(FIG, sub), exist_ok=True)
    path = os.path.join(FIG, sub, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_head(w, h) + body + "</svg>\n")
    print(f"{os.path.relpath(path, REPO)}  svg")
    return path


def box_svg(x, y, w, h, title, sub="", fill="#eef3fb", stroke="#1d63c4", tsize=17, ssize=13):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    lines = sub.split("\n") if sub else []
    ty = y + (h / 2 + 6 if not lines else h / 2 - 4 - (len(lines) - 1) * ssize * 0.6)
    s += f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" font-size="{tsize}" font-weight="700" fill="#1c2026">{esc(title)}</text>'
    for i, line in enumerate(lines):
        s += f'<text x="{x + w / 2}" y="{ty + 20 + i * (ssize + 4)}" text-anchor="middle" font-size="{ssize}" fill="#4c5560">{esc(line)}</text>'
    return s


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line_svg(x1, y1, x2, y2, dash=False):
    da = ' stroke-dasharray="6,5"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1c2026" stroke-width="2"{da} marker-end="url(#ah)"/>'


def text_svg(x, y, t, size=14, weight="400", fill="#4c5560", anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>'


def fig_navgraph_hist():
    on, off = Counter(e[4] for e in nav("on")), Counter(e[4] for e in nav("off"))
    cats = sorted(set(on) | set(off))
    W, H, x0, y0 = 1000, 430, 80, 340
    mx = 3400
    b = text_svg(20, 28, f"Arestas do navgraph por limite: original ({sum(off.values()):,} arestas) × 1.0.0 ({sum(on.values()):,})".replace(",", "."), 16, "700", "#1c2026")
    for t in (0, 1000, 2000, 3000):
        y = y0 - t / mx * 270
        b += f'<line x1="{x0}" y1="{y}" x2="{W - 20}" y2="{y}" stroke="#e3e6ea"/>'
        b += text_svg(x0 - 8, y + 4, f"{t:,}".replace(",", "."), 12, anchor="end")
    gw = (W - 20 - x0) / len(cats)
    for i, c in enumerate(cats):
        gx = x0 + i * gw
        for j, (cnt, fill) in enumerate(((off.get(c, 0), "#e67814" if c % 10 else "#9aa3ad"), (on.get(c, 0), "#1d63c4"))):
            hgt = max(1.5, cnt / mx * 270) if cnt else 0
            x = gx + 6 + j * (gw / 2 - 4)
            b += f'<rect x="{x}" y="{y0 - hgt}" width="{gw / 2 - 8}" height="{hgt}" fill="{fill}"/>'
            if cnt:
                b += text_svg(x + (gw / 2 - 8) / 2, y0 - hgt - 5, f"{cnt:,}".replace(",", "."), 11, anchor="middle", fill="#1c2026")
        b += text_svg(gx + gw / 2, y0 + 20, f"{c:g}".replace(".", ","), 13, "700", "#1c2026", "middle")
    b += text_svg(x0, y0 + 46, "km/h", 12)
    b += (f'<rect x="{x0}" y="{y0 + 60}" width="14" height="14" fill="#9aa3ad"/>' + text_svg(x0 + 20, y0 + 72, "original, valor métrico", 13)
          + f'<rect x="{x0 + 200}" y="{y0 + 60}" width="14" height="14" fill="#e67814"/>' + text_svg(x0 + 220, y0 + 72, "original, herdado de mph", 13)
          + f'<rect x="{x0 + 420}" y="{y0 + 60}" width="14" height="14" fill="#1d63c4"/>' + text_svg(x0 + 440, y0 + 72, "versão 1.0.0 (só múltiplos de 10)", 13))
    return write_svg("functional", "navgraph_histogram_original_v100.svg", b, W, H)


def fig_radar_chart():
    data = json.load(open(p("tests", "reports", "phase7", "radar_test.json"), encoding="utf-8"))
    rel = json.load(open(p("tests", "reports", "release", "release_smoke.json"), encoding="utf-8")).get("radar", [])
    runs = [(r["radar"], r["limit_kmh"], r["trigger_above_kmh"], r["speed_at_radar_kmh"], r["triggered"], "7") for r in data.values()]
    runs += [(r["radar"], r["limit_kmh"], r["trigger_above_kmh"], r["speed_at_radar_kmh"], r["triggered"], "9") for r in rel]
    W, H, x0, y0 = 1000, 500, 150, 60
    vmin, vmax = 40, 130
    sx = lambda v: x0 + (v - vmin) / (vmax - vmin) * (W - x0 - 40)
    b = text_svg(20, 28, "Radares: velocidade medida na passagem × limite e limiar de disparo (limite + 10 %)", 16, "700", "#1c2026")
    for v in range(40, 131, 10):
        b += f'<line x1="{sx(v)}" y1="{y0}" x2="{sx(v)}" y2="{H - 90}" stroke="#eef0f2"/>' + text_svg(sx(v), H - 72, str(v), 12, anchor="middle")
    b += text_svg(sx(85), H - 50, "km/h no gatilho", 13, anchor="middle")
    radars = sorted({r[0] for r in runs})
    rh = (H - 90 - y0) / len(radars)
    for i, rid in enumerate(radars):
        y = y0 + i * rh + rh / 2
        rr = [r for r in runs if r[0] == rid]
        lim, thr = rr[0][1], rr[0][2]
        b += text_svg(20, y + 5, f"radar {rid} ({lim} km/h)", 14, "700", "#1c2026")
        b += f'<line x1="{sx(lim)}" y1="{y - rh / 2 + 6}" x2="{sx(lim)}" y2="{y + rh / 2 - 6}" stroke="#1c2026" stroke-width="2"/>'
        b += f'<rect x="{sx(lim)}" y="{y - rh / 2 + 6}" width="{sx(thr) - sx(lim)}" height="{rh - 12}" fill="#fff1d6"/>'
        b += f'<line x1="{sx(thr)}" y1="{y - rh / 2 + 6}" x2="{sx(thr)}" y2="{y + rh / 2 - 6}" stroke="#d62828" stroke-width="2" stroke-dasharray="5,4"/>'
        for k, r in enumerate(rr):
            dy = (k % 3 - 1) * 9
            fill = "#d62828" if r[4] else "#148c46"
            shape = (f'<circle cx="{sx(r[3])}" cy="{y + dy}" r="7" fill="{fill}" stroke="#ffffff" stroke-width="1.5"/>' if r[5] == "7"
                     else f'<rect x="{sx(r[3]) - 7}" y="{y + dy - 7}" width="14" height="14" fill="{fill}" stroke="#ffffff" stroke-width="1.5"/>')
            b += shape
    ly = H - 8
    b += (f'<circle cx="160" cy="{ly - 4}" r="7" fill="#148c46"/>' + text_svg(172, ly, "não disparou", 12)
          + f'<circle cx="280" cy="{ly - 4}" r="7" fill="#d62828"/>' + text_svg(292, ly, "disparou", 12)
          + text_svg(370, ly, "● Fase 7 (mod de desenvolvimento)   ■ Fase 9 (ZIP de release)   faixa amarela: tolerância", 12))
    return write_svg("functional", "radar_trigger_chart.svg", b, W, H)


# ===================================================================== diagrams
def fig_problem_expansion():
    steps = [("Texto", "palavra na imagem"), ("Atlas", "muitas placas numa textura"), ("UV", "região fixa por vértice"),
             ("Alfa", "recorte por alphaTest"), ("Material", "mapas auxiliares"), ("Malha", "letras como quads"),
             ("Navgraph", "limite em m/s"), ("Radar / zonas", "fiscalização e dados"), ("ADAS", "cenários de pesquisa"),
             ("QA / release", "prova reproduzível")]
    b = text_svg(20, 28, "Como o problema cresceu: da troca de palavras à coerência do mundo simulado", 16, "700", "#1c2026")
    w, h, gx = 170, 74, 22
    for i, (t, s) in enumerate(steps):
        r, c = divmod(i, 5)
        x = 20 + (c if r == 0 else 4 - c) * (w + gx)
        y = 50 + r * (h + 60)
        fill, st = (("#eef3fb", "#1d63c4") if i < 3 else ("#fff7e8", "#e67814") if i < 6 else ("#eaf6ee", "#148c46") if i < 9
                    else ("#f3f4f6", "#1c2026"))
        b += box_svg(x, y, w, h, t, s, fill, st, 17, 12)
        if i < len(steps) - 1:
            if i == 4:
                b += line_svg(x + w / 2, y + h, x + w / 2, y + h + 58)
            elif r == 0:
                b += line_svg(x + w, y + h / 2, x + w + gx - 2, y + h / 2)
            else:
                b += line_svg(x, y + h / 2, x - gx + 2, y + h / 2)
    b += text_svg(20, 300, "Azul: Fases 0–5 (gráfico). Laranja: Fases 5–6 (material e malha). Verde: Fase 7 (funcional). Cinza: Fases 8–9.", 13)
    return write_svg("diagrams", "problem_expansion.svg", b, 990, 315)


def fig_vfs_release():
    b = ""
    b += box_svg(270, 20, 460, 70, "BeamNG pede um caminho virtual", "/assets/materials/signage/roadsigns/t_roadsigns_b.color.dds", "#f3f4f6", "#1c2026")
    b += box_svg(270, 130, 460, 64, "Sistema de arquivos virtual (VFS)", "monta os zips do jogo e os mods ativos; o mod tem precedência", "#fff7e8", "#e67814")
    b += line_svg(500, 90, 500, 128)
    b += line_svg(430, 194, 230, 246)
    b += line_svg(570, 194, 770, 246)
    b += box_svg(20, 248, 440, 120, "MOD ATIVO (1.0.0)", "mods/traducao_ptbr_wcusa_v1.0.0.zip\n→ assets/.../t_roadsigns_b.color.dds\nPARE; 116/116 arquivos de runtime vêm do ZIP", "#eaf6ee", "#148c46")
    b += box_svg(540, 248, 440, 120, "MOD DESATIVADO", "content/assets/materials/signage.zip\n(instalação, só leitura)\nSTOP; 0/116 vêm do ZIP", "#fbeaea", "#d62828")
    b += text_svg(500, 400, "Mesmo nome e mesmo caminho: material e malha do jogo não mudam; só a origem do arquivo (MCP file_info → realPath).", 13, anchor="middle")
    b += text_svg(500, 420, "Fase 1: pasta unpacked com 1 textura. Fase 9: ZIP de release com 117 arquivos, conferido arquivo a arquivo.", 13, anchor="middle")
    return write_svg("diagrams", "vfs_override_release.svg", b, 1000, 435)


def fig_state_protocol():
    steps = [("Trocar o mod", "core_modmanager:\nactivate / deactivate"), ("Carregar smallgrid", "libera texturas,\nshapes e dados"),
             ("Carregar West Coast", "~70–85 s"), ("Preset de ambiente", "hora, sol fixo,\nvento 0, céu limpo"),
             ("Câmera do catálogo", "pose salva (posição,\nquaternion, FOV)"), ("Captura + VFS + log", "file_info, get_logs")]
    b = text_svg(20, 28, "Protocolo de troca de estado no QA (consolidado nas Fases 5–9)", 16, "700", "#1c2026")
    w, h, gx = 150, 92, 14
    for i, (t, s) in enumerate(steps):
        x = 20 + i * (w + gx)
        b += box_svg(x, 50, w, h, t, s, "#eef3fb" if i < 3 else "#eaf6ee", "#1d63c4" if i < 3 else "#148c46", 14, 11)
        if i < len(steps) - 1:
            b += line_svg(x + w, 96, x + w + gx - 1, 96)
    b += box_svg(20, 172, 470, 92, "Cache que sobrevive ao mod (Fase 5)", "recarregar o MESMO mapa mantém textura e dados;\num .dae mais novo que o .cdae é recompilado em\ncurrent/temp e continua valendo com o mod desligado", "#fbeaea", "#d62828", 15, 12)
    b += box_svg(510, 172, 470, 92, "Resposta adotada", "trocar de mapa a cada mudança de estado;\ndistribuir o .cdae compilado pelo jogo, com data\nposterior à do .dae (no ZIP: +2 min)", "#eaf6ee", "#148c46", 15, 12)
    return write_svg("diagrams", "qa_state_protocol.svg", b, 1000, 280)


def fig_master():
    b = text_svg(20, 28, "Do arquivo editado à mão ao asset reproduzível", 16, "700", "#1c2026")
    ins = [("Original do jogo", "SHA-256 no manifesto"), ("Regiões com evidência", "UV de malhas instanciadas,\ntextureCoords de decalques"),
           ("Master declarativo", "layout.json / spec.json\n(texto, fonte, cor, caixa)"), ("Scripts determinísticos", "compose.py, build_*.py,\nglyph_rewrite.py, r19_mesh.py")]
    for i, (t, s) in enumerate(ins):
        y = 50 + i * 82
        b += box_svg(20, y, 300, 70, t, s, "#eef3fb", "#1d63c4", 15, 12)
        b += line_svg(320, y + 35, 418, 200)
    b += box_svg(420, 150, 220, 100, "Asset localizado", "PNG → DDS no formato\ndo original; malha + .cdae", "#eaf6ee", "#148c46", 16, 12)
    b += line_svg(640, 200, 698, 200)
    b += box_svg(700, 120, 280, 160, "Verificação", "0 px fora das regiões\nalfa preservado\nformato e mips do original\nfamília completa\nestrutura da malha idêntica", "#fff7e8", "#e67814", 16, 12)
    b += text_svg(20, 390, "Refazer = rodar de novo. Nenhum pixel é pintado à mão; nenhuma etapa generativa.", 13)
    return write_svg("diagrams", "reproducible_master.svg", b, 1000, 400)


def fig_speed_chain():
    b = ""
    items = [("25 mph", "placa original", "#f3f4f6", "#1c2026"), ("40,23 km/h", "× 1,609344", "#fff7e8", "#e67814"),
             ("40 km/h", "múltiplo de 10 (MBST-I)", "#eaf6ee", "#148c46"), ("11,1111 m/s", "÷ 3,6, gravado no mapa", "#eef3fb", "#1d63c4")]
    for i, (t, s, f, st) in enumerate(items):
        x = 20 + i * 245
        b += box_svg(x, 40, 205, 84, t, s, f, st, tsize=22)
        if i < 3:
            b += line_svg(x + 205, 82, x + 243, 82)
    b += text_svg(20, 24, "Placa (o que o jogador lê)", 15, "700", "#1c2026") + text_svg(980, 24, "Lógica (IA, tráfego, radar)", 15, "700", "#1c2026", "end")
    rows = [("5 mph", "8,05", "10", "2,7778", "cabines e pátios (Fase 5)"), ("25 mph", "40,23", "40", "11,1111", "vias locais (Fase 5); praça de pedágio (Fase 7)"),
            ("30 mph (zona)", "48,28", "50", "13,8889", "zonas e garagens; zona ADAS (via de 120, Fase 7)"), ("35 mph", "56,33", "60", "16,6667", "8 vias, radares 3/5/6/7, zona das docas (Fase 7)"),
            ("—", "—", "70", "19,4444", "corredor do Event 01 e radar 2 (Fase 7)"), ("50 mph (zona)", "80,47", "80", "22,2222", "zona Mount Wallis; placas embutidas"),
            ("automático", "—", "100 / 120", "27,7778 / 33,3333", "vias rápidas e rodovias (motor do jogo)")]
    y0 = 166
    heads = ["Original", "Exato (km/h)", "1.0.0 (km/h)", "Gravado (m/s)", "Onde vale"]
    xs = [20, 165, 295, 420, 590]
    for j, hd in enumerate(heads):
        b += text_svg(xs[j], y0, hd, 14, "700", "#1c2026")
    for i, r in enumerate(rows):
        y = y0 + 26 + i * 25
        if i % 2 == 0:
            b += f'<rect x="14" y="{y - 17}" width="972" height="25" fill="#f6f7f9"/>'
        for j, v in enumerate(r):
            b += text_svg(xs[j], y, v, 14 if j < 4 else 13, "700" if j == 2 else "400", "#1c2026" if j < 4 else "#4c5560")
    return write_svg("diagrams", "speed_conversion_chain_v100.svg", b, 1000, 380)


def fig_architecture():
    b = text_svg(20, 28, "Arquitetura final: do arquivo ao comportamento", 16, "700", "#1c2026")
    layers = [("Texturas, malhas, materiais", "31 DDS · 32 DAE + 32 CDAE · 1 materials", "#eef3fb", "#1d63c4"),
              ("Mod pelo VFS", "traducao_ptbr_wcusa_v1.0.0.zip (117 arquivos)", "#fff7e8", "#e67814"),
              ("Mapa West Coast", "items.level.json (vias, radares, placas), main.decals.json, city.sites.json, info.json", "#f3f4f6", "#1c2026"),
              ("Navgraph", "DecalRoad.speedLimit → arestas em m/s (598 mudaram)", "#eaf6ee", "#148c46"),
              ("Tráfego, polícia, radares", "slotTraffic.json (1.109 linhas) · 6 gatilhos speedTrap", "#eaf6ee", "#148c46"),
              ("Missões e pesquisa (ADAS)", "garages.sites.json · zona 50 · corredor 70 (mods externos)", "#f5ecfa", "#783ca8")]
    for i, (t, s, f, st) in enumerate(layers):
        y = 46 + i * 86
        b += box_svg(160, y, 680, 58, t, s, f, st, 16, 12)
        if i < len(layers) - 1:
            b += line_svg(500, y + 60, 500, y + 84)
    b += text_svg(20, 74, "visual", 13, "700") + text_svg(20, 390, "funcional", 13, "700")
    b += f'<line x1="140" y1="50" x2="140" y2="220" stroke="#1d63c4" stroke-width="4"/><line x1="140" y1="304" x2="140" y2="535" stroke="#148c46" stroke-width="4"/>'
    return write_svg("diagrams", "final_architecture.svg", b, 1000, 550)


def fig_qa_pipeline_final():
    steps = [("Auditoria", "Fase 0"), ("Regras de localização", "Fase 3: matriz"), ("Produção do asset", "master + scripts"),
             ("Validação PNG", "regiões, alfa"), ("DDS", "formato do original"), ("Validação de família", "mapas auxiliares, malhas"),
             ("Mod", "install + mod --installed"), ("QA no jogo (MCP)", "pares original × PT-BR"), ("QA funcional", "navgraph, IA, radar, ADAS"),
             ("QA com usuários", "Fase 8"), ("Build de release", "ZIP determinístico"), ("Validação do ZIP", "instalação limpa, VFS, mod OFF")]
    b, x, y = text_svg(20, 24, "Pipeline final: do original do jogo ao ZIP validado", 16, "700", "#1c2026"), 20, 40
    w, h, gx, gy = 230, 70, 28, 40
    for i, (t, s) in enumerate(steps):
        r, c = divmod(i, 4)
        cx = x + (c if r % 2 == 0 else 3 - c) * (w + gx)
        cy = y + r * (h + gy)
        fill, st = (("#eef3fb", "#1d63c4") if i < 7 else ("#eaf6ee", "#148c46") if i < 10 else ("#fff7e8", "#e67814"))
        b += box_svg(cx, cy, w, h, f"{i + 1}. {t}", s, fill, st, 15, 12)
        if i < len(steps) - 1:
            r2, c2 = divmod(i + 1, 4)
            nx = x + (c2 if r2 % 2 == 0 else 3 - c2) * (w + gx)
            ny = y + r2 * (h + gy)
            if r2 == r:
                b += line_svg(cx + w if nx > cx else cx, cy + h / 2, nx if nx > cx else nx + w, ny + h / 2)
            else:
                b += line_svg(cx + w / 2, cy + h, nx + w / 2, ny)
    b += text_svg(20, 375, "Azul: repositório (validador automático). Verde: jogo e pessoas. Laranja: engenharia de release (Fase 9). Um passo só avança com zero FAIL.", 13)
    return write_svg("diagrams", "qa_pipeline_final.svg", b, 1060, 390)


def fig_release_pipeline():
    smoke = json.load(open(p("tests", "reports", "release", "release_smoke.json"), encoding="utf-8"))
    build = json.load(open(p("release", "output", "traducao_ptbr_wcusa_v1.0.0_build.json"), encoding="utf-8"))
    st_on, st_off = smoke["state_on"], smoke["state_off"]
    steps = [(f"{build['files']} arquivos", "mod/traducao_ptbr_wcusa\n100 modificados · 16 novos\n1 metadado"),
             ("build_release.py", "árvore, overrides gerados,\nnomes proibidos, originais,\nvarredura de texto"),
             ("Staging + ZIP", "entradas ordenadas, datas fixas,\n.cdae 2 min depois do .dae"),
             ("Manifesto + SHA-256", f"{build['zip_size']:,} bytes\n684bcf6c…3b57".replace(",", ".")),
             ("Extração e conferência", "pasta nova, mesmos 117\narquivos e hashes"),
             ("Instalação limpa", f"só o ZIP montado\nVFS: {st_on['from_release_zip']}/{st_on['files_checked']} do ZIP\nZIP off: {st_off['from_release_zip']}/{st_off['files_checked']}")]
    b = text_svg(20, 28, "Engenharia da release 1.0.0 (Fase 9)", 16, "700", "#1c2026")
    w, h, gx = 196, 120, 14
    for i, (t, s) in enumerate(steps):
        x = 20 + i * (w + gx)
        b += box_svg(x, 50, w, h, t, s, "#eef3fb" if i < 4 else "#eaf6ee", "#1d63c4" if i < 4 else "#148c46", 14, 11)
        if i < len(steps) - 1:
            b += line_svg(x + w, 110, x + w + gx - 1, 110)
    b += text_svg(20, 200, "Reprodutibilidade: o mesmo SHA-256 em builds a partir de ac2ddf6, 896fa36 e b4a7450 (tag v1.0.0); o conteúdo do ZIP não depende do commit nem da data.", 12)
    return write_svg("release", "release_pipeline_v100.svg", b, 1300, 215)


def fig_validation_progress():
    phases = ["Fase 4", "Fase 5", "Fase 6", "Fase 7", "Fase 9"]
    fails = [17, 13, 13, 0, 0]
    # mod: Phase 4 = `mod` (6 PASS + 1 WARN, no installed copy yet); Phases 5-9 = `mod --installed`. new: suite created in Phase 5.
    tests = [("selftest", [72, 75, 121, 121, 121]), ("mod --installed", [6, 48, 217, 274, 274]), ("new", [None, 24, 75, 108, 108]),
             ("unittest", [33, 44, 44, 59, 63])]
    W, H = 1060, 400
    b = text_svg(20, 28, "Validador: FAIL de consistência de velocidade e tamanho das suítes por fase", 16, "700", "#1c2026")
    x0, y0, cw = 70, 300, 80
    b += text_svg(20, 60, "FAIL de velocidade (validate.py speeds)", 13, "700", "#1c2026")
    for i, (ph, f) in enumerate(zip(phases, fails)):
        x = x0 + i * (cw + 14)
        hgt = f / 17 * 200
        b += f'<rect x="{x}" y="{y0 - hgt}" width="{cw}" height="{max(hgt, 1)}" fill="{"#d62828" if f else "#148c46"}"/>'
        b += text_svg(x + cw / 2, y0 - hgt - 6, str(f), 14, "700", "#1c2026", "middle")
        b += text_svg(x + cw / 2, y0 + 20, ph, 12, anchor="middle")
    gx0 = 560
    b += text_svg(gx0, 60, "Verificações PASS por suíte", 13, "700", "#1c2026")
    cols = ["#1d63c4", "#e67814", "#783ca8", "#148c46"]
    sx = lambda i: gx0 + 20 + i * 80
    sy = lambda v: y0 - v / 280 * 210
    for v in (0, 100, 200):
        b += f'<line x1="{gx0}" y1="{sy(v)}" x2="{gx0 + 360}" y2="{sy(v)}" stroke="#eef0f2"/>' + text_svg(gx0 - 6, sy(v) + 4, str(v), 11, anchor="end")
    for k, (name, vals) in enumerate(tests):
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals) if v is not None)
        b += f'<polyline points="{pts}" fill="none" stroke="{cols[k]}" stroke-width="3"/>'
        for i, v in enumerate(vals):
            if v is not None:
                b += f'<circle cx="{sx(i)}" cy="{sy(v)}" r="4" fill="{cols[k]}"/>'
        b += text_svg(sx(4) + 10, sy(vals[-1]) + 4 + (k == 3) * 10 - (k == 0) * 2, f"{name} {vals[-1]}", 12, "700", cols[k])
    for i, ph in enumerate(phases):
        b += text_svg(sx(i), y0 + 20, ph, 12, anchor="middle")
    b += text_svg(20, 360, "Fase 4: suítes recém-criadas (mod: 6 PASS + 1 WARN do PoC, sem cópia instalada; new criada na Fase 5). Os FAIL da Fase 4 eram inconsistências do mapa original.", 12)
    b += text_svg(20, 378, "Nenhuma regra, tolerância ou SKIP foi relaxada para zerar o relatório; a Fase 7 acrescentou verificações (placas embutidas, pedágio).", 12)
    return write_svg("validation", "validator_progress_by_phase.svg", b, W, H)


def fig_qa_growth():
    data = [("Fase 2", 3, 8), ("Fase 5", 33, 79), ("Fase 6", 203, 365), ("Fase 7", 203, 133), ("Fase 9", 203, 38)]
    W, H, x0, y0 = 1000, 330, 80, 250
    b = text_svg(20, 28, "QA visual: pontos no catálogo de câmeras (acumulado) e capturas por fase", 16, "700", "#1c2026")
    for i, (ph, pts, caps) in enumerate(data):
        x = x0 + i * 180
        h1, h2 = pts / 400 * 190, caps / 400 * 190
        b += f'<rect x="{x}" y="{y0 - h1}" width="60" height="{h1}" fill="#1d63c4"/>' + text_svg(x + 30, y0 - h1 - 6, str(pts), 13, "700", "#1c2026", "middle")
        b += f'<rect x="{x + 66}" y="{y0 - h2}" width="60" height="{max(h2, 0.5)}" fill="#e67814"/>' + text_svg(x + 96, y0 - h2 - 6, str(caps), 13, "700", "#1c2026", "middle")
        b += text_svg(x + 63, y0 + 20, ph, 13, "700", "#1c2026", "middle")
    b += (f'<rect x="{x0}" y="{y0 + 40}" width="14" height="14" fill="#1d63c4"/>' + text_svg(x0 + 20, y0 + 52, "pontos de QA em tests/qa_locations.json", 13)
          + f'<rect x="{x0 + 330}" y="{y0 + 40}" width="14" height="14" fill="#e67814"/>' + text_svg(x0 + 350, y0 + 52, "capturas guardadas em tests/screenshots/<fase>/", 13))
    b += text_svg(x0, y0 + 74, "Fase 2: 3 pontos (8 capturas em baseline/ e current/). Fases 7 e 9 reaproveitam o catálogo e usam poses próprias.", 12)
    return write_svg("qa", "qa_coverage_growth.svg", b, W, H)


FIGS = {f.__name__[4:]: f for f in [fig_reused, fig_opening, fig_day_night_opening, fig_stop_original_poc_v100, fig_r2,
                                    fig_roadmarkings_ingame, fig_roadmarkings_opacity, fig_r19_values, fig_speed_limit_to_r19,
                                    fig_toll_booth, fig_fuel_day_night, fig_billboard, fig_industry, fig_transport,
                                    fig_commercial, fig_glyph_examples, fig_glyph_explained, fig_adas, fig_mod_off,
                                    fig_speed_map, fig_navgraph_hist, fig_radar_chart, fig_problem_expansion, fig_vfs_release,
                                    fig_state_protocol, fig_master, fig_speed_chain, fig_architecture, fig_qa_pipeline_final,
                                    fig_release_pipeline, fig_validation_progress, fig_qa_growth]}

if __name__ == "__main__":
    names = sys.argv[1:] or list(FIGS)
    for n in names:
        FIGS[n]()
