"""Unit tests for the Phase 7 functional generator (tools/production/apply_phase7_functional.py) and the Phase 7
extensions of tools/production/speed_overrides.py. Synthetic fixtures only (no game files needed).

Run:  python -m unittest discover -s tools/validation/tests -v
"""
import json
import math
import os
import sys
import unittest

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "production")))

import apply_phase7_functional as P7  # noqa: E402
import speed_overrides as SO  # noqa: E402

SITES = """{
  "name":"x",
  "zones":[
    {
      "customFields":{
        "names":["speedLimit","trafficType"],
        "types":{"speedLimit":"number"},
        "values":{"speedLimit":13.3999996,"trafficType":"residential"}
      },
      "name":"zone.a"
    },
    {
      "customFields":{
        "names":["speedLimit"],
        "types":{"speedLimit":"number"},
        "values":{"speedLimit":13.3999996}
      },
      "name":"zone.b"
    },
    {"customFields":{"values":{}},"name":"zone.c"}
  ]
}"""


class TestZones(unittest.TestCase):
    def test_only_declared_zone_changes(self):
        ch = [{"zone": "zone.b", "from": 13.3999996, "to": 13.8889}]
        new = P7.edit_zones(SITES, ch)
        d = json.loads(new)
        self.assertEqual(d["zones"][0]["customFields"]["values"]["speedLimit"], 13.3999996)
        self.assertEqual(d["zones"][1]["customFields"]["values"]["speedLimit"], 13.8889)
        self.assertEqual(P7.verify_zones(SITES, new, ch), [])
        # byte-minimal: only the value token differs
        self.assertEqual(new.replace("13.8889", "13.3999996"), SITES)

    def test_verify_catches_undeclared_change(self):
        ch = [{"zone": "zone.b", "from": 13.3999996, "to": 13.8889}]
        tampered = P7.edit_zones(SITES, ch).replace('"trafficType":"residential"', '"trafficType":"commercial"')
        self.assertTrue(P7.verify_zones(SITES, tampered, ch))

    def test_wrong_expected_value_refused(self):
        with self.assertRaises(SystemExit):
            P7.edit_zones(SITES, [{"zone": "zone.a", "from": 15.6, "to": 16.6667}])


class TestInfo(unittest.TestCase):
    RAW = '{\r\n  "size":[\r\n    2048\r\n  ],\r\n  "localUnits":{\r\n    "gasoline":"gallonUS",\r\n    "diesel":"gallonUS"\r\n  },\r\n\r\n  "minimap": [\r\n    {"file":"a.png",},\r\n  ],\r\n  "url":"http://x//y,}"\r\n}'
    CH = {"remove_key": "localUnits", "from": {"gasoline": "gallonUS", "diesel": "gallonUS"}}

    def test_relaxed_json(self):
        d = P7.relaxed_json(self.RAW)
        self.assertEqual(d["minimap"], [{"file": "a.png"}])
        self.assertEqual(d["url"], "http://x//y,}")   # strings untouched

    def test_remove_key_keeps_everything_else(self):
        new = P7.edit_info(self.RAW, self.CH)
        self.assertNotIn("localUnits", new)
        self.assertEqual(P7.verify_info(self.RAW, new, self.CH), [])
        self.assertEqual(new.count("\r\n"), self.RAW.count("\r\n") - 4)

    def test_verify_info_catches_extra_change(self):
        new = P7.edit_info(self.RAW, self.CH).replace("2048", "1024")
        self.assertTrue(P7.verify_info(self.RAW, new, self.CH))


class TestSigns(unittest.TestCase):
    def test_yaw_quat_matches_game_quatFromDir(self):
        # values returned by the game (quatFromDir(dir, up)) for the Event 01 start headings
        q = P7.yaw_quat(0.951, -0.307)
        self.assertAlmostEqual(q[2], 0.80845761640658, places=3)
        self.assertAlmostEqual(q[3], 0.58855440060727, places=3)
        q = P7.yaw_quat(0.3661, 0.9306)
        self.assertAlmostEqual(q[2], 0.18630781384088, places=3)
        self.assertAlmostEqual(q[3], 0.98249142413653, places=3)

    def test_sign_faces_oncoming_traffic_and_pole_behind(self):
        f = (0.6, 0.8)
        adas = {"sign_template": {"group": "g", "sign_height_m": 2.224, "pole_shape": "/p.dae", "pole_height_m": 1.098, "pole_behind_m": 0.11},
                "signs": [{"id": "s1", "value": 50, "_regulated": [], "_measured": {"flow": list(f), "xy": [10.0, 20.0], "ground_z": 5.0}}]}
        add, reg = P7.sign_objects(adas)
        self.assertEqual(json.loads(add["append"]["items.level.json"][0])["class"], "SimGroup")
        sign, pole = (json.loads(x) for x in add["new"]["g/items.level.json"])
        R = sign["rotationMatrix"]
        row0, row1, row2 = R[0:3], R[3:6], R[6:9]
        self.assertAlmostEqual(row1[0], f[0])                                             # local +Y = flow,
        self.assertAlmostEqual(row1[1], f[1])                                             # so the face (-Y) looks at traffic
        cross = [row0[1] * row1[2] - row0[2] * row1[1], row0[2] * row1[0] - row0[0] * row1[2], row0[0] * row1[1] - row0[1] * row1[0]]
        self.assertEqual([round(v, 6) for v in cross], [0, 0, 1])                         # right-handed, upright
        self.assertEqual(row2, [0, 0, 1])
        self.assertAlmostEqual(sign["position"][2], 7.224)
        self.assertTrue(sign["shapeName"].endswith("/sign_r19_50.dae"))
        self.assertEqual(pole["rotationMatrix"][6:9], [0, 0, -1])                       # mounted upside down like the original
        self.assertAlmostEqual(pole["position"][0], 10.0 + 0.11 * f[0])
        add2, _ = P7.sign_objects(adas)
        self.assertEqual(add, add2)                                                      # deterministic ids
        self.assertEqual(reg[0]["persistentId"], sign["persistentId"])


class TestPlan(unittest.TestCase):
    def plan(self):
        return {"entries": [{"id": "p60", "roads": [{"persistentId": "r1", "to": "16.6667"}], "radars": [], "zones": [], "missions": [],
                             "visual_signs": []}]}

    def test_consistent(self):
        rec = {"speed": [{"id": "a", "plan_id": "p60", "pid": "r1", "to": "16.6667"}], "radar": [], "zone": [], "sign": []}
        self.assertEqual(P7.check_plan(self.plan(), rec), [])

    def test_unplanned_record_and_value_mismatch(self):
        rec = {"speed": [{"id": "a", "plan_id": "p60", "pid": "r1", "to": "19.4444"},
                         {"id": "b", "plan_id": "nope", "pid": "r2", "to": "16.6667"}], "radar": [], "zone": [], "sign": []}
        errs = P7.check_plan(self.plan(), rec)
        self.assertTrue(any("nope" in e for e in errs))
        self.assertTrue(any("r1" in e for e in errs))


class TestTriggerEdit(unittest.TestCase):
    LINE = ('{"name":"speedTrapTrigger3","class":"BeamNGTrigger","persistentId":"8f20ac08","__parent":"g","position":[1,2,3],'
            '"luaFunction":"onBeamNGTrigger","speedLimit":"15.6464","speedTrapType":"speed"}')

    def test_only_speedlimit_changes(self):
        new = SO.edit_line(self.LINE, "8f20ac08", "15.6464", "16.6667", "BeamNGTrigger")
        self.assertEqual(new, self.LINE.replace("15.6464", "16.6667"))

    def test_class_is_checked(self):
        with self.assertRaises(SystemExit):
            SO.edit_line(self.LINE, "8f20ac08", "15.6464", "16.6667")   # default class DecalRoad

    def test_expected_old_value_is_checked(self):
        with self.assertRaises(SystemExit):
            SO.edit_line(self.LINE, "8f20ac08", "11.18", "16.6667", "BeamNGTrigger")


if __name__ == "__main__":
    unittest.main()


class TestPlatesPlan(unittest.TestCase):
    def test_plates_must_match_plan(self):
        plan = {"entries": [{"id": "roadsigns_speed_plates", "roads": [], "radars": [], "zones": [], "missions": [], "visual_signs": [],
                             "visual_plates": [{"id": "reg_00", "value_kmh": 60}]},
                            {"id": "toll_plaza_40", "roads": [], "radars": [], "zones": [], "missions": [], "visual_signs": [],
                             "visual_plates": [{"id": "toll_booth", "value_kmh": 40}]}]}
        ok = {"speed": [], "radar": [], "zone": [], "sign": [], "plate": [{"id": "reg_00", "value_kmh": 60}]}
        self.assertEqual(P7.check_plan(plan, ok), [])
        bad = {"speed": [], "radar": [], "zone": [], "sign": [], "plate": [{"id": "reg_00", "value_kmh": 80}, {"id": "reg_01", "value_kmh": 60}]}
        errs = P7.check_plan(plan, bad)
        self.assertTrue(any("reg_00" in e for e in errs) and any("reg_01" in e for e in errs))


class TestUvMapSelection(unittest.TestCase):
    """glyph_rewrite.plan_uv_map: an entry with "at" only re-targets the quad at that point (shared atlas cells)."""

    def test_at_selects_one_quad(self):
        import glyph_rewrite as GR
        fake = [{"rect": (370.0, 188.0, 517.0, 381.0), "centroid": np.array([0.0, 0.0, 0.0])},
                {"rect": (370.0, 188.0, 517.0, 381.0), "centroid": np.array([5.0, 0.0, 0.0])}]
        orig = (GR.G.read_quads, GR.Frame, GR.quad_box)
        GR.G.read_quads = lambda *a, **k: fake
        GR.Frame = lambda q: None
        GR.quad_box = lambda fr, q: {"Xa": 0, "Xb": 1, "Ya": 0, "Yb": 1, "depth": 0}
        try:
            d, n, _ = GR.plan_uv_map("x.dae", "roadsigns", (2048, 1024),
                                     [{"id": "a", "from": [370, 188, 517, 381], "to": [0, 0, 147, 193], "at": [[5.0, 0.0, 0.0]], "radius": 0.02}])
        finally:
            GR.G.read_quads, GR.Frame, GR.quad_box = orig
        self.assertEqual(len(d), 1)
        self.assertEqual(float(d[0]["centroid"][0]), 5.0)
