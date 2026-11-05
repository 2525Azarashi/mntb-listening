#!/usr/bin/env python3
"""共通テスト リスニング予想問題（第1〜5回）の日本語アナウンスを、全回共通の原稿1本にする（ElevenLabs 用）。
・大問・設問の並びは5回とも同じ（assets_plan.tracks で確認）→ 番号・指示の音声は全回で使い回せる
・第4〜6問の場面説明（回ごとに違う）は読まず、問題冊子に書かれている前提の共通の言い方にする
・「問1」は「もんいち」と読まれないよう「問い1」と書く
・1つの音声（クリップ）ごとに <break time="1.5s" /> を入れ、無音で切り分けられるようにする
・改行は文末（。）の後だけ（文の途中で改行すると、読み上げで不自然な間が入るため）"""
import json, re, subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('JA', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
pdfmetrics.registerFont(TTFont('EN', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
BR = '<break time="1.5s" />'
W, H = A4; M = 14*mm

CLIPS = [
 ('ja_open',   '開始', ['大学入学共通テスト予想問題、英語リスニング。', 'これからリスニングテストを始めます。']),
] + [(f'ja_round{n}', f'第{n}回（開始の直後）', [f'第{n}回。']) for n in range(1, 6)] + [
 ('ja_p1a', '第1問A の指示', ['第1問A。', '第1問Aは、問い1から問い4までの、4問です。', '英語を聞き、それぞれの内容と最も近い意味のものを、四つの選択肢のうちから一つずつ選びなさい。', '2回流します。']),
] + [(f'ja_q{q:02d}', f'問{q}', [f'問い{q}。']) for q in range(1, 5)] + [
 ('ja_p1b', '第1問B の指示', ['第1問B。', '第1問Bは、問い5から問い7までの、3問です。', '英語を聞き、それぞれの内容と最も近い絵を、四つの選択肢のうちから一つずつ選びなさい。', '2回流します。']),
] + [(f'ja_q{q:02d}', f'問{q}', [f'問い{q}。']) for q in range(5, 8)] + [
 ('ja_p2', '第2問 の指示', ['第2問。', '第2問は、問い8から問い11までの、4問です。', '対話と問いを聞き、その答えとして最も適切なものを、四つの選択肢のうちから一つずつ選びなさい。', '2回流します。']),
] + [(f'ja_q{q:02d}', f'問{q}', [f'問い{q}。']) for q in range(8, 12)] + [
 ('ja_repeat', '2回読みの間（第1・2問で毎回使う）', ['もう一度読みます。']),
 ('ja_p3', '第3問 の指示', ['第3問。', '第3問は、問い12から問い17までの、6問です。', '対話を聞き、問いの答えとして最も適切なものを、四つの選択肢のうちから一つずつ選びなさい。', '問いと選択肢は、問題冊子に書かれています。', '1回流します。']),
] + [(f'ja_q{q:02d}', f'問{q}', [f'問い{q}。']) for q in range(12, 18)] + [
 ('ja_p4a', '第4問A の指示', ['第4問A。', '第4問Aは、問い18から問い25までの、8問です。', '話を聞き、それぞれの問いに答えなさい。', '状況と問いは、問題冊子に書かれています。', '問題冊子を読む時間が与えられた後、音声が流れます。', '1回流します。']),
 ('ja_start', '先読み時間の後（第4〜6問で使う）', ['それでは、始めます。']),
 ('ja_q18-21', '問18〜21', ['問い18から問い21。']),
 ('ja_q22-25', '問22〜25', ['問い22から問い25。']),
 ('ja_p4b', '第4問B の指示', ['第4問B。', '第4問Bは、問い26の、1問です。', '4人の説明を聞き、問題冊子の条件をすべて満たすものを、選択肢のうちから一つ選びなさい。', '問題冊子を読む時間が与えられた後、音声が流れます。', '1回流します。']),
 ('ja_q26', '問26', ['問い26。']),
 ('ja_p5', '第5問 の指示', ['第5問。', '第5問は、問い27から問い33までの、7問です。', '講義を聞き、ワークシートを完成させ、問いに答えなさい。', '状況とワークシート、問いは、問題冊子に書かれています。', '問題冊子を読む時間が与えられた後、音声が流れます。', '1回流します。']),
 ('ja_q27-32', '問27〜32', ['問い27から問い32。']),
 ('ja_q33', '問33（講義の続き）', ['問い33。', '講義の後、二人の学生がグラフを見ながら話しています。']),
 ('ja_p6a', '第6問A の指示', ['第6問A。', '第6問Aは、問い34と問い35の、2問です。', '二人の対話を聞き、それぞれの問いに答えなさい。', '状況と問いは、問題冊子に書かれています。', '問題冊子を読む時間が与えられた後、音声が流れます。', '1回流します。']),
 ('ja_q34-35', '問34・35', ['問い34と問い35。']),
 ('ja_p6b', '第6問B の指示', ['第6問B。', '第6問Bは、問い36と問い37の、2問です。', '四人の会話を聞き、それぞれの問いに答えなさい。', '状況と問いは、問題冊子に書かれています。', '問題冊子を読む時間が与えられた後、音声が流れます。', '1回流します。']),
 ('ja_q36-37', '問36・37', ['問い36と問い37。']),
 ('ja_end', '終了', ['これでリスニングの問題は終わりです。']),
]

def font_for(ch): return 'EN' if ord(ch) < 0x2000 else 'JA'
def runs(t):
    out = []
    for ch in t:
        f = font_for(ch)
        if out and out[-1][0] == f: out[-1][1] += ch
        else: out.append([f, ch])
    return out
def width(t, s): return sum(pdfmetrics.stringWidth(x, f, s) for f, x in runs(t))
def draw(c, x, y, t, s):
    for f, x_ in runs(t):
        c.setFont(f, s); c.drawString(x, y, x_); x += pdfmetrics.stringWidth(x_, f, s)

def script_lines():
    lines = []
    for i, (_, _, sents) in enumerate(CLIPS):
        lines += sents
        if i < len(CLIPS) - 1: lines.append(BR)
    return lines

def build_script_pdf(path, lines, size=11):
    while max(width(l, size) for l in lines) > W - 2*M: size -= 0.25
    lead = size * 1.6; per = int((H - 2*M) // lead)
    c = canvas.Canvas(path, pagesize=A4); c.setTitle('共通テスト リスニング 日本語アナウンス（全回共通・ElevenLabs原稿）'); c.setAuthor('まなとび')
    for p in range(0, len(lines), per):
        y = H - M - size
        for l in lines[p:p+per]:
            c.setFillColor(colors.HexColor('#7a8793') if l == BR else colors.black)
            draw(c, M, y, l, size); y -= lead
        c.showPage()
    c.save()
    t = subprocess.run(['pdftotext', '-raw', path, '-'], capture_output=True, text=True).stdout
    got = [x for x in t.replace('\f', '\n').split('\n') if x.strip()]
    ok = got == lines
    pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout).group(1)
    print(f'{path}: {pages}ページ {len(lines)}行 文字サイズ{size} PDFから取り出した文字が原稿と一致={ok}')
    if not ok:
        for a, b in zip(got, lines):
            if a != b: print('  違い:', repr(a), repr(b)); break
    assert ok
    return pages

def build_list_pdf(path):
    c = canvas.Canvas(path, pagesize=A4); c.setTitle('日本語アナウンス 音声の一覧と使う場所')
    y = H - 20*mm
    c.setFillColor(colors.HexColor('#0f5c63')); draw(c, M, y, '日本語アナウンス　音声の一覧（原稿の上から順・全%d個）' % len(CLIPS), 14); y -= 9*mm
    c.setFillColor(colors.black)
    notes = ['生成した1本の音声を、1.5秒の無音で切ると、上から順にこの名前の音声になります。',
             '番号・指示の音声は第1〜5回のすべてで同じものを使います（回ごとに作り直す必要はありません）。']
    for n in notes: draw(c, M, y, n, 9.5); y -= 6*mm
    y -= 2*mm
    TX = M + 92*mm; TW = W - M - TX
    for i, (name, use, sents) in enumerate(CLIPS, 1):
        rows, cur = [], ''
        for ch in ''.join(sents):
            if width(cur + ch, 8.5) > TW: rows.append(cur); cur = ch
            else: cur += ch
        rows.append(cur)
        if y - 4.2*mm*(len(rows)-1) < 16*mm: c.showPage(); y = H - 18*mm
        c.setFillColor(colors.HexColor('#5d6d7e')); draw(c, M, y, f'{i:02d}', 9)
        c.setFillColor(colors.HexColor('#0f5c63')); draw(c, M + 8*mm, y, name, 9)
        c.setFillColor(colors.black); draw(c, M + 34*mm, y, use, 9)
        c.setFillColor(colors.HexColor('#333333'))
        for r in rows: draw(c, TX, y, r, 8.5); y -= 4.2*mm
        y -= 1.6*mm
    c.showPage(); c.save()

if __name__ == '__main__':
    lines = script_lines()
    open('共通テスト_日本語アナウンス_原稿.txt', 'w').write('\n'.join(lines) + '\n')
    build_script_pdf('共通テスト_日本語アナウンス_原稿.pdf', lines)
    build_list_pdf('共通テスト_日本語アナウンス_音声一覧.pdf')
    json.dump([{'name': n, 'use': u, 'text': ''.join(s)} for n, u, s in CLIPS], open('kyotsu_ja_clips.json', 'w'), ensure_ascii=False, indent=1)
    body = '\n'.join(lines)
    print(f'音声 {len(CLIPS)}個・break {len(CLIPS)-1}個・{len(body):,}文字（タグを除く読み上げ部分 {len("".join(l for l in lines if l != BR)):,}文字）')
