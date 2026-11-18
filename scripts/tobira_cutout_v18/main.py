"""Main entry point for Tobira-kun Cutout v18:
- Validates video FPS / CFR / frame count & mmap neural masks
- Compares straight RGBA vs Premultiplied `RGBa` Lanczos downscaling
- Streams frame-by-frame cutout + QC inspection + SBS/WebM encoding inside an isolated TemporaryDirectory
- Generates diagnostic sheets, full 124-frame JSON QC report, and verifies SHA-256 parity across all repos.
"""
import argparse
import json
import os
import sys
import tempfile
import time
import numpy as np
from PIL import Image, ImageDraw

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from tobira_cutout_v18.accessories import build_accessories
    from tobira_cutout_v18.alpha_refiner import refine_alpha_and_rgb, resize_rgba_exact_aspect
    from tobira_cutout_v18.character_mask import build_background_plate, build_character_body, measure_clean_trunk_geometry
    from tobira_cutout_v18.config import CoordinateGrid, CutoutConfig
    from tobira_cutout_v18.mask_loader import MaskPairLoader
    from tobira_cutout_v18.quality_check import SequenceQCInspector
    from tobira_cutout_v18.video_encoder import StreamingCutoutEncoder, install_outputs_atomically, verify_encoded_outputs
    from tobira_cutout_v18.video_loader import iter_video_frames, probe_video
else:
    from .accessories import build_accessories
    from .alpha_refiner import refine_alpha_and_rgb, resize_rgba_exact_aspect
    from .character_mask import build_background_plate, build_character_body, measure_clean_trunk_geometry
    from .config import CoordinateGrid, CutoutConfig
    from .mask_loader import MaskPairLoader
    from .quality_check import SequenceQCInspector
    from .video_encoder import StreamingCutoutEncoder, install_outputs_atomically, verify_encoded_outputs
    from .video_loader import iter_video_frames, probe_video


def composite_rgba_on_bg(im_rgba: Image.Image, bg_rgb: np.ndarray) -> np.ndarray:
    arr = np.asarray(im_rgba, dtype=np.float32)
    a = arr[..., 3:4] / 255.0
    return np.clip(arr[..., :3] * a + bg_rgb * (1.0 - a), 0, 255).astype(np.uint8)


def save_resize_comparison(clean_rgb: np.ndarray, alpha_u8: np.ndarray, cfg: CutoutConfig, out_path: str) -> None:
    """REVIEW ITEM #4: Compare straight RGBA resize vs premultiplied `RGBa` resize on green, dark navy, and title-plate."""
    out_w, out_h = cfg.out_size
    im_straight = resize_rgba_exact_aspect(clean_rgb, alpha_u8, cfg, premultiplied=False)
    im_premult = resize_rgba_exact_aspect(clean_rgb, alpha_u8, cfg, premultiplied=True)

    plate = np.asarray(
        Image.open(cfg.title_plate_path).convert("RGB").resize((out_w, out_h), Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    bgs = [
        ("green", np.broadcast_to(np.array([0.0, 230.0, 64.0], dtype=np.float32), (out_h, out_w, 3))),
        ("navy", np.broadcast_to(np.array([13.0, 24.0, 46.0], dtype=np.float32), (out_h, out_w, 3))),
        ("plate", plate),
    ]
    sheet = Image.new("RGB", (out_w * 3, out_h * 2))
    for col, (bname, bg_arr) in enumerate(bgs):
        for row, (im_r, mode_tag) in enumerate(((im_straight, "Straight RGBA"), (im_premult, "Premult RGBa"))):
            comp = Image.fromarray(composite_rgba_on_bg(im_r, bg_arr))
            d = ImageDraw.Draw(comp)
            d.rectangle([8, 8, 250, 38], fill=(0, 0, 0))
            d.text((14, 14), f"{mode_tag} ({bname})", fill=(255, 255, 0))
            sheet.paste(comp, (col * out_w, row * out_h))
    sheet.save(out_path, quality=95)


def run_pipeline(diag_dir: str = "/tmp/v18_diagnostics") -> dict:
    t0 = time.time()
    os.makedirs(diag_dir, exist_ok=True)
    cfg = CutoutConfig()

    meta = probe_video(cfg.video_path, expected_w=cfg.expected_src_size[0], expected_h=cfg.expected_src_size[1])
    print(
        f"[v18] Video verified: {meta.width}x{meta.height}, fps={meta.fps_str}, "
        f"frames={meta.nb_frames}, duration={meta.duration_sec:.3f}s, vfr={meta.is_vfr}",
        flush=True,
    )

    masks = MaskPairLoader(cfg.u2_mask_path, cfg.sil_mask_path, meta.nb_frames, meta.height, meta.width)
    grid = CoordinateGrid(meta.width, meta.height)

    print("[v18] Pass 1/2: Reconstructing clean background plate & measuring trunk geometry...", flush=True)
    bg_plate = build_background_plate(meta, cfg)
    geom = measure_clean_trunk_geometry(meta, masks, grid)

    sample25 = sorted(set(
        list(np.linspace(0, meta.nb_frames - 1, 16).round().astype(int))
        + [10, 14, 16, 36, 41, 46, 51, 62, 67, 92, 94, 97, 101]
    ))[:25]
    sample_set = set(sample25)
    diag_thumbs: dict[str, list[tuple[int, Image.Image]]] = {"green": [], "navy": [], "plate": []}

    out_w, out_h = cfg.out_size
    plate_out = np.asarray(
        Image.open(cfg.title_plate_path).convert("RGB").resize((out_w, out_h), Image.Resampling.LANCZOS),
        dtype=np.float32,
    )
    bg_defs = {
        "green": np.broadcast_to(np.array([0.0, 230.0, 64.0], dtype=np.float32), (out_h, out_w, 3)),
        "navy": np.broadcast_to(np.array([13.0, 24.0, 46.0], dtype=np.float32), (out_h, out_w, 3)),
        "plate": plate_out,
    }

    qc = SequenceQCInspector(meta.width, meta.height)

    print("[v18] Pass 2/2: Streaming frame cutout, QC inspection & isolated TemporaryDirectory encoding...", flush=True)
    with tempfile.TemporaryDirectory(prefix="tobira_cutout_v18_") as work_dir:
        encoder = StreamingCutoutEncoder(work_dir, meta, cfg)
        for fi, rgb in enumerate(iter_video_frames(meta)):
            u2f, silf = masks.get_normalized(fi)
            body = build_character_body(rgb, u2f, silf, fi, geom, bg_plate, grid)
            acc = build_accessories(rgb, u2f, silf, body, grid)
            clean_rgb, alpha_u8 = refine_alpha_and_rgb(rgb, u2f, body, acc, grid)

            qc.inspect_frame(fi, alpha_u8, body, acc)

            if fi == 14:
                save_resize_comparison(
                    clean_rgb, alpha_u8, cfg, os.path.join(diag_dir, "v18_resize_mode_compare_f014.jpg")
                )

            im_out = resize_rgba_exact_aspect(clean_rgb, alpha_u8, cfg, premultiplied=True)
            encoder.push_frame(fi, im_out)

            if fi in sample_set:
                for bname, bg_arr in bg_defs.items():
                    im_c = Image.fromarray(composite_rgba_on_bg(im_out, bg_arr))
                    d = ImageDraw.Draw(im_c)
                    d.rectangle([6, 6, 155, 36], fill=(0, 0, 0))
                    d.text((12, 12), f"v18 {bname} f{fi:03d}", fill=(255, 255, 0))
                    diag_thumbs[bname].append((fi, im_c))

        encoded_paths = encoder.finalize()
        stream_check = verify_encoded_outputs(encoded_paths, meta, cfg)
        installed = install_outputs_atomically(encoded_paths, cfg.output_dirs)

    cols, rows = 5, 5
    tw, th = 336, 588
    for bname, items in diag_thumbs.items():
        sheet = Image.new("RGB", (tw * cols, th * rows), (0, 0, 0))
        for k, (_, im_c) in enumerate(items[:25]):
            sheet.paste(im_c.resize((tw, th), Image.Resampling.LANCZOS), ((k % cols) * tw, (k // cols) * th))
        sp = os.path.join(diag_dir, f"v18_25f_{bname}.jpg")
        sheet.save(sp, quality=93)
        print(f"[v18] Saved diagnostic sheet: {sp}", flush=True)

    qc_summary = qc.summary_report()
    qc_summary["stream_verification"] = stream_check
    qc_summary["installed_files"] = installed
    qc_summary["elapsed_sec"] = round(time.time() - t0, 2)

    report_path = os.path.join(diag_dir, "v18_qc_report.json")
    with open(report_path, "w", encoding="utf-8") as fp:
        json.dump(qc_summary, fp, ensure_ascii=False, indent=2)

    print(
        f"[v18] Done in {qc_summary['elapsed_sec']}s | flagged_frames={qc_summary['flagged_frame_count']}/{meta.nb_frames} "
        f"| WebM alpha={stream_check['webm_alpha_verified']} | installed={len(installed)} files",
        flush=True,
    )
    return qc_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Tobira-kun Cutout v18")
    parser.add_argument("--diag-dir", default="/tmp/v18_diagnostics")
    args = parser.parse_args()
    run_pipeline(diag_dir=args.diag_dir)


if __name__ == "__main__":
    main()
