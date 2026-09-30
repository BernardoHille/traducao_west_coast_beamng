"""Pixel and alpha comparison between an original PNG and a candidate PNG."""
import numpy as np
from PIL import Image


def load_rgba(path):
    with Image.open(path) as im:
        return np.asarray(im.convert("RGBA"), dtype=np.int16)


def region_mask(shape, regions):
    """Boolean mask (H, W) that is True inside any allowed region {x, y, width, height}."""
    h, w = shape[:2]
    mask = np.zeros((h, w), dtype=bool)
    for r in regions or []:
        x0, y0 = max(0, int(r["x"])), max(0, int(r["y"]))
        x1, y1 = min(w, x0 + int(r["width"])), min(h, y0 + int(r["height"]))
        mask[y0:y1, x0:x1] = True
    return mask


def alpha_stats(a):
    n = a.size
    return {"transparent_pct": round(float((a == 0).sum()) * 100 / n, 3),
            "semi_pct": round(float(((a > 0) & (a < 255)).sum()) * 100 / n, 3),
            "opaque_pct": round(float((a == 255).sum()) * 100 / n, 3),
            "min": int(a.min()), "max": int(a.max()), "mean": round(float(a.mean()), 3)}


def _bbox(mask):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return {"x": int(xs.min()), "y": int(ys.min()), "width": int(xs.max() - xs.min() + 1), "height": int(ys.max() - ys.min() + 1)}


def _psnr(a, b):
    mse = float(((a.astype(np.float64) - b) ** 2).mean())
    return None if mse == 0 else round(10 * np.log10(255 ** 2 / mse), 2)


def compare(orig, cand, regions=None, rgb_tol=0, alpha_tol=0):
    """Return diff metrics. orig/cand: int16 arrays (H, W, 4) of equal shape."""
    rgb_d = np.abs(orig[..., :3] - cand[..., :3]).max(axis=2)
    a_o, a_c = orig[..., 3], cand[..., 3]
    a_d = np.abs(a_o - a_c)
    rgb_changed = rgb_d > rgb_tol
    a_changed = a_d > alpha_tol
    any_changed = rgb_changed | a_changed
    inside = region_mask(orig.shape, regions)
    outside = ~inside
    n = any_changed.size
    n_out = int(outside.sum())

    def pct(x, base):
        return round(float(x) * 100 / base, 4) if base else 0.0

    opaque, transp = a_o == 255, a_o == 0
    semi = ~opaque & ~transp
    return {
        "pixels": n,
        "rgb": {"changed": int(rgb_changed.sum()), "changed_pct": pct(rgb_changed.sum(), n),
                "mean_abs": round(float(rgb_d.mean()), 4), "max_abs": int(rgb_d.max()),
                "psnr_db": _psnr(orig[..., :3], cand[..., :3])},
        "alpha": {"changed": int(a_changed.sum()), "changed_pct": pct(a_changed.sum(), n),
                  "mean_abs": round(float(a_d.mean()), 4), "max_abs": int(a_d.max()),
                  "original": alpha_stats(a_o), "candidate": alpha_stats(a_c),
                  "opaque_pixels_modified": int((opaque & (a_c < 255 - alpha_tol)).sum()),
                  "opaque_pixels_modified_outside": int((opaque & outside & (a_c < 255 - alpha_tol)).sum()),
                  "transparent_pixels_modified": int((transp & (a_c > alpha_tol)).sum()),
                  "semi_transparent_pixels_modified": int((semi & a_changed).sum()),
                  "transparent_pixels_original": int(transp.sum()),
                  "semi_pixels_original": int(semi.sum())},
        "changed_any": int(any_changed.sum()),
        "changed_any_pct": pct(any_changed.sum(), n),
        "changed_inside_regions": int((any_changed & inside).sum()),
        "changed_outside_regions": int((any_changed & outside).sum()),
        "changed_outside_pct": pct((any_changed & outside).sum(), n_out),
        "outside_area_pixels": n_out,
        "bbox_changes": _bbox(any_changed),
        "bbox_changes_outside": _bbox(any_changed & outside),
        "_masks": (rgb_d, a_d, inside),
    }


def save_heatmaps(metrics, orig, out_rgb, out_alpha, gain=4):
    """Diff heatmaps: grey original, red = RGB change, allowed regions outlined in green."""
    rgb_d, a_d, inside = metrics["_masks"]
    base = (orig[..., :3].mean(axis=2) * 0.35).astype(np.uint8)
    img = np.stack([base, base, base], axis=2)
    heat = np.clip(rgb_d * gain, 0, 255).astype(np.uint8)
    img[..., 0] = np.maximum(img[..., 0], heat)
    edge = inside & ~np.roll(inside, 1, 0) | inside & ~np.roll(inside, 1, 1) | inside & ~np.roll(inside, -1, 0) | inside & ~np.roll(inside, -1, 1)
    img[edge] = (0, 255, 0)
    Image.fromarray(img).save(out_rgb)
    ah = np.clip(a_d * gain, 0, 255).astype(np.uint8)
    aimg = np.stack([base, base, base], axis=2)
    aimg[..., 2] = np.maximum(aimg[..., 2], ah)
    aimg[edge] = (0, 255, 0)
    Image.fromarray(aimg).save(out_alpha)
