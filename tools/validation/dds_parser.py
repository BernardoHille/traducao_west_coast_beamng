"""Pure-Python DDS header parser (no texconv dependency).

Reads DDS_HEADER (124 bytes after the 'DDS ' magic) and, when FourCC is 'DX10',
the DDS_HEADER_DXT10 extension. Reports format, colour space and mip chain.
"""
import math
import os
import struct

DDS_MAGIC = b"DDS "
DDPF_ALPHAPIXELS, DDPF_FOURCC, DDPF_RGB = 0x1, 0x4, 0x40

# DXGI_FORMAT -> (name, block bytes (0 = uncompressed), bits per pixel, srgb)
DXGI = {
    28: ("R8G8B8A8_UNORM", 0, 32, False), 29: ("R8G8B8A8_UNORM_SRGB", 0, 32, True),
    87: ("B8G8R8A8_UNORM", 0, 32, False), 91: ("B8G8R8A8_UNORM_SRGB", 0, 32, True),
    71: ("BC1_UNORM", 8, 4, False), 72: ("BC1_UNORM_SRGB", 8, 4, True),
    74: ("BC2_UNORM", 16, 8, False), 75: ("BC2_UNORM_SRGB", 16, 8, True),
    77: ("BC3_UNORM", 16, 8, False), 78: ("BC3_UNORM_SRGB", 16, 8, True),
    80: ("BC4_UNORM", 8, 4, False), 81: ("BC4_SNORM", 8, 4, False),
    83: ("BC5_UNORM", 16, 8, False), 84: ("BC5_SNORM", 16, 8, False),
    95: ("BC6H_UF16", 16, 8, False), 96: ("BC6H_SF16", 16, 8, False),
    98: ("BC7_UNORM", 16, 8, False), 99: ("BC7_UNORM_SRGB", 16, 8, True),
}
# Legacy FourCC -> (canonical name, block bytes). Legacy headers carry no colour-space flag.
FOURCC = {
    "DXT1": ("BC1_UNORM", 8), "DXT2": ("BC2_UNORM", 16), "DXT3": ("BC2_UNORM", 16),
    "DXT4": ("BC3_UNORM", 16), "DXT5": ("BC3_UNORM", 16),
    "BC4U": ("BC4_UNORM", 8), "ATI1": ("BC4_UNORM", 8), "BC4S": ("BC4_SNORM", 8),
    "BC5U": ("BC5_UNORM", 16), "ATI2": ("BC5_UNORM", 16), "BC5S": ("BC5_SNORM", 16),
}
ALPHA_MODES = {0: "UNKNOWN", 1: "STRAIGHT", 2: "PREMULTIPLIED", 3: "OPAQUE", 4: "CUSTOM"}


class DDSError(ValueError):
    pass


def full_mip_count(width, height):
    return int(math.floor(math.log2(max(width, height, 1)))) + 1


def expected_data_size(width, height, mips, block_bytes, bpp):
    total = 0
    for i in range(mips):
        w, h = max(1, width >> i), max(1, height >> i)
        if block_bytes:
            total += max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * block_bytes
        else:
            total += w * h * bpp // 8
    return total


def parse(path_or_bytes):
    data = path_or_bytes
    if isinstance(path_or_bytes, (str, os.PathLike)):
        with open(path_or_bytes, "rb") as f:
            data = f.read(148)
        file_size = os.path.getsize(path_or_bytes)
    else:
        file_size = len(data)
    if len(data) < 128 or data[:4] != DDS_MAGIC:
        raise DDSError("not a DDS file (missing 'DDS ' magic)")
    (size, flags, height, width, pitch, depth, mips) = struct.unpack_from("<7I", data, 4)
    if size != 124:
        raise DDSError(f"invalid DDS_HEADER size {size} (expected 124)")
    pf_size, pf_flags = struct.unpack_from("<2I", data, 76)
    fourcc = data[84:88].decode("ascii", "replace")
    rgb_bits = struct.unpack_from("<I", data, 88)[0]
    caps, caps2 = struct.unpack_from("<2I", data, 108)
    info = {"width": width, "height": height, "mip_count": max(1, mips), "mip_count_raw": mips,
            "header_flags": flags, "fourcc": fourcc.strip("\x00") if pf_flags & DDPF_FOURCC else "",
            "dx10": False, "dxgi": None, "alpha_mode": None, "array_size": 1, "file_size": file_size}
    header_len = 128
    if pf_flags & DDPF_FOURCC and fourcc == "DX10":
        if len(data) < 148:
            raise DDSError("DX10 FourCC but DDS_HEADER_DXT10 missing")
        dxgi, dim, misc, arr, misc2 = struct.unpack_from("<5I", data, 128)
        header_len = 148
        if dxgi not in DXGI:
            raise DDSError(f"unsupported DXGI format {dxgi}")
        name, block, bpp, srgb = DXGI[dxgi]
        info.update(dx10=True, dxgi=dxgi, format=name, block_bytes=block, bpp=bpp, srgb=srgb,
                    resource_dimension=dim, array_size=arr, alpha_mode=ALPHA_MODES.get(misc2 & 7, str(misc2 & 7)))
    elif pf_flags & DDPF_FOURCC:
        if fourcc not in FOURCC:
            raise DDSError(f"unsupported legacy FourCC '{fourcc}'")
        name, block = FOURCC[fourcc]
        info.update(format=name, block_bytes=block, bpp=block // 2, srgb=None)  # legacy: colour space not encoded
    elif pf_flags & DDPF_RGB:
        info.update(format=f"UNCOMPRESSED_{rgb_bits}BPP", block_bytes=0, bpp=rgb_bits, srgb=None)
    else:
        raise DDSError(f"unknown pixel format flags 0x{pf_flags:x}")
    info["family"] = info["format"].split("_")[0]
    info["full_mip_count"] = full_mip_count(width, height)
    info["expected_size"] = header_len + expected_data_size(width, height, info["mip_count"], info["block_bytes"], info["bpp"])
    info["colour_space"] = {True: "sRGB", False: "linear", None: "unspecified (legacy header)"}[info["srgb"]]
    return info


def describe(info):
    cs = info["colour_space"]
    return f"{info['width']}x{info['height']} {info['format']} ({'DX10' if info['dx10'] else 'legacy ' + info['fourcc']}) {cs}, {info['mip_count']} mips"


def build_header(width, height, mips, fmt, alpha_mode=0):
    """Synthetic DDS header for tests. fmt: DXGI int or legacy FourCC str."""
    flags = 0x1 | 0x2 | 0x4 | 0x1000 | (0x20000 if mips > 1 else 0) | 0x80000
    caps = 0x1000 | ((0x8 | 0x400000) if mips > 1 else 0)
    fourcc = b"DX10" if isinstance(fmt, int) else fmt.encode()
    head = DDS_MAGIC + struct.pack("<7I", 124, flags, height, width, 0, 0, mips) + b"\0" * 44
    head += struct.pack("<2I", 32, DDPF_FOURCC) + fourcc + b"\0" * 20
    head += struct.pack("<2I", caps, 0) + b"\0" * 12
    if isinstance(fmt, int):
        head += struct.pack("<5I", fmt, 3, 0, 1, alpha_mode)
    return head
