# -*- coding: utf-8 -*-
"""宇都宮大 予想問題の検査（商用利用のため毎回実行）。 python3 check.py 1 2 3 → logs/check.json（NG があれば終了コード1）
 1) オリジナル性：過去問（公式PDFのOCR・解答例・出題の意図）と英語4語連続／日本語13字連続の一致，登場人物名の重複，題材の近さ（TF-IDF）。
    照合先は .tmpwork/utsunomiya_ref に加え，あれば fukushima・yamagata・akita・iwate・hirosaki・tohoku・hokudai・kobe・osaka・ritsu の ref も使う。
 2) 設問の質：下線 {n|…}・空所 [[n]] と設問の対応（trans/jp の target・mc の blank）・選択肢の数と重複・正解位置の偏り・
    正解だけ極端に長い選択肢・〇×が全部同じでない・注の付け忘れ・全訳の段落数・配点と採点基準の合計・字数指定の範囲・
    第3問の解答例が2つ（賛否の両方）・第4問の空所の数と解答例の数・解説の英文引用“…”が本文か選択肢に実在・禁止語・render.py の固定文言。
"""
import re, sys, json, glob, importlib
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
REFS = [ROOT / '.tmpwork/utsunomiya_ref'] + [ROOT / f'.tmpwork/{u}_ref' for u in ('fukushima', 'yamagata', 'akita', 'iwate', 'hirosaki', 'tohoku', 'hokudai', 'kobe', 'osaka', 'ritsu')]
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

def choice_stats(tag, ch, ans):
    if len(set(map(norm, ch))) != len(ch): ng.append((tag, 'dup_choices'))
    if not 0 <= ans < len(ch): ng.append((tag, 'answer_index')); return
    pos[ans] += 1
    Ls = [len(c) for c in ch]; longest[1] += 1
    if Ls[ans] == max(Ls) and Ls.count(max(Ls)) == 1 and max(Ls) > 1.4 * sorted(Ls)[-2]: longest[0] += 1

def quotes_ok(tag, texts, pool):
    for t in texts:
        for qt in re.findall(r'“([^”]+)”', t):
            for seg in re.split(r'\s*(?:…|\.\.\.)\s*', norm(qt)):
                seg = seg.strip(' ,.;:!?"\'').lower()
                if len(seg) >= 8 and re.search(r'[a-z]{3}', seg) and seg not in pool: ng.append((tag, 'quote_not_found', seg[:80]))

for R in rounds:
    D = importlib.import_module(f'u{R}').DATA
    if sum(D['points'].values()) != 200: ng.append((f'r{R}', 'total_points'))
    for part in ('1', '2', '3', '4'):
        texts = []; collect(D[part], texts)
        e4, j13 = overlaps(texts)
        rep[f'r{R}-{part}'] = dict(en4=e4, ja13=j13)
        if e4: ng.append((f'r{R}-{part}', 'en4', list(e4)))
        if j13: ng.append((f'r{R}-{part}', 'ja13', list(j13)))
        for b in BANNED:
            if any(b in t for t in texts): ng.append((f'r{R}-{part}', 'banned_word', b))
    for nm in D.get('names', []):
        if re.search(r'\b' + re.escape(nm) + r'\b', ALLSRC): ng.append((f'r{R}', 'name_in_past', nm))
    for n in ('1', '2'):
        P = D[n]; tag = f'r{R}-{n}'; raw = ' '.join(P['paras'])
        if len(P['translation']) != len(P['paras']): ng.append((tag, 'translation_paragraphs'))
        for nt, _ in P['notes']:
            if not re.search(re.escape(nt) + r'\*', raw, re.I): ng.append((tag, 'note_not_marked', nt))
        for m in re.findall(r"([A-Za-z][A-Za-z\-]*)\*", raw):
            if m.lower() not in [x.lower() for x, _ in P['notes']]: ng.append((tag, 'mark_without_note', m))
        U = {k: v for k, v in re.findall(r'\{(\d+)\|([^}]*)\}', raw)}
        B = re.findall(r'\[\[(\d+)\]\]', raw)
        seen_u, seen_b = [], []
        for i, q in enumerate(P['questions'], 1):
            qt = f'{tag}-問{i}'
            if q.get('ul'):
                u = str(q['ul']); seen_u.append(u)
                if u not in U: ng.append((qt, 'underline_missing', u))
                elif q.get('target') and q['target'] != U[u]: ng.append((qt, 'target_mismatch', u))
                if f'下線部({u})' not in q['stem']: ng.append((qt, 'stem_label', u))
            if q.get('blank'):
                b = str(q['blank']); seen_b.append(b)
                if b not in B: ng.append((qt, 'blank_missing', b))
                if f'空所({b})' not in q['stem']: ng.append((qt, 'stem_blank_label', b))
            if q['kind'] == 'mc':
                if len(q['choices']) not in (4, 5): ng.append((qt, 'choices_count'))
                choice_stats(qt, q['choices'], q['answer'])
            elif q['kind'] == 'tf':
                if len(q['answers']) != len(q['statements']) or set(q['answers']) - {'〇', '×'}: ng.append((qt, 'tf_answers'))
                if len(set(q['answers'])) < 2: ng.append((qt, 'tf_all_same'))
            else:
                if sum(p for _, p in q['criteria']) != q['points']: ng.append((qt, 'criteria_sum'))
                if q.get('hi'):
                    for a in [q['answer']] + q.get('alts', []):
                        if not q['lo'] <= len(a) <= q['hi']: ng.append((qt, 'length', len(a)))
            if len(q.get('explain', [])) < 2: ng.append((qt, 'explain_too_short'))
            pool = norm(render.filled(P)).lower() + ' ' + ' '.join(norm(c).lower() for qq in P['questions'] for c in qq.get('choices', []) + qq.get('statements', []))
            quotes_ok(qt, q.get('explain', []), pool)
        if sorted(seen_u) != sorted(U): ng.append((tag, 'underline_vs_questions', sorted(U), sorted(seen_u)))
        if sorted(seen_b) != sorted(B): ng.append((tag, 'blank_vs_questions', sorted(B), sorted(seen_b)))
        if sum(q['points'] for q in P['questions']) != D['points'][n]: ng.append((tag, 'points_sum'))
    E = D['3']
    if sum(p for _, p in E['criteria']) != D['points']['3']: ng.append((f'r{R}-3', 'criteria_sum'))
    if len(E['models']) != 2 or len(E['models_ja']) != 2: ng.append((f'r{R}-3', 'models'))
    C = D['4']
    if len(C['convs']) != 2: ng.append((f'r{R}-4', 'conv_count'))
    for c in C['convs']:
        k = sum(t is None for _, t in c['lines'])
        if k != 4 or len(c['answers']) != k: ng.append((f'r{R}-4', 'gaps', c['label'], k, len(c['answers'])))
        if len(c['explain']) < 4: ng.append((f'r{R}-4', 'conv_explain', c['label']))

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
        D = importlib.import_module(f'u{R}').DATA
        for n in ('1', '2'): mk.append(f'r{R}-{n}'); mt.append(render.filled(D[n]))
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
rep['answer_positions'] = {render.CL[p]: c for p, c in sorted(pos.items())}
rep['far_longest_answer'] = f'{longest[0]}/{longest[1]}'
if longest[1] and longest[0] / longest[1] > 0.2: ng.append(('all', 'longest_answer_bias', rep['far_longest_answer']))
cs = [pos.get(p, 0) for p in range(4)]
if sum(cs) >= 8 and max(cs) - min(cs) > max(2, sum(cs) // 4): ng.append(('all', 'position_bias', cs))
rep['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(rep, open(HERE / 'logs/check.json', 'w'), ensure_ascii=False, indent=1, default=list)
print(json.dumps({k: v for k, v in rep.items() if k in ('topic', 'topic_past_ref', 'render_fixed', 'answer_positions', 'far_longest_answer', 'ng', 'topic_error')}, ensure_ascii=False, indent=1, default=list))
sys.exit(1 if ng else 0)
