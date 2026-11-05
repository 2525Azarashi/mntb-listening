# 長崎大学 前期 英語 予想問題 第1回（A・B・C）
import importlib.util, pathlib
_d = pathlib.Path(__file__).resolve().parent.parent / 'nagasaki'
def _load(name):
    spec = importlib.util.spec_from_file_location(name, _d / f'{name}.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
R = {'no': 1, 'sections': [_load('r1_a').S, _load('r1_b').S, _load('r1_cd').SC]}
