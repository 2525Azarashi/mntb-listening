# -*- coding: utf-8 -*-
"""群馬大学 一般選抜（前期日程）情報学部 英語 予想問題 — 紙面づくり（2026-11-05）

  python3 scripts/gacha-prints/gunma_mock/render_j.py j1     # 第1回（j1.py）
  python3 scripts/gacha-prints/gunma_mock/render_j.py all    # 3冊すべて
→ .tmpwork/gunma/out/ と public/prints/print_lr_niji_gunmaj_en_N.pdf（問題＋解答・解説）

参考にしたのは公開されている出題の「形」だけ（令和6〜8年度の問題冊子の設問と解答例）。
  1・2 長文読解（語の選択・語の組み合わせ・下線部和訳・日本語での説明・内容一致の〇×）
  3 日本語の会話（3つのせりふ）を英語で表現する
120分・400点（募集要項）。大問の配点（150・150・100）は編集部の想定。
英文・設問・解答はすべて書き下ろしで，過去問の英文・設問文・解答例は引用していない。
"""
import html, importlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / '.tmpwork' / 'gunma' / 'out'
UNIV = '群馬大学'
DISCLAIMER = f'{UNIV}の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。'
T = {'id': 'gunmaj', 'name': '情報学部', 'min': 120, 'total': 400,
     'points': {'P1': 150, 'P2': 150, 'P3': 100}, 'words': (620, 900),
     'time': '大問1 50 分，大問2 45 分，大問3 20 分，見直し 5 分'}
KANA = 'アイウエオ'
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'


def e(s):
    return html.escape(str(s), quote=False)


def m(s):
    """{u:b|…} 下線＋(b)、{b:a} 空所（a）、**…** 太字、//…// 斜体"""
    t = e(s)
    t = re.sub(r'\{u:([a-z])\|(.+?)\}', lambda x: f'<span class="ul"><span class="ulab">({x.group(1)})</span>{x.group(2)}</span>', t)
    t = re.sub(r'\{b:([a-z])\}', lambda x: f'<span class="blank">（　{x.group(1)}　）</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'//(.+?)//', r'<i>\1</i>', t)
    return t.replace('{br}', '<br>')


def plain(s):
    t = re.sub(r'\{u:[a-z]\|(.+?)\}', r'\1', s)
    t = re.sub(r'\{b:[a-z]\}', ' ', t)
    return re.sub(r'\*\*|//|\{br\}', ' ', t)


def wcount(text):
    return len(re.findall(r"[A-Za-z0-9'’.%-]*[A-Za-z0-9]", text))


CSS = (HERE / 'style.css').read_text(encoding='utf-8') + '''
.jq { margin: 2.2mm 0 0.8mm; padding-left: 10mm; text-indent: -10mm; font-size: 9.8pt; line-height: 1.65; }
.jq .cl { display: inline-block; width: 10mm; text-indent: 0; font-family: 'Noto Sans CJK JP', sans-serif; font-weight: bold; font-size: 9pt; }
.opt { margin: 0.3mm 0 0.3mm 13mm; padding-left: 7mm; text-indent: -7mm; font-size: 9.8pt; line-height: 1.55; }
.opt .en-o { font-family: 'Noto Serif', 'Times New Roman', serif; font-size: 10pt; }
.combo { border-collapse: collapse; margin: 1mm 0 1mm 14mm; font-family: 'Noto Serif', 'Times New Roman', serif; font-size: 10pt; }
.combo td, .combo th { padding: 0.4mm 4mm; text-align: left; }
.combo th { font-family: 'Noto Sans CJK JP', sans-serif; font-size: 8.8pt; font-weight: normal; }
.pn { font-family: 'Noto Sans CJK JP', sans-serif; font-size: 9pt; margin-right: 1.5mm; }
.pnotes { font-size: 8.6pt; line-height: 1.55; margin: 2mm 0 1mm; border-top: 1px solid #777; padding-top: 1mm; }
.pnotes p { margin: 0.2mm 0; }
.pnotes i { font-family: 'Noto Serif', 'Times New Roman', serif; }
.jdlg { margin: 2mm 0 2mm 2mm; font-size: 10.4pt; line-height: 1.9; }
.jdlg p { margin: 0.6mm 0; padding-left: 9mm; text-indent: -9mm; }
.model-en p { text-align: left; }
'''


def page(body, cls=''):
    return f'<section class="page {cls}">{body}</section>'


def logo():
    return f'<img class="logo" src="file://{HERE / "logo_gray.png"}" alt="マナトビ">'


def pts_text():
    return '・'.join(f'大問{k[1]} {v}' for k, v in T['points'].items())


def cover(R, kind, ranges):
    label = '問　題' if kind == 'q' else '解答・解説'
    rng = (f'（問題 {ranges[0]}〜{ranges[1]} ページ・解答用紙 {ranges[2]}〜{ranges[3]} ページ）' if kind == 'q'
           else f'（解答・解説 {ranges[0]}〜{ranges[1]} ページ）')
    if kind == 'q':
        notes = [f'解答時間は {T["min"]} 分。時間の目安は，{T["time"]}。',
                 f'問題は大問1〜3の 3 題。{T["total"]} 点満点（{pts_text()}）。大問の配点は大学が公表していないため編集部の想定である。',
                 '情報学部の前期日程の個別試験は「数学」と「英語」から 1 科目以上を出願時に選ぶ（2027年度の募集要項による）。この冊子は「英語」の対策用である。',
                 '記号で答える問題は記号を，日本語で答える問題は日本語で書く。答えは巻末の解答用紙の決められた欄に書くこと。',
                 '英文はすべて編集部が新しく作ったもので，人物・団体・地名・調査・数値はすべて架空である。']
    else:
        notes = ['各大問の最初に解答一覧と配点（編集部の想定）をまとめた。',
                 '和訳・説明・英訳の解答は一例である。「採点の目安」の要素がそろっていれば，表現が違っても得点としてよい。',
                 '大問1・2には全訳をつけた。答え合わせのあと，根拠になる段落をもう一度読み直すこと。',
                 '大問3は解答例を2つと，せりふごとの解説・まちがえやすい点を示した。']
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
<div class="cv-foot"><span>学習アプリ マナトビ 編集部</span><span>{UNIV} {T['name']} 第{R['n']}回 ／ {'問題' if kind == 'q' else '解答・解説'}</span></div>
''', 'cover')


def head(k, name, pts, suffix=''):
    return f'<h2 class="part"><span class="pnum">{k[1]}</span>大問{k[1]}　{name}{suffix}（配点 {pts}）</h2>'


def passage_html(P):
    title = f'<p class="ptitle">{e(P["title"])}</p>' if P.get('title') else ''
    body = ''.join(f'<p class="en"><span class="pn">{CIRC[i]}</span>{m(p)}</p>' for i, p in enumerate(P['passage']))
    notes = ''
    if P.get('notes'):
        by = {}
        for para, w, j in P['notes']:
            by.setdefault(para, []).append(f'<i>{e(w)}</i> {e(j)}')
        notes = '<div class="pnotes"><p><b>注</b></p>' + ''.join(
            f'<p>第{CIRC[p - 1]}段落　' + '，'.join(v) + '</p>' for p, v in sorted(by.items())) + '</div>'
    return title + body + notes


def q_html(i, q):
    s = f'<p class="jq"><span class="cl">問 {i}</span>{m(q["stem"])}</p>'
    k = q['kind']
    if k == 'choice':
        s += ''.join(f'<p class="opt">（{KANA[j]}）<span class="en-o">{m(o)}</span></p>' for j, o in enumerate(q['options']))
    elif k == 'combo':
        hd = ''.join(f'<th>（ {x} ）</th>' for x in q['marks'])
        rows = ''.join(f'<tr><td>（{KANA[j]}）</td>' + ''.join(f'<td>{e(w)}</td>' for w in r) + '</tr>' for j, r in enumerate(q['rows']))
        s += f'<table class="combo"><tr><th></th>{hd}</tr>{rows}</table>'
    elif k == 'tf':
        s += ''.join(f'<p class="opt">（{KANA[j]}）<span class="en-o">{m(o)}</span></p>' for j, o in enumerate(q['statements']))
    return s


def part_read(R, k, name):
    P = R[k]
    body = head(k, name, P['points'])
    body += (f'<p class="lead">{e(P["intro"])}これを読んで，問 1〜問 {len(P["questions"])} に答えよ。答えは解答用紙の決められた欄に書くこと。'
             f'（{CIRC[0]}〜{CIRC[len(P["passage"]) - 1]} は段落の番号を表す。）</p>')
    body += passage_html(P) + '<p class="qhead">［設問］</p>' + ''.join(q_html(i, q) for i, q in enumerate(P['questions'], 1))
    return page(body, 'flow')


P3_LEAD = 'ＡさんとＢさんの会話を英語で表現せよ。答えは解答用紙の決められた欄に書くこと。'


def part_comp(R):
    P = R['P3']
    body = head('P3', '和文英訳（会話文）', P['points']) + f'<p class="lead">{e(P3_LEAD)}</p>'
    if P.get('scene'):
        body += f'<p class="small">（場面：{e(P["scene"])}）</p>'
    body += '<div class="jdlg">' + ''.join(f'<p>{e(s)}：{e(t)}</p>' for s, t in P['lines']) + '</div>'
    return page(body, 'flow')


def sheet_head(R, i, n):
    return (f'<div class="sh-head"><span class="sh-t">解答用紙</span><span class="sh-s">{UNIV} {T["name"]} 第{R["n"]}回　{i}枚目／{n}枚</span>'
            f'<span class="sh-name">受験番号　　　　　　　氏名</span></div>')


def lines(n):
    return ''.join('<div class="ln ln4"></div>' for _ in range(n))


SCORE = '<div class="score">得　点<div></div></div>'


def sheet_read(R, k, i, n):
    s = sheet_head(R, i, n) + f'<p><span class="bignum">{k[1]}</span>大問{k[1]}</p>'
    for j, q in enumerate(R[k]['questions'], 1):
        if q['kind'] == 'ja':
            s += f'<p class="sq">問 {j}</p>' + lines(q.get('lines', 3))
        elif q['kind'] == 'tf':
            s += f'<p class="sq">問 {j}　' + '　'.join(f'（{KANA[x]}）［　　］' for x in range(len(q['statements']))) + '</p>'
        else:
            s += f'<p class="sq">問 {j}　［　　　　］</p>'
    return s + SCORE


def sheets(R):
    n = 3
    s = [sheet_read(R, 'P1', 1, n), sheet_read(R, 'P2', 2, n)]
    x = sheet_head(R, 3, n) + '<p><span class="bignum">3</span>大問3</p>'
    for sp, _ in R['P3']['lines']:
        x += f'<p class="sq">{e(sp)}</p>' + lines(4)
    s.append(x + SCORE)
    return ''.join(page(y, 'sheet') for y in s)


def colophon(R, kind):
    kosei = '大問1・大問2 長文読解（記号選択・下線部和訳・日本語での説明・内容一致）／大問3 日本語の会話を英語で表現'
    return page(f'''
<h2 class="colh">奥　付</h2>
<table class="col">
<tr><th>書名</th><td>国公立2次 予想問題 {UNIV} {T['name']} 第{R['n']}回 英語 {'問題' if kind == 'q' else '解答・解説'}</td></tr>
<tr><th>想定</th><td>{UNIV} 一般選抜 前期日程（{T['name']}・個別学力検査「英語」）の出題形式に準拠</td></tr>
<tr><th>構成</th><td>{kosei}／{T['min']} 分／{T['total']} 点（{pts_text()}。大問の配点は編集部の想定）</td></tr>
<tr><th>編集・作成</th><td>学習アプリ マナトビ 編集部（{R.get('date', '2026年11月')}）</td></tr>
</table>
<div class="disc"><b>{e(DISCLAIMER)}</b><br><span>英文・設問・解答・解説はすべて編集部の書き下ろしです。実際の試験の問題文・解答例の文章は引用していません。</span></div>
<p class="small">本冊子の無断転載・複製を禁じます。学習アプリ マナトビの利用者が個人の学習に使う範囲でご利用ください。</p>
''', 'colophon')


def crit(items, title='採点の目安'):
    total = sum(p for _, p in items)
    lis = ''.join(f'<li>{m(t)}（{p:g}点）</li>' for t, p in items)
    return f'<div class="crit"><p class="crit-h">{title}（{total:g}点）</p><ul>{lis}</ul></div>'


def akey(rows):
    body = ''.join(f'<tr><td>{e(a)}</td><td>{m(b)}</td><td class="pt">{c:g}</td></tr>' for a, b, c in rows)
    total = sum(c for _, _, c in rows)
    return f'<table class="akey"><tr><th>設問</th><th>解答</th><th>配点</th></tr>{body}<tr class="sum"><td>合計</td><td></td><td class="pt">{total:g}</td></tr></table>'


def short_answer(q):
    k = q['kind']
    if k in ('choice', 'combo'):
        return f'（{KANA[q["answer"]]}）'
    if k == 'tf':
        return '　'.join(f'（{KANA[x]}）{a}' for x, a in enumerate(q['answers']))
    return '解答例を参照'


def check_read(k, P):
    text = ' '.join(P['passage'])
    wc = wcount(plain(text))
    assert T['words'][0] <= wc <= T['words'][1], (k, '本文の語数', wc)
    assert len(P['translation']) == len(P['passage']), (k, '全訳の段落数', len(P['translation']), len(P['passage']))
    for para, w, _ in P.get('notes', []):
        assert w.lower() in plain(P['passage'][para - 1]).lower(), (k, '注の語が段落にない', para, w)
    marks = re.findall(r'\{[ub]:([a-z])', text)
    assert marks == list('abcdefghijklmnop'[:len(marks)]), (k, '印の順番', marks)
    need = [x for q in P['questions'] for x in q.get('marks', [])]
    assert need == marks, (k, '印と設問の対応', need, marks)
    ans = []
    for i, q in enumerate(P['questions'], 1):
        kd = q['kind']
        if kd == 'choice':
            assert len(q['options']) == 4 and len(set(q['options'])) == 4 and 0 <= q['answer'] < 4, (k, '選択肢', i)
            ans.append(q['answer'])
        elif kd == 'combo':
            assert len(q['rows']) == 4 and all(len(r) == len(q['marks']) for r in q['rows']), (k, '組み合わせ', i)
            assert len({tuple(r) for r in q['rows']}) == 4 and 0 <= q['answer'] < 4, (k, '組み合わせ', i)
            ans.append(q['answer'])
        elif kd == 'tf':
            assert len(q['statements']) == 4 and len(q['answers']) == 4 and set(q['answers']) == {'〇', '×'}, (k, '〇×', i)
        else:
            assert kd == 'ja', (k, kd)
            assert sum(p for _, p in q['criteria']) == q['points'], (k, '採点基準の合計', i)
    assert len(set(ans)) >= 3, (k, '記号の答えが偏っている', ans)
    assert sum(q['points'] for q in P['questions']) == P['points'], (k, '配点の合計', sum(q['points'] for q in P['questions']))
    return wc


def a_read(R, k, name):
    P = R[k]
    wc = check_read(k, P)
    rows = [(f'問 {i}', short_answer(q), q['points']) for i, q in enumerate(P['questions'], 1)]
    body = head(k, name, P['points'], ' — 解答・解説') + f'<p class="small">本文 {wc} 語</p><p class="ah">解答一覧</p>' + akey(rows)
    for i, q in enumerate(P['questions'], 1):
        body += f'<h3 class="aq"><span class="qk">問 {i}</span>{e(q["tag"])}（{q["points"]}点）</h3>'
        body += f'<p class="ans">【解答例】{m(q["answer"])}</p>' if q['kind'] == 'ja' else f'<p class="ans">【正解】{m(short_answer(q))}</p>'
        body += f'<p class="expl">{m(q["expl"])}</p>'
        if q['kind'] == 'ja':
            body += crit(q['criteria'])
    tr = ''.join(f'<p class="trp"><span class="pn">{CIRC[j]}</span>{m(t)}</p>' for j, t in enumerate(P['translation']))
    return page(body + f'<p class="ah">全訳</p>{tr}', 'flow')


def a_comp(R):
    P = R['P3']
    assert sum(p for _, p in P['criteria']) == P['points'], ('P3 採点基準',)
    assert len(P['expl']) == len(P['lines']) and all(len(md) == len(P['lines']) for md in P['models']), ('P3 解答例・解説の数',)
    body = head('P3', '和文英訳（会話文）', P['points'], ' — 解答・解説') + crit(P['criteria'])
    for j, md in enumerate(P['models'], 1):
        body += f'<p class="ah">解答例{j}</p><div class="model-en">' + ''.join(
            f'<p>{e(sp)}: {m(t)}</p>' for (sp, _), t in zip(P['lines'], md)) + '</div>'
    body += '<p class="ah">せりふごとの解説</p>' + ''.join(f'<p class="expl">{m(x)}</p>' for x in P['expl'])
    body += '<p class="ah">まちがえやすい点</p><ul class="tips">' + ''.join(f'<li>{m(t)}</li>' for t in P['tips']) + '</ul>'
    return page(body, 'flow')


def build(R, kind, ranges):
    if kind == 'q':
        parts = cover(R, 'q', ranges) + part_read(R, 'P1', '長文読解') + part_read(R, 'P2', '長文読解') + part_comp(R) + sheets(R) + colophon(R, 'q')
    else:
        parts = cover(R, 'a', ranges) + a_read(R, 'P1', '長文読解') + a_read(R, 'P2', '長文読解') + a_comp(R) + colophon(R, 'a')
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
    q = OUT / f'予想問題_{UNIV}_{T["name"]}_英語_第{n}回_問題.pdf'
    a = OUT / f'予想問題_{UNIV}_{T["name"]}_英語_第{n}回_解答解説.pdf'
    lab = f'{UNIV} {T["name"]} 第{n}回'
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
    for key in (['j1', 'j2', 'j3'] if arg == 'all' else sys.argv[1:]):
        render(key)
