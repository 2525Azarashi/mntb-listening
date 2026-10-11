#!/usr/bin/env bash
# カサニマロに送る「差分ZIP」を作る。
#   基準 = タグ kasa-baseline（カサニマロの手元にある版）。送ったら基準を進める（docs/APP_SYNC.md）。
#   使い方: bash scripts/kasa-diff.sh [出力先.zip]
set -euo pipefail
BASE=${BASE:-kasa-baseline}
OUT=${1:-kasa_diff_$(date +%Y-%m-%d).zip}
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT";; esac
cd "$(git rev-parse --show-toplevel)"
TMP=$(mktemp -d)
git diff --name-only --diff-filter=ACMRT "$BASE" HEAD > "$TMP/changed.txt"
git diff --name-only --diff-filter=D "$BASE" HEAD > "$TMP/deleted.txt"
mkdir -p "$TMP/app"
while IFS= read -r f; do [ -n "$f" ] && mkdir -p "$TMP/app/$(dirname "$f")" && git show "HEAD:$f" > "$TMP/app/$f"; done < "$TMP/changed.txt"
cp "$TMP/changed.txt" "$TMP/app/_変更したファイル.txt"
cp "$TMP/deleted.txt" "$TMP/app/_消すファイル.txt"
rm -f "$OUT"; (cd "$TMP" && zip -qr "$OUT" app)
echo "基準 $(git rev-parse --short "$BASE") → HEAD $(git rev-parse --short HEAD)"
echo "変更 $(wc -l < "$TMP/changed.txt") 件 / 削除 $(wc -l < "$TMP/deleted.txt") 件 → $OUT"
rm -rf "$TMP"
