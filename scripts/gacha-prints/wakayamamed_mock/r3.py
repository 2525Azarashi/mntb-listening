# -*- coding: utf-8 -*-
from r3_p1 import P1
from r3_p1t import TR as P1T
from r3_p1q import P1Q
from r3_p2 import P2
from r3_p2t import TR as P2T
from r3_p2q import P2Q
from r3_p3 import P3
from r3_p3t import TR as P3T
from r3_p3q import P3Q
from r3_p4 import P4

ROUND = {'n': 3, 'date': '2026年11月', 'P1': {**P1, 'translation': P1T, **P1Q},
         'P2': {**P2, 'translation': P2T, **P2Q}, 'P3': {**P3, 'translation': P3T, **P3Q}, 'P4': P4}
