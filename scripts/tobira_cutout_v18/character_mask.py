"""Body, legs, swung-out door leaf, head dome, and cape reconstruction for Tobira-kun Cutout v18."""
from dataclasses import dataclass
import cv2
import numpy as np
from .config import CoordinateGrid, CutoutConfig
from .mask_loader import MaskPairLoader
from .video_loader import VideoMetadata, iter_video_frames, read_frame_subset


def fill_hull(mask_bool: np.ndarray, erode_px: int = 0) -> np.ndarray:
    pts = np.column_stack(np.where(mask_bool)[::-1])
    if len(pts) < 12:
        return mask_bool
    hm = np.zeros(mask_bool.shape, dtype=np.uint8)
    cv2.fillConvexPoly(hm, cv2.convexHull(pts), 255)
    if erode_px > 0:
        hm = cv2.erode(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_px * 2 + 1, erode_px * 2 + 1)))
    return hm > 0


@dataclass(frozen=True)
class TrunkGeometry:
    ny0: np.ndarray
    ny1: np.ndarray
    hx0: np.ndarray
    hx1: np.ndarray


def build_background_plate(meta: VideoMetadata, cfg: CutoutConfig) -> np.ndarray:
    c0, c1 = cfg.bg_calm_range
    j0, j1 = cfg.bg_jump_range
    if j1 > meta.nb_frames or c1 > meta.nb_frames:
        raise ValueError(f"Background sample ranges {cfg.bg_calm_range} / {cfg.bg_jump_range} exceed nb_frames={meta.nb_frames}")
    need = set(range(c0, c1)) | set(range(j0, j1))
    sub = read_frame_subset(meta, need)
    bg_plate = np.median([sub[i] for i in range(c0, c1)], axis=0).astype(np.float32)
    bg_jump = np.median([sub[i] for i in range(j0, j1)], axis=0).astype(np.float32)
    x0, y0, x1, y1 = cfg.bg_patch_box
    bg_plate[y0:y1, x0:x1] = bg_jump[y0:y1, x0:x1]
    return bg_plate


def measure_clean_trunk_geometry(meta: VideoMetadata, masks: MaskPairLoader, grid: CoordinateGrid) -> TrunkGeometry:
    ny0_arr, ny1_arr, hx0_arr, hx1_arr = [], [], [], []
    yy, xx, yn = grid.yy, grid.xx, grid.yn
    ell5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    for fi, rgb in enumerate(iter_video_frames(meta)):
        f = rgb.astype(np.float32)
        r, b = f[..., 0], f[..., 2]
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
        hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
        u2f, _ = masks.get_normalized(fi)

        rich_blue = (
            (hue >= 92) & (hue <= 138) & (sat >= 55) & (b > r + 22)
            & (val >= 45) & (val <= 215) & (u2f > 0.60) & (yn > 0.03) & (yn < 0.742)
        )
        rb_u8 = cv2.morphologyEx(rich_blue.astype(np.uint8) * 255, cv2.MORPH_OPEN, ell5)
        rb_central = (rb_u8 > 0) & (xx >= 165) & (xx <= 605)
        if rb_central.sum() > 500:
            ys, xs = np.where(rb_central)
            y0 = int(np.percentile(ys, 1))
            y1 = int(np.percentile(ys, 99))
            h_mask = rb_central & (yy >= y0) & (yy <= y0 + 230)
            if h_mask.sum() > 200:
                _, hxs = np.where(h_mask)
                x0, x1 = int(np.percentile(hxs, 2)), int(np.percentile(hxs, 98))
            else:
                x0, x1 = int(np.percentile(xs, 3)), int(np.percentile(xs, 97))
        else:
            y0, y1, x0, x1 = 300, 960, 220, 548
        ny0_arr.append(y0)
        ny1_arr.append(y1)
        hx0_arr.append(x0)
        hx1_arr.append(x1)

    def med5(arr):
        a = np.array(arr, dtype=np.float32)
        out = np.empty_like(a)
        for i in range(len(a)):
            out[i] = np.median(a[max(0, i - 2):min(len(a), i + 3)])
        return out.round().astype(int)

    return TrunkGeometry(ny0=med5(ny0_arr), ny1=med5(ny1_arr), hx0=med5(hx0_arr), hx1=med5(hx1_arr))


@dataclass
class CharacterBodyParts:
    fi: int
    ny0: int
    ny1: int
    head_x0: int
    head_x1: int
    body_cx: float
    head_rx: float
    is_navy: np.ndarray
    is_door_cyan: np.ndarray
    is_cool_white: np.ndarray
    is_yellow_prop: np.ndarray
    is_pink_eraser: np.ndarray
    is_steel_room_wall: np.ndarray
    is_standing_leg: np.ndarray
    is_jump_leg: np.ndarray
    shell_core: np.ndarray
    geom_trunk: np.ndarray
    open_door_fill: np.ndarray
    spin_cape: np.ndarray
    solid_body_interior: np.ndarray
    bg_rgb_diff: np.ndarray


def build_character_body(
    rgb: np.ndarray,
    u2f: np.ndarray,
    silf: np.ndarray,
    fi: int,
    geom: TrunkGeometry,
    bg_plate: np.ndarray,
    grid: CoordinateGrid,
) -> CharacterBodyParts:
    h, w = grid.h, grid.w
    yy, xx, yn, xn = grid.yy, grid.xx, grid.yn, grid.xn

    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    neural = np.maximum(u2f, silf)
    rb_diff = r - b
    rg_diff = r - g

    ny0, ny1 = int(geom.ny0[fi]), int(geom.ny1[fi])
    head_x0, head_x1 = int(geom.hx0[fi]), int(geom.hx1[fi])
    body_cx = 0.5 * (head_x0 + head_x1)
    head_rx = max(110.0, 0.5 * (head_x1 - head_x0))
    bg_rgb_diff = np.linalg.norm(f - bg_plate, axis=2)

    is_navy = (
        ((hue >= 92) & (hue <= 148) & (sat >= 34) & (b > r + 8) & (val >= 54) & (val < 224))
        | ((hue >= 92) & (hue <= 152) & (sat >= 26) & (b >= r + 2) & (val >= 18) & (val < 62) & (u2f > 0.55))
        | ((hue >= 100) & (hue <= 152) & (sat >= 26) & (b >= r + 1) & (val >= 32) & (val <= 150) & (u2f > 0.50))
    )
    is_door_cyan = (hue >= 86) & (hue <= 118) & (sat >= 40) & (b > r + 14) & (val >= 70)

    # Standing & landing legs (`fi <= 43` or `fi >= 88`) separated cleanly against reconstructed `bg_plate`
    is_landing_glow = (89 <= fi <= 101)
    leg_center_ok = True if (38 <= fi <= 43) else (
        ((xx >= body_cx - 106) & (xx <= body_cx - 42))
        | ((xx >= body_cx + 42) & (xx <= body_cx + 102))
    )
    in_standing_leg_box = (
        (not (44 <= fi <= 89))
        & leg_center_ok
        & (yy >= ny1 - 26) & (yn <= (0.760 if (38 <= fi <= 43) else 0.768))
    )
    darker_than_pedestal = (
        ((bg_plate[..., 0] - r) > 40.0)
        & ((bg_plate[..., 1] - g) > 38.0)
        & (val < (186 if is_landing_glow else 178))
    )
    is_standing_leg_raw = (
        in_standing_leg_box
        & (
            darker_than_pedestal
            | ((val < 155) & (b >= r - 30) & (neural > 0.14))
        )
    )
    is_standing_leg = np.zeros((h, w), dtype=bool)
    if is_standing_leg_raw.any():
        nsl, sl_lbl, sl_stats, _ = cv2.connectedComponentsWithStats(
            cv2.dilate(is_standing_leg_raw.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 11))),
            connectivity=8,
        )
        for sid in range(1, nsl):
            stop = sl_stats[sid, cv2.CC_STAT_TOP]
            sw_b = sl_stats[sid, cv2.CC_STAT_WIDTH]
            sarea = sl_stats[sid, cv2.CC_STAT_AREA]
            if stop <= ny1 + 28 and sw_b <= 72 and sarea >= 120:
                is_standing_leg |= (is_standing_leg_raw & (sl_lbl == sid))

    # Bottom horizontal navy threshold bar (`0 <= fi <= 35` or `88 <= fi <= 104`) + lower crouch tan door face (`88 <= fi <= 104`)
    landing_bottom_bar = (
        ((fi <= 35) | (88 <= fi <= 104))
        & (xx >= head_x0 + 6) & (xx <= head_x1 - 6)
        & (yy >= ny1 - 24) & (yy <= min(int(0.746 * h), ny1 + 48))
        & ((u2f > 0.36) | (silf > 0.72))
        & (val < 188) & ((bg_plate[..., 0] - r) > 34.0)
    )
    crouch_lower_tan_fill = (
        (88 <= fi <= 104)
        & (xx >= head_x0 + 8) & (xx <= head_x1 - 8)
        & (yy >= ny1 - 12) & (yy <= min(int(0.738 * h), ny1 + 38))
        & (u2f > 0.72) & (silf > 0.78)
    )

    # Airborne jump legs (`44 <= fi <= 89`)
    left_leg_zone = (xx >= body_cx - 102) & (xx <= body_cx - 24)
    right_leg_zone = (xx >= body_cx + 22) & (xx <= body_cx + 92)
    in_jump_leg_box = (
        (44 <= fi <= 89)
        & (left_leg_zone | right_leg_zone)
        & (yy >= ny1 - 24) & (yy <= min(int(0.735 * h), ny1 + 98))
    )
    not_dark_brown_pillar = ~((xx >= body_cx + 10) & (rb_diff > 18) & (neural < 0.06))
    leg_darker_than_bg = ((bg_plate[..., 0] - r) > 52.0) & ((bg_plate[..., 1] - g) > 45.0) & (val <= 155)
    is_jump_leg_raw = (
        in_jump_leg_box
        & not_dark_brown_pillar
        & (val >= 14) & (val <= 165)
        & (~((r > 165) & (g > 138)))
        & (
            ((b >= r + 4) & (hue >= 96) & (hue <= 152))
            | ((b >= r - 24) & (neural > 0.06))
            | (leg_darker_than_bg & (b >= r - 28) & (yy <= ny1 + 94))
        )
    )
    is_jump_leg = np.zeros((h, w), dtype=bool)
    if is_jump_leg_raw.any():
        njl, jl_lbl, jl_stats, _ = cv2.connectedComponentsWithStats(
            cv2.dilate(is_jump_leg_raw.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 13))),
            connectivity=8,
        )
        for jid in range(1, njl):
            jtop = jl_stats[jid, cv2.CC_STAT_TOP]
            jw = jl_stats[jid, cv2.CC_STAT_WIDTH]
            jarea = jl_stats[jid, cv2.CC_STAT_AREA]
            if jtop <= ny1 + 22 and jw <= 96 and jarea >= 110:
                comp = is_jump_leg_raw & (jl_lbl == jid)
                is_jump_leg |= fill_hull(comp, erode_px=0) & in_jump_leg_box & (~((r > 175) & (g > 150)))

    is_cool_white = (sat <= 32) & (val >= 126) & (rb_diff <= 20)
    is_yellow_prop = (hue >= 17) & (hue <= 33) & (sat >= 128) & (val >= 115) & (r > b + 80) & (g > b + 50)
    is_pink_eraser = ((hue <= 12) | (hue >= 164)) & (sat >= 46) & (rg_diff >= 26) & ((g - b) <= 22) & (val >= 126) & (xn < 0.32)
    is_dark_feature = (val < 76) & (u2f > 0.68) & (yn > 0.05) & (yn < 0.772) & (
        ~(
            (44 <= fi <= 88)
            & ((xx < head_x0 - 20) | (xx > head_x1 + 20))
            & (yy >= ny0 + 260)
        )
    )

    is_steel_room_wall = (
        ((xx > head_x1 + 32) & (g >= 84) & ((b - g) <= 36) & (u2f < 0.52))
        | ((44 <= fi <= 88) & (xx > head_x1 + 36) & (yy >= ny0 + 280) & (val < 62))
    )
    jump_arm_blue_ok = (
        (44 <= fi <= 88)
        & (is_navy | is_door_cyan)
        & (~is_steel_room_wall)
        & (
            (u2f > 0.50)
            | (
                (yy >= ny0 + 135) & (yy <= ny0 + 335)
                & (xx >= max(18, head_x0 - 145)) & (xx <= min(685, head_x1 + 130))
                & (b > r + 26) & (sat >= 120) & (val >= 42) & (bg_rgb_diff > 38.0)
            )
        )
    )
    door_blue_ok = (
        (u2f > 0.50)
        | jump_arm_blue_ok
        | ((34 <= fi <= 46) & ((u2f > 0.44) | (is_door_cyan & (silf > 0.32) & (xn < 0.58))))
    )

    shell_raw = (
        ((is_navy | is_door_cyan) & door_blue_ok & (yn > 0.03) & (yn < 0.785))
        | is_standing_leg
        | landing_bottom_bar
        | crouch_lower_tan_fill
        | is_jump_leg
        | (is_cool_white & (u2f > 0.52) & (yn > 0.03) & (yn < 0.75))
        | ((is_yellow_prop | is_pink_eraser) & ((neural > 0.20) | (44 <= fi <= 88)) & (yn > 0.10) & (yn < 0.72))
        | is_dark_feature
    )
    if not (36 <= fi <= 45):
        outside_upper_arch = (yy < ny0 + 165) & ((xx < head_x0 - 44) | (xx > head_x1 + 44)) & (~is_yellow_prop) & (~is_pink_eraser)
        shell_raw = shell_raw & (~outside_upper_arch)
    else:
        shell_raw = shell_raw & (~((yy < ny0 - 20) & ((xx < 110) | (xx > w - 110))))

    bridged = cv2.dilate(shell_raw.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    num_l, labels, stats, _ = cv2.connectedComponentsWithStats(bridged, connectivity=8)
    valid_bridge = np.zeros((h, w), dtype=bool)
    for lid in range(1, num_l):
        area = stats[lid, cv2.CC_STAT_AREA]
        top = stats[lid, cv2.CC_STAT_TOP]
        bot = top + stats[lid, cv2.CC_STAT_HEIGHT]
        if area > 4500 and top < int(0.62 * h) and bot > int(0.32 * h):
            valid_bridge |= (labels == lid)
    shell_core = shell_raw & valid_bridge

    arch_cy = ny0 + int(head_rx * 0.96)
    in_rect_part = (xx >= head_x0 + 6) & (xx <= head_x1 - 6) & (yy >= arch_cy) & (yy <= ny1 - 6)
    in_arch_dome = (
        (yy >= ny0 + 5) & (yy <= arch_cy + 4)
        & (((xx - body_cx) / max(1.0, head_rx - 5.0)) ** 2 + ((yy - arch_cy) / max(1.0, (arch_cy - ny0) - 5.0)) ** 2 <= 1.0)
    )

    if not (35 <= fi <= 45):
        geom_trunk = ((in_rect_part | in_arch_dome) & (u2f > 0.50)) | crouch_lower_tan_fill
    else:
        not_bg_cyan_arch = ~(
            (39 <= fi <= 42)
            & (xx < 435) & (yy < ny0 + 340)
            & (
                ((hue <= 108) & (g >= 74) & ((b - g) < 35))
                | ((xx < 214) & (r >= 52))
            )
        )
        spin_blue = (is_navy | is_door_cyan) & not_bg_cyan_arch & (u2f > 0.62) & (xx >= 155) & (xx <= 725) & (yy >= ny0 - 4) & (yy <= ny1 + 8)
        spin_head_body = spin_blue & (xx <= 565)
        geom_trunk = fill_hull(spin_head_body, erode_px=2) & (u2f > 0.56) & not_bg_cyan_arch
        shell_core = shell_core & not_bg_cyan_arch

    open_door_fill = np.zeros((h, w), dtype=bool)
    if 35 <= fi <= 39:
        door_zone = (xx >= 6) & (xx <= head_x0 + 35) & (yy >= ny0 + 150) & (yy <= ny1 + 28)
        cyan_door_px = door_zone & (
            ((hue >= 88) & (hue <= 116) & (sat >= 42) & (b > r + 18) & (val >= 68) & ((silf >= 0.05) | (u2f >= 0.08)))
            | is_yellow_prop
        )
        nd_c, nd_lbl, nd_stats, _ = cv2.connectedComponentsWithStats(
            cv2.dilate(cyan_door_px.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))),
            connectivity=8,
        )
        if nd_c > 1:
            best_d = 1 + int(np.argmax(nd_stats[1:, cv2.CC_STAT_AREA]))
            if nd_stats[best_d, cv2.CC_STAT_AREA] >= 1600:
                dcomp = cyan_door_px & (nd_lbl == best_d)
                lys, lxs = np.where(dcomp)
                leaf_solid = fill_hull(dcomp, erode_px=1)
                rx_leaf = int(np.percentile(lxs, 97))
                y_top_h = int(np.percentile(lys, 22))
                y_bot_h = int(np.percentile(lys, 82))
                bridge_im = leaf_solid.astype(np.uint8) * 255
                cv2.line(bridge_im, (rx_leaf - 4, y_top_h), (head_x0 + 34, y_top_h), 255, thickness=12)
                cv2.line(bridge_im, (rx_leaf - 4, y_bot_h), (head_x0 + 34, y_bot_h), 255, thickness=12)
                open_door_fill = bridge_im > 0
    elif 40 <= fi <= 43:
        rdoor_zone = (xx >= 490) & (xx <= 725) & (yy >= ny0 + 125) & (yy <= ny1 + 25)
        rcyan = rdoor_zone & ((is_door_cyan | is_yellow_prop) & (u2f > 0.72) & (silf > 0.72))
        if rcyan.sum() >= 1200:
            open_door_fill = fill_hull(rcyan, erode_px=1) & (u2f > 0.65)

    spin_side_tan = (
        (36 <= fi <= 39)
        & ((u2f > 0.68) | (silf > 0.72))
        & (yy >= ny0 + 25) & (yy <= ny1 - 8)
        & (xx >= max(45, head_x0 - 45)) & (xx <= head_x1 + 10)
        & (r > b + 28) & (sat >= 48) & (val >= 108) & (val <= 235)
    )

    spin_cape = np.zeros((h, w), dtype=bool)
    if 39 <= fi <= 48:
        cape_cand = (
            (xx < head_x0 + 40) & (yy >= ny0 + 165) & (yy <= ny1 + 22)
            & ((u2f > 0.56) | (silf > 0.58))
            & (b >= r - 4) & (val >= 30) & (val <= 168) & (rb_diff <= 4)
        )
        anchor_strip = geom_trunk & (xx <= head_x0 + 36) & (yy >= ny0 + 210) & (yy <= ny1 - 16)
        if cape_cand.sum() >= 260:
            cape_hull = fill_hull(cape_cand | anchor_strip, erode_px=0)
            spin_cape = cape_hull & (~((r > b + 8) & (val > 98)))

    standing_cape_fill = np.zeros((h, w), dtype=bool)
    if fi <= 35 or fi >= 89:
        for side in ("left", "right"):
            if side == "left":
                cz = (xx >= head_x0 - 82) & (xx <= head_x0 + 14) & (yy >= ny1 - 210) & (yy <= ny1 + 8)
            else:
                cz = (xx >= head_x1 - 14) & (xx <= head_x1 + 82) & (yy >= ny1 - 210) & (yy <= ny1 + 8)
            cape_px = cz & ((is_navy | is_door_cyan) | ((val < 72) & (b >= r - 4))) & ((u2f > 0.35) | (silf > 0.35))
            if cape_px.sum() >= 350:
                standing_cape_fill |= (fill_hull(cape_px, erode_px=1) & (~((r > b + 12) & (val > 95))))

    jump_cape_fill = np.zeros((h, w), dtype=bool)
    if 49 <= fi <= 88:
        for side in ("left", "right"):
            if side == "left":
                cz = (xx >= max(16, head_x0 - 155)) & (xx <= head_x0 + 16) & (yy >= ny0 + 250) & (yy <= ny1 + 8)
                on_valid = (neural > 0.14) | ((bg_plate[..., 0] - bg_plate[..., 2]) > 22.0)
                c_px = cz & (~is_steel_room_wall) & on_valid & (hue >= 98) & (hue <= 140) & (b > r + 20) & (val >= 46) & (val <= 165)
            else:
                cz = (xx >= head_x1 - 16) & (xx <= min(668, head_x1 + 102)) & (yy >= ny0 + 275) & (yy <= ny1 + 4)
                # Right side above arch rim has dark starry night (`val < 58, silf == 0`); require genuine bright slate-blue cape (`val >= 60, b > r + 24`)!
                on_valid = (silf > 0.20) | ((u2f > 0.55) & (xx <= head_x1 + 78)) | (((bg_plate[..., 0] - bg_plate[..., 2]) > 24.0) & (xx <= head_x1 + 74))
                c_px = cz & (~is_steel_room_wall) & on_valid & (hue >= 98) & (hue <= 136) & (b > r + 24) & (val >= 60) & (val <= 162)
            if c_px.sum() >= 220:
                jump_cape_fill |= (fill_hull(c_px, erode_px=1) & (~((r > 165) & (rb_diff > 24))) & (~((xx > head_x1 + 42) & (val < 56))))

    solid_body_interior = (
        geom_trunk | open_door_fill | spin_side_tan | spin_cape
        | standing_cape_fill | landing_bottom_bar | crouch_lower_tan_fill | jump_cape_fill
    )

    return CharacterBodyParts(
        fi=fi,
        ny0=ny0,
        ny1=ny1,
        head_x0=head_x0,
        head_x1=head_x1,
        body_cx=body_cx,
        head_rx=head_rx,
        is_navy=is_navy,
        is_door_cyan=is_door_cyan,
        is_cool_white=is_cool_white,
        is_yellow_prop=is_yellow_prop,
        is_pink_eraser=is_pink_eraser,
        is_steel_room_wall=is_steel_room_wall,
        is_standing_leg=is_standing_leg,
        is_jump_leg=is_jump_leg,
        shell_core=shell_core,
        geom_trunk=geom_trunk,
        open_door_fill=open_door_fill,
        spin_cape=spin_cape,
        solid_body_interior=solid_body_interior,
        bg_rgb_diff=bg_rgb_diff,
    )
