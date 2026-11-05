# -*- coding: utf-8 -*-
"""公立鳥取環境大学 一般選抜（前期日程）「英語」対策 予想問題 — 紙面づくり（2026-11-04）

  python3 scripts/gacha-prints/kankyo_mock/render.py 1      # 第1回（r1.py のデータ）
  python3 scripts/gacha-prints/kankyo_mock/render.py all    # 第1〜3回
→ .tmpwork/kankyo/予想問題_公立鳥取環境大学_英語_第N回_{問題,解答解説}.pdf と public/prints/print_lr_niji_kankyo_en_N.pdf

紙面は onomichi_mock と同じ試験冊子の形（表紙 → Part 1〜4 → 解答用紙3枚 → 奥付 ／ 解答・解説編）。
参考にしたのは公開されている出題の「形」だけ：90分・Part 1〜4。
  Part 1 約700語の記事を読み，英語の4択20問（内容・語の意味・指す語・段落の主旨）
  Part 2 与えられた問いに150語以上の英語で答える
  Part 3 会話の空所（4つの文から選ぶ／会話に合う英語を自分で書く）
  Part 4 約120語の短い記事を読み，問いに80〜100語の英語で答える
英文・設問・解答はすべて書き下ろしで，過去問の英文・解答例は引用していない。
配点は大学非公表のため編集部の想定（40・24・12・24）。
"""
import html, importlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'kankyo'
UNIV = '公立鳥取環境大学'
ID = 'kankyo'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'
POINTS = {'P1': 40, 'P2': 24, 'P3': 12, 'P4': 24}
P1_WORDS = (620, 800)
P4_WORDS = (100, 150)
LET = 'abcd'
CIRC = '①②③④⑤⑥'


def e(s):
    return html.escape(str(s), quote=False)


def m(s):
    """**…** 太字、//…// 斜体、{blank} 会話の空所、{cN} 番号つき空所"""
    t = e(s)
    t = t.replace('{blank}', '<span class="cblank"></span>')
    t = re.sub(r'\{c(\d)\}', lambda x: f'<span class="blank">（　{x.group(1)}　）<span class="cblank"></span></span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


def plain(s):
    return re.sub(r'\*\*|//|\{br\}|\{blank\}|\{c\d\}', ' ', s)


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
            '時間は 90 分。目安は，Part 1 が 35 分，Part 2 が 25 分，Part 3 が 5 分，Part 4 が 20 分，見直し 5 分。',
            'Part は 1〜4 の 4 つ。100 点満点として採点する（Part 1 40 点・Part 2 24 点・Part 3 12 点・Part 4 24 点）。配点は大学が公表していないため編集部の想定である。',
            'Part 1 の答えは a〜d の記号で書くこと。Part 2・Part 4 は，指定された語数を守り，最後に使った語数を書くこと。',
            '答えは巻末の 3 枚の解答用紙（切り取り可）の決められた欄に書くこと。',
            '英文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値はすべて架空である。',
        ]
    else:
        notes = [
            '各 Part の最初に解答一覧と配点（編集部の想定）をまとめた。',
            'Part 1 は全問に日本語の解説をつけ，本文の全訳と語句を載せた。根拠の段落を必ず読み直すこと。',
            'Part 2・Part 4 の解答例は一例である。「採点の目安」の要素がそろっていれば，内容や表現が違っても得点としてよい。',
            'Part 3 の書く問題は，会話の流れに合っていれば別の表現でも正解とする（別解を示した）。',
        ]
    lis = ''.join(f'<li>{e(x)}</li>' for x in notes)
    return page(f'''
<div class="cv-head">{logo()}<span>学習アプリ マナトビ ｜ 国公立2次 予想問題</span></div>
<div class="cv-main">
  <p class="cv-round">予想問題 第{R['n']}回</p>
  <p class="cv-subject">英　　　語</p>
  <p class="cv-sub">（ 90 分 ）</p>
  <p class="cv-kind">{label}</p>
  <p class="cv-range">{rng}</p>
  <p class="cv-univ">{UNIV} 一般選抜 前期日程 対策</p>
</div>
<div class="cv-notes"><p class="cv-notes-h">はじめに読むこと</p><ol>{lis}</ol></div>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>出題の傾向を研究し，編集部が一から書き下ろした演習用の冊子です。</span></div>
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>第{R['n']}回 ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


def head(k, name, pts, suffix=''):
    return f'<h2 class="part"><span class="pnum">Part {k}</span>{name}{suffix}（{pts} 点）</h2>'


def notes_html(notes):
    if not notes:
        return ''
    return '<table class="notes"><tr><th>注</th><td>' + '　'.join(
        f'<span class="note"><i>{e(w)}</i>　{e(j)}</span>' for w, j in notes) + '</td></tr></table>'


def choices_html(ch):
    longest = max(len(c) for c in ch)
    cols = 4 if longest <= 16 else (2 if longest <= 38 else 0)
    if cols:
        return f'<div class="cgrid c{cols}">' + ''.join(f'<span><span class="sl">{LET[i]}.</span> {m(c)}</span>' for i, c in enumerate(ch)) + '</div>'
    return '<ol class="choices ind">' + ''.join(f'<li><span class="cl">{LET[i]}.</span> {m(c)}</li>' for i, c in enumerate(ch)) + '</ol>'


def part1(R):
    P = R['P1']
    body = head(1, '読解', P['points']) + f'<p class="lead">{m(P["lead"])}</p><p class="ptitle">{e(P["title"])}</p>'
    body += ''.join(f'<p class="en"><span class="pno">{i + 1}</span>{m(p)}</p>' for i, p in enumerate(P['passage']))
    body += notes_html(P.get('notes'))
    for i, q in enumerate(P['questions'], 1):
        body += f'<div class="q en-q"><span class="qk">{i}</span><div class="qbody"><div>{m(q["stem"])}</div>{choices_html(q["choices"])}</div></div>'
    return page(body, 'flow')


def part2(R):
    P = R['P2']
    body = head(2, '英作文', P['points']) + f'<p class="lead">{m(P["lead"])}</p><div class="topic en-topic">{m(P["prompt"])}</div>'
    return body


def part3(R):
    P = R['P3']
    body = head(3, '会話', P['points']) + f'<p class="lead">{m(P["lead"])}</p>'
    if P['type'] == 'choose':
        body += '<ol class="opts">' + ''.join(f'<li><span class="cl">{CIRC[i]}</span> {m(o)}</li>' for i, o in enumerate(P['options'])) + '</ol>'
        for i, cv in enumerate(P['convs'], 1):
            body += f'<div class="cvq"><span class="qk">{i}</span><table class="conv">' + ''.join(
                f'<tr><th>{e(s)}:</th><td>{m(t)}</td></tr>' for s, t in cv) + '</table></div>'
    else:
        if P.get('info'):
            body += f'<div class="art"><p class="art-t">{e(P["info"]["title"])}</p>' + ''.join(f'<p class="en">{m(x)}</p>' for x in P['info']['lines']) + '</div>'
        body += '<table class="conv">' + ''.join(f'<tr><th>{e(s)}:</th><td>{m(t)}</td></tr>' for s, t in P['conv']) + '</table>'
    return body


def part4(R):
    P = R['P4']
    body = head(4, '読んで意見を書く', P['points']) + f'<p class="lead">{m(P["lead"])}</p>'
    body += f'<div class="art"><p class="art-t">{e(P["title"])}</p>' + ''.join(f'<p class="en">{m(x)}</p>' for x in P['article']) + '</div>'
    body += f'<div class="topic en-topic">{m(P["question"])}</div>'
    return body


def parts_234(R):
    return page(part2(R) + '<div class="gap"></div>' + part3(R), 'flow') + page(part4(R), 'flow')


# ───────── 解答用紙 ─────────

def sheet_head(R, k):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">予想問題 第{R["n"]}回 英語　{k}枚目／3枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def lines(n):
    return ''.join('<div class="ln ln4"></div>' for _ in range(n))


SCORE = '<div class="score">得　点<div></div></div>'


def grid(labels, cls='ast'):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels)
    td = ''.join('<td></td>' for _ in labels)
    return f'<table class="{cls}"><tr>{th}</tr><tr>{td}</tr></table>'


def sheets(R):
    s1 = sheet_head(R, 1) + '<p><span class="bignum">Part 1</span></p>'
    s1 += grid([str(i) for i in range(1, 11)], 'ast g10') + grid([str(i) for i in range(11, 21)], 'ast g10')
    s1 += '<p><span class="bignum">Part 3</span></p>'
    P3 = R['P3']
    if P3['type'] == 'choose':
        s1 += grid([str(i) for i in range(1, len(P3['convs']) + 1)], 'ast g4')
    else:
        for i in range(len(P3['answers'])):
            s1 += f'<p class="sq">（{i + 1}）</p>' + lines(2)
    s2 = sheet_head(R, 2) + '<p><span class="bignum">Part 2</span><span class="wc-box">（　　　　）語</span></p>' + lines(22)
    s3 = sheet_head(R, 3) + '<p><span class="bignum">Part 4</span><span class="wc-box">（　　　　）語</span></p>' + lines(14)
    return ''.join(page(x + SCORE, 'sheet') for x in (s1, s2, s3))


def colophon(R, kind):
    return page(f'''
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 第{R['n']}回 英語 {'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程（個別学力検査「英語」・環境学部／経営学部 共通）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>Part 1 読解（4択20問）／Part 2 150語以上の英作文／Part 3 会話の空所／Part 4 短い記事を読んで80〜100語の意見／90 分（配点 40・24・12・24 は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
''', 'colophon')


# ───────── 検査と解答・解説編 ─────────

def akey_table(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c:g}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total:g}</td></tr></table>'


def crit(cr):
    total = sum(p for _, p in cr)
    return f'<div class="crit"><p class="crit-h">採点の目安（{total:g}点）</p><ul>' + ''.join(f'<li>{m(t)}（{p:g}点）</li>' for t, p in cr) + '</ul></div>'


def check_p1(P):
    qs = P['questions']
    assert len(qs) == 20, ('P1 設問数', len(qs))
    wc = wcount(plain(' '.join(P['passage'])))
    assert P1_WORDS[0] <= wc <= P1_WORDS[1], ('P1 本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), ('P1 全訳の段落数', len(P['translation']), len(P['passage']))
    n = len(P['passage'])
    cnt = {k: 0 for k in LET}
    for i, q in enumerate(qs, 1):
        assert len(q['choices']) == 4 and len(set(q['choices'])) == 4, ('P1 選択肢', i)
        assert q['answer'] in LET, ('P1 答え', i)
        cnt[q['answer']] += 1
        for k in re.findall(r'paragraph (\d+)', q['stem']):
            assert 1 <= int(k) <= n, ('P1 段落番号', i, k)
        if q.get('word'):
            w, k = q['word']
            assert re.search(r'\b' + re.escape(w) + r'\b', P['passage'][k - 1], re.I), ('P1 語が段落にない', i, w, k)
            assert f'"{w}"' in q['stem'] and f'paragraph {k}' in q['stem'], ('P1 語・段落の表示', i)
        assert q.get('expl'), ('P1 解説', i)
    assert all(3 <= v <= 7 for v in cnt.values()), ('P1 答えの偏り', cnt)
    return wc


def a_part1(R):
    P = R['P1']
    wc = check_p1(P)
    per = P['points'] / 20
    rows = [(str(i), q['answer'], per) for i, q in enumerate(P['questions'], 1)]
    body = head(1, '読解', P['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey_table(rows)
    body += '<p class="ah">解説</p><ul class="tips p1ex">' + ''.join(
        f'<li><b>{i}</b>（{q["answer"]}）　{m(q["expl"])}</li>' for i, q in enumerate(P['questions'], 1)) + '</ul>'
    body += '<p class="ah">全訳</p>' + ''.join(f'<p class="trp"><span class="pno">{i + 1}</span>{m(t)}</p>' for i, t in enumerate(P['translation']))
    if P.get('vocab'):
        body += '<p class="ah">語句</p><div class="vocab">' + ''.join(f'<span class="vw"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['vocab']) + '</div>'
    return page(body, 'flow')


def a_writing(P, k, name, lo, hi):
    wc = wcount(plain(P['model']))
    assert lo <= wc <= hi, (f'P{k} 解答例の語数', wc)
    assert sum(p for _, p in P['criteria']) == P['points'], (f'P{k} 採点の目安の合計',)
    body = head(k, name, P['points'], ' — 解答・解説')
    body += f'<p class="ah">解答例（{wc} 語）</p><div class="model-en">' + ''.join(f'<p>{m(x)}</p>' for x in P['model'].split('\n')) + '</div>'
    body += '<p class="ah">解答例の訳</p>' + ''.join(f'<p class="trp">{m(x)}</p>' for x in P['model_ja'])
    body += '<p class="ah">書き方のポイント</p><ul class="tips">' + ''.join(f'<li>{m(t)}</li>' for t in P['tips']) + '</ul>' + crit(P['criteria'])
    return body, wc


def a_part3(R):
    P = R['P3']
    body = head(3, '会話', P['points'], ' — 解答・解説')
    if P['type'] == 'choose':
        assert len(P['convs']) == len(P['options']) == len(P['answers']) == len(P['expl'])
        assert sorted(P['answers']) == list(range(len(P['options']))), ('P3 選択肢は1回ずつ', P['answers'])
        assert P['answers'] != list(range(len(P['options']))), ('P3 答えが①②③④の順',)
        for cv in P['convs']:
            assert sum(t.count('{blank}') for _, t in cv) == 1, ('P3 空所は会話に1つ',)
        per = P['points'] / len(P['convs'])
        rows = [(str(i + 1), f'{CIRC[a]} {P["options"][a]}', per) for i, a in enumerate(P['answers'])]
    else:
        n = sum(len(re.findall(r'\{c\d\}', t)) for _, t in P['conv'])
        assert n == len(P['answers']) == len(P['expl']), ('P3 空所の数', n)
        per = P['points'] / n
        rows = [(f'（{i + 1}）', ' ／ '.join(a), per) for i, a in enumerate(P['answers'])]
    assert per == int(per), ('P3 配点',)
    body += '<p class="ah">解答一覧（／ は別解）</p>' + akey_table(rows)
    body += '<ul class="tips">' + ''.join(f'<li><b>{i + 1}</b>　{m(x)}</li>' for i, x in enumerate(P['expl'])) + '</ul>'
    body += '<p class="ah">訳</p>' + ''.join(f'<p class="trp">{m(t)}</p>' for t in P['ja'])
    return body


def a_part4(R):
    P = R['P4']
    wc = wcount(plain(' '.join(P['article'])))
    assert P4_WORDS[0] <= wc <= P4_WORDS[1], ('P4 記事の語数', wc)
    body, _ = a_writing(P, 4, '読んで意見を書く', 80, 100)
    body += f'<p class="ah">記事の訳（{wc} 語）</p>' + ''.join(f'<p class="trp">{m(t)}</p>' for t in P['article_ja'])
    body += f'<p class="ah">問いの訳</p><p class="trp">{m(P["question_ja"])}</p>'
    return body


def build(R, kind, ranges):
    if kind == 'q':
        parts = cover(R, 'q', ranges) + part1(R) + parts_234(R) + sheets(R) + colophon(R, 'q')
    else:
        p2, _ = a_writing(R['P2'], 2, '英作文', 150, 185)
        p2 += f'<p class="ah">問いの訳</p><p class="trp">{m(R["P2"]["prompt_ja"])}</p>'
        parts = (cover(R, 'a', ranges) + a_part1(R) + page(p2, 'flow') + page(a_part3(R), 'flow')
                 + page(a_part4(R), 'flow') + colophon(R, 'a'))
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
