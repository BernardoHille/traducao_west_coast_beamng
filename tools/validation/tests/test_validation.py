"""Unit tests for the validation pipeline (stdlib unittest; also collected by pytest).

Run:  python -m unittest discover -s tools/validation/tests -v
All fixtures are synthetic and generated in a temporary directory.
"""
import os
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dds_parser  # noqa: E402
from common import FAIL, PASS, SKIP, WARN  # noqa: E402
from validate_dds import validate_dds  # noqa: E402
from validate_family import validate_family  # noqa: E402
from validate_mod_tree import validate_mod_tree  # noqa: E402
from validate_speed_consistency import is_multiple_of_10, kmh, mps, point_in_polygon, same_speed  # noqa: E402
from validate_texture import validate_png  # noqa: E402


def write_dds(path, w, h, mips, fmt, truncate=0, alpha_mode=0):
    head = dds_parser.build_header(w, h, mips, fmt, alpha_mode)
    info = dds_parser.parse(head + b"\0" * 64)
    size = info["expected_size"] - len(head)
    with open(path, "wb") as f:
        f.write(head + b"\0" * max(0, size - truncate))
    return path


def status_of(rep, name):
    return [c.status for c in rep.checks if c.name == name]


class Tmp(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.d = self._td.name

    def tearDown(self):
        self._td.cleanup()

    def p(self, *parts):
        path = os.path.join(self.d, *parts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path


class TestDDSParser(Tmp):
    def test_bc7_srgb(self):
        i = dds_parser.parse(write_dds(self.p("a_b.color.dds"), 2048, 1024, 12, 99))
        self.assertEqual((i["width"], i["height"], i["format"], i["srgb"], i["mip_count"]), (2048, 1024, "BC7_UNORM_SRGB", True, 12))
        self.assertTrue(i["dx10"])
        self.assertEqual(i["full_mip_count"], 12)

    def test_bc7_linear(self):
        i = dds_parser.parse(write_dds(self.p("a_o.data.dds"), 256, 256, 9, 98))
        self.assertEqual((i["format"], i["srgb"], i["colour_space"]), ("BC7_UNORM", False, "linear"))

    def test_bc4_legacy(self):
        i = dds_parser.parse(write_dds(self.p("m.dds"), 1024, 256, 11, "BC4U"))
        self.assertEqual((i["format"], i["dx10"], i["block_bytes"]), ("BC4_UNORM", False, 8))

    def test_dxt1(self):
        i = dds_parser.parse(write_dds(self.p("d.dds"), 512, 256, 10, "DXT1"))
        self.assertEqual((i["format"], i["block_bytes"], i["srgb"]), ("BC1_UNORM", 8, None))

    def test_dxt5(self):
        i = dds_parser.parse(write_dds(self.p("d5.dds"), 1024, 1024, 11, "DXT5"))
        self.assertEqual(i["format"], "BC3_UNORM")

    def test_full_mip_count(self):
        self.assertEqual(dds_parser.full_mip_count(2048, 1024), 12)
        self.assertEqual(dds_parser.full_mip_count(1024, 256), 11)
        self.assertEqual(dds_parser.full_mip_count(64, 64), 7)

    def test_not_dds(self):
        with open(self.p("x.dds"), "wb") as f:
            f.write(b"PNG....." * 40)
        with self.assertRaises(dds_parser.DDSError):
            dds_parser.parse(self.p("x.dds"))


class TestDDSValidation(Tmp):
    def test_identical_pass(self):
        a = write_dds(self.p("o", "t_b.color.dds"), 512, 512, 10, 99)
        self.assertEqual(validate_dds(a, a).status, PASS)

    def test_srgb_vs_linear_fail(self):
        o = write_dds(self.p("o", "t_b.color.dds"), 512, 512, 10, 99)
        c = write_dds(self.p("c", "t_b.color.dds"), 512, 512, 10, 98)
        r = validate_dds(c, o)
        self.assertIn(FAIL, status_of(r, "DDS format"))
        self.assertIn(FAIL, status_of(r, "Colour space"))

    def test_data_map_srgb_fail(self):
        o = write_dds(self.p("o", "t_o.data.dds"), 256, 256, 9, 99)
        r = validate_dds(o, o)
        self.assertIn(FAIL, status_of(r, "Colour space (data map)"))

    def test_mip_mismatch_fail(self):
        o = write_dds(self.p("o", "t_b.color.dds"), 512, 512, 10, 99)
        c = write_dds(self.p("c", "t_b.color.dds"), 512, 512, 1, 99)
        self.assertIn(FAIL, status_of(validate_dds(c, o), "Mipmaps"))

    def test_resolution_mismatch_fail(self):
        o = write_dds(self.p("o", "t_b.color.dds"), 512, 512, 10, 99)
        c = write_dds(self.p("c", "t_b.color.dds"), 1024, 1024, 11, 99)
        self.assertIn(FAIL, status_of(validate_dds(c, o), "Resolution"))

    def test_truncated_fail(self):
        o = write_dds(self.p("o", "t_b.color.dds"), 512, 512, 10, 99)
        c = write_dds(self.p("c", "t_b.color.dds"), 512, 512, 10, 99, truncate=100)
        self.assertIn(FAIL, status_of(validate_dds(c, o), "File size"))

    def test_alpha_mode_compatible(self):
        o = write_dds(self.p("o", "t_b.color.dds"), 64, 64, 7, 99, alpha_mode=0)
        c = write_dds(self.p("c", "t_b.color.dds"), 64, 64, 7, 99, alpha_mode=1)
        self.assertIn(PASS, status_of(validate_dds(c, o), "DX10 alpha mode"))


def save_rgba(path, arr):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(arr.astype(np.uint8), "RGBA").save(path)
    return path


class TestPNG(Tmp):
    def base(self, alpha=255):
        a = np.zeros((64, 64, 4), dtype=np.uint8)
        a[..., :3] = 120
        a[..., 3] = alpha
        return a

    def test_identical_pass(self):
        o = save_rgba(self.p("o.png"), self.base())
        r = validate_png(o, o, regions=[], heatmap=False)
        self.assertEqual(r.status, PASS)

    def test_resolution_fail(self):
        o = save_rgba(self.p("o.png"), self.base())
        c = save_rgba(self.p("c.png"), np.zeros((32, 64, 4), dtype=np.uint8))
        self.assertIn(FAIL, status_of(validate_png(c, o, regions=[], heatmap=False), "Resolution"))

    def test_alpha_loss_fail(self):
        a = self.base(); a[:, :32, 3] = 0
        o = save_rgba(self.p("o.png"), a)
        c = save_rgba(self.p("c.png"), self.base(255))
        self.assertIn(FAIL, status_of(validate_png(c, o, regions=[], heatmap=False), "Alpha preservation"))

    def test_alpha_noise_fail(self):
        o = save_rgba(self.p("o.png"), self.base(255))
        b = self.base(255); b[:10, :10, 3] = 210
        c = save_rgba(self.p("c.png"), b)
        self.assertIn(FAIL, status_of(validate_png(c, o, regions=[], heatmap=False), "Alpha noise"))

    def test_change_outside_region_fail(self):
        o = save_rgba(self.p("o.png"), self.base())
        b = self.base(); b[40:60, 40:60, :3] = 250
        c = save_rgba(self.p("c.png"), b)
        r = validate_png(c, o, regions=[{"x": 0, "y": 0, "width": 16, "height": 16}], heatmap=False)
        self.assertIn(FAIL, status_of(r, "Changes outside allowed regions"))

    def test_change_inside_region_pass(self):
        o = save_rgba(self.p("o.png"), self.base())
        b = self.base(); b[2:14, 2:14, :3] = 250; b[2:14, 2:14, 3] = 0
        c = save_rgba(self.p("c.png"), b)
        r = validate_png(c, o, regions=[{"x": 0, "y": 0, "width": 16, "height": 16}], heatmap=False)
        self.assertEqual(r.status, PASS)

    def test_heatmap_written(self):
        import common
        old = common.IMAGE_DIR
        try:
            import validate_texture
            validate_texture.IMAGE_DIR = self.p("img")
            o = save_rgba(self.p("o.png"), self.base())
            b = self.base(); b[0:4, 0:4, :3] = 255
            c = save_rgba(self.p("cand.png"), b)
            r = validate_png(c, o, regions=[], heatmap=True)
            self.assertTrue(os.path.exists(os.path.join(self.p("img"), "cand_diff.png")))
            self.assertIn("heatmaps", r.meta)
        finally:
            validate_texture.IMAGE_DIR = old


class TestModTree(Tmp):
    def make_mod(self, files, info=True):
        root = self.p("traducao_ptbr_wcusa", "x")[:-2]
        if info:
            with open(self.p("traducao_ptbr_wcusa", "mod_info", "traducao_ptbr_wcusa", "info.json"), "w") as f:
                f.write('{"name":"n","author":"a","version":"1","description":"d"}')
        for rel_path in files:
            with open(self.p("traducao_ptbr_wcusa", *rel_path.split("/")), "wb") as f:
                f.write(b"x")
        return root

    def test_correct_path_pass(self):
        root = self.make_mod(["assets/materials/signage/roadsigns/t_roadsigns_b.color.dds"])
        self.assertEqual(validate_mod_tree(root).status, PASS)

    def test_ptbr_suffix_fail(self):
        root = self.make_mod(["assets/materials/signage/roadsigns/t_roadsigns_b.color_ptbr.dds"])
        self.assertIn(FAIL, status_of(validate_mod_tree(root), "File name"))

    def test_unknown_path_fail(self):
        root = self.make_mod(["assets/materials/wrong/t_roadsigns_b.color.dds"])
        self.assertIn(FAIL, status_of(validate_mod_tree(root), "Asset path"))

    def test_missing_mod_info_fail(self):
        root = self.make_mod(["assets/materials/signage/roadsigns/t_roadsigns_b.color.dds"], info=False)
        self.assertIn(FAIL, status_of(validate_mod_tree(root), "mod_info"))

    def test_stray_file_fail(self):
        root = self.make_mod(["assets/materials/signage/roadsigns/Thumbs.db"])
        self.assertIn(FAIL, status_of(validate_mod_tree(root), "Stray file"))


class TestFamily(Tmp):
    def test_shape_changed_missing_aux_fail(self):
        open(self.p("pkg", "t_decal_roadmarkings_b.color.dds"), "wb").close()
        r = validate_family("t_decal_roadmarkings", "dir", self.p("pkg"), shape_changed=True)
        self.assertIn(FAIL, status_of(r, "shape_changed"))

    def test_shape_changed_complete_pass(self):
        for f in ("t_decal_roadmarkings_b.color.dds", "t_decal_roadmarkings_o.data.dds",
                  "t_decal_roadmarkings_nm.normal.dds", "t_decal_roadmarkings_ao.data.dds"):
            open(self.p("pkg", f), "wb").close()
        r = validate_family("t_decal_roadmarkings", "dir", self.p("pkg"), shape_changed=True)
        self.assertEqual(r.status, PASS)

    def test_undeclared_shape_warn(self):
        open(self.p("pkg", "t_roadsigns_b.color.dds"), "wb").close()
        r = validate_family("t_roadsigns", "dir", self.p("pkg"))
        self.assertIn(WARN, status_of(r, "shape_changed"))


class TestSpeed(unittest.TestCase):
    def test_conversion(self):
        self.assertAlmostEqual(kmh(mps(40)), 40)
        self.assertAlmostEqual(mps(40), 11.1111, places=4)

    def test_tolerance(self):
        self.assertTrue(same_speed(11.1111, 11.11111111))
        self.assertTrue(same_speed(11.1111, 11.14))
        self.assertFalse(same_speed(11.1111, 11.18 + 0.05))

    def test_multiple_of_10(self):
        self.assertTrue(is_multiple_of_10(13.8889))   # 50 km/h
        self.assertTrue(is_multiple_of_10(2.7778))    # 10 km/h
        self.assertFalse(is_multiple_of_10(13.4))     # 30 mph
        self.assertFalse(is_multiple_of_10(11.18))    # 25 mph
        self.assertFalse(is_multiple_of_10(15.6464))  # 35 mph

    def test_point_in_polygon(self):
        sq = [[0, 0], [10, 0], [10, 10], [0, 10]]
        self.assertTrue(point_in_polygon(5, 5, sq))
        self.assertFalse(point_in_polygon(15, 5, sq))


if __name__ == "__main__":
    unittest.main()
