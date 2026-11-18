"""Memory-mapped neural saliency mask loader with strict frame count, dimension, and value-range validation."""
import os
import numpy as np


class MaskPairLoader:
    """REVIEW ITEMS #3 & #6: Load `u2netp` & `silueta` `.npy` masks via `mmap_mode='r'` and validate shape & scale."""

    def __init__(self, u2_path: str, sil_path: str, expected_frames: int, expected_h: int, expected_w: int):
        for p in (u2_path, sil_path):
            if not os.path.isfile(p):
                raise FileNotFoundError(f"Required saliency mask file missing: {p}")

        self.u2 = np.load(u2_path, mmap_mode="r")
        self.sil = np.load(sil_path, mmap_mode="r")
        expected_shape = (expected_frames, expected_h, expected_w)

        if self.u2.shape != expected_shape:
            raise ValueError(f"u2netp mask shape {self.u2.shape} != expected {expected_shape}")
        if self.sil.shape != expected_shape:
            raise ValueError(f"silueta mask shape {self.sil.shape} != expected {expected_shape}")

        self._u2_scale = self._detect_scale(self.u2, "u2netp")
        self._sil_scale = self._detect_scale(self.sil, "silueta")

    @staticmethod
    def _detect_scale(arr: np.ndarray, name: str) -> float:
        sample = np.asarray(arr[::max(1, len(arr) // 8)], dtype=np.float32)
        vmin, vmax = float(sample.min()), float(sample.max())
        if vmin < -1e-4 or vmax > 255.001:
            raise ValueError(f"{name} mask values out of valid range [0, 255]: min={vmin}, max={vmax}")
        if vmax <= 1.0001:
            if vmax < 0.25:
                raise ValueError(f"{name} mask looks nearly empty (max={vmax})")
            return 1.0
        if vmax < 64.0:
            raise ValueError(f"{name} mask has suspicious maximum value {vmax}")
        return 255.0

    def get_normalized(self, fi: int) -> tuple[np.ndarray, np.ndarray]:
        u2f = np.clip(np.asarray(self.u2[fi], dtype=np.float32) / self._u2_scale, 0.0, 1.0)
        silf = np.clip(np.asarray(self.sil[fi], dtype=np.float32) / self._sil_scale, 0.0, 1.0)
        return u2f, silf
