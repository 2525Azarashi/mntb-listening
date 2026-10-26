"""英文解釈（リーディング）に入れる動画・図のプロンプト PDF（2026-10-26）。

  python3 scripts/firefly-kit/build_reading_media.py [出力先=/tmp/firefly_kit]

出力：Firefly_リーディング用_動画と図.pdf（全部コピペできる文字で入れる）
  1. 設定（Firefly Video / Firefly Image）
  2. 読む画面の動画 R01〜R07（カード画像は build_kit.py が作った cards/ を使う）
  3. 英文60本の扉絵（Firefly Image）
  4. UR 本「リーディング大問別演習」の図
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reading_media as RM
import videos as VD

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/firefly_kit')
PDF_NAME = 'Firefly_リーディング用_動画と図.pdf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'


def main():
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
    pdfmetrics.registerFont(TTFont('JP', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
    pdfmetrics.registerFont(TTFont('MONO', MONO))
    P = lambda n, **k: ParagraphStyle(n, fontName=k.pop('f', 'JP'), **k)
    h1 = P('h1', fontSize=20, leading=28, textColor=colors.HexColor('#172a4f'), spaceAfter=6)
    h2 = P('h2', fontSize=13.5, leading=19, textColor=colors.HexColor('#2458a6'), spaceBefore=8, spaceAfter=4)
    b = P('b', fontSize=9.6, leading=14.5)
    sm = P('sm', fontSize=8.4, leading=12, textColor=colors.HexColor('#555555'))
    mono = P('m', f='MONO', fontSize=7.8, leading=10.4)
    e = lambda s: str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    GRID = [('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#c9ced8')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eef9')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
    pg = landscape(A4)
    doc = SimpleDocTemplate(str(OUT / PDF_NAME), pagesize=pg, leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=11 * mm, bottomMargin=11 * mm, title='リーディング用 動画と図（Adobe Firefly）', author='まなとび')
    s = [Paragraph('英文解釈（リーディング）に入れる 動画と図のプロンプト', h1),
         Paragraph(f'2026-10-26 ／ 動画 {len(RM.READING_VIDEOS)} 本（Firefly Video）＋ 扉絵 {len(RM.PASSAGE_ART)} 枚 ＋ 本の図 {len(RM.BOOK_FIGURES)} 枚（Firefly Image）。'
                   'プロンプトはすべて文字で入れてあるので、PDF から選択してそのまま貼れる。', b),
         Paragraph('1. 設定', h2)]
    rows = [['', '動画（R01〜R07）', '図・扉絵（r1-01〜r5-12・F01〜）'],
            ['モデル', 'Firefly Video（パートナーモデルは使わない）', 'Firefly Image（最新の Firefly Image モデル。パートナーモデルは使わない）'],
            ['縦横', 'Square 1:1 ／ 1080p ／ 5秒', 'Square 1:1（扉絵）・本の図も 1:1'],
            ['参照', '★First と Last の両方に refs/ のとびら君の画像を必ず入れる（片方でも空にすると別キャラになる）', '扉絵・図はとびら君が出ない絵なので参照なし。とびら君を入れたい絵は Composition 参照に refs/transparent/ の画像を入れる'],
            ['Content type', '—', 'Art（イラスト）'],
            ['Enhance prompt', 'オフ', '—'],
            ['禁止', '文字・数字・記号が出たら作り直し', '文字・数字・ロゴが出たら作り直し。グラフの目盛りや数字はアプリ側で描くのでイラストに入れない'],
            ['ファイル名', 'R01.mp4 など ID.mp4', '扉絵＝r1-01.png など英文の ID、本の図＝F01.png など']]
    t = Table([[Paragraph(e(c), b) for c in r] for r in rows], colWidths=[32 * mm, 110 * mm, 131 * mm])
    t.setStyle(TableStyle(GRID)); s += [t]
    s += [Paragraph('どこに入るか', h2)]
    for x in ['R01〜R04：英文解釈を読む画面の上（いまの静止画のとびら君の位置）。緑背景で作り、とびら君だけ透過にする',
              'R05・R06：結果画面（1本読み終えた／レベルを全部読み終えた）。クリーム背景のまま',
              'R07：UR 本「リーディング大問別演習」を開いたとき',
              '扉絵：英文を読み始める前に1枚だけ見せる（内容を想像させる）。60本の題名と1対1',
              '本の図：UR 本の大問ページ（本番は第4問以外のほぼ全大問に図・写真が出る）']:
        s.append(Paragraph('・' + e(x), b))
    s += [Paragraph('共通の画風（扉絵・図のプロンプトの最後に入れてある）', b), Paragraph(e(RM.IMG_STYLE), mono)]

    # 2. 動画
    s += [PageBreak(), Paragraph('2. 読む画面の動画（R01〜R07・Firefly Video）', h2)]
    rows = [['ID', '名前', '種類', '優先', '秒', 'First → Last', 'どこで使う・動き']]
    for v in RM.READING_VIDEOS:
        rows.append([v['id'], v['name'], '背景なし（緑）' if v['kind'] == 'motion' else '全画面（クリーム）', v['prio'],
                     v['sec'] + ('↻' if v['loop'] else ''), f"refs/{v['first'].replace(':', '/')}.png → refs/{v['last'].replace(':', '/')}.png",
                     f"{v['where']}\n{v['ja']}"])
    t = Table([[Paragraph(e(c).replace('\n', '<br/>'), sm) for c in r] for r in rows],
              colWidths=[11 * mm, 25 * mm, 28 * mm, 10 * mm, 12 * mm, 70 * mm, 117 * mm], repeatRows=1)
    t.setStyle(TableStyle(GRID)); s += [t, Spacer(1, 6)]
    for v in RM.READING_VIDEOS:
        s += [Paragraph(f"<b>{v['id']} {v['name']}</b>　Prompt（そのまま貼る）", b),
              Paragraph(e(VD.prompt(v)).replace('\n', '<br/>'), mono), Spacer(1, 4)]
    for v in RM.READING_VIDEOS:
        c = OUT / 'cards' / f"{v['id']}_{v['name']}.png"
        if c.exists():
            s += [PageBreak(), RLImage(str(c), width=pg[0] - 24 * mm, height=(pg[0] - 24 * mm) * 1000 / 1600)]

    # 3. 扉絵
    s += [PageBreak(), Paragraph(f'3. 英文{len(RM.PASSAGE_ART)}本の扉絵（Firefly Image・1:1）', h2),
          Paragraph('ID はアプリの英文の ID（src/data/reading/level1〜5.ts）。r1＝Lv1 … r5＝Lv5。', sm)]
    rows = [['ID', '英文の題名', 'Prompt（そのまま貼る）']]
    for pid, title, subj in RM.PASSAGE_ART:
        rows.append([Paragraph(e(pid), sm), Paragraph(e(title), sm), Paragraph(e(RM.image_prompt(subj)), mono)])
    t = Table(rows, colWidths=[14 * mm, 52 * mm, 207 * mm], repeatRows=1)
    t.setStyle(TableStyle(GRID)); s += [t]

    # 4. 本の図
    s += [PageBreak(), Paragraph(f'4. UR 本「リーディング大問別演習」の図（Firefly Image・1:1）', h2),
          Paragraph('数字・目盛りの入るグラフは本を作るスクリプトで描く。ここは「場面のイラスト」と「形の参考」だけ。', sm)]
    rows = [['ID', '入る場所', '内容', 'Prompt（そのまま貼る）']]
    for fid, loc, ja, subj in RM.BOOK_FIGURES:
        rows.append([Paragraph(e(fid), sm), Paragraph(e(loc), sm), Paragraph(e(ja), sm), Paragraph(e(RM.image_prompt(subj)), mono)])
    t = Table(rows, colWidths=[12 * mm, 30 * mm, 42 * mm, 189 * mm], repeatRows=1)
    t.setStyle(TableStyle(GRID)); s += [t]
    doc.build(s)
    return OUT / PDF_NAME


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    p = main()
    print('OK', p)
