# -*- coding: utf-8 -*-
"""茨城大学 一般選抜（前期日程）対策 英語 予想問題 — 紙面づくり（2026-11-04）

  python3 scripts/gacha-prints/ibaraki_mock/render.py r1      # 第1回（r1.py）
  python3 scripts/gacha-prints/ibaraki_mock/render.py all     # 3冊すべて
→ .tmpwork/ibaraki/out/予想問題_茨城大学_英語_第N回_{問題,解答解説}.pdf
  と public/prints/print_lr_niji_ibaraki_en_N.pdf（問題＋解答・解説）

参考にしたのは公開されている出題の「形」だけ（令和7・8年度の問題冊子の設問文・解答例）。
  前期の英語は人文社会科学部・工学部・農学部・地域未来共創学環の共通問題（90分・200点）。
  Ⅰ・Ⅱ 長文読解（下線部和訳・下線部の内容を日本語で説明）／Ⅲ 長文読解（設問も解答も英語・5問）
  ／Ⅳ 日本語の文章の下線部2か所を，内容をかみくだいて英語で表現する。
大問の配点は大学が公表していないため編集部の想定（各50点）。
英文・日本文・設問・解答はすべて書き下ろしで，過去問の文章・設問文・解答例は引用していない。
"""
import html, importlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'ibaraki' / 'out'
UNIV = '茨城大学'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'

T = {'id': 'ibaraki', 'name': '人文社会科学部・工学部・農学部・地域未来共創学環（共通問題）', 'short': '共通問題',
     'min': 90, 'total': 200, 'points': {'P1': 50, 'P2': 50, 'P3': 50, 'P4': 50}, 'words': (430, 640),
     'time': 'Ⅰ 25 分，Ⅱ 25 分，Ⅲ 20 分，Ⅳ 15 分，見直し 5 分'}
ROMAN = {'P1': 'Ⅰ', 'P2': 'Ⅱ', 'P3': 'Ⅲ', 'P4': 'Ⅳ'}


def e(s):
    return html.escape(str(s), quote=False)


def m(s):
    """{u1|…} 下線＋(1)、**…** 太字、//…// 斜体、{br} 改行、word* は注の印"""
    t = e(s)
    t = re.sub(r'\{u(\d)\|(.+?)\}',
               lambda x: f'<span class="ul"><span class="ulab">({x.group(1)})</span>{x.group(2)}</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def plain(s):
    t = re.sub(r'\{u\d\|(.+?)\}', r'\1', s)
    return re.sub(r'\*\*|//|\{br\}|\*', ' ', t)


def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


CSS = (HERE / 'style.css').read_text(encoding='utf-8') + '''
.jq { margin: 1.6mm 0; padding-left: 10mm; text-indent: -10mm; font-size: 9.8pt; }
.jq .cl { width: 10mm; font-family: 'Noto Sans CJK JP', sans-serif; font-weight: bold; font-size: 9pt; }
.eq { margin: 1.4mm 0; padding-left: 7mm; text-indent: -7mm; font-family: 'Noto Serif', 'Times New Roman', serif; font-size: 10.2pt; line-height: 1.7; }
.eq .cl { width: 7mm; font-weight: bold; }
.ja-p { text-align: justify; margin: 0 0 1.8mm; font-size: 10pt; line-height: 1.95; text-indent: 1em; font-family: 'Noto Serif CJK JP', serif; }
.reph { margin: 1mm 0 1.5mm; padding: 1.5mm 3mm; background: #f3f3f3; font-size: 9pt; line-height: 1.7; }
.sh-t { white-space: nowrap; }
'''


def page(body, cls=''):
    return f'<section class="page {cls}">{body}</section>'


def logo():
    return f'<img class="logo" src="file://{HERE / "logo_gray.png"}" alt="マナトビ">'


def pts_text():
    return '・'.join(f'{ROMAN[k]} {v}' for k, v in T['points'].items())


def cover(R, kind, ranges):
    label = '問　題' if kind == 'q' else '解答・解説'
    rng = (f'（問題 {ranges[0]}〜{ranges[1]} ページ・解答用紙 {ranges[2]}〜{ranges[3]} ページ）' if kind == 'q'
           else f'（解答・解説 {ranges[0]}〜{ranges[1]} ページ）')
    if kind == 'q':
        notes = [f'解答時間は {T["min"]} 分。時間の目安は，{T["time"]}。',
                 f'大問はⅠ〜Ⅳの 4 題。{T["total"]} 点満点（{pts_text()}）。配点は大学が公表していないため編集部の想定である。',
                 'Ⅰ・Ⅱは日本語で，Ⅲは英語で答えること。Ⅳは日本文の下線部を英語で書くこと。',
                 '答えは巻末の解答用紙の決められた欄に書くこと。',
                 '英文・日本文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値はすべて架空である。']
    else:
        notes = ['各大問の最初に配点（編集部の想定）をまとめた。',
                 '解答は一例である。「採点の目安」の要素がそろっていれば，表現が違っても得点としてよい。',
                 'Ⅰ〜Ⅲには全訳と語句をつけた。答え合わせのあと，根拠になる段落をもう一度読み直すこと。',
                 'Ⅳは日本語をいったん英語にしやすい形に言いかえてから書く手順を示した。']
    lis = ''.join(f'<li>{e(x)}</li>' for x in notes)
    return page(f'''
<div class="cv-head">{logo()}<span>学習アプリ マナトビ ｜ 国公立2次 予想問題</span></div>
<div class="cv-main">
  <p class="cv-round">予想問題 第{R['n']}回</p>
  <p class="cv-subject">英　　　語</p>
  <p class="cv-sub">（ {T['min']} 分 ・ {T['total']} 点 ）</p>
  <p class="cv-kind">{label}</p>
  <p class="cv-range">{rng}</p>
  <p class="cv-univ">{UNIV} 一般選抜 前期日程 対策<br>{T['name']}</p>
</div>
<div class="cv-notes"><p class="cv-notes-h">はじめに読むこと</p><ol>{lis}</ol></div>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>出題の傾向を研究し，編集部が一から書き下ろした演習用の冊子です。</span></div>
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>{UNIV} 第{R['n']}回 ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


def head(k, name, pts, suffix=''):
    return f'<h2 class="part"><span class="pnum">{ROMAN[k]}</span>{name}{suffix}（配点 {pts}）</h2>'


def notes_html(P):
    if not P.get('notes'):
        return ''
    return '<table class="notes"><tr><th>注</th><td>' + '　'.join(
        f'<span class="note"><i>{e(w)}</i>：{e(j)}</span>' for w, j in P['notes']) + '</td></tr></table>'


def passage_html(P):
    title = f'<p class="ptitle">{e(P["title"])}</p>' if P.get('title') else ''
    return title + ''.join(f'<p class="en">{m(p)}</p>' for p in P['passage']) + notes_html(P)


def part_read(R, k):
    P = R[k]
    body = head(k, '読解問題', P['points'])
    body += f'<p class="lead">{m(P.get("lead", "以下の英文を読んで，あとの設問に答えよ。"))}</p>' + passage_html(P)
    body += '<p class="qhead">［設問］</p>' + ''.join(
        f'<p class="jq"><span class="cl">問 {i}</span>{m(q["stem"])}</p>' for i, q in enumerate(P['questions'], 1))
    return page(body, 'flow')


def part_eqa(R, k):
    P = R[k]
    body = head(k, '読解問題（英語で答える）', P['points'])
    body += '<p class="lead">以下の英文を読み，あとの問い 1〜5 に英語で答えよ。</p>' + passage_html(P)
    body += '<p class="qhead">［問い］</p>' + ''.join(
        f'<p class="eq"><span class="cl">{i}.</span>{e(q["q"])}</p>' for i, q in enumerate(P['questions'], 1))
    return page(body, 'flow')


def part_ja(R, k):
    P = R[k]
    body = head(k, '英語による表現', P['points'])
    body += ('<p class="lead">次の文章を読み，下線部(1)・(2)の意味するところを，前後の流れに合う自然な英語で書け。'
             '日本語を一語ずつ置きかえる必要はない。</p>')
    if P.get('title'):
        body += f'<p class="ptitle">{e(P["title"])}</p>'
    body += ''.join(f'<p class="ja-p">{m(p)}</p>' for p in P['passage'])
    return page(body, 'flow')


# ───────── 解答用紙 ─────────

def sheet_head(R, i, n):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">{UNIV} 第{R["n"]}回　{i}枚目／{n}枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def lines(n):
    return ''.join('<div class="ln ln4"></div>' for _ in range(n))


SCORE = '<div class="score">得　点<div></div></div>'


def sheets(R):
    n = 4
    s = []
    for i, k in enumerate(('P1', 'P2'), 1):
        x = sheet_head(R, i, n) + f'<p><span class="bignum">{ROMAN[k]}</span></p>'
        for j, q in enumerate(R[k]['questions'], 1):
            x += f'<p class="sq">問 {j}</p>' + lines(q.get('lines', 3))
        s.append(x + SCORE)
    x = sheet_head(R, 3, n) + '<p><span class="bignum">Ⅲ</span></p>'
    for j, q in enumerate(R['P3']['questions'], 1):
        x += f'<p class="sq">{j}.</p>' + lines(q.get('lines', 3))
    s.append(x + SCORE)
    x = sheet_head(R, 4, n) + '<p><span class="bignum">Ⅳ</span></p>'
    for j in range(1, len(R['P4']['items']) + 1):
        x += f'<p class="sq">({j})</p>' + lines(7)
    s.append(x + SCORE)
    return ''.join(page(y, 'sheet') for y in s)


def colophon(R, kind):
    kosei = 'Ⅰ・Ⅱ 読解（下線部和訳・内容説明）／Ⅲ 読解（英問英答）／Ⅳ 日本文の下線部を英語で表現'
    return page(f'''
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 {UNIV} 第{R['n']}回 英語 {'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程（{T['name']}・個別学力検査「英語」）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>{kosei}／{T['min']} 分／{T['total']} 点（{pts_text()}。配点は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・日本文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
''', 'colophon')


# ───────── 解答・解説編 ─────────

def crit(items, title='採点の目安'):
    total = sum(p for _, p in items)
    lis = ''.join(f'<li>{m(t)}（{p:g}点）</li>' for t, p in items)
    return f'<div class="crit"><p class="crit-h">{title}（{total:g}点）</p><ul>{lis}</ul></div>'


def akey(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c:g}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total:g}</td></tr></table>'


def translation_html(P):
    tr = ''.join(f'<p class="trp">{m(t)}</p>' for t in P['translation'])
    vocab = ''
    if P.get('vocab'):
        vocab = '<p class="ah">語句</p><div class="vocab">' + ''.join(
            f'<span class="vw"><i>{e(w)}</i>　{e(j)}</span>' for w, j in P['vocab']) + '</div>'
    return f'<p class="ah">全訳</p>{tr}{vocab}'


def check_passage(k, P):
    text = ' '.join(P['passage'])
    wc = wcount(plain(text))
    assert T['words'][0] <= wc <= T['words'][1], (k, '本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), (k, '全訳の段落数', len(P['translation']), len(P['passage']))
    for w, _ in P.get('notes', []):
        assert re.search(re.escape(w) + r'\*', text), (k, '注の印がない', w)
    return text, wc


def a_read(R, k):
    P = R[k]
    text, wc = check_passage(k, P)
    refs = [int(x) for x in re.findall(r'\{u(\d)\|', text)]
    qrefs = [r for q in P['questions'] for r in (q.get('refs') or ([q['ref']] if q.get('ref') else []))]
    assert refs == list(range(1, len(refs) + 1)), (k, '下線の番号', refs)
    assert sorted(qrefs) == refs, (k, '下線と設問の対応', refs, qrefs)
    assert len(P['questions']) == 4, (k, '設問数')
    for q in P['questions']:
        assert sum(p for _, p in q['criteria']) == q['points'], (k, '採点基準の合計', q['stem'][:20])
    rows = [(f'問 {i}', '解答例を参照', q['points']) for i, q in enumerate(P['questions'], 1)]
    assert sum(r[2] for r in rows) == P['points'], (k, '配点の合計')
    body = head(k, '読解問題', P['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">配点</p>' + akey(rows)
    for i, q in enumerate(P['questions'], 1):
        body += f'<h3 class="aq"><span class="qk">問 {i}</span>{e(q["kind"])}（{q["points"]}点）</h3>'
        body += f'<p class="ans">【解答例】{m(q["answer"])}</p>'
        if q.get('expl'):
            body += f'<p class="expl">{m(q["expl"])}</p>'
        body += crit(q['criteria'])
    return page(body + translation_html(P), 'flow')


def a_eqa(R, k):
    P = R[k]
    text, wc = check_passage(k, P)
    assert '{u' not in text, (k, 'Ⅲに下線は使わない')
    assert len(P['questions']) == 5, (k, '問いの数')
    for i, q in enumerate(P['questions'], 1):
        assert sum(p for _, p in q['criteria']) == q['points'], (k, '採点基準の合計', i)
        assert 2 <= wcount(q['answer']) <= 32, (k, '解答の語数', i, wcount(q['answer']))
        assert q['q'].rstrip().endswith('?'), (k, '問いは疑問文', i)
    rows = [(f'{i}.', q['answer'], q['points']) for i, q in enumerate(P['questions'], 1)]
    assert sum(r[2] for r in rows) == P['points'], (k, '配点の合計')
    body = head(k, '読解問題（英語で答える）', P['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey(rows)
    for i, q in enumerate(P['questions'], 1):
        body += f'<h3 class="aq"><span class="qk">{i}.</span>{e(q["q"])}（{q["points"]}点）</h3>'
        body += f'<p class="ans">【解答例】<span class="en-ans">{m(q["answer"])}</span></p>'
        if q.get('alt'):
            body += f'<p class="ans">【別解】<span class="en-ans">{m(q["alt"])}</span></p>'
        body += f'<p class="expl">{m(q["expl"])}</p>' + crit(q['criteria'])
    return page(body + translation_html(P), 'flow')


def a_ja(R, k):
    P = R[k]
    text = ''.join(P['passage'])
    refs = [int(x) for x in re.findall(r'\{u(\d)\|', text)]
    assert refs == list(range(1, len(P['items']) + 1)) == [1, 2], (k, '下線の番号', refs)
    assert sum(it['points'] for it in P['items']) == P['points'], (k, '配点')
    rows = [(f'({i})', '解答例を参照', it['points']) for i, it in enumerate(P['items'], 1)]
    body = head(k, '英語による表現', P['points'], ' — 解答・解説') + akey(rows)
    segs = re.findall(r'\{u\d\|(.+?)\}', text)
    for i, (it, seg) in enumerate(zip(P['items'], segs), 1):
        assert sum(p for _, p in it['criteria']) == it['points'], (k, '採点基準', i)
        assert len(it['models']) == 2, (k, '解答例は2つ', i)
        body += f'<h3 class="aq"><span class="qk">({i})</span>{e(seg)}（{it["points"]}点）</h3>'
        body += f'<p class="reph">【英語にしやすい日本語に言いかえる】{m(it["rephrase"])}</p>'
        body += ''.join(f'<p class="ans">【解答例{j}】<span class="en-ans">{m(t)}</span></p>' for j, t in enumerate(it['models'], 1))
        body += '<ul class="tips">' + ''.join(f'<li>{m(t)}</li>' for t in it['tips']) + '</ul>' + crit(it['criteria'])
    return page(body, 'flow')


def build(R, kind, ranges):
    if kind == 'q':
        mid = part_read(R, 'P1') + part_read(R, 'P2') + part_eqa(R, 'P3') + part_ja(R, 'P4')
        parts = cover(R, 'q', ranges) + mid + sheets(R) + colophon(R, 'q')
    else:
        mid = a_read(R, 'P1') + a_read(R, 'P2') + a_eqa(R, 'P3') + a_ja(R, 'P4')
        parts = cover(R, 'a', ranges) + mid + colophon(R, 'a')
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{parts}</body></html>'


def pdf(html_text, path, label):
    hp = path.with_suffix('.html')
    hp.write_text(html_text, encoding='utf-8')
    subprocess.run(['node', str(HERE / 'pdf.mjs'), str(hp), str(path), label], check=True)


def page_texts(path):
    import unicodedata
    from pypdf import PdfReader
    return [unicodedata.normalize('NFKC', re.sub(r'\s+', '', p.extract_text() or '')) for p in PdfReader(str(path)).pages]


def render(key):
    n = int(key[1])
    R = importlib.import_module(key).ROUND
    assert R['n'] == n
    for k, v in T['points'].items():
        assert R[k]['points'] == v, (k, R[k]['points'])
    OUT.mkdir(parents=True, exist_ok=True)
    q = OUT / f'予想問題_{UNIV}_英語_第{n}回_問題.pdf'
    a = OUT / f'予想問題_{UNIV}_英語_第{n}回_解答解説.pdf'
    lab = f'{UNIV} 第{n}回'
    pdf(build(R, 'a', (1, 1)), a, f'{lab} 解答・解説')
    pdf(build(R, 'q', (1, 1, 1, 1)), q, f'{lab} 問題')
    t = page_texts(q)
    first_sheet = next(i for i, s in enumerate(t) if '解答用紙' in s and '受験番号' in s) + 1
    last = len(t)
    qr = (2, first_sheet - 1, first_sheet, last - 1)
    pdf(build(R, 'q', qr), q, f'{lab} 問題')
    ar = (2, len(page_texts(a)) - 1)
    pdf(build(R, 'a', ar), a, f'{lab} 解答・解説')
    assert len(page_texts(q)) == last, 'ページ数が2回目で変わった'
    dest = ROOT / 'public' / 'prints' / f'print_lr_niji_{T["id"]}_en_{n}.pdf'
    subprocess.run(['pdfunite', str(q), str(a), str(dest)], check=True)
    print(f'{key}: 問題 {last}p（解答用紙 {qr[2]}〜{qr[3]}）・解答解説 {ar[1] + 1}p → {dest.relative_to(ROOT)} {dest.stat().st_size // 1024}KB')


if __name__ == '__main__':
    sys.path.insert(0, str(HERE))
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    keys = ['r1', 'r2', 'r3'] if arg == 'all' else sys.argv[1:]
    for key in keys:
        render(key)
