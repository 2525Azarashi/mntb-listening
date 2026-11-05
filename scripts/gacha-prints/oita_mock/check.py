# -*- coding: utf-8 -*-
"""大分大学 予想問題の検査（商用利用のため毎回実行）。 python3 check.py [1 2 3]
 1) オリジナル性：過去問（R7・R8 公式PDFのOCR・解答例）と英語5語連続／日本語12字連続の一致 = 0 件。
    照合先は環境変数 OITA_REF（既定 ~/.cache_kk/kk/oita）の *.txt。リポジトリには入れない。render.py の固定文言も照合。
 2) 禁止語（的中・必ず出る・合格できる）。
NG があれば終了コード1。
"""
import glob, importlib, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render

REF = Path(os.environ.get('OITA_REF', Path.home() / '.cache_kk/kk/oita'))
BANNED = ['的中', '必ず出る', '合格できる']


def norm(t):
    return t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')


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


def main():
    files = sorted(glob.glob(str(REF / '*.txt')))
    assert files, f'照合先がない: {REF}'
    EN, JA = {}, {}
    for f in files:
        t = open(f, errors='ignore').read()
        w = words(t)
        for i in range(len(w) - 4):
            EN.setdefault(tuple(w[i:i + 5]), Path(f).name)
        j = jchars(t)
        for i in range(len(j) - 11):
            JA.setdefault(j[i:i + 12], Path(f).name)
    rounds = [int(x) for x in sys.argv[1:]] or [1, 2, 3]
    ng = []
    targets = {f'r{n}': importlib.import_module(f'r{n}').ROUND for n in rounds}
    fixed = [render.DISCLAIMER] + [s for s in re.findall(r"'([^'\n]{12,})'", (HERE / 'render.py').read_text(encoding='utf-8'))]
    targets['render.py'] = fixed
    for tag, obj in targets.items():
        texts = []
        collect(obj, texts)
        for x in texts:
            for b in BANNED:
                if b in x:
                    ng.append((tag, '禁止語', b))
            w = words(x)
            for i in range(len(w) - 4):
                g = tuple(w[i:i + 5])
                if g in EN:
                    ng.append((tag, '英5語', ' '.join(g), EN[g]))
            j = jchars(x)
            for i in range(len(j) - 11):
                if j[i:i + 12] in JA:
                    ng.append((tag, '日12字', j[i:i + 12], JA[j[i:i + 12]]))
    seen = set()
    for x in ng:
        if x not in seen:
            seen.add(x)
            print('NG', *x)
    print(f'照合先 {len(files)} ファイル / 対象 {", ".join(targets)} / NG {len(seen)} 件')
    sys.exit(1 if seen else 0)


if __name__ == '__main__':
    main()
