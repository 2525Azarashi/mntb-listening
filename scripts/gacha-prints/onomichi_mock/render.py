# -*- coding: utf-8 -*-
"""尾道市立大学 一般選抜（前期日程）経済情報学部「英語」対策 予想問題 — 紙面づくり（2026-11-04）

  python3 scripts/gacha-prints/onomichi_mock/render.py 1      # 第1回（r1.py のデータ）
  python3 scripts/gacha-prints/onomichi_mock/render.py all    # 第1〜3回
→ .tmpwork/onomichi/予想問題_尾道市立大学_英語_第N回_{問題,解答解説}.pdf と public/prints/print_lr_niji_onomichi_en_N.pdf

紙面は yamaguchi_mock と同じ試験冊子の形（表紙 → Ⅰ〜Ⅳ → 解答用紙2枚 → 奥付 ／ 解答・解説編）。
参考にしたのは公開されている出題の「形」だけ：80分・100点・大問4題。
  Ⅰ・Ⅱ 約550語の読解（語の並べ替え・空所の語選択・語義・指示内容・抜き出し・内容の○×）各33点
  Ⅲ 約400語の英文の空所8か所に入る語を4択で選ぶ（16点）
  Ⅳ 日本文に合わせて8語を並べ替え，4番目と7番目を答える（6題・18点）
英文・設問・解答はすべて書き下ろしで，過去問の英文・解答例は引用していない。
大問の配点（33・33・16・18）は公開問題にならい，小問の配点は編集部の想定。
並べ替えの記号の順は random.Random(固定の種) で決める（何度描いても同じ）。
"""
import html, importlib, random, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'onomichi'
UNIV = '尾道市立大学'
ID = 'onomichi'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'
POINTS = {'P1': 33, 'P2': 33, 'P3': 16, 'P4': 18}
PASSAGE_WORDS = (480, 650)
CLOZE_WORDS = (330, 500)
KANA = 'イロハニホヘトチリヌ'
TF = 'アイウエオカ'


def e(s):
    return html.escape(str(s), quote=False)


def shuffled(words, seed):
    """words（正しい順）に記号を振って並べ替えた表示順と，正解の記号列を返す"""
    rng = random.Random(seed)
    idx = list(range(len(words)))
    while True:
        rng.shuffle(idx)
        if idx != sorted(idx) and all(idx[i] + 1 != idx[i + 1] for i in range(len(idx) - 1)):
            break
    shown = [(KANA[k], words[i]) for k, i in enumerate(idx)]        # 表示順：イ=words[idx[0]] …
    label_of = {i: KANA[k] for k, i in enumerate(idx)}
    answer = ''.join(label_of[i] for i in range(len(words)))       # 正しい順に並べた記号
    return shown, answer


def m(s, P=None):
    """{uN|…} 下線＋(N)、{pN} 下線つき空所 (N)(　　)、{rN} 並べ替え、{kN} Ⅲの空所 ( N )、{bA} 空所 ( A )、**…** 太字、//…// 斜体"""
    t = e(s)
    t = re.sub(r'\{u(\d)\|(.+?)\}',
               lambda x: f'<span class="ul"><span class="ulab">({x.group(1)})</span>{x.group(2)}</span>', t)
    t = re.sub(r'\{p(\d)\}', lambda x: f'<span class="blank"><span class="ulab">({x.group(1)})</span><span class="ul">（　　　　　）</span></span>', t)
    t = re.sub(r'\{k(\d)\}', lambda x: f'<span class="blank">（　{x.group(1)}　）</span>', t)
    t = re.sub(r'\{b([A-Z])\}', lambda x: f'<span class="blank">（　{x.group(1)}　）</span>', t)
    if P is not None:
        t = re.sub(r'\{r(\d)\}', lambda x: reorder_html(P, int(x.group(1))), t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def oq(P, n):
    return next(q for q in P['questions'] if q['type'] == 'order' and q['ref'] == n)


def reorder_html(P, n):
    q = oq(P, n)
    shown, _ = shuffled(q['words'], q['seed'])
    inner = ', '.join(f'{k} {e(w)}' for k, w in shown)
    return f'<span class="ul"><span class="ulab">({n})</span>( {inner} )</span>'


def plain(s, P=None):
    """語数・照合用：並べ替えは正しい順の語，空所は正解の語で埋める"""
    t = s
    if P is not None:
        t = re.sub(r'\{r(\d)\}', lambda x: ' '.join(oq(P, int(x.group(1)))['words']), t)
        def fill(x):
            n = int(x.group(1))
            q = next((q for q in P['questions'] if q.get('ref') == n and q['type'] == 'mc'), None)
            return q['choices'][KANA.index(q['answer'])] if q else ' '
        t = re.sub(r'\{p(\d)\}', fill, t)
    t = re.sub(r'\{u\d\|(.+?)\}', r'\1', t)
    t = re.sub(r'\{[pkr]\d\}|\{b[A-Z]\}', ' ', t)
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
            '解答時間は 80 分。時間の目安は，Ⅰ 25 分，Ⅱ 25 分，Ⅲ 12 分，Ⅳ 13 分，見直し 5 分。',
            '大問はⅠ〜Ⅳの 4 題。100 点満点（Ⅰ 33 点・Ⅱ 33 点・Ⅲ 16 点・Ⅳ 18 点）。小問の配点は編集部の想定である。',
            '記号で答える問題は，イ・ロ・ハ…の記号を書くこと。並べ替えの問題は，記号を左から順に書くこと。',
            '答えは巻末の 2 枚の解答用紙（切り取り可）の決められた欄に書くこと。',
            '英文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値はすべて架空である。',
        ]
    else:
        notes = [
            '各大問の最初に解答一覧と配点（小問は編集部の想定）をまとめた。',
            'Ⅰ・Ⅱ・Ⅲには全訳をつけた。答え合わせのあと，根拠になる段落をもう一度読み直すこと。',
            '並べ替えの問題は，完成した英文と，語順を決める手がかり（文の骨組み）を示した。',
            '抜き出しの問題は，つづりが 1 文字でも違えば得点にならないものとして採点する。',
        ]
    lis = ''.join(f'<li>{e(x)}</li>' for x in notes)
    return page(f'''
<div class="cv-head">{logo()}<span>学習アプリ マナトビ ｜ 国公立2次 予想問題</span></div>
<div class="cv-main">
  <p class="cv-round">予想問題 第{R['n']}回</p>
  <p class="cv-subject">英　　　語</p>
  <p class="cv-sub">（ 80 分 ・ 100 点 ）</p>
  <p class="cv-kind">{label}</p>
  <p class="cv-range">{rng}</p>
  <p class="cv-univ">{UNIV} 一般選抜 前期日程 経済情報学部 対策</p>
</div>
<div class="cv-notes"><p class="cv-notes-h">はじめに読むこと</p><ol>{lis}</ol></div>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>出題の傾向を研究し，編集部が一から書き下ろした演習用の冊子です。</span></div>
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>第{R['n']}回 ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


ROMAN = {1: 'Ⅰ', 2: 'Ⅱ', 3: 'Ⅲ', 4: 'Ⅳ'}


def head(k, name, pts, suffix=''):
    return f'<h2 class="part"><span class="pnum">{ROMAN[k]}</span>{name}{suffix}（配点 {pts}）</h2>'


def notes_html(notes):
    if not notes:
        return ''
    return '<table class="notes"><tr><th>注</th><td>' + '　'.join(
        f'<span class="note"><i>{e(w)}</i>　{e(j)}</span>' for w, j in notes) + '</td></tr></table>'


def passage(P):
    title = f'<p class="ptitle">{e(P["title"])}</p>' if P.get('title') else ''
    paras = ''.join(f'<p class="en">{m(p, P)}</p>' for p in P['passage'])
    src = f'<p class="src">{e(P["source"])}</p>' if P.get('source') else ''
    return title + paras + src + notes_html(P.get('notes'))


def choice_list(ch):
    longest = max(len(c) for c in ch)
    cols = 4 if longest <= 14 else (2 if longest <= 30 else 0)
    if cols:
        return f'<div class="cgrid c{cols}">' + ''.join(f'<span><span class="sl">({KANA[i]})</span> {m(c)}</span>' for i, c in enumerate(ch)) + '</div>'
    return '<ol class="choices ind">' + ''.join(f'<li><span class="cl">({KANA[i]})</span> {m(c)}</li>' for i, c in enumerate(ch)) + '</ol>'


def question(q, P):
    body = f'<div>{m(q["stem"])}</div>'
    t = q['type']
    if t == 'mc':
        body += choice_list(q['choices'])
    elif t == 'tf':
        body += '<ol class="tfl ja-tf">' + ''.join(f'<li><span class="cl">({TF[i]})</span> {m(s)}</li>'
                                                   for i, (s, _) in enumerate(q['items'])) + '</ol>'
    return f'<div class="q"><span class="qk">{e(q["label"])}</span><div class="qbody">{body}</div></div>'


TF_RULE = 'ただし，すべての欄に〇，またはすべての欄に×を書いた解答は得点にならない。'


def part_read(R, k):
    P = R[f'P{k}']
    return page(head(k, '読解問題', P['points']) + f'<p class="lead">{m(P["lead"])}</p>' + passage(P)
                + '<p class="qhead">設　問</p>' + ''.join(question(q, P) for q in P['questions']), 'flow')


def part_34(R):
    C, W = R['P3'], R['P4']
    body = head(3, '空所補充', C['points']) + f'<p class="lead">{m(C["lead"])}</p>'
    body += ''.join(f'<p class="en">{m(p)}</p>' for p in C['passage'])
    if C.get('source'):
        body += f'<p class="src">{e(C["source"])}</p>'
    body += notes_html(C.get('notes'))
    body += '<div class="cloze-ch">' + ''.join(
        f'<div class="ccrow"><span class="ccn">{i + 1}.</span>' + ''.join(
            f'<span><span class="sl">({KANA[j]})</span> {e(w)}</span>' for j, w in enumerate(ch)) + '</div>'
        for i, ch in enumerate(C['choices'])) + '</div>'
    body += '<div class="pbreak"></div>' + head(4, '語句の並べ替え', W['points'])
    body += f'<p class="lead">{m(W["lead"])}</p>'
    for i, it in enumerate(W['items']):
        shown, _ = shuffled(it['words'], it['seed'])
        inner = ', '.join(f'{k} {e(w)}' for k, w in shown)
        body += (f'<div class="wq"><p class="wja"><span class="wn">{i + 1}.</span>{e(it["ja"])}</p>'
                 f'<p class="wen">{e(it["pre"])} ( {inner} ) {e(it["post"])}</p></div>')
    return page(body, 'flow')


# ───────── 解答用紙 ─────────

def sheet_head(R, k):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">予想問題 第{R["n"]}回 英語　{k}枚目／2枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def ast(labels, cls='ast'):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels)
    td = ''.join('<td></td>' for _ in labels)
    return f'<table class="{cls}"><tr>{th}</tr><tr>{td}</tr></table>'


def sheet_part(P, k):
    body = f'<p><span class="bignum">{ROMAN[k]}</span></p><div class="sqrow">'
    for q in P['questions']:
        t = q['type']
        if t == 'tf':
            body += '</div>' + f'<p class="sq">{e(q["label"])}</p>' + ast([f'({TF[i]})' for i in range(len(q['items']))], 'ast tf') + '<div class="sqrow">'
            continue
        if t == 'order':
            cell = ast(['→'.join(['　'] * len(q['words']))], 'ast wide')
        elif t == 'word':
            cell = ast(['　' * 12], 'ast wide')
        else:
            cell = ast(['記号'])
        body += f'<div><p class="sq">{e(q["label"])}</p>{cell}</div>'
    return body + '</div>'


SCORE = '<div class="score">得　点<div></div></div>'


def sheets(R):
    s1 = sheet_head(R, 1) + sheet_part(R['P1'], 1) + sheet_part(R['P2'], 2) + SCORE
    s2 = sheet_head(R, 2) + '<p><span class="bignum">Ⅲ</span></p>'
    s2 += ast([str(i) for i in range(1, len(R['P3']['answers']) + 1)], 'ast c8')
    s2 += '<p><span class="bignum">Ⅳ</span></p><table class="fill4"><tr><th></th><th>4番目</th><th>7番目</th><th></th><th>4番目</th><th>7番目</th></tr>'
    for i in range(0, 6, 2):
        s2 += f'<tr><th>{i + 1}</th><td></td><td></td><th>{i + 2}</th><td></td><td></td></tr>'
    s2 += '</table>' + SCORE
    return page(s1, 'sheet') + page(s2, 'sheet')


def colophon(R, kind):
    return page(f'''
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 第{R['n']}回 英語 {'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程 経済情報学部（個別学力検査「外国語（英語）」）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>Ⅰ・Ⅱ 読解／Ⅲ 空所補充（4択）／Ⅳ 日本文に合わせた語句の並べ替え／80 分／100 点（33・33・16・18。小問の配点は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
''', 'colophon')


# ───────── 検査 ─────────

def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


def check_read(P, k):
    text = ' '.join(P['passage'])
    qs = P['questions']
    for kind, pat in (('u', r'\{u(\d)\|'), ('p', r'\{p(\d)\}'), ('r', r'\{r(\d)\}')):
        for n in re.findall(pat, text):
            assert any(q.get('ref') == int(n) for q in qs), (f'P{k} 本文の({n})に設問がない', kind)
    refs = [q['ref'] for q in qs if q.get('ref')]
    assert len(refs) == len(set(refs)), (f'P{k} ref の重複', refs)
    nums = sorted(int(n) for n in re.findall(r'\{[upr](\d)', text))
    assert nums == list(range(1, len(nums) + 1)), (f'P{k} 下線番号が連番でない', nums)
    pt = plain(text, P)
    for q in qs:
        lab, t = q['label'], q['type']
        if q.get('ref'):
            assert re.search(r'\{[upr]' + str(q['ref']) + r'[|}]', text), (f'P{k} 下線部が本文にない', lab)
        if t == 'mc':
            assert q['answer'] in KANA[:len(q['choices'])], ('mc', lab)
            assert len(set(q['choices'])) == len(q['choices']), ('mc 重複', lab)
        elif t == 'order':
            assert 5 <= len(q['words']) <= 8, ('order 語数', lab)
            assert q.get('ja'), ('order 和訳', lab)
        elif t == 'word':
            if q.get('in_text'):
                assert re.search(r'\b' + re.escape(q['answer']) + r'\b', pt), ('抜き出しが本文にない', lab, q['answer'])
        elif t == 'tf':
            vs = [v for _, v in q['items']]
            assert True in vs and False in vs, ('tf 偏り', lab)
        else:
            raise AssertionError(('unknown type', t))
    assert sum(q['points'] for q in qs) == P['points'], (f'P{k} points', sum(q['points'] for q in qs))
    wc = wcount(pt)
    assert PASSAGE_WORDS[0] <= wc <= PASSAGE_WORDS[1], (f'P{k} 本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), (f'P{k} 全訳の段落数', len(P['translation']), len(P['passage']))
    return wc


def short_answer(q):
    t = q['type']
    if t == 'mc':
        return f'({q["answer"]})'
    if t == 'order':
        return ' → '.join(shuffled(q['words'], q['seed'])[1])
    if t == 'word':
        return q['answer']
    return '　'.join(f'({TF[i]}) {"〇" if v else "×"}' for i, (_, v) in enumerate(q['items']))


def akey_table(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c:g}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total:g}</td></tr></table>'


def full_translation(P):
    tr = ''.join(f'<p class="trp"><span class="pno">{i + 1}</span>{m(t)}</p>' for i, t in enumerate(P['translation']))
    vocab = ''
    if P.get('vocab'):
        vocab = '<p class="ah">語句</p><div class="vocab">' + ''.join(
            f'<span class="vw"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['vocab']) + '</div>'
    return f'<p class="ah">全訳</p>{tr}{vocab}'


def a_part_read(R, k):
    P = R[f'P{k}']
    wc = check_read(P, k)
    qs = P['questions']
    rows = [(q['label'], short_answer(q), q['points']) for q in qs]
    body = head(k, '読解問題', P['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey_table(rows)
    for q in qs:
        body += f'<h3 class="aq"><span class="qk">{e(q["label"])}</span>{e(q["kind"])}（{q["points"]}点）</h3>'
        body += f'<p class="ans">【解答】{m(short_answer(q))}</p>'
        if q['type'] == 'order':
            body += f'<p class="ans en-ans">{e(" ".join(q["words"]))}</p>'
        if q.get('expl'):
            body += f'<p class="expl">{m(q["expl"])}</p>'
    body += full_translation(P)
    return page(body, 'flow')


def a_part_3(R):
    C = R['P3']
    text = ' '.join(C['passage'])
    n = [int(x) for x in re.findall(r'\{k(\d)\}', text)]
    assert n == list(range(1, 9)), ('Ⅲ 空所', n)
    assert len(C['choices']) == len(C['answers']) == len(C['expl']) == 8, ('Ⅲ 数',)
    for ch, a in zip(C['choices'], C['answers']):
        assert len(ch) == 4 and len(set(ch)) == 4 and a in KANA[:4], ('Ⅲ 選択肢', ch, a)
    filled = re.sub(r'\{k(\d)\}', lambda x: C['choices'][int(x.group(1)) - 1][KANA.index(C['answers'][int(x.group(1)) - 1])], text)
    wc = wcount(plain(filled))
    assert CLOZE_WORDS[0] <= wc <= CLOZE_WORDS[1], ('Ⅲ 語数', wc)
    assert len(C['translation']) == len(C['passage']), ('Ⅲ 全訳の段落数',)
    rows = [(str(i + 1), f'({a}) {C["choices"][i][KANA.index(a)]}', 2) for i, a in enumerate(C['answers'])]
    body = head(3, '空所補充', C['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey_table(rows)
    body += '<ul class="tips">' + ''.join(f'<li><b>{i + 1}</b>　{m(x)}</li>' for i, x in enumerate(C['expl'])) + '</ul>'
    body += full_translation(C)
    return page(body, 'flow')


def a_part_4(R):
    W = R['P4']
    assert len(W['items']) == 6
    rows = []
    for i, it in enumerate(W['items']):
        assert len(it['words']) == 8, ('Ⅳ 語数', i)
        ans = shuffled(it['words'], it['seed'])[1]
        rows.append((str(i + 1), f'4番目 {ans[3]}（{it["words"][3]}）・7番目 {ans[6]}（{it["words"][6]}）', 3))
    body = head(4, '語句の並べ替え', W['points'], ' — 解答・解説') + '<p class="ah">解答一覧（4番目・7番目の両方が合って 3 点）</p>' + akey_table(rows)
    for i, it in enumerate(W['items']):
        ans = shuffled(it['words'], it['seed'])[1]
        body += f'<h3 class="aq"><span class="qk">{i + 1}</span>{e(it["ja"])}</h3>'
        body += f'<p class="ans en-ans">{e(it["pre"])} <b>{e(" ".join(it["words"]))}</b> {e(it["post"])}</p>'
        body += f'<p class="small">記号の順：{" → ".join(ans)}</p><p class="expl">{m(it["expl"])}</p>'
    return page(body, 'flow')


def build(R, kind, ranges):
    if kind == 'q':
        parts = cover(R, 'q', ranges) + part_read(R, 1) + part_read(R, 2) + part_34(R) + sheets(R) + colophon(R, 'q')
    else:
        parts = cover(R, 'a', ranges) + a_part_read(R, 1) + a_part_read(R, 2) + a_part_3(R) + a_part_4(R) + colophon(R, 'a')
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
    assert sum(R[k]['points'] for k in POINTS) == 100
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
