"""取り込んだイラスト（assets/img/*.jpg）を問題データに差し込む。

- リスニング：('pics', …) の文字カードを本物の4枚組の絵に、('map', …) を見取り図の画像に置き換える
- リーディング：本番と同じく、チラシ・ウェブサイト・物語・スライドの中に図を入れる
画像は一度描いたら変えられないので、絵と台本が合わない所は台本（set*_l.py）の方を絵に合わせてある。
"""
from pathlib import Path

IMG = Path(__file__).resolve().parent / 'assets' / 'img'

# 4枚組の絵の下に入れる文字（座席番号・発車時刻など、絵だけでは区別できないもの）
CAPS = {
    (2, 11): ['12A', '12C', '21A', '21C'],
    (4, 11): ['10:20', '10:05', '10:35', '10:50'],
}

# 見取り図：①〜④を重ねる位置（画像の幅・高さに対する%）
MAP_MARKS = {   # (x%, y%, 半径%, 番号)：絵に描かれた空の丸の位置（画像解析で測った値）
    (1, 9): [(28.0, 41.1, 3.6, '①'), (72.0, 41.1, 3.6, '②'), (28.0, 71.1, 3.4, '③'), (72.0, 71.1, 3.4, '④')],
    (2, 9): [(18.5, 18.7, 3.2, '①'), (70.2, 19.2, 3.3, '②'), (13.0, 73.6, 3.0, '③'), (78.8, 73.4, 3.0, '④')],
    (3, 8): [(13.4, 22.3, 3.4, '①'), (61.9, 22.7, 3.5, '②'), (13.3, 76.6, 3.5, '③'), (61.9, 77.4, 3.5, '④')],
    (5, 9): [(30.2, 14.9, 2.7, '①'), (83.9, 15.2, 3.0, '②'), (18.6, 73.9, 2.7, '③'), (93.0, 75.9, 2.9, '④')],
}

# リーディング：(回, 大問, 何番目の資料(blocks の番号), 入れる位置, 画像, 幅mm)
#   位置 'after_title' = 枠の中の見出しの直後 / 'end' = 枠の中の最後 / 'after' = 枠の外・直後
R_PLACE = [
    (1, '第2問', 0, 'after_title', 'kyotsu_r1_2_cuploop_header', 120),
    (1, '第3問', 0, 'after_title', 'kyotsu_r1_3_jam_blog', 80),
    (1, '第5問', 0, 'after_title', 'kyotsu_r1_5_ranger_flyer', 112),
    (1, '第5問', 2, 'end', 'kyotsu_r1_5_ranger_map', 92),
    (1, '第6問', 0, 'after_title', 'kyotsu_r1_6_ruth_snow', 58),
    (1, '第6問', 0, 'end', 'kyotsu_r1_6_snow_chart', 100),
    (1, '第7問', 1, 'after', 'kyotsu_r1_7_sleep_brain', 62),
    (2, '第1問', 0, 'after_title', 'kyotsu_r2_1_foodnight_poster', 100),
    (2, '第2問', 0, 'after_title', 'kyotsu_r2_2_vocab_apps', 100),
    (2, '第3問', 0, 'after_title', 'kyotsu_r2_3_rugby_bottles', 62),
    (2, '第5問', 0, 'after_title', 'kyotsu_r2_5_lakeland_map', 92),
    (2, '第5問', 0, 'end', 'kyotsu_r2_5_coach_sizes', 100),
    (2, '第6問', 0, 'after_title', 'kyotsu_r2_6_fog_catcher', 96),
    (2, '第7問', 1, 'end', 'kyotsu_r2_7_anchoring_poster', 100),
    (3, '第2問', 0, 'after_title', 'kyotsu_r3_2_museum_lates', 100),
    (3, '第3問', 0, 'after_title', 'kyotsu_r3_3_bakery_photo', 88),
    (3, '第5問', 0, 'end', 'kyotsu_r3_5_festival_map', 100),
    (3, '第6問', 0, 'after_title', 'kyotsu_r3_6_gull_point', 62),
    (3, '第7問', 1, 'after', 'kyotsu_r3_7_microplastic_scale', 58),
    (4, '第1問', 0, 'after_title', 'kyotsu_r4_1_fridge_note', 50),
    (4, '第2問', 0, 'after_title', 'kyotsu_r4_2_refectory', 92),
    (4, '第3問', 0, 'after_title', 'kyotsu_r4_3_duck_race', 92),
    (4, '第6問', 0, 'after_title', 'kyotsu_r4_6_indigo_dye', 88),
    (4, '第7問', 1, 'after', 'kyotsu_r4_7_heat_island', 150),
    (5, '第2問', 0, 'after_title', 'kyotsu_r5_2_sunfold', 100),
    (5, '第3問', 0, 'after_title', 'kyotsu_r5_3_calligraphy', 84),
    (5, '第5問', 0, 'after_title', 'kyotsu_r5_5_green_futures', 42),
    (5, '第6問', 0, 'after_title', 'kyotsu_r5_6_feel_music', 100),
    (5, '第7問', 1, 'after', 'kyotsu_r5_7_habit_loop', 58),
]


def _img(name, width):
    assert (IMG / f'{name}.jpg').exists(), name
    return ('img', name, width)


def apply_listening(n, data):
    for p in data['parts']:
        for s in p['sections']:
            marks = [m for q in s['qs'] for m in q['marks']]
            for i, b in enumerate(s.get('blocks', [])):
                if b[0] == 'pics':
                    name = f'kyotsu_l{n}_q{marks[0]:02d}-{marks[-1]:02d}_pics'
                    s['blocks'][i] = ('img', name, 174, {'quad': True, 'cols': 4})
            for q in s['qs']:
                m0 = q['marks'][0]
                for i, b in enumerate(q.get('pre', [])):
                    if b[0] == 'pics':
                        name = f'kyotsu_l{n}_q{m0:02d}_pics'
                        q['pre'][i] = ('img', name, 174, {'quad': True, 'cols': 4, 'caps': CAPS.get((n, m0))})
                    elif b[0] == 'map':
                        name = f'kyotsu_l{n}_q{m0:02d}_map'
                        q['pre'][i] = ('img', name, 112, {'marks': MAP_MARKS[(n, m0)]})
    return data


def apply_reading(n, data):
    parts = {p['label']: p for p in data['parts']}
    for sn, label, bi, where, name, width in R_PLACE:
        if sn != n:
            continue
        blocks = parts[label]['sections'][0]['blocks']
        b = blocks[bi]
        fig = _img(name, width)
        if where == 'after':
            blocks.insert(bi + 1, fig)
            continue
        assert b[0] == 'box', (n, label, bi, b[0])
        inner = list(b[1])
        if where == 'end':
            inner.append(fig)
        else:
            k = next((i for i, x in enumerate(inner) if x[0] in ('title', 'h')), -1)
            while k + 1 < len(inner) and inner[k + 1][0] in ('small', 'c'):
                k += 1
            inner.insert(k + 1, fig)
        blocks[bi] = ('box', inner) + tuple(b[2:])
    return data
