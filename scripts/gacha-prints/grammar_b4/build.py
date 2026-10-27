#!/usr/bin/env python3
"""
英文法 4択 B4プリント（B4横に B5縦を左右2面・問題と解答を同じ PDF・白黒）2026-10-27

  アプリの「英文法」第1〜16章（4択・729問）を、アプリと同じ問題・同じ順（章 → 問題番号）・同じ選択肢の並びで。
  1つの面（B5）＝ 1回分（8〜10問）。見出しは「時制（1）」「時制（2）」…
  章の問題を 10問以内の回にほぼ均等に分ける（章をまたがない）
  1枚目：左右2回分の問題、2枚目：同じ配置で解答（切ってB5にしても問題と解答の面が対応する）
  解説はアプリより短く：正解の英文（答えの部分を太字＋下線）・和訳・ポイント1行

  入力：src/data/egV3Items.generated.ts（../idiom_reading/dump.ts で JSON に）
  出力：.tmpwork/idiom_reading/英文法_4択_第1-16章.pdf
  使い方：npx tsx scripts/gacha-prints/idiom_reading/dump.ts && python3 scripts/gacha-prints/grammar_b4/build.py
"""
import io, json, math, re, sys
from collections import OrderedDict
from pathlib import Path
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from b4common import (ROOT, F, FB, INK, SUB, LINE, PALE, H, PANES, MARKS,  # noqa: E402
                      esc, mix, jtext, para, bar, footer, cut_line, page_size)

OUT = ROOT / '.tmpwork/idiom_reading'
ITEMS = [x for x in json.load(open(OUT / 'grammar.json')) if x['c'] <= 16]
PER = 10
BOTTOM = 13 * mm
SCALES = (1.0, 0.95, 0.9, 0.86, 0.82)


def sections():
    """章ごとに番号順 → 10問以内の回に均等に分ける"""
    ch = OrderedDict()
    for x in sorted(ITEMS, key=lambda x: (x['c'], x['n'])):
        ch.setdefault(x['c'], []).append(x)
    out = []
    for c, xs in ch.items():
        k = math.ceil(len(xs) / PER); base, extra = divmod(len(xs), k); i = 0
        for j in range(k):
            m = base + (1 if j < extra else 0)
            out.append({'c': c, 't': xs[0]['t'], 'no': j + 1, 'of': k, 'items': xs[i:i + m]}); i += m
    return out


def en(size, lead, **kw):
    return ParagraphStyle('e', fontName='EN', fontSize=size, leading=lead, textColor=INK, **kw)

def jp(size, lead, color=INK, **kw):
    return ParagraphStyle('j', fontName=F, fontSize=size, leading=lead, textColor=color, **kw)

def sentence_html(s):
    # 空所は少し長めの下線に
    return mix(s).replace('______', '<font name="EN">__________</font>')

def point_of(x):
    for l in x['cm']:
        if l.startswith('【ポイント】'): return l[len('【ポイント】'):]
    return x['one']

def full_html(x):
    f, k = x['f'], x['k']
    m = re.search(r'(?<![A-Za-z])' + re.escape(k) + r'(?![A-Za-z])', f)
    i = m.start() if m else f.find(k)   # 単語の途中（sister の is など）に当てない
    if i < 0: return mix(f)
    return mix(f[:i]) + f'<b><u>{mix(k)}</u></b>' + mix(f[i + len(k):])


def draw_questions(c, x0, x1, ytop, sec, s):
    w = x1 - x0; y = ytop; half = (w - 6 * mm) / 2
    for i, x in enumerate(sec['items']):
        num = f'<font name="{FB}">{i + 1}</font>　'
        y -= para(c, num + sentence_html(x['s']), en(10.6 * s, 14.2 * s, leftIndent=6 * mm, firstLineIndent=-6 * mm), x0, y, w) + 0.6 * mm
        opts = [f'<font name="{F}">{MARKS[j]}</font> {mix(o)}' for j, o in enumerate(x['o'])]
        st = en(10.2 * s, 13.2 * s)
        widths = [pdfmetrics.stringWidth(f'{MARKS[j]} ', F, 10.2 * s) + pdfmetrics.stringWidth(o, 'EN', 10.2 * s) for j, o in enumerate(x['o'])]
        if max(widths) < half - 2 * mm:
            for r in range(2):
                hs = [para(c, opts[r * 2 + k], st, x0 + 6 * mm + k * half, y, half) for k in range(2)]
                y -= max(hs)
        else:
            for o in opts: y -= para(c, o, st, x0 + 6 * mm, y, w - 6 * mm)
        c.setFont(F, 8.5); c.setFillColor(SUB); c.drawRightString(x1, y - 3.0 * mm, '答（　　　）'); c.setFillColor(INK)
        y -= 4.6 * mm * s
    return y

def draw_answers(c, x0, x1, ytop, sec, s):
    w = x1 - x0; y = ytop
    for i, x in enumerate(sec['items']):
        y -= para(c, f'<font name="{FB}">{i + 1}</font>　<b><u><font name="{FB}">正解 {MARKS[x["a"]]}</font>　{mix(x["o"][x["a"]])}</u></b>'
                  f'　<font name="{F}" size="{8 * s:.1f}" color="#555555">（アプリ No.{x["n"]}）</font>', en(10.2 * s, 13.4 * s), x0, y, w) + 0.4 * mm
        body = (f'{full_html(x)}<br/><font name="{F}">{esc(x["tr"])}</font><br/>'
                f'<font name="{FB}">ポイント</font>　<font name="{F}">{jtext(point_of(x))}</font>')
        h = para(c, body, en(9.4 * s, 12.6 * s, backColor=PALE, borderPadding=(2, 3, 2, 3), leftIndent=6 * mm), x0, y, w)
        y -= h + 3.4 * mm * s
    return y


def sec_title(sec):
    return f'{sec["t"]}（{sec["no"]}）'

def ns_range(sec):
    return f'No.{sec["items"][0]["n"]}〜{sec["items"][-1]["n"]}'

def pane_top():
    return H - 11 * mm - 9 * mm - 3 * mm - 6 * mm

def fit_scale(sec):
    (x0, x1) = PANES[0]
    for s in SCALES:
        ok = True
        for fn in (draw_questions, draw_answers):
            cc = canvas.Canvas(io.BytesIO(), pagesize=page_size())
            if fn(cc, x0, x1, pane_top(), sec, s) < BOTTOM: ok = False
        if ok: return s
    raise SystemExit(f'入りきらない: {sec_title(sec)}')

def draw_pane(c, side, sec, answer, s):
    x0, x1 = PANES[side]
    y = bar(c, x0, x1, f'第{sec["c"]}章　{sec_title(sec)}', f'　　点 ／ {len(sec["items"])}点', answer) - 3 * mm
    c.setFont(F, 8.4); c.setFillColor(SUB)
    if answer:
        c.drawString(x0, y - 3 * mm, '正解の英文は答えの部分を太字＋下線で示した。')
    else:
        c.drawString(x0, y - 3 * mm, '空所に入る最も適当なものを①〜④から選びなさい。')
        c.setFont(F, 9); c.setFillColor(INK); c.drawRightString(x1, y - 3 * mm, '名前　　　　　　　　　　　　')
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(x1 - 40 * mm, y - 3.8 * mm, x1, y - 3.8 * mm)
    c.setFillColor(INK)
    yb = (draw_answers if answer else draw_questions)(c, x0, x1, pane_top(), sec, s)
    assert yb >= BOTTOM - 0.5
    footer(c, x0, x1, f'マナトビ 英文法 第{sec["c"]}章 {sec["t"]}　{ns_range(sec)}（アプリと同じ問題・選択肢の順）［{"解答" if answer else "問題"}］')


def build():
    secs = sections()
    for sec in secs: sec['s'] = fit_scale(sec)
    path = OUT / '英文法_4択_第1-16章.pdf'
    c = canvas.Canvas(str(path), pagesize=page_size()); c.setTitle('英文法 4択（アプリと同じ問題）第1〜16章')
    for i in range(0, len(secs), 2):
        pair = secs[i:i + 2]
        for answer in (False, True):
            for side, sec in enumerate(pair): draw_pane(c, side, sec, answer, sec['s'])
            cut_line(c); c.showPage()
    c.save()
    small = [f'{sec_title(x)}={x["s"]}' for x in secs if x['s'] < 1]
    print(f'{len(secs)}回分 / B4 {math.ceil(len(secs) / 2) * 2}ページ  縮小: {small}')
    cur = None
    for x in secs:
        if x['c'] != cur: cur = x['c']; print(f'\n第{cur}章 {x["t"]}:', end='')
        print(f' （{x["no"]}）{len(x["items"])}問', end='')
    print()

if __name__ == '__main__':
    build()
