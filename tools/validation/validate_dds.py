"""DDS validation: header metadata of a candidate vs the original DDS."""
import os
import re

import dds_parser
from common import FAIL, PASS, SKIP, WARN, Report, check_original_integrity, find_original, rel, texture_stem

DATA_MAP = re.compile(r"(_o\.data|_r\.data|_ao\.data|_m\.data|\.normal|_nm\b)", re.I)
COMPATIBLE_ALPHA = {frozenset({"UNKNOWN", "STRAIGHT"}), frozenset({"UNKNOWN", "OPAQUE"})}


def validate_dds(candidate, original=None, report=None, verify_manifest=True):
    rep = report or Report("DDS validation", rel(candidate))
    stem = texture_stem(candidate)
    if not os.path.exists(candidate):
        rep.add(FAIL, "Candidate", f"file not found: {candidate}")
        return rep
    try:
        c = dds_parser.parse(candidate)
    except dds_parser.DDSError as e:
        rep.add(FAIL, "DDS header", str(e))
        return rep
    rep.add(PASS, "DDS header", dds_parser.describe(c))

    row = None
    if original is None:
        original, row = find_original(stem, "dds")
    if original is None:
        rep.add(SKIP, "Original comparison", f"no original DDS named '{stem}' in the manifest (standalone checks only)")
        o = None
    else:
        if verify_manifest and row is not None and not check_original_integrity(rep, original, row):
            return rep
        o = dds_parser.parse(original)
        rep.meta.update(original=rel(original), original_format=dds_parser.describe(o))

    if c["file_size"] < c["expected_size"]:
        rep.add(FAIL, "File size", f"{c['file_size']} bytes < {c['expected_size']} expected for the declared mip chain (truncated)")
    elif c["file_size"] > c["expected_size"]:
        rep.add(WARN, "File size", f"{c['file_size']} bytes > {c['expected_size']} expected (extra data)")
    else:
        rep.add(PASS, "File size", f"{c['file_size']} bytes consistent with header")

    if c["mip_count"] <= 1 and c["full_mip_count"] > 1:
        rep.add(FAIL, "Mipmaps", f"no mip chain (1 level, {c['full_mip_count']} expected)")
    elif o and c["mip_count"] != o["mip_count"]:
        rep.add(FAIL, "Mipmaps", f"{c['mip_count']} levels vs original {o['mip_count']}")
    elif c["mip_count"] != c["full_mip_count"]:
        rep.add(WARN, "Mipmaps", f"{c['mip_count']} levels; full chain to 1x1 would be {c['full_mip_count']}")
    else:
        rep.add(PASS, "Mipmaps", f"{c['mip_count']} (full chain to 1x1)")

    if DATA_MAP.search(stem) and c["srgb"] is True:
        rep.add(FAIL, "Colour space (data map)", f"'{stem}' is a data/normal map but the DDS is sRGB ({c['format']})")

    if not o:
        return rep
    if (c["width"], c["height"]) != (o["width"], o["height"]):
        rep.add(FAIL, "Resolution", f"{c['width']}x{c['height']} vs original {o['width']}x{o['height']}")
    else:
        rep.add(PASS, "Resolution", f"{c['width']}x{c['height']}")
    if c["format"] != o["format"]:
        rep.add(FAIL, "DDS format", f"{c['format']} vs original {o['format']}")
    else:
        rep.add(PASS, "DDS format", c["format"])
    if c["srgb"] is None or o["srgb"] is None:
        if c["dx10"] != o["dx10"]:
            rep.add(WARN, "Colour space", f"header type differs (candidate {'DX10' if c['dx10'] else 'legacy'}, original {'DX10' if o['dx10'] else 'legacy'})")
        else:
            rep.add(PASS, "Colour space", "legacy header on both (colour space not encoded)")
    elif c["srgb"] != o["srgb"]:
        rep.add(FAIL, "Colour space", f"{c['colour_space']} vs original {o['colour_space']}")
    else:
        rep.add(PASS, "Colour space", c["colour_space"])
    if c["dx10"] and o["dx10"] and c["alpha_mode"] != o["alpha_mode"]:
        pair = frozenset({c["alpha_mode"], o["alpha_mode"]})
        st = PASS if pair in COMPATIBLE_ALPHA else FAIL
        rep.add(st, "DX10 alpha mode", f"{c['alpha_mode']} vs original {o['alpha_mode']}" + (" (compatible)" if st == PASS else ""))
    return rep
