#!/usr/bin/env bash
# とびら君の「背景なし」モーション動画を取り込む（2026-10-23）
#
#   使い方: bash scripts/tobira-motion/import.sh <生成AIの原本.mp4> <名前> [開始秒] [長さ秒]
#     例:   bash scripts/tobira-motion/import.sh ~/Downloads/idle.mp4 idle 0.2 3.0
#
#   Adobe Firefly（Firefly Video モデル）で「真緑 #00FF00 の単色背景・1:1・5秒」で作る（docs/TOBIRA_MOTION_PROMPTS.md）。
#   とびら君は青い体なので、ブルーバックは体が抜けて使えない（実測：体の 52% が透けた）。
#
#   出力（public/tobira-motion/）
#     <名前>.webm  … VP9 + 透過（Chrome / Android / Edge / Firefox）  480×480・24fps・音声なし
#     <名前>.webp  … 透過アニメ WebP（Safari / iOS 用の代わり）     320×320・15fps
#     <名前>.png   … 1コマ目（読み込み中・動きを減らす設定のときの静止画）
#
#   どちらかの動画が 1MB を超えたらエラーで止める（tests/tobiraMotion.test.ts と同じ上限）。
set -euo pipefail
SRC="${1:?原本の動画を指定してください}"; NAME="${2:?名前（idle / cheer など）を指定してください}"
SS="${3:-0}"; DUR="${4:-}"
OUT="$(cd "$(dirname "$0")/../.." && pwd)/public/tobira-motion"; mkdir -p "$OUT"
CUT=(-ss "$SS"); [ -n "$DUR" ] && CUT+=(-t "$DUR")
# 緑を抜く → 縁に残る緑をにごす（despill）→ 正方形に縮める
KEY="chromakey=0x00FF00:0.18:0.06,despill=type=green:mix=0.6:expand=0.2"
ffmpeg -v error -y "${CUT[@]}" -i "$SRC" -an -vf "$KEY,fps=24,scale=480:480:force_original_aspect_ratio=decrease,pad=480:480:(ow-iw)/2:(oh-ih)/2:color=black@0,format=yuva420p" \
  -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1 "$OUT/$NAME.webm"
ffmpeg -v error -y "${CUT[@]}" -i "$SRC" -an -vf "$KEY,fps=15,scale=320:320:force_original_aspect_ratio=decrease,pad=320:320:(ow-iw)/2:(oh-ih)/2:color=black@0" \
  -c:v libwebp_anim -lossless 0 -q:v 55 -compression_level 6 -loop 0 "$OUT/$NAME.webp"
ffmpeg -v error -y "${CUT[@]}" -i "$SRC" -an -frames:v 1 -vf "$KEY,scale=320:320:force_original_aspect_ratio=decrease,pad=320:320:(ow-iw)/2:(oh-ih)/2:color=black@0,format=rgba" "$OUT/$NAME.png"
for f in "$OUT/$NAME.webm" "$OUT/$NAME.webp"; do
  size=$(stat -c %s "$f"); echo "$(basename "$f"): $((size/1024)) KB"
  [ "$size" -lt 1000000 ] || { echo "1MB を超えました。長さを短くするか、開始秒・長さ秒で切ってください" >&2; exit 1; }
done
echo "OK → src/components/TobiraMotion.tsx の TOBIRA_MOTIONS に '$NAME' があるか確認し、docs/TOBIRA_MOTION.md の表を更新してください"
