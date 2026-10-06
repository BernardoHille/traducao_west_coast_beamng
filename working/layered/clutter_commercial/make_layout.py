"""layout.json for clutter_commercial (Phase 6, 6F). Atlas 2048x2048, art_shapes copy (the one the material
clutter_commercial of art_shapes.zip names). Boxes read from coordinate grids of the ORIGINAL; texts from
LOCALIZATION_MASTER.csv (commerce_*, dealer_*, fuel_*). Brands, logos, Chinese signs, product photos and the
glyph alphabets are preserved. Elements without UV evidence are dropped by compose.py regions.

Element tuple: id, matrix id, element box, list of (text, cap box) lines, legend, colour, style extras."""
import json
from pathlib import Path

HERE = Path(__file__).parent
BAHN = {"font": "bahnschrift", "wght": 650, "wdth": 85, "min_wdth": 70}
BAHN_B = {"font": "bahnschrift", "wght": 800, "wdth": 80, "min_wdth": 65}
IMPACT = {"font": "impact"}
ARIALB = {"font": "arial_bold"}
NARROW = {"font": "arial_narrow_bold"}
WHITE = [242, 242, 240]
E = []


def el(i, m, box, lines, legend="auto", color=None, style=BAHN, **kw):
    d = {"id": i, "matrix": m, "op": "panel", "box": box, "legend": legend, "erase": kw.pop("erase", [box]),
         "erase_dilate": kw.pop("erase_dilate", 1), "no_grow": True, "bg_tol": kw.pop("bg_tol", 26), "style": dict(style),
         "lines": [{"text": t, "box": b} for t, b in lines]}
    if legend == "auto":
        d["legend_tol"] = kw.pop("legend_tol", 55)
    if "glow" in style:  # neon: the glow reaches far, so the erase box covers the whole sign incl. its halo
        d["erase_dilate"] = max(d["erase_dilate"], 3)
    if color:
        d["color"] = color
    if kw.pop("draw_only", False):  # second line of a sign already erased by the previous element
        d["erase"] = []
    if "legend_override" in kw:
        d["legend"] = kw.pop("legend_override")
    d.update(kw)
    E.append(d)


def stack(x0, y0, x1, y1, texts, gap=0.35):
    """Evenly stacked cap boxes for len(texts) lines inside the box."""
    n = len(texts)
    h = (y1 - y0) / (n + (n - 1) * gap)
    return [(t, [x0, int(round(y0 + k * h * (1 + gap))), x1, int(round(y0 + k * h * (1 + gap) + h))]) for k, t in enumerate(texts)]


NEON = lambda c: "neon"
# --- neon shop signs (area a)
el("nails_l1", "commerce_nails", [0, 2, 129, 66], [("UNHAS E", [14, 14, 118, 32])], NEON([235, 70, 120]), [245, 80, 130],
   dict(BAHN, wght=500, glow={"px": 3, "alpha": 0.5}), erase_dilate=3)
el("nails_l2", "commerce_nails", [0, 2, 129, 66], [("DEPILAÇÃO", [12, 42, 120, 56])], NEON([90, 230, 70]), [100, 235, 80],
   dict(BAHN, wght=500, glow={"px": 3, "alpha": 0.5}), erase_dilate=3, draw_only=True)
el("beauty_l1", "commerce_nails", [131, 2, 252, 64], [("SALÃO DE", [138, 14, 238, 31])], NEON([240, 70, 70]), [245, 80, 80],
   dict(BAHN, wght=650, glow={"px": 3, "alpha": 0.5}), erase_dilate=3)
el("beauty_l2", "commerce_nails", [131, 2, 252, 64], [("BELEZA", [142, 38, 234, 56])], NEON([80, 210, 70]), [90, 215, 80],
   dict(BAHN, wght=650, glow={"px": 3, "alpha": 0.5}), erase_dilate=3, draw_only=True)
el("open_oval", "commerce_nails", [22, 96, 96, 122], [("ABERTO", [28, 101, 90, 117])], NEON([70, 200, 240]), [90, 210, 245],
   dict(BAHN, wght=650, glow={"px": 3, "alpha": 0.5}), erase=[[22, 97, 96, 122]], erase_dilate=2)
el("open_tilt", "commerce_nails", [166, 146, 234, 190], [("ABERTO", [173, 159, 227, 176])], NEON([235, 60, 60]), [245, 75, 75],
   dict(BAHN, wght=650, glow={"px": 3, "alpha": 0.5}), legend_override="neon_red", keep_legend={"rgbs": [[60, 220, 240], [120, 235, 245]], "tol": 60}, erase=[[168, 150, 232, 186]], erase_dilate=2,
   rotate={"deg": 13, "pivot": [200, 168]})
el("dry_cleaning", "commerce_nails", [118, 70, 246, 134], [("LAVANDERIA", [124, 110, 240, 128])], NEON([240, 70, 80]),
   [245, 80, 85], dict(BAHN, wght=500, glow={"px": 3, "alpha": 0.5}), legend_override="neon_red", keep_legend={"rgbs": [[60, 70, 230], [90, 110, 250]], "tol": 70}, erase=[[150, 70, 212, 100], [114, 101, 250, 137]],
   erase_dilate=3)
el("facial_waxing_l1", "commerce_nails", [156, 192, 252, 252], [("Depilação", [168, 206, 240, 226])], NEON([240, 60, 70]),
   [245, 70, 80], {"font": "segoe_script_bold", "glow": {"px": 3, "alpha": 0.5}}, erase_dilate=3)
el("facial_waxing_l2", "commerce_nails", [156, 192, 252, 252], [("FACIAL", [176, 233, 228, 245])], NEON([60, 140, 240]),
   [70, 150, 245], dict(BAHN, wght=500, glow={"px": 2, "alpha": 0.5}), erase_dilate=3, draw_only=True)
YEL = {"rgbs": [[240, 230, 70]], "tol": 80}
F_MENU = {"font": "franklin_demi_cond"}
el("menu_3d", "commerce_nail_menu", [264, 174, 340, 200], [("Design 3D", [268, 180, 336, 196])], YEL, [240, 232, 70], F_MENU)
el("menu_airbrush", "commerce_nail_menu", [264, 201, 340, 226], [("Aerografia", [268, 206, 336, 222])], YEL, [240, 232, 70], F_MENU)
el("menu_gel", "commerce_nail_menu", [426, 174, 506, 200], [("Unha em Gel", [430, 180, 502, 196])], YEL, [240, 232, 70], F_MENU)
el("menu_acrylic", "commerce_nail_menu", [426, 201, 506, 226], [("Unha Acrílica", [430, 206, 502, 222])], YEL, [240, 232, 70], F_MENU)
# --- sale posters
el("entire_store_60", "commerce_sales", [2, 272, 90, 334], [("LOJA", [10, 279, 84, 297]), ("TODA", [10, 309, 84, 328])], "white",
   WHITE, dict(BAHN, wght=400, wdth=90))
el("sale_red", "commerce_sales", [108, 268, 244, 320], [("OFERTA%", [112, 274, 240, 314])], {"rgbs": [[195, 20, 20]], "tol": 80},
   [190, 18, 22], IMPACT, erase_dilate=2)
el("special_top", "commerce_sales", [132, 337, 222, 352], [("ITENS SELECIONADOS", [136, 340, 218, 349])], "dark", [70, 60, 55], NARROW)
el("special_bottom", "commerce_sales", [132, 419, 222, 434], [("ITENS SELECIONADOS", [136, 422, 218, 431])], "dark", [70, 60, 55], NARROW)
el("sale_white", "commerce_sales", [258, 262, 392, 314], [("OFERTA%", [262, 268, 388, 310])], "white", WHITE, IMPACT, erase_dilate=2)
el("store_closing", "commerce_store_closing", [262, 364, 412, 504], [("QUEIMA", [282, 372, 394, 418]), ("TOTAL", [276, 442, 400, 498])],
   {"rgbs": [[245, 210, 20]], "tol": 80}, [245, 212, 22], IMPACT, erase_dilate=2)
el("big_sale_oval_1", "commerce_sales", [420, 380, 468, 460], [("MEGA", [414, 410, 474, 428])], {"rgbs": [[240, 240, 240], [40, 60, 200]], "tol": 70},
   [40, 60, 200], dict(IMPACT, stroke={"px": 1.4, "color": [245, 245, 245]}), rotate={"deg": 78, "pivot": [444, 419]}, erase=[[427, 396, 462, 462]], erase_dilate=2)
el("big_sale_oval_2", "commerce_sales", [458, 376, 506, 476], [("OFERTA", [446, 418, 518, 435])], {"rgbs": [[240, 240, 240], [40, 60, 200]], "tol": 70},
   [40, 60, 200], dict(IMPACT, stroke={"px": 1.4, "color": [245, 245, 245]}), rotate={"deg": 78, "pivot": [482, 426]}, erase=[[464, 390, 500, 464]], erase_dilate=2)
el("entire_store_box", "commerce_sales", [138, 446, 248, 502], [("LOJA", [158, 452, 228, 470]), ("TODA", [158, 478, 228, 496])], "white",
   WHITE, dict(BAHN, wght=700))
# --- logistics / warehouse signs (area c)
el("logistics", "commerce_logistics", [8, 1102, 568, 1138], [("LOGÍSTICA E DISTRIBUIÇÃO", [14, 1108, 562, 1134])], "white", [236, 236, 232],
   dict(BAHN, wght=700, italic_shear=0.25), erase_dilate=2)
RED_T = "red"
el("shop_personnel", "commerce_shop_parking", [4, 1160, 156, 1242], stack(10, 1168, 150, 1236, ["ESTACIONAMENTO", "EXCLUSIVO DE", "FUNCIONÁRIOS"]),
   RED_T, [205, 40, 40], dict(BAHN, wght=500))
el("employee_parking", "commerce_shop_parking", [160, 1160, 308, 1242], stack(166, 1168, 302, 1236, ["ESTACIONAMENTO", "EXCLUSIVO DE", "FUNCIONÁRIOS"]),
   "dark", [30, 30, 30], dict(BAHN, wght=600))
el("visitors_report", "commerce_visitors_report", [312, 1166, 468, 1226], stack(318, 1170, 462, 1222, ["VISITANTES DEVEM SE", "APRESENTAR AO", "ESCRITÓRIO"]),
   RED_T, [210, 35, 35], dict(BAHN, wght=650))
el("own_risk_hdr", "commerce_own_risk", [476, 1160, 566, 1180], [("ATENÇÃO", [482, 1163, 560, 1177])], "dark", [30, 30, 30], BAHN)
el("own_risk_body", "commerce_own_risk", [474, 1182, 568, 1278], stack(480, 1188, 562, 1272, ["ESTACIONE", "POR SUA", "CONTA E", "RISCO"]),
   "dark", [30, 30, 30], BAHN)
el("no_dumping", "commerce_no_dumping", [4, 1252, 152, 1294], stack(10, 1256, 146, 1290, ["PROIBIDO", "JOGAR LIXO"]), RED_T, [210, 40, 40],
   dict(BAHN, wght=500))
el("private_property", "commerce_private_property", [158, 1252, 284, 1330],
   stack(164, 1256, 278, 1326, ["PROPRIEDADE", "PRIVADA", "ENTRADA", "PROIBIDA"], gap=0.4),
   {"rgbs": [[40, 80, 140], [60, 100, 150]], "tol": 60}, [40, 80, 140], dict(BAHN, wght=500, italic_shear=0.15))
el("caution_hdr", "commerce_caution_smoking", [292, 1244, 452, 1272], [("ATENÇÃO", [304, 1249, 440, 1268])],
   {"rgbs": [[30, 30, 30], [240, 210, 40]], "tol": 50}, [240, 212, 40], dict(BAHN_B, stroke={"px": 1.6, "color": [25, 25, 25]}), erase_dilate=2)
el("caution_body", "commerce_caution_smoking", [290, 1274, 456, 1300], [("PROIBIDO FUMAR", [296, 1279, 450, 1296])], "dark", [30, 30, 30], BAHN)
el("no_smoking_icon", "commerce_caution_smoking", [470, 1320, 516, 1332], [("PROIBIDO FUMAR", [471, 1322, 515, 1330])], "dark", [40, 40, 40], NARROW)
el("tennis", "commerce_tennis", [8, 1346, 520, 1384], [("CLUBE DE TÊNIS DE EAST BELASCO", [14, 1352, 514, 1378])], RED_T, [205, 35, 35],
   dict(ARIALB, italic_shear=0.2), erase_dilate=2)
# --- area d
el("no_parking_gate", "commerce_towed", [522, 1288, 668, 1344], [("PROIBIDO", [548, 1291, 642, 1312]), ("ESTACIONAR", [528, 1318, 662, 1340])],
   RED_T, [210, 35, 35], dict(BAHN_B))
el("towed", "commerce_towed", [522, 1346, 670, 1380], [("VEÍCULOS BLOQUEANDO O PORTÃO", [526, 1350, 666, 1360]),
   ("SERÃO GUINCHADOS", [530, 1366, 662, 1376])], "white", WHITE, BAHN)
el("warning_pump_hdr", "fuel_warning_pump", [522, 1384, 614, 1400], [("ATENÇÃO", [530, 1386, 606, 1398])], "white", WHITE, BAHN_B)
el("warning_pump_body", "fuel_warning_pump", [522, 1401, 614, 1452], stack(526, 1403, 610, 1449,
   ["NÃO DEIXE A BOMBA", "SEM SUPERVISÃO.", "Você é responsável", "por derramamentos"]), "dark", [60, 55, 55], NARROW)
el("danger_flam_hdr", "fuel_danger_flammable", [628, 1384, 690, 1400], [("PERIGO", [636, 1386, 686, 1398])], "white", WHITE, BAHN_B)
el("danger_flam_body", "fuel_danger_flammable", [646, 1406, 690, 1450], stack(648, 1410, 688, 1446, ["Altamente", "Inflamável"]), "dark",
   [60, 55, 55], NARROW)
el("notice_auth_hdr", "fuel_notice_authorized", [698, 1384, 766, 1400], [("AVISO", [712, 1386, 752, 1398])], "white", WHITE, BAHN_B)
el("notice_auth_body", "fuel_notice_authorized", [694, 1406, 768, 1428], stack(696, 1408, 766, 1426, ["SOMENTE PESSOAL", "AUTORIZADO"]), "dark",
   [60, 55, 55], NARROW)
el("flam_gas_diamond", "fuel_flammable_gas", [680, 1296, 752, 1370], [("GÁS", [700, 1316, 732, 1326]), ("INFLAMÁVEL", [690, 1330, 742, 1340])],
   "white", WHITE, BAHN, rotate={"deg": -48, "pivot": [716, 1328]}, erase=[[684, 1300, 748, 1366]], keep=[[722, 1300, 760, 1336]])
el("stop_engine", "fuel_stop_engine", [768, 1294, 858, 1326], [("DESLIGUE O MOTOR", [772, 1298, 854, 1310]),
   ("EVITE INCÊNDIO", [786, 1314, 840, 1322])], "white", WHITE, BAHN)
el("warranty_banner", "dealer_warranty", [940, 1336, 1064, 1370], [("GARANTIA", [950, 1342, 1054, 1364])], "white", WHITE, BAHN_B)
el("warranty_curve", "dealer_warranty", [960, 1366, 1052, 1400], [("DE 3 ANOS", [970, 1372, 1042, 1392])], "white", WHITE, BAHN_B,
   erase_dilate=2)
el("warranty_available", "dealer_warranty", [934, 1420, 1078, 1452], [("DISPONÍVEL", [940, 1424, 1072, 1450])], "white", WHITE, BAHN_B)
# --- area e (dealer banners)
el("best", "dealer_best_deals", [1180, 1218, 1346, 1272], [("MELHORES", [1186, 1224, 1340, 1266])], {"rgbs": [[200, 30, 40]], "tol": 70},
   [200, 30, 40], BAHN_B)
el("deals", "dealer_best_deals", [1160, 1274, 1360, 1330], [("OFERTAS", [1166, 1280, 1354, 1324])], "white", WHITE, BAHN_B)
el("guaranteed", "dealer_best_deals", [1120, 1334, 1404, 1372], [("GARANTIDAS", [1126, 1340, 1398, 1368])], "white", WHITE, BAHN_B)
el("big_sale", "dealer_big_sale", [1740, 1206, 2034, 1290], [("MEGA OFERTA!", [1752, 1222, 2024, 1278])],
   {"rgbs": [[220, 30, 40], [240, 240, 240], [120, 20, 25], [160, 160, 165], [60, 60, 60]], "tol": 55}, [220, 30, 40],
   dict(IMPACT, stroke={"px": 2, "color": [120, 20, 25]}), erase_dilate=3)
el("great_deals", "dealer_great_deals", [1730, 1296, 2030, 1340], [("ÓTIMAS OFERTAS", [1738, 1302, 2022, 1334])], "white", WHITE, BAHN_B)
el("fresh_cars", "dealer_great_deals", [1770, 1340, 1994, 1380], [("CARROS NOVOS", [1778, 1346, 1986, 1374])],
   {"rgbs": [[240, 240, 240], [240, 160, 40]], "tol": 60}, WHITE, BAHN_B)
el("auto_sales", "dealer_auto_sales", [1806, 1400, 2044, 1446], [("VENDAS E", [1814, 1406, 2036, 1440])], {"rgbs": [[230, 200, 40]], "tol": 70},
   [232, 202, 42], BAHN_B)
el("and_service", "dealer_auto_sales", [1806, 1450, 2044, 1494], [("SERVIÇOS", [1814, 1456, 2036, 1490])], "white", WHITE, BAHN_B)
# --- area h
el("used_cars", "dealer_used_cars", [1412, 1438, 1454, 1650], [("SEMINOVOS", [1333, 1530, 1533, 1560])], "white", WHITE, BAHN_B,
   rotate={"deg": -90, "pivot": [1433, 1545]})
SV = [("svc_tire", "TROCA DE PNEUS", 1632, 1520), ("svc_headlight", "RESTAURAÇÃO DE FARÓIS", 1736, 1520),
      ("svc_led", "LUZES DE LED", 1632, 1542), ("svc_steering", "DIREÇÃO E SUSPENSÃO", 1736, 1542),
      ("svc_smash", "FUNILARIA", 1632, 1564), ("svc_windscreen", "REPARO DE PARA-BRISA", 1736, 1564),
      ("svc_aftermarket", "PEÇAS E ACESSÓRIOS", 1632, 1586), ("svc_brake", "FREIOS E EMBREAGEM", 1736, 1586)]
for i, t, x, y in SV:
    el(i, "dealer_services_list", [x, y, x + 96, y + 18], [(t, [x + 3, y + 5, x + 93, y + 13])], "white", WHITE, NARROW)
el("testing_station", "dealer_testing_station", [1840, 1572, 1936, 1602], stack(1842, 1575, 1934, 1600,
   ["Posto de Inspeção Veicular", "aprovado pelo", "Departamento de Transportes"]), "white", WHITE, NARROW)
el("recycle", "dealer_recycle", [1942, 1522, 2042, 1604], stack(1950, 1530, 2034, 1598, ["RECEBEMOS ÓLEO", "USADO E", "BATERIAS", "GRATUITAMENTE"]),
   RED_T, [205, 60, 60], BAHN)
el("office", "dealer_facility", [1632, 1618, 1698, 1644], [("ESCRITÓRIO", [1636, 1624, 1694, 1638])], {"rgbs": [[80, 180, 100]], "tol": 70},
   [70, 175, 95], BAHN)
el("entrance", "dealer_facility", [1726, 1620, 1824, 1652], [("ENTRADA", [1732, 1626, 1818, 1646])], "white", WHITE, BAHN)
el("exit", "dealer_facility", [1730, 1670, 1824, 1704], [("SAÍDA", [1752, 1676, 1802, 1698])], "white", WHITE, BAHN)
el("no_smoking", "dealer_facility", [1854, 1616, 1924, 1654], stack(1858, 1620, 1922, 1650, ["PROIBIDO", "FUMAR"]), RED_T, [210, 50, 50], BAHN)
el("service", "dealer_facility", [1832, 1660, 1924, 1694], [("SERVIÇOS", [1836, 1666, 1920, 1690])], "white", WHITE, BAHN_B)
el("notice_hdr", "dealer_facility", [1732, 1716, 1822, 1748], [("AVISO", [1748, 1722, 1806, 1742])], "white", WHITE, BAHN_B)
el("notice_body", "dealer_facility", [1732, 1750, 1822, 1804], stack(1734, 1752, 1820, 1800,
   ["RETIRE SEUS OBJETOS DE VALOR", "ANTES DE DEIXAR O VEÍCULO", "NÃO NOS RESPONSABILIZAMOS", "POR PERDA DE OBJETOS"]),
   {"rgbs": [[200, 210, 225], [235, 240, 245]], "tol": 50}, [225, 230, 238], NARROW)
el("no_parking_hdr", "dealer_facility", [1828, 1708, 1928, 1740], [("PROIBIDO ESTACIONAR", [1832, 1714, 1924, 1734])], RED_T, [205, 40, 40], BAHN)
el("no_parking_body", "dealer_facility", [1828, 1744, 1928, 1804], stack(1832, 1748, 1924, 1800,
   ["GARAGEM EM USO CONSTANTE", "ACESSO 24 h", "NECESSÁRIO", "OBRIGADO"]), "white", WHITE, NARROW)
el("drive_away", "dealer_drive_away", [1958, 1630, 2000, 1860], [("SAIA DIRIGINDO", [1864, 1730, 2094, 1760])], "dark", [25, 25, 25],
   BAHN_B, rotate={"deg": -90, "pivot": [1979, 1745]})
el("today", "dealer_drive_away", [1940, 1690, 1968, 1800], [("HOJE", [1914, 1736, 1994, 1756])], "white", WHITE, BAHN_B,
   rotate={"deg": -90, "pivot": [1954, 1746]})
el("no_deposit_no", "dealer_no_deposit", [1548, 1640, 1700, 1720], [("SEM", [1560, 1648, 1690, 1714])], {"rgbs": [[200, 225, 60]], "tol": 70},
   [200, 225, 60], BAHN_B)
el("no_deposit_deposit", "dealer_no_deposit", [1536, 1722, 1706, 1754], [], {"rgbs": [[200, 225, 60]], "tol": 70}, [200, 225, 60], BAHN_B)
el("no_deposit_required", "dealer_no_deposit", [1548, 1768, 1694, 1804], [("ENTRADA", [1556, 1774, 1686, 1798])],
   {"rgbs": [[40, 70, 190]], "tol": 70}, [40, 70, 190], BAHN_B)
el("rotopad", "dealer_rotopad", [1418, 1702, 1518, 1744], stack(1422, 1706, 1514, 1740, ["As pastilhas certas", "para o seu", "veículo"]),
   "dark", [60, 60, 70], {"font": "segoe"})
el("all_brands", "commerce_all_brands", [1302, 1842, 1624, 1888], [("Atendemos Todas as Marcas!", [1310, 1850, 1616, 1882])], "white", WHITE,
   dict(ARIALB, italic_shear=0.2), erase_dilate=2)
el("tire_alignment", "dealer_tire_offer", [1414, 1892, 1618, 1964], [("TROCA DE PNEUS", [1424, 1898, 1608, 1924]),
   ("E ALINHAMENTO", [1424, 1932, 1608, 1958])], {"rgbs": [[235, 225, 50]], "tol": 70}, [236, 226, 50], IMPACT)
el("tire_fine", "dealer_tire_offer", [1430, 2010, 1604, 2026], [("NA COMPRA DE UM JOGO DE PNEUS", [1436, 2014, 1598, 2022])], "dark",
   [40, 60, 30], NARROW)
el("rapid_repair", "commerce_rapid_repair", [1636, 1922, 1920, 2034], [("Conserto Rápido e", [1646, 1934, 1910, 1972]),
   ("Instalação de Peças", [1646, 1986, 1910, 2024])], "dark", [25, 25, 25], dict(ARIALB, italic_shear=0.2))
# --- area f
el("got_a", "commerce_lemon", [98, 1478, 256, 1530], [("TEM UMA", [104, 1486, 250, 1520])], "dark", [45, 45, 45],
   {"font": "bahnschrift", "wght": 400, "wdth": 100, "tracking": 3})
el("lemon", "commerce_lemon", [286, 1474, 584, 1532], [("BOMBA?", [300, 1480, 574, 1524])], {"rgbs": [[235, 200, 30], [30, 30, 30]], "tol": 60},
   [236, 202, 32], dict(BAHN_B, italic_shear=0.25, stroke={"px": 1.5, "color": [30, 30, 30]}), erase_dilate=2)
el("lemon_body", "commerce_lemon", [100, 1536, 376, 1610], stack(106, 1542, 370, 1604, ["Pagamos o melhor preço", "por carros para sucata",
   "de qualquer marca!"]), "dark", [30, 30, 30], {"font": "georgia_bold", "italic_shear": 0.2})
lay = {"family": "clutter_commercial", "_doc": __doc__,
       "maps": {"color": {"original": "source/originals/png/art_shapes/clutter_commercial_b.color.png",
                          "out": "working/png/art_shapes/clutter_commercial_b.color.png"},
                "opacity": {"original": "source/originals/png/art_shapes/clutter_commercial_o.data.png",
                            "out": "working/png/art_shapes/clutter_commercial_o.data.png", "mode": "L"}},
       "region_maps": ["color", "opacity"],
       "materials": ["clutter_commercial"], "usage_texture": "clutter_commercial_b.color", "uv_min_coverage": 0.4, "seed": 20261007,
       "elements": E}
json.dump(lay, open(HERE / "layout.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(E))


# ---------------------------------------------------------------- fit / measurement (Phase 6 review): the first boxes of
# areas c/d/e/h were read from coarse grids and are off by -20..+20 px. ACCEPT_FIT: the legend bbox is measured on the
# ORIGINAL in a window 20 px lower (checked one by one on a contact sheet). MEASURED (M): boxes read on 2-4x gridded
# zooms of the original (10 px grid) where the automatic fit grabbed a neighbouring sign.
import sys  # noqa: E402
sys.path.insert(0, str(HERE.parents[2] / "tools/production"))
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import compose as C  # noqa: E402

RGB = np.asarray(Image.open(HERE.parents[2] / lay["maps"]["color"]["original"]).convert("RGB")).astype(int)
FIXED = ("nails", "beauty", "open_", "dry_", "facial", "menu_", "entire_store", "sale_", "special", "store_closing", "big_sale_oval",
         "got_a", "lemon", "used_cars", "drive_away", "today", "flam_gas", "no_deposit_deposit")
DY = {}  # per-element vertical correction where 20 px is not right
ACCEPT_FIT = {"logistics", "shop_personnel", "employee_parking", "visitors_report", "own_risk_hdr", "own_risk_body",
              "no_dumping", "private_property", "caution_hdr", "caution_body", "no_smoking_icon", "tennis",
              "warranty_available", "best", "deals", "guaranteed", "big_sale", "great_deals", "fresh_cars", "auto_sales",
              "no_deposit_required", "rapid_repair"}


def legend_px(e, pix):
    if e["legend"] == "auto":
        bg = np.median(np.concatenate([pix[0], pix[-1], pix[:, 0], pix[:, -1]]), 0)
        return np.linalg.norm(pix - bg, axis=-1) > e.get("legend_tol", 55)
    return C.legend_mask(pix, e["legend"])


fits = {}
for e in E:
    if e["id"] not in ACCEPT_FIT:
        continue
    dy = DY.get(e["id"], 20)
    x0, y0, x1, y1 = e["box"]
    sx0, sy0, sx1, sy1 = max(0, x0 - 6), y0 + dy - 8, min(2048, x1 + 6), min(2048, y1 + dy + 8)
    m = legend_px(e, RGB[sy0:sy1, sx0:sx1])
    # drop isolated specks (dirt) before measuring
    m &= C.dilate(m, 1) & (np.convolve(m.sum(1), np.ones(3), "same")[:, None] > 2)
    ys, xs = np.nonzero(m)
    if len(xs) < 10:
        print("no legend found", e["id"])
        continue
    bx = [int(sx0 + xs.min()), int(sy0 + ys.min()), int(sx0 + xs.max() + 1), int(sy0 + ys.max() + 1)]
    n = len(e["lines"])
    ob = list(e["erase"][0]) if e["erase"] else list(e["box"])
    e["box"] = [bx[0] - 4, bx[1] - 4, bx[2] + 4, bx[3] + 4]
    e["erase"] = [[bx[0] - 2, bx[1] - 2, bx[2] + 2, bx[3] + 2]]
    texts = [l["text"] for l in e["lines"]]
    e["lines"] = [{"text": t, "box": b} for t, b in stack(bx[0], bx[1], bx[2], bx[3], texts)] if n > 1 else         [{"text": texts[0], "box": bx}]
    fits[e["id"]] = {"orig": ob, "fit": bx}
M = {  # id: (erase boxes, [(text, cap box)], extras); coordinates read on gridded zooms of the original
 "no_parking_gate": ([[523, 1309, 671, 1361]], [("PROIBIDO", [540, 1311, 654, 1331]), ("ESTACIONAR", [525, 1336, 669, 1359])], {}),
 "towed": ([[522, 1366, 669, 1392]], [("VEÍCULOS BLOQUEANDO O PORTÃO", [526, 1368, 665, 1376]), ("SERÃO GUINCHADOS", [526, 1382, 665, 1390])], {}),
 "warning_pump_hdr": ([[523, 1402, 613, 1418]], [("ATENÇÃO", [527, 1404, 609, 1416])], {}),
 "warning_pump_body": ([[519, 1418, 619, 1457]], [("NÃO DEIXE A BOMBA", [523, 1420, 615, 1426]), ("SEM SUPERVISÃO.", [523, 1430, 615, 1436]),
                        ("Você é responsável", [523, 1440, 615, 1446]), ("por derramamentos", [523, 1449, 615, 1455])], {}),
 "danger_flam_hdr": ([[627, 1403, 689, 1419]], [("PERIGO", [631, 1405, 687, 1417])], {}),
 "danger_flam_body": ([[641, 1428, 690, 1452]], [("Altamente", [645, 1430, 688, 1439]), ("Inflamável", [645, 1442, 688, 1450])], {}),
 "notice_auth_hdr": ([[705, 1405, 752, 1420]], [("AVISO", [709, 1407, 748, 1418])], {}),
 "notice_auth_body": ([[693, 1429, 768, 1450]], [("SOMENTE PESSOAL", [697, 1431, 764, 1438]), ("AUTORIZADO", [697, 1441, 764, 1448])], {}),
 "stop_engine": ([[770, 1314, 856, 1341]], [("DESLIGUE O MOTOR", [772, 1316, 854, 1328]), ("EVITE INCÊNDIO", [786, 1332, 840, 1340])], {}),
 "flam_gas_diamond": ([], [("GÁS", [697, 1347, 721, 1357]), ("INFLAMÁVEL", [680, 1363, 738, 1373])],
                      {"rotate": {"deg": -45, "pivot": [709, 1360]}, "erase_rot": [[713, 1356, 58, 13, -45], [704, 1364, 24, 13, -45]],
                       "keep": [[724, 1312, 756, 1350]], "erase_dilate": 1}),
 "warranty_banner": ([[949, 1358, 1053, 1388]], [("GARANTIA", [952, 1361, 1050, 1385])], {}),
 "warranty_curve": ([], [], {"erase_ring": [[1003, 1372, 31, 48, 22, 158]], "erase_dilate": 2,
                             "lines": [{"text": "DE 3 ANOS", "box": [955, 1406, 1051, 1418], "arc": {"cx": 1003, "cy": 1372, "r": 46, "deg": 90}}]}),
 "and_service": ([[1802, 1452, 2044, 1492]], [("SERVIÇOS", [1812, 1456, 2036, 1490])], {}),
 "testing_station": ([[1842, 1556, 1936, 1586]], [("Posto de Inspeção Veicular", [1844, 1559, 1934, 1566]),
                     ("aprovado pelo", [1844, 1568, 1934, 1575]), ("Departamento de Transportes", [1844, 1577, 1934, 1584])], {}),
 "recycle": ([[1944, 1508, 2044, 1574]], [("RECEBEMOS ÓLEO", [1948, 1511, 2040, 1520]), ("USADO E", [1948, 1529, 2040, 1537]),
             ("BATERIAS", [1948, 1546, 2040, 1554]), ("GRATUITAMENTE", [1948, 1563, 2040, 1571])], {}),
 "office": ([[1634, 1604, 1695, 1622]], [("ESCRITÓRIO", [1637, 1607, 1692, 1619])], {}),
 "entrance": ([[1728, 1613, 1822, 1631]], [("ENTRADA", [1731, 1615, 1819, 1629])], {}),
 "exit": ([[1752, 1665, 1798, 1683]], [("SAÍDA", [1750, 1667, 1800, 1681])], {}),
 "no_smoking": ([[1855, 1606, 1924, 1637]], [("PROIBIDO", [1858, 1609, 1922, 1619]), ("FUMAR", [1858, 1625, 1922, 1635])], {}),
 "service": ([[1833, 1649, 1922, 1674]], [("SERVIÇOS", [1835, 1651, 1920, 1672])], {}),
 "notice_hdr": ([[1733, 1705, 1819, 1729]], [("AVISO", [1745, 1707, 1807, 1727])], {}),
 "notice_body": ([[1731, 1770, 1821, 1796]], [("NÃO NOS RESPONSABILIZAMOS", [1734, 1773, 1818, 1779]),
                 ("POR PERDA DE OBJETOS", [1734, 1780, 1818, 1786]), ("PESSOAIS", [1734, 1787, 1818, 1793])],
                 {"legend": "white", "color": [236, 240, 246]}),
 "no_parking_hdr": ([[1828, 1700, 1928, 1716]], [("PROIBIDO ESTACIONAR", [1831, 1702, 1925, 1714])], {}),
 "no_parking_body": ([[1831, 1732, 1925, 1784]], [("GARAGEM EM USO CONSTANTE", [1834, 1734, 1922, 1742]), ("ACESSO 24 h", [1834, 1749, 1922, 1756]),
                     ("NECESSÁRIO", [1834, 1761, 1922, 1768]), ("OBRIGADO", [1834, 1774, 1922, 1782])], {}),
 "no_deposit_no": ([[1556, 1655, 1694, 1733]], [("SEM", [1560, 1658, 1690, 1730])], {}),
 "no_deposit_deposit": ([[1556, 1739, 1692, 1766]], [("ENTRADA", [1560, 1742, 1688, 1763])], {}),
 "no_deposit_required": ([[1552, 1787, 1694, 1810]], [], {}),
 "rotopad": ([[1418, 1685, 1513, 1727]], [("As pastilhas", [1424, 1688, 1508, 1698]), ("certas para o", [1424, 1701, 1508, 1711]),
             ("seu veículo", [1424, 1714, 1508, 1724])], {}),
 "all_brands": ([[1308, 1846, 1620, 1881]], [("Atendemos Todas as Marcas!", [1312, 1850, 1616, 1878])], {}),
 "tire_alignment": ([[1428, 1894, 1598, 1966]], [("TROCA DE PNEUS", [1428, 1900, 1598, 1923]), ("E ALINHAMENTO", [1428, 1937, 1598, 1960])], {}),
 "tire_fine": ([[1436, 2034, 1594, 2045]], [("NA COMPRA DE UM JOGO DE PNEUS", [1440, 2036, 1590, 2043])], {}),
 "got_a": ([[100, 1483, 254, 1516]], [("TEM UMA", [104, 1487, 250, 1512])], {}),
 "lemon": ([[284, 1469, 582, 1521]], [("BOMBA?", [296, 1473, 574, 1517])], {}),
 "used_cars": ([[1452, 1429, 1478, 1628]], [(ch, [1455, int(1432 + k * 21.4), 1475, int(1432 + k * 21.4) + 16]) for k, ch in enumerate("SEMINOVOS")],
               {"rotate": None, "style": dict(BAHN_B, wdth=100, min_wdth=60)}),
 "drive_away": ([[1971, 1649, 1999, 1850]], [("SAIA DIRIGINDO", [1888, 1738, 2082, 1762])], {"rotate": {"deg": -90, "pivot": [1985, 1750]}}),
 "today": ([[1943, 1700, 1971, 1796]], [("HOJE", [1913, 1737, 2001, 1759])], {"rotate": {"deg": -90, "pivot": [1957, 1748]}}),
}
# second review round (before/after crops c1..c7)
WL = {"rgbs": [[246, 242, 242]], "tol": 45}
YEL_C = {"rgbs": [[235, 205, 45], [205, 170, 30]], "tol": 60}
M.update({
 "employee_parking": ([[165, 1170, 303, 1252]], [("ESTACIONAMENTO", [168, 1173, 300, 1189]), ("EXCLUSIVO DE", [168, 1194, 300, 1211]),
                      ("FUNCIONÁRIOS", [168, 1225, 300, 1247])], {}),
 "own_risk_hdr": ([[478, 1173, 564, 1191]], [("ATENÇÃO", [484, 1177, 558, 1189])], {}),
 "own_risk_body": ([[479, 1200, 564, 1295]], [("ESTACIONE", [481, 1202, 562, 1218]), ("POR SUA", [481, 1225, 562, 1242]),
                   ("CONTA E", [481, 1250, 562, 1267]), ("RISCO", [481, 1277, 562, 1293])], {}),
 "caution_hdr": ([[301, 1266, 449, 1294]], [("ATENÇÃO", [306, 1270, 444, 1291])],
                 {"legend": YEL_C, "style": dict(BAHN_B, stroke={"px": 1.0, "color": [25, 25, 25]}), "erase_dilate": 2}),
 "warning_pump_hdr": ([[523, 1402, 613, 1418]], [("ATENÇÃO", [527, 1404, 609, 1416])], {"legend": WL}),
 "warning_pump_body": ([[519, 1418, 619, 1457]], [("NÃO DEIXE A BOMBA", [523, 1420, 615, 1426]), ("SEM SUPERVISÃO.", [523, 1430, 615, 1436]),
                       ("Você é responsável", [523, 1440, 615, 1446]), ("por derramamentos", [523, 1449, 615, 1455])],
                       {"legend": "auto", "legend_tol": 35, "erase_dilate": 2}),
 "warranty_available": ([[935, 1437, 1070, 1461]], [("DISPONÍVEL", [939, 1441, 1066, 1458])], {"legend": WL}),
 "big_sale": ([[1721, 1220, 2040, 1301]], [("MEGA", [1728, 1234, 1862, 1288])],
              {"legend": "auto", "legend_tol": 60, "erase_dilate": 2, "color": [246, 240, 240],
               "style": dict(IMPACT, stroke={"px": 2.5, "color": [200, 25, 40]}, shadow={"dx": 3, "dy": 2, "color": [30, 20, 20]})}),
 "great_deals": ([[1733, 1312, 2030, 1355]], [("ÓTIMAS OFERTAS", [1740, 1322, 2022, 1351])], {"erase_dilate": 3}),
 "no_deposit_no": ([[1552, 1655, 1694, 1733]], [("SEM", [1560, 1658, 1690, 1730])], {}),
 "no_deposit_required": ([[1550, 1785, 1696, 1812]], [], {"erase_dilate": 2}),
 "rotopad": ([[1418, 1685, 1513, 1727]], [("As pastilhas", [1424, 1688, 1508, 1698]), ("certas para o", [1424, 1701, 1508, 1711]),
             ("seu veículo", [1424, 1714, 1508, 1724])], {"erase_dilate": 2}),
 "tire_fine": ([[1436, 2022, 1594, 2031]], [("NA COMPRA DE UM JOGO DE PNEUS", [1440, 2024, 1590, 2030])], {}),
 "notice_body": ([[1731, 1770, 1821, 1796]], [("NÃO NOS RESPONSABILIZAMOS", [1734, 1773, 1818, 1779]),
                 ("POR PERDA DE OBJETOS", [1734, 1780, 1818, 1786]), ("PESSOAIS", [1734, 1787, 1818, 1793])],
                 {"legend": "auto", "legend_tol": 40, "erase_dilate": 2, "color": [236, 240, 246]}),
})
# third review round
NOT_RED = {"legend": "auto", "legend_tol": 70, "erase_dilate": 2}  # off-white letters on a faded red band
M.update({
 "caution_hdr": ([[301, 1266, 447, 1290]], [("ATENÇÃO", [308, 1271, 440, 1287])],
                 {"legend": YEL_C, "style": dict(BAHN_B, stroke={"px": 1.0, "color": [25, 25, 25]}), "erase_dilate": 2}),
 "caution_body": ([[294, 1295, 452, 1317]], [("PROIBIDO FUMAR", [298, 1298, 448, 1314])], {}),
 "warning_pump_hdr": ([[521, 1403, 615, 1416]], [("ATENÇÃO", [527, 1405, 609, 1415])], NOT_RED),
 "warranty_available": ([[930, 1437, 1075, 1460]], [("DISPONÍVEL", [939, 1441, 1066, 1458])], NOT_RED),
 "fresh_cars": ([[1770, 1360, 1994, 1394]], [("CARROS NOVOS", [1778, 1364, 1986, 1391])], {"erase_dilate": 3}),
})
M["tennis"] = ([[8, 1365, 522, 1401]], [("CLUBE DE TÊNIS DE EAST BELASCO", [14, 1370, 512, 1397])], {})
M["fresh_cars"] = ([[1770, 1360, 1994, 1394]], [("CARROS NOVOS", [1778, 1364, 1986, 1391])], {"legend": "auto", "legend_tol": 50, "erase_dilate": 3})
M["flam_gas_diamond"][2]["erase_rot"] = [[714, 1357, 68, 14, -45], [704, 1364, 24, 13, -45]]
for k in range(4):  # services list: four rows of red bars, 22 px pitch
    for col, x in ((0, 1632), (1, 1736)):
        i, t, _, _ = SV[2 * k + col]
        y = 1502 + 22 * k
        M[i] = ([[x + 2, y + 1, x + 94, y + 15]], [(t, [x + 4, y + 4, x + 92, y + 12])],
                {"legend": "auto", "legend_tol": 40, "erase_dilate": 2})
byid = {e["id"]: e for e in E}
for i, (er, lines, extra) in M.items():
    e = byid[i]
    extra = dict(extra)
    e["lines"] = extra.pop("lines") if "lines" in extra else [{"text": t, "box": b} for t, b in lines]
    e["erase"] = er
    for k, v in extra.items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = v
    bxs = list(er)
    for cx, cy, ln, hh, _ in e.get("erase_rot", []):
        r = (ln + hh) / 2 ** 0.5 / 2 + 2
        bxs.append([int(cx - r), int(cy - r), int(cx + r) + 1, int(cy + r) + 1])
    for cx, cy, r0, r1, a0, a1 in e.get("erase_ring", []):
        bxs.append([cx - r1 - 2, cy - 2, cx + r1 + 2, cy + r1 + 2])
    e["box"] = [min(b[0] for b in bxs) - 2, min(b[1] for b in bxs) - 2, max(b[2] for b in bxs) + 2, max(b[3] for b in bxs) + 2]
    fits[i] = {"measured": e["box"]}
el("big_sale_2", "dealer_big_sale", [1868, 1232, 2040, 1290], [("OFERTA!", [1874, 1238, 2034, 1284])], "auto", [220, 30, 40],
   dict(IMPACT, stroke={"px": 2, "color": [120, 20, 25]}), draw_only=True)
# coverage audit (6H): English left in UV-used parts of the atlas
el("no_entry_cn", "commerce_chinese", [588, 26, 646, 47], [("ENTRADA", [592, 28, 642, 35]), ("PROIBIDA", [592, 38, 642, 45])], "dark",
   [45, 40, 35], NARROW, erase=[[589, 27, 644, 41]])
el("rentabox_storage", "commerce_rentabox", [578, 1150, 1076, 1195], [("GUARDA-VOLUMES SEGURO", [584, 1156, 1068, 1190])], "dark",
   [25, 25, 25], {"font": "bahnschrift", "wght": 700, "wdth": 100, "min_wdth": 75}, erase=[[580, 1152, 1074, 1193]], erase_dilate=2)
# blue text on the white strip of the NOTICE sign, as its own element
el("notice_body_top", "dealer_facility", [1729, 1733, 1823, 1769], [("RETIRE SEUS OBJETOS DE VALOR", [1734, 1738, 1818, 1744]),
   ("ANTES DE DEIXAR O VEÍCULO", [1734, 1747, 1818, 1753]), ("PARA O SERVIÇO", [1734, 1756, 1818, 1762])], "auto", [120, 140, 190], NARROW,
   erase=[[1731, 1735, 1821, 1767]], legend_tol=30)
# 15% OFF: the 15% stays, OFF -> DE / DESCONTO in the slot of OFF
el("tire_off", "dealer_tire_offer", [1516, 1976, 1612, 2017], [("DE", [1522, 1980, 1606, 1993]), ("DESCONTO", [1522, 1999, 1606, 2012])],
   {"rgbs": [[70, 150, 50]], "tol": 70}, [70, 150, 50], IMPACT, erase=[[1520, 1978, 1610, 2015]], erase_dilate=2)
todo = [e["id"] for e in E if e["box"][1] >= 1020 and e["id"] not in ACCEPT_FIT and e["id"] not in M
        and e["id"] not in ("lemon_body", "notice_body_top", "tire_off", "big_sale_2", "rentabox_storage")]
print("unchecked:", todo)
# drawing area: the element box bounds the ink, so leave room for accents above the caps and cedillas below
for e in E:
    caps = [l["box"][3] - l["box"][1] for l in e.get("lines", [])]
    if not caps or e.get("rotate"):
        continue
    c = max(caps)
    tops = min(l["box"][1] for l in e["lines"])
    bots = max(l["box"][3] for l in e["lines"])
    b = e["box"]
    e["box"] = [max(0, b[0] - 1), max(0, min(b[1], tops - int(0.45 * c) - 1)), min(2048, b[2] + 1), min(2048, max(b[3], bots + int(0.3 * c) + 1))]
# neon signs and the SALE% posters are cut out letter by letter by the opacity map (alphaTest 64): the erased legend
# is cleared from the mask and the new letters (+ stroke / glow) are added to it
CUTOUT = {"nails_l1", "nails_l2", "beauty_l1", "beauty_l2", "open_tilt", "dry_cleaning", "facial_waxing_l1", "facial_waxing_l2",
          "sale_red", "sale_white"}
for e in E:
    if e["id"] in CUTOUT:
        e["aux"] = {"opacity": "cutout"}
        if not e["id"].startswith("sale_"):
            e["cutout_clear"] = 4 if e["id"] == "dry_cleaning" else True  # the hanger crosses the DRY CLEANING erase area
# not sampled by any instanced West Coast mesh (compose.py regions, UV coverage below 0.4): not edited
NOT_USED = {"entire_store_60", "big_sale_oval_1", "big_sale_oval_2", "no_smoking_icon", "tennis", "warning_pump_hdr",
            "warning_pump_body", "stop_engine"}
E[:] = [e for e in E if e["id"] not in NOT_USED]
lay["_not_used"] = sorted(NOT_USED)
lay["_fitted_boxes"] = fits
json.dump(lay, open(HERE / "layout.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(fits), "fitted")
