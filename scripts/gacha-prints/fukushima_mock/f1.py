# -*- coding: utf-8 -*-
import f1_1, f1_1q, f1_2, f1_4
DATA = {
    'points': {'1': 100, '2': 25, '3': 25, '4': 50},
    '1': {'paras': f1_1.PARAS, 'notes': f1_1.NOTES, 'translation': f1_1.TRANSLATION, 'questions': f1_1q.QUESTIONS, 'vocab': f1_1.VOCAB},
    '2': {'items': f1_2.DIALOGS},
    '3': {'items': f1_2.ORDERS},
    '4': f1_4.W,
    'names': [],
}
