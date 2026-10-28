"""
B4横（B5縦×2面）の白黒プリント共通部品（2026-10-27）
  ・フォント：日本語＝IPAゴシック（疑似ボールド）、英語＝Liberation Serif
  ・白黒で見やすく：赤字の代わりに 太字／下線／波下線（<u color="#010101"> が波下線になる）
  ・英日混在：英語フォントに無い字（～・日本語・全角記号）だけ日本語フォントで描く
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import B4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.platypus import Paragraph
from reportlab.platypus import paragraph as _pg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/gacha-prints'))
import fonts as _fonts  # noqa: E402

F, FB = _fonts.setup(); _fonts.install_fake_bold(); _fonts.match_stroke_to_fill()

# Paragraph は文字の途中の書体切り替えに _setFont を使う（fonts.py は setFont だけ太らせる）。
# そのままだと太字のあとの普通の字まで太字になるので、_setFont でも描き方を切り替える
from reportlab.pdfgen import textobject as _to
_orig__setFont = _to.PDFTextObject._setFont
def _setFont(self, psfontname, size):
    _orig__setFont(self, psfontname, size)
    self._code.append('2 Tr 0.18 w' if psfontname == 'JPB' else '0 Tr')
_to.PDFTextObject._setFont = _setFont
_EN = '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
pdfmetrics.registerFont(TTFont('EN', _EN))
pdfmetrics.registerFont(TTFont('ENB', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
addMapping('EN', 0, 0, 'EN'); addMapping('EN', 1, 0, 'ENB'); addMapping('EN', 0, 1, 'EN'); addMapping('EN', 1, 1, 'ENB')
EN_CMAP = set(pdfmetrics.getFont('EN').face.charToGlyph.keys())

# 白黒用の色（黒とグレーだけ）
INK = colors.black
SUB = colors.HexColor('#555555')
LINE = colors.HexColor('#999999')
BAR = colors.HexColor('#e4e4e4')     # 見出し帯（薄いグレー）
PALE = colors.HexColor('#f1f1f1')    # 解説の地（薄いグレー）
WAVY = '#010101'                     # <u color="#010101"> → 波下線

W, H = landscape(B4)                 # 364 x 257 mm
HALF = W / 2                         # B5 縦 = 182 x 257
M = 11 * mm                          # 各面の外余白
GUT = 9 * mm                         # 中央の余白（切ってB5にしても読める）
PANES = ((M, HALF - GUT / 2), (HALF + GUT / 2, W - M))
MARKS = '①②③④'


# ---- 波下線：Paragraph の下線を描く関数を差し替え、色が WAVY のときだけ波線にする ----
_orig_do_line = _pg._do_line
def _do_line(tx, x1, y1, x2, y2, nlw, nsc):
    try:
        wavy = nsc is not None and nsc.hexval().lower() == '0x010101'
    except Exception:
        wavy = False
    if not wavy:
        return _orig_do_line(tx, x1, y1, x2, y2, nlw, nsc)
    canv = tx._canvas
    canv.setLineWidth(0.55); canv.setStrokeColor(INK)
    y = y1 - 0.5; step = 1.6; amp = 0.75
    p = canv.beginPath(); p.moveTo(x1, y); x = x1; up = True
    while x < x2 - 0.01:
        nx = min(x + step, x2)
        d = amp if up else -amp
        p.curveTo(x + (nx - x) / 3, y + d, x + 2 * (nx - x) / 3, y + d, nx, y)
        x = nx; up = not up
    canv.drawPath(p, stroke=1, fill=0)
_pg._do_line = _do_line


def esc(s):
    return str(s).replace('\u301c', '～').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def enesc(s):
    """英語フォントで描く部分：全角の～は英語フォントに無いので半角 ~ に"""
    return esc(s).replace('～', '~')

def mix(s):
    """英語フォントの Paragraph 用：英語フォントに無い字だけ日本語フォントに切り替える（esc 済みの記号は保つ）"""
    out = []; buf = ''; jp = False
    s = str(s).replace('\u301c', '～')
    def flush():
        if not buf: return
        t = esc(buf)
        out.append(f'<font name="{F}">{t}</font>' if jp else t)
    for ch in s:
        j = ord(ch) not in EN_CMAP and ch not in '\n'
        if j != jp:
            flush(); buf = ''; jp = j
        buf += ch
    flush()
    return ''.join(out).replace('\n', '<br/>')

import re as _re
_EN_RUN = _re.compile(r"[A-Za-z][A-Za-z0-9'’\-]*(?:[ ,.;:!?]+[A-Za-z0-9][A-Za-z0-9'’\-]*)*[.,!?]?")
def jtext(s):
    """日本語の Paragraph 用：英単語のつながりだけ英語フォントに（esc もする）"""
    s = str(s).replace('\u301c', '～').replace('~', '～')
    out = []; last = 0
    for m in _EN_RUN.finditer(s):
        out.append(esc(s[last:m.start()])); out.append(f'<font name="EN">{esc(m.group())}</font>'); last = m.end()
    out.append(esc(s[last:]))
    return ''.join(out)

def segs(t):
    """drawString 用：英字は EN、それ以外（～・括弧・日本語）は日本語フォント"""
    out = []
    for ch in t:
        f = 'EN' if ord(ch) < 128 else F
        if out and out[-1][0] == f: out[-1][1] += ch
        else: out.append([f, ch])
    return out

def mixed_width(t, size):
    return sum(pdfmetrics.stringWidth(x, f, size) for f, x in segs(t))

def draw_mixed(c, x, y, t, size):
    for f, x_ in segs(t):
        c.setFont(f, size); c.drawString(x, y, x_); x += pdfmetrics.stringWidth(x_, f, size)

def para(c, text, style, x, y, w):
    """y を上端にして Paragraph を描き、高さを返す"""
    p = Paragraph(text, style); _, h = p.wrap(w, 9999); p.drawOn(c, x, y - h); return h

def para_h(text, style, w):
    p = Paragraph(text, style); _, h = p.wrap(w, 9999); return h

def bar(c, x0, x1, title, right='', answer=False):
    """面の見出し帯（薄いグレー＋黒字）。解答は右端に黒地白抜きの「解答」"""
    y = H - M
    c.setFillColor(BAR); c.setStrokeColor(INK); c.setLineWidth(0.8)
    c.rect(x0, y - 9 * mm, x1 - x0, 9 * mm, fill=1, stroke=1)
    c.setFillColor(INK); c.setFont(FB, 11.5); c.drawString(x0 + 3 * mm, y - 6.3 * mm, title)
    if answer:
        c.setFillColor(INK); c.rect(x1 - 17 * mm, y - 7.6 * mm, 14 * mm, 6.2 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont(FB, 10); c.drawCentredString(x1 - 10 * mm, y - 5.9 * mm, '解答')
        c.setFillColor(INK)
    elif right:
        c.setFont(F, 9); c.drawRightString(x1 - 3 * mm, y - 6.3 * mm, right)
    return y - 9 * mm

def footer(c, x0, x1, txt):
    c.setFont(F, 7.4); c.setFillColor(SUB); c.drawCentredString((x0 + x1) / 2, 6 * mm, txt); c.setFillColor(INK)

def cut_line(c):
    c.setStrokeColor(colors.HexColor('#bbbbbb')); c.setDash(2, 3); c.setLineWidth(0.4)
    c.line(HALF, 8 * mm, HALF, H - 8 * mm); c.setDash()

def page_size():
    return landscape(B4)
