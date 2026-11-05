#!/usr/bin/env python3
"""一発で貼れる版：全文を1本の原稿にする。ページには見出し・ページ番号など原稿以外の文字を一切置かない
（PDFを開いて Ctrl+A → Ctrl+C で原稿だけがコピーされる）。"""
import json, re, subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from make import grammar_batches
pdfmetrics.registerFont(TTFont('EN', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
W, H = A4; M = 12*mm

def build(path, title, lines, size=9.5):
    while max(pdfmetrics.stringWidth(l, 'EN', size) for l in lines) > W - 2*M: size -= 0.25
    lead = size * 1.45; per = int((H - 2*M) // lead)
    c = canvas.Canvas(path, pagesize=A4); c.setTitle(title); c.setAuthor('まなとび')
    for p in range(0, len(lines), per):
        c.setFont('EN', size); y = H - M - size
        for l in lines[p:p+per]: c.drawString(M, y, l); y -= lead
        c.showPage()
    c.save()
    t = subprocess.run(['pdftotext', '-raw', path, '-'], capture_output=True, text=True).stdout
    ok = re.sub(r'\s+', ' ', t).strip() == re.sub(r'\s+', ' ', '\n'.join(lines)).strip()
    pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout).group(1)
    chars = len('\n'.join(lines))
    print(f'{path}: {pages}p {len(lines)}行 {chars:,}文字 size={size} 一致={ok}')
    assert ok
    open(path.replace('.pdf', '.txt'), 'w').write('\n'.join(lines) + '\n')
    return chars

# 英文法：1文1行、文の間に1.5秒
g = grammar_batches()
sent = [t for b in g for t in b['texts']]; ids = [i for b in g for i in b['ids']]
assert len(sent) == 1163
gl = []
for k, s in enumerate(sent):
    gl.append(s)
    if k < len(sent) - 1: gl.append('<break time="1.5s" />')
# 英単語：194回分を順につなぐ（各回の最後の語にも間を付ける）
man = json.load(open('vocab_manifest.json'))
vl, vids = [], []
for name, m in man.items():
    vl += open(f'vocab_batches/{name}.txt').read().rstrip('\n').split('\n'); vids += m['ids']
vl = [l if l.endswith('/>') else l + ' <break time="1.2s" />' for l in vl]
vl[-1] = vl[-1].replace(' <break time="1.2s" />', '')
assert len(vl) == 5713 == len(vids)
plain = lambda ls: [l.replace(' <break time="1.2s" />', '') for l in ls if not l.startswith('<break')]

build('一括_英文法_間あり.pdf', '英文法 全1163文（ElevenLabs一括・間あり）', gl)
build('一括_英文法_間なし.pdf', '英文法 全1163文（ElevenLabs一括・間なし）', plain(gl))
build('一括_英単語熟語_間あり.pdf', '英単語・英熟語 全5713語（ElevenLabs一括・間あり）', vl)
build('一括_英単語熟語_間なし.pdf', '英単語・英熟語 全5713語（ElevenLabs一括・間なし）', plain(vl))
json.dump({'grammar': ids, 'vocab': vids}, open('一括_並び順_ID.json', 'w'), indent=0)
