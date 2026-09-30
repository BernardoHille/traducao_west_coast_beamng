"""PNG validation: candidate texture vs the original (resolution, alpha, pixel diff, allowed regions)."""
import os

from common import (FAIL, IMAGE_DIR, PASS, SKIP, WARN, Report, check_original_integrity, find_original,
                    load_config, rel, texture_stem, thresholds)
import image_diff


def allowed_regions(stem):
    entry = load_config("allowed_regions.json").get(stem)
    return (entry or {}).get("regions", [])


def validate_png(candidate, original=None, regions=None, heatmap=True, report=None, verify_manifest=True):
    t = thresholds()
    stem = texture_stem(candidate)
    rep = report or Report("PNG validation", rel(candidate))
    if not os.path.exists(candidate):
        rep.add(FAIL, "Candidate", f"file not found: {candidate}")
        return rep
    row = None
    if original is None:
        original, row = find_original(stem, "png")
        if original is None:
            rep.add(FAIL, "Original lookup", f"no original PNG named '{stem}' in the manifest")
            return rep
    if verify_manifest and row is not None and not check_original_integrity(rep, original, row):
        return rep
    if regions is None:
        regions = allowed_regions(stem)
    rep.meta.update(original=rel(original), texture=stem, allowed_regions=len(regions))

    orig = image_diff.load_rgba(original)
    cand = image_diff.load_rgba(candidate)
    (oh, ow), (ch, cw) = orig.shape[:2], cand.shape[:2]
    if (ow, oh) != (cw, ch):
        rep.add(FAIL, "Resolution", f"{cw}x{ch} differs from original {ow}x{oh} (no up/downscale allowed)")
        return rep
    rep.add(PASS, "Resolution", f"{cw}x{ch}")

    m = image_diff.compare(orig, cand, regions, t["pixel_rgb_tolerance"], t["alpha_tolerance"])
    a = m["alpha"]
    rep.meta["metrics"] = {k: v for k, v in m.items() if not k.startswith("_")}

    # --- alpha: transparency preserved outside allowed regions
    inside_mask = image_diff.region_mask(orig.shape, regions)
    ao, ac = orig[..., 3], cand[..., 3]
    tr = (ao == 0) & ~inside_mask
    n_tr = int(tr.sum())
    if n_tr:
        lost = int((tr & (ac > t["alpha_tolerance"])).sum())
        pct = lost * 100 / n_tr
        if cand[..., 3].min() >= 255 - t["alpha_tolerance"] and ao.min() < 255:
            rep.add(FAIL, "Alpha preservation", f"original has transparency ({a['original']['transparent_pct']}% alpha=0) but candidate is fully opaque")
        elif pct > t["alpha_transparent_loss_fail_pct"]:
            rep.add(FAIL, "Alpha preservation", f"{pct:.1f}% of originally transparent pixels outside allowed regions lost transparency ({lost} px)")
        elif lost:
            rep.add(WARN, "Alpha preservation", f"{lost} originally transparent pixels ({pct:.3f}%) changed outside allowed regions")
        else:
            rep.add(PASS, "Alpha preservation", f"all {n_tr} transparent pixels outside allowed regions preserved")
    else:
        rep.add(SKIP, "Alpha preservation", "original has no fully transparent pixels outside allowed regions")

    semi = (ao > 0) & (ao < 255) & ~inside_mask
    n_semi = int(semi.sum())
    if n_semi:
        changed = int((semi & (abs(ac - ao) > t["alpha_tolerance"])).sum())
        pct = changed * 100 / n_semi
        st = FAIL if pct > t["alpha_semi_change_fail_pct"] else (WARN if changed else PASS)
        rep.add(st, "Semi-transparency", f"{pct:.2f}% of {n_semi} originally semi-transparent pixels changed outside allowed regions")
    else:
        rep.add(SKIP, "Semi-transparency", "original has no semi-transparent pixels outside allowed regions")

    noise = a["opaque_pixels_modified_outside"]
    if noise > t["alpha_opaque_noise_fail_pixels"]:
        rep.add(FAIL, "Alpha noise", f"{noise} originally opaque pixels outside allowed regions now have alpha < 255 (candidate alpha min {a['candidate']['min']})")
    elif noise:
        rep.add(WARN, "Alpha noise", f"{noise} originally opaque pixels outside allowed regions lost full opacity")
    else:
        rep.add(PASS, "Alpha noise", "no opaque pixel lost opacity outside allowed regions")

    # --- pixel diff inside/outside allowed regions
    rep.add(PASS, "Pixel diff (global, informative)",
            f"{m['changed_any_pct']}% changed · RGB mean {m['rgb']['mean_abs']} max {m['rgb']['max_abs']}"
            f" · alpha mean {a['mean_abs']} max {a['max_abs']} · PSNR {m['rgb']['psnr_db'] or '∞'} dB · bbox {m['bbox_changes']}")
    out_pct = m["changed_outside_pct"]
    label = "Changes outside allowed regions" if regions else "Changes (no allowed regions configured)"
    if out_pct > t["outside_region_change_fail_pct"]:
        rep.add(FAIL, label, f"{out_pct}% of pixels outside allowed regions changed ({m['changed_outside_regions']} px, bbox {m['bbox_changes_outside']})")
    elif out_pct > t["outside_region_change_warn_pct"]:
        rep.add(WARN, label, f"{out_pct}% of pixels outside allowed regions changed ({m['changed_outside_regions']} px)")
    else:
        rep.add(PASS, label, f"{m['changed_outside_regions']} px changed outside; {m['changed_inside_regions']} px inside {len(regions)} region(s)")

    if heatmap and m["changed_any"]:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        base = os.path.join(IMAGE_DIR, os.path.splitext(os.path.basename(candidate))[0])
        image_diff.save_heatmaps(m, orig, base + "_diff.png", base + "_alpha_diff.png")
        rep.meta["heatmaps"] = [rel(base + "_diff.png"), rel(base + "_alpha_diff.png")]
    return rep
