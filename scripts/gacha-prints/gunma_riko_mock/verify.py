# -*- coding: utf-8 -*-
"""群馬大 予想問題の難易度・形式チェック。 python3 verify.py N → logs/verify_rN.json（NG があれば終了コード1）
基準：2024〜2026年度 前期日程「英語」（理工学部。2026年度は医学部保健学科と同じ冊子）の公式PDFと解答例。
  第1問 A 語句の選択10・B 誤りの指摘10・C 会話の空所10（4場面）。各文は8〜30語程度。
  第2問 A・B 読解各5問（英語の問い・最後は表題）。公開されている2026年度の本文は A 447語（平均文長15.4・難語率5.1%）・B 549語（20.3・6.4%）
    → 1本 400〜600語・平均文長 13〜22語・難語率 3〜9%。
  第3問 A・B 書き出しの文字つきの語の完成 各10（本文は非公開。解答の語は falls・money・dangerous・gradually など日常語）
    → 本文 220〜420語・平均文長 10〜20語，空所の語は wordfreq zipf 3.5 以上。
"""
import sys, re, json, importlib
from pathlib import Path
from wordfreq import zipf_frequency as z
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import render
sys.path.insert(0, str(HERE))
R = sys.argv[1] if len(sys.argv) > 1 else '1'
D = importlib.import_module(f'g{R}').DATA

def wc(x): return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", x))
def stats(t):
    t = t.replace('’', "'")
    S = [x for x in re.split(r'(?<=[.?!])["”’]?\s+(?=[A-Z“"])', t) if wc(x) > 2]
    toks = [w.lower() for w in re.findall(r'[A-Za-z]+', t) if len(w) > 1]
    caps = set(w.lower() for w in re.findall(r"(?<![.?!]\s)\b[A-Z][a-z]+", t))
    cont = [w for w in toks if w not in caps and z(w, 'en') > 0]
    return dict(words=wc(t), avg=round(wc(t) / max(1, len(S)), 1),
                zipf_lt4=round(sum(z(w, 'en') < 4 for w in cont) / max(1, len(cont)) * 100, 1))
RANGE = {'2': dict(words=(400, 600), avg=(13, 22), zipf_lt4=(3, 9)),
         '3': dict(words=(220, 420), avg=(10, 20), zipf_lt4=(1, 9))}
log, ng = {}, []
for k in ('2A', '2B', '3A', '3B'):
    P = D[k]
    d = stats(' '.join(render.plain(p) for p in P['paras'])); d['paras'] = len(P['paras'])
    d['range'] = {m: f'{lo}–{hi}:' + ('OK' if lo <= d[m] <= hi else 'NG') for m, (lo, hi) in RANGE[k[0]].items()}
    log[k] = d
    if any('NG' in v for v in d['range'].values()): ng.append((k, 'passage'))
for k in ('3A', '3B'):
    zs = {a + b: round(z((a + b).lower(), 'en'), 2) for a, b in render.gaps(D[k])}
    log[k + '-gapwords'] = zs
    for w, s in zs.items():
        if s < 3.5: ng.append((k, 'rare_gap_word', w, s))
for i, q in enumerate(D['A'], 1):
    n = wc(q['stem'].replace('[[]]', q['choices'][q['answer']]))
    if not 7 <= n <= 30: ng.append(('A', i, 'len', n))
for i, q in enumerate(D['B'], 1):
    n = wc(render.b_fixed(q))
    if not 8 <= n <= 30: ng.append(('B', i, 'len', n))
for i, c in enumerate(D['C'], 1):
    if not 6 <= len(c['lines']) <= 13: ng.append(('C', i, 'lines', len(c['lines'])))
log['ng'] = ng
(HERE / 'logs').mkdir(exist_ok=True)
json.dump(log, open(HERE / f'logs/verify_r{R}.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(log, ensure_ascii=False, indent=1)); sys.exit(1 if ng else 0)
