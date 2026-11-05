# -*- coding: utf-8 -*-
"""茨城大 予想問題の検査（商用利用のため毎回実行）。
  python3 check.py r1 r2 r3   → logs/check.json（NG があれば終了コード 1）
 1) オリジナル性：過去問（茨城大の公式PDFのOCR・解答例）＋これまで作った大学の照合データと
    英語4語連続／日本語13字連続の一致、登場人物・地名の重複、禁止語。
 2) 設問の質：解説の英文引用（5語以上）が本文に実在するか。Ⅲの解答例が本文の丸写し（8語以上連続）でないか。
"""
import glob, importlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import render  # noqa: E402

REFS = [ROOT / '.tmpwork/ibaraki_ref'] + [Path(p) for p in glob.glob(str(ROOT / '.tmpwork/*_ref')) if 'ibaraki' not in p]
BANNED = ['的中', '必ず出る', '合格できる']
GENERIC = {('a', 'lot', 'of', 'time'), ('it', 'is', 'not', 'worth')}


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()


def words(t):
    return [w.lower() for w in re.findall(r"[A-Za-z]+(?:'[a-z]+)?", norm(t))]


def jchars(t):
    return re.sub(r'[^\u3040-\u30ff\u4e00-\u9fff]', '', t)


def collect(o, out):
    if isinstance(o, str):
        out.append(render.plain(o))
    elif isinstance(o, dict):
        for v in o.values():
            collect(v, out)
    elif isinstance(o, (list, tuple)):
        for v in o:
            collect(v, out)


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
    fixed = re.findall(r"[^'\"<>]*[\u3040-\u30ff\u4e00-\u9fff][^'\"<>]*", (HERE / 'render.py').read_text(encoding='utf-8'))
    e4, j13 = overlaps(fixed)
    if j13:
        ng.append(('render.py', 'ja13', list(j13)))
    for key in keys:
        R = importlib.import_module(key).ROUND
        for part in ('P1', 'P2', 'P3', 'P4'):
            texts = []
            collect(R[part], texts)
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
        # 解説の引用が本文にあるか（Ⅰ〜Ⅲ）
        for part in ('P1', 'P2', 'P3'):
            P = R[part]
            pool = norm(render.plain(' '.join(P['passage']))).lower()
            for q in P['questions']:
                for qt in re.findall(r'([A-Za-z][A-Za-z ,\'’\-]{12,}[A-Za-z])', q.get('expl', '')):
                    seg = norm(qt).lower().strip(' ,')
                    if len(seg.split()) >= 5 and seg not in pool:
                        ng.append((f'{key}-{part}', 'quote_not_in_passage', seg[:70]))
        # Ⅲ の解答例が本文の丸写しでないか（8語以上の連続一致）
        pw = words(' '.join(R['P3']['passage']))
        p8 = {tuple(pw[i:i + 8]) for i in range(len(pw) - 7)}
        for i, q in enumerate(R['P3']['questions'], 1):
            aw = words(q['answer'])
            if any(tuple(aw[j:j + 8]) in p8 for j in range(len(aw) - 7)):
                ng.append((f'{key}-P3', 'answer_copies_passage', i))
    out = HERE / 'logs'
    out.mkdir(exist_ok=True)
    (out / 'check.json').write_text(json.dumps({'report': rep, 'ng': ng}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'照合データ {len(SRC)} ページ。NG {len(ng)} 件')
    for x in ng:
        print('  NG', x)
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['r1']))
