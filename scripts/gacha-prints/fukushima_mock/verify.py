# -*- coding: utf-8 -*-
"""福島大 予想問題の難易度・形式チェック。 python3 verify.py N → logs/verify_rN.json（NG があれば終了コード1）
基準：2024〜2026年度（R6〜R8）経済経営学類 前期日程「英語」の公式PDF（画像PDFを OCR。R7 は長文本文が著作権のため非公開）。
  試験時間 70分・大問4つ（Ⅰ 長文＋日本語で答える設問6つ〔うち下線部和訳1〜2〕／Ⅱ 対話文の空所に英単語1語×5／
  Ⅲ 6語句の並べかえ×5／Ⅳ 2つの問いから1つを選んで100語程度の英作文）。3年とも同じ構成。
  Ⅰの本文：R6 約380語・R8 約320語（OCR で数えた値），平均文長 20〜23語，難語率（zipf<4）3〜7% → 280〜420語・14〜25語・2〜10%。
  Ⅳの解答例：「100語程度」→ 90〜120語。和訳の解答例は 20〜120字，日本語で説明する設問の解答例は 15〜120字。
"""
import sys, re, json, importlib
from pathlib import Path
from wordfreq import zipf_frequency as z
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
R = sys.argv[1] if len(sys.argv) > 1 else '1'
D = importlib.import_module(f'f{R}').DATA

def wc(x): return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", x))
def stats(t):
    t = t.replace('’', "'")
    S = [x for x in re.split(r'(?<=[.?!])["”’]?\s+(?=[A-Z“"])', t) if wc(x) > 2]
    toks = [w.lower() for w in re.findall(r'[A-Za-z]+', t) if len(w) > 1]
    caps = set(w.lower() for w in re.findall(r"(?<![.?!]\s)\b[A-Z][a-z]+", t))
    cont = [w for w in toks if w not in caps and z(w, 'en') > 0]
    return dict(words=wc(t), avg=round(wc(t) / max(1, len(S)), 1),
                zipf_lt4=round(sum(z(w, 'en') < 4 for w in cont) / max(1, len(cont)) * 100, 1))
RANGE = dict(words=(280, 420), avg=(14, 25), zipf_lt4=(2, 10))

log, ng = {}, []
d = stats(render.filled(D)); d['paras'] = len(D['1']['paras'])
d['range'] = {m: f'{lo}–{hi}:' + ('OK' if lo <= d[m] <= hi else 'NG') for m, (lo, hi) in RANGE.items()}
log['I'] = d
if any('NG' in v for v in d['range'].values()): ng.append(('I', 'passage'))
nt = sum(q['kind'] == 'trans' for q in D['1']['questions'])
log['I-trans'] = nt
if not 1 <= nt <= 2: ng.append(('I', 'trans_count', nt))
for i, q in enumerate(D['1']['questions'], 1):
    lo, hi = (20, 120) if q['kind'] == 'trans' else (15, 120)
    for a in [q['answer']] + q.get('alts', []):
        if not lo <= len(a) <= hi: ng.append(('I', i, 'answer_len', len(a)))
for i, it in enumerate(D['3']['items'], 1):
    full = f'{it["pre"]} {it["answer"]} {it["post"]}'
    log[f'III-{i}'] = wc(full)
    if not 7 <= wc(full) <= 20: ng.append(('III', i, 'sentence_len', wc(full)))
ws = [wc(m) for _, m in D['4']['models']]
log['IV-models'] = dict(words=ws, range='90〜120語')
for w in ws:
    if not 90 <= w <= 120: ng.append(('IV', 'model_words', w))
log['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(log, open(HERE / f'logs/verify_r{R}.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(log, ensure_ascii=False, indent=1)); sys.exit(1 if ng else 0)
