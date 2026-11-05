# -*- coding: utf-8 -*-
"""宇都宮大学 前期日程 英語（データサイエンス経営学部・国際学部・工学部・農学部の共通問題冊子）予想問題の PDF。白黒・A4縦。
紙面の部品・書体・白黒化は神戸大（../kobe_mock/render.py）と北大（../hokudai_mock/render.py）の部品を読み込んで流用する。
  python3 render.py 1   → .tmpwork/utsunomiya_mock/manatobi_utsunomiya_eng_yoso{1}_{mondai,kaitou}.pdf
データ：uN.py（N＝回）。DATA = {'points': {'1':60,'2':60,'3':40,'4':40}, '1': 論説文, '2': 物語文, '3': 意見英作文, '4': 会話文, 'names': [...]}
  長文 = {'title', 'paras', 'notes', 'translation', 'questions', 'vocab'}。
    本文の記法：{n|…} 番号つきの下線（下線部(n)）・[[n]] 番号つきの空所（空所(n)）・word* 注のある語。
    設問の kind：mc（記号選択。choices, answer）／tf（〇×。statements, answers）／trans（下線部の和訳。target, answer, alts, criteria）／
      jp（日本語で説明。answer, alts, criteria, lo/hi は字数指定があるときだけ）。どれも points と explain（リスト）を持つ。
  意見英作文 = {'passage', 'passage_ja', 'question', 'question_ja', 'criteria', 'models': [(立場, 英文)], 'models_ja', 'tips'}。
  会話文 = {'convs': [{'label', 'setting', 'lines': [(話者, 文 or None)], 'answers': [例], 'explain': [...], 'ja': [...]}]}。None が空所。
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
# 北大の render.py は自分のフォルダを sys.path の先頭に入れるので，宇都宮のフォルダを先頭に戻す
sys.path.insert(0, str(HERE))
from weasyprint import HTML, CSS
e, mono, FC, crit_table, genko = kb.e, kb.mono, kb.FC, kb.crit_table, kb.genko
OUT_DIR = Path(os.environ.get('UTSUNOMIYA_OUT_DIR', str(ROOT / '.tmpwork/utsunomiya_mock')))
DISCLAIMER = '宇都宮大学の過去問・公式問題ではありません。予想問題であり，大学とは関係がありません。'
CL = 'abcdefg'
NAMES = {'1': '第1問', '2': '第2問', '3': '第3問', '4': '第4問'}
TITLES = {'1': '長文読解（論説文）', '2': '長文読解（物語文）', '3': '意見を述べる英作文', '4': '会話文の完成'}
INTRO = {
    '1': 'つぎの英文を読み，下の各問いに答えよ。',
    '2': 'つぎの英文を読み，下の各問いに答えよ。',
    '3': 'Read the text that follows. Then respond to the question in roughly 150 English words, giving reasons for your view. Write the total word count after your response; punctuation marks do not count as words.',
    '4': 'Each of the two dialogues below has four gaps, (1) to (4). Write a suitable line of English for every gap so that the dialogue flows naturally. Your lines may be longer or shorter than the space shown.',
}
TF_STEM = 'つぎの英文 {r} について，本文に書かれていることに合うなら〇，合わないなら×を書け。'
PAGE_INFO = {}

def em(s): return kb.em(s)
def mark(t):
    t = e(t)
    t = re.sub(r'\{(\d+)\|([^}]*)\}', r'<span class="ul">\2</span><sub class="ulab">(\1)</sub>', t)
    t = re.sub(r'\[\[(\d+)\]\]', r'<span class="blank">(&#8194;\1&#8194;)</span>', t)
    return re.sub(r'(?<=[A-Za-z)])\*', '<sup class="ast">＊</sup>', t)
def plain(t):
    t = re.sub(r'\{\d+\|([^}]*)\}', r'\1', t)
    return re.sub(r'\[\[\d+\]\]', ' ', t).replace('*', '')
def filled(P):
    """空所に正解を入れた本文（語数・照合用）。mc の blank 番号つきの設問の正解を使う。"""
    ans = {str(q['blank']): q['choices'][q['answer']] for q in P['questions'] if q['kind'] == 'mc' and q.get('blank')}
    return ' '.join(plain(re.sub(r'\[\[(\d+)\]\]', lambda m: ans.get(m.group(1), ' '), p)) for p in P['paras'])

H_CSS = hk.H_CSS + """
.passage p { text-indent: 1.2em; }
.ptitle { font-family: 'Noto Serif'; font-weight: 700; font-size: 11.2pt; text-align: center; margin: 1mm 0 2.4mm; }
.ulab { font-size: 7pt; margin-left: .3mm; }
.notes { margin: 2mm 0 3mm; font-size: 9pt; display: grid; grid-template-columns: 1fr 1fr; gap: .4mm 6mm; }
.notes .en { font-family: 'Noto Serif'; font-style: italic; }
.uq { margin: 2.2mm 0 0; display: grid; grid-template-columns: 11mm 1fr; font-size: 10pt; break-inside: avoid; }
.uq .n { font-weight: 700; }
.uq .ch div { font-family: 'Noto Serif'; margin: .3mm 0; padding-left: 6mm; text-indent: -6mm; }
.uq .chrow { font-family: 'Noto Serif'; display: flex; flex-wrap: wrap; gap: 0 7mm; margin-top: .4mm; }
.essay-text { border: .6pt solid #777; padding: 2mm 4mm; margin: 2mm 0 3mm; font-family: 'Noto Serif'; font-size: 10pt; line-height: 1.7; }
.qline { font-family: 'Noto Serif'; font-weight: 700; margin: 2mm 0; }
.conv { margin: 2.6mm 0 0; font-family: 'Noto Serif'; font-size: 10pt; break-inside: avoid; }
.conv .lab { font-weight: 700; margin-bottom: .8mm; }
.conv .setting { font-size: 9pt; font-style: italic; margin-bottom: 1mm; }
.conv .ln { display: grid; grid-template-columns: 16mm 1fr; margin: .5mm 0; }
.conv .gap { border-bottom: .6pt solid #333; display: inline-block; min-width: 105mm; }
.ansgrid { border-collapse: collapse; margin: 1mm 0 2mm; }
.ansgrid td, .ansgrid th { border: .6pt solid #555; min-width: 13mm; height: 8.5mm; text-align: center; font-size: 8.8pt; padding: 0 1.5mm; }
.ansgrid th { height: 5.5mm; font-weight: 500; }
.wcbox { border: .6pt solid #555; display: inline-block; padding: 1mm 4mm; margin: 1mm 0 2mm; font-size: 9pt; }
"""

def cover(R, kind, D):
    sub = '問題' if kind == 'q' else '解答・解説'
    rng = PAGE_INFO.get((R, kind), '')
    pts = '・'.join(f'{NAMES[n]} {D["points"][n]}点' for n in ('1', '2', '3', '4')) + '（計200点）'
    if kind == 'q':
        items = [f'問題部分と解答用紙で構成されている{rng}。答えは解答用紙の決められた欄に書くこと。',
                 '試験時間の目安は120分（第1問〜第4問のすべてを解く場合）。第1問は論説文，第2問は物語文の読解。',
                 '第3問・第4問の指示は英語で書かれている。第3問は約150語の英作文，第4問は会話文の空所に英文を書く問題。',
                 f'配点は {pts}。本予想問題が独自に定めた配点である。',
                 '本冊子の英文・設問はすべてオリジナルである。登場する人物・団体・地名は架空。']
    else:
        items = [f'解答一覧・設問ごとの解答と解説{rng}。',
                 '記号で答える設問は，正解の根拠と，ほかの選択肢が誤りである理由を示した。',
                 '和訳・日本語の説明・英作文は，採点基準と解答例（別解）を示した。第4問は空所ごとの解答例を示した。',
                 '第1問・第2問の英文は全訳と重要語句つき。',
                 f'配点は {pts}。本予想問題が独自に定めた配点で，大学の配点ではない。']
    lis = ''.join(f'<li>{x}</li>' for x in items)
    return f"""<section class="ocover">
<div class="brand"><img src="file://{HERE}/logo_gray.png"><div class="kicker">学習アプリ マナトビ</div></div>
<div class="box">{R}</div>
<div class="l1">予想問題 第{R}回</div>
<div class="l2">前期日程 対策</div>
<h1>英語{'問題' if kind == 'q' else '解答'}</h1>
<div class="sub">宇都宮大学（データサイエンス経営学部・国際学部・工学部・農学部 共通の問題冊子）の出題形式に準拠 ／ {sub}</div>
<div class="chui"><span class="ttl">注　意</span><ol>{lis}</ol></div>
<div class="disc">{DISCLAIMER}<br>本冊子は過去の出題形式を分析して作成した練習用の教材です。</div>
<div class="foot"><span>学習アプリ マナトビ</span><span>予想問題 第{R}回 ／ {sub}</span></div></section>"""

def head(n, pts):
    return f'<div class="parthead" data-run="{NAMES[n]}　{TITLES[n]}"><span class="roman">{n}</span><span class="t">{NAMES[n]}　{TITLES[n]}（配点 {pts}点）</span></div>'

def intro(n):
    style = ' style="font-family:\'Noto Serif\'"' if n in ('3', '4') else ''
    return f'<p class="intro"{style}>{e(INTRO[n])}</p>'

def chs(choices):
    if max(len(c) for c in choices) <= 22:
        return '<div class="chrow">' + ''.join(f'<span>{CL[i]}. {e(c)}</span>' for i, c in enumerate(choices)) + '</div>'
    return '<div class="ch">' + ''.join(f'<div>{CL[i]}. {e(c)}</div>' for i, c in enumerate(choices)) + '</div>'

def stem(q):
    if q['kind'] == 'tf': return TF_STEM.format(r=f'a〜{CL[len(q["statements"]) - 1]}')
    return q['stem']

def q_html(q, i):
    body = ''
    if q['kind'] == 'mc': body = chs(q['choices'])
    elif q['kind'] == 'tf': body = '<div class="ch">' + ''.join(f'<div>{CL[k]}. {e(s)}</div>' for k, s in enumerate(q['statements'])) + '</div>'
    return f'<div class="uq"><span class="n">問{i}</span><div><div>{e(stem(q))}</div>{body}</div></div>'

def long_html(P, n, pts):
    out = f'<section class="part">{head(n, pts)}{intro(n)}'
    if P.get('title'): out += f'<div class="ptitle">{e(P["title"])}</div>'
    out += '<div class="passage">' + ''.join(f'<p>{mark(p)}</p>' for p in P['paras']) + '</div>'
    out += '<div style="font-size:9pt;margin-top:2mm">〔注〕</div><div class="notes">' + ''.join(f'<div><span class="en">{e(a)}</span>：{e(b)}</div>' for a, b in P['notes']) + '</div>'
    out += ''.join(q_html(q, i) for i, q in enumerate(P['questions'], 1))
    return out + '</section>'

def essay_html(P, pts):
    return (f'<section class="part">{head("3", pts)}{intro("3")}<div class="essay-text">{e(P["passage"])}</div>'
            f'<div class="qline">Question: {e(P["question"])}</div></section>')

def conv_lines(c, fill=None):
    out, k = '', 0
    for s, t in c['lines']:
        if t is None:
            txt = f'<b>({k + 1})</b> ' + (f'<span class="x-ul">{e(fill[k])}</span>' if fill else '<span class="gap"></span>')
            k += 1
        else: txt = e(t)
        out += f'<div class="ln"><span>{e(s)}:</span><span>{txt}</span></div>'
    return out

def conv_html(P, pts):
    out = f'<section class="part">{head("4", pts)}{intro("4")}'
    for c in P['convs']:
        out += f'<div class="conv"><div class="lab">Conversation {e(c["label"])}</div><div class="setting">{e(c["setting"])}</div>{conv_lines(c)}</div>'
    return out + '</section>'

def grid(labels):
    th = ''.join(f'<th>{e(x)}</th>' for x in labels); td = ''.join('<td></td>' for _ in labels)
    return f'<table class="ansgrid"><tr>{th}</tr><tr>{td}</tr></table>'

def sheet(D, R):
    H4 = '<h4 style="font-family:MPR;font-weight:800;margin:3mm 0 1mm">{}</h4>'
    out = f'<section class="sheet"><h2>解答用紙　予想問題 第{R}回</h2><div style="font-size:8.6pt;margin-bottom:2mm">受験番号・氏名欄は省略。記号は a のように小文字で書く。</div>'
    for n in ('1', '2'):
        out += H4.format(NAMES[n])
        mcs = [i for i, q in enumerate(D[n]['questions'], 1) if q['kind'] == 'mc']
        out += grid([f'問{i}' for i in mcs])
        for i, q in enumerate(D[n]['questions'], 1):
            if q['kind'] == 'trans': out += f'<div>問{i}</div>' + hk.wlines(3, False)
            elif q['kind'] == 'jp':
                if q.get('hi'): out += f'<div class="row tall"><span class="h">問{i}</span><div>{genko(q["hi"] + (20 - q["hi"] % 20) % 20)}</div></div>'
                else: out += f'<div>問{i}</div>' + hk.wlines(3, False)
            elif q['kind'] == 'tf': out += f'<div>問{i}</div>' + grid([CL[k] for k in range(len(q['statements']))])
    out += H4.format('第3問（約150語）') + hk.wlines(16) + '<div class="wcbox">語数：（　　　　）語</div>'
    out += H4.format('第4問')
    for c in D['4']['convs']:
        out += f'<div style="margin-top:1.5mm">Conversation {e(c["label"])}</div>'
        for k in range(len(c['answers'])): out += f'<div class="row"><span class="h">({k + 1})</span><span></span></div>'
    return out + '</section>'

def colophon(R, kind):
    return f"""<section class="colophon"><div class="box"><h2>奥付</h2>
<div>予想問題 第{R}回　英語　{'問題' if kind == 'q' else '解答・解説'}</div>
<div>対象：宇都宮大学 前期日程 英語（データサイエンス経営学部・国際学部・工学部・農学部 共通の問題冊子）の受験準備</div>
<div>作成：学習アプリ マナトビ 編集部（2026年11月）</div>
<div>作成方法：2024〜2026年度の出題形式・分量・難易度を分析し，英文・設問をすべて新たに書き下ろした。</div>
<div class="disc">{DISCLAIMER}</div>
<div style="margin-top:2.5mm;font-size:8.4pt">本冊子の英文は実在の記事・書籍・論文・統計からの引用・翻案ではありません。登場する人物・団体・地名・数値は架空です。無断転載・再配布を禁じます。</div>
<img src="file://{HERE}/logo_gray.png"></div></section>"""

# ---------------------------------------------------------------- 解答・解説
def box(inner): return f'<div class="abox">{inner}</div>'
def ul(items): return '<ul>' + ''.join(f'<li>{em(x)}</li>' for x in items) + '</ul>'
def wc(m): return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9’'-]*", m))

def answer_str(q):
    if q['kind'] == 'mc': return CL[q['answer']]
    if q['kind'] == 'tf': return '　'.join(f'{CL[k]}. {v}' for k, v in enumerate(q['answers']))
    return '解答例は解説参照（採点基準つき）'

def akey_long(P, n, pts):
    out = f'<section class="part akey"><h3>{NAMES[n]}　解答・解説（{pts}点）</h3>'
    for i, q in enumerate(P['questions'], 1):
        h = f'<h4>問{i}（{q["points"]}点）</h4>'
        st = f'<div style="font-size:8.8pt;margin:.6mm 0">設問：{e(stem(q))}</div>'
        if q['kind'] in ('mc', 'tf'):
            out += h + box(f'<div class="ans">正解　<span class="en">{e(answer_str(q))}</span></div>' + st + ul(q['explain']))
            continue
        b = f'<div><span class="lbl">解答例</span><span class="ans">{e(q["answer"])}</span></div>'
        for a in q.get('alts', []): b += f'<div style="margin-top:.8mm"><span class="lbl">別解</span><span class="x-ul">{e(a)}</span></div>'
        if q.get('hi'): b += f'<div style="font-size:8.4pt;margin-top:.6mm">字数：{"・".join(f"{len(a)}字" for a in [q["answer"]] + q.get("alts", []))}（{q["lo"]}〜{q["hi"]}字）</div>'
        out += h + box(b + st + crit_table(q['criteria']) + ul(q['explain']))
    out += '<h4>全訳</h4><div class="trs">' + ''.join(f'<p>{e(t)}</p>' for t in P['translation']) + '</div>'
    out += '<h4>重要語句</h4><table class="voc">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in P['vocab']) + '</table>'
    return out + '</section>'

def akey_essay(P, pts):
    out = f'<section class="part akey"><h3>第3問　解答・解説（{pts}点）</h3>'
    out += box(f'<div style="font-size:8.8pt">英文の訳：{e(P["passage_ja"])}</div><div style="font-size:8.8pt;margin-top:1mm">問いの訳：{e(P["question_ja"])}</div>' + crit_table(P['criteria']))
    for (lab, m), mja in zip(P['models'], P['models_ja']):
        out += f'<h4>解答例：{e(lab)}</h4>' + box(f'<div class="model">{e(m)} <span class="wc">（{wc(m)}語）</span></div><div style="font-size:8.6pt;margin-top:1mm">訳：{e(mja)}</div>')
    out += '<h4>書き方のポイント・減点されやすい点</h4>' + box(ul(P['tips']))
    return out + '</section>'

def akey_conv(P, pts):
    out = f'<section class="part akey"><h3>第4問　解答・解説（{pts}点・空所1つ{pts // sum(len(c["answers"]) for c in P["convs"])}点）</h3>'
    for c in P['convs']:
        out += f'<h4>Conversation {e(c["label"])}</h4>' + f'<div class="conv">{conv_lines(c, c["answers"])}</div>'
        out += box('<div style="font-size:8.8pt">会話の訳：' + '　'.join(e(x) for x in c['ja']) + '</div>' + ul(c['explain']))
    return out + '</section>'

def summary_table(D, R):
    rows = ''
    for n in ('1', '2'):
        for i, q in enumerate(D[n]['questions'], 1):
            rows += f'<tr><td>{NAMES[n]}</td><td>問{i}</td><td>{e(answer_str(q))}</td><td>{q["points"]}</td></tr>'
    rows += f'<tr><td>第3問</td><td>—</td><td>意見を述べる英作文：採点基準と解答例は解説参照</td><td>{D["points"]["3"]}</td></tr>'
    rows += f'<tr><td>第4問</td><td>—</td><td>会話文の完成：空所ごとの解答例は解説参照</td><td>{D["points"]["4"]}</td></tr>'
    return f'<section class="part akey"><h3>解答一覧　予想問題 第{R}回</h3><table class="sum"><tr><th>大問</th><th>設問</th><th>解答</th><th>配点</th></tr>{rows}<tr><td colspan="3" style="text-align:right">合計</td><td>200</td></tr></table></section>'

def check_points(D):
    assert sum(D['points'].values()) == 200
    for n in ('1', '2'):
        assert sum(q['points'] for q in D[n]['questions']) == D['points'][n], n
        for q in D[n]['questions']:
            if q['kind'] in ('trans', 'jp'): assert sum(p for _, p in q['criteria']) == q['points'], (n, q.get('stem', '')[:10])
    assert sum(p for _, p in D['3']['criteria']) == D['points']['3']
    k = sum(len(c['answers']) for c in D['4']['convs']); assert D['points']['4'] % k == 0

def write(doc, out):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    css = [CSS(string=mono(kb.CSS_TEXT + H_CSS), font_config=FC)]
    HTML(string=mono(doc), base_url=str(HERE)).write_pdf(out, stylesheets=css, font_config=FC, metadata={'author': 'マナトビ'})
    return out

def load(R): return importlib.import_module(f'u{R}').DATA

def build_q(R):
    D = load(R); check_points(D); p = D['points']
    body = cover(R, 'q', D) + long_html(D['1'], '1', p['1']) + long_html(D['2'], '2', p['2']) + essay_html(D['3'], p['3']) + conv_html(D['4'], p['4']) + sheet(D, R) + colophon(R, 'q')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 問題</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_utsunomiya_eng_yoso{R}_mondai.pdf')

def build_a(R):
    D = load(R); check_points(D); p = D['points']
    body = cover(R, 'a', D) + summary_table(D, R) + akey_long(D['1'], '1', p['1']) + akey_long(D['2'], '2', p['2']) + akey_essay(D['3'], p['3']) + akey_conv(D['4'], p['4']) + colophon(R, 'a')
    return write(f'<html lang="ja"><head><meta charset="utf-8"><title>予想問題 第{R}回 英語 解答・解説</title></head><body>{body}</body></html>', OUT_DIR / f'manatobi_utsunomiya_eng_yoso{R}_kaitou.pdf')

if __name__ == '__main__':
    R = sys.argv[1] if len(sys.argv) > 1 else '1'
    for kind, f in (('q', build_q), ('a', build_a)):
        o = f(R); PAGE_INFO[(R, kind)] = hk.page_range(o, kind)
        o = f(R); print(o.name, o.stat().st_size // 1024, 'KB', PAGE_INFO[(R, kind)])
