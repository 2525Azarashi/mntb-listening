"""Streaming encoder (TemporaryDirectory PNGs + stdin SBS H.264), post-encode WebM alpha decode verification, and SHA-256 atomic installer."""
import hashlib
import json
import os
import shutil
import subprocess
from typing import Dict, Iterable, List
import numpy as np
from PIL import Image
from .config import CutoutConfig
from .video_loader import VideoMetadata


class StreamingCutoutEncoder:
    """REVIEW ITEMS #2, #7, #8:
    - Writes numbered RGBA PNGs inside an isolated TemporaryDirectory (`work_dir/frames/%04d.png`)
    - Streams side-by-side H.264 frames directly into `ffmpeg` stdin without holding `sbs_frames` in RAM
    - Uses dynamically probed `meta.fps_str` (`24/1`) instead of hardcoded FPS
    - Encodes silent (`-an`) VP9 `yuva420p` WebM + poster/end WebPs.
    """

    def __init__(self, work_dir: str, meta: VideoMetadata, cfg: CutoutConfig):
        self.work_dir = work_dir
        self.frames_dir = os.path.join(work_dir, "frames")
        os.makedirs(self.frames_dir, exist_ok=True)
        self.meta = meta
        self.cfg = cfg
        self.out_w, self.out_h = cfg.out_size
        self.matte_bg = np.array(cfg.matte_bg_rgb, dtype=np.float32).reshape((1, 1, 3))

        self.sbs_path = os.path.join(work_dir, "battle_countdown-sbs.mp4")
        self.webm_path = os.path.join(work_dir, "battle_countdown.webm")
        self.poster_path = os.path.join(work_dir, "battle_countdown-poster.webp")
        self.end_path = os.path.join(work_dir, "battle_countdown-end.webp")

        sbs_cmd = [
            "ffmpeg", "-y",
            "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{self.out_w}x{self.out_h * 2}",
            "-r", meta.fps_str,
            "-i", "pipe:0",
            "-an",
            "-c:v", "libx264",
            "-profile:v", "main",
            "-pix_fmt", "yuv420p",
            "-crf", "22",
            "-preset", "slow",
            "-movflags", "+faststart",
            self.sbs_path,
        ]
        self._sbs_proc = subprocess.Popen(sbs_cmd, stdin=subprocess.PIPE)
        self._count = 0
        self._first_rgba: Image.Image | None = None
        self._last_rgba: Image.Image | None = None

    def push_frame(self, fi: int, im_rgba: Image.Image) -> None:
        if fi != self._count:
            raise RuntimeError(f"Out-of-order frame push: got {fi}, expected {self._count}")
        png_path = os.path.join(self.frames_dir, f"{fi:04d}.png")
        im_rgba.save(png_path, format="PNG", compress_level=1)

        arr = np.asarray(im_rgba, dtype=np.float32)
        rgb = arr[..., :3]
        a_u8 = arr[..., 3].round().astype(np.uint8)
        af = arr[..., 3:4] / 255.0
        top_rgb = np.clip(rgb * af + self.matte_bg * (1.0 - af), 0, 255).round().astype(np.uint8)
        bot_rgb = np.repeat(a_u8[..., None], 3, axis=2)
        sbs_rgb = np.concatenate([top_rgb, bot_rgb], axis=0)

        assert self._sbs_proc.stdin is not None
        self._sbs_proc.stdin.write(sbs_rgb.tobytes())

        if fi == 0:
            self._first_rgba = im_rgba.copy()
        self._last_rgba = im_rgba
        self._count += 1

    def finalize(self) -> Dict[str, str]:
        if self._sbs_proc.stdin:
            self._sbs_proc.stdin.close()
        rc = self._sbs_proc.wait()
        if rc != 0:
            raise RuntimeError(f"SBS H.264 ffmpeg encode failed with exit code {rc}")
        if self._count != self.meta.nb_frames:
            raise RuntimeError(f"Encoded {self._count} frames != expected {self.meta.nb_frames}")

        # Encode VP9 yuva420p WebM from the isolated TemporaryDirectory PNG sequence (`-start_number 0`)
        webm_cmd = [
            "ffmpeg", "-y",
            "-hide_banner", "-loglevel", "error",
            "-framerate", self.meta.fps_str,
            "-start_number", "0",
            "-i", os.path.join(self.frames_dir, "%04d.png"),
            "-an",
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "0",
            "-crf", "28",
            "-row-mt", "1",
            "-auto-alt-ref", "0",
            "-lag-in-frames", "0",
            self.webm_path,
        ]
        subprocess.run(webm_cmd, check=True)

        assert self._first_rgba is not None and self._last_rgba is not None
        self._first_rgba.save(self.poster_path, format="WEBP", lossless=True, quality=100)
        self._last_rgba.save(self.end_path, format="WEBP", lossless=True, quality=100)

        return {
            "battle_countdown.webm": self.webm_path,
            "battle_countdown-sbs.mp4": self.sbs_path,
            "battle_countdown-poster.webp": self.poster_path,
            "battle_countdown-end.webp": self.end_path,
        }


def verify_encoded_outputs(paths: Dict[str, str], meta: VideoMetadata, cfg: CutoutConfig) -> dict:
    """REVIEW ITEM #9: Post-encode verification:
    - Confirm 0 audio streams and < 1,000,000 bytes on all 4 files
    - Confirm exact dimensions (WebM 420x736, vertical-stacked SBS MP4 420x1472) and frame counts
    - Decode WebM with explicit `-c:v libvpx-vp9 -pix_fmt rgba` to prove real `alpha_mode=1` transparency!
    """
    out_w, out_h = cfg.out_size
    results: dict = {}

    for fname, p in paths.items():
        sz = os.path.getsize(p)
        if sz >= 1_000_000:
            raise RuntimeError(f"{fname} size {sz} bytes exceeds 1,000,000-byte mobile budget!")

    for label, p, exp_w, exp_h in (
        ("webm", paths["battle_countdown.webm"], out_w, out_h),
        ("sbs", paths["battle_countdown-sbs.mp4"], out_w, out_h * 2),
    ):
        probe = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-count_frames",
                "-show_entries", "stream=codec_type,codec_name,width,height,pix_fmt,nb_read_frames,tags",
                "-of", "json", p,
            ],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(probe.stdout).get("streams", [])
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        if audio_streams:
            raise RuntimeError(f"{label} unexpectedly contains audio stream(s): {audio_streams}")
        if len(video_streams) != 1:
            raise RuntimeError(f"{label} expected 1 video stream, got {len(video_streams)}")
        vs = video_streams[0]
        if (int(vs["width"]), int(vs["height"])) != (exp_w, exp_h):
            raise RuntimeError(f"{label} size {(vs['width'], vs['height'])} != {(exp_w, exp_h)}")
        if int(vs["nb_read_frames"]) != meta.nb_frames:
            raise RuntimeError(f"{label} frame count {vs['nb_read_frames']} != {meta.nb_frames}")
        results[label] = {
            "codec": vs.get("codec_name"),
            "size": [int(vs["width"]), int(vs["height"])],
            "frames": int(vs["nb_read_frames"]),
            "audio_streams": 0,
            "tags": vs.get("tags", {}),
        }

    # Explicit libvpx-vp9 RGBA decode check across ALL frames to verify real transparency + non-empty foreground
    rgba_bytes = out_w * out_h * 4
    dec = subprocess.Popen(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-c:v", "libvpx-vp9",
            "-i", paths["battle_countdown.webm"],
            "-f", "rawvideo", "-pix_fmt", "rgba",
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
    )
    trans_ratios, opaq_ratios = [], []
    decoded_n = 0
    try:
        assert dec.stdout is not None
        while True:
            buf = dec.stdout.read(rgba_bytes)
            if not buf:
                break
            arr = np.frombuffer(buf, dtype=np.uint8).reshape((out_h, out_w, 4))
            a = arr[..., 3]
            trans_ratios.append(float((a <= 4).mean()))
            opaq_ratios.append(float((a >= 250).mean()))
            decoded_n += 1
    finally:
        if dec.stdout:
            dec.stdout.close()
        dec.wait()

    if decoded_n != meta.nb_frames:
        raise RuntimeError(f"libvpx-vp9 RGBA decode count {decoded_n} != {meta.nb_frames}")
    mean_trans = float(np.mean(trans_ratios))
    mean_opaq = float(np.mean(opaq_ratios))
    if mean_trans < 0.50 or mean_opaq < 0.12:
        raise RuntimeError(f"WebM alpha sanity failed: transparent_ratio={mean_trans:.4f}, opaque_ratio={mean_opaq:.4f}")

    results["webm_alpha_verified"] = True
    results["webm_mean_transparent_ratio"] = round(mean_trans, 4)
    results["webm_mean_opaque_ratio"] = round(mean_opaq, 4)
    return results


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def install_outputs_atomically(paths: Dict[str, str], dest_dirs: Iterable[str]) -> List[dict]:
    """REVIEW ITEM #9: Copy to `.tmp` in each target directory, verify SHA-256 parity, and `os.replace()` atomically."""
    installed: List[dict] = []
    src_hashes = {fname: _sha256_file(src) for fname, src in paths.items()}
    for d in dest_dirs:
        os.makedirs(d, exist_ok=True)
        for fname, src in paths.items():
            dst = os.path.join(d, fname)
            tmp_dst = f"{dst}.v18.tmp"
            shutil.copy2(src, tmp_dst)
            dst_hash = _sha256_file(tmp_dst)
            if dst_hash != src_hashes[fname]:
                os.unlink(tmp_dst)
                raise RuntimeError(f"SHA-256 mismatch while installing {dst}")
            os.replace(tmp_dst, dst)
            installed.append({
                "path": dst,
                "bytes": os.path.getsize(dst),
                "sha256": dst_hash[:16],
            })
    return installed
