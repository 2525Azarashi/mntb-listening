# 島根大学 前期 英語 予想問題 第1回（法文・人間科学・総合理工・生物資源科学部用：1・2・4）
import importlib.util, pathlib
_d = pathlib.Path(__file__).resolve().parent.parent / 'shimane'
def _load(name):
    spec = importlib.util.spec_from_file_location(name, _d / f'{name}.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
R = {'no': 1, 'sections': [_load('r1_s1').S, _load('r1_s2').S, _load('r1_s45').S4]}
