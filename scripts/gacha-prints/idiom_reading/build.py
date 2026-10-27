#!/usr/bin/env python3
"""
熟語＋英文解釈 小テスト（B4横に B5縦を左右2面・問題と解答を同じ PDF）2026-10-27

  左の面 … 英熟語（基礎 ilv1）をアプリの単語帳と同じ順に。英語を見て日本語を書く
  右の面 … 英文解釈 レベル1（基礎）の1題（本文＋4択3問。アプリと同じ選択肢の並び）
           本文と設問の下に余白があれば、続きの熟語で埋める
  1回分 ＝ B4 2枚（1枚目：問題、2枚目：解答。解答は同じ配置で赤字）
  全12回（英文解釈 r1-01〜r1-12 に合わせる）。熟語は 1番から通し番号で、1回あたり N 語

  入力：public/data/listeningVocabulary.json（熟語）、src/data/reading（英文解釈：dump.ts で JSON に）
  出力：.tmpwork/idiom_reading/熟語英文解釈_小テスト_第01-12回.pdf（＋各回の PDF）
  使い方：npx tsx scripts/gacha-prints/idiom_reading/dump.ts && python3 scripts/gacha-prints/idiom_reading/build.py
"""
import json, sys
from pathlib import Path
from reportlab.lib.pagesizes import B4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/gacha-prints'))
import fonts as _fonts
F, FB = _fonts.setup(); _fonts.install_fake_bold(); _fonts.match_stroke_to_fill()
pdfmetrics.registerFont(TTFont('EN', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('ENB', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
from reportlab.lib.fonts import addMapping
addMapping('EN', 0, 0, 'EN'); addMapping('EN', 1, 0, 'ENB'); addMapping('EN', 0, 1, 'EN'); addMapping('EN', 1, 1, 'ENB')

OUT = ROOT / '.tmpwork/idiom_reading'; OUT.mkdir(parents=True, exist_ok=True)
READ = json.load(open(ROOT / '.tmpwork/idiom_reading/reading.json'))
VOC = json.load(open(ROOT / 'public/data/listeningVocabulary.json'))['words']
IDIOMS = [w for w in VOC if w['level'] == 'ilv1']
ROUNDS = 12
PER_ROUND = 50          # 1回あたりの熟語数（左 34＋右の空き 16 前後）
INK = colors.HexColor('#1f1f1f'); SUB = colors.HexColor('#5a5a5a'); RED = colors.HexColor('#c62828'); LINE = colors.HexColor('#9a9a9a')
NAVY = colors.HexColor('#1d3557'); PALE = colors.HexColor('#f2f4f7')

W, H = landscape(B4)            # 364 x 257 mm
HALF = W / 2                    # B5 縦 = 182 x 257
M = 11 * mm                     # 各面の外余白
GUT = 9 * mm                    # 中央の余白（切ってB5にしても読める）
MARKS = '①②③④'

def esc(s):
    return str(s).replace('\u301c', '～').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def enesc(s):
    """英語フォントで描く部分：全角の～は英語フォントに無いので半角 ~ に"""
    return esc(s).replace('～', '~').replace('\u2019', "'")

def jp_style(size, lead, color=INK, font=F, **kw):
    return ParagraphStyle('x', fontName=font, fontSize=size, leading=lead, textColor=color, **kw)
EN_BODY = ParagraphStyle('en', fontName='EN', fontSize=10.6, leading=14.6, textColor=INK, firstLineIndent=10, alignment=4)

def segs(t):
    """英字は EN、それ以外（～・括弧・日本語）は日本語フォントで描くための区切り"""
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
    p = Paragraph(text, style); _, h = p.wrap(w, 9999); p.drawOn(c, x, y - h); return h

def header(c, x0, x1, rnd, side, answer):
    y = H - M
    c.setFillColor(NAVY); c.rect(x0, y - 9 * mm, x1 - x0, 9 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont(FB, 11.5)
    title = f'第{rnd}回　' + ('英熟語 小テスト（英→日）' if side == 'L' else '英文解釈（基礎）')
    c.drawString(x0 + 3 * mm, y - 6.3 * mm, title)
    c.setFont(F, 9)
    tag = '解答' if answer else ('名前（　　　　　　　　）　　　／' if side == 'L' else '')
    if side == 'L' and not answer:
        c.drawRightString(x1 - 3 * mm, y - 6.3 * mm, '　　点 ／ 熟語 %d点' % PER_ROUND)
    elif side == 'R' and not answer:
        c.drawRightString(x1 - 3 * mm, y - 6.3 * mm, '　　点 ／ 3点')
    if answer:
        c.setFillColor(colors.HexColor('#ffd54f')); c.roundRect(x1 - 17 * mm, y - 7.6 * mm, 14 * mm, 6.2 * mm, 2, fill=1, stroke=0)
        c.setFillColor(NAVY); c.setFont(FB, 10); c.drawCentredString(x1 - 10 * mm, y - 5.9 * mm, '解答')
    return y - 9 * mm

def idiom_rows(c, x0, x1, ytop, ybot, items, answer, row_h=6.55 * mm):
    """熟語の行を ytop から ybot まで並べ、置けた数を返す"""
    y = ytop; n = 0; en_w = (x1 - x0) * 0.50
    for no, w in items:
        if y - row_h < ybot: break
        c.setFillColor(SUB); c.setFont('EN', 8.6); c.drawRightString(x0 + 8 * mm, y - row_h + 2.1 * mm, str(no))
        word = str(w['word']).replace('\u301c', '～')
        size = 10.6
        while mixed_width(word, size) > en_w - 11 * mm and size > 7.4: size -= 0.3
        c.setFillColor(INK); draw_mixed(c, x0 + 10 * mm, y - row_h + 2.1 * mm, word, size)
        lx = x0 + en_w
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(lx, y - row_h + 1.2 * mm, x1, y - row_h + 1.2 * mm)
        if answer:
            m = w['meaning']; sz = 9.4
            while pdfmetrics.stringWidth(m, F, sz) > x1 - lx - 2 * mm and sz > 6.2: sz -= 0.3
            c.setFillColor(RED); c.setFont(F, sz); c.drawString(lx + 1.5 * mm, y - row_h + 2.2 * mm, m)
        y -= row_h; n += 1
    return n, y

def reading_side(c, x0, x1, ytop, p, ja, answer):
    w = x1 - x0; y = ytop - 3 * mm
    y -= para(c, f'<b>{esc(p["title"])}</b>　<font name="{F}" size="8.5" color="#5a5a5a">（{esc(p["topic"])}・{len(p["text"].split())}語）</font>',
              ParagraphStyle('t', fontName='EN', fontSize=12, leading=15, textColor=NAVY), x0, y, w) + 1.5 * mm
    for i, par in enumerate(p['paragraphs']):
        y -= para(c, f'<font name="{FB}" size="8.5">［{i+1}］</font> ' + esc(par), EN_BODY, x0, y, w) + 1.4 * mm
    y -= 1.5 * mm
    qs = sorted(p['questions'], key=lambda q: (q['para'] or 99))
    for k, q in enumerate(qs):
        y -= para(c, f'<b>問{k+1}</b>　' + esc(q['prompt']) + (f'<font size="8" color="#5a5a5a">（第{q["para"]}段落）</font>' if q['para'] else '（全体）'),
                  jp_style(9.6, 13.2), x0, y, w) + 0.6 * mm
        opts = q['shuffled']['options']; ai = q['shuffled']['answerIndex']
        for j, o in enumerate(opts):
            col = RED if (answer and j == ai) else INK
            txt = f'{MARKS[j]} {esc(o)}'
            if answer and j == ai: txt = f'<b>{txt}</b>'
            y -= para(c, txt, jp_style(9.2, 12.4, col, leftIndent=4 * mm), x0, y, w)
        if not answer:
            c.setFont(F, 8.5); c.setFillColor(SUB); c.drawRightString(x1, y - 3.2 * mm, '答（　　　）'); y -= 4.4 * mm
        else:
            y -= 0.8 * mm
            h = para(c, f'<font color="#c62828"><b>正解 {MARKS[ai]}</b></font>　{esc(q["explanation"])}<br/><font name="EN" color="#5a5a5a">{enesc(q["evidence"])}</font><br/><font color="#5a5a5a">→ {esc(q["evidenceJa"])}</font>'
                     + (f'<br/><font color="#1d3557">ポイント：{esc(q["point"])}</font>' if q.get('point') else ''),
                     jp_style(8.2, 11.2, INK, backColor=PALE, borderPadding=(2, 3, 2, 3), leftIndent=4 * mm), x0, y, w)
            y -= h + 2.4 * mm
        y -= 1.6 * mm
    return y

def answer_reading(c, x0, x1, ytop, p, ja, answer):
    """解答ページの右面：設問の解答・根拠・全訳（本文の代わりに全訳を載せる）"""
    w = x1 - x0; y = ytop - 3 * mm
    y -= para(c, f'<b>{esc(p["title"])}</b>　<font name="{F}" size="8.5" color="#5a5a5a">全訳と解答</font>',
              ParagraphStyle('t', fontName='EN', fontSize=12, leading=15, textColor=NAVY), x0, y, w) + 1.2 * mm
    for i, t in enumerate(ja):
        y -= para(c, f'<font name="{FB}">［{i+1}］</font>' + esc(t), jp_style(8.6, 12.0, SUB), x0, y, w) + 1.0 * mm
    y -= 1.5 * mm
    qs = sorted(p['questions'], key=lambda q: (q['para'] or 99))
    for k, q in enumerate(qs):
        ai = q['shuffled']['answerIndex']; o = q['shuffled']['options'][ai]
        y -= para(c, f'<b>問{k+1}</b>　{esc(q["prompt"])}', jp_style(9.2, 12.4), x0, y, w) + 0.4 * mm
        h = para(c, f'<font color="#c62828"><b>正解 {MARKS[ai]}</b>　{esc(o)}</font><br/>{esc(q["explanation"])}<br/><font name="EN" color="#5a5a5a">{enesc(q["evidence"])}</font><font color="#5a5a5a">（{esc(q["evidenceJa"])}）</font>'
                 + (f'<br/><font color="#1d3557">ポイント：{esc(q["point"])}</font>' if q.get('point') else ''),
                 jp_style(8.2, 11.2, INK, backColor=PALE, borderPadding=(2, 3, 2, 3), leftIndent=3 * mm), x0, y, w)
        y -= h + 3.2 * mm
    if p.get('phrases'):
        y -= para(c, '<b>本文の重要表現</b>　' + '　'.join(f'<font name="EN">{enesc(a)}</font> {esc(b)}' for a, b in p['phrases']),
                  jp_style(8.2, 11.4, NAVY), x0, y, w) + 2 * mm
    return y

def footer(c, x0, x1, txt):
    c.setFont(F, 7.4); c.setFillColor(SUB); c.drawCentredString((x0 + x1) / 2, 6 * mm, txt)

def draw_round(c, rnd, start_no, plan=None):
    p = READ['passages'][rnd - 1]; ja = READ['ja'][p['id']]
    items = [(start_no + i, IDIOMS[start_no - 1 + i]) for i in range(PER_ROUND)]
    for answer in (False, True):
        Lx0, Lx1 = M, HALF - GUT / 2; Rx0, Rx1 = HALF + GUT / 2, W - M
        # 左
        y = header(c, Lx0, Lx1, rnd, 'L', answer) - 3 * mm
        c.setFont(F, 8.4); c.setFillColor(SUB)
        if not answer:
            c.setFont(F, 9); c.setFillColor(INK); c.drawRightString(Lx1, y - 3 * mm, '名前　　　　　　　　　　　　　　')
            c.setStrokeColor(LINE); c.line(Lx1 - 46 * mm, y - 3.8 * mm, Lx1, y - 3.8 * mm)
            c.setFont(F, 8.4); c.setFillColor(SUB)
        c.drawString(Lx0, y - 3 * mm, '英語を見て、意味を日本語で書きなさい。' if not answer else '赤字が解答例（「／」はどちらでも正解）。')
        nL, _ = idiom_rows(c, Lx0, Lx1, y - 5 * mm, 13 * mm, items, answer)
        footer(c, Lx0, Lx1, f'マナトビ　熟語・基礎 No.{start_no}〜{start_no + PER_ROUND - 1}　［{"解答" if answer else "問題"}］')
        # 右
        y = header(c, Rx0, Rx1, rnd, 'R', answer)
        yb = (answer_reading if answer else reading_side)(c, Rx0, Rx1, y, p, ja, answer)
        rest = items[nL:]
        if rest:
            c.setStrokeColor(NAVY); c.setLineWidth(0.8); c.line(Rx0, yb - 1 * mm, Rx1, yb - 1 * mm)
            c.setFont(FB, 9.4); c.setFillColor(NAVY); c.drawString(Rx0, yb - 5.2 * mm, f'英熟語（つづき）No.{rest[0][0]}〜')
            nR, _ = idiom_rows(c, Rx0, Rx1, yb - 6.5 * mm, 13 * mm, rest, answer)
            if nR < len(rest): return False, nL + nR
        footer(c, Rx0, Rx1, f'英文解釈 レベル1（基礎）{p["id"]}　アプリの「英文解釈」と同じ問題・選択肢の順　［{"解答" if answer else "問題"}］')
        # 中央の切り取り線
        c.setStrokeColor(colors.HexColor('#cccccc')); c.setDash(2, 3); c.setLineWidth(0.4); c.line(HALF, 8 * mm, HALF, H - 8 * mm); c.setDash()
        c.showPage()
    return True, PER_ROUND

def build():
    global PER_ROUND
    allc = canvas.Canvas(str(OUT / '熟語英文解釈_小テスト_第01-12回.pdf'), pagesize=landscape(B4))
    allc.setTitle('英熟語＋英文解釈 小テスト（基礎）第1〜12回')
    no = 1; log = []
    for rnd in range(1, ROUNDS + 1):
        # まず収まるかを捨てキャンバスで試し、入りきらなければ熟語を減らす
        import io
        base = PER_ROUND
        while True:
            ok, n = draw_round(canvas.Canvas(io.BytesIO(), pagesize=landscape(B4)), rnd, no)
            if ok: break
            PER_ROUND -= 1
        one = canvas.Canvas(str(OUT / f'第{rnd:02d}回.pdf'), pagesize=landscape(B4)); draw_round(one, rnd, no); one.save()
        draw_round(allc, rnd, no)
        log.append((rnd, no, no + PER_ROUND - 1, READ['passages'][rnd - 1]['id']))
        no += PER_ROUND; PER_ROUND = base
    allc.save()
    for r in log: print('第%d回 熟語 %d〜%d / %s' % r)

if __name__ == '__main__':
    build()
