"""英文法 全20章（1,163問）を1問ずつ解析し、文中の手がかり語・着眼点・要点・4択すべての正誤理由・プラス補足を精緻化するモジュール。

設計原則：
  1. 機械的な「空所の前後『…』に注目」や単調なテンプレ文言を全廃し、章・構文ごとの着眼点（どこを見て何を判定するか）をネタバレなしで記述する。
  2. 【ポイント】（＝カード直下の『要点』）が公式名だけで終わっていた問をすべて解消し、
     問題文中の実際の手がかり語（マーカー ¹ ²）と正解に至る文法根拠を自然な日本語で結ぶ。
  3. 4択（全4,652肢）の短い断片的な理由を、実際の選択肢語句・空所前後の支配語・正解肢との対比を含んだ具体的な説明（全肢16文字以上）へ引き上げる。
  4. 第12〜17章で空欄だった372問すべてに、混同しやすい対比表現・ひっかけ回避の【プラス】を付与する。
"""
from __future__ import annotations
import re
from typing import List, Optional, Tuple

STOPWORDS = {
    'the', 'a', 'an', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
    'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'this',
    'that', 'these', 'those', 'is', 'am', 'are', 'was', 'were', 'be', 'been',
    'do', 'does', 'did', 'have', 'has', 'had', 'will', 'would', 'can', 'could',
    'to', 'of', 'in', 'on', 'at', 'for', 'with', 'by', 'from', 'as', 'and',
    'but', 'or', 'so', 'very', 'really', 'just', 'too', 'also', 'well', 'oh',
    'yes', 'no', 'ok', 'mr', 'ms', 'mrs', 'dr', 'ken', 'tom', 'bob', 'mary',
    'jane', 'john', 'mike', 'emma', 'linda', 'robert', 'jack', 'smith', 'brown',
    'sato', 'yamada', 'tokyo', 'japan', 'kyoto', 'london', 'australia', 'some',
    'any', 'all', 'many', 'much', 'more', 'most', 'other', 'new', 'old', 'good',
    'hello', 'hi', 'hey', "i'm", "he's", "she's", "it's", "we're", "you're",
    "they're", "there's", "that's", "what's", "who's", "let's", "don't",
    "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't", "won't",
    "can't", "couldn't", "i'll", "i'd", "i've", "you'll", "you'd", "you've",
    "he'll", "he'd", "she'll", "she'd", "we'll", "they'll",
}

EDGE_TRIMS = {'the', 'a', 'an', 'to', 'of', 'in', 'on', 'at', 'for', 'and', 'or', 'but'}

TIME_CUES = [
    'every morning', 'every day', 'every night', 'every week', 'every summer', 'every year',
    'this time tomorrow', 'this time next week', 'at nine tonight', 'next weekend', 'next week',
    'next month', 'next year', 'next Sunday', 'next Monday', 'in ten minutes', 'in a few days',
    'last Sunday', 'last night', 'last week', 'last month', 'last year', 'yesterday',
    'two days ago', 'three years ago', 'five years ago', 'ten years ago', 'a few minutes ago',
    'just now', 'at that time', 'at seven last night', 'when the phone rang', 'when I arrived',
    'by the time', 'as soon as', 'since last', 'since I was', 'since then', 'for ten years',
    'for five years', 'for three hours', 'for two hours', 'for a long time', 'for months',
    'lately', 'recently', 'already', 'yet', 'tonight', 'tomorrow', 'ago', 'since', 'while',
]

GOV_PATTERNS = [
    r'How do you do\??', r'Nice to meet you', r'Would you like', r'Shall I', r'Shall we',
    r'Why don\'t we', r'Why don\'t you', r'Would you mind', r'Do you mind',
    r'cannot help', r"can't help", r"couldn't help",
    r'look forward to', r'looking forward to', r'looked forward to',
    r'am used to', r'is used to', r'are used to', r'was used to', r'get used to', r'used to',
    r'object to', r'when it comes to', r'What do you say to', r'How about', r'What about',
    r'no use', r'no sense in', r'no point in', r'worth', r'feel like', r'have trouble',
    r'have difficulty', r'had difficulty', r'had trouble', r'busy',
    r'prevent [A-Za-z]+ from', r'keep [A-Za-z]+ from', r'stop [A-Za-z]+ from',
    r'prohibit [A-Za-z]+ from', r'discourage [A-Za-z]+ from',
    r'remind [A-Za-z]+', r'inform [A-Za-z]+', r'warn [A-Za-z]+', r'convince [A-Za-z]+',
    r'rob [A-Za-z]+', r'deprive [A-Za-z]+', r'provide [A-Za-z]+', r'supply [A-Za-z]+',
    r'blame [A-Za-z]+', r'thank [A-Za-z]+', r'praise [A-Za-z]+',
    r'apologize', r'graduate', r'marry', r'discuss', r'reach', r'enter', r'approach', r'resemble',
    r'suggest', r'suggested', r'insist', r'insisted', r'demand', r'demanded', r'recommend', r'recommended',
    r'made [A-Za-z]+', r'make [A-Za-z]+', r"won't let [A-Za-z]+", r'let [A-Za-z]+',
    r'saw (?:a |the )?[A-Za-z]+', r'see (?:a |the )?[A-Za-z]+',
    r'heard (?:a |the )?[A-Za-z]+', r'hear (?:a |the )?[A-Za-z]+',
    r'watched (?:a |the )?[A-Za-z]+', r'watch (?:a |the )?[A-Za-z]+',
    r'felt (?:a |the )?[A-Za-z]+', r'noticed (?:a |the )?[A-Za-z]+',
    r'wish', r'If only', r'as if', r'as though', r"It's time", r'It is time', r'It is high time',
    r'would rather', r'had better', r'ought to', r'need not', r'dare not',
    r'without', r'instead of', r'in spite of', r'despite', r'because of', r'due to', r'owing to',
    r'good at', r'interested in', r'fond of', r'proud of', r'tired of', r'afraid of', r'ashamed of',
    r'capable of', r'aware of', r'full of', r'filled with', r'satisfied with', r'pleased with',
    r'surprised at', r'known to', r'known for', r'known as', r'made of', r'made from',
    r'caught', r'engaged in', r'absorbed in', r'dressed in',
]

PREPOSITIONS = {
    'in', 'on', 'at', 'by', 'with', 'for', 'from', 'of', 'to', 'into', 'out',
    'over', 'under', 'through', 'between', 'among', 'during', 'until', 'till',
    'without', 'about', 'against', 'across', 'along', 'around', 'behind', 'beyond',
}

CHAPTER_LENS = {
    1: '時を表す副詞句や時・条件の節から「いつの動作・状態か（現在・過去・進行・完了）」を見極める',
    2: '主語が動作を「する側（能動）」か「される側（受動）」かと、時制・前置詞の結びつきを確かめる',
    3: '発話の場面（推量・義務・必要・過去の推量や後悔助動詞＋have p.p.）に合う助動詞を選ぶ',
    4: '事実と反対の仮定か単なる条件かを見分け、いつの仮定か（仮定法過去／仮定法過去完了）で時制を揃える',
    5: '空所が文中で担う働き（名詞・形容詞・副詞用法、または SVOC の補語・意味上の主語）を確認する',
    6: '直前の動詞・前置詞・慣用表現が「動名詞（doing）」と「不定詞（to do）」のどちらを要求するかを判定する',
    7: '修飾される名詞や主語と分詞の意味関係が「〜している（能動→現在分詞）」か「〜される（受動→過去分詞）」かを判断する',
    8: '比較の標識（as … as / 比較級＋than / 最上級＋in, of / 倍数表現）と形容詞・副詞の級を対応させる',
    9: '指している名詞が「特定のその物（it / they）」か「不特定の同種（one / ones）」か、単複とあわせて確認する',
    10: '先行詞の種類（人・物・時・場所）と、空所に続く節の中で主語・目的語が欠けているか完全な文かを点検する',
    11: '前後の節の論理関係（逆接・原因結果・譲歩・時・条件）と、空所の後ろが「SV の節」か「名詞句」かを見分ける',
    12: '空所直後の名詞の性質（時刻・日付・期間・手段・材料など）や直前の動詞・形容詞とのコロケーションを確認する',
    13: '修飾語句に惑わされず「主語の核」が単数扱い・複数扱いのどちらになるかを見極めて動詞の形を一致させる',
    14: '直接疑問文か間接疑問文（疑問詞＋S＋V）か、または否定語・So などの文頭配置による倒置の有無を確認する',
    15: 'not と all / every / both などの組み合わせ（部分否定）か全体否定か、強調構文の型かを整理する',
    16: '伝達動詞の種類（平叙・疑問・命令・提案）に応じて、接続詞・語順・人称・時制の一致・副詞の変化を点検する',
    17: '動詞が他動詞（前置詞不要）か自動詞か、また目的語・補語にどの形（to do / doing / 原形 / that節）をとるかを確認する',
    18: '修飾する名詞が「可算（複数）」か「不可算」かと、肯定・否定のニュアンス（a few / few / a little / little 等）を確かめる',
    19: '名詞自体の可算・不可算の性質や、文脈が求める語義・語法（熟語の組み合わせ）を見極める',
    20: '相手の発言の意図（初対面のあいさつ・依頼・申し出・許可・謝罪など）をつかみ、場面に合う応答表現を選ぶ',
}


def strip_jp_header(prompt: str) -> Tuple[str, str]:
    m = re.match(r'^(【並べかえ】「[^」]+」)\s*(.*)$', prompt.strip(), re.S)
    if m:
        return m.group(1), m.group(2).strip()
    return '', prompt.strip()


def split_blank(eng: str) -> Tuple[str, str]:
    parts = eng.split('______', 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return eng, ''


def last_words(text: str, n: int = 3) -> str:
    words = re.findall(r"[A-Za-z0-9']+", text)
    return ' '.join(words[-n:]) if words else ''


def first_words(text: str, n: int = 3) -> str:
    words = re.findall(r"[A-Za-z0-9']+", text)
    return ' '.join(words[:n]) if words else ''


def clean_candidate_phrase(raw: str) -> str:
    ph = ' '.join(raw.split()).strip(" ,.;:()[]")
    words = ph.split()
    while len(words) > 1 and words[-1].lower().rstrip('?.!') in EDGE_TRIMS:
        words.pop()
    while len(words) > 1 and words[0].lower() in {'and', 'or', 'but', 'hello.', 'hi.', 'hi,'}:
        words.pop(0)
    return ' '.join(words)


def clean_formula_label(label: str) -> str:
    """二重カギ括弧にならないよう公式見出し内の『…』を（…）に整える。"""
    s = (label or '').strip().replace('___', '空所')
    s = re.sub(r'「([^」]+)」', r'（\1）', s)
    return s


def clean_theme_no_spoiler(grammar: str, options: List[str]) -> str:
    """着眼点（hint）で正解の英単語を直接ネタバレしないよう括弧内の英語例や公式の答え部分を整理する。"""
    s = (grammar or '').strip()
    # 括弧内に英語が含まれる場合は括弧ごと除去（例：あいさつ (How do you do?) → あいさつ）
    s = re.sub(r'[（(][^）)]*[A-Za-z][^）)]*[）)]', '', s)
    # 「A＝B」「〜「意味」」のような公式文字列に正解そのものが露出している場合は日本語テーマ側を優先
    for opt in options:
        ow = opt.strip().rstrip('.?!')
        if len(ow) >= 3 and re.search(r'(?<![A-Za-z])' + re.escape(ow) + r'(?![A-Za-z])', s, re.I):
            return ''
    s = re.sub(r'「[^」]*」', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' ・／/+-＋＝=')
    if re.search(r'[A-Za-z]{3,}', s) and len(s) > 18:
        return ''
    return s


def _is_trivial_greeting_sentence(sent: str) -> bool:
    low = sent.strip().lower().rstrip('.!')
    if low in ('hello', 'hi', 'hey', 'excuse me', 'pardon me'):
        return True
    if re.match(r"^(?:hello[.!,]?\s*)?(?:i'm|i am|my name is|this is)\s+[a-z .]+$", low) and 'friend' not in low:
        return True
    return False


def find_english_cues(prompt: str, grammar: str, existing_text: str, chapter: int) -> List[str]:
    """英文 prompt（空所 ______ の外）から、正答の決め手となる英語表現を最大2つ抽出する。"""
    _, eng = strip_jp_header(prompt)
    before, after = split_blank(eng)
    candidates: List[str] = []

    # 1) (a)/(b) 書き換え・A = B 書き換えの場合：前半文の核心表現を最優先
    ab_match = re.match(r'^\(a\)\s*(.+?)\n\(b\)\s*(.+)$', eng, re.S)
    if ab_match:
        a_sent = ab_match.group(1).strip().rstrip('.')
        b_before, b_after = split_blank(ab_match.group(2))
        b_words = set(re.findall(r"[A-Za-z']+", (b_before + ' ' + b_after).lower()))
        diff_words = [w for w in re.findall(r"[A-Za-z']+", a_sent) if w.lower() not in b_words]
        if diff_words:
            diff_join = ' '.join(diff_words[:4])
            if diff_join in a_sent:
                candidates.append(diff_join)

    if '=' in before:
        left_side = before.split('=', 1)[0].strip().strip('“”"')
        lw = first_words(left_side, 4)
        if lw and lw in before:
            candidates.append(lw)

    # 2) 会話文の場合：空所を含まない相手発話の核心文（単なる Hello. / I'm Sato. は除外して後ろの疑問文等を優先）
    quotes = re.findall(r'[“"]([^”"]+)[”"]', eng)
    if len(quotes) >= 2:
        for q in quotes:
            if '______' not in q:
                sents = [s.strip() for s in re.split(r'(?<=[.?!])\s+', q.strip()) if s.strip()]
                meaningful = [s for s in sents if not _is_trivial_greeting_sentence(s)]
                target_sents = meaningful if meaningful else sents
                key_sent = target_sents[-1] if target_sents else q.strip()
                key_clean = key_sent.rstrip('.')
                if 3 <= len(key_clean) <= 40 and (key_clean in before or key_clean in after):
                    candidates.append(key_clean)
            else:
                # 同じ発話内に空所以外の決め手文がある場合（例："______ I'm late." 等）
                q_before, q_after = split_blank(q)
                for part in (q_before.strip(), q_after.strip()):
                    part_clean = part.strip(' ,').rstrip('.')
                    if 4 <= len(part_clean) <= 32 and not _is_trivial_greeting_sentence(part_clean):
                        if part_clean in before or part_clean in after:
                            candidates.append(part_clean)

    # 3) 支配語パターン（How do you do, Would you mind, without, saw a boy 等）
    for pat in GOV_PATTERNS:
        for seg in (before, after):
            m = re.search(r'(?<![A-Za-z])(' + pat + r')(?![A-Za-z])', seg)
            if not m:
                m = re.search(r'(?<![A-Za-z])(' + pat + r')(?![A-Za-z])', seg, re.I)
            if m:
                candidates.append(clean_candidate_phrase(m.group(1)))

    # 4) 時制・仮定法・助動詞では時・条件の手がかり語を優先
    if chapter in (1, 2, 3, 4, 11, 12, 16):
        for tc in TIME_CUES:
            for seg in (before, after):
                m = re.search(r'(?<![A-Za-z])(' + re.escape(tc) + r')(?![A-Za-z])', seg, re.I)
                if m:
                    candidates.append(m.group(1))

    # 5) 既存解説（hint / point / body / why）の中に明示されている英語フレーズで prompt にもあるもの
    eng_in_exp = re.findall(r"[A-Za-z][A-Za-z0-9'’\-\s]{1,26}[A-Za-z0-9?]", existing_text)
    for raw in eng_in_exp:
        ph = clean_candidate_phrase(raw)
        if len(ph) < 3 or ph.lower().rstrip('?.!') in STOPWORDS:
            continue
        if ph in before or ph in after:
            candidates.append(ph)

    single_in_exp = re.findall(r"(?<![A-Za-z])[A-Za-z']{3,18}(?![A-Za-z])", existing_text)
    for w in single_in_exp:
        if w.lower() in STOPWORDS:
            continue
        if re.search(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])', before + '  ' + after):
            candidates.append(w)

    # 6) 語法・語彙章や候補不足のとき：空所直後・直前の実質語（STOPWORDS 除外）を拾う
    aw = [w for w in re.findall(r"[A-Za-z']{3,}", after) if w.lower() not in STOPWORDS]
    bw = [w for w in re.findall(r"[A-Za-z']{3,}", before) if w.lower() not in STOPWORDS]
    if chapter in (18, 19):
        if aw:
            candidates.insert(0, aw[0])
        if bw:
            candidates.append(bw[-1])
    else:
        if bw:
            candidates.append(bw[-1])
        if aw:
            candidates.append(aw[0])

    if not candidates:
        lw = last_words(before, 2) or first_words(after, 2)
        if lw:
            candidates.append(lw)

    blank_at = prompt.find('______')
    selected: List[Tuple[int, str]] = []
    seen_lower = set()
    for cand in candidates:
        c = cand.strip()
        if not c or len(c) < 2 or c.lower() in seen_lower or c.lower() in EDGE_TRIMS or c.lower() in STOPWORDS:
            continue
        pos = -1
        search_from = 0
        while True:
            idx = prompt.find(c, search_from)
            if idx < 0:
                break
            end = idx + len(c)
            if '【並べかえ】' in prompt and idx < prompt.find('」') + 1:
                search_from = idx + 1
                continue
            if blank_at >= 0 and idx < blank_at + 6 and end > blank_at:
                search_from = idx + 1
                continue
            if idx > 0 and prompt[idx - 1].isalpha() and c[0].isalpha():
                search_from = idx + 1
                continue
            if end < len(prompt) and prompt[end].isalpha() and c[-1].isalpha():
                search_from = idx + 1
                continue
            if any(idx < s_idx + len(s_c) and end > s_idx for s_idx, s_c in selected):
                search_from = idx + 1
                continue
            pos = idx
            break
        if pos >= 0:
            selected.append((pos, c))
            seen_lower.add(c.lower())
            if len(selected) >= 2:
                break

    selected.sort(key=lambda x: x[0])
    return [c for _, c in selected]


def compose_bespoke_hint(r: dict, cues: List[str]) -> str:
    """正解を直接ネタバレせず、『文のどこを見て何を判定すれば解けるか』を示す実践的な【着眼点】を作る。"""
    key = f"{r['chapter']}-{r['no']}"
    if key == '10-16':
        return '先行詞 the café（場所の名詞）に対し、空所の後ろ we first met に主語・目的語の欠けがあるかを確かめる。'

    ans = r['options'][r['answerIndex']].strip().rstrip('.?!')
    orig_hint = (r.get('hint') or '').strip().replace('___', '空所')
    if (
        orig_hint
        and not orig_hint.startswith('空所の前後「')
        and not orig_hint.startswith('問われているのは')
        and len(orig_hint) >= 16
        and (len(ans) < 4 or ans.lower() not in orig_hint.lower())
    ):
        return orig_hint if orig_hint.endswith('。') else orig_hint + '。'

    prompt = r['prompt']
    ch = r['chapter']
    theme = clean_theme_no_spoiler(r['grammar'], r['options'])
    lens = CHAPTER_LENS.get(ch, '空所前後の文構造と語法の結びつきを確かめる')
    jp_head, eng = strip_jp_header(prompt)

    if jp_head:
        jp_quote = re.search(r'「([^」]+)」', jp_head)
        jp_meaning = jp_quote.group(1) if jp_quote else ''
        cue_str = f'空所前後の “{cues[0]}” とのつながりを軸に、' if cues else ''
        theme_note = f'（{theme}）' if theme else ''
        return f'日本文「{jp_meaning}」に対応させ、{cue_str}主語・動詞・修飾語の語順{theme_note}を組み立てる。'

    if eng.startswith('(a)') and '(b)' in eng:
        cue_str = f'（特に “{cues[0]}”）' if cues else ''
        return f'(a) の文意{cue_str}を保ったまま、(b) の空所前後の品詞・構文に合う形へ言い換える。'

    if '=' in eng:
        cue_str = f' “{cues[0]}” ' if cues else '元の表現'
        return f'イコール前の{cue_str}と意味が等しくなるよう、書き換え後の時制・人称・構文をそろえる。'

    if ch == 20 or len(re.findall(r'[“"]([^”"]+)[”"]', eng)) >= 2:
        cue_str = f'発言中の “{cues[0]}” に注目し、' if cues else '前後の発言の流れに注目し、'
        theme_note = f'（{theme}）' if theme else ''
        return f'{cue_str}相手の意図{theme_note}に対して最も自然なやり取りになる応答を選ぶ。'

    if len(cues) >= 2:
        return f'文中の “{cues[0]}” と “{cues[1]}” を手がかりに、{lens}。'
    if len(cues) == 1:
        return f'文中の “{cues[0]}” を手がかりに、{lens}。'
    return f'{lens}。'


def is_formula_only(point: str) -> bool:
    p = (point or '').strip()
    if not p:
        return True
    if '。' not in p and len(p) < 34:
        return True
    if re.search(r'→', p) and len(p) < 25:
        return True
    return False


def _natural_cue_lead(ch: int, prompt: str, cues: List[str]) -> str:
    """要点の先頭に添える手がかり導入を、章・文脈に合わせて自然な日本語にする。"""
    _, eng = strip_jp_header(prompt)
    is_dialogue = ch == 20 or len(re.findall(r'[“"]([^”"]+)[”"]', eng)) >= 2
    if is_dialogue and cues:
        return f'会話の “{cues[0]}” に注目。'
    if eng.startswith('(a)') and '(b)' in eng and cues:
        return f'(a) の “{cues[0]}” からの書き換え。'
    if '=' in eng and cues:
        return f'元の文の “{cues[0]}” に注目。'
    if ch in (1, 3, 4) and len(cues) >= 2:
        return f'文中の “{cues[0]}” と “{cues[1]}” から時制・法を判断する。'
    if ch in (1, 3, 4) and len(cues) == 1:
        return f'文中の “{cues[0]}” が時制・法の目印。'
    if ch == 10 and len(cues) >= 2:
        return f'“{cues[0]}” とその後ろの “{cues[1]}” の関係に注目。'
    if ch in (6, 17, 18, 19) and len(cues) == 1:
        return f'空所と結びつく “{cues[0]}” の語法に注目。'
    if len(cues) >= 2:
        return f'文中の “{cues[0]}” と “{cues[1]}” に注目。'
    if len(cues) == 1:
        return f'文中の “{cues[0]}” に注目。'
    return ''


def compose_bespoke_point(r: dict, cues: List[str], ja_point_override: Optional[str]) -> Tuple[str, List[Tuple[str, int, str]]]:
    """カード直下の『要点』（【ポイント】）を1問ごとに具体化し、手がかりマーカー（cues）との対応を確定する。"""
    key = f"{r['chapter']}-{r['no']}"
    ans = r['options'][r['answerIndex']]

    if key == '4-104':
        core = '文中の “now” と “If he were here” から現在の事実に反する仮定だとわかるため、帰結節には助動詞の過去形を用いた would tell（今ここにいれば教えてくれるのに）を置く。'
    elif key == '10-16':
        core = '場所を表す the café を修飾し、後ろの節 we first met に主語・目的語の欠けがないため、“at [in] the café” の働きを兼ねる where を選ぶ。'
    else:
        orig_point = (ja_point_override or r.get('point') or '').strip()
        body = (r.get('body') or '').strip()
        orig_hint = (r.get('hint') or '').strip().replace('___', '空所')
        ans_why = (r['why'][r['answerIndex']] or '').strip().rstrip('。')

        if body:
            clean_pt = clean_formula_label(orig_point)
            if clean_pt and clean_pt not in body and len(clean_pt) <= 28:
                core = f'{clean_pt}。{body}'
            else:
                core = body
            if ans_why and len(core) < 55 and ans_why not in core:
                core = f'{core.rstrip("。")}（本問は {ans_why}）。'
        elif is_formula_only(orig_point):
            clean_pt = clean_formula_label(orig_point)
            parts: List[str] = []
            if orig_hint and not orig_hint.startswith('空所の前後「'):
                parts.append(orig_hint.rstrip('。'))
            if clean_pt:
                if ans_why and clean_pt not in ans_why and ans_why != orig_point.strip():
                    parts.append(f'「{clean_pt}」にあたるため、正解は {ans}（{ans_why}）')
                else:
                    parts.append(f'「{clean_pt}」の形をとるため、空所には {ans} が入る')
            elif ans_why:
                parts.append(f'{ans_why}ため、正解は {ans}')
            core = '。'.join(p for p in parts if p) + '。'
        else:
            core = orig_point if orig_point.endswith('。') else orig_point + '。'
            eng_words_in_core = set(w.lower() for w in re.findall(r"[A-Za-z']{3,}", core))
            prompt_words = set(w.lower() for w in re.findall(r"[A-Za-z']{3,}", r['prompt']) if w.lower() not in STOPWORDS)
            if not (eng_words_in_core & prompt_words) and ans_why and ans_why not in core:
                if orig_point.rstrip('。') in ans_why:
                    core = ans_why + '。'
                else:
                    core = f'{ans_why}。{core}'

    prompt = r['prompt']
    blank_at = prompt.find('______')

    def _matches_exact_stem_phrase(text: str, phrase: str) -> bool:
        if len(phrase) < 2 or phrase in ('SV', 'SVO', 'SVC', 'SVOO', 'SVOC'):
            return False
        in_stem = False
        jp_end = prompt.find('」') + 1 if ('【並べかえ】' in prompt and '」' in prompt) else 0
        for sm in re.finditer(re.escape(phrase), prompt[jp_end:], re.IGNORECASE):
            s_i, e_i = jp_end + sm.start(), jp_end + sm.end()
            if blank_at >= 0 and s_i < blank_at + 6 and e_i > blank_at:
                continue
            if s_i > 0 and prompt[s_i - 1].isalpha() and phrase[0].isalpha():
                continue
            if e_i < len(prompt) and prompt[e_i].isalpha() and phrase[-1].isalpha():
                continue
            in_stem = True
            break
        if not in_stem:
            return False

        for qm in re.finditer(r'[“"]([^”"]+)[”"]|「([A-Za-z][^」]+)」', text):
            q_inner = (qm.group(1) or qm.group(2) or '').strip().rstrip('.,')
            if q_inner.lower() == phrase.lower():
                return True

        for m in re.finditer(re.escape(phrase), text, re.IGNORECASE):
            s_i, e_i = m.start(), m.end()
            if s_i > 0 and text[s_i - 1].isalpha() and phrase[0].isalpha():
                continue
            if e_i < len(text) and text[e_i].isalpha() and phrase[-1].isalpha():
                continue
            after_tail = text[e_i:e_i + 16]
            if re.match(r"^\s*(?:＋|\+)?\s*(?:doing|done|to\s+do|S\b|O\b|A\b|B\b|C\b|V\b|one's\b|\(in\)|〜|…)", after_tail):
                continue
            before_head = text[max(0, s_i - 12):s_i]
            if re.search(r"(?:S|A|B|O|be|is|was)\s*(?:＋|\+)?\s*$", before_head) and phrase.lower() in (
                'known', 'surprised', 'caught', 'made', 'seen', 'busy', 'worth', 'afraid', 'hope', 'wish'
            ):
                continue
            en_span_before = re.search(r"[A-Za-z0-9'’-]+\s+$", text[:s_i])
            en_span_after = re.match(r"^\s+[A-Za-z0-9'’-]+", text[e_i:])
            if en_span_before or en_span_after:
                continue
            return True
        return False

    present_cues = [c for c in cues if _matches_exact_stem_phrase(core, c)]
    if not present_cues:
        if cues:
            lead = _natural_cue_lead(r['chapter'], prompt, cues)
            core = f'{lead}{core}'
        else:
            _, eng_only = strip_jp_header(prompt)
            b_part, a_part = split_blank(eng_only)
            fallback_toks: List[str] = []
            b_toks = [t for t in re.findall(r"[A-Za-z][A-Za-z']+", b_part) if t.lower() not in {'hello', 'hi'}]
            a_toks = [t for t in re.findall(r"[A-Za-z][A-Za-z']+", a_part) if t.lower() not in {'hello', 'hi'}]
            if b_toks:
                fallback_toks.append(b_toks[-1])
            if a_toks and (not fallback_toks or a_toks[0].lower() != fallback_toks[0].lower()):
                fallback_toks.append(a_toks[0])
            if fallback_toks:
                cues = fallback_toks
                if not any(_matches_exact_stem_phrase(core, ft) for ft in fallback_toks):
                    core = f'文中の “{fallback_toks[0]}” に注目。{core}'

    core = re.sub(r'([？?！!])。', r'\1 ', core).replace('。。', '。').strip()
    if not core.endswith('。'):
        core += '。'

    resolved_cues: List[Tuple[str, int, str]] = []
    used_why_spans: List[Tuple[int, int]] = []
    for c in cues:
        p_idx = prompt.find(c)
        if p_idx < 0:
            continue
        if blank_at >= 0 and p_idx < blank_at + 6 and p_idx + len(c) > blank_at:
            continue
        w_idx = core.find(c)
        if w_idx < 0:
            continue
        w_end = w_idx + len(c)
        if any(w_idx < s and w_end > e_s for e_s, s in used_why_spans):
            continue
        used_why_spans.append((w_idx, w_end))
        resolved_cues.append((c, 1, c))

    return core, resolved_cues


def enrich_choice_reason(r: dict, opt_idx: int, raw_reason: str) -> str:
    """4択それぞれの理由（○／×）で短絡的な定型句を排し、実際の語句と文構造に即した具体的な解説（全肢16文字以上）にする。"""
    reason = (raw_reason or '').strip().rstrip('。')
    opt = r['options'][opt_idx].strip()
    ans = r['options'][r['answerIndex']].strip()
    is_correct = opt_idx == r['answerIndex']
    _, eng = strip_jp_header(r['prompt'])
    before, after = split_blank(eng)
    prev_word = last_words(before, 1)
    prev_two = last_words(before, 2)
    next_word = first_words(after, 1)
    grammar = clean_formula_label(r['grammar'])

    if is_correct:
        if len(reason) < 16:
            if next_word and next_word.lower() not in EDGE_TRIMS:
                return f'{reason}。直後の {next_word} と結びついて文意に合致する形'
            if prev_word and prev_word.lower() not in EDGE_TRIMS:
                return f'{reason}。直前の {prev_word} に続く適切な語法・文構造'
            return f'{reason}。この文脈・構文に最も適切な表現'
        return reason

    # 1) 「<語> の位置が違う／誤り」の汎用精緻化
    pos_m = re.match(r'^([A-Za-z\']+)\s*の位置が(?:違う|誤り|逆)$', reason)
    if pos_m or reason in ('語順が違う', '語順が崩れている', 'not の位置・形が違う'):
        target_tok = pos_m.group(1) if pos_m else ''
        opt_words = opt.split()
        ans_words = ans.split()
        if target_tok and target_tok in ans_words:
            ti = ans_words.index(target_tok)
            around = ' '.join(ans_words[max(0, ti - 1):min(len(ans_words), ti + 2)])
            return f'{target_tok} を置く位置が不適切。ここでは “{around}”（全体は “{ans}”）の語順にする'
        if 'not' in opt_words and 'not' in ans_words and opt_words.index('not') != ans_words.index('not'):
            ni = ans_words.index('not')
            around = ' '.join(ans_words[max(0, ni - 1):min(len(ans_words), ni + 2)])
            return f'否定語 not を置く位置が不適切。ここでは “{around}” の順で否定を作る'
        if 'to' in opt_words and 'to' in ans_words and opt_words.index('to') != ans_words.index('to'):
            ti = ans_words.index('to')
            around = ' '.join(ans_words[max(0, ti - 1):min(len(ans_words), ti + 2)])
            return f'to の位置が不適切。“{around}” のまとまりになる語順にする'
        if set(w.lower() for w in opt_words) == set(w.lower() for w in ans_words) and len(ans_words) >= 2:
            if opt_words[0].lower() in ('am', 'is', 'are', 'was', 'were', 'do', 'does', 'did', 'can', 'will', 'would', 'has', 'have', 'had'):
                return f'疑問文の語順（{opt_words[0]}＋主語）になっている。節の内部では “{ans}” と平叙文の語順にする'
            for ow, aw in zip(opt_words, ans_words):
                if ow != aw:
                    return f'“{ow}” から続ける語順は不可。ここでは “{ans}” の順に並べる決まり'
        return f'{reason}。正しい語順は “{ans}” となる'

    if reason in ('倒置していない', '倒置になっていない'):
        return f'否定・強調の語句が文頭にあるのに通常の平叙文語順（{opt}）のままで、倒置（{ans}）になっていない'

    gov = prev_word if prev_word.lower() in PREPOSITIONS else prev_two or prev_word
    if reason in ('原形は目的語にならない', '原形は置けない', '動詞の原形は置けない', '原形は mind の目的語にならない', '動詞の原形は補語にならない'):
        if prev_word.lower() in PREPOSITIONS:
            return f'直前の {prev_word} は前置詞なので動詞の原形（{opt}）は続けられない。動名詞（{ans}）にする'
        return f'{gov or "この文構造"}の位置に動詞の原形単独（{opt}）は置けない。ここでは {ans} の形をとる'

    if reason in ('動詞の現在形は置けない', '三単現の形は置けない', '動詞の現在形は名詞を修飾しない'):
        if prev_word.lower() in PREPOSITIONS:
            return f'直前の前置詞 {prev_word} の目的語には動名詞（{ans}）が必要で、述語動詞の現在形（{opt}）は置けない'
        return f'すでに文の述語動詞があるため現在形（{opt}）は重ねられない。準動詞の {ans} を用いる'

    if reason in ('過去形は置けない', '過去形は目的語にならない', '過去形は補語にならない'):
        if prev_word.lower() in PREPOSITIONS:
            return f'前置詞 {prev_word} の直後に動詞の過去形（{opt}）は置けない。動名詞（{ans}）にする'
        return f'この空所は述語動詞の位置ではないため過去形（{opt}）は不可。{ans} の形にする'

    if reason in ('過去分詞は置けない', '過去分詞は目的語にならない', '過去分詞は不可'):
        if prev_word.lower() in PREPOSITIONS:
            return f'前置詞 {prev_word} の目的語には動名詞（{ans}）を置くため、過去分詞単独（{opt}）は続けられない'
        return f'受け身や完了の意味を作る文脈ではないため過去分詞（{opt}）は不適。能動・原形などの {ans} を選ぶ'

    if reason in ('前置詞の後ろに to do は置けない', 'to は前置詞なので後ろは doing'):
        return f'直前の {prev_word or "to"} は前置詞なので、to 不定詞（{opt}）ではなく動名詞（{ans}）を続ける'

    if reason in ('to は不要', '能動の see A の後に to は不要', 'let A の後に to は不要'):
        return f'知覚・使役動詞の能動態では目的語の後ろに原形（{ans}）を置くため、to を付けた “{opt}” は不可（受動態になると to が復活）'

    if reason in ('現在形では仮定法にならない', '現在完了は仮定法にならない'):
        return f'事実に反する仮定（仮定法）では時制を1段階過去へずらす決まりのため、直説法の “{opt}” は使えない（正解は “{ans}”）'

    if reason in ('現在の形で過去を表せない',):
        return f'過去の時点についての推量・後悔を表す場面なので、現在推量の “{opt}” ではなく「助動詞＋have＋過去分詞」（{ans}）を用いる'

    if reason in ('過去完了は過去の基準時が必要',):
        return f'過去完了（{opt}）は「過去のある時点よりさらに前」を表す形。基準となる過去の時点がない本問では “{ans}” を使う'

    if reason in ('other は単独では使えない',):
        return f'other は形容詞用法が基本で単独の名詞としては使えないため、冠詞や -s を伴う “{ans}” を選ぶ'

    if reason in ('another は単数', 'the other は単数'):
        return f'{opt} は単数の対象を受ける表現。本問の対象は複数なので “{ans}” を用いる'

    if reason in ('単数なので those は不可',):
        return f'those は複数名詞を受ける代名詞（that の複数形）。ここは単数の名詞を受けるため “{ans}” を使う'

    if reason in ('none は3者以上で使う',):
        return f'none は原則として3つ以上の対象に使う全体否定。2者の全体否定である本問では “{ans}” を選ぶ'

    if reason in ('限定のない名詞の前は most',):
        return f'the や所有格が付かない一般の名詞を直接修飾するときは most of ではなく most（{ans}）を用いる'

    if reason in ('which の後ろは不完全な文', 'what の後ろは不完全な文'):
        return f'関係代名詞 {opt} の後ろには主語や目的語が欠けた不完全な節が続く。後ろが完全な文の本問では “{ans}” を選ぶ'

    if reason in ('所有格の後ろには名詞が必要', 'whose の後ろには名詞が必要'):
        return f'所有格（{opt}）の直後には無冠詞の名詞が続く決まり。直後に {next_word or "動詞"} が続く本問では “{ans}” を用いる'

    if reason in ('what には非制限用法がない', 'that は非制限用法では使えない'):
        return f'コンマ（,）の直後に続ける非制限用法では {opt} は使えない決まり。ここでは “{ans}” を用いる'

    if reason in ('whom は目的格', 'whom は目的格で、主語になれない', 'whom は人の目的格'):
        return f'whom は「人」を目的語にとる目的格。この空所の文法役割（正解は “{ans}”）とは一致しない'

    if reason in ('which は人以外の先行詞に使う',):
        return f'which は事物を先行詞にとる関係代名詞。先行詞が「人」の本問では {ans} を用いる'

    if reason in ('who は人の先行詞に使う', 'who は人'):
        return f'who は「人」の先行詞専用の主格関係代名詞。本問の文脈では {ans} を選ぶ'

    if reason in ('what は先行詞を含む',):
        return f'what（＝the thing which）はそれ自体に先行詞を含むため、前に先行詞の名詞がある空所には置けない（正解は {ans}）'

    if reason in ('which には先行詞が必要', 'that には先行詞が必要'):
        return f'{opt} は前に修飾される名詞（先行詞）が必要。空所の前に先行詞がないため、先行詞を含む {ans} を用いる'

    if reason in ('during は前置詞',):
        return f'during は前置詞なので後ろには名詞句しか置けない。SV を備えた節が続く本問では接続詞の “{ans}” を使う'

    if reason in ('that は副詞節を作らない', 'as では名詞節を作れない'):
        return f'{reason}ため文構造が成り立たない。前後の節関係に合う接続詞 “{ans}” を選ぶ'

    if reason in ('it では接続詞がない',):
        return f'代名詞 {opt} だけでは2つの SV 節をつなぐ接続詞の働きがないため、関係詞・接続詞を含む “{ans}” が必要'

    if reason in ('最上級は than と組まない',):
        return f'直後に比較相手を示す than があるため最上級（{opt}）は不可。比較級の “{ans}” を用いる'

    if reason in ('a few は可算名詞に付ける',):
        return f'a few は数えられる複数名詞に使う表現。不可算名詞を修飾する本問では “{ans}” を用いる'

    if reason in ('語尾の -s にだまされた誤り',):
        return f'直前の名詞の -s（または学科名・単数扱い語）に引きずられた誤り。主語の核に合わせて “{ans}” を選ぶ'

    if reason in ('副詞は be の補語にならない', '副詞で名詞を修飾できない', '副詞は補語にならない'):
        return f'{opt} は副詞なので、名詞の直接修飾や be 動詞等の補語（C）には置けない。形容詞の “{ans}” を選ぶ'

    if reason in ('語順が疑問文のまま', '疑問文の語順にはしない'):
        return f'間接疑問文（疑問詞節）の内部では疑問文語順（{opt}）にせず、「疑問詞＋S＋V」（{ans}）の平叙文語順にする'

    if reason in ('of は不可', 'with は不可', 'for は不可', 'at は地点', 'on は接触'):
        prep_meanings = {
            'of': '所属・分離・関連（〜の）',
            'with': '同伴・道具・付帯（〜と一緒に／〜を使って）',
            'for': '目的・対象・期間（〜のために／〜の間）',
            'at': '一点・時刻・狭い場所（〜に）',
            'on': '接触・特定の日付や曜日（〜の上に／〜に）',
            'in': '空間の内部・着用・月や年（〜の中に／〜を着て）',
        }
        pm = prep_meanings.get(opt.lower(), '別の関係')
        return f'{opt} は主に「{pm}」を表す前置詞で、この文が求める結びつき（正解は {ans}）には合わない'

    if reason in ('it は形容詞で修飾できない', 'it は修飾語句を伴わない'):
        return f'代名詞 it は「特定のその物」を丸ごと指す語で、形容詞や前置詞句で直接修飾できないため限定可能な {ans} を使う'

    if reason in ('a が必要', '形容詞を a の前に出す'):
        return f'how / so / too / as の後ろに単数可算名詞を置くときは「how＋形容詞＋a＋名詞」（{ans}）の語順が必須'

    # 16文字未満の残りの短文理由もすべて、その選択肢と正解肢の対比が伝わる具体的説明へ引き上げる
    if len(reason) < 16:
        if reason in ('語順が逆', 'A と B が逆', '人と物が逆', '主語と目的語が逆'):
            return f'{reason}になっている。ここでは “{ans}” の語順で並べる決まり'
        if '位置が' in reason or 'a は名詞の前' in reason or '語順' in reason:
            return f'{reason}。正しい語順は “{ans}” となる'
        if '不要' in reason:
            return f'{reason}（“{opt}” のようには言わず、“{ans}” の形で用いる）'
        if '抜けている' in reason or 'が必要' in reason:
            return f'{reason}ため文構造が不完全。“{ans}” の形にして完成させる'
        if '意味が通らない' in reason or '意味が逆' in reason or '文脈に合わない' in reason:
            return f'{opt} では{reason}。前後の文脈に合う “{ans}” を選ぶ'
        if 'という形はない' in reason or '英語として不自然' in reason:
            return f'“{opt}” {reason}。正しい表現は “{ans}” となる'
        if reason.endswith('は不可') or reason.endswith('は誤り') or reason.endswith('使わない') or reason.endswith('しない') or reason.endswith('組まない'):
            return f'{reason}ため、空所前後の語法に合致する “{ans}” を選ぶ'
        return f'{reason}ため、この文脈・構文では “{ans}” を用いるのが適切'

    return reason


def compose_bespoke_plus(r: dict, tip: str) -> str:
    """第12〜17章（372問）など【プラス】が空欄だった問に対し、その問固有の対比・ひっかけ回避メモを付与する。"""
    existing = (r.get('plus') or '').strip()
    if existing:
        return existing

    ch = r['chapter']
    ans = r['options'][r['answerIndex']].strip()
    point = clean_formula_label(r.get('point') or '')
    body = (r.get('body') or '').strip()
    grammar = clean_formula_label(r['grammar'])
    prompt = r['prompt']

    if ch == 12:
        if re.search(r'着ている|身につけ|服|dress|suit|coat|hat|red|black', point + body + prompt):
            return '身につけている衣服・色・靴・眼鏡には in（a woman in a white dress）、身体的特徴や手に持っている物には with（a girl with long hair）を使い分ける。'
        if ans in ('on', 'in', 'at') and re.search(r'時|日付|曜|時刻|朝|月|年|季節', grammar + point + body):
            return f'時を表す in / on / at の使い分け：時刻の一点は at、特定の日・曜日・特定の日の朝夕は on、月・季節・年は in（本問は {ans}）。'
        if ans in ('by', 'until', 'till'):
            return '期限と継続の対比：完了の期限「〜までに（1回終える）」は by、動作・状態の継続「〜までずっと続ける」は until [till] を使う。'
        if ans in ('for', 'during', 'within') or (ans == 'in' and re.search(r'期間|間|経過|後', point + body)):
            return '期間・経過の前置詞：数値つきの長さ（three days 等）には for、特定の出来事・期間名（the vacation 等）には during、「（今から）〜後に」は in を使う。'
        if ans in ('between', 'among'):
            return '2者の間（または A, B, and C の個別の関係）は between、3つ以上の集団の中は among で表す。'
        if re.search(r'差|勝|負|年上|年下|単位', point + body):
            return '差・増減幅・売買の単位は by で表す（lose by one point / sell eggs by the dozen / pay by the hour）。'
        return f'前置詞は日本語訳の丸暗記ではなく、「直前の動詞・形容詞と直後の名詞の結びつき（本問：{point or ans}）」で押さえると応用が利く。'

    if ch == 13:
        return f'主語と動詞の呼応では、空所直前の複数形や修飾語句に惑わされず「主語全体の核が単数概念か複数概念か（本問：{point or grammar} → {ans}）」で決める。'

    if ch == 14:
        if '付加疑問' in grammar:
            return "付加疑問・応答の鉄則：前の主節が肯定なら否定形、否定語（never / little / seldom 等）を含むなら肯定形で受け、Let's → shall we?、命令文 → will you? も押さえる。"
        if '倒置' in grammar or re.search(r'倒置', point + body):
            return '否定・制限の副詞句や So / Nor が文頭に出たときは「助動詞［be動詞］＋主語」の疑問文語順へ倒置する点が4択・整序ともに最頻出。'
        if re.search(r'how|so|too|such', grammar, re.I):
            return '語順の対比：「how / so / too / as＋形容詞＋a＋単数名詞」に対し、what と such は「what [such]＋a＋形容詞＋単数名詞」の順になる。'
        return '疑問文が他の文の一部（間接疑問）に埋め込まれるときは「疑問詞＋S＋V」の平叙文語順に戻す（do you think 等の連鎖疑問文だけ疑問詞が文頭へ出る）。'

    if ch == 15:
        if '部分否定' in grammar or re.search(r'部分否定', point + body):
            return 'not＋all / every / always / both / necessarily は「すべて〜とは限らない（部分否定）」。「1つも〜ない（全体否定）」は none / neither / never で表す。'
        if '強調' in grammar or re.search(r'強調', point + body):
            return 'It is [was] A that … の強調構文は名詞・副詞句を挟んで強調でき、一般動詞そのものを「本当に〜する」と強めるときは do / does / did＋原形 を使う。'
        return '否定語を含まない否定・制限表現（anything but「決して〜ない」⇔ nothing but「〜にすぎない」、far from doing、the last 人 to do）は対比で整理する。'

    if ch == 16:
        return '直接話法⇔間接話法の転換では「①伝達動詞（told / asked / suggested）・②人称代名詞・③時制の一致・④時や場所の副詞（yesterday→the day before 等）」の4箇所を連動して点検する。'

    if ch == 17:
        if re.search(r'他動詞|自動詞', grammar + point + body):
            return '日本語では「〜について／〜に」と訳しても前置詞不要の他動詞（discuss / marry / reach / enter / resemble / approach / mention）と、前置詞必須の自動詞（graduate from / apologize to）を対比で覚える。'
        if re.search(r'動名詞|不定詞', grammar):
            return '動詞の目的語選択：反復・完了・回避（mind / enjoy / finish / avoid / give up / put off）は doing、未来志向（want / decide / hope / expect / refuse / promise）は to do をとる。'
        if re.search(r'仮定法現在|should|提案|要求|主張', grammar + point + body):
            return '提案・要求・主張の動詞（suggest / insist / demand / recommend / propose）に続く that 節では「S＋(should)＋動詞の原形」となり、三人称単数や過去時制でも原形が保たれる。'
        if re.search(r'知覚|使役|let|make|have|see|hear|watch', grammar + point + body):
            return '使役（make / let / have）や知覚動詞（see / hear / watch 等）は能動態では原形不定詞をとるが、allow / get / force / cause A to do は to が必須である点と対比する。'
        return f'動詞の語法問題では単語の意味だけで選ばず、「動詞＋目的語＋前置詞／補語の型（{point or grammar}）」を丸ごとフレーズで定着させる。'

    return tip or ''
