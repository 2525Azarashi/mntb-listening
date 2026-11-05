#!/usr/bin/env python3
"""
F6（2026-11-04）タイトル動画の「最後のコマ」から、とびら君だけを消した背景（雲・星・紙飛行機・光の輪・床）を作る。
  動画が終わったあと、この背景の上に「装備したポーズ・アクセサリのとびら君」を重ねるので、
  背景が切り替わらず、動画と静止画がひと続きに見える。
  使い方：python3 scripts/launch/make_title_plate.py  → public/cinematics/title-plate.webp
"""
import subprocess, numpy as np, cv2
SRC = 'public/cinematics/title.mp4'
OUT = 'public/cinematics/title-plate.webp'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.05', '-i', SRC, '-frames:v', '1', '/tmp/title_last.png'], check=True)
img = cv2.imread('/tmp/title_last.png')
h, w = img.shape[:2]
bg = np.median(img[np.r_[0:20, h-20:h]].reshape(-1, 3), axis=0)
diff = np.linalg.norm(img.astype(int) - bg, axis=2)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
fg = ((diff > 38) | (hsv[..., 2] < 170)).astype(np.uint8)
roi = np.zeros_like(fg); roi[95:600, 120:600] = 1   # とびら君のまわり（雲・星・紙飛行機は外）
fg &= roi
fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
keep = np.zeros_like(fg)
for i in range(1, n):
    x, y, ww, hh, area = stats[i]
    if area > 4000 or (area > 150 and 200 < x + ww / 2 < 520 and 150 < y + hh / 2 < 600 and abs((x + ww / 2) - 360) < 230 and area > 600):
        keep[lab == i] = 1
cnts, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros_like(keep); cv2.drawContours(mask, cnts, -1, 1, -1)
mask = cv2.dilate(mask, np.ones((15, 15), np.uint8))
plate = cv2.inpaint(img, mask * 255, 9, cv2.INPAINT_TELEA)
plate = cv2.GaussianBlur(plate, (0, 0), 1.2) * (mask[..., None] > 0) + plate * (mask[..., None] == 0)
cv2.imwrite('/tmp/title_plate.png', plate.astype(np.uint8))
cv2.imwrite('/tmp/title_mask.png', mask * 255)
import os
from PIL import Image
Image.open('/tmp/title_plate.png').save(OUT, 'WEBP', quality=82, method=6)
print(OUT, os.path.getsize(OUT))
