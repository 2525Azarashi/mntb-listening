"""共通テスト予想問題（リスニング）の「ElevenLabs（Eleven v4）音声 制作指示書」PDF。

  python3 scripts/gacha-prints/kyotsu_mock/build_orders_el.py
  → .tmpwork/kyotsu_mock_elevenlabs_v4.pdf

中身：1 使い方（アプリ／API）／2 声のキャスト（Voice Library の探し方・役名）／3 読み方のルールと設定
      ／4 全トラックの台本（ElevenLabs にそのまま貼れる形：役名＋音声タグ＋英文）／5 納品チェック表
台本・声の割り当ては assets_plan.py から作るので、問題を直したら作り直すだけで追従する。
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assets_plan as A  # noqa: E402
import render as R  # noqa: E402
import build_orders as BO  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, CondPageBreak  # noqa: E402
from reportlab.platypus.flowables import PageBreakIfNotEmpty as PageBreak  # noqa: E402

ROOT = HERE.parent.parent.parent
OUT = ROOT / '.tmpwork' / 'kyotsu_mock_elevenlabs_v4.pdf'
P, E, st, grid, head, S = BO.P, BO.E, BO.st, BO.grid, BO.head, BO.S


def role_rows():
    rows = [['役名', '役', 'Voice Library での探し方（フィルター）', '各行の先頭に付けるタグ']]
    for k, v in A.EL_CAST.items():
        rows.append([k, v['ja'], v['search'], v['tag'] or '（なし）'])
    return rows


def usage_rows(n):
    """第n回で各役が出てくる問題"""
    seen = {}
    for t in A.tracks(n):
        for role, _, _ in A.el_track(t):
            seen.setdefault(role, []).append(A.q_label(t['marks']))
    rows = [['役名', '役', '出てくる問題']]
    for role in A.EL_CAST:
        if role in seen:
            qs = list(dict.fromkeys(seen[role]))
            rows.append([role, A.EL_CAST[role]['ja'], '・'.join(qs[:10]) + ('…' if len(qs) > 10 else '')])
    rows.append(['JA', A.EL_CAST['JA']['ja'], '問番号・指示文・「もう一度読みます。」'])
    return rows


def track_block(t):
    gaps = []
    if A.PAUSE_PREVIEW.get(t['part']) and t['intro_ja'].startswith('第'):
        gaps.append(f'先読み{A.PAUSE_PREVIEW[t["part"]]}秒')
    gaps.append(f'解答{A.PAUSE_ANSWER[t["part"]]}秒')
    lines = A.el_track(t)
    chars = sum(len(x[2]) for x in lines)
    title = (f'<font name="JPB">{R.esc(t["label"])}</font>　→　<font name="EN">{t["file"]}</font>'
             f'　（{t["times"]}回読み・{"・".join(gaps)}・約{chars}字）')
    rows = [[Paragraph('<font name="JPB" size="8">JA</font>', st['tc']), Paragraph(R.esc(t['intro_ja']), st['tc'])]]
    if t['situation']:
        rows.append([Paragraph('<font name="JPB" size="8">場面</font>', st['tc']),
                     Paragraph(R.esc(t['situation']) + '（問題冊子に書いてある。読まない）', st['tc'])])
    for role, sp, text in lines:
        v = f'<font name="ENB">{R.esc(role)}</font><br/><font name="EN" size="7">{R.esc(sp)}</font>'
        rows.append([Paragraph(v, S('sp3', fontSize=8.4, leading=10.5)), E(text)])
    tb = Table(rows, colWidths=[26 * mm, R.W - 26 * mm])
    tb.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, R.BLACK),
                            ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.HexColor('#999999')),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3),
                            ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]))
    return [Paragraph(title, st['ps']), tb, Spacer(1, 3 * mm)]


def build():
    tr = {n: A.tracks(n) for n in A.SETS}
    n_tr = sum(len(v) for v in tr.values())
    chars = sum(len(x[2]) for v in tr.values() for t in v for x in A.el_track(t))
    doc = R.make_doc(OUT, '共通テスト予想問題 ElevenLabs v4 音声制作指示書', '共通テスト予想問題　音声の制作指示書（ElevenLabs v4）')
    story = R.cover_story(
        '大学入学共通テスト 予想問題（LR プリント）第1回〜第5回　リスニング',
        '音声の制作指示書\n（ElevenLabs・Eleven v4）',
        '声のキャスト・読み方のルール・全トラックの台本（そのまま貼れる形）\nアプリで1問ずつ作っても、付属スクリプトで一括作成してもよい',
        [(f'{n_tr}', '音声トラック'), (f'{len(A.EL_CAST)}', '声の役'), (f'約{chars // 1000}千字', '英文（1回分）'), ('v4', 'モデル')],
        ['**モデル**は Eleven v4（API の model_id は `eleven_v4`）。2人以上が話す問題は **Dialogue（対話）** で1回に生成する。',
         '**最初に「2 声のキャスト」**で12の役に声を決める。イギリス英語・非母語話者の役は、必ずそのなまりの声を Voice Library から選ぶ（v4 は声のなまりを英語に持ち込まないため）。',
         '**台本の [ ] は音声タグ**（読まれない演技の指示）。そのまま貼ってよい。長い無音（先読み・解答時間）はつなぐときに入れる。',
         '**一括で作るなら** `make_audio_el.py`（API キーと声の ID を入れて実行）。全120トラックの作成・つなぎ合わせ・通し音声まで自動。'],
        [('1', '使い方（アプリで作る／API で一括）'), ('2', '声のキャスト（12役）'), ('3', '読み方のルールと設定'),
         ('4', f'全{n_tr}トラックの台本（第1回〜第5回）'), ('5', '納品ファイル一覧（チェック表）')])

    story += head('1', '使い方')
    story += [P('**A．ElevenLabs のアプリで1問ずつ作る**', 'h3'),
              P('① 「2 声のキャスト」の表どおり、Voice Library で声を12個選んで「My Voices」に追加する（役名をメモ）。', 'li'),
              P('② Text to Speech を開き、モデルを **Eleven v4** にする。1人で話す問題はそのまま、2人以上の問題は **Dialogue** に切り替える。', 'li'),
              P('③ 「4 台本」の1トラック分を、行ごとに声を選んで貼る（役名の声を使う）。[ ] のタグも一緒に貼る。Stability は 0.5 前後。', 'li'),
              P('④ 生成した英語の部分をダウンロードし、ファイル名どおりに保存。日本語の案内（JA の行）も同じように作る。', 'li'),
              P('⑤ 編集ソフトで「案内 →（先読み）→ 英語 →（2回読みは「もう一度読みます。」と同じ英語をもう一度）→ 解答の間」の順につなぐ。', 'li'),
              P('**B．API で一括作成（おすすめ）**', 'h3'),
              BO.prompt_box(['export ELEVENLABS_API_KEY=...（自分のキー）',
                             'cp scripts/gacha-prints/kyotsu_mock/el_voices.example.json scripts/gacha-prints/kyotsu_mock/el_voices.json',
                             '　→ el_voices.json を開き、役名ごとに選んだ声の voice_id を書く（Voice Library の声の「ID をコピー」）',
                             'python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py --dry-run　← 台本・役・文字数の確認（課金なし）',
                             'python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py 1　← まず第1回だけ作って聞いてみる',
                             'python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py　← 5回分すべて',
                             f'出力：{A.ASSET_DIR}/audio/ に1問ごとの mp3（{n_tr}本）と各回の通し mp3（5本）'],
                            caption='▼ ターミナルで実行（ffmpeg が必要）'),
              Spacer(1, 2 * mm),
              P(f'・使う文字数は、英文が約{chars:,}字、日本語の案内を合わせて約3.2万字（2回読みは同じ音声を使い回すので、文字数は1回分）。生成済みの部品は保存され、やり直しても同じ台本は再生成しない。', 'li'),
              P('・料金はキーの持ち主の ElevenLabs のプラン（月の文字数枠）から引かれる。最新のプラン表で確認してください。', 'li'),
              PageBreak()]

    story += head('2', f'声のキャスト（{len(A.EL_CAST)}役）')
    story += [P('Voice Library で、表のフィルター（Language・Accent・Gender・Age・Use case）を使って探す。試し聞きで「はっきり・落ち着いた・速すぎない」声を選ぶ。キャラクター声・ささやき声・ナレーションが芝居がかった声は避ける。', 'ps'),
              Spacer(1, 2 * mm),
              grid(role_rows(), [16 * mm, 38 * mm, 68 * mm, R.W - 122 * mm], size=8.2), Spacer(1, 3 * mm),
              P('・**W_us と W_us2（M_us と M_us2）は声の高さ・年齢がはっきり違う2人**にする。同じ問題に同じ性別の話し手が2人出てくるときに使う。', 'li'),
              P('・**W_uk・M_uk** はイギリス（Southern English / RP）の声。**W_nn・M_nn** は英語を話すスペインやインドなどの声で、なまりは軽く、聞き取りやすいもの。', 'li'),
              P('・**JA** は日本語の声。問番号・指示文・「もう一度読みます。」だけを読む。', 'li'),
              PageBreak()]

    story += head('3', '読み方のルールと設定')
    for k, r in enumerate(A.EL_RULES, 1):
        story.append(P(f'{k}．{r}', 'li'))
    story += [Spacer(1, 2 * mm), P('**つなぎ方（無音の長さ）**', 'h3')]
    rows = [['大問', '読む回数', '先読みの間', '1回目と2回目の間', '解答の間']]
    for part in ['第1問', '第2問', '第3問', '第4問', '第5問', '第6問']:
        times = '2回' if part in ('第1問', '第2問') else '1回'
        rows.append([part, times, f'{A.PAUSE_PREVIEW[part]}秒' if part in A.PAUSE_PREVIEW else '—',
                     f'{A.PAUSE_REPEAT}秒＋「もう一度読みます。」' if times == '2回' else '—', f'{A.PAUSE_ANSWER[part]}秒'])
    story += [grid(rows, [22 * mm, 20 * mm, 26 * mm, 50 * mm, R.W - 118 * mm]), Spacer(1, 3 * mm),
              P('**よく使う音声タグ（必要なときだけ）**', 'h3'),
              grid([['タグ', '使う場面'],
                    ['[pause]', '講義や長いせりふの段落の切れ目（文中の短い間は「…」やカンマでよい）'],
                    ['[British accent]', 'イギリス英語の役（声もイギリスの声にする）'],
                    ['[light Spanish accent, speaking clearly and a little slowly]', '非母語話者の役（声もそのなまりの声にする）'],
                    ['[calm university lecturer, measured pace]', '第5問の講義'],
                    ['[neutral exam announcer]', '第2問の「Question: …」の読み手'],
                    ['（使わない）[excited] [laughs] [whispers] など', '試験音声には感情・効果音のタグは入れない']],
                   [70 * mm, R.W - 70 * mm]),
              PageBreak()]

    story += head('4', f'全{n_tr}トラックの台本')
    story.append(P('左の列が**役名**（2章の声）、右が**そのまま貼る本文**（[ ] は音声タグ）。「JA」は日本語の案内、「場面」は問題冊子に印刷済みで読まない。', 'ps'))
    for n in A.SETS:
        story += [R.bar(f'第{n}回　リスニング（{len(tr[n])}トラック）'), Spacer(1, 2 * mm), P('**この回で使う役**', 'h3'),
                  grid(usage_rows(n), [18 * mm, 50 * mm, R.W - 68 * mm]), Spacer(1, 3 * mm)]
        for t in tr[n]:
            story.append(CondPageBreak(min(80, 20 + 8 * len(t['lines'])) * mm))
            story += track_block(t)
        story.append(PageBreak())

    story += head('5', '納品ファイル一覧（チェック表）')
    rows = [['□', 'ファイル名', '内容']]
    for n in A.SETS:
        for t in tr[n]:
            rows.append(['□', t['file'], t['label']])
        rows.append(['□', f'kyotsu_l{n}_full.mp3', f'第{n}回 リスニング 通し'])
    story.append(grid(rows, [7 * mm, 62 * mm, R.W - 69 * mm], size=8))
    doc.build(story)
    print(OUT, R.pdf_pages(OUT), 'pages')


if __name__ == '__main__':
    OUT.parent.mkdir(exist_ok=True)
    build()
