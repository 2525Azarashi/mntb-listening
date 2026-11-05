# -*- coding: utf-8 -*-
"""群馬大学 前期日程 英語（理工学部・医学部保健学科 共通の問題冊子）予想問題の PDF。白黒・A4縦。
紙面の部品・書体・白黒化は神戸大（../kobe_mock/render.py）と北大（../hokudai_mock/render.py）の部品を読み込んで流用する。
  python3 render.py 1   → .tmpwork/gunma_mock/manatobi_gunma_eng_yoso{1}_{mondai,kaitou}.pdf
データ：gN.py（N＝回）。DATA = {'points': {'1': 90, '2': 50, '3': 60}, 'A', 'B', 'C', '2A', '2B', '3A', '3B', 'names'}
  解答番号は通し番号：1A 1〜10・1B 11〜20・1C 21〜30・2A 31〜35・2B 36〜40・3A 41〜50・3B 51〜60。
  A（語句の選択）= [{'stem': '… [[]] …', 'choices': [4], 'answer': 0〜3, 'ja': 完成文の訳, 'explain': [...]}] × 10
  B（誤りの指摘）= [{'sent': '… {1|…} … {2|…} … {3|…} … {4|…} …', 'answer': 1〜4, 'correct': 正しい形, 'ja', 'explain'}] × 10
  C（会話の完成）= [{'title': 場面（日本語）, 'lines': [(話者, 英文。空所は [[1]] [[2]] …)], 'choices': [4], 'answers': [空所ごとの正解], 'ja': [訳], 'explain': [空所ごと＋使わない選択肢]}] × 4（空所は計10）
  2A・2B（読解）= {'paras', 'notes': [(語, 意味)], 'questions': [{'q', 'choices', 'answer', 'explain'}] × 5（最後は表題）, 'translation', 'vocab'}
  3A・3B（語の完成）= {'title', 'paras'（空所は {{書き出し|残り}}）, 'alts': {空所番号: [別解]}, 'explain': [空所ごと], 'translation'}
"""
import sys, re, os, importlib, importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, HERE.parent / rel)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
kb = _load('kb', 'kobe_mock/render.py')
hk = _load('hk', 'hokudai_mock/render.py')
sys.path.insert(0, str(HERE))
from weasyprint import HTML, CSS
e, mono, FC = kb.e, kb.mono, kb.FC
OUT_DIR = Path(os.environ.get('GUNMA_OUT_DIR', str(ROOT / '.tmpwork/gunma_mock')))
DISCLAIMER = '群馬大学の過去問・公式問題ではありません。予想問題であり，大学とは関係がありません。'
CN = '①②③④'
NO = {'A': 1, 'B': 11, 'C': 21, '2A': 31, '2B': 36, '3A': 41, '3B': 51}
INTRO = {
    'A': '次の各文の空所 {a} 〜 {b} を補うのに最もふさわしい語句を，それぞれ①〜④から一つ選べ。',
    'B': '次の各文には，英語として正しくない箇所が一つずつある。直すべき箇所を下線部①〜④から一つ選べ（解答番号 {a} 〜 {b} ）。',
    'C': '次の四つの会話を読み，空所 {a} 〜 {b} に入れるのに最もふさわしい文を，会話ごとに示した①〜④から一つずつ選べ。選択肢には使わないものも含まれている。',
    '2': '次の英文を読み，問1〜問5（解答番号 {a} 〜 {b} ）に対する答えとして最も適当なものを，それぞれ①〜④から一つ選べ。',
    '3': '次の二つの英文（A・B）には，語の書き出しの文字だけが示された空所が10か所ずつある（解答番号 41 〜 60 ）。文意が通るように，示された文字で始まる英単語を1語ずつ書いて，単語を完成させよ。',
}
EXAMPLE = ('We ate lunch together in the school caf', 'eteria', ' at noon.')
PAGE_INFO = {}

def nbox(n): return f'<span class="nbox">{n}</span>'
def a_stem(s, n): return e(s).replace('[[]]', nbox(n))
def b_sent(s, n):
    t = e(s)
    t = re.sub(r'\{(\d)\|([^}]*)\}', lambda m: f'<span class="bseg"><span class="ul">{m.group(2)}</span><span class="bn">{CN[int(m.group(1)) - 1]}</span></span>', t)
    return t + ' ' + nbox(n)
def b_fixed(q):
    return re.sub(r'\{(\d)\|([^}]*)\}', lambda m: q['correct'] if int(m.group(1)) == q['answer'] else m.group(2), q['sent'])
def b_plain(s): return re.sub(r'\{\d\|([^}]*)\}', r'\1', s)
def c_line(t, base, fill=None):
    def rep(m):
        k = int(m.group(1)) - 1
        return f'<span class="x-ul">{e(fill[k])}</span>' if fill else nbox(base + k)
    return re.sub(r'\[\[(\d)\]\]', rep, e(t))
def mark(t): return re.sub(r'(?<=[A-Za-z)])\*', '<sup class="ast">＊</sup>', e(t))
def plain(t):
    t = re.sub(r'\{\{([^|}]*)\|([^}]*)\}\}', r'\1\2', t)
    t = re.sub(r'\{\d\|([^}]*)\}', r'\1', t)
    return t.replace('[[]]', ' ').replace('*', '')
def gaps(P): return re.findall(r'\{\{([^|}]*)\|([^}]*)\}\}', ' '.join(P['paras']))
def g_para(t, base, cnt, fill=False):
    out = []
    pos = 0
    for m in re.finditer(r'\{\{([^|}]*)\|([^}]*)\}\}', t):
        out.append(e(t[pos:m.start()]))
        n = base + cnt[0]; cnt[0] += 1
        out.append(f'{e(m.group(1))}<b class="x-ul">{e(m.group(2))}</b><sub class="gn">{n}</sub>' if fill else f'{e(m.group(1))}<span class="gbox">{n}</span>')
        pos = m.end()
    out.append(e(t[pos:]))
    return re.sub(r'(?<=[A-Za-z)])\*', '<sup class="ast">＊</sup>', ''.join(out))

H_CSS = hk.H_CSS + """
.nbox { display: inline-block; border: .7pt solid #000; min-width: 15mm; text-align: center; font-family: 'Noto Sans CJK JP'; font-size: 8.4pt; line-height: 1.35; margin: 0 1mm; vertical-align: 1pt; }
.gbox { display: inline-block; border: .7pt solid #000; min-width: 13mm; text-align: center; font-family: 'Noto Sans CJK JP'; font-size: 7.8pt; line-height: 1.3; margin-left: .5mm; vertical-align: 1pt; }
.gn { font-size: 6.5pt; margin-left: .3mm; }
.gi { margin: 4mm 0 0; break-inside: avoid; font-size: 10pt; }
.gi .stem { display: grid; grid-template-columns: 12mm 1fr; font-family: 'Noto Serif'; line-height: 1.9; }
.gi .stem .n { font-family: 'Noto Serif CJK JP'; }
.gi .chs { margin-left: 12mm; font-family: 'Noto Serif'; display: grid; grid-template-columns: 1fr 1fr; gap: .2mm 6mm; }
.gi .chs.one { grid-template-columns: 1fr; }
.bseg { display: inline-block; text-align: center; line-height: 1.15; vertical-align: top; }
.bseg .bn { display: block; font-size: 7.2pt; font-family: 'Noto Sans CJK JP'; }
.gi.b .stem { line-height: 2.3; }
.dlg { margin: 4mm 0 0; font-family: 'Noto Serif'; font-size: 10pt; break-inside: avoid; }
.dlg .tt { font-family: 'Noto Serif CJK JP'; font-weight: 700; margin-bottom: 1mm; }
.dlg .ln { display: grid; grid-template-columns: 8mm 1fr; margin: .5mm 0 .5mm 4mm; line-height: 1.8; }
.dlg .chs { margin: 1.5mm 0 0 8mm; }
.passage p { text-indent: 1.4em; }
.ptitle { font-family: 'Noto Serif'; font-weight: 700; font-size: 11pt; text-align: center; margin: 1mm 0 2.4mm; }
.gnotes { margin: 2mm 0 3mm; font-size: 9pt; display: grid; grid-template-columns: 1fr 1fr; gap: .4mm 6mm; }
.gnotes .en { font-family: 'Noto Serif'; font-style: italic; }
.exbox { border: .6pt solid #777; padding: 1.5mm 4mm; margin: 1mm 0 3mm; font-size: 9.4pt; }
.exbox .en { font-family: 'Noto Serif'; }
.subhead { font-family: 'Noto Sans CJK JP'; font-weight: 700; font-size: 10.2pt; margin: 4mm 0 1mm; }
.mk { border-collapse: collapse; margin: 1mm 0 3mm; font-size: 8.6pt; }
.mk td, .mk th { border: .6pt solid #555; padding: .6mm 2.4mm; text-align: center; }
.mk th { font-weight: 500; }
.mkwrap { display: flex; gap: 5mm; flex-wrap: wrap; }
.wbox td { width: 30mm; height: 7mm; }
.sum3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3mm; }
.sum3 table { border-collapse: collapse; width: 100%; font-size: 8.6pt; }
.sum3 td, .sum3 th { border: .5pt solid #777; padding: .5mm 1.5mm; text-align: center; }
.akline { margin: 2.6mm 0 0; break-inside: avoid; }
.akline .hd { font-family: 'Noto Sans CJK JP'; font-weight: 700; }
.akline .en { font-family: 'Noto Serif'; }
.akline ul { margin: .5mm 0 0; padding-left: 4.5mm; }
"""

def cover(R, kind, D):
    sub = '問題' if kind == 'q' else '解答・解説'
    rng = PAGE_INFO.get((R, kind), '')
    pts = f'第1問 {D["points"]["1"]}点・第2問 {D["points"]["2"]}点・第3問 {D["points"]["3"]}点（計200点）'
    if kind == 'q':
        items = [f'問題部分と解答用紙で構成されている{rng}。答えは解答用紙の決められた欄に書くこと。',
                 '解答番号は 1 〜 60 の通し番号。1〜40 は選択肢の番号を〇で囲み，41〜60 は英単語を書く。',
                 '試験時間の目安は60分（本予想問題の想定）。大問は第1問〜第3問の3題。',
                 f'配点は {pts}。本予想問題が独自に定めた配点である。',
                 '本冊子の英文・設問はすべてオリジナルである。登場する人物・団体・地名は架空。']
    else:
        items = [f'解答一覧・設問ごとの解答と解説{rng}。',
                 '選択問題は，正解の根拠と，ほかの選択肢が当てはまらない理由を示した。',
                 '第1問の各文と会話には訳を，第2問・第3問の英文には全訳をつけた。',
                 '第3問は完成した英文と，認められる別の綴り・語形を示した。',
                 f'配点は {pts}。本予想問題が独自に定めた配点で，大学の配点ではない。']
    lis = ''.join(f'<li>{x}</li>' for x in items)
    return f"""<section class="ocover">
<div class="brand"><img src="file://{HERE}/logo_gray.png"><div class="kicker">学習アプリ マナトビ</div></div>
<div class="box">{R}</div>
<div class="l1">予想問題 第{R}回</div>
<div class="l2">前期日程 対策</div>
<h1>英語{'問題' if kind == 'q' else '解答'}</h1>
<div class="sub">群馬大学（理工学部・医学部保健学科 共通の問題冊子）の出題形式に準拠 ／ {sub}</div>
<div class="chui"><span class="ttl">注　意</span><ol>{lis}</ol></div>
<div class="disc">{DISCLAIMER}<br>本冊子は過去の出題形式を分析して作成した練習用の教材です。</div>
<div class="foot"><span>学習アプリ マナトビ</span><span>予想問題 第{R}回 ／ {sub}</span></div></section>"""

def head(n, title, pts):
    return f'<div class="parthead" data-run="第{n}問　{title}"><span class="roman">{n}</span><span class="t">第{n}問　{title}（配点 {pts}点）</span></div>'

def chs(choices, one=False):
    one = one or max(len(c) for c in choices) > 26
    return f'<div class="chs{" one" if one else ""}">' + ''.join(f'<div>{CN[i]} {e(c)}</div>' for i, c in enumerate(choices)) + '</div>'

def part1(D):
    out = f'<section class="part">{head(1, "文法・語法・会話表現", D["points"]["1"])}'
    out += f'<div class="subhead">A</div><p class="intro">{INTRO["A"].format(a=1, b=10)}</p>'
    for i, q in enumerate(D['A']):
        out += f'<div class="gi"><div class="stem"><span class="n">問{i + 1}</span><span>{a_stem(q["stem"], NO["A"] + i)}</span></div>{chs(q["choices"])}</div>'
    out += f'<div class="subhead" style="break-before:page">B</div><p class="intro">{INTRO["B"].format(a=11, b=20)}</p>'
    for i, q in enumerate(D['B']):
        out += f'<div class="gi b"><div class="stem"><span class="n">問{i + 1}</span><span>{b_sent(q["sent"], NO["B"] + i)}</span></div></div>'
    out += f'<div class="subhead" style="break-before:page">C</div><p class="intro">{INTRO["C"].format(a=21, b=30)}</p>'
    base = NO['C']
    for i, c in enumerate(D['C']):
        out += f'<div class="dlg"><div class="tt">問{i + 1}：{e(c["title"])}</div>'
        out += ''.join(f'<div class="ln"><span>{e(s)}：</span><span>{c_line(t, base)}</span></div>' for s, t in c['lines'])
        out += chs(c['choices'], True) + '</div>'
        base += len(c['answers'])
    return out + '</section>'

def part2(D):
    out = f'<section class="part">{head(2, "長文読解", D["points"]["2"])}'
    for k in ('2A', '2B'):
        P = D[k]
        style = ' style="break-before:page"' if k == '2B' else ''
        out += f'<div class="subhead"{style}>{k[1]}</div><p class="intro">{INTRO["2"].format(a=NO[k], b=NO[k] + 4)}</p>'
        out += '<div class="passage">' + ''.join(f'<p>{mark(p)}</p>' for p in P['paras']) + '</div>'
        out += '<div style="font-size:9pt;margin-top:2mm">〔注〕</div><div class="gnotes">' + ''.join(f'<div><span class="en">{e(a)}</span>：{e(b)}</div>' for a, b in P['notes']) + '</div>'
        for i, q in enumerate(P['questions']):
            out += f'<div class="gi"><div class="stem"><span class="n">問{i + 1}</span><span>{e(q["q"])} {nbox(NO[k] + i)}</span></div>{chs(q["choices"], True)}</div>'
    return out + '</section>'

def part3(D):
    out = f'<section class="part">{head(3, "語の完成", D["points"]["3"])}<p class="intro">{INTRO["3"]}</p>'
    a, g, b = EXAMPLE
    out += f'<div class="exbox">（例）<span class="en">{e(a)}<span class="gbox">例</span>{e(b)}</span>　→　答：<span class="en">{e(a.split()[-1] + g)}</span></div>'
    for k in ('3A', '3B'):
        P = D[k]; cnt = [0]
        style = ' style="break-before:page"' if k == '3B' else ''
        out += f'<div class="subhead"{style}>{k[1]}</div><div class="ptitle">{e(P["title"])}</div>'
        out += '<div class="passage">' + ''.join(f'<p>{g_para(p, NO[k], cnt)}</p>' for p in P['paras']) + '</div>'
        if P.get('notes'):
            out += '<div style="font-size:9pt;margin-top:2mm">〔注〕</div><div class="gnotes">' + ''.join(f'<div><span class="en">{e(x)}</span>：{e(y)}</div>' for x, y in P['notes']) + '</div>'
    return out + '</section>'

def sheet(D, R):
    out = f'<section class="sheet"><h2>解答用紙　予想問題 第{R}回</h2><div style="font-size:8.6pt;margin-bottom:2mm">受験番号・氏名欄は省略。1〜40 は番号を〇で囲み，41〜60 は英単語を書く。</div>'
    def mk(a, b):
        rows = ''.join(f'<tr><th>{n}</th>' + ''.join(f'<td>{c}</td>' for c in CN) + '</tr>' for n in range(a, b + 1))
        return f'<table class="mk"><tr><th>解答番号</th><th colspan="4">解答欄</th></tr>{rows}</table>'
    out += '<div class="subhead">第1問</div><div class="mkwrap">' + mk(1, 10) + mk(11, 20) + mk(21, 30) + '</div>'
    out += '<div class="subhead">第2問</div><div class="mkwrap">' + mk(31, 35) + mk(36, 40) + '</div>'
    def wb(a, b):
        rows = ''.join(f'<tr><th>{n}</th><td></td></tr>' for n in range(a, b + 1))
        return f'<table class="mk wbox"><tr><th>解答番号</th><th>単語（全体を書く）</th></tr>{rows}</table>'
    out += '<div class="subhead">第3問</div><div class="mkwrap">' + wb(41, 50) + wb(51, 60) + '</div>'
    return out + '</section>'

def colophon(R, kind):
    return f"""<section class="colophon"><div class="box"><h2>奥付</h2>
<div>予想問題 第{R}回　英語　{'問題' if kind == 'q' else '解答・解説'}</div>
<div>対象：群馬大学 前期日程 英語（理工学部・医学部保健学科 共通の問題冊子）の受験準備</div>
<div>作成：学習アプリ マナトビ 編集部（2026年11月）</div>
<div>作成方法：2024〜2026年度の出題形式・分量・難易度を分析し，英文・設問をすべて新たに書き下ろした。</div>
<div class="disc">{DISCLAIMER}</div>
<div style="margin-top:2.5mm;font-size:8.4pt">本冊子の英文は実在の記事・書籍・論文・統計からの引用・翻案ではありません。登場する人物・団体・地名・数値は架空です。無断転載・再配布を禁じます。</div>
<img src="file://{HERE}/logo_gray.png"></div></section>"""

# ---------------------------------------------------------------- 解答・解説
def ul(items): return '<ul>' + ''.join(f'<li>{kb.em(x)}</li>' for x in items) + '</ul>'
def answers(D):
    out = []
    for q in D['A']: out.append(CN[q['answer']])
    for q in D['B']: out.append(CN[q['answer'] - 1])
    for c in D['C']: out += [CN[a] for a in c['answers']]
    for k in ('2A', '2B'): out += [CN[q['answer']] for q in D[k]['questions']]
    for k in ('3A', '3B'): out += [a + b for a, b in gaps(D[k])]
    return out

def pts_of(D, n):
    if n <= 30: return D['points']['1'] // 30
    if n <= 40: return D['points']['2'] // 10
    return D['points']['3'] // 20

def summary(D, R):
    A = answers(D)
    def tb(a, b):
        rows = ''.join(f'<tr><td>{n}</td><td class="en">{e(A[n - 1])}</td><td>{pts_of(D, n)}</td></tr>' for n in range(a, b + 1))
        return f'<table><tr><th>番号</th><th>正解</th><th>配点</th></tr>{rows}</table>'
    return (f'<section class="part akey"><h3>解答一覧　予想問題 第{R}回（200点）</h3>'
            f'<div class="sum3">{tb(1, 20)}{tb(21, 40)}{tb(41, 60)}</div>'
            f'<div style="font-size:8.6pt;margin-top:2mm">配点：第1問 各{pts_of(D, 1)}点×30・第2問 各{pts_of(D, 31)}点×10・第3問 各{pts_of(D, 41)}点×20。第3問の別解は解説を参照。</div></section>')

def akey1(D):
    out = f'<section class="part akey"><h3>第1問　解答・解説（{D["points"]["1"]}点）</h3><h4>A</h4>'
    for i, q in enumerate(D['A']):
        n = NO['A'] + i
        out += (f'<div class="akline"><span class="hd">{n}　正解 {CN[q["answer"]]}</span>　<span class="en">{e(q["stem"].replace("[[]]", q["choices"][q["answer"]]))}</span>'
                f'<div style="font-size:9pt">訳：{e(q["ja"])}</div>{ul(q["explain"])}</div>')
    out += '<h4>B</h4>'
    for i, q in enumerate(D['B']):
        n = NO['B'] + i
        wrong = re.findall(r'\{(\d)\|([^}]*)\}', q['sent'])[q['answer'] - 1][1]
        out += (f'<div class="akline"><span class="hd">{n}　正解 {CN[q["answer"] - 1]}</span>　（誤）<span class="en">{e(wrong)}</span> → （正）<span class="en x-ul">{e(q["correct"])}</span>'
                f'<div class="en" style="font-size:9.2pt">{e(b_fixed(q))}</div><div style="font-size:9pt">訳：{e(q["ja"])}</div>{ul(q["explain"])}</div>')
    out += '<h4>C</h4>'
    base = NO['C']
    for i, c in enumerate(D['C']):
        nums = '・'.join(f'{base + k}：{CN[a]}' for k, a in enumerate(c['answers']))
        fills = [c['choices'][a] for a in c['answers']]
        out += f'<div class="akline"><span class="hd">問{i + 1}（{e(c["title"])}）　{nums}</span>'
        out += '<div class="dlg" style="margin-top:1mm">' + ''.join(f'<div class="ln"><span>{e(s)}：</span><span>{c_line(t, base, fills)}</span></div>' for s, t in c['lines']) + '</div>'
        out += '<div style="font-size:9pt">訳：' + '　'.join(e(x) for x in c['ja']) + '</div>' + ul(c['explain']) + '</div>'
        base += len(c['answers'])
    return out + '</section>'

def akey2(D):
    out = f'<section class="part akey"><h3>第2問　解答・解説（{D["points"]["2"]}点）</h3>'
    for k in ('2A', '2B'):
        P = D[k]; out += f'<h4>{k[1]}</h4>'
        for i, q in enumerate(P['questions']):
            out += (f'<div class="akline"><span class="hd">{NO[k] + i}　正解 {CN[q["answer"]]}</span>　<span class="en">{e(q["choices"][q["answer"]])}</span>'
                    f'<div style="font-size:9pt">問い：<span class="en">{e(q["q"])}</span>（{e(q["q_ja"])}）</div>{ul(q["explain"])}</div>')
        out += f'<h4>{k[1]} の全訳</h4><div class="trs">' + ''.join(f'<p>{e(t)}</p>' for t in P['translation']) + '</div>'
        out += f'<h4>{k[1]} の重要語句</h4><table class="voc">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in P['vocab']) + '</table>'
    return out + '</section>'

def akey3(D):
    out = f'<section class="part akey"><h3>第3問　解答・解説（{D["points"]["3"]}点）</h3>'
    for k in ('3A', '3B'):
        P = D[k]; cnt = [0]
        out += f'<h4>{k[1]}　{e(P["title"])}（完成した英文）</h4><div class="passage" style="font-size:9.8pt">' + ''.join(f'<p>{g_para(p, NO[k], cnt, True)}</p>' for p in P['paras']) + '</div>'
        out += '<h4>解答と解説</h4>'
        for j, ((a, b), ex) in enumerate(zip(gaps(P), P['explain'])):
            n = NO[k] + j
            alt = P.get('alts', {}).get(n, [])
            out += f'<div class="akline"><span class="hd">{n}　</span><span class="en"><b>{e(a + b)}</b></span>' + (f'　（別解：<span class="en">{e(" / ".join(alt))}</span>）' if alt else '') + f'　{kb.em(ex)}</div>'
        out += f'<h4>{k[1]} の全訳</h4><div class="trs">' + ''.join(f'<p>{e(t)}</p>' for t in P['translation']) + '</div>'
    return out + '</section>'

def check_points(D):
    p = D['points']; assert sum(p.values()) == 200 and p['1'] % 30 == 0 and p['2'] % 10 == 0 and p['3'] % 20 == 0
    assert len(D['A']) == 10 and len(D['B']) == 10 and sum(len(c['answers']) for c in D['C']) == 10
    for k in ('2A', '2B'): assert len(D[k]['questions']) == 5
    for k in ('3A', '3B'): assert len(gaps(D[k])) == 10 and len(D[k]['explain']) == 10, k

def write(doc, out):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    css = [CSS(string=mono(kb.CSS_TEXT + H_CSS), font_config=FC)]
    HTML(string=mono(doc), base_url=str(HERE)).write_pdf(out, stylesheets=css, font_config=FC, metadata={'author': 'マナトビ'})
    return out

def load(R): return importlib.import_module(f'g{R}').DATA

def build_q(R):
    D = load(R); check_points(D)
    body = cover(R, 'q', D) + part1(D) + part2(D) + part3(D) + sheet(D, R) + colophon(R, 'q')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 問題</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_gunma_eng_yoso{R}_mondai.pdf')

def build_a(R):
    D = load(R); check_points(D)
    body = cover(R, 'a', D) + summary(D, R) + akey1(D) + akey2(D) + akey3(D) + colophon(R, 'a')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 解答・解説</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_gunma_eng_yoso{R}_kaitou.pdf')

if __name__ == '__main__':
    R = sys.argv[1] if len(sys.argv) > 1 else '1'
    for kind, f in (('q', build_q), ('a', build_a)):
        o = f(R); PAGE_INFO[(R, kind)] = hk.page_range(o, kind)
        o = f(R); print(o.name, o.stat().st_size // 1024, 'KB', PAGE_INFO[(R, kind)])
