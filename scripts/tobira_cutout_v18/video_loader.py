"""Dynamic ffprobe metadata verification and memory-efficient RGB24 streaming decoder."""
from dataclasses import dataclass
from fractions import Fraction
import json
import subprocess
from typing import Dict, Iterator, Set
import numpy as np


@dataclass(frozen=True)
class VideoMetadata:
    path: str
    width: int
    height: int
    fps_str: str
    fps_float: float
    avg_fps_str: str
    nb_frames: int
    duration_sec: float
    is_vfr: bool


def probe_video(path: str, expected_w: int = 768, expected_h: int = 1344) -> VideoMetadata:
    """REVIEW ITEM #8: Dynamically probe FPS, CFR/VFR, dimensions, and exact frame count via ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames,nb_frames,duration",
        "-of", "json",
        path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(proc.stdout)
    streams = info.get("streams") or []
    if not streams:
        raise ValueError(f"No video stream found in {path}")
    st = streams[0]
    w = int(st["width"])
    h = int(st["height"])
    if (w, h) != (expected_w, expected_h):
        raise ValueError(f"Unexpected video dimensions {(w, h)} != {(expected_w, expected_h)} in {path}")

    r_fps_str = st.get("r_frame_rate", "24/1")
    avg_fps_str = st.get("avg_frame_rate", r_fps_str)
    r_fps = float(Fraction(r_fps_str))
    avg_fps = float(Fraction(avg_fps_str)) if avg_fps_str not in ("0/0", "") else r_fps
    is_vfr = abs(r_fps - avg_fps) > 0.05

    nb_str = st.get("nb_read_frames") or st.get("nb_frames")
    if not nb_str:
        raise ValueError(f"Could not determine exact frame count for {path}")
    nb_frames = int(nb_str)
    dur = float(st.get("duration") or (nb_frames / r_fps))

    if is_vfr:
        raise ValueError(
            f"VFR source video detected (r_frame_rate={r_fps_str}, avg_frame_rate={avg_fps_str}); "
            "convert to CFR first so neural mask alignment cannot drift."
        )

    return VideoMetadata(
        path=path,
        width=w,
        height=h,
        fps_str=r_fps_str,
        fps_float=r_fps,
        avg_fps_str=avg_fps_str,
        nb_frames=nb_frames,
        duration_sec=dur,
        is_vfr=is_vfr,
    )


def iter_video_frames(meta: VideoMetadata) -> Iterator[np.ndarray]:
    """REVIEW ITEM #6: Stream raw RGB24 frames one-by-one via `-fps_mode passthrough` without storing all frames in RAM."""
    frame_bytes = meta.width * meta.height * 3
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", meta.path,
        "-fps_mode", "passthrough",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "pipe:1",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    count = 0
    try:
        assert proc.stdout is not None
        while True:
            buf = proc.stdout.read(frame_bytes)
            if not buf:
                break
            if len(buf) != frame_bytes:
                raise RuntimeError(f"Truncated RGB24 frame at index {count}: got {len(buf)} bytes, expected {frame_bytes}")
            arr = np.frombuffer(buf, dtype=np.uint8).reshape((meta.height, meta.width, 3)).copy()
            count += 1
            yield arr
    finally:
        if proc.stdout:
            proc.stdout.close()
        rc = proc.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg decode failed with exit code {rc}")
    if count != meta.nb_frames:
        raise RuntimeError(f"Decoded frame count {count} != ffprobe nb_frames {meta.nb_frames}")


def read_frame_subset(meta: VideoMetadata, indices: Set[int]) -> Dict[int, np.ndarray]:
    """Stream through the video once and retain only the requested frame indices."""
    if not indices:
        return {}
    max_idx = max(indices)
    out: Dict[int, np.ndarray] = {}
    frame_bytes = meta.width * meta.height * 3
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", meta.path,
        "-fps_mode", "passthrough",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "pipe:1",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    try:
        assert proc.stdout is not None
        fi = 0
        while fi <= max_idx:
            buf = proc.stdout.read(frame_bytes)
            if not buf:
                break
            if fi in indices:
                out[fi] = np.frombuffer(buf, dtype=np.uint8).reshape((meta.height, meta.width, 3)).copy()
            fi += 1
    finally:
        if proc.stdout:
            proc.stdout.close()
        proc.terminate()
        proc.wait()
    missing = indices - set(out.keys())
    if missing:
        raise RuntimeError(f"Missing requested frame indices: {sorted(missing)}")
    return out
