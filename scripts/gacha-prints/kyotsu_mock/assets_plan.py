"""共通テスト予想問題（LR プリント）の「まだ無い素材」の一覧（音声・リスニングの絵・地図・リーディングの図）。

制作指示書 PDF（build_orders.py）と音声生成スクリプト（make_audio.py）が同じ一覧を使う。
台本・絵の説明は set{n}_l.py / set{n}_r*.py から自動で取り出すので、問題を直したらここも自動で追従する。
"""
import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render as R  # noqa: E402

SETS = [1, 2, 3, 4, 5]
ASSET_DIR = 'public/prints/kyotsu_assets'   # 素材を置く場所（受け取り後に PDF へ組み込む）

# ───────── 音声：話し手と声 ─────────
# OpenAI TTS（gpt-4o-mini-tts）の声。女性：coral / nova / sage / shimmer　男性：ash / echo / onyx / verse / ballad
ACCENT = {
    'us': 'Speak clear, natural General American English at an exam-appropriate pace (about 140-150 words per minute).',
    'uk': 'Speak with a clear standard British (Southern English) accent at an exam-appropriate pace (about 140-150 words per minute).',
    'nn': 'Speak fluent, clear English with a light non-native accent (for example, a native Spanish speaker), slightly slower than a native speaker. Every word must stay easy to understand.',
    'lec': 'Speak like a friendly university lecturer: clear General American English, measured pace (about 130-140 words per minute), short natural pauses between sentences.',
    'nar': 'Neutral, calm exam announcer. Clear General American English, steady pace.',
    'ja': '落ち着いた標準語の試験アナウンス。はっきり、ややゆっくり読む。',
}
ACCENT_JA = {'us': 'アメリカ英語', 'uk': 'イギリス英語', 'nn': '非母語話者（軽いなまり）', 'lec': '講義口調（アメリカ英語）',
             'nar': 'アナウンス（英語）', 'ja': '日本語アナウンス'}

FEMALE = {'Aisha', 'Aoi', 'Chloe', 'Emma', 'Grace', 'Hana', 'Lily', 'Mia', 'Mika', 'Nora', 'Rin', 'Sakura', 'Sara', 'Sarah', 'Yui'}
MALE = {'Alex', 'Ben', 'Daniel', 'James', 'Ken', 'Kenji', 'Leo', 'Max', 'Omar', 'Raj', 'Ryan', 'Taku', 'Tom'}
F_VOICES = ['coral', 'shimmer', 'nova', 'sage']
M_VOICES = ['ash', 'echo', 'verse', 'onyx']

# 第3問などで「（女性は英国人）」のように指定がある設問：(回, 問) → {話し手: なまり}
ACCENT_OVERRIDE = {
    (1, 13): {'W': 'uk'}, (1, 17): {'W': 'nn'}, (2, 13): {'M': 'nn'}, (2, 14): {'W': 'uk'},
    (3, 13): {'W': 'uk'}, (3, 16): {'M': 'nn'}, (4, 12): {'M': 'uk'}, (4, 14): {'M': 'nn'},
    (5, 13): {'W': 'uk'}, (5, 15): {'W': 'nn'},
}

NARRATOR = {'voice': 'alloy', 'accent': 'nar', 'who': 'Narrator（問いの読み手）'}
JA_NARRATOR = {'voice': 'alloy', 'accent': 'ja', 'who': 'アナウンス（日本語）'}

# 間（ま）の目安（秒）
PAUSE_LINE = 0.6        # 話し手が替わるとき
PAUSE_REPEAT = 4        # 2回読みの1回目と2回目のあいだ
PAUSE_ANSWER = {'第1問': 8, '第2問': 8, '第3問': 8, '第4問': 15, '第5問': 30, '第6問': 20}
PAUSE_PREVIEW = {'第4問': 15, '第5問': 60, '第6問': 20}   # 読み上げ前に問題冊子を見る時間（本番の先読み時間の目安）


def load_l(n):
    m = importlib.import_module(f'set{n}_l')
    importlib.reload(m)
    parts = m.LISTENING['parts']
    R.number_marks(parts)
    return m.LISTENING


def load_r(n):
    m = importlib.import_module(f'set{n}_r')
    return m.READING


def mark_label(marks):
    return f'{marks[0]:02d}' if len(marks) == 1 else f'{marks[0]:02d}-{marks[-1]:02d}'


def q_label(marks):
    return f'問{marks[0]}' if len(marks) == 1 else f'問{marks[0]}〜{marks[-1]}'


def _parse_label(sp):
    """'W (lecturer)' / '2 (M, non-native)' / 'Ken' → (key, gender, accent, role)"""
    m = re.match(r'^(\w+)\s*\((.+)\)$', sp)
    if m:
        head, inside = m.group(1), [x.strip() for x in m.group(2).split(',')]
        if head in ('W', 'M'):
            role = inside[0]
            return sp, head, 'lec' if role == 'lecturer' else 'us', role
        g = inside[0]
        acc = 'us'
        if 'British' in inside[1:]:
            acc = 'uk'
        if 'non-native' in inside[1:]:
            acc = 'nn'
        return sp, g, acc, f'話し手{head}'
    if sp in ('W', 'M'):
        return sp, sp, 'us', ''
    if sp in FEMALE:
        return sp, 'W', 'us', ''
    if sp in MALE:
        return sp, 'M', 'us', ''
    raise ValueError(f'unknown speaker {sp!r}')


def cast_for(lines, n, qno=None):
    """1トラック内の話し手ごとに声を割り当てる（同じトラックで同じ声が重ならないように）"""
    cast = {}
    used = {'W': 0, 'M': 0}
    over = ACCENT_OVERRIDE.get((n, qno), {}) if qno else {}
    for sp, text, _ in lines:
        if not sp or sp in cast:
            continue
        key, g, acc, role = _parse_label(sp)
        acc = over.get(sp, acc)
        pool = F_VOICES if g == 'W' else M_VOICES
        # 講義は落ち着いた声、それ以外は順番に
        if acc == 'lec':
            voice = 'nova' if g == 'W' else 'onyx'
        else:
            voice = pool[used[g] % len(pool)]
            used[g] += 1
        gender = '女性' if g == 'W' else '男性'
        who = f'{sp}（{gender}' + (f'・{role}' if role and not role.startswith('話し手') else '') + f'・{ACCENT_JA[acc]}）'
        cast[sp] = {'voice': voice, 'accent': acc, 'who': who}
    return cast


def resolve_lines(lines, cast):
    """話し手が '' の行：'Question:' なら Narrator、それ以外は直前の話し手の続き（講義の段落など）"""
    out = []
    prev = None
    for sp, text, ja in lines:
        if sp:
            v = cast[sp]; prev = sp; name = sp
        elif text.startswith('Question') or prev is None:
            v = NARRATOR; name = 'Narrator'
        else:
            v = cast[prev]; name = prev
        out.append({'speaker': name, 'voice': v['voice'], 'accent': v['accent'], 'text': text, 'ja': ja})
    return out


def tracks(n):
    """第n回の音声トラック一覧（本番の流れの順）"""
    data = load_l(n)
    out = []
    for p in data['parts']:
        for si, s in enumerate(p['sections']):
            tag = s.get('tag') or ''
            head = p['label'] + (tag[0] if tag[:1] in ('A', 'B') else '')
            groups = []
            if s.get('script'):
                marks = [m for q in s['qs'] for m in q['marks']]
                groups.append((marks, s['script'], s.get('situation', ''), None, True))
            else:
                for q in s['qs']:
                    if q.get('script'):
                        groups.append((q['marks'], q['script'], q.get('situation', ''), q['marks'][0], False))
            for gi, (marks, lines, situation, qno, whole) in enumerate(groups):
                cast = cast_for(lines, n, qno)
                intro = []
                if gi == 0 and not tag.startswith('問'):
                    intro.append(f'{head}。{s["instr"]}')
                if not whole or tag.startswith('問'):
                    intro.append(f'{q_label(marks)}。')
                elif whole:
                    intro.append(f'{q_label(marks)}。')
                out.append({
                    'file': f'kyotsu_l{n}_q{mark_label(marks)}.mp3',
                    'set': n, 'part': p['label'], 'tag': tag, 'head': head, 'marks': marks,
                    'label': f'第{n}回 {head} {q_label(marks)}',
                    'times': s['times'], 'situation': situation, 'instr': s['instr'],
                    'intro_ja': ' '.join(intro), 'cast': cast, 'lines': resolve_lines(lines, cast),
                })
    return out


# ───────── ElevenLabs（Eleven v4・有料プラン）用の設定 ─────────
# v4 は Text to Dialogue API（model_id = eleven_v4）。1リクエスト2,000字以内が推奨。SSML の <break> は使えないので、
# 間は「…」と句読点・音声タグ [pause] で作り、問題間の長い無音（解答時間など）は ffmpeg で足す。
# なまりは「その国の声（Voice Library の Accent で絞り込み）」を選ぶのが基本。タグはその補助。
EL_MODEL = 'eleven_v4'
EL_SETTINGS = {'stability': 0.5}     # v4 は Stability のみ（0＝表現豊か／0.5＝自然／1＝安定）。試験音声は 0.5 前後
# 役ごとの声（キャスト）。voice_id は Voice Library で選んだ声の ID を入れる（未設定ならスクリプトは止まる）
EL_CAST = {
    'W_us':  {'ja': '女性・アメリカ英語', 'search': 'Accent: American / Female / Young adult / Conversational', 'tag': '', 'voice_id': ''},
    'W_us2': {'ja': '女性・アメリカ英語（2人目）', 'search': 'Accent: American / Female / Middle-aged / Conversational', 'tag': '', 'voice_id': ''},
    'M_us':  {'ja': '男性・アメリカ英語', 'search': 'Accent: American / Male / Young adult / Conversational', 'tag': '', 'voice_id': ''},
    'M_us2': {'ja': '男性・アメリカ英語（2人目）', 'search': 'Accent: American / Male / Middle-aged / Conversational', 'tag': '', 'voice_id': ''},
    'W_uk':  {'ja': '女性・イギリス英語', 'search': 'Accent: British / Female / Conversational', 'tag': '[British accent]', 'voice_id': ''},
    'M_uk':  {'ja': '男性・イギリス英語', 'search': 'Accent: British / Male / Conversational', 'tag': '[British accent]', 'voice_id': ''},
    'W_nn':  {'ja': '女性・非母語話者（軽いなまり）', 'search': 'Language: English / Accent: Spanish・Indian など / Female', 'tag': '[light Spanish accent, speaking clearly and a little slowly]', 'voice_id': ''},
    'M_nn':  {'ja': '男性・非母語話者（軽いなまり）', 'search': 'Language: English / Accent: Spanish・Indian など / Male', 'tag': '[light Spanish accent, speaking clearly and a little slowly]', 'voice_id': ''},
    'W_lec': {'ja': '女性・講義（講師）', 'search': 'Accent: American / Female / Middle-aged / Educational・Narrative', 'tag': '[calm university lecturer, measured pace]', 'voice_id': ''},
    'M_lec': {'ja': '男性・講義（講師）', 'search': 'Accent: American / Male / Middle-aged / Educational・Narrative', 'tag': '[calm university lecturer, measured pace]', 'voice_id': ''},
    'NAR':   {'ja': '問いの読み手（Narrator・英語）', 'search': 'Accent: American / Neutral / Narrative・Informative', 'tag': '[neutral exam announcer]', 'voice_id': ''},
    'JA':    {'ja': '日本語アナウンス', 'search': 'Language: Japanese / Female or Male / Narrative・Informative（落ち着いた標準語）', 'tag': '[落ち着いた試験アナウンス]', 'voice_id': ''},
}
EL_RULES = [
    'モデルは **Eleven v4**（API の model_id は `eleven_v4`）。アプリなら「Text to Speech」でモデル v4 を選び、2人以上が話す問題は **Dialogue（対話）モード**で、行ごとに声を割り当てる。',
    'Voice settings は **Stability 0.5 前後（Natural）**。0 に近いと感情が出すぎて試験らしくなくなる。',
    '**なまりは声で決める**：v4 は英語を流ちょうに話すので、日本語や別言語の声に英語を読ませても、なまりは自然に付かない。イギリス英語・非母語話者の役は Voice Library の Accent で絞り込んだ声を使い、各行の先頭に表のタグも付ける。',
    '**SSML の <break> は使えない**。文中の短い間は「…」やカンマ、`[pause]` タグで作る。問題と問題のあいだの長い無音（先読み・解答時間）は、生成した音声をつなぐときに足す（付属スクリプトが自動で入れる）。',
    '音声タグ（[ ] の中）は**読まれない**演技の指示。感情タグ（[excited] など）は使わない。試験音声は落ち着いた自然な話し方が基本。',
    '1回の生成は **2,000字以内**に（それより長いと途中で切れることがある）。最長のトラックでも約1,050字なので、1問＝1回の生成でよい。',
    '同じ話し手名は同じ声で。同じ問題の中で同じ性別の話し手が2人いるときは、「2人目」の声を使う。',
    '**第1問・第2問は2回**、**第3〜6問は1回**。2回読みの問題は、同じ音声を2回つなぐ（読み直して生成しない）。',
]


def el_role(v, g_index=0):
    """assets_plan の声の割り当て（性別・なまり）→ EL_CAST の役名"""
    g = 'W' if '女性' in v['who'] else 'M'
    acc = v['accent']
    if acc in ('uk', 'nn', 'lec'):
        return f'{g}_{acc}'
    return f'{g}_us2' if g_index else f'{g}_us'


def el_track(t):
    """1トラックを ElevenLabs 用に：[(役名, タグつき本文)]。同じ性別のアメリカ英語の2人目は *_us2"""
    roles = {}
    count = {'W': 0, 'M': 0}
    for sp, v in t['cast'].items():
        g = 'W' if '女性' in v['who'] else 'M'
        if v['accent'] in ('us',):
            roles[sp] = el_role(v, count[g]); count[g] += 1
        else:
            roles[sp] = el_role(v)
    out = []
    for ln in t['lines']:
        role = 'NAR' if ln['speaker'] == 'Narrator' else roles.get(ln['speaker'], 'NAR')
        tag = EL_CAST[role]['tag']
        out.append((role, ln['speaker'], (tag + ' ' if tag else '') + ln['text']))
    return out


# ───────── リスニングの絵（4択の絵・4コマの順番） ─────────
def pics(n):
    data = load_l(n)
    out = []
    for p in data['parts']:
        for s in p['sections']:
            for b in s.get('blocks', []):
                if b[0] == 'pics':
                    marks = [m for q in s['qs'] for m in q['marks']]
                    out.append({'file': f'kyotsu_l{n}_q{mark_label(marks)}_pics.png', 'set': n, 'part': p['label'],
                                'label': f'第{n}回 {p["label"]}{(s.get("tag") or "")[:1]} {q_label(marks)}', 'kind': 'order',
                                'descs': b[1], 'prompt': '', 'situation': s['instr'], 'script': [l[1] for l in s.get('script', [])]})
            for q in s['qs']:
                for b in q.get('pre', []):
                    if b[0] == 'pics':
                        out.append({'file': f'kyotsu_l{n}_q{mark_label(q["marks"])}_pics.png', 'set': n, 'part': p['label'],
                                    'label': f'第{n}回 {p["label"]}{(s.get("tag") or "")[:1]} {q_label(q["marks"])}', 'kind': 'choice',
                                    'descs': b[1], 'prompt': q.get('prompt', ''), 'situation': q.get('situation', ''),
                                    'script': [l[1] for l in q.get('script', [])]})
    return out


# 地図・見取り図（4つ）。セルの並びを人が読める説明に直したもの
MAPS = {
    (1, 9): {'title': '映画館の座席（上から見た見取り図）', 'aspect': '3:2',
             'layout': ['いちばん上（前方）に横長のスクリーン。四角の中に「SCREEN」と書く。',
                        '座席のブロックを4つ：前方の左＝①、前方の右＝②、後方の左＝③、後方の右＝④。各ブロックに座席の小さな四角を数個並べ、その中央に丸数字を大きく書く。',
                        '左右のブロックの間に縦の通路。通路に小さく「aisle」。',
                        '後方の右側の壁（④の近く）に出口の表示「EXIT →」。'],
             'check': '④が「後方」かつ「右」かつ「出口の近く」に見えること。①〜④の位置関係が問題文と一致すること。'},
    (2, 9): {'title': '部屋の見取り図（上から見た図）', 'aspect': '3:2',
             'layout': ['部屋を上から見た四角い図。上の壁の左端に窓（「window」）、上の壁の中央に本棚（「bookshelf」）。',
                        '置き場所の候補を4つ：窓の前（左上）＝①、本棚の右（右上）＝②、左下の隅＝③、右下のヒーターの前＝④。',
                        '下の壁の中央にソファ（「sofa」）、右下の隅にヒーター（「heater」）。',
                        '①〜④の場所には、点線の丸と丸数字を描く（植木鉢そのものは描かない）。'],
             'check': '①が「窓のそば・本棚の近く」、④が「ヒーターのそば」に見えること。'},
    (3, 8): {'title': '町の地図（通りの両側に建物）', 'aspect': '3:2',
             'layout': ['中央を左右に通る広い道。道に「Main Street」と書く。',
                        '道の上側に左から：①（空き区画）、「BANK」、②（空き区画）、「PARK」（木を数本）。',
                        '道の下側に左から：③（空き区画）、「CAFÉ」、④（空き区画）、「HOTEL」。',
                        '①〜④の区画は建物の形だけ描き、中に丸数字を書く（郵便局のマークは描かない）。'],
             'check': '②が「BANK と PARK のあいだ」、④が「CAFÉ と同じ側」に見えること。郵便局がどこかを絵で示さないこと。'},
    (5, 9): {'title': '公園の見取り図（上から見た図）', 'aspect': '3:2',
             'layout': ['公園を上から見た図。上段の左に噴水（「fountain」）、上段の中央に遊び場（「playground」、すべり台やぶらんこ）。',
                        'ベンチの場所の候補を4つ：噴水のそば（左上）＝①、遊び場の右（右上）＝②、左下＝③、右下の駐車場のそば＝④。',
                        '下段の中央にカフェ（「café」）、右下に駐車場（「car park」）。',
                        '①〜④にはベンチを1つずつ描き、丸数字を添える。木陰がわかるよう①のそばに木を2本。'],
             'check': '①が「噴水のそばで木陰がある」、②が「遊び場の近く」に見えること。'},
}


def maps():
    out = []
    for (n, qn), v in MAPS.items():
        data = load_l(n)
        q = next(q for p in data['parts'] for s in p['sections'] for q in s['qs'] if q['marks'][0] == qn and p['label'] == '第2問')
        out.append({**v, 'file': f'kyotsu_l{n}_q{qn:02d}_map.png', 'set': n, 'label': f'第{n}回 第2問 問{qn}',
                    'prompt': q['prompt'], 'situation': q.get('situation', ''), 'script': [l[1] for l in q['script']]})
    return out


# ───────── リーディングの図（本番ならイラスト・写真・図が入る所） ─────────
# (回, 大問, ファイルの短い名前, 入れる場所, 縦横比, 何を描くか, 注意)
R_FIGS = [
    # 第1回
    (1, '第2問', 'cuploop_header', 'ウェブサイト「Cup Loop」のタイトルの下（横長の見出し画像）', '3:2',
     'Cup Loop のロゴ風イラストと、ふた付きの再利用カップ（側面に小さな四角いQRコード）。その右に「借りる仕組み」の3つの手順を左から並べた小さな絵：①スマートフォンでアプリに登録 → ②カフェのカウンターでカップのQRコードを読み取る → ③町なかの返却ボックスにカップを入れる。手順の番号は 1・2・3 の数字だけ。',
     '料金（£3・£5・20p）や数字の「38」「12」「500」「7 days」は絵に入れない（設問の答えになるため）。返却ボックスは「いっぱいではない」状態で描く。'),
    (1, '第3問', 'jam_blog', 'ブログ「Grandma\'s Jam」のタイトルの下（記事の写真の代わり）', '3:2',
     '古いノートが開いて置かれ、ページに紫色のしみ（白黒なので濃いしみ）がある。横に梅ジャムのびんと、ジャムを塗ったトースト1枚。木のテーブル。人物は描かない。',
     'ノートの文字は読めない手書き風の線にする。レモンは描かない。'),
    (1, '第5問', 'ranger_flyer', 'チラシ「Become a Youth Ranger this Summer!」のタイトルの右か下', '3:2',
     '3つのコースを表す3コマ：A 長ぐつで川に入り、ビンで水を調べる10代の男女／B 湿地の観察小屋から双眼鏡で鳥を見る10代／C 長ズボン・手袋で若い木を植える10代。背景に川と森。',
     '人数は各コマ2〜3人。文字・料金は入れない。'),
    (1, '第5問', 'ranger_map', 'メール（Joanna Price）の下（任意：集合場所の地図）', '3:2',
     '川（River Avel）が左上から右下へ流れる簡単な地図。上流側に「Riverside Nature Centre」、下流側の橋のそばに「Mill Bridge car park」。道を細い線で。北の矢印。',
     '地名の文字は英語でこの2つと「River Avel」だけ。距離や時刻は書かない。'),
    (1, '第6問', 'ruth_snow', '伝記「Ruth Okada」の本文の第1段落の横（挿絵）', '1:1',
     '1930年代の少女が家の裏のポーチで、古い箱型カメラを黒い毛糸の手袋の上の雪の結晶に向けている。雪が降っている。',
     '実在の人物の写真に似せない。文字なし。'),
    (1, '第6問', 'snow_chart', '伝記の本文の後、発表メモの前（図：雪の結晶の形）', '3:2',
     '雪の結晶の4つの形を横に並べた図：針状（needle）、板状（plate）、柱状（column）、星形（star）。それぞれの下に英語で小さく名前。',
     '温度や湿度の数値は書かない（設問に関わるため）。'),
    (1, '第7問', 'sleep_brain', 'スライド「Sleep and Learning」の右側（スライドの図）', '1:1',
     '人の頭の横からの輪郭の中に脳。脳の奥の小さな部分（hippocampus）から外側の大きな部分（cortex）へ矢印。横に眠っている人の小さなアイコン。ラベルは「hippocampus」「cortex」の2語だけ。',
     '数字（20–40%）は描かない。'),
    # 第2回
    (2, '第1問', 'foodnight_poster', 'お知らせ「International Food Night」のタイトルの下', '3:2',
     '長いテーブルに各国の家庭料理がならぶ持ち寄りパーティー（巻きずし、タコス、カレー、パスタ、ケーキなど）。皿とフォーク、飲み物のピッチャー。人物は手だけでもよい。',
     '国旗・文字は入れない。料理の数は6〜8皿。'),
    (2, '第2問', 'vocab_apps', '記事「We Tested Three Vocabulary Apps」の表の上', '3:2',
     'スマートフォンの画面を3台横に並べた図：左＝単語カードに「もうすぐ復習」の時計マーク（WordNest）／中＝単語カードに小さな写真と例文の線（Flashly）／右＝ゲーム風のレベル表示と順位表（LexiQuest）。各スマホの下にアプリ名を英語で。',
     '点数（78・71・64）や価格は書かない。'),
    (2, '第3問', 'rugby_bottles', '体験談「The Water Bottle Manager」の本文の横', '1:1',
     'ラグビー場のベンチにずらりと並んだ水筒。それぞれに手書きの名前のラベル（読めない線でよい）。そばに太いマーカーペン1本。後ろにラグビーボール。',
     'カタカナ・英字をはっきり描かない（崩れるため）。人物は描かない。'),
    (2, '第5問', 'lakeland_map', '料金表「Lakeland Coaches」の上（旅行先の地図）', '3:2',
     '湖水地方の簡単な地図：縦に細長い湖「Lake Windermere」（ボート乗り場の小さな船のマーク）と、そこから北へ離れた町「Keswick」（鉛筆のマーク＝Pencil Museum）。2つを結ぶ道。北の矢印。',
     'Keswick は Lake Windermere から離れた北に置く（隣に描かない）。距離・料金は書かない。'),
    (2, '第5問', 'coach_sizes', '料金表「Lakeland Coaches」の左（任意：バスの大きさ）', '3:2',
     'バス3台を小さい順に横に並べた側面図：ミニバス、中型バス、大型バス。',
     '座席数・料金は描かない。'),
    (2, '第6問', 'fog_catcher', '文章「Catching Water from the Clouds」の本文の横（図）', '3:2',
     '丘の上に立つ大きな網（2本の柱に張られた長方形のメッシュ）。左から霧が流れてきて、網に水滴がつき、下のとい（gutter）を通ってタンクにたまる。矢印で水の流れ。ラベルは「fog」「net」「gutter」「tank」の4語。',
     '数値なし。'),
    (2, '第7問', 'anchoring_poster', 'ポスター「The Anchoring Effect」の上', '3:2',
     '左：数字が書かれたルーレット（10 と 65 の位置に針が止まりそうな絵）／右：値札（元値に横線、その下に安い値段）とレストランのメニュー（いちばん上の料理だけ大きく）。',
     'ルーレットの数字は 10 と 65 だけ描く。推測の答え（25%・45%）は書かない。'),
    # 第3回
    (3, '第2問', 'museum_lates', 'ウェブページ「Museum Lates」のタイトルの下（見出し画像）', '3:2',
     '夜の科学博物館の大きなホール。天井から吊られた模型や恐竜の骨格の下で、大人たちが懐中電灯を持って見学している。奥に小さなステージで演奏する人。',
     '子どもは描かない（18歳以上のイベントのため）。文字・時刻なし。'),
    (3, '第3問', 'bakery_photo', '物語「The Picture I Didn\'t Plan」の本文の横（Ren が撮った写真）', '3:2',
     '早朝、小さなパン屋のシャッターを開ける年配の男性を少し離れた所から撮った、自然なスナップ写真風の絵。朝の光、店先の看板（文字なし）。',
     '男性はカメラを見ていない（ポーズをとっていない）こと。'),
    (3, '第5問', 'festival_map', '募集「Meadowfield Music Festival」の表の下（会場の地図・任意）', '3:2',
     '野外フェスの会場の簡単な地図：入口ゲート（Gates）、メインステージ（Main Stage）、案内所（Info Point）、子どもエリア（Kids\' Zone）、リサイクルごみ置き場（Recycling）、ボランティア用キャンプ場（Volunteers\' Campsite、シャワーのマーク）。',
     'ラベルは英語でこの6つだけ。時刻・料金なし。'),
    (3, '第6問', 'gull_point', '物語「The Keeper of Gull Point」の本文の横', '1:1',
     '嵐の夜、岩の岬に立つ灯台。荒れた海に傾いた帆船、灯台の下から小さな手こぎボートを出す人影。',
     '文字なし。'),
    (3, '第7問', 'microplastic_scale', 'スライド「Microplastics」の右側（スライドの図）', '1:1',
     '定規（ミリ目盛り、5 mm の所に印）の横に、色々な形の小さなプラスチックのかけら（つぶ・繊維・破片）をならべた拡大図。ラベルは「5 mm」だけ。',
     '発生源（衣類・タイヤなど）は描かない（設問の答えになるため）。'),
    # 第4回
    (4, '第1問', 'fridge_note', 'メモ「Riku — Weekend To-Do List」の横（冷蔵庫に貼ったメモの雰囲気）', '1:1',
     '冷蔵庫の扉にマグネットで留めたメモ用紙（文字は読めない線）。まわりに小さなイラスト：植木鉢、ネコとえさ皿、ごみ箱。',
     '曜日・時刻は書かない。'),
    (4, '第2問', 'refectory', '記事「Refectory Survey」のタイトルの下', '3:2',
     '大学の食堂。料理カウンターの前に学生の長い列、テーブルで食べる学生たち。',
     '文字・数字なし。'),
    (4, '第3問', 'duck_race', '物語「The Great Duck Race」の本文の横', '3:2',
     '公園の横の細くて静かな運河。たくさんのアヒルのおもちゃ（番号つき）が流れ、両岸に網を持った中学生たちが並び、見物人が応援している。奥に水門（lock）。',
     '石の橋や増水した川は描かない（場面がずれるため）。アヒルの番号は読めなくてよい。'),
    (4, '第6問', 'indigo_dye', '文章「Colours That Last」の本文の横', '1:1',
     '家の裏に並んだ大きな土のつぼ。女性が白い布をつぼから引き上げ、空気にふれた布が少しずつ色が変わっていく様子（白黒なので濃淡で表す）。',
     '文字なし。'),
    (4, '第7問', 'heat_island', 'スライド「The Urban Heat Island Effect」の右側（スライドの図）', '3:2',
     '左から「田園 → 住宅地 → 都心 → 公園 → 住宅地 → 田園」の町並みの断面図。上に気温を表す曲線（都心で高く、公園で少し下がる）。下に緑化した屋上、白い屋根、街路樹、打ち水の小さなアイコンを4つ（ラベルなし）。',
     '気温の数値は書かない。屋根のアイコンに A・B などの記号をつけない。'),
    # 第5回
    (5, '第2問', 'sunfold', 'ウェブサイト「SunFold Portable Solar Charger」の商品説明の横（商品画像）', '3:2',
     '折りたたみ式の太陽光充電器：左に閉じた状態（文庫本くらいの大きさ）、右に広げた状態（パネル3枚）。側面にUSBの差し込み口が2つ。スマートフォンを1台つないでいる。',
     '価格・重さなどの文字なし。USBの口は必ず2つ。'),
    (5, '第3問', 'calligraphy', '体験談「One Character, One Year」の本文の横', '1:1',
     '書道部の部屋。外国人の男子生徒が正座して、大きな筆で半紙に字を書いている。先生がそばで見守る。',
     '半紙の字は筆の動きだけ見せて、字そのものは見えない角度にする（崩れた漢字を描かせないため）。'),
    (5, '第5問', 'green_futures', '要項「Green Futures Challenge 2026」のタイトルの横', '1:1',
     '葉っぱと雨つぶを組み合わせたロゴ風のマーク。下に学校の屋根から雨水をためるタンク（雨どい→タンク）の小さな絵。',
     '文字・日付なし。'),
    (5, '第6問', 'feel_music', '文章「Music You Can Feel」の本文の横', '3:2',
     '木の床の教室で、大きな太鼓を叩く先生。床に座った子どもたちが床やスピーカーに手を当てて振動を感じている。',
     '耳を強調した描写や悲しげな表情にしない。文字なし。'),
    (5, '第7問', 'habit_loop', 'スライド「Building Better Habits」の右側（スライドの図）', '1:1',
     '3つの矢印でつながった輪（ループ）。輪の上に「cue」、右下に「routine」、左下に「reward」の英語ラベル。中央に小さなスマートフォンのアイコン。',
     '日数（21・66 など）は書かない。'),
]


def r_figs():
    out = []
    for n, part, slug, where, aspect, what, note in R_FIGS:
        out.append({'file': f'kyotsu_r{n}_{part[1]}_{slug}.png', 'set': n, 'part': part, 'where': where,
                    'aspect': aspect, 'what': what, 'note': note, 'label': f'第{n}回 {part}'})
    return out
