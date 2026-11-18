"""normalized.json → src/data/egV3Items.generated.ts（アプリ用・統一形式）
統一形式（3つの納品のうち最も情報量の多い第8〜11章 v3 の形にそろえる）:
  【着眼点】→【ポイント】→ 選択肢ごとの ○／× の理由 →【プラス】
  和訳は「完成した英文」の枠に出す。元データに無い段は作らない（でっち上げない）。"""
import json, os, re, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from ja_gloss import POINT as JA_POINT, WHY as JA_WHY, KM as JA_KM   # 英語だけだった解説の日本語（手書き）
from exam_tips import tip_for                          # 【入試ではここ】（手書き・文法事項ごと）
from bespoke_composer import (
    compose_bespoke_hint,
    compose_bespoke_plus,
    compose_bespoke_point,
    enrich_choice_reason,
    find_english_cues,
)
JP = re.compile('[ぁ-んァ-ン一-龥]')
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
d = json.load(open(os.path.join(HERE, 'normalized.json')))
MARKS = ['①', '②', '③', '④']
def count_word(text, phrase):
    return len(re.findall(r'(?<![A-Za-z])' + re.escape(phrase) + r'(?![A-Za-z])', text, re.I))

def marked(r, ans):
    # 完成文に同じ語が2回出るとき（as … as など）は、空所の直後の語まで含めて1か所に絞る
    full = r['full']
    if count_word(full, ans) <= 1: return ans
    m = re.search(r'______\s*([A-Za-z\'’]+)', r['prompt'])
    if m and count_word(full, ans + ' ' + m.group(1)) == 1: return ans + ' ' + m.group(1)
    m = re.search(r'([A-Za-z\'’]+)\s*______', r['prompt'])
    if m and count_word(full, m.group(1) + ' ' + ans) == 1: return m.group(1) + ' ' + ans
    return ans

def around_blank(prompt):
    """空所の前後の語（各2語まで）。【着眼点】で「どこを見るか」を示す"""
    m = re.search(r'([^\s_]+\s+)?([^\s_]+\s+)?_{3,}(\s+[^\s_]+)?(\s+[^\s_]+)?', prompt)
    if not m: return ''
    before = ''.join(g for g in m.groups()[:2] if g).strip()
    after = ''.join(g for g in m.groups()[2:] if g).strip()
    return f"{before} ＿＿ {after}".strip()

def first_jp_sentence(*texts):
    for t in texts:
        if t and JP.search(t):
            return re.split(r'(?<=。)', t.strip())[0].strip()
    return ''

items = []
for r in d:
    key = f"{r['chapter']}-{r['no']}"
    ans = r['options'][r['answerIndex']]
    lines = []
    # ★2026-11-15 全1,163問 個別精緻化★
    #   機械的な「空所の前後『…』に注目」や公式名だけの【ポイント】・短絡的な選択肢理由を廃止し、
    #   その文の手がかり語（英語アンカー）・着眼点・具体根拠の要点・4択すべての理由・対比プラスを組み立てる。
    existing_exp_blob = ' '.join(
        str(x or '')
        for x in [
            r.get('hint'),
            JA_POINT.get(key),
            r.get('body'),
            r.get('point'),
            r['why'][r['answerIndex']],
            r.get('plus'),
        ]
    )
    cues = find_english_cues(r['prompt'], r['grammar'], existing_exp_blob, r['chapter'])
    hint_line = compose_bespoke_hint(r, cues)
    point, _resolved_cues = compose_bespoke_point(r, cues, JA_POINT.get(key))
    lines.append(f"【着眼点】{hint_line}")
    lines.append(f"【ポイント】{point}")
    lines.append('【選択肢】')
    for i, (o, w) in enumerate(zip(r['options'], r['why'])):
        ok = i == r['answerIndex']
        w = JA_WHY.get(f"{key}-{i}", w)
        w = enrich_choice_reason(r, i, w)
        lines.append(f"{MARKS[i]} {o}　{'○' if ok else '×'} {w}")
    tip, specific = tip_for(r['chapter'], r['grammar'] + ' ' + r['point'])
    plus_line = compose_bespoke_plus(r, tip if specific else '')
    if plus_line:
        lines.append(f"【プラス】{plus_line}")
    if tip and (specific or not plus_line):
        lines.append(f"【入試ではここ】{tip}")
    # 「押さえたい表現」に出す一言：12〜16章は一言ポイント、ほかは文法事項名（【ポイント】と重ねない）
    meaning = r['point'] if r['src'] == 'C' else r['grammar']
    if key in JA_KM: meaning = JA_KM[key]
    if not JP.search(meaning):
        # 英語の公式だけのときは日本語の意味を添える
        ja = first_jp_sentence(JA_POINT.get(key), r.get('body'), r['point'], r['why'][r['answerIndex']])
        if ja: meaning = ja if meaning in ja else f"{meaning}　{ja}"
    one_point = JA_POINT.get(key) or (r['point'] if JP.search(r['point']) else (JA_KM.get(key) or first_jp_sentence(r.get('body'), r['why'][r['answerIndex']]) or r['point']))
    theme = ''
    items.append(dict(c=r['chapter'], t=r['chapterTitle'], n=r['no'], g=r['grammar'], s=r['prompt'],
                      o=r['options'], a=r['answerIndex'], f=r['full'], tr=r['translation'],
                      k=marked(r, ans), km=meaning, th=theme, cm=lines, tl=r['timeLimit'], one=f"{ans}。{one_point}"[:140]))
out = os.path.join(ROOT, 'src/data/egV3Items.generated.ts')
with open(out, 'w') as fp:
    fp.write("/**\n * 英文法 第1〜20章 4択（全%d問）※自動生成・手で編集しないこと\n" % len(items))
    fp.write(" * 元データ: scripts/data/grammar_v3/normalized.json（normalize.py → build_ts.py）\n */\n")
    fp.write("export type EgV3Item = { c: number; t: string; n: number; g: string; s: string; o: [string, string, string, string]; a: 0 | 1 | 2 | 3; f: string; tr: string; k: string; km: string; th: string; cm: string[]; tl: number; one: string };\n")
    fp.write("export const EG_V3_ITEMS: readonly EgV3Item[] = JSON.parse(%s);\n" % json.dumps(json.dumps(items, ensure_ascii=False), ensure_ascii=False))
print('wrote', out, len(items))
