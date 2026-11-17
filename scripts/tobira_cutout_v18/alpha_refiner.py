"""Final mask assembly, signed-distance feathering, glare fix, edge color decontamination, and premultiplied RGBA resize."""
import cv2
import numpy as np
from PIL import Image
from .accessories import CharacterAccessories
from .character_mask import CharacterBodyParts
from .config import CoordinateGrid, CutoutConfig


def refine_alpha_and_rgb(
    rgb: np.ndarray,
    u2f: np.ndarray,
    body: CharacterBodyParts,
    acc: CharacterAccessories,
    grid: CoordinateGrid,
) -> tuple[np.ndarray, np.ndarray]:
    h, w = grid.h, grid.w
    yy, xx, yn, xn = grid.yy, grid.xx, grid.yn, grid.xn
    fi = body.fi
    ny0, ny1 = body.ny0, body.ny1
    head_x0, head_x1 = body.head_x0, body.head_x1

    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    rb_diff = r - b

    is_pencil_yellow = body.is_yellow_prop | (
        (35 <= fi <= 46) & (hue >= 15) & (hue <= 35) & (sat >= 92) & (val >= 106) & (r > b + 54)
    )

    blue_limbs_and_frame = (
        ((body.is_navy | body.is_door_cyan) & (~body.is_steel_room_wall) & body.shell_core)
        | body.is_standing_leg
        | body.is_jump_leg
        | acc.left_arm_bridge
        | acc.right_arm_bridge
    )
    if fi <= 35:
        sw_ring = (yy < ny0 + 330) & (acc.dist_to_head > 39.5)
        sw_right = (xx > head_x1 + 34) & (val > 165) & (~acc.tail_solid) & (~acc.right_arm_bridge)
        blue_limbs_and_frame = blue_limbs_and_frame & (~sw_ring) & (~sw_right)
    elif 39 <= fi <= 43:
        bg_cyan_veto = (
            (xx < 435) & (yy < ny0 + 340)
            & (((hue <= 108) & (g >= 74) & ((b - g) < 35)) | ((xx < 214) & (r >= 52)))
        )
        blue_limbs_and_frame = blue_limbs_and_frame & (~bg_cyan_veto)

    trunk_border = (acc.dist_to_head <= 7.5) & (yy >= ny0) & (yy <= ny1) & (u2f > 0.58)
    if not (35 <= fi <= 45):
        trunk_border = trunk_border & (xx >= head_x0 - 4) & (xx <= head_x1 + 4)

    fg_mask = (
        blue_limbs_and_frame | trunk_border | body.solid_body_interior
        | acc.pencil_solid | acc.tail_solid | acc.eraser_cube | acc.hp_all
    )

    pedestal_veto = (yn >= 0.742) & (~body.is_navy) & (~body.is_door_cyan) & (~body.is_standing_leg)
    spin_pedestal_veto = (38 <= fi <= 44) & (yn >= 0.695) & (rb_diff > 10) & (~body.is_standing_leg)
    cape_shadow_veto = (39 <= fi <= 48) & (xn < 0.34) & (yn > 0.54) & (r > b + 6) & (~is_pencil_yellow) & (~body.is_pink_eraser) & (~body.spin_cape)
    right_wall_veto = (xx >= 756) | (
        (44 <= fi <= 88)
        & (body.is_steel_room_wall | ((xx > head_x1 + 28) & (yy >= ny0 + 260) & (val < 68)))
        & (~acc.tail_solid) & (~acc.eraser_cube)
    )
    border_veto = ((xx < 5) | (xx > w - 5)) & (not (35 <= fi <= 45))

    fg_mask = fg_mask & (~pedestal_veto) & (~spin_pedestal_veto) & (~cape_shadow_veto) & (~right_wall_veto) & (~border_veto)

    fg_u8 = cv2.morphologyEx(
        fg_mask.astype(np.uint8) * 255,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
    )
    fg_u8 = cv2.morphologyEx(
        fg_u8,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
    )

    top_part = fg_u8.copy()
    top_part[int(0.70 * h):, :] = 0
    ff2 = top_part.copy()
    ff2_m = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff2, ff2_m, (0, 0), 128)
    holes = (ff2 == 0) & (yy < int(0.695 * h)) & (xx >= head_x0 - 20) & (xx <= head_x1 + 20)
    nh, h_lbl, h_stats, _ = cv2.connectedComponentsWithStats(holes.astype(np.uint8), connectivity=8)
    for hid in range(1, nh):
        if h_stats[hid, cv2.CC_STAT_AREA] < 1100:
            fg_u8[h_lbl == hid] = 255

    explicit_parts = (
        acc.pencil_solid | acc.tail_solid | acc.eraser_cube
        | body.open_door_fill | body.is_standing_leg | body.is_jump_leg
    )
    verified_prop = acc.pencil_solid | acc.tail_solid | acc.eraser_cube
    main_n, main_lbl, main_stats, _ = cv2.connectedComponentsWithStats((fg_u8 > 127).astype(np.uint8), connectivity=8)
    if main_n > 1:
        largest_id = 1 + int(np.argmax(main_stats[1:, cv2.CC_STAT_AREA]))
        main_comp = (main_lbl == largest_id)
        near_main = cv2.dilate(main_comp.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0
        near_main_prop = cv2.dilate(main_comp.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))) > 0
        clean_bin = np.zeros((h, w), dtype=np.uint8)
        for cid in range(1, main_n):
            area = main_stats[cid, cv2.CC_STAT_AREA]
            comp = (main_lbl == cid)
            keep = (
                cid == largest_id
                or (area >= 260 and (comp & explicit_parts).sum() >= 180 and (comp & near_main).any())
                or (area >= 320 and (comp & verified_prop).sum() >= 260 and (comp & near_main_prop).any())
                or ((43 <= fi <= 46) and area >= 700 and (comp & acc.pencil_solid).sum() >= 600)
            )
            if keep:
                clean_bin[comp] = 255
    else:
        clean_bin = fg_u8

    smooth_bin = (cv2.GaussianBlur(clean_bin.astype(np.float32), (5, 5), 1.15) > 128.0).astype(np.uint8) * 255

    dist_in = cv2.distanceTransform(smooth_bin, cv2.DIST_L2, 5)
    dist_out = cv2.distanceTransform(255 - smooth_bin, cv2.DIST_L2, 5)
    signed = dist_in - dist_out
    alpha = np.clip((signed - 0.65) / 1.45, 0.0, 1.0)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0.5)
    alpha = np.where(alpha < 0.02, 0.0, np.where(alpha > 0.985, 1.0, alpha))

    # REVIEW FIX #1: Apply glare softening strictly to `glare` / `glare_soft` pixels, NEVER `eye_band`!
    rgb_work = f.copy()
    if 11 <= fi <= 25:
        eye_band = (yy >= ny0 + 115) & (yy <= ny0 + 235) & (xx >= head_x0 + 45) & (xx <= head_x1 - 35)
        glare = eye_band & (r > 232) & (g > 205) & (b > 155)
        if glare.any():
            glare_soft = cv2.GaussianBlur(glare.astype(np.float32), (5, 5), 1.0)
            g_strength = np.clip((r - 222.0) / 33.0, 0.0, 1.0) * 0.35 * glare_soft
            target_tan = np.array([218.0, 176.0, 126.0], dtype=np.float32)
            rgb_work = rgb_work * (1.0 - g_strength[..., None]) + target_tan * g_strength[..., None]

    # Edge Color Decontamination: replace outer 4.5px RGB with nearest pure interior foreground pixel
    interior = (dist_in >= 4.5).astype(np.uint8)
    if interior.sum() > 100:
        _, labels_idx = cv2.distanceTransformWithLabels(1 - interior, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        flat_rgb = rgb_work[interior == 1]
        nearest_rgb = flat_rgb[np.clip(labels_idx - 1, 0, len(flat_rgb) - 1)]
        edge_blend = np.clip((4.5 - dist_in) / 3.6, 0.0, 1.0)[..., None]
        clean_rgb = np.clip(rgb_work * (1.0 - edge_blend) + nearest_rgb * edge_blend, 0, 255).astype(np.uint8)
    else:
        clean_rgb = np.clip(rgb_work, 0, 255).astype(np.uint8)

    return clean_rgb, (alpha * 255.0).round().astype(np.uint8)


def resize_rgba_exact_aspect(
    clean_rgb: np.ndarray,
    alpha_u8: np.ndarray,
    cfg: CutoutConfig,
    premultiplied: bool = True,
) -> Image.Image:
    """REVIEW ITEM #4: Resize `768x1344` (`4:7`) to `420x735` (`4:7` exact aspect ratio!) via premultiplied `RGBa` Lanczos,
    then pad 1 transparent row at the bottom to `420x736` even macroblock height."""
    out_w, out_h = cfg.out_size
    act_h = cfg.active_scaled_height
    rgba = np.concatenate([clean_rgb, alpha_u8[..., None]], axis=2)
    im_src = Image.fromarray(rgba, mode="RGBA")
    if premultiplied:
        im_scaled = im_src.convert("RGBa").resize((out_w, act_h), Image.Resampling.LANCZOS).convert("RGBA")
    else:
        im_scaled = im_src.resize((out_w, act_h), Image.Resampling.LANCZOS)

    if act_h == out_h:
        return im_scaled
    canvas = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    canvas.paste(im_scaled, (0, 0))
    return canvas
