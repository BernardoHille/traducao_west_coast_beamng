"""Unit tests for the Phase 5 checks: new_asset_spec (R-19), speedLimit-only level edits, R-19 mesh tool.

Run:  python -m unittest discover -s tools/validation/tests -v
Synthetic fixtures; the mesh test uses the extracted original only when it exists locally.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "production")))

import dds_parser  # noqa: E402
import validate_new_assets as vna  # noqa: E402
from common import FAIL, PASS, Report  # noqa: E402
from test_validation import Tmp, write_dds  # noqa: E402

REPO = Path(HERE).resolve().parents[2]


def statuses(rep):
    return {c.name: c.status for c in rep.checks}


class TestNewAssetSpec(Tmp):
    def setUp(self):
        super().setUp()
        self._mod = vna.MOD_DIR
        vna.MOD_DIR = self.d

    def tearDown(self):
        vna.MOD_DIR = self._mod
        super().tearDown()

    FAM = {"dir": "lvl/r19"}

    def test_texture_spec_pass(self):
        write_dds(self.p("lvl", "r19", "c.dds"), 512, 1024, 11, 99)
        rep = Report("t")
        vna.check_texture(rep, self.FAM, {"file": "c.dds", "width": 512, "height": 1024, "format": "BC7_UNORM_SRGB", "srgb": True, "mips": "full"})
        self.assertEqual(statuses(rep)["c.dds: spec"], PASS)

    def test_texture_linear_instead_of_srgb_fail(self):
        write_dds(self.p("lvl", "r19", "c.dds"), 512, 1024, 11, 98)
        rep = Report("t")
        vna.check_texture(rep, self.FAM, {"file": "c.dds", "width": 512, "height": 1024, "format": "BC7_UNORM_SRGB", "srgb": True, "mips": "full"})
        self.assertEqual(statuses(rep)["c.dds: spec"], FAIL)

    def test_texture_partial_mips_fail(self):
        write_dds(self.p("lvl", "r19", "o.dds"), 512, 1024, 1, 80)
        rep = Report("t")
        vna.check_texture(rep, self.FAM, {"file": "o.dds", "width": 512, "height": 1024, "format": "BC4_UNORM", "srgb": False, "mips": "full"})
        self.assertEqual(statuses(rep)["o.dds: spec"], FAIL)

    def test_disc_mask_with_opaque_corners_fail(self):
        write_dds(self.p("lvl", "r19", "o.dds"), 64, 128, 8, 80)
        png = self.p("o.png")
        Image.fromarray(np.full((128, 64, 4), 255, np.uint8)).save(png)   # fully opaque: no disc
        rep = Report("t")
        vna.REPO = self.d
        try:
            vna.check_texture(rep, self.FAM, {"file": "o.dds", "width": 64, "height": 128, "format": "BC4_UNORM", "srgb": False,
                                              "mips": "full", "source_png": "o.png",
                                              "disc": {"corners_max": 8, "center_min": 247, "coverage_range": [0.52, 0.6]}})
        finally:
            vna.REPO = str(REPO)
        self.assertEqual(statuses(rep)["o.dds: disc mask"], FAIL)

    def test_material_redefining_game_material_fail(self):
        os.makedirs(self.p("lvl", "r19", "x"), exist_ok=True)
        with open(self.p("lvl", "r19", "main.materials.json"), "w") as f:
            json.dump({"roadsigns": {"name": "roadsigns", "mapTo": "roadsigns", "Stages": [{}]}}, f)
        rep = Report("t")
        vna.check_materials(rep, {"dir": "lvl/r19", "materials_file": "main.materials.json", "materials": {},
                                  "forbidden_material_names": ["roadsigns"]})
        self.assertEqual(statuses(rep)["Materials: no game material redefined"], FAIL)

    def test_material_texture_not_shipped_fail(self):
        with open(self.p("lvl", "r19", "main.materials.json"), "w") as f:
            json.dump({"m": {"name": "m", "mapTo": "m", "alphaTest": True, "alphaRef": 128,
                             "Stages": [{"baseColorMap": "/lvl/r19/missing.dds"}]}}, f)
        rep = Report("t")
        vna.check_materials(rep, {"dir": "lvl/r19", "materials_file": "main.materials.json", "forbidden_material_names": [],
                                  "materials": {"m": {"baseColorMap": "missing.dds", "alphaTest": True, "alphaRef": 128}}})
        self.assertEqual(statuses(rep)["Material m"], FAIL)


class TestSpeedOverrideEdit(unittest.TestCase):
    def setUp(self):
        import speed_overrides
        self.so = speed_overrides

    LINE = ('{"class":"DecalRoad","persistentId":"p1","__parent":"g","position":[1,2,3],"drivability":1,'
            '"nodes":[[0,0,0,8],[10,0,0,8]],"textureLength":5}')

    def test_insert_keeps_everything_else(self):
        out = self.so.edit_line(self.LINE, "p1", None, "2.7778")
        a, b = json.loads(self.LINE), json.loads(out)
        self.assertEqual(b.pop("speedLimit"), "2.7778")
        self.assertEqual(a, b)
        self.assertLess(out.index('"speedLimit"'), out.index('"textureLength"'))   # alphabetical position

    def test_replace_value(self):
        line = self.LINE.replace('"drivability":1,', '"drivability":1,"speedLimit":"11.18",')
        out = self.so.edit_line(line, "p1", "11.18", "11.1111")
        self.assertEqual(json.loads(out)["speedLimit"], "11.1111")
        self.assertEqual(len(out), len(line) + 2)

    def test_wrong_expected_value_refused(self):
        line = self.LINE.replace('"drivability":1,', '"drivability":1,"speedLimit":"15.6464",')
        with self.assertRaises(SystemExit):
            self.so.edit_line(line, "p1", "11.18", "11.1111")

    def test_slot_walker_reads_lane_and_link(self):
        text = ('{\n  "nodes":{\n    "N1":{\n      "links":{\n        "N2":{\n          "roadId":"L7",\n'
                '          "speedLimit":11.18\n        }\n      }\n    }\n  },\n  "roads":{\n    "L7":{\n'
                '      "properties":{\n        "oneWay":true,\n        "speedLimit":11.18\n      }\n    }\n  }\n}')
        got = list(self.so.walk_speed_lines(text.split("\n")))
        self.assertEqual([(k, o, v) for _, k, o, v in got], [("link", "L7", 11.18), ("road", "L7", 11.18)])


@unittest.skipUnless((REPO / "source/originals/meshes/objects/sign_speed25.dae").exists(), "original mesh not extracted locally")
class TestR19Mesh(unittest.TestCase):
    def test_only_materials_and_uvs_change(self):
        import r19_mesh
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "sign_speed25.dae"
            info = r19_mesh.build(REPO / "source/originals/meshes/objects/sign_speed25.dae", out, 40)
            self.assertEqual(info["orientation_from_overlays"], {"du_dx": 1, "dv_dz": 1})
            rows = {r["check"]: r for r in r19_mesh.compare(REPO / "source/originals/meshes/objects/sign_speed25.dae", out)["rows"]}
            for k in ("positions_sha", "normals_sha", "colors_sha", "p_lists_sha", "bbox_min", "bbox_max", "nodes"):
                self.assertTrue(rows[k]["same"], k)
            self.assertEqual(sorted(rows["materials"]["new"]), ["roadsigns_ptbr_r19_40", "roadsigns_ptbr_r19_back"])


if __name__ == "__main__":
    unittest.main()
