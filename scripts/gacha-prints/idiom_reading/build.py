#!/usr/bin/env python3
"""
熟語＋英文解釈 小テスト（B4横に B5縦を左右2面・問題と解答を同じ PDF・白黒）2026-10-27

  左の面 … 英熟語（ilv1）をアプリの単語帳と同じ順に。英語を見て日本語を書く
  右の面 … 上に「左の面の熟語のつづき」、その下に英文解釈の1題（本文＋4択。アプリと同じ選択肢の並び）
           → 熟語は 左上→左下→右上 と続く
  1回分 ＝ B4 2枚（1枚目：問題、2枚目：解答。解答は同じ配置で、右の面の本文は全訳に入れかわる）
  コース：基礎（英文解釈 レベル1）・標準（レベル2）・発展（レベル3）各12回
          熟語の番号は 基礎 No.1 → 標準 → 発展 と通しで続く
  白黒で見やすく：熟語の答え＝太字、設問の正解＝太字＋下線、本文の根拠＝波下線、ポイント＝太字

  入力：public/data/listeningVocabulary.json（熟語）、src/data/reading（dump.ts で JSON に）
  出力：.tmpwork/idiom_reading/熟語英文解釈_{基礎,標準,発展}_第01-12回.pdf
  使い方：npx tsx scripts/gacha-prints/idiom_reading/dump.ts && python3 scripts/gacha-prints/idiom_reading/build.py
"""
import io, json, sys
from pathlib import Path
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from b4common import (ROOT, F, FB, INK, SUB, LINE, PALE, WAVY, H, PANES, MARKS,  # noqa: E402
                      esc, enesc, jtext, mixed_width, draw_mixed, para, bar, footer, cut_line, page_size)

OUT = ROOT / '.tmpwork/idiom_reading'; OUT.mkdir(parents=True, exist_ok=True)
VOC = json.load(open(ROOT / 'public/data/listeningVocabulary.json'))['words']
IDIOMS = [w for w in VOC if w['level'] == 'ilv1']
COURSES = [(1, '基礎'), (2, '標準'), (3, '発展')]
ROUNDS = 12
ROW_H = 6.55 * mm
BOTTOM = 13 * mm
SCALES = (1.0, 0.96, 0.92, 0.88, 0.85)   # 本文が長い回は文字を少しずつ小さく（最小で本文 9pt）
MIN_RIGHT = 4                             # 右の面の上に最低これだけ熟語を置く


def jp(size, lead, color=INK, font=F, **kw):
    return ParagraphStyle('x', fontName=font, fontSize=size, leading=lead, textColor=color, **kw)

def en_body(s):
    return ParagraphStyle('en', fontName='EN', fontSize=10.6 * s, leading=14.6 * s, textColor=INK, firstLineIndent=10, alignment=4)


def idiom_rows(c, x0, x1, ytop, items, answer, n_max):
    """熟語を ytop から n_max 行並べ、最後の y を返す。解答は意味を太字で"""
    y = ytop; en_w = (x1 - x0) * 0.50
    for no, w in items[:n_max]:
        c.setFillColor(SUB); c.setFont('EN', 8.6); c.drawRightString(x0 + 8 * mm, y - ROW_H + 2.1 * mm, str(no))
        word = str(w['word']).replace('\u301c', '～')
        size = 10.6
        while mixed_width(word, size) > en_w - 11 * mm and size > 7.4: size -= 0.3
        c.setFillColor(INK); draw_mixed(c, x0 + 10 * mm, y - ROW_H + 2.1 * mm, word, size)
        lx = x0 + en_w
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(lx, y - ROW_H + 1.2 * mm, x1, y - ROW_H + 1.2 * mm)
        if answer:
            m = w['meaning']; sz = 9.6
            while pdfmetrics.stringWidth(m, FB, sz) > x1 - lx - 2 * mm and sz > 6.2: sz -= 0.3
            c.setFillColor(INK); c.setFont(FB, sz); c.drawString(lx + 1.5 * mm, y - ROW_H + 2.2 * mm, m)
        y -= ROW_H
    return y

def rows_fit(ytop, ybot):
    return int((ytop - ybot + 0.01) // ROW_H)


def title_line(c, x0, x1, y, p, label, s):
    return para(c, f'<b>{esc(p["title"])}</b>　<font name="{F}" size="{8.5 * s:.1f}" color="#555555">{label}</font>',
                ParagraphStyle('t', fontName='EN', fontSize=12 * s, leading=15 * s, textColor=INK), x0, y, x1 - x0)

def reading_q(c, x0, x1, ytop, p, s):
    """問題ページの右面の下段：本文＋設問"""
    w = x1 - x0; y = ytop
    y -= title_line(c, x0, x1, y, p, f'（{esc(p["topic"])}・{len(p["text"].split())}語）', s) + 1.5 * mm
    for i, par in enumerate(p['paragraphs']):
        y -= para(c, f'<font name="{FB}" size="{8.5 * s:.1f}">［{i+1}］</font> ' + esc(par), en_body(s), x0, y, w) + 1.4 * mm * s
    y -= 1.5 * mm
    for k, q in enumerate(sorted(p['questions'], key=lambda q: (q['para'] or 99))):
        y -= para(c, f'<b>問{k+1}</b>　' + jtext(q['prompt']) + (f'<font size="{8 * s:.1f}" color="#555555">（第{q["para"]}段落）</font>' if q['para'] else '（全体）'),
                  jp(9.6 * s, 13.2 * s), x0, y, w) + 0.6 * mm
        for j, o in enumerate(q['shuffled']['options']):
            y -= para(c, f'{MARKS[j]} {jtext(o)}', jp(9.2 * s, 12.4 * s, leftIndent=4 * mm), x0, y, w)
        c.setFont(F, 8.5); c.setFillColor(SUB); c.drawRightString(x1, y - 3.2 * mm, '答（　　　）'); c.setFillColor(INK)
        y -= 4.4 * mm + 1.4 * mm * s
    return y

def reading_a(c, x0, x1, ytop, p, ja, s):
    """解答ページの右面の下段：全訳＋正解・根拠（白黒：正解＝太字下線、根拠＝波下線）"""
    w = x1 - x0; y = ytop
    y -= title_line(c, x0, x1, y, p, '全訳と解答', s) + 1.2 * mm
    for i, t in enumerate(ja):
        y -= para(c, f'<font name="{FB}">［{i+1}］</font>' + esc(t), jp(8.6 * s, 12.0 * s, SUB), x0, y, w) + 1.0 * mm * s
    y -= 1.5 * mm
    for k, q in enumerate(sorted(p['questions'], key=lambda q: (q['para'] or 99))):
        ai = q['shuffled']['answerIndex']; o = q['shuffled']['options'][ai]
        y -= para(c, f'<b>問{k+1}</b>　{jtext(q["prompt"])}', jp(9.2 * s, 12.4 * s), x0, y, w) + 0.4 * mm
        body = (f'<b><u>正解 {MARKS[ai]}　{jtext(o)}</u></b><br/>{jtext(q["explanation"])}<br/>'
                f'根拠：<font name="EN"><u color="{WAVY}">{enesc(q["evidence"])}</u></font>（{esc(q["evidenceJa"])}）')
        if q.get('point'): body += f'<br/><b>ポイント</b>　{jtext(q["point"])}'
        h = para(c, body, jp(8.2 * s, 11.4 * s, INK, backColor=PALE, borderPadding=(2, 3, 2, 3), leftIndent=3 * mm), x0, y, w)
        y -= h + 3.2 * mm * s
    if p.get('phrases'):
        y -= para(c, '<b>本文の重要表現</b>　' + '　'.join(f'<font name="EN"><b>{enesc(a)}</b></font> {esc(b)}' for a, b in p['phrases']),
                  jp(8.2 * s, 11.4 * s), x0, y, w) + 2 * mm
    return y

def reading_height(fn, p, ja, s):
    """捨てキャンバスに描いて高さを測る"""
    c = canvas.Canvas(io.BytesIO(), pagesize=page_size())
    (x0, x1) = PANES[1]
    return H - (fn(c, x0, x1, H, p, s) if fn is reading_q else fn(c, x0, x1, H, p, ja, s))


def plan_round(p, ja):
    """右の面に置ける熟語の行数と、本文の文字の倍率を決める"""
    (Rx0, Rx1) = PANES[1]
    top = H - 11 * mm - 9 * mm - 2 * mm          # 見出し帯の下
    sub_h = 6.5 * mm                              # 「英熟語（つづき）」の小見出し
    gap = 4 * mm                                  # 熟語と本文の間（区切り線）
    best = None
    for s in SCALES:
        hq = reading_height(reading_q, p, ja, s); ha = reading_height(reading_a, p, ja, s)
        avail = top - BOTTOM - sub_h - gap - max(hq, ha)
        n = rows_fit(avail + BOTTOM, BOTTOM) if avail > 0 else -1
        if n >= MIN_RIGHT: return n, s
        best = (max(n, 0), s)
    return best

def left_rows():
    y = H - 11 * mm - 9 * mm - 3 * mm - 5 * mm
    return rows_fit(y, BOTTOM)


def draw_round(c, level, cname, rnd, p, ja, start_no, nR, s):
    nL = left_rows(); per = nL + nR
    items = [(start_no + i, IDIOMS[start_no - 1 + i]) for i in range(per)]
    (Lx0, Lx1), (Rx0, Rx1) = PANES
    nq = len(p['questions'])
    for answer in (False, True):
        tag = '解答' if answer else '問題'
        # ---- 左：熟語 ----
        y = bar(c, Lx0, Lx1, f'第{rnd}回　英熟語 小テスト（英→日）', f'　　点 ／ {per}点', answer) - 3 * mm
        if not answer:
            c.setFont(F, 9); c.setFillColor(INK); c.drawRightString(Lx1, y - 3 * mm, '名前　　　　　　　　　　　　　　')
            c.setStrokeColor(LINE); c.line(Lx1 - 46 * mm, y - 3.8 * mm, Lx1, y - 3.8 * mm)
        c.setFont(F, 8.4); c.setFillColor(SUB)
        c.drawString(Lx0, y - 3 * mm, '英語を見て、意味を日本語で書きなさい。（右の面の上につづく）' if not answer else '太字が解答例（「／」はどちらでも正解）。')
        idiom_rows(c, Lx0, Lx1, y - 5 * mm, items, answer, nL)
        footer(c, Lx0, Lx1, f'マナトビ　英熟語（{cname}コース）No.{start_no}〜{start_no + per - 1}　［{tag}］')
        # ---- 右：上に熟語のつづき、下に英文解釈 ----
        y = bar(c, Rx0, Rx1, f'第{rnd}回　英熟語（つづき）・英文解釈（{cname}）', f'　　点 ／ {nq}点', answer) - 2 * mm
        c.setFont(FB, 9.4); c.setFillColor(INK); c.drawString(Rx0, y - 4.2 * mm, f'英熟語（つづき）No.{items[nL][0]}〜{items[-1][0]}' if nR else '')
        y = idiom_rows(c, Rx0, Rx1, y - 6.5 * mm, items[nL:], answer, nR) if nR else y - 6.5 * mm
        c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(Rx0, y - 1.5 * mm, Rx1, y - 1.5 * mm)
        y -= 4 * mm
        yb = reading_a(c, Rx0, Rx1, y, p, ja, s) if answer else reading_q(c, Rx0, Rx1, y, p, s)
        assert yb >= BOTTOM - 0.5, (cname, rnd, answer, yb / mm)
        footer(c, Rx0, Rx1, f'英文解釈 レベル{level}（{cname}）{p["id"]}　アプリの「英文解釈」と同じ問題・選択肢の順　［{tag}］')
        cut_line(c)
        c.showPage()
    return per


def build():
    no = 1
    for level, cname in COURSES:
        R = json.load(open(OUT / f'reading{level}.json'))
        allc = canvas.Canvas(str(OUT / f'熟語英文解釈_{cname}_第01-12回.pdf'), pagesize=page_size())
        allc.setTitle(f'英熟語＋英文解釈 小テスト（{cname}）第1〜12回')
        first = no
        for rnd in range(1, ROUNDS + 1):
            p = R['passages'][rnd - 1]; ja = R['ja'][p['id']]
            nR, s = plan_round(p, ja)
            per = draw_round(allc, level, cname, rnd, p, ja, no, nR, s)
            print(f'{cname} 第{rnd}回 熟語 {no}〜{no + per - 1}（左{left_rows()}＋右{nR}）/ {p["id"]} 文字{s:.2f}')
            no += per
        allc.save()
        print(f'== {cname}: 熟語 No.{first}〜{no - 1}')

if __name__ == '__main__':
    build()
