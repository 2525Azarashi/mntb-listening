# -*- coding: utf-8 -*-
"""和歌山県立医科大学 一般選抜（前期日程）「英語」対策 予想問題 — 紙面づくり（2026-11-04）

  python3 scripts/gacha-prints/wakayamamed_mock/render.py 1      # 第1回（r1.py のデータ）
  python3 scripts/gacha-prints/wakayamamed_mock/render.py all    # 第1〜3回
→ .tmpwork/wakayamamed/予想問題_和歌山県立医科大学_英語_第N回_{問題,解答解説}.pdf と public/prints/print_lr_niji_wakayamamed_en_N.pdf

紙面は fwu_mock と同じ試験冊子の形（表紙 → 問題Ⅰ〜Ⅳ → 解答用紙4枚 → 奥付 ／ 解答・解説編）。
参考にしたのは公開されている出題の「形」だけ（120分・大問4題。医学部・薬学部で同じ問題）：
  Ⅰ〜Ⅲ 学術的な英文・評論・物語などの長文。下線部和訳（指示語の内容を明らかにして訳す など）・内容の説明（日本語）・
        空所に入る語の選択・下線部の言い換え・語の意味の説明。
  Ⅳ 日本語の随筆を読み，下線部 2 か所を英語で表現する。
英文・日本文・設問・解答はすべて書き下ろしで，過去問の文章・解答例は引用していない。
配点は大学が小問ごとに公表していないため，200 点満点（50・50・50・50）は編集部の想定。
"""
import html, importlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'wakayamamed'
UNIV = '和歌山県立医科大学'
ID = 'wakayamamed'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'
ROMAN = {1: 'Ⅰ', 2: 'Ⅱ', 3: 'Ⅲ', 4: 'Ⅳ'}
PART_NAMES = {1: '長文読解', 2: '長文読解', 3: '長文読解', 4: '和文英訳'}
KEYS = ('P1', 'P2', 'P3', 'P4')
POINTS = {'P1': 50, 'P2': 50, 'P3': 50, 'P4': 50}
PASSAGE_WORDS = (420, 720)
JA_CHARS = (300, 700)
SMALL = ('mc', 'word')   # 解答用紙で小さな欄になるもの


def e(s):
    return html.escape(str(s), quote=False)


UL = r'\{u([0-9a-zア-ン])\|(.+?)\}'
BL = r'\{b([^}|]{1,3})\}'


def m(s):
    """{u1|…} 下線＋(1)、{bア} 空所［ ア ］、**…** 太字、//…// 斜体、{br} 改行"""
    t = e(s)
    t = re.sub(UL, lambda x: f'<span class="ul"><span class="ulab">({x.group(1)})</span>{x.group(2)}</span>', t)
    t = re.sub(BL, lambda x: f'<span class="blank">［　{x.group(1)}　］</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def plain(s):
    t = re.sub(UL, r'\2', s)
    t = re.sub(BL, ' ', t)
    return re.sub(r'\*\*|//|\{br\}', ' ', t)


CSS = (HERE / 'style.css').read_text(encoding='utf-8')


def page(body, cls=''):
    return f'<section class="page {cls}">{body}</section>'


def logo():
    return f'<img class="logo" src="file://{HERE / "logo_gray.png"}" alt="マナトビ">'


def cover(R, kind, ranges):
    label = '問　題' if kind == 'q' else '解答・解説'
    rng = (f'（問題 {ranges[0]}〜{ranges[1]} ページ・解答用紙 {ranges[2]}〜{ranges[3]} ページ）' if kind == 'q'
           else f'（解答・解説 {ranges[0]}〜{ranges[1]} ページ）')
    if kind == 'q':
        notes = [
            '解答時間は 120 分。時間の目安は，問題Ⅰ・Ⅱ・Ⅲ 各 30 分，問題Ⅳ 20 分，見直し 10 分。',
            '問題はⅠ〜Ⅳの 4 題。この冊子では 200 点満点（各 50 点）として採点する。配点は大学が公表していないため編集部の想定である。',
            '和訳・説明の問題は，指示語や省略された内容を補い，日本語として自然な文で答えること。',
            '答えは巻末の 4 枚の解答用紙（大問ごとに 1 枚・切り取り可）の決められた欄に書くこと。',
            '英文・日本文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値・書名はすべて架空である。',
        ]
    else:
        notes = [
            '各大問の最初に解答一覧と配点（編集部の想定）をまとめた。',
            '和訳・説明・英訳の解答は一例である。「採点の目安」の要素がそろっていれば，表現が違っても得点としてよい。',
            '問題Ⅰ〜Ⅲには全訳と語句をつけた。下線部の前後の文をもう一度読み，指示語が何を指すかを確かめること。',
            '問題Ⅳは解答例を 2 つずつ示し，日本語をどう言いかえれば英語にしやすいかを「考え方」に書いた。',
        ]
    lis = ''.join(f'<li>{e(x)}</li>' for x in notes)
    return page(f'''
<div class="cv-head">{logo()}<span>学習アプリ マナトビ ｜ 国公立2次 予想問題</span></div>
<div class="cv-main">
  <p class="cv-round">予想問題 第{R['n']}回</p>
  <p class="cv-subject">英　　　語</p>
  <p class="cv-sub">（ 120 分 ・ 200 点 ）</p>
  <p class="cv-kind">{label}</p>
  <p class="cv-range">{rng}</p>
  <p class="cv-univ">{UNIV} 一般選抜 前期日程 対策</p>
</div>
<div class="cv-notes"><p class="cv-notes-h">はじめに読むこと</p><ol>{lis}</ol></div>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>出題の傾向を研究し，編集部が一から書き下ろした演習用の冊子です。</span></div>
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>第{R['n']}回 ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


def part_head(n, P, suffix=''):
    return f'<h2 class="part"><span class="pnum">{ROMAN[n]}</span>{PART_NAMES[n]}{suffix}（{P["points"]}点）</h2>'


def passage(P):
    title = f'<p class="ptitle">{e(P["title"])}</p>' if P.get('title') else ''
    paras = ''.join(f'<p class="en"><span class="pno">{i + 1}</span>{m(p)}</p>' for i, p in enumerate(P['passage']))
    notes = ''
    if P.get('notes'):
        notes = '<table class="notes"><tr><th>注</th><td>' + '　'.join(
            f'<span class="note"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['notes']) + '</td></tr></table>'
    src = f'<p class="small" style="text-align:right">{e(P["source"])}</p>' if P.get('source') else ''
    return title + paras + src + notes


def choice_list(ch, cols=None):
    if cols is None:
        longest = max(len(c[1]) for c in ch)
        cols = 4 if longest <= 14 else (2 if longest <= 32 else 0)
    if cols:
        return f'<div class="cgrid c{cols}">' + ''.join(f'<span><span class="sl">{e(c[0])}</span> {m(c[1])}</span>' for c in ch) + '</div>'
    return '<ol class="choices ind">' + ''.join(f'<li><span class="cl">{e(c[0])}</span>{m(c[1])}</li>' for c in ch) + '</ol>'


def question(q):
    body = f'<div>{m(q["stem"])}</div>'
    if q['type'] == 'mc':
        body += choice_list(q['choices'], q.get('cols'))
    return f'<div class="q"><span class="qk">{e(q["label"])}</span><div class="qbody">{body}</div></div>'


def part_read(R, k):
    P = R[f'P{k}']
    return page(part_head(k, P) + f'<p class="lead">{m(P["lead"])}</p>' + passage(P)
                + '<p class="qhead">【設問】</p>' + ''.join(question(q) for q in P['questions']), 'flow')


def part_4(R):
    P = R['P4']
    body = part_head(4, P) + f'<p class="lead">{m(P["lead"])}</p>'
    body += ''.join(f'<p class="ja-s">　{m(p)}</p>' for p in P['passage_ja'])
    body += f'<p class="small" style="text-align:right">{e(P["source"])}</p>'
    return page(body, 'flow')


# ───────── 解答用紙 ─────────

def sheet_head(R, k):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">予想問題 第{R["n"]}回 英語　{k}枚目／4枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def lines(n, cls='ln ln4'):
    return ''.join(f'<div class="{cls}"></div>' for _ in range(n))


def ast(labels, cls='ast'):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels)
    td = ''.join('<td></td>' for _ in labels)
    return f'<table class="{cls}"><tr>{th}</tr><tr>{td}</tr></table>'


def sheet_field(q):
    if q['type'] == 'mc':
        return ast(['記号'])
    if q['type'] == 'word':
        return ast(['英語 1 語'], 'ast wide')
    return lines(q.get('lines', 3))


SCORE = '<div class="score">得　点<div></div></div>'


def sheet_read(R, k):
    P = R[f'P{k}']
    body = sheet_head(R, k) + f'<p><span class="bignum">問題{ROMAN[k]}</span></p>'
    small = []
    for q in P['questions']:
        if q['type'] in SMALL:
            small.append(f'<div><p class="sq">{e(q["label"])}</p>{sheet_field(q)}</div>')
            continue
        if small:
            body += '<div class="sqrow">' + ''.join(small) + '</div>'
            small = []
        body += f'<p class="sq">{e(q["label"])}</p>' + sheet_field(q)
    if small:
        body += '<div class="sqrow">' + ''.join(small) + '</div>'
    return body + SCORE


def sheets(R):
    s = [sheet_read(R, k) for k in (1, 2, 3)]
    s4 = sheet_head(R, 4) + '<p><span class="bignum">問題Ⅳ</span></p>'
    for q in R['P4']['questions']:
        s4 += f'<p class="sq">{e(q["label"])}</p>' + lines(6)
    s.append(s4 + SCORE)
    return ''.join(page(x, 'sheet') for x in s)


def colophon(R, kind):
    return page(f'''
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 第{R['n']}回 英語 {'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程（個別学力検査「英語」・医学部・薬学部共通）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>問題Ⅰ〜Ⅳ（長文読解 3 題・日本語の随筆の下線部英訳 2 か所）／120 分／この冊子では 200 点満点（各 50 点。配点は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・日本文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例・出題意図の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
''', 'colophon')


# ───────── 解答・解説編 ─────────

def crit(q, title='採点の目安'):
    total = sum(p for _, p in q['criteria'])
    items = ''.join(f'<li>{m(t)}（{p:g}点）</li>' for t, p in q['criteria'])
    return f'<div class="crit"><p class="crit-h">{title}（{total:g}点）</p><ul>{items}</ul></div>'


def akey_table(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c:g}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total:g}</td></tr></table>'


def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


def check_q(q, P):
    text = ' '.join(P['passage'])
    lab = q['label']
    for r in ([q['ref']] if isinstance(q.get('ref'), str) else q.get('ref', [])):
        assert text.count(f'{{u{r}|') == 1, ('下線部が本文に1つない', lab, r)
    if q.get('blank'):
        assert text.count(f'{{b{q["blank"]}}}') == 1, ('空所が本文に1つない', lab, q['blank'])
    t = q['type']
    if t == 'mc':
        keys = [c[0] for c in q['choices']]
        assert len(keys) == 4 and len(set(c[1] for c in q['choices'])) == 4, ('mc 選択肢', lab)
        assert q['answer'] in keys, ('mc 答え', lab)
    elif t == 'word':
        assert len(q['answer'].split()) == 1, ('1語', lab)
    elif t == 'ja':
        assert sum(p for _, p in q['criteria']) == q['points'], ('ja 採点の目安の合計', lab)
    else:
        raise AssertionError(('unknown type', t))


def short_answer(q):
    if q['type'] in ('mc', 'word'):
        return q['answer']
    return '解答例を参照'


def full_translation(P):
    tr = ''.join(f'<p class="trp"><span class="pno">{i + 1}</span>{m(t)}</p>' for i, t in enumerate(P['translation']))
    vocab = ''
    if P.get('vocab'):
        vocab = '<p class="ah">語句</p><div class="vocab">' + ''.join(
            f'<span class="vw"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['vocab']) + '</div>'
    return f'<p class="ah">全訳</p>{tr}{vocab}'


def a_part_read(R, k):
    P = R[f'P{k}']
    wc = wcount(plain(' '.join(P['passage'])))
    assert PASSAGE_WORDS[0] <= wc <= PASSAGE_WORDS[1], (f'P{k} 本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), (f'P{k} 全訳の段落数', len(P['translation']), len(P['passage']))
    qs = P['questions']
    for q in qs:
        check_q(q, P)
    labels_u = re.findall(r'\{u([0-9a-zア-ン])\|', ' '.join(P['passage']))
    used = [r for q in qs for r in ([q['ref']] if isinstance(q.get('ref'), str) else q.get('ref', []))]
    assert sorted(labels_u) == sorted(used), (f'P{k} 下線部と設問が対応しない', labels_u, used)
    blanks = re.findall(BL, ' '.join(P['passage']))
    assert sorted(blanks) == sorted(q['blank'] for q in qs if q.get('blank')), (f'P{k} 空所と設問が対応しない', blanks)
    rows = [(q['label'], short_answer(q), q['points']) for q in qs]
    assert sum(r[2] for r in rows) == P['points'], (f'P{k} 配点の合計', sum(r[2] for r in rows))
    body = part_head(k, P, ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p>'
    if P.get('about'):
        body += f'<p class="expl">{m(P["about"])}</p>'
    body += '<p class="ah">解答一覧</p>' + akey_table(rows)
    for q in qs:
        body += f'<h3 class="aq"><span class="qk">{e(q["label"])}</span>{e(q["kind"])}（{q["points"]}点）</h3>'
        if q['type'] == 'ja':
            body += f'<p class="ans">【解答例】{m(q["answer"])}</p>'
        else:
            body += f'<p class="ans">【解答】{m(short_answer(q))}</p>'
        if q.get('expl'):
            body += f'<p class="expl">{m(q["expl"])}</p>'
        if q.get('criteria'):
            body += crit(q)
    body += full_translation(P)
    return page(body, 'flow')


def a_part_4(R):
    P = R['P4']
    ja = ''.join(plain(p) for p in P['passage_ja'])
    n = len(re.sub(r'\s', '', ja))
    assert JA_CHARS[0] <= n <= JA_CHARS[1], ('P4 日本文の字数', n)
    qs = P['questions']
    assert sum(q['points'] for q in qs) == P['points'], ('P4 配点の合計',)
    text = ' '.join(P['passage_ja'])
    assert sorted(x[0] for x in re.findall(UL, text)) == sorted(q['ref'] for q in qs), ('P4 下線部と設問',)
    rows = [(q['label'], '解答例を参照', q['points']) for q in qs]
    body = part_head(4, P, ' — 解答・解説') + '<p class="ah">解答一覧</p>' + akey_table(rows)
    for q in qs:
        assert sum(p for _, p in q['criteria']) == q['points'], ('P4 criteria', q['label'])
        assert len(q['models']) == 2, ('P4 models', q['label'])
        src = re.search(r'\{u' + re.escape(q['ref']) + r'\|(.+?)\}', text).group(1)
        body += f'<h3 class="aq"><span class="qk">{e(q["label"])}</span>和文英訳（{q["points"]}点）</h3>'
        body += f'<p class="ja-s">{m(src)}</p>'
        for j, txt in enumerate(q['models'], 1):
            body += f'<p class="ah">解答例{j}</p><div class="model-en"><p>{m(txt)}</p></div>'
        body += '<p class="ah">考え方</p><ul class="tips">' + ''.join(f'<li>{m(t)}</li>' for t in q['tips']) + '</ul>'
        body += crit(q)
    if P.get('about'):
        body += f'<p class="ah">本文について</p><p class="expl">{m(P["about"])}</p>'
    return page(body, 'flow')


def build(R, kind, ranges):
    if kind == 'q':
        parts = (cover(R, 'q', ranges) + part_read(R, 1) + part_read(R, 2) + part_read(R, 3) + part_4(R)
                 + sheets(R) + colophon(R, 'q'))
    else:
        parts = (cover(R, 'a', ranges) + a_part_read(R, 1) + a_part_read(R, 2) + a_part_read(R, 3) + a_part_4(R)
                 + colophon(R, 'a'))
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{parts}</body></html>'


def pdf(html_text, path, label):
    hp = path.with_suffix('.html')
    hp.write_text(html_text, encoding='utf-8')
    subprocess.run(['node', str(HERE / 'pdf.mjs'), str(hp), str(path), label], check=True)


def page_texts(path):
    import unicodedata
    from pypdf import PdfReader
    return [unicodedata.normalize('NFKC', re.sub(r'\s+', '', p.extract_text() or '')) for p in PdfReader(str(path)).pages]


def render(n):
    R = importlib.import_module(f'r{n}').ROUND
    assert R['n'] == n
    for k, v in POINTS.items():
        assert R[k]['points'] == v, (k, R[k]['points'])
    assert sum(R[k]['points'] for k in KEYS) == 200
    OUT.mkdir(parents=True, exist_ok=True)
    q = OUT / f'予想問題_{UNIV}_英語_第{n}回_問題.pdf'
    a = OUT / f'予想問題_{UNIV}_英語_第{n}回_解答解説.pdf'
    pdf(build(R, 'a', (1, 1)), a, f'第{n}回 解答・解説')   # 先に解答編（検査で止まるならここ）
    pdf(build(R, 'q', (1, 1, 1, 1)), q, f'第{n}回 問題')
    t = page_texts(q)
    first_sheet = next(i for i, s in enumerate(t) if '解答用紙' in s and '受験番号' in s) + 1
    last = len(t)
    qr = (2, first_sheet - 1, first_sheet, last - 1)
    pdf(build(R, 'q', qr), q, f'第{n}回 問題')
    ar = (2, len(page_texts(a)) - 1)
    pdf(build(R, 'a', ar), a, f'第{n}回 解答・解説')
    assert len(page_texts(q)) == last, 'ページ数が2回目で変わった'
    dest = ROOT / 'public' / 'prints' / f'print_lr_niji_{ID}_en_{n}.pdf'
    subprocess.run(['pdfunite', str(q), str(a), str(dest)], check=True)
    print(f'第{n}回: 問題 {last}p（解答用紙 {qr[2]}〜{qr[3]}）・解答解説 {ar[1] + 1}p → {dest.relative_to(ROOT)} {dest.stat().st_size // 1024}KB')


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for k in ([1, 2, 3] if arg == 'all' else [int(arg)]):
        render(k)
