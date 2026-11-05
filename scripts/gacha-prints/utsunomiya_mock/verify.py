# -*- coding: utf-8 -*-
"""宇都宮大 予想問題の難易度・形式チェック。 python3 verify.py N → logs/verify_rN.json（NG があれば終了コード1）
基準：2024〜2026年度（R6〜R8）前期日程「英語」の公式PDF（データサイエンス経営・国際・工・農の共通問題冊子。画像PDFを OCR）と解答例・出題の意図。
  第1問・第2問の英文は著作権のため非公開（出典と注・設問のみ公開）。紙面は各2.5〜3ページ分 → 1本 550〜900語と推定。
  第1問は論説文（3年とも言語・ことばの話題），第2問は物語文。設問は各8〜9問：記号選択（語義・空所・言い換え）・下線部和訳・
  日本語での説明（字数指定つきのこともある）・〇×の内容一致（4〜6文）。
  第3問は短い英文（調査結果など）と問いを読み，約150語で意見を書く → 解答例 130〜170語。第4問は会話文2つ×空所4つ。
"""
import sys, re, json, importlib
from pathlib import Path
from wordfreq import zipf_frequency as z
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
R = sys.argv[1] if len(sys.argv) > 1 else '1'
D = importlib.import_module(f'u{R}').DATA

def wc(x): return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", x))
def stats(t):
    t = t.replace('’', "'")
    S = [x for x in re.split(r'(?<=[.?!])["”’]?\s+(?=[A-Z“"])', t) if wc(x) > 2]
    toks = [w.lower() for w in re.findall(r'[A-Za-z]+', t) if len(w) > 1]
    caps = set(w.lower() for w in re.findall(r"(?<![.?!]\s)\b[A-Z][a-z]+", t))
    cont = [w for w in toks if w not in caps and z(w, 'en') > 0]
    return dict(words=wc(t), avg=round(wc(t) / max(1, len(S)), 1),
                zipf_lt4=round(sum(z(w, 'en') < 4 for w in cont) / max(1, len(cont)) * 100, 1))
RANGE = {'1': dict(words=(550, 900), avg=(14, 25), zipf_lt4=(3, 12)),
         '2': dict(words=(550, 900), avg=(9, 20), zipf_lt4=(2, 12))}

log, ng = {}, []
for n in ('1', '2'):
    P = D[n]
    d = stats(render.filled(P)); d['paras'] = len(P['paras'])
    d['range'] = {m: f'{lo}–{hi}:' + ('OK' if lo <= d[m] <= hi else 'NG') for m, (lo, hi) in RANGE[n].items()}
    log[n] = d
    if any('NG' in v for v in d['range'].values()): ng.append((n, 'passage'))
    k = len(P['questions']); log[f'{n}-questions'] = k
    if not 7 <= k <= 9: ng.append((n, 'question_count', k))
    kinds = {q['kind'] for q in P['questions']}
    if not {'mc', 'tf', 'trans', 'jp'} <= kinds: ng.append((n, 'kinds', sorted(kinds)))
    if P['questions'][-1]['kind'] != 'tf': ng.append((n, 'tf_last'))
    for i, q in enumerate(P['questions'], 1):
        if q['kind'] == 'trans':
            for a in [q['answer']] + q.get('alts', []):
                if not 20 <= len(a) <= 120: ng.append((n, i, 'trans_len', len(a)))
        if q['kind'] == 'tf' and not 4 <= len(q['statements']) <= 6: ng.append((n, i, 'tf_count'))
ws = [wc(m) for _, m in D['3']['models']]
log['3-models'] = dict(words=ws, range='130〜170語')
for w in ws:
    if not 130 <= w <= 170: ng.append(('3', 'model_words', w))
log['3-passage_words'] = wc(D['3']['passage'])
if not 60 <= log['3-passage_words'] <= 160: ng.append(('3', 'passage_words', log['3-passage_words']))
for c in D['4']['convs']:
    for a in c['answers']:
        if not 3 <= wc(a) <= 22: ng.append(('4', c['label'], 'answer_len', wc(a)))
log['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(log, open(HERE / f'logs/verify_r{R}.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(log, ensure_ascii=False, indent=1)); sys.exit(1 if ng else 0)
