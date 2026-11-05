# -*- coding: utf-8 -*-
"""群馬大 予想問題の検査（商用利用のため毎回実行）。
  python3 check.py j1 j2 j3 r1 r2 r3   → logs/check.json（NG があれば終了コード 1）
  j＝情報学部（render_j.py）、r＝理工学部・医学部保健学科（render_r.py）
 1) オリジナル性：過去問（群馬大の公式PDFのOCR）・解答例＋これまで作った大学の照合データと
    英語4語連続／日本語13字連続の一致、登場人物・地名の重複、禁止語。
 2) 設問の質：解説の英文引用（5語以上）が本文・選択肢に実在するか。
"""
import glob, importlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

REFS = [ROOT / '.tmpwork/gunma_ref'] + [Path(p) for p in glob.glob(str(ROOT / '.tmpwork/*_ref')) if 'gunma' not in p]
BANNED = ['的中', '必ず出る', '合格できる']
GENERIC = {('a', 'lot', 'of', 'time'), ('it', 'is', 'not', 'worth')}


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()


def words(t):
    return [w.lower() for w in re.findall(r"[A-Za-z]+(?:'[a-z]+)?", norm(t))]


def jchars(t):
    return re.sub(r'[^\u3040-\u30ff\u4e00-\u9fff]', '', t)


def collect(o, out, plain):
    if isinstance(o, str):
        out.append(plain(o))
    elif isinstance(o, dict):
        for v in o.values():
            collect(v, out, plain)
    elif isinstance(o, (list, tuple)):
        for v in o:
            collect(v, out, plain)


SRC = {}
for d in REFS:
    for f in glob.glob(str(d / 'ocr/*.txt')):
        SRC[f'{d.name}/{Path(f).stem}'] = open(f, errors='ignore').read()
ALLSRC = '\n'.join(SRC.values())
EN4, JA13 = {}, {}
for k, t in SRC.items():
    w = words(t)
    for i in range(len(w) - 3):
        EN4.setdefault(tuple(w[i:i + 4]), set()).add(k)
    j = jchars(t)
    for i in range(len(j) - 12):
        JA13.setdefault(j[i:i + 13], set()).add(k)


def overlaps(texts):
    e4, j13 = {}, {}
    for x in texts:
        w = words(x)
        for i in range(len(w) - 3):
            g = tuple(w[i:i + 4])
            if g in EN4 and g not in GENERIC and not all(len(y) <= 2 for y in g):
                e4[' '.join(g)] = sorted(EN4[g])[:3]
        j = jchars(x)
        for i in range(len(j) - 12):
            if j[i:i + 13] in JA13:
                j13[j[i:i + 13]] = sorted(JA13[j[i:i + 13]])[:3]
    return e4, j13


def main(keys):
    rep, ng = {'refs': len(SRC)}, []
    for rf in sorted(HERE.glob('render_*.py')):
        fixed = re.findall(r"[^'\"<>]*[\u3040-\u30ff\u4e00-\u9fff][^'\"<>]*", rf.read_text(encoding='utf-8'))
        _, j13 = overlaps(fixed)
        if j13:
            ng.append((rf.name, 'ja13', list(j13)))
    for key in keys:
        rmod = importlib.import_module('render_j' if key.startswith('j') else 'render_r')
        R = importlib.import_module(key).ROUND
        parts = [p for p in ('P1', 'P2', 'P3', 'P4') if p in R]
        for part in parts:
            texts = []
            collect(R[part], texts, rmod.plain)
            e4, j13 = overlaps(texts)
            rep[f'{key}-{part}'] = {'en4': e4, 'ja13': j13}
            if e4:
                ng.append((f'{key}-{part}', 'en4', list(e4)))
            if j13:
                ng.append((f'{key}-{part}', 'ja13', list(j13)))
            for b in BANNED:
                if any(b in t for t in texts):
                    ng.append((f'{key}-{part}', 'banned', b))
        for nm in R.get('names', []):
            if re.search(r'\b' + re.escape(nm) + r'\b', ALLSRC):
                ng.append((key, 'name_in_past', nm))
        for part in parts:
            P = R[part]
            if 'passage' not in P or 'questions' not in P:
                continue
            pool = norm(rmod.plain(' '.join(P['passage']))).lower()
            for q in P['questions']:
                extra = [norm(rmod.plain(str(o))).lower() for o in q.get('options', []) + q.get('statements', [])]
                for qt in re.findall(r"([A-Za-z][A-Za-z ,'’\-]{12,}[A-Za-z])", q.get('expl', '')):
                    seg = norm(qt).lower().strip(' ,')
                    if len(seg.split()) >= 5 and seg not in pool and not any(seg in o for o in extra):
                        ng.append((f'{key}-{part}', 'quote_not_in_passage', seg[:70]))
    out = HERE / 'logs'
    out.mkdir(exist_ok=True)
    (out / 'check.json').write_text(json.dumps({'report': rep, 'ng': ng}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'照合データ {len(SRC)} ページ。NG {len(ng)} 件')
    for x in ng:
        print('  NG', x)
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['j1']))
