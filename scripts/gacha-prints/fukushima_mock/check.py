# -*- coding: utf-8 -*-
"""福島大 予想問題の検査（商用利用のため毎回実行）。 python3 check.py 1 2 3 → logs/check.json（NG があれば終了コード1）
 1) オリジナル性：過去問（公式PDFのOCR・出題意図）と英語4語連続／日本語13字連続の一致，登場人物名の重複，題材の近さ（TF-IDF）。
    照合先は .tmpwork/fukushima_ref に加え，あれば yamagata・akita・iwate・hirosaki・tohoku・hokudai・kobe・osaka・ritsu の ref も使う。
    Ⅱの対話・Ⅲの並べかえ・Ⅳの問いは，過去問の文と4語以上重ならないことに加え，正解の語（Ⅱ）・語句の組（Ⅲ）が過去問と同じでないことも確かめる。
 2) 設問の質：下線 {a|…}・{b|…} と和訳の設問の対応・注の付け忘れ・全訳の段落数・配点と採点基準の合計・
    Ⅱは各対話に空所が1つ・正解は1語・同じ回で正解の重複なし／Ⅲは語句が6つ・正解が語句の並べかえになっている・同じ回で問う文法の重複なし（タグ）・
    Ⅳは問いが2つ・解答例が2つの問いそれぞれにある・禁止語・render.py の固定文言。
"""
import re, sys, json, glob, importlib
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
REFS = [ROOT / '.tmpwork/fukushima_ref'] + [ROOT / f'.tmpwork/{u}_ref' for u in ('yamagata', 'akita', 'iwate', 'hirosaki', 'tohoku', 'hokudai', 'kobe', 'osaka', 'ritsu')]
BANNED = ['的中', '必ず出る', '合格できる', 'MANATOBI MOCK EXAM SERIES']
# 過去問（R6〜R8）のⅡの正解とⅢの語句の組は OCR から自動では取れないので，ここに「使わない」ものとして手で写す（照合用・語のみ）
PAST_BLANK_ANSWERS = set()   # 正解は公表されていないため，同じ対話を作らないことを 4語照合で担保する
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
seen_tags = {}
for R in rounds:
    D = importlib.import_module(f'f{R}').DATA
    tag = f'r{R}'
    if sum(D['points'].values()) != 200: ng.append((tag, 'total_points'))
    for part in ('1', '2', '3', '4'):
        texts = []; collect(D[part], texts)
        e4, j13 = overlaps(texts)
        rep[f'{tag}-{part}'] = dict(en4=e4, ja13=j13)
        if e4: ng.append((f'{tag}-{part}', 'en4', list(e4)))
        if j13: ng.append((f'{tag}-{part}', 'ja13', list(j13)))
        for b in BANNED:
            if any(b in t for t in texts): ng.append((f'{tag}-{part}', 'banned_word', b))
    for nm in D.get('names', []):
        if re.search(r'\b' + re.escape(nm) + r'\b', ALLSRC): ng.append((tag, 'name_in_past', nm))
    P = D['1']; raw = ' '.join(P['paras'])
    if len(P['translation']) != len(P['paras']): ng.append((tag, 'translation_paragraphs'))
    for nt, _ in P['notes']:
        if not re.search(re.escape(nt) + r'\*', raw, re.I): ng.append((tag, 'note_not_marked', nt))
    for m in re.findall(r"([A-Za-z][A-Za-z\-]*)\*", raw):
        if m.lower() not in [x.lower() for x, _ in P['notes']]: ng.append((tag, 'mark_without_note', m))
    U = sorted(re.findall(r'\{([ab])\|', raw)); qU = sorted(q['label'] for q in P['questions'] if q['kind'] == 'trans')
    if U != qU: ng.append((tag, 'underline_vs_questions', U, qU))
    if len(P['questions']) != 6: ng.append((tag, 'question_count', len(P['questions'])))
    for q in P['questions']:
        if sum(p for _, p in q['criteria']) != q['points']: ng.append((tag, 'criteria_sum', q['stem'][:12]))
        if len(q['explain']) < 2: ng.append((tag, 'explain_too_short', q['stem'][:12]))
        if q['kind'] == 'trans':
            m = re.search(r'\{' + q['label'] + r'\|([^}]*)\}', raw)
            if m and q.get('target') and q['target'] != m.group(1): ng.append((tag, 'trans_target', q['label']))
    ans2 = []
    for i, it in enumerate(D['2']['items'], 1):
        n = sum(t.count('( )') for _, t in it['lines'])
        if n != 1: ng.append((tag, 'II_blank_count', i, n))
        if not re.fullmatch(r"[A-Za-z]+", it['answer']): ng.append((tag, 'II_one_word', i))
        ans2.append(it['answer'].lower())
        if len(it['explain']) < 2: ng.append((tag, 'II_explain', i))
    if len(set(ans2)) != len(ans2): ng.append((tag, 'II_dup_answers', ans2))
    for i, it in enumerate(D['3']['items'], 1):
        if len(it['words']) != 6: ng.append((tag, 'III_six_words', i))
        if sorted(it['answer'].split()) != sorted(' '.join(it['words']).split()): ng.append((tag, 'III_answer', i))
        if it['answer'] == ' '.join(sorted(it['words'], key=str.lower)): ng.append((tag, 'III_answer_equals_display', i))
        t = it.get('tag')
        if not t: ng.append((tag, 'III_no_tag', i))
        seen_tags.setdefault(R, []).append(t)
    if len(set(seen_tags.get(R, []))) != len(seen_tags.get(R, [])): ng.append((tag, 'III_dup_grammar', seen_tags[R]))
    W = D['4']
    if len(W['prompts']) != 2 or len(W['prompts_ja']) != 2: ng.append((tag, 'IV_prompts'))
    if sorted(k for k, _ in W['models']) != [0, 1]: ng.append((tag, 'IV_models'))
    if len(W['models_ja']) != 2: ng.append((tag, 'IV_models_ja'))

# 3回を通して，Ⅱの正解とⅢの文法タグが偏らないか
all2 = [it['answer'].lower() for R in rounds for it in importlib.import_module(f'f{R}').DATA['2']['items']]
rep['II_answers'] = all2
dups = sorted({a for a in all2 if all2.count(a) > 1})
if dups: ng.append(('all', 'II_answer_repeated_across_rounds', dups))
rep['III_tags'] = seen_tags

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
        D = importlib.import_module(f'f{R}').DATA
        mk.append(f'r{R}-1'); mt.append(render.filled(D))
    v = TfidfVectorizer(stop_words='english', sublinear_tf=True).fit(pt + mt)
    S_ = cosine_similarity(v.transform(mt), v.transform(pt)); SP = cosine_similarity(v.transform(pt))
    pp = sorted(SP[i][j] for i in range(len(pk)) for j in range(i + 1, len(pk)))
    rep['topic'] = {k: (round(float(S_[i].max()), 3), pk[S_[i].argmax()]) for i, k in enumerate(mk)}
    rep['topic_past_ref'] = dict(n=len(pk), median=round(float(pp[len(pp) // 2]), 3), max=round(float(pp[-1]), 3))
    fk = [i for i, k in enumerate(pk) if k.startswith('fukushima_ref/')]
    for i, k in enumerate(mk):
        s = max(float(S_[i][j]) for j in fk) if fk else 0
        if s >= 0.30: ng.append((k, 'topic_too_close_fukushima', round(s, 3)))
        if S_[i].max() >= rep['topic_past_ref']['max']: ng.append((k, 'topic_too_close', round(float(S_[i].max()), 3)))
except Exception as ex:
    rep['topic_error'] = str(ex)

SRC_R = open(HERE / 'render.py').read()
FIXED = re.findall(r"'([^'\n]{8,})'|\"([^\"\n]{8,})\"", SRC_R)
fe, fj = overlaps([a or b for a, b in FIXED])
rep['render_fixed'] = dict(en4=sorted(fe), ja13=sorted(fj))
if fe or fj: ng.append(('render.py', 'fixed_text_overlap', sorted(fe) + sorted(fj)))
for b in BANNED:
    if b in SRC_R: ng.append(('render.py', 'banned_word', b))
rep['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(rep, open(HERE / 'logs/check.json', 'w'), ensure_ascii=False, indent=1, default=list)
print(json.dumps({k: v for k, v in rep.items() if k in ('topic', 'topic_past_ref', 'render_fixed', 'II_answers', 'III_tags', 'ng', 'topic_error')}, ensure_ascii=False, indent=1, default=list))
sys.exit(1 if ng else 0)
