# -*- coding: utf-8 -*-
"""大分大学 一般選抜（前期日程）対策 英語 予想問題 — 紙面づくり（2026-11-04）

  python3 scripts/gacha-prints/oita_mock/render.py all          # 第1〜3回 × 3系統（9冊）
  python3 scripts/gacha-prints/oita_mock/render.py 1            # 第1回の3系統
  python3 scripts/gacha-prints/oita_mock/render.py 1 oitam      # 第1回の医学部版だけ
→ .tmpwork/oita/ に問題・解答解説、public/prints/print_lr_niji_{oitae,oitak,oitam}_en_N.pdf

前期の英語は学部で3種類（令和7・8年度の公開問題・出題の意図・解答例の「形」だけを参考にした）。
  教育学部 80分・150点：〔1〕長文読解（3学部共通）〔2〕日本語の文章の概要を 75〜85 語の英語で書く
  経済学部 80分・200点：〔1〕長文読解（共通）〔2〕日本文の下線部(A)〜(D)を英語で表現する
  医学部（医学科・先進医療科学科）80分・100点：〔1〕長文読解（共通）〔2〕長文読解（医療の話題）
                                       〔3〕[ ]内の語句を並べ替え、本文の【①】〜【⑥】の適切な場所に入れる
大問・小問の配点は大学非公表のため編集部の想定。〔1〕の小問配点は教育学部版（100点）を基準に、
経済学部版は1.2倍（120点）、医学部版は0.4倍（40点）にする（基準の配点・採点の目安はすべて5の倍数）。
英文・日本文・設問・解答はすべて書き下ろしで、過去問の文章・解答例は引用していない。
"""
import html, importlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'oita'
UNIV = '大分大学'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'
TRACKS = {
    'oitae': {'track': '教育学部', 'parts': ['P1', 'E2'], 'points': {'P1': 100, 'E2': 50}, 'scale': 1.0,
              'time': '〔1〕50 分，〔2〕25 分，見直し 5 分',
              'struct': '〔1〕長文読解（3学部共通）／〔2〕日本語の文章の概要を 75〜85 語の英語で書く'},
    'oitak': {'track': '経済学部', 'parts': ['P1', 'K2'], 'points': {'P1': 120, 'K2': 80}, 'scale': 1.2,
              'time': '〔1〕50 分，〔2〕25 分，見直し 5 分',
              'struct': '〔1〕長文読解（3学部共通）／〔2〕日本文の下線部(A)〜(D)を英語で表現する'},
    'oitam': {'track': '医学部（医学科・先進医療科学科）', 'parts': ['P1', 'M2', 'M3'], 'points': {'P1': 40, 'M2': 36, 'M3': 24},
              'scale': 0.4, 'time': '〔1〕35 分，〔2〕30 分，〔3〕12 分，見直し 3 分',
              'struct': '〔1〕長文読解（3学部共通）／〔2〕長文読解（医療の話題）／〔3〕語句の並べ替え（本文の【①】〜【⑥】に入れる）'},
}
PNAME = {'P1': ('1', '長文読解'), 'E2': ('2', '英文要約'), 'K2': ('2', '和文英訳'), 'M2': ('2', '長文読解'), 'M3': ('3', '語句整序')}
WORDS = {'P1': (600, 790), 'M2': (620, 900), 'M3': (380, 600)}


def e(s):
    return html.escape(str(s), quote=False)


def m(s):
    """{uA|…} 下線＋(A)、{bA} 空所（ A ）、{c1} 空所（ ① ）、{o1} 挿入箇所【 ① 】、**…** 太字、//…// 斜体、{br} 改行"""
    t = e(s)
    t = re.sub(r'\{u([A-Z])\|(.+?)\}', lambda x: f'<span class="ul"><span class="ulab">({x.group(1)})</span>{x.group(2)}</span>', t)
    t = re.sub(r'\{b([A-Z])\}', lambda x: f'<span class="blank">（　{x.group(1)}　）</span>', t)
    t = re.sub(r'\{c(\d+)\}', lambda x: f'<span class="blank">（　{CIRC[int(x.group(1)) - 1]}　）</span>', t)
    t = re.sub(r'\{o(\d)\}', lambda x: f'<span class="slot">【　{CIRC[int(x.group(1)) - 1]}　】</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def plain(s):
    t = re.sub(r'\{u[A-Z]\|(.+?)\}', r'\1', s)
    t = re.sub(r'\{b[A-Z]\}|\{c\d+\}|\{o\d\}', ' ', t)
    return re.sub(r'\*\*|//|\{br\}', ' ', t)


def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


CSS = (HERE / 'style.css').read_text(encoding='utf-8')


def page(body, cls=''):
    return f'<section class="page {cls}">{body}</section>'


def logo():
    return f'<img class="logo" src="file://{HERE / "logo_gray.png"}" alt="マナトビ">'


def total_of(tr):
    return sum(TRACKS[tr]['points'].values())


def cover(R, tr, kind, ranges):
    T = TRACKS[tr]
    label = '問　題' if kind == 'q' else '解答・解説'
    rng = (f'（問題 {ranges[0]}〜{ranges[1]} ページ・解答用紙 {ranges[2]}〜{ranges[3]} ページ）' if kind == 'q'
           else f'（解答・解説 {ranges[0]}〜{ranges[1]} ページ）')
    alloc = '・'.join(f'〔{PNAME[p][0]}〕{v} 点' for p, v in T['points'].items())
    if kind == 'q':
        notes = [
            f'解答時間は 80 分。時間の目安は，{T["time"]}。',
            f'大問は {len(T["parts"])} 題。{total_of(tr)} 点満点（{alloc}）。大問・小問の配点は編集部の想定である。',
            '〔1〕は教育学部・経済学部・医学部の 3 つの版に共通の問題である（同じ回なら同じ英文・同じ設問。配点だけが違う）。',
            '答えは巻末の解答用紙（大問ごとに 1 枚・切り取り可）の決められた欄に書くこと。',
            '英文・日本文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値はすべて架空である。',
        ]
    else:
        notes = [
            '各大問の最初に解答一覧と配点（編集部の想定）をまとめた。',
            '日本語・英語で書く問題の解答は一例である。「採点の目安」の要素がそろっていれば，表現が違っても得点としてよい。',
            '長文には全訳と語句をつけた。答え合わせのあと，根拠になる段落をもう一度読み直すこと。',
            '英作文は解答例を 2 つずつ示し，使える言い方と間違えやすい点を書いた。',
        ]
    lis = ''.join(f'<li>{e(x)}</li>' for x in notes)
    return page(f'''
<div class="cv-head">{logo()}<span>学習アプリ マナトビ ｜ 国公立2次 予想問題</span></div>
<div class="cv-main">
  <p class="cv-round">予想問題 第{R['n']}回</p>
  <p class="cv-subject">英　　　語</p>
  <p class="cv-sub">（ 80 分 ・ {total_of(tr)} 点 ）</p>
  <p class="cv-kind">{label}</p>
  <p class="cv-range">{rng}</p>
  <p class="cv-univ">{UNIV} 一般選抜 前期日程 対策</p>
  <p class="cv-track">{e(T['track'])}</p>
</div>
<div class="cv-notes"><p class="cv-notes-h">はじめに読むこと</p><ol>{lis}</ol></div>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>出題の傾向を研究し，編集部が一から書き下ろした演習用の冊子です。</span></div>
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>第{R['n']}回 ／ {e(T['track'])} ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


def head(part, pts, suffix=''):
    num, name = PNAME[part]
    return f'<h2 class="part"><span class="pnum">{num}</span>{name}{suffix}（配点 {pts}）</h2>'


def passage(P):
    title = f'<p class="ptitle">{e(P["title"])}</p>' if P.get('title') else ''
    paras = ''.join(f'<p class="en"><span class="pno">{i + 1}</span>{m(p)}</p>' for i, p in enumerate(P['passage']))
    notes = ''
    if P.get('notes'):
        notes = '<table class="notes"><tr><th>〔注〕</th><td>' + '　'.join(
            f'<span class="note"><i>{e(w)}</i>：{e(j)}</span>' for w, j in P['notes']) + '</td></tr></table>'
    return title + paras + notes


def choice_list(ch, cols=None):
    if cols is None:
        longest = max(len(c[1]) for c in ch)
        cols = 4 if longest <= 14 else (2 if longest <= 34 else 0)
    if cols:
        return f'<div class="cgrid c{cols}">' + ''.join(f'<span><span class="sl">({e(k)})</span> {m(t)}</span>' for k, t in ch) + '</div>'
    return '<ol class="choices ind">' + ''.join(f'<li><span class="cl">({e(k)})</span> {m(t)}</li>' for k, t in ch) + '</ol>'


def question(q):
    body = f'<div>{m(q["stem"])}</div>'
    if q.get('box'):
        body += '<div class="words">' + ''.join(f'<span>{e(w)}</span>' for w in q['box']) + '</div>'
    if q.get('text'):
        body += '<div class="frame">' + ''.join(f'<p class="fp">{m(p)}</p>' for p in q['text']) + '</div>'
    if q.get('frame'):
        body += f'<div class="frame">{m(q["frame"])}</div>'
    if q['type'] in ('mc', 'multi', 'tfill'):
        body += choice_list(q['choices'], q.get('cols'))
    return f'<div class="q"><span class="qk">{e(q["label"])}</span><div class="qbody">{body}</div></div>'


def part_read(P, part, pts):
    return page(head(part, pts) + f'<p class="lead">{m(P["lead"])}</p>' + passage(P)
                + '<p class="qhead">設　問</p>' + ''.join(question(q) for q in P['questions']), 'flow')


def part_e2(E, pts):
    body = head('E2', pts) + f'<p class="lead">{m(E["lead"])}</p>'
    body += '<div class="jabox">' + ''.join(f'<p class="ja">{m(p)}</p>' for p in E['text']) + '</div>'
    return page(body + '<p class="src">（編集部による書き下ろしの文章）</p>', 'flow')


def part_k2(K, pts):
    body = head('K2', pts) + f'<p class="lead">{m(K["lead"])}</p>'
    body += '<div class="jabox">' + ''.join(f'<p class="ja">{m(p)}</p>' for p in K['text']) + '</div>'
    return page(body + '<p class="src">（編集部による書き下ろしの文章）</p>', 'flow')


def part_m3(M, pts):
    body = head('M3', pts) + f'<p class="lead">{m(M["lead"])}</p>' + passage(M)
    body += '<div class="ordl">' + ''.join(
        f'<p class="ordi"><span class="cl">{e(it["key"])}.</span> [ {" / ".join(e(c) for c in it["shown"])} ]</p>' for it in M['items']) + '</div>'
    return page(body, 'flow')



# ───────── 解答用紙 ─────────

def sheet_head(R, tr, k, n):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">予想問題 第{R["n"]}回 英語（{e(TRACKS[tr]["track"])}）　{k}枚目／{n}枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def lines(n):
    return ''.join('<div class="ln ln4"></div>' for _ in range(n))


def ast(labels, cls='ast'):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels)
    td = ''.join('<td></td>' for _ in labels)
    return f'<table class="{cls}"><tr>{th}</tr><tr>{td}</tr></table>'


def genko(limit, per=20):
    out = '<div class="genko">'
    for r in range((limit + per - 1) // per):
        n = min(per, limit - r * per)
        out += '<div class="gkrow">' + ''.join('<div class="gk"></div>' for _ in range(n)) + f'<span class="gkn">{min(limit, (r + 1) * per)}</span></div>'
    return out + '</div>'


def labels_of(q):
    return [CIRC[i - 1] for i in q['nums']]


def sheet_field(q):
    t = q['type']
    if t == 'mc':
        return ast(['記号'])
    if t in ('fill', 'formfill'):
        return ast(labels_of(q), 'ast wide')
    if t in ('multi', 'tfill'):
        return ast(labels_of(q))
    if t == 'ja':
        return genko(q['limit']) if q.get('limit') else lines(q.get('lines', 3))
    if t == 'en':
        return lines(q.get('lines', 1))
    raise AssertionError(('sheet type', t))


SMALL = ('mc', 'multi')
SCORE = '<div class="score">得　点<div></div></div>'


def sheet_read(R, tr, k, n, P, part):
    body = sheet_head(R, tr, k, n) + f'<p><span class="bignum">〔{PNAME[part][0]}〕</span></p>'
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


def sheets(R, tr):
    T = TRACKS[tr]
    n = len(T['parts'])
    out = []
    for k, part in enumerate(T['parts'], 1):
        if part in ('P1', 'M2'):
            out.append(sheet_read(R, tr, k, n, R[part], part))
        elif part == 'E2':
            out.append(sheet_head(R, tr, k, n) + '<p><span class="bignum">〔2〕</span></p>'
                       + lines(10) + '<p class="wcbox">（　　　　　語）</p>' + SCORE)
        elif part == 'K2':
            b = sheet_head(R, tr, k, n) + '<p><span class="bignum">〔2〕</span></p>'
            for it in R['K2']['items']:
                b += f'<p class="sq">({it["ref"]})</p>' + lines(3)
            out.append(b + SCORE)
        elif part == 'M3':
            b = sheet_head(R, tr, k, n) + '<p><span class="bignum">〔3〕</span></p>'
            for i in range(len(R['M3']['items'])):
                b += f'<p class="sq">【{CIRC[i]}】</p>' + lines(2)
            out.append(b + SCORE)
    return ''.join(page(x, 'sheet') for x in out)


def colophon(R, tr, kind):
    T = TRACKS[tr]
    alloc = '・'.join(str(v) for v in T['points'].values())
    return page(f"""
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 第{R['n']}回 英語（{e(T['track'])}）{'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程（{e(T['track'])}の個別学力検査「英語」）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>{e(T['struct'])}／80 分／{total_of(tr)} 点（{alloc}。大問・小問の配点は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・日本文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
""", 'colophon')


# ───────── 検査 ─────────

def sc(p, scale):
    v = p * scale
    assert abs(v - round(v)) < 1e-9, ('配点が整数にならない', p, scale)
    return int(round(v))


def words_of(s):
    return re.findall(r"[a-z0-9]+(?:['’][a-z]+)?", s.lower())


def blanks_in(text):
    return [int(x) for x in re.findall(r'\{c(\d+)\}', text)]


def check_q(q, P, base5):
    text = ' '.join(P['passage'])
    lab = q['label']
    if base5:
        assert q['points'] % 5 == 0, ('〔1〕の小問配点は5の倍数', lab)
        for _, p in q.get('criteria', []):
            assert p % 5 == 0, ('〔1〕の採点の目安は5の倍数', lab)
    if q.get('ref'):
        assert f'{{u{q["ref"]}|' in text, ('下線部が本文にない', lab, q['ref'])
    t = q['type']
    if t == 'mc':
        assert q['answer'] in [k for k, _ in q['choices']], ('mc', lab)
    elif t == 'fill':
        assert len(q['answers']) == len(q['nums']), ('fill 数', lab)
        for a in q['answers']:
            assert len(a.split()) == 1, ('fill 1語', lab, a)
    elif t == 'formfill':
        assert len(q['answers']) == len(q['nums']) == len(q['bases']), ('formfill 数', lab)
        assert len(set(q['bases'])) == len(q['bases']), ('同じ語を2度', lab)
        for b in q['bases']:
            assert b in q['box'], ('語群にない', lab, b)
    elif t == 'multi':
        keys = [k for k, _ in q['choices']]
        assert len(q['answers']) == len(q['nums']) and all(a in keys for a in q['answers']), ('multi', lab)
    elif t == 'tfill':
        keys = [k for k, _ in q['choices']]
        nb = [b for p in q['text'] for b in blanks_in(p)]
        assert nb == q['nums'], ('tfill 空所', lab, nb)
        assert len(q['answers']) == len(nb) and all(a in keys for a in q['answers']), ('tfill', lab)
        assert len(set(q['answers'])) == len(q['answers']), ('tfill 同じ語を2度', lab)
    elif t == 'ja':
        assert sum(p for _, p in q['criteria']) == q['points'], ('ja criteria', lab)
        if q.get('limit'):
            assert len(re.sub(r'\s', '', q['answer'])) <= q['limit'], ('字数オーバー', lab)
    elif t == 'en':
        assert sum(p for _, p in q['criteria']) == q['points'], ('en criteria', lab)
        for a in q['answers']:
            if q.get('min'):
                assert len(words_of(a)) >= q['min'], ('語数不足', lab, a)
            if q.get('exact'):
                assert len(words_of(a)) == q['exact'], ('語数', lab, a)
    else:
        raise AssertionError(('unknown type', t))


def short_answer(q):
    t = q['type']
    if t == 'mc':
        return f'({q["answer"]})'
    if t in ('fill', 'formfill'):
        return '　'.join(f'{CIRC[i - 1]} {a}' for i, a in zip(q['nums'], q['answers']))
    if t in ('multi', 'tfill'):
        return '　'.join(f'{CIRC[i - 1]} ({a})' for i, a in zip(q['nums'], q['answers']))
    if t == 'en':
        return q['answers'][0]
    return '解答例を参照'


def crit(q, scale=1.0, title='採点の目安'):
    total = sum(sc(p, scale) for _, p in q['criteria'])
    items = ''.join(f'<li>{m(t)}（{sc(p, scale)}点）</li>' for t, p in q['criteria'])
    return f'<div class="crit"><p class="crit-h">{title}（{total}点）</p><ul>{items}</ul></div>'


def akey_table(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total}</td></tr></table>'


def full_translation(P):
    tr = ''.join(f'<p class="trp"><span class="pno">{i + 1}</span>{m(t)}</p>' for i, t in enumerate(P['translation']))
    vocab = ''
    if P.get('vocab'):
        vocab = '<p class="ah">語句</p><div class="vocab">' + ''.join(
            f'<span class="vw"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['vocab']) + '</div>'
    return f'<p class="ah">全訳</p>{tr}{vocab}'


def check_read(P, part):
    wc = wcount(plain(' '.join(P['passage'])))
    lo, hi = WORDS[part]
    assert lo <= wc <= hi, (f'{part} 本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), (f'{part} 全訳の段落数', len(P['translation']), len(P['passage']))
    text = ' '.join(P['passage'])
    used = sorted(i for q in P['questions'] if q['type'] in ('fill', 'formfill', 'multi') for i in q['nums'])
    assert sorted(blanks_in(text)) == used, (f'{part} 本文の空所と設問', sorted(blanks_in(text)), used)
    for q in P['questions']:
        check_q(q, P, part == 'P1')
    return wc


def a_part_read(P, part, pts, scale):
    wc = check_read(P, part)
    qs = P['questions']
    rows = [(q['label'], short_answer(q), sc(q['points'], scale)) for q in qs]
    assert sum(r[2] for r in rows) == pts, (f'{part} points', sum(r[2] for r in rows), pts)
    body = head(part, pts, ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey_table(rows)
    for q in qs:
        body += f'<h3 class="aq"><span class="qk">{e(q["label"])}</span>{e(q["kind"])}（{sc(q["points"], scale)}点）</h3>'
        if q['type'] == 'ja':
            body += f'<p class="ans">【解答例】{m(q["answer"])}</p>'
        elif q['type'] == 'en':
            body += '<p class="ans">【解答例】' + ' ／ '.join(m(a) for a in q['answers']) + '</p>'
        else:
            body += f'<p class="ans">【解答】{m(short_answer(q))}</p>'
        if q.get('expl'):
            body += f'<p class="expl">{m(q["expl"])}</p>'
        if q.get('criteria'):
            body += crit(q, scale)
    body += full_translation(P)
    return page(body, 'flow')


def a_part_e2(E, pts):
    assert len(E['models']) == 2, 'E2 models'
    for t in E['models']:
        n = wcount(t)
        assert 75 <= n <= 85, ('E2 解答例の語数', n)
    assert sum(p for _, p in E['criteria']) == pts, ('E2 points',)
    body = head('E2', pts, ' — 解答・解説')
    body += '<p class="ah">文章の要点（概要に入れる内容）</p><ol class="instr">' + ''.join(f'<li>{m(x)}</li>' for x in E['outline']) + '</ol>'
    for j, t in enumerate(E['models'], 1):
        body += f'<p class="ah2">解答例{j}（{wcount(t)} 語）</p><div class="model-en"><p>{m(t)}</p></div>'
    body += '<ul class="tips">' + ''.join(f'<li>{m(x)}</li>' for x in E['tips']) + '</ul>' + crit(E)
    return page(body, 'flow')


def a_part_k2(K, pts):
    text = ' '.join(K['text'])
    refs = re.findall(r'\{u([A-Z])\|', text)
    assert refs == [it['ref'] for it in K['items']], ('K2 下線と設問', refs)
    assert sum(sum(p for _, p in it['criteria']) for it in K['items']) == pts, ('K2 points',)
    body = head('K2', pts, ' — 解答・解説')
    for it in K['items']:
        assert len(it['models']) == 2, ('K2 models', it['ref'])
        src = re.search(r'\{u' + it['ref'] + r'\|(.+?)\}', text).group(1)
        sp = sum(p for _, p in it['criteria'])
        body += f'<h3 class="aq"><span class="qk">({it["ref"]})</span>和文英訳（{sp}点）</h3><p class="ja-src">{e(src)}</p>'
        body += ''.join(f'<p class="ans">【解答例{j}】{m(t)}</p>' for j, t in enumerate(it['models'], 1))
        body += '<ul class="tips">' + ''.join(f'<li>{m(t)}</li>' for t in it['tips']) + '</ul>' + crit(it)
    return page(body, 'flow')


def a_part_m3(M, pts):
    wc = wcount(plain(' '.join(M['passage'])))
    lo, hi = WORDS['M3']
    assert lo <= wc <= hi, ('M3 本文の語数', wc)
    assert len(M['translation']) == len(M['passage']), ('M3 全訳の段落数',)
    text = ' '.join(M['passage'])
    slots = [int(x) for x in re.findall(r'\{o(\d)\}', text)]
    items = M['items']
    assert slots == list(range(1, len(items) + 1)), ('M3 挿入箇所', slots)
    assert sorted(it['slot'] for it in items) == slots, ('M3 slot', [it['slot'] for it in items])
    assert [it['slot'] for it in items] != slots, ('M3 a〜f が最初から①〜⑥の順になっている',)
    for it in items:
        assert sorted(it['shown']) == sorted(it['answer']), ('M3 語句', it['key'])
        assert it['shown'] != it['answer'], ('M3 並べ替えが不要', it['key'])
    per = pts // len(items)
    assert per * len(items) == pts, ('M3 points',)
    by_slot = sorted(items, key=lambda it: it['slot'])
    rows = [(f'【{CIRC[it["slot"] - 1]}】', f'{it["key"]}．' + ' '.join(it['answer']), per) for it in by_slot]
    body = head('M3', pts, ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧（a〜f は入る記号。解答欄には英文だけを書く）</p>' + akey_table(rows)
    body += '<ul class="tips">' + ''.join(f'<li><b>【{CIRC[it["slot"] - 1]}】{e(it["key"])}</b>　{m(it["expl"])}</li>' for it in by_slot) + '</ul>'
    filled = text
    for it in items:
        filled = filled.replace(f'{{o{it["slot"]}}}', '**' + ' '.join(it['answer']) + '**')
    body += '<p class="ah">完成した本文（太字が入れた部分）</p>' + ''.join(
        f'<p class="en"><span class="pno">{i + 1}</span>{m(p)}</p>' for i, p in enumerate(
            [re.sub(r'\{o(\d)\}', lambda x: '**' + ' '.join(next(it for it in items if it['slot'] == int(x.group(1)))['answer']) + '**', p) for p in M['passage']]))
    body += full_translation(M)
    return page(body, 'flow')


# ───────── 組み立て ─────────

def build(R, tr, kind, ranges):
    T = TRACKS[tr]
    pts = T['points']
    if kind == 'q':
        parts = cover(R, tr, 'q', ranges)
        for p in T['parts']:
            if p in ('P1', 'M2'):
                parts += part_read(R[p], p, pts[p])
            elif p == 'E2':
                parts += part_e2(R['E2'], pts[p])
            elif p == 'K2':
                parts += part_k2(R['K2'], pts[p])
            elif p == 'M3':
                parts += part_m3(R['M3'], pts[p])
        parts += sheets(R, tr) + colophon(R, tr, 'q')
    else:
        parts = cover(R, tr, 'a', ranges)
        for p in T['parts']:
            if p == 'P1':
                parts += a_part_read(R['P1'], 'P1', pts[p], T['scale'])
            elif p == 'M2':
                parts += a_part_read(R['M2'], 'M2', pts[p], 1.0)
            elif p == 'E2':
                parts += a_part_e2(R['E2'], pts[p])
            elif p == 'K2':
                parts += a_part_k2(R['K2'], pts[p])
            elif p == 'M3':
                parts += a_part_m3(R['M3'], pts[p])
        parts += colophon(R, tr, 'a')
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{parts}</body></html>'


def pdf(html_text, path, label):
    hp = path.with_suffix('.html')
    hp.write_text(html_text, encoding='utf-8')
    subprocess.run(['node', str(HERE / 'pdf.mjs'), str(hp), str(path), label], check=True)


def page_texts(path):
    import unicodedata
    from pypdf import PdfReader
    return [unicodedata.normalize('NFKC', re.sub(r'\s+', '', p.extract_text() or '')) for p in PdfReader(str(path)).pages]


def render(n, trs):
    import json
    R = importlib.import_module(f'r{n}').ROUND
    assert R['n'] == n
    OUT.mkdir(parents=True, exist_ok=True)
    meta_p = OUT / 'meta.json'
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
    for tr in trs:
        T = TRACKS[tr]
        lab = f'第{n}回 {T["track"]}'
        q = OUT / f'予想問題_{UNIV}_英語_第{n}回_{tr}_問題.pdf'
        a = OUT / f'予想問題_{UNIV}_英語_第{n}回_{tr}_解答解説.pdf'
        pdf(build(R, tr, 'a', (1, 1)), a, f'{lab} 解答・解説')   # 先に解答編（検査で止まるならここ）
        pdf(build(R, tr, 'q', (1, 1, 1, 1)), q, f'{lab} 問題')
        t = page_texts(q)
        first_sheet = next(i for i, s in enumerate(t) if '解答用紙' in s and '受験番号' in s) + 1
        last = len(t)
        qr = (2, first_sheet - 1, first_sheet, last - 1)
        pdf(build(R, tr, 'q', qr), q, f'{lab} 問題')
        ar = (2, len(page_texts(a)) - 1)
        pdf(build(R, tr, 'a', ar), a, f'{lab} 解答・解説')
        assert len(page_texts(q)) == last, 'ページ数が2回目で変わった'
        dest = ROOT / 'public' / 'prints' / f'print_lr_niji_{tr}_en_{n}.pdf'
        subprocess.run(['pdfunite', str(q), str(a), str(dest)], check=True)
        pages = last + ar[1] + 1
        meta[f'{tr}_{n}'] = {'pages': pages, 'kb': round(dest.stat().st_size / 1024)}
        print(f'第{n}回 {tr}: 問題 {last}p（解答用紙 {qr[2]}〜{qr[3]}）・解答解説 {ar[1] + 1}p → {dest.relative_to(ROOT)} {dest.stat().st_size // 1024}KB')
    meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    trs = sys.argv[2:] or list(TRACKS)
    for k in ([1, 2, 3] if arg == 'all' else [int(arg)]):
        render(k, trs)
