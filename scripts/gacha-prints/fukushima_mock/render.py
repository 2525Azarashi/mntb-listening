# -*- coding: utf-8 -*-
"""福島大学 前期日程 英語（経済経営学類〔令和9年度から政経学部（仮称）〕の「英語・小論文から1科目」の英語）予想問題の PDF。白黒・A4縦。
紙面の部品・書体・白黒化は神戸大（../kobe_mock/render.py）と北大（../hokudai_mock/render.py）の部品を読み込んで流用する。
  python3 render.py 1   → .tmpwork/fukushima_mock/manatobi_fukushima_eng_yoso{1}_{mondai,kaitou}.pdf
データ：fN.py（N＝回）。DATA = {'points': {'1':100,'2':25,'3':25,'4':50}, '1': 長文, '2': 対話の空所, '3': 並べ替え, '4': 英作文, 'names': [...]}
  長文 = {'paras', 'notes', 'translation', 'questions', 'vocab'}。本文の {a|…}・{b|…} は記号つきの下線（和訳させる箇所）。
    設問の kind：jp（日本語で答える。answer, alts, criteria, explain）／trans（下線部の和訳。label, answer, alts, criteria, explain）。
  対話 = {'items': [{'lines': [(話者, 文)], 'answer', 'ja', 'explain'}]}。文中の ( ) が空所。
  並べ替え = {'items': [{'pre', 'words', 'post', 'answer', 'ja', 'explain'}]}。answer は words を正しい順に並べた文字列。
  英作文 = {'prompts': [2つ], 'limit', 'criteria', 'models': [(問い番号, 英文)], 'tips'}。
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
# 北大の render.py は自分のフォルダを sys.path の先頭に入れるので，福島のフォルダを先頭に戻す
sys.path.insert(0, str(HERE))
from weasyprint import HTML, CSS
e, mono, FC, crit_table = kb.e, kb.mono, kb.FC, kb.crit_table
OUT_DIR = Path(os.environ.get('FUKUSHIMA_OUT_DIR', str(ROOT / '.tmpwork/fukushima_mock')))
DISCLAIMER = '福島大学の過去問・公式問題ではありません。予想問題であり，大学とは関係がありません。'
ROMAN = {'1': 'Ⅰ', '2': 'Ⅱ', '3': 'Ⅲ', '4': 'Ⅳ'}
TITLES = {'1': '長文読解', '2': '対話文の空所補充', '3': '語句の並べかえ', '4': '自由英作文'}
INTRO = {
    '1': '以下の英文を読んで，あとの設問(1)〜(6)にすべて日本語で答えよ。',
    '2': '(1)〜(5)の各対話が自然な流れになるよう，空所(　　)に入る英単語をそれぞれ1語ずつ書け。',
    '3': '(1)〜(5)の(　　)内の語句を並べかえて，意味の通る英文を完成させよ。答えは(　　)内の語句だけを順に書くこと。',
    '4': '(1)・(2)のうち一方の問いを選んで，あなたの考えを英語100語程度で述べよ。選んだ問いの番号も解答用紙に書くこと。語数の数え方の例：I\'m fine. は2語。',
}
PAGE_INFO = {}

def em(s): return kb.em(s)
def mark(t):
    t = e(t)
    t = re.sub(r'\{([ab])\|([^}]*)\}', r'<span class="ul">\2</span><sub class="ulab">(\1)</sub>', t)
    return re.sub(r'(?<=[A-Za-z)])\*', '<sup class="ast">＊</sup>', t)
def plain(t):
    t = re.sub(r'\{[ab]\|([^}]*)\}', r'\1', t)
    return t.replace('*', '')
def filled(D):
    return ' '.join(plain(p) for p in D['1']['paras'])

H_CSS = hk.H_CSS + """
.passage p { text-indent: 1.2em; }
.ulab { font-size: 7pt; margin-left: .3mm; }
.notes { margin: 2mm 0 3mm; font-size: 9pt; display: grid; grid-template-columns: 1fr 1fr; gap: .4mm 6mm; }
.notes .en { font-family: 'Noto Serif'; font-style: italic; }
.fq { margin: 1.6mm 0 0; display: grid; grid-template-columns: 9mm 1fr; font-size: 10pt; break-inside: avoid; }
.dlg { margin: 2.4mm 0 0; font-family: 'Noto Serif'; font-size: 10pt; break-inside: avoid; display: grid; grid-template-columns: 9mm 1fr; }
.dlg .ln { display: grid; grid-template-columns: 6mm 1fr; }
.ordq { margin: 2.4mm 0 0; font-family: 'Noto Serif'; font-size: 10pt; display: grid; grid-template-columns: 9mm 1fr; break-inside: avoid; }
.prompt { margin: 2.4mm 0 0; font-family: 'Noto Serif'; font-size: 10.4pt; display: grid; grid-template-columns: 9mm 1fr; }
.ansgrid { border-collapse: collapse; margin: 1mm 0 2mm; }
.ansgrid td, .ansgrid th { border: .6pt solid #555; min-width: 24mm; height: 9mm; text-align: center; font-size: 8.8pt; padding: 0 1.5mm; }
.ansgrid th { height: 5.5mm; font-weight: 500; }
.selbox { border: .6pt solid #555; display: inline-block; padding: 1mm 4mm; margin: 1mm 0 2mm; font-size: 9pt; }
"""

def cover(R, kind, D):
    sub = '問題' if kind == 'q' else '解答・解説'
    rng = PAGE_INFO.get((R, kind), '')
    pts = '・'.join(f'{ROMAN[n]} {D["points"][n]}点' for n in ('1', '2', '3', '4')) + '（計200点）'
    if kind == 'q':
        items = [f'問題部分と解答用紙で構成されている{rng}。答えは解答用紙の決められた欄に書くこと。',
                 '試験時間の目安は70分。大問は Ⅰ〜Ⅳ の4題。',
                 'Ⅰは日本語で答える。Ⅱ・Ⅲは英語で答え，Ⅳは英語で書く。',
                 f'配点は {pts}。本予想問題が独自に定めた配点である。',
                 '本冊子の英文・設問はすべてオリジナルである。登場する人物・団体・地名は架空。']
    else:
        items = [f'解答一覧・設問ごとの解答と解説{rng}。',
                 'Ⅰは解答例・別解と採点基準，Ⅱ・Ⅲは正解の根拠と対話・英文の訳を示した。',
                 'Ⅳは採点基準と，2つの問いそれぞれの解答例を示した。',
                 'Ⅰの英文は全訳と重要語句つき。',
                 f'配点は {pts}。本予想問題が独自に定めた配点で，大学の配点ではない。']
    lis = ''.join(f'<li>{x}</li>' for x in items)
    return f"""<section class="ocover">
<div class="brand"><img src="file://{HERE}/logo_gray.png"><div class="kicker">学習アプリ マナトビ</div></div>
<div class="box">{R}</div>
<div class="l1">予想問題 第{R}回</div>
<div class="l2">前期日程 対策</div>
<h1>英語{'問題' if kind == 'q' else '解答'}</h1>
<div class="sub">福島大学（経済経営学類〔令和9年度から政経学部（仮称）〕 英語・小論文選択の「英語」）の出題形式に準拠 ／ {sub}</div>
<div class="chui"><span class="ttl">注　意</span><ol>{lis}</ol></div>
<div class="disc">{DISCLAIMER}<br>本冊子は過去の出題形式を分析して作成した練習用の教材です。</div>
<div class="foot"><span>学習アプリ マナトビ</span><span>予想問題 第{R}回 ／ {sub}</span></div></section>"""

def head(n, pts):
    return f'<div class="parthead" data-run="{ROMAN[n]}　{TITLES[n]}"><span class="roman">{ROMAN[n]}</span><span class="t">{TITLES[n]}（配点 {pts}点）</span></div>'

def intro(n): return f'<p class="intro">{e(INTRO[n])}</p>'

def part1(P, pts):
    out = f'<section class="part">{head("1", pts)}{intro("1")}<div class="passage">'
    out += ''.join(f'<p>{mark(p)}</p>' for p in P['paras']) + '</div>'
    out += '<div style="font-size:9pt;margin-top:2mm">［注］</div><div class="notes">' + ''.join(f'<div><span class="en">{e(a)}</span>：{e(b)}</div>' for a, b in P['notes']) + '</div>'
    out += '<div style="margin-top:2mm">［設問］</div>'
    out += ''.join(f'<div class="fq"><span>({i})</span><span>{e(q["stem"])}</span></div>' for i, q in enumerate(P['questions'], 1))
    return out + '</section>'

def dlg_html(it, i, blank='(　　　　)'):
    lines = ''.join(f'<div class="ln"><span>{e(s)}:</span><span>{e(t).replace("( )", blank)}</span></div>' for s, t in it['lines'])
    return f'<div class="dlg"><span>({i})</span><div>{lines}</div></div>'

def part2(P, pts):
    return f'<section class="part">{head("2", pts)}{intro("2")}' + ''.join(dlg_html(it, i) for i, it in enumerate(P['items'], 1)) + '</section>'

def ord_html(it, i):
    post = it['post'] if re.fullmatch(r'[.?!]', it['post']) else ' ' + it['post']
    return f'<div class="ordq"><span>({i})</span><span>{e(it["pre"])} ({e(", ".join(sorted(it["words"], key=str.lower)))}){e(post)}</span></div>'

def part3(P, pts):
    return f'<section class="part">{head("3", pts)}{intro("3")}' + ''.join(ord_html(it, i) for i, it in enumerate(P['items'], 1)) + '</section>'

def part4(P, pts):
    return f'<section class="part">{head("4", pts)}{intro("4")}' + ''.join(f'<div class="prompt"><span>({i})</span><span>{e(p)}</span></div>' for i, p in enumerate(P['prompts'], 1)) + '</section>'

def grid(labels):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels); td = ''.join('<td></td>' for _ in labels)
    return f'<table class="ansgrid"><tr>{th}</tr><tr>{td}</tr></table>'

def sheet(D, R):
    H4 = '<h4 style="font-family:MPR;font-weight:800;margin:3mm 0 1mm">{}</h4>'
    out = f'<section class="sheet"><h2>解答用紙　予想問題 第{R}回</h2><div style="font-size:8.6pt;margin-bottom:2mm">受験番号・氏名欄は省略。</div>'
    out += H4.format('Ⅰ')
    for i, q in enumerate(D['1']['questions'], 1):
        out += f'<div>({i}){"　下線部(" + q["label"] + ")" if q["kind"] == "trans" else ""}</div>' + hk.wlines(4 if q['kind'] == 'trans' else 3, False)
    out += H4.format('Ⅱ') + grid([f'({i})' for i in range(1, 6)])
    out += H4.format('Ⅲ（(　　)内の語句だけを書く）')
    for i in range(1, 6): out += f'<div class="row lines"><span class="h">({i})</span><span></span></div>'
    out += H4.format('Ⅳ（100語程度）') + '<div class="selbox">選んだ問いの番号：（　　　）</div>' + hk.wlines(14)
    return out + '</section>'

def colophon(R, kind):
    return f"""<section class="colophon"><div class="box"><h2>奥付</h2>
<div>予想問題 第{R}回　英語　{'問題' if kind == 'q' else '解答・解説'}</div>
<div>対象：福島大学 前期日程 英語（経済経営学類〔令和9年度から政経学部（仮称）〕の英語・小論文選択の英語）の受験準備</div>
<div>作成：学習アプリ マナトビ 編集部（2026年11月）</div>
<div>作成方法：2024〜2026年度の出題形式・分量・難易度を分析し，英文・設問をすべて新たに書き下ろした。</div>
<div class="disc">{DISCLAIMER}</div>
<div style="margin-top:2.5mm;font-size:8.4pt">本冊子の英文は実在の記事・書籍・論文・統計からの引用・翻案ではありません。登場する人物・団体・地名・数値は架空です。無断転載・再配布を禁じます。</div>
<img src="file://{HERE}/logo_gray.png"></div></section>"""

# ---------------------------------------------------------------- 解答・解説
def box(inner): return f'<div class="abox">{inner}</div>'
def ul(items): return '<ul>' + ''.join(f'<li>{em(x)}</li>' for x in items) + '</ul>'
def wc(m): return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'-]*", m))

def akey1(P, pts):
    out = f'<section class="part akey"><h3>Ⅰ　解答・解説（{pts}点）</h3>'
    for i, q in enumerate(P['questions'], 1):
        t = f'<h4>({i})（{q["points"]}点）</h4>'
        b = f'<div style="font-size:8.8pt;margin:.6mm 0">設問：{e(q["stem"])}</div><div><span class="lbl">解答例</span><span class="ans">{e(q["answer"])}</span></div>'
        for a in q.get('alts', []): b += f'<div style="margin-top:.8mm"><span class="lbl">別解</span><span class="x-ul">{e(a)}</span></div>'
        out += t + box(b + crit_table(q['criteria']) + ul(q['explain']))
    out += '<h4>全訳</h4><div class="trs">' + ''.join(f'<p>{e(t)}</p>' for t in P['translation']) + '</div>'
    out += '<h4>重要語句</h4><table class="voc">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in P['vocab']) + '</table>'
    return out + '</section>'

def akey2(P, pts):
    out = f'<section class="part akey"><h3>Ⅱ　解答・解説（{pts}点・各{pts // 5}点）</h3>'
    for i, it in enumerate(P['items'], 1):
        out += dlg_html(it, i, f'( <b>{e(it["answer"])}</b> )') + box(f'<div class="ans">正解　<span class="en">{e(it["answer"])}</span></div><div style="font-size:8.8pt;margin:.6mm 0">訳：{e(it["ja"])}</div>' + ul(it['explain']))
    return out + '</section>'

def akey3(P, pts):
    out = f'<section class="part akey"><h3>Ⅲ　解答・解説（{pts}点・各{pts // 5}点）</h3>'
    for i, it in enumerate(P['items'], 1):
        full = f'{it["pre"]} {it["answer"]} {it["post"]}'.replace(' ,', ',').replace(' .', '.').replace(' ?', '?').strip()
        out += f'<h4>({i})</h4>' + box(f'<div class="ans">正解　<span class="en">{e(it["answer"])}</span></div><div class="en" style="margin:.6mm 0">{e(full)}</div><div style="font-size:8.8pt">訳：{e(it["ja"])}</div>' + ul(it['explain']))
    return out + '</section>'

def akey4(P, pts):
    out = f'<section class="part akey"><h3>Ⅳ　解答・解説（{pts}点）</h3>'
    out += box('<div style="font-size:8.8pt;margin-bottom:1mm">問いの訳：' + '／'.join(f'({i}) {e(j)}' for i, j in enumerate(P['prompts_ja'], 1)) + '</div>' + crit_table(P['criteria']))
    for k, m in P['models']:
        out += f'<h4>解答例：({k + 1}) を選んだ場合</h4>' + box(f'<div class="model">{e(m)} <span class="wc">（{wc(m)}語）</span></div><div style="font-size:8.6pt;margin-top:1mm">訳：{e(P["models_ja"][k])}</div>')
    out += '<h4>書き方のポイント・減点されやすい点</h4>' + box(ul(P['tips']))
    return out + '</section>'

def summary_table(D, R):
    rows = ''
    for i, q in enumerate(D['1']['questions'], 1):
        rows += f'<tr><td>Ⅰ</td><td>({i})</td><td>{"下線部(" + q["label"] + ")の和訳" if q["kind"] == "trans" else "日本語で説明"}：解答例は解説参照（採点基準つき）</td><td>{q["points"]}</td></tr>'
    for n in ('2', '3'):
        for i, it in enumerate(D[n]['items'], 1):
            rows += f'<tr><td>{ROMAN[n]}</td><td>({i})</td><td><span class="en">{e(it["answer"])}</span></td><td>{D["points"][n] // 5}</td></tr>'
    rows += f'<tr><td>Ⅳ</td><td>—</td><td>自由英作文：採点基準と解答例は解説参照</td><td>{D["points"]["4"]}</td></tr>'
    return f'<section class="part akey"><h3>解答一覧　予想問題 第{R}回</h3><table class="sum"><tr><th>大問</th><th>設問</th><th>解答</th><th>配点</th></tr>{rows}<tr><td colspan="3" style="text-align:right">合計</td><td>200</td></tr></table></section>'

def check_points(D):
    assert sum(D['points'].values()) == 200
    assert sum(q['points'] for q in D['1']['questions']) == D['points']['1']
    for q in D['1']['questions']: assert sum(p for _, p in q['criteria']) == q['points'], q['stem']
    assert sum(p for _, p in D['4']['criteria']) == D['points']['4']
    assert len(D['2']['items']) == 5 and len(D['3']['items']) == 5 and D['points']['2'] % 5 == 0 and D['points']['3'] % 5 == 0

def write(doc, out):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    css = [CSS(string=mono(kb.CSS_TEXT + H_CSS), font_config=FC)]
    HTML(string=mono(doc), base_url=str(HERE)).write_pdf(out, stylesheets=css, font_config=FC, metadata={'author': 'マナトビ'})
    return out

def load(R): return importlib.import_module(f'f{R}').DATA

def build_q(R):
    D = load(R); check_points(D); p = D['points']
    body = cover(R, 'q', D) + part1(D['1'], p['1']) + part2(D['2'], p['2']) + part3(D['3'], p['3']) + part4(D['4'], p['4']) + sheet(D, R) + colophon(R, 'q')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 問題</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_fukushima_eng_yoso{R}_mondai.pdf')

def build_a(R):
    D = load(R); check_points(D); p = D['points']
    body = cover(R, 'a', D) + summary_table(D, R) + akey1(D['1'], p['1']) + akey2(D['2'], p['2']) + akey3(D['3'], p['3']) + akey4(D['4'], p['4']) + colophon(R, 'a')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 解答・解説</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_fukushima_eng_yoso{R}_kaitou.pdf')

if __name__ == '__main__':
    R = sys.argv[1] if len(sys.argv) > 1 else '1'
    for kind, f in (('q', build_q), ('a', build_a)):
        o = f(R); PAGE_INFO[(R, kind)] = hk.page_range(o, kind)
        o = f(R); print(o.name, o.stat().st_size // 1024, 'KB', PAGE_INFO[(R, kind)])
