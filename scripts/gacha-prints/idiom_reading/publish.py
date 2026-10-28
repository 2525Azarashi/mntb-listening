#!/usr/bin/env python3
"""
B4プリント（熟語＋英文解釈 3コース・英文法4択 3冊）をガチャの UR（完全版）用に public/prints へ置く 2026-10-27

  前提：dump.ts → idiom_reading/build.py → grammar_b4/build.py を実行済み（.tmpwork/idiom_reading に PDF がある）
  やること：PDF を public/prints/<id>.pdf にコピー、1ページ目の左の面（B5）からサムネイル 360×510 の webp を作る、
            src/data/gachaPrints.generated.ts に書く pages・kb を表示する
  使い方：python3 scripts/gacha-prints/idiom_reading/publish.py
"""
import re, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / '.tmpwork/idiom_reading'
PRINTS = ROOT / 'public/prints'

# (ガチャ id, 元の PDF)
ITEMS = [
    ('print_book_idiom_reading_basic', '熟語英文解釈_基礎_第01-12回.pdf'),
    ('print_book_idiom_reading_standard', '熟語英文解釈_標準_第01-12回.pdf'),
    ('print_book_idiom_reading_advanced', '熟語英文解釈_発展_第01-12回.pdf'),
    ('print_book_grammar_b4_bunpo', '英文法_4択_第1-16章.pdf'),
    ('print_book_grammar_b4_gohou', '英文法_4択_語法_第17-19章.pdf'),
    ('print_book_grammar_b4_kaiwa', '英文法_4択_会話表現_第20章.pdf'),
]

def thumb(pdf: Path, pid: str):
    """B4横の1ページ目の左半分（B5縦の問題面）をサムネイルに"""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['pdftoppm', '-r', '110', '-f', '1', '-l', '1', '-png', str(pdf), f'{d}/p'], check=True, capture_output=True)
        im = Image.open(next(Path(d).glob('p*.png'))).convert('RGB')
        im = im.crop((0, 0, im.width // 2, im.height))
        im = im.resize((360, int(360 * im.height / im.width)), Image.LANCZOS)
        canvas = Image.new('RGB', (360, 510), 'white'); canvas.paste(im.crop((0, 0, 360, min(510, im.height))), (0, 0))
        canvas.save(PRINTS / f'thumbs/{pid}.webp', 'WEBP', quality=82)

def pages(pdf: Path) -> int:
    r = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', r).group(1))

for pid, name in ITEMS:
    src = SRC / name; dst = PRINTS / f'{pid}.pdf'
    shutil.copyfile(src, dst); thumb(dst, pid)
    print(f'{pid}: pages={pages(dst)} kb={round(dst.stat().st_size / 1024)}')
