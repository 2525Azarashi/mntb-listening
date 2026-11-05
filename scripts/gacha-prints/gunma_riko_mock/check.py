# -*- coding: utf-8 -*-
"""群馬大 予想問題の検査（商用利用のため毎回実行）。 python3 check.py 1 2 3 → logs/check.json（NG があれば終了コード1）
 1) オリジナル性：過去問（公式PDFのテキスト・解答例）と英語4語連続／日本語13字連続の一致，登場人物名の重複，題材の近さ（TF-IDF）。
    照合先は .tmpwork/gunma_ref に加え，あれば utsunomiya・fukushima・yamagata・akita・iwate・hirosaki・tohoku・hokudai・kobe・osaka・ritsu の ref も使う。
 2) 設問の質：第1問A 空所1つ・選択肢4つの重複なし／B 下線4か所が①〜④の順・訂正が元と違う／C 空所が通し番号・正解の重複なし・使わない選択肢がある・空所は計10／
    第2問 注の付け忘れ・全訳の段落数・各5問・最後は表題／第3問 空所10・書き出し1〜4字・残り2字以上・全訳の段落数・解説10／
    正解位置の偏り・正解だけ極端に長い選択肢・禁止語・render.py の固定文言。
"""
import re, sys, json, glob, importlib
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
REFS = [ROOT / '.tmpwork/gunma_ref'] + [ROOT / f'.tmpwork/{u}_ref' for u in ('utsunomiya', 'fukushima', 'yamagata', 'akita', 'iwate', 'hirosaki', 'tohoku', 'hokudai', 'kobe', 'osaka', 'ritsu')]
BANNED = ['的中', '必ず出る', '合格できる', 'MANATOBI MOCK EXAM SERIES']
def norm(t): return re.sub(r'\s+', ' ', t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()
def words(t): return [w.lower() for w in re.findall(r"[A-Za-z]+(?:'[a-z]+)?", norm(t))]
def jchars(t): return re.sub(r'[^\u3040-\u30ff\u4e00-\u9fff]', '', t)
def collect(o, out):
    if isinstance(o, str): out.append(render.plain(o))
    elif isinstance(o, dict): [collect(v, out) for v in o.values()]
    elif isinstance(o, (list, tuple)): [collect(v, out) for v in o]

SRC = {}
for d in REFS:
    for f in glob.glob(str(d / 'ocr/*.txt')): SRC[f'{d.name}/{Path(f).stem}'] = open(f, errors='ignore').read()
ALLSRC = '\n'.join(SRC.values())
EN4, JA13 = {}, {}
for k, t in SRC.items():
    w = words(t)
    for i in range(len(w) - 3): EN4.setdefault(tuple(w[i:i + 4]), set()).add(k)
    j = jchars(t)
    for i in range(len(j) - 12): JA13.setdefault(j[i:i + 13], set()).add(k)

def overlaps(texts):
    e4, j13 = {}, {}
    for x in texts:
        w = words(x)
        for i in range(len(w) - 3):
            g = tuple(w[i:i + 4])
            if g in EN4 and not all(len(y) == 1 for y in g): e4[' '.join(g)] = sorted(EN4[g])[:3]
        j = jchars(x)
        for i in range(len(j) - 12):
            if j[i:i + 13] in JA13: j13[j[i:i + 13]] = sorted(JA13[j[i:i + 13]])[:3]
    return e4, j13

rounds = sys.argv[1:] or ['1']
rep, ng = {}, []
pos = Counter(); longest = [0, 0]

def choice_stats(tag, ch, ans, count_pos=True):
    if len(set(map(norm, ch))) != len(ch): ng.append((tag, 'dup_choices'))
    if len(ch) != 4: ng.append((tag, 'choices_count', len(ch)))
    if not 0 <= ans < len(ch): ng.append((tag, 'answer_index')); return
    if count_pos: pos[ans] += 1
    Ls = [len(c) for c in ch]; longest[1] += 1
    if Ls[ans] == max(Ls) and Ls.count(max(Ls)) == 1 and max(Ls) > 1.4 * sorted(Ls)[-2]: longest[0] += 1

def para_checks(tag, P):
    raw = ' '.join(P['paras'])
    if len(P['translation']) != len(P['paras']): ng.append((tag, 'translation_paragraphs', len(P['translation']), len(P['paras'])))
    for nt, _ in P.get('notes', []):
        if not re.search(re.escape(nt) + r'\*', raw, re.I): ng.append((tag, 'note_not_marked', nt))
    for m in re.findall(r"([A-Za-z][A-Za-z\-]*)\*", raw):
        if m.lower() not in [x.lower() for x, _ in P.get('notes', [])]: ng.append((tag, 'mark_without_note', m))

for R in rounds:
    D = importlib.import_module(f'g{R}').DATA
    if sum(D['points'].values()) != 200: ng.append((f'r{R}', 'total_points'))
    for part in ('A', 'B', 'C', '2A', '2B', '3A', '3B'):
        texts = []; collect(D[part], texts)
        if part == 'B': texts += [render.b_fixed(q) for q in D['B']]
        if part == 'A': texts += [q['stem'].replace('[[]]', q['choices'][q['answer']]) for q in D['A']]
        e4, j13 = overlaps(texts)
        rep[f'r{R}-{part}'] = dict(en4=e4, ja13=j13)
        if e4: ng.append((f'r{R}-{part}', 'en4', list(e4)))
        if j13: ng.append((f'r{R}-{part}', 'ja13', list(j13)))
        for b in BANNED:
            if any(b in t for t in texts): ng.append((f'r{R}-{part}', 'banned_word', b))
    for nm in D.get('names', []):
        if re.search(r'\b' + re.escape(nm) + r'\b', ALLSRC): ng.append((f'r{R}', 'name_in_past', nm))
    for i, q in enumerate(D['A'], 1):
        t = f'r{R}-A{i}'
        if q['stem'].count('[[]]') != 1: ng.append((t, 'blank_count'))
        choice_stats(t, q['choices'], q['answer'])
        if len(q['explain']) < 2: ng.append((t, 'explain_short'))
    for i, q in enumerate(D['B'], 1):
        t = f'r{R}-B{i}'
        segs = re.findall(r'\{(\d)\|([^}]*)\}', q['sent'])
        if [s for s, _ in segs] != ['1', '2', '3', '4']: ng.append((t, 'underline_order', [s for s, _ in segs]))
        elif not 1 <= q['answer'] <= 4: ng.append((t, 'answer_range'))
        else:
            pos[q['answer'] - 1] += 1
            if segs[q['answer'] - 1][1] == q['correct']: ng.append((t, 'correct_same'))
        if len(q['explain']) < 2: ng.append((t, 'explain_short'))
    total_c = 0
    for i, c in enumerate(D['C'], 1):
        t = f'r{R}-C{i}'
        nums = [int(x) for s, l in c['lines'] for x in re.findall(r'\[\[(\d)\]\]', l)]
        m = len(c['answers']); total_c += m
        if nums != list(range(1, m + 1)): ng.append((t, 'gap_numbers', nums))
        if len(c['choices']) != 4 or len(set(c['answers'])) != m or m >= 4: ng.append((t, 'conv_choices'))
        for a in c['answers']:
            if not 0 <= a < 4: ng.append((t, 'answer_index'))
            else: pos[a] += 1
        if len(c['explain']) < m + 1: ng.append((t, 'explain_short'))
        if len(c['ja']) != len(c['lines']): ng.append((t, 'ja_lines'))
    if total_c != 10: ng.append((f'r{R}-C', 'gap_total', total_c))
    for k in ('2A', '2B'):
        P = D[k]; para_checks(f'r{R}-{k}', P)
        if len(P['questions']) != 5: ng.append((f'r{R}-{k}', 'question_count'))
        if 'title' not in P['questions'][-1]['q'].lower(): ng.append((f'r{R}-{k}', 'last_not_title'))
        for i, q in enumerate(P['questions'], 1):
            choice_stats(f'r{R}-{k}-{i}', q['choices'], q['answer'])
            if len(q['explain']) < 2: ng.append((f'r{R}-{k}-{i}', 'explain_short'))
    for k in ('3A', '3B'):
        P = D[k]; para_checks(f'r{R}-{k}', P)
        G = render.gaps(P)
        if len(G) != 10: ng.append((f'r{R}-{k}', 'gap_count', len(G)))
        if len(P['explain']) != len(G): ng.append((f'r{R}-{k}', 'explain_count'))
        for j, (a, b) in enumerate(G):
            if not 1 <= len(a) <= 4 or len(b) < 2 or not re.fullmatch(r'[A-Za-z]+', a + b): ng.append((f'r{R}-{k}-{j + 1}', 'gap_shape', a, b))
        fulls = [(a + b).lower() for a, b in G]
        if len(set(fulls)) != len(fulls): ng.append((f'r{R}-{k}', 'gap_duplicate_word'))

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    pk, pt = [], []
    for d in REFS:
        f = d / 'analysis/passages.json'
        if not f.exists(): continue
        for y, P in json.load(open(f)).items():
            for k, t in (P.items() if isinstance(P, dict) else []):
                if isinstance(t, str) and len(t) > 200: pk.append(f'{d.name}/{y}-{k}'); pt.append(t)
    mk, mt = [], []
    for R in rounds:
        D = importlib.import_module(f'g{R}').DATA
        for k in ('2A', '2B', '3A', '3B'): mk.append(f'r{R}-{k}'); mt.append(' '.join(render.plain(p) for p in D[k]['paras']))
    v = TfidfVectorizer(stop_words='english', sublinear_tf=True).fit(pt + mt)
    S_ = cosine_similarity(v.transform(mt), v.transform(pt)); SP = cosine_similarity(v.transform(pt))
    pp = sorted(SP[i][j] for i in range(len(pk)) for j in range(i + 1, len(pk)))
    rep['topic'] = {k: (round(float(S_[i].max()), 3), pk[S_[i].argmax()]) for i, k in enumerate(mk)}
    rep['topic_past_ref'] = dict(n=len(pk), median=round(float(pp[len(pp) // 2]), 3), max=round(float(pp[-1]), 3))
    for k, (s, _) in rep['topic'].items():
        if s >= rep['topic_past_ref']['max']: ng.append((k, 'topic_too_close', s))
except Exception as ex:
    rep['topic_error'] = str(ex)

SRC_R = open(HERE / 'render.py').read()
FIXED = re.findall(r"'([^'\n]{8,})'|\"([^\"\n]{8,})\"", SRC_R)
fe, fj = overlaps([a or b for a, b in FIXED])
rep['render_fixed'] = dict(en4=sorted(fe), ja13=sorted(fj))
if fe or fj: ng.append(('render.py', 'fixed_text_overlap', sorted(fe) + sorted(fj)))
for b in BANNED:
    if b in SRC_R: ng.append(('render.py', 'banned_word', b))
rep['answer_positions'] = {render.CN[p]: c for p, c in sorted(pos.items())}
rep['far_longest_answer'] = f'{longest[0]}/{longest[1]}'
if longest[1] and longest[0] / longest[1] > 0.2: ng.append(('all', 'longest_answer_bias', rep['far_longest_answer']))
cs = [pos.get(p, 0) for p in range(4)]
if sum(cs) >= 8 and max(cs) - min(cs) > max(3, sum(cs) // 6): ng.append(('all', 'position_bias', cs))
rep['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(rep, open(HERE / 'logs/check.json', 'w'), ensure_ascii=False, indent=1, default=list)
print(json.dumps({k: v for k, v in rep.items() if k in ('topic', 'topic_past_ref', 'render_fixed', 'answer_positions', 'far_longest_answer', 'ng', 'topic_error')}, ensure_ascii=False, indent=1, default=list))
sys.exit(1 if ng else 0)
