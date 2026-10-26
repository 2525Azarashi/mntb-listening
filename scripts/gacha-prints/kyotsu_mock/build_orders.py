"""共通テスト予想問題（LR）の「素材の制作指示書」PDF を1冊にまとめる（ChatGPT に貼るプロンプト集）。

  python3 scripts/gacha-prints/kyotsu_mock/build_orders.py
  → .tmpwork/kyotsu_mock_seisaku_shijisho.pdf

中身：1 使い方／2 画像の共通スタイル／3 リスニングの絵（34）／4 地図（4）／5 リーディングの図（29）
      ／6 音声（声の割り当て・読み方のルール・全トラックの台本）／7 納品ファイル一覧（チェック表）
一覧は assets_plan.py から作るので、問題を直したら作り直すだけで追従する。
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assets_plan as A  # noqa: E402
import render as R  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether, CondPageBreak  # noqa: E402
from reportlab.platypus.flowables import PageBreakIfNotEmpty as PageBreak  # noqa: E402

ROOT = HERE.parent.parent.parent
OUT = ROOT / '.tmpwork' / 'kyotsu_mock_seisaku_shijisho.pdf'

S = R.S
st = {
    'h2': S('oh2', font='JPB', fontSize=15, leading=21, spaceBefore=4, spaceAfter=4),
    'h3': S('oh3', font='JPB', fontSize=11.5, leading=16, spaceBefore=3, spaceAfter=2),
    'p': S('op', fontSize=10, leading=15.5),
    'ps': S('ops', fontSize=9, leading=13.2),
    'li': S('oli', fontSize=10, leading=15.5, leftIndent=5 * mm, firstLineIndent=-5 * mm),
    'pr': S('opr', fontSize=9.4, leading=14),           # プロンプト本文（和文）
    'pre': S('opre', font='EN', fontSize=9.6, leading=13.4),  # 英語の台本
    'cap': S('ocap', font='JPB', fontSize=8.5, leading=11),
    'tc': S('otc', fontSize=8.6, leading=11.6),
}


def P(text, style='p'):
    return Paragraph(R.ml(text), st[style])


def E(text, style='pre'):
    return Paragraph(R.en(text), st[style])


def prompt_box(lines, caption='▼ ChatGPT にこのまま貼る'):
    flows = [Paragraph(caption, st['cap']), Spacer(1, 1.5)]
    flows += [P(l, 'pr') for l in lines]
    t = Table([[flows]], colWidths=[R.W])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.9, R.BLACK), ('LINEBEFORE', (0, 0), (0, -1), 3, R.BLACK),
                           ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f4f4f4')),
                           ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    return t


def grid(rows, widths, header=True, size=8.6):
    data = [[c if not isinstance(c, str) else Paragraph(R.en(c), S('g', fontSize=size, leading=size + 3)) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    sty = [('GRID', (0, 0), (-1, -1), 0.5, R.BLACK), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
           ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header:
        sty.append(('BACKGROUND', (0, 0), (-1, 0), R.GRAY))
    t.setStyle(TableStyle(sty))
    return t


def head(no, title):
    return [R.bar(f'{no}　{title}'), Spacer(1, 3 * mm)]


# ───────── 共通スタイル（画像） ─────────
STYLE = [
    '【共通スタイル】これから大学入学共通テスト（英語）の予想問題に載せるイラストを何枚もお願いします。全部この条件で描いてください。',
    '・本番の問題冊子と同じ、**白黒の線画**。黒い線だけで描き、塗りは白。影や区別が必要なときだけ、うすいグレーの網かけを1段階まで。',
    '・色、グラデーション、写真風、3D、アニメ調の強い表現は使わない。教科書の挿絵のような、シンプルで落ち着いたタッチ。',
    '・背景は白。細かい描き込みより「違いがひと目でわかる」ことを優先。',
    '・**画像の中に文字・数字・記号を入れない**（各指示で英語のラベルを指定した場合だけ、その語をはっきりした活字体で入れる）。選択肢の番号①〜④はこちらで後から入れるので描かない。',
    '・人物は特定の実在人物に似せない。年齢・人数・持ち物・動作は指示どおりに正確に。',
    '・指示にないものを足さない（答えのヒントになったり、別の選択肢と区別できなくなったりするため）。',
    'この条件を覚えたら「OK」とだけ答えてください。次のメッセージから1枚ずつ指示します。',
]


def pics_prompt(p):
    pos = ['左上', '右上', '左下', '右下']
    lines = [f'【{p["label"]}】ファイル名：{p["file"]}　（縦横比 3:2・横長）',
             '1枚の画像を細い黒線で**2×2の4つの枠**に区切り、同じ大きさで並べてください。枠の中の場面は次のとおり。']
    for i, d in enumerate(p['descs']):
        lines.append(f'・{pos[i]}の枠：{d}')
    if p['kind'] == 'order':
        lines.append('4つの枠には**同じ人物**（同じ髪型・服装）を描いてください。枠の並びは出来事の順ではありません（このままの位置で描く）。')
    else:
        lines.append('4枚の絵は、上に書いた**違いの点だけ**が変わり、それ以外（人物・向き・背景・物の大きさ）はそろえてください。違いの点ははっきり大きく見えるように。')
    lines.append('白黒の線画、文字・数字なし（共通スタイルどおり）。')
    return lines


def map_prompt(m):
    lines = [f'【{m["label"]}】ファイル名：{m["file"]}　（縦横比 {m["aspect"]}・横長）',
             f'{m["title"]}を、真上から見た簡単な見取り図として描いてください。']
    lines += [f'・{x}' for x in m['layout']]
    lines.append('英語のラベルは指定した語だけを活字体で。丸数字①〜④は**描かずに、その位置に直径の同じ白い丸を置く**（番号はこちらで入れる）。')
    lines.append('白黒の線画、地図記号は簡単なもの（木＝丸い木、車＝四角）でよい。')
    return lines


def rfig_prompt(f):
    return [f'【{f["label"]}】ファイル名：{f["file"]}　（縦横比 {f["aspect"]}）',
            f'{f["what"]}',
            f'注意：{f["note"]}',
            '白黒の線画（共通スタイルどおり）。']


# ───────── 音声 ─────────
AUDIO_RULES = [
    '**第1問・第2問は2回**、**第3〜6問は1回**だけ読む（本番と同じ）。2回読む問題は、1回目と2回目のあいだに約4秒あける。',
    '各問の前に日本語の案内（例「問1。」）を入れる。大問・A/B の最初は、問題冊子の指示文も日本語で読む。',
    f'解答の間（読み終えてから次の問題まで）：第1〜3問 8秒／第4問 15秒／第5問 30秒／第6問 20秒。',
    f'先読みの間（日本語の案内のあと、英語が始まる前）：第4問 15秒／第5問 60秒（ワークシートを読む時間）／第6問 20秒。',
    '話し手が替わるときは0.5〜1秒あける。「Question: …」は問いの読み手（Narrator）の声で読む。',
    '話し手の欄が空いている行（第5問の講義の続きなど）は、直前の話し手がそのまま読み続ける。',
    'なまりの指定：「British」＝イギリス英語、「non-native」＝非母語話者（軽いなまり・少しゆっくり）、それ以外はアメリカ英語。講義は落ち着いた講師の口調。',
    '速さの目安：1分間に140〜150語（講義は130〜140語）。本番よりはっきり速くしない。',
]


def cast_rows(n):
    """第n回の声の割り当て表（同じ話し手名は同じ声）"""
    seen = {}
    for t in A.tracks(n):
        for sp, v in t['cast'].items():
            key = (v['who'], v['voice'])
            seen.setdefault(key, []).append(A.q_label(t['marks']))
    rows = [['話し手', 'OpenAI の声', '出てくる問題']]
    for (who, voice), qs in seen.items():
        qs2 = list(dict.fromkeys(qs))
        rows.append([who, voice, '・'.join(qs2[:8]) + ('…' if len(qs2) > 8 else '')])
    rows.append([A.NARRATOR['who'], A.NARRATOR['voice'], '第2問の「Question: …」'])
    rows.append([A.JA_NARRATOR['who'], A.JA_NARRATOR['voice'], '問番号・指示文・「もう一度読みます」'])
    return rows


def track_flow(t):
    gaps = []
    if A.PAUSE_PREVIEW.get(t['part']) and t['intro_ja'].startswith('第'):
        gaps.append(f'先読み{A.PAUSE_PREVIEW[t["part"]]}秒')
    gaps.append(f'解答{A.PAUSE_ANSWER[t["part"]]}秒')
    title = f'<font name="JPB">{R.esc(t["label"])}</font>　→　<font name="EN">{t["file"]}</font>　（{t["times"]}回読み・{"・".join(gaps)}）'
    out = [Paragraph(title, st['ps'])]
    rows = [[Paragraph('<font name="JPB" size="8">案内</font>', st['tc']), Paragraph(R.esc(t['intro_ja']), st['tc'])]]
    if t['situation']:
        rows.append([Paragraph('<font name="JPB" size="8">場面</font>', st['tc']), Paragraph(R.esc(t['situation']) + '（読まない）', st['tc'])])
    for ln in t['lines']:
        v = (f'<font name="ENB">{R.esc(ln["speaker"])}</font><br/>'
             f'<font name="EN" size="7">{ln["voice"]}</font><font size="7">・{A.ACCENT_JA[ln["accent"]]}</font>')
        rows.append([Paragraph(v, S('sp2', fontSize=8.4, leading=10.5)), E(ln['text'])])
    tb = Table(rows, colWidths=[30 * mm, R.W - 30 * mm])
    tb.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, R.BLACK), ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.HexColor('#999999')),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3),
                            ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]))
    return out + [tb, Spacer(1, 3 * mm)]


def build():
    all_tracks = {n: A.tracks(n) for n in A.SETS}
    all_pics = [p for n in A.SETS for p in A.pics(n)]
    all_maps = A.maps()
    all_rf = A.r_figs()
    n_tr = sum(len(v) for v in all_tracks.values())
    n_img = len(all_pics) + len(all_maps) + len(all_rf)

    doc = R.make_doc(OUT, '共通テスト予想問題 素材の制作指示書', '共通テスト予想問題　素材の制作指示書（音声・画像）')
    story = R.cover_story(
        '大学入学共通テスト 予想問題（LR プリント）第1回〜第5回',
        '素材の制作指示書\n（音声・イラスト・図）',
        'ChatGPT に貼るプロンプト集　＋　リスニング全トラックの台本\nこの1冊にある素材がそろえば、問題冊子を本番と同じ形（音声つき・絵つき）にできます',
        [(f'{n_tr}', '音声トラック'), (f'{len(all_pics)}', 'リスニングの絵'), (f'{len(all_maps)}', '地図'), (f'{len(all_rf)}', 'リーディングの図')],
        ['**画像**：ChatGPT（画像生成が使えるプラン）で、まず「2 共通スタイル」を貼り、そのあと各プロンプトを**1つずつ**貼る。できた画像は指定のファイル名で保存する。',
         '**音声**：ChatGPT の会話画面からは MP3 を書き出せないため、**OpenAI の API キー**で付属の `make_audio.py` を実行するのがいちばん確実（全120トラックを自動で作成・つなぎ合わせ）。手で作る場合は「6 音声」の台本を、声の割り当てどおり読み上げアプリや人に読んでもらう。',
         '絵・図は**答えのヒントにならない**ことが最優先。各プロンプトの「注意」は必ず守る。思った絵にならないときは「〇〇だけ直して、ほかはそのまま」と同じ会話で頼む。',
         'できたファイルはまとめて zip にして、このチャットかハブに上げてください。こちらで問題冊子の PDF に組み込み、アプリのガチャ景品（LR）を差し替えます。'],
        [('1', '使い方と全体の流れ'), ('2', '画像の共通スタイル（最初に1回だけ貼る）'),
         ('3', f'リスニングの絵（4択・4コマ）{len(all_pics)}枚'), ('4', f'リスニングの地図・見取り図 {len(all_maps)}枚'),
         ('5', f'リーディングの図・イラスト {len(all_rf)}枚'), ('6', f'音声：声の割り当て・読み方のルール・全{n_tr}トラックの台本'),
         ('7', '納品ファイル一覧（チェック表）')])

    # 1 使い方
    story += head('1', '使い方と全体の流れ')
    story += [P('**画像（67枚）**', 'h3'),
              P('① ChatGPT で新しいチャットを開く → ②「2 共通スタイル」の枠の中を貼る → ③「OK」と返ってきたら、3〜5章のプロンプトを1つずつ貼る → ④できた画像をダウンロードし、プロンプトの先頭にあるファイル名に変える。', 'li'),
              P('・20枚くらいで画像のタッチがずれてきたら、新しいチャットで②からやり直す。', 'li'),
              P('・4択の絵は**1枚の画像を2×2に区切って**描いてもらう（左上＝①、右上＝②、左下＝③、右下＝④）。こちらで切り分けて、本番と同じく横一列に並べ、番号を入れる。', 'li'),
              P('・地図の①〜④は白い丸だけ描いてもらい、番号はこちらで入れる（画像生成は丸数字がよく崩れるため）。', 'li'),
              P('**音声（120トラック）**', 'h3'),
              P('おすすめ：API で自動作成（台本・声・間の取り方はこの指示書と同じ設定が入っています）。', 'p'),
              prompt_box(['export OPENAI_API_KEY=sk-...（自分のキー）',
                          'python3 scripts/gacha-prints/kyotsu_mock/make_audio.py --dry-run　← 台本の確認だけ（課金なし）',
                          'python3 scripts/gacha-prints/kyotsu_mock/make_audio.py　← 5回分を作成',
                          '出力：public/prints/kyotsu_assets/audio/ に 1問ごとの mp3（120本）と 各回の通し mp3（5本）'],
                         caption='▼ ターミナルで実行（ffmpeg が必要）'),
              Spacer(1, 2 * mm),
              P(f'・読み上げる英文と日本語の案内は重複を除いて約3万字。モデルは gpt-4o-mini-tts（声とアクセントを指示できる）。料金はキーの持ち主の OpenAI アカウントにかかります（目安は数ドル程度。最新の料金表で確認してください）。', 'li'),
              P('・手で作る場合：「6 音声」のトラックごとに、案内 →（先読みの間）→ 英文 →（2回読みならもう一度）→ 解答の間、の順で録音し、ファイル名どおりに保存する。', 'li'),
              P('**置き場所（こちらで組み込むときの場所）**', 'h3'),
              P(f'画像：{A.ASSET_DIR}/img/　音声：{A.ASSET_DIR}/audio/　（zip で渡してもらえれば、こちらで配置します）', 'p'),
              PageBreak()]

    # 2 共通スタイル
    story += head('2', '画像の共通スタイル（最初に1回だけ貼る）')
    story += [prompt_box(STYLE), Spacer(1, 4 * mm),
              P('**うまくいかないときの直し方（同じチャットで送る）**', 'h3')]
    for t in ['「色がついています。白黒の線画だけにして、ほかはそのままで描き直してください。」',
              '「文字や数字が入っています。画像の中の文字をすべて消して描き直してください。」',
              '「右下の枠だけ、〇〇が△△になるように直してください。ほかの3つは変えないで。」',
              '「4つの枠の人物が別人に見えます。同じ髪型・同じ服装にそろえてください。」']:
        story.append(P('・' + t, 'li'))
    story.append(PageBreak())

    # 3 リスニングの絵
    story += head('3', f'リスニングの絵（4択・4コマ）　全{len(all_pics)}枚')
    story.append(P('各プロンプトの下の「正解・台本」は**描く人の確認用**です（ChatGPT に貼らなくてよい）。正解の絵が台本どおりに見えるか、ほかの3枚と取り違えないかを確認してください。', 'ps'))
    story.append(Spacer(1, 2 * mm))
    for p in all_pics:
        block = [prompt_box(pics_prompt(p))]
        chk = ('台本：' + ' / '.join(p['script'][:6]))[:520]
        if p['prompt']:
            chk = f'問い：{p["prompt"]}　' + chk
        block += [Paragraph(R.en(chk), S('chk', fontSize=8, leading=11, color=colors.HexColor('#333333'))), Spacer(1, 4 * mm)]
        story.append(KeepTogether(block))
    story.append(PageBreak())

    # 4 地図
    story += head('4', f'リスニングの地図・見取り図　全{len(all_maps)}枚')
    for m in all_maps:
        block = [prompt_box(map_prompt(m)),
                 Paragraph(R.en(f'確認：{m["check"]}　問い：{m["prompt"]}　台本：' + ' / '.join(m['script'])),
                           S('chk2', fontSize=8, leading=11, color=colors.HexColor('#333333'))), Spacer(1, 4 * mm)]
        story.append(KeepTogether(block))
    story.append(PageBreak())

    # 5 リーディング
    story += head('5', f'リーディングの図・イラスト　全{len(all_rf)}枚')
    story.append(P('本番のリーディングは、チラシ・ウェブサイト・ブログ・スライドに写真や図が入っています。下の場所に入れると本番に近い見た目になります。「任意」と書いたものは無くても解けます。', 'ps'))
    story.append(Spacer(1, 2 * mm))
    for n in A.SETS:
        story.append(P(f'第{n}回', 'h3'))
        for f in [x for x in all_rf if x['set'] == n]:
            story.append(KeepTogether([Paragraph(f'<font name="JPB">入れる場所：</font>{R.esc(f["where"])}', st['ps']), Spacer(1, 1),
                                       prompt_box(rfig_prompt(f)), Spacer(1, 4 * mm)]))
    story.append(PageBreak())

    # 6 音声
    story += head('6', f'音声：声の割り当て・読み方のルール・全{n_tr}トラックの台本')
    story.append(P('**読み方のルール（全回共通）**', 'h3'))
    for k, r in enumerate(AUDIO_RULES, 1):
        story.append(P(f'{k}．{r}', 'li'))
    story += [Spacer(1, 2 * mm), P('**OpenAI TTS に渡す読み方の指示（instructions）**', 'h3')]
    rows = [['なまり', 'instructions（英語のまま渡す）']] + [[A.ACCENT_JA[k], v] for k, v in A.ACCENT.items()]
    story += [grid(rows, [34 * mm, R.W - 34 * mm]), Spacer(1, 3 * mm),
              P('**人に読んでもらう／読み上げアプリを使う場合**：男女の声を分け、同じ名前の話し手は同じ人（同じ声）に。「British」「non-native」の指定がある行は、その話し方ができる声を選ぶ（無ければアメリカ英語で可。ただし男女は必ず守る）。', 'ps'),
              PageBreak()]
    for n in A.SETS:
        story += [R.bar(f'第{n}回　リスニング（{len(all_tracks[n])}トラック）'), Spacer(1, 2 * mm), P('**声の割り当て**', 'h3'),
                  grid(cast_rows(n), [62 * mm, 24 * mm, R.W - 86 * mm]), Spacer(1, 3 * mm), P('**台本**', 'h3')]
        for t in all_tracks[n]:
            story.append(CondPageBreak(min(80, 20 + 8 * len(t['lines'])) * mm))
            story += track_flow(t)
        story.append(PageBreak())

    # 7 チェック表
    story += head('7', '納品ファイル一覧（チェック表）')
    rows = [['□', 'ファイル名', '種類', '入る場所']]
    for p in all_pics:
        rows.append(['□', p['file'], '絵（2×2）', p['label']])
    for m in all_maps:
        rows.append(['□', m['file'], '地図', m['label']])
    for f in all_rf:
        rows.append(['□', f['file'], '図', f['label'] + '　' + f['where'][:28]])
    for n in A.SETS:
        rows.append(['□', f'kyotsu_l{n}_q01.mp3 〜 kyotsu_l{n}_q36-37.mp3（{len(all_tracks[n])}本）', '音声', f'第{n}回 リスニング'])
        rows.append(['□', f'kyotsu_l{n}_full.mp3', '音声（通し）', f'第{n}回 リスニング 全体'])
    story.append(grid(rows, [7 * mm, 72 * mm, 22 * mm, R.W - 101 * mm], size=8))
    doc.build(story)
    print(OUT, R.pdf_pages(OUT), 'pages')


if __name__ == '__main__':
    OUT.parent.mkdir(exist_ok=True)
    build()
