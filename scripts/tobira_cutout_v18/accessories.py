"""Pencil, golden triangle tail, eraser cube, and headphone reconstruction for Tobira-kun Cutout v18."""
from dataclasses import dataclass
import cv2
import numpy as np
from .character_mask import CharacterBodyParts, fill_hull
from .config import CoordinateGrid


@dataclass
class CharacterAccessories:
    pencil_solid: np.ndarray
    left_arm_bridge: np.ndarray
    tail_solid: np.ndarray
    right_arm_bridge: np.ndarray
    eraser_cube: np.ndarray
    hp_all: np.ndarray
    dist_to_head: np.ndarray


def build_accessories(
    rgb: np.ndarray,
    u2f: np.ndarray,
    silf: np.ndarray,
    body: CharacterBodyParts,
    grid: CoordinateGrid,
) -> CharacterAccessories:
    h, w = grid.h, grid.w
    yy, xx, yn, xn = grid.yy, grid.xx, grid.yn, grid.xn
    fi = body.fi
    ny0, ny1 = body.ny0, body.ny1
    head_x0, head_x1 = body.head_x0, body.head_x1

    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    neural = np.maximum(u2f, silf)
    rb_diff = r - b
    rg_diff = r - g

    # (a) Left-hand Pencil + Clean Blue Wrist Bridge
    # Include spin-entry (`35 <= fi <= 46`) and backlit settle frames (`f010, f101`) where `sat >= 98` and `bg_rgb_diff > 36`!
    is_pencil_yellow = (
        body.is_yellow_prop
        | ((35 <= fi <= 46) & (hue >= 15) & (hue <= 35) & (sat >= 92) & (val >= 106) & (r > b + 54))
        | ((xn < 0.34) & (hue >= 16) & (hue <= 34) & (sat >= 108) & (val >= 112) & (r > b + 66) & (g > b + 38))
    )
    pencil_y_max = min(int(0.725 * h), ny1 + 14)
    pencil_neural_ok = (
        (neural > 0.24)
        | ((47 <= fi <= 88) & (yy <= ny0 + 360))
        | ((35 <= fi <= 37) & (body.bg_rgb_diff > 38.0) & (sat >= 120))
        | ((body.bg_rgb_diff > 44.0) & (sat >= 135) & (r > b + 82))
    )
    pencil_shaft = (
        (is_pencil_yellow | body.is_pink_eraser)
        & pencil_neural_ok
        & (xn < 0.36) & (yy >= max(80, ny0 + 20)) & (yy <= pencil_y_max)
    )
    if fi <= 34:
        pencil_shaft = pencil_shaft & (xx >= head_x0 - 98)

    pencil_solid = np.zeros((h, w), dtype=bool)
    left_arm_bridge = np.zeros((h, w), dtype=bool)
    if pencil_shaft.any():
        np_c, np_lbl, np_stats, _ = cv2.connectedComponentsWithStats(
            cv2.dilate(pencil_shaft.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 17))),
            connectivity=8,
        )
        best_p, best_score = 0, 0.0
        for pid in range(1, np_c):
            comp = pencil_shaft & (np_lbl == pid)
            ph = np_stats[pid, cv2.CC_STAT_HEIGHT]
            if comp.sum() >= 25 and ph <= 245:
                sc = float(comp.sum()) * (0.5 + float(neural[comp].mean()))
                if sc > best_score:
                    best_score = sc
                    best_p = pid
        if best_p > 0:
            pencil_shaft = pencil_shaft & (np_lbl == best_p)
            pys, pxs = np.where(pencil_shaft)
            pts_p = np.column_stack([pxs, pys]).astype(np.float32)
            if len(pts_p) >= 15:
                vx, vy, x0p, y0p = cv2.fitLine(pts_p, cv2.DIST_L2, 0, 0.01, 0.01).flatten()
                if vy < 0:
                    vx, vy = -vx, -vy
                proj = (pxs - x0p) * vx + (pys - y0p) * vy
                t_min, t_max = float(proj.min()) - 28.0, float(proj.max()) + 24.0
                p1 = (int(round(x0p + vx * t_min)), int(round(y0p + vy * t_min)))
                p2 = (int(round(x0p + vx * t_max)), int(round(y0p + vy * t_max)))
                capsule = np.zeros((h, w), dtype=np.uint8)
                cv2.line(capsule, p1, p2, 255, thickness=24)
                near_eraser = cv2.dilate(
                    body.is_pink_eraser.astype(np.uint8),
                    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)),
                ) > 0
                is_ferrule = near_eraser & (sat <= 32) & (val >= 135) & (np.abs(rb_diff) <= 18)
                tip_dist2 = (xx - p2[0]) ** 2 + (yy - p2[1]) ** 2
                is_graphite = (tip_dist2 <= 26 ** 2) & (val < 95) & ((u2f > 0.45) | (silf > 0.45))
                cap_neural_ok = (
                    (neural > 0.28)
                    | (47 <= fi <= 88)
                    | ((35 <= fi <= 37) & (body.bg_rgb_diff > 36.0))
                    | ((body.bg_rgb_diff > 42.0) & (sat >= 125))
                )
                pencil_solid = (capsule > 0) & (yy <= pencil_y_max + 18) & cap_neural_ok & (
                    is_pencil_yellow | body.is_pink_eraser | is_ferrule | is_graphite
                    | ((u2f > 0.72) & (silf > 0.72) & (sat >= 75) & (val < 210))
                )
                pencil_solid = fill_hull(pencil_solid, erode_px=0) & (capsule > 0)

                if not (37 <= fi <= 42):
                    grip_x = int(round(np.median(pxs)))
                    grip_y = int(round(np.percentile(pys, 56 if fi <= 43 or fi >= 90 else 65)))
                    sh_x = int(head_x0 + 18)
                    sh_y = int(np.clip(grip_y + (16 if fi <= 36 or fi >= 90 else 42), ny0 + 210, ny1 - 45))
                    arm_tube = np.zeros((h, w), dtype=np.uint8)
                    cv2.line(arm_tube, (grip_x, grip_y), (sh_x, sh_y), 255, thickness=20)
                    thin_conn = np.zeros((h, w), dtype=np.uint8)
                    cv2.line(thin_conn, (grip_x + 4, grip_y), (sh_x, sh_y), 255, thickness=14)
                    not_bright_arch = ~((r > 212) & (g > 188) & (rb_diff > 36))
                    left_arm_bridge = (
                        ((arm_tube > 0) & ((b >= r - 8) | (val < 118)) & ((silf > 0.24) | (u2f > 0.24) | (43 <= fi <= 88)))
                        | ((thin_conn > 0) & not_bright_arch & ((silf > 0.35) | (u2f > 0.30) | (body.bg_rgb_diff > 32.0)))
                    )

    # (b) Right-side Golden Triangle Tail + Solid Curved Tail Cord
    # Note: during high jump (`55 <= fi <= 75`), `ny0` rises to ~100 while the triangle tail sits at `y=270..430` (`x <= 755`),
    # whereas the background golden swirl ring + tan block sit below `y >= ny0 + 380` (`y >= 480`)!
    tail_y_max = (ny0 + 385) if (48 <= fi <= 82) else min(int(0.72 * h), ny1 - 6)
    is_tail_yellow = (
        body.is_yellow_prop
        | ((36 <= fi <= 98) & (hue >= 16) & (hue <= 34) & (sat >= 106) & (val >= 118) & (r > b + 62) & (g > b + 34))
        | ((xx >= head_x1 + 38) & (hue >= 16) & (hue <= 35) & (sat >= 104) & (val >= 118) & (r > b + 62) & (g > b + 34))
    )
    tail_neural_ok = (neural > 0.20) | (
        (body.bg_rgb_diff > 34.0) & (~((r > 235) & (g > 215) & (b > 175)))
    )
    tail_seed = (
        is_tail_yellow & tail_neural_ok
        & (xx > head_x1 + 6) & (xx < min(w - 6, head_x1 + 195))
        & (yy > max(40, ny0 + 105)) & (yy < tail_y_max)
    )
    tail_solid = np.zeros((h, w), dtype=bool)
    right_arm_bridge = np.zeros((h, w), dtype=bool)
    if tail_seed.any():
        nt_c, nt_lbl, nt_stats, _ = cv2.connectedComponentsWithStats(
            cv2.dilate(tail_seed.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))),
            connectivity=8,
        )
        best_t, best_area = 0, 0
        for tid in range(1, nt_c):
            ty = nt_stats[tid, cv2.CC_STAT_TOP]
            tw = nt_stats[tid, cv2.CC_STAT_WIDTH]
            th = nt_stats[tid, cv2.CC_STAT_HEIGHT]
            tarea = nt_stats[tid, cv2.CC_STAT_AREA]
            # Exclude bottom-right golden swirl ring (`ty > ny0 + 480` during jump `44 <= fi <= 88`)!
            max_tail_top = (ny0 + 480) if (44 <= fi <= 88) else (ny1 - 12)
            if ty <= max_tail_top and 16 <= tw <= 136 and 16 <= th <= 165 and tarea >= 140 and tarea > best_area:
                best_area = tarea
                best_t = tid
        if best_t > 0:
            t_core = tail_seed & (nt_lbl == best_t)
            near_tail = cv2.dilate(t_core.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (14, 14))) > 0
            tail_yellow = near_tail & (hue >= 15) & (hue <= 35) & (sat >= 98) & (r > b + 56) & (
                (neural > 0.22) | (body.bg_rgb_diff > 32.0)
            )
            tail_yellow = fill_hull(tail_yellow, erode_px=0)
            tail_cord = near_tail & (body.is_navy | body.is_door_cyan) & (~body.is_steel_room_wall)
            tail_solid = tail_yellow | tail_cord

            tys, txs = np.where(tail_yellow)
            if len(txs) >= 10 and not (37 <= fi <= 42):
                tx0 = int(np.percentile(txs, 8))
                ty0 = int(np.percentile(tys, 72))
                sh_rx = int(head_x1 - 14)
                sh_ry = int(min(ny1 - 42, ty0 + 34))
                cord_tube = np.zeros((h, w), dtype=np.uint8)
                cv2.line(cord_tube, (sh_rx, sh_ry), (tx0 + 4, ty0), 255, thickness=22)
                thin_rcord = np.zeros((h, w), dtype=np.uint8)
                cv2.line(thin_rcord, (sh_rx, sh_ry), (tx0 + 4, ty0), 255, thickness=12)
                not_warm_arch = ~((r > 205) & (g > 180) & (rb_diff > 34))
                right_arm_bridge = (
                    ((cord_tube > 0) & (~body.is_steel_room_wall) & ((b > r + 12) | ((val < 122) & (rb_diff <= 10))))
                    | ((thin_rcord > 0) & (~body.is_steel_room_wall) & not_warm_arch & ((neural > 0.25) | (body.bg_rgb_diff > 30.0)))
                )

    # (c) Right-hand Eraser Cube (`fi >= 42`)
    right_arm_blue = (
        (body.is_navy | body.is_door_cyan) & (~body.is_steel_room_wall) & (body.shell_core | right_arm_bridge)
        & (xx > head_x1 - 12) & (xx < min(685, head_x1 + 150))
        & (yy > ny0 + 130) & (yn < 0.725)
    )
    eraser_cube = np.zeros((h, w), dtype=bool)
    if fi >= 42 and right_arm_blue.any():
        near_rhand = cv2.dilate(
            right_arm_blue.astype(np.uint8),
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)),
        ) > 0
        eraser_y_max = (ny0 + 465) if (48 <= fi <= 82) else int(0.725 * h)
        hand_zone = near_rhand & (yy > ny0 + 145) & (yy < eraser_y_max) & (xx <= min(688, head_x1 + 155))
        is_ew = (val >= 178) & (sat <= 22) & (np.abs(rb_diff) <= 14)
        is_ep = ((hue <= 12) | (hue >= 164)) & (sat >= 46) & (sat <= 135) & (rg_diff >= 30) & ((g - b) <= 20) & (val >= 122)
        e_ok = (u2f > 0.62) if fi >= 88 else ((u2f > 0.45) | ((body.bg_rgb_diff > 48.0) & (val >= 165)))
        e_seed = hand_zone & e_ok & (is_ew | is_ep)
        if e_seed.sum() >= 22:
            ne_c, ne_lbl, ne_stats, _ = cv2.connectedComponentsWithStats(
                cv2.dilate(e_seed.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))),
                connectivity=8,
            )
            best_eid, best_ea = 0, 0
            for eid in range(1, ne_c):
                ew_box = ne_stats[eid, cv2.CC_STAT_WIDTH]
                eh_box = ne_stats[eid, cv2.CC_STAT_HEIGHT]
                ecomp = e_seed & (ne_lbl == eid)
                if ecomp.sum() >= 22 and ew_box <= 62 and eh_box <= 62 and ecomp.sum() > best_ea:
                    best_ea = int(ecomp.sum())
                    best_eid = eid
            if best_eid > 0:
                ecomp = e_seed & (ne_lbl == best_eid)
                eraser_cube = fill_hull(ecomp, erode_px=0)
                eys, exs = np.where(eraser_cube)
                ex_mid, ey_mid = int(np.median(exs)), int(np.median(eys))
                wrist_line = np.zeros((h, w), dtype=np.uint8)
                cv2.line(wrist_line, (head_x1 - 8, ey_mid - 14), (ex_mid, ey_mid), 255, thickness=18)
                eraser_cube |= ((wrist_line > 0) & (~body.is_steel_room_wall) & ((b >= r - 6) | (val < 130)))

    # (d) Complete Smooth Headphone Band + Symmetric 3D Oval Earcups
    upper_head = body.geom_trunk & (yy <= ny0 + 315)
    dist_to_head = cv2.distanceTransform((1 - upper_head.astype(np.uint8)), cv2.DIST_L2, 5)

    hp_band = body.is_cool_white & (
        ((yy < ny0 + 135) & (dist_to_head <= 26.0))
        | ((yy >= ny0 + 135) & (yy <= ny0 + 275) & (dist_to_head <= 32.0))
    ) & (u2f > 0.62)

    earcup_solid = np.zeros((h, w), dtype=bool)
    if not (36 <= fi <= 47):
        ear_rows = upper_head[max(0, ny0 + 130):min(h, ny0 + 250), :]
        if ear_rows.any():
            _, exs = np.where(ear_rows)
            lx = int(np.percentile(exs, 1))
            rx = int(np.percentile(exs, 99))
        else:
            lx, rx = head_x0 + 6, head_x1 - 6
        ecy = int(ny0 + 190)
        earcup_geom = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(earcup_geom, (lx - 8, ecy), (30, 58), 0, 0, 360, 255, -1)
        cv2.ellipse(earcup_geom, (rx + 8, ecy), (30, 58), 0, 0, 360, 255, -1)
        earcup_solid = (earcup_geom > 0) & (dist_to_head <= 38.0) & ((u2f > 0.74) | (silf > 0.84)) & (val >= 138)
    else:
        earcup_cand = (
            (dist_to_head <= (40.0 if fi >= 44 else 66.0))
            & (yy >= ny0 + 25) & (yy <= ny0 + 295)
            & (u2f > 0.84) & (silf > 0.84)
            & (val >= 140) & (sat <= 36) & (rb_diff <= 22)
        )
        nec, ne_l, ne_s, _ = cv2.connectedComponentsWithStats(earcup_cand.astype(np.uint8), connectivity=8)
        for cid in range(1, nec):
            if ne_s[cid, cv2.CC_STAT_AREA] >= 220:
                c_mask = (ne_l == cid)
                adj_head = body.geom_trunk & (
                    cv2.dilate(c_mask.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))) > 0
                )
                earcup_solid |= fill_hull(c_mask | adj_head, erode_px=0) & ((u2f > 0.78) | body.geom_trunk)

    hp_all = cv2.morphologyEx(
        (hp_band | earcup_solid).astype(np.uint8) * 255,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 21)),
    ) > 0
    if not (36 <= fi <= 47):
        hp_all = hp_all & (((yy < ny0 + 125) & (dist_to_head <= 26.0)) | ((yy >= ny0 + 125) & (dist_to_head <= 38.0)))
        hp_all = hp_all & (xx >= head_x0 - 40) & (xx <= head_x1 + 40)

    return CharacterAccessories(
        pencil_solid=pencil_solid,
        left_arm_bridge=left_arm_bridge,
        tail_solid=tail_solid,
        right_arm_bridge=right_arm_bridge,
        eraser_cube=eraser_cube,
        hp_all=hp_all,
        dist_to_head=dist_to_head,
    )
