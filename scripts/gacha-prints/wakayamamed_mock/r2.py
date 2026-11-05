# -*- coding: utf-8 -*-
from r2_p1 import P1
from r2_p1q import P1Q
from r2_p2 import P2
from r2_p2t import TR as P2T
from r2_p2q import P2Q
from r2_p3 import P3
from r2_p3t import TR as P3T
from r2_p3q import P3Q
from r2_p4 import P4

ROUND = {'n': 2, 'date': '2026年11月', 'P1': {**P1, **P1Q},
         'P2': {**P2, 'translation': P2T, **P2Q}, 'P3': {**P3, 'translation': P3T, **P3Q}, 'P4': P4}
