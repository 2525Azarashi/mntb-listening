"""Automated 124-frame quality control (area, centroid, contour IoU, accessory continuity, alpha flicker) for v18."""
from dataclasses import asdict, dataclass, field
from typing import Any
import numpy as np
from .accessories import CharacterAccessories
from .character_mask import CharacterBodyParts


@dataclass
class FrameQCMetrics:
    frame: int
    area_px: int
    centroid_x: float
    centroid_y: float
    bbox: tuple[int, int, int, int]
    pencil_px: int
    tail_px: int
    hp_px: int
    leg_px: int
    iou_prev: float
    area_delta_pct: float
    centroid_step_px: float
    alpha_mad_prev: float
    warnings: list[str] = field(default_factory=list)


class SequenceQCInspector:
    """REVIEW ITEM #5: Tracks per-frame metrics across all frames without keeping full-resolution frame buffers in memory."""

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self._prev_bin: np.ndarray | None = None
        self._prev_alpha_f: np.ndarray | None = None
        self._prev_cx: float | None = None
        self._prev_cy: float | None = None
        self._prev_area: int | None = None
        self.records: list[FrameQCMetrics] = []

    @staticmethod
    def _is_rapid_motion_phase(fi: int) -> bool:
        return (34 <= fi <= 55) or (86 <= fi <= 101)

    @staticmethod
    def _is_3d_spin_phase(fi: int) -> bool:
        return 37 <= fi <= 43

    def inspect_frame(
        self,
        fi: int,
        alpha_u8: np.ndarray,
        body: CharacterBodyParts,
        acc: CharacterAccessories,
    ) -> FrameQCMetrics:
        fg = alpha_u8 >= 128
        area = int(fg.sum())
        alpha_f = alpha_u8.astype(np.float32) / 255.0

        if area > 0:
            ys, xs = np.where(fg)
            cx, cy = float(xs.mean()), float(ys.mean())
            bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        else:
            cx, cy = self.w * 0.5, self.h * 0.5
            bbox = (0, 0, 0, 0)

        pencil_px = int((acc.pencil_solid & fg).sum())
        tail_px = int((acc.tail_solid & fg).sum())
        hp_px = int((acc.hp_all & fg).sum())
        leg_region = np.zeros_like(fg)
        leg_region[
            max(0, body.ny1 - 12):min(self.h, body.ny1 + 95),
            max(0, body.head_x0 + 25):min(self.w, body.head_x1 - 25),
        ] = True
        leg_px = int((fg & leg_region).sum())

        if self._prev_bin is not None and self._prev_area and self._prev_area > 0:
            inter = int((fg & self._prev_bin).sum())
            union = max(1, int((fg | self._prev_bin).sum()))
            iou_prev = float(inter / union)
            area_delta_pct = abs(area - self._prev_area) * 100.0 / float(self._prev_area)
            centroid_step = float(np.hypot(cx - (self._prev_cx or cx), cy - (self._prev_cy or cy)))
            alpha_mad = float(np.mean(np.abs(alpha_f - self._prev_alpha_f)))
        else:
            iou_prev = 1.0
            area_delta_pct = 0.0
            centroid_step = 0.0
            alpha_mad = 0.0

        rapid = self._is_rapid_motion_phase(fi)
        spin3d = self._is_3d_spin_phase(fi)
        warns: list[str] = []

        if area < 95_000:
            warns.append(f"character_area_too_small({area})")
        if not spin3d:
            if area_delta_pct > (24.0 if rapid else 11.0):
                warns.append(f"area_jump({area_delta_pct:.1f}%)")
            if centroid_step > (56.0 if rapid else 18.0):
                warns.append(f"centroid_jump({centroid_step:.1f}px)")
            if iou_prev < (0.62 if rapid else 0.84):
                warns.append(f"contour_iou_drop({iou_prev:.3f})")
            if alpha_mad > (0.095 if rapid else 0.040):
                warns.append(f"alpha_flicker_mad({alpha_mad:.4f})")

            # Accessory presence checks outside 3D back-spin (`37 <= fi <= 43`)
            if pencil_px < 450:
                warns.append(f"pencil_low({pencil_px}px)")
            if tail_px < 350:
                warns.append(f"tail_low({tail_px}px)")
            if leg_px < 350:
                warns.append(f"legs_low({leg_px}px)")

        if hp_px < 1200:
            warns.append(f"headphone_low({hp_px}px)")

        rec = FrameQCMetrics(
            frame=fi,
            area_px=area,
            centroid_x=round(cx, 2),
            centroid_y=round(cy, 2),
            bbox=bbox,
            pencil_px=pencil_px,
            tail_px=tail_px,
            hp_px=hp_px,
            leg_px=leg_px,
            iou_prev=round(iou_prev, 4),
            area_delta_pct=round(area_delta_pct, 2),
            centroid_step_px=round(centroid_step, 2),
            alpha_mad_prev=round(alpha_mad, 5),
            warnings=warns,
        )
        self.records.append(rec)
        self._prev_bin = fg
        self._prev_alpha_f = alpha_f
        self._prev_cx = cx
        self._prev_cy = cy
        self._prev_area = area
        return rec

    def summary_report(self) -> dict[str, Any]:
        flagged = [r for r in self.records if r.warnings]
        return {
            "total_frames": len(self.records),
            "flagged_frame_count": len(flagged),
            "flagged_frames": [{"frame": r.frame, "warnings": r.warnings} for r in flagged],
            "min_area_px": min((r.area_px for r in self.records), default=0),
            "max_area_px": max((r.area_px for r in self.records), default=0),
            "max_calm_area_delta_pct": max(
                (r.area_delta_pct for r in self.records if not self._is_rapid_motion_phase(r.frame)),
                default=0.0,
            ),
            "min_calm_iou_prev": min(
                (r.iou_prev for r in self.records if r.frame > 0 and not self._is_rapid_motion_phase(r.frame)),
                default=1.0,
            ),
            "frames": [asdict(r) for r in self.records],
        }
