#!/usr/bin/env python3
"""
F4（2026-11-04）作り直すリスニングのイラスト一覧 PDF。
  きっかけ：ストアのレビュー「白黒のイラストなのに赤色のバッグはどれか」。
  選び方：スクリプトに色の語がある問を機械で拾い（.tmpwork/listening_dump.json）、
          絵が白黒（彩度ほぼ0）で、しかも「色でしか選択肢を区別できない」ものを目で確認して選んだ。
  使い方：python3 scripts/listening-data/build_redo_illustrations_pdf.py [出力先.pdf]
  PDF の文字はコピーできる（スクリプト・作り直し用プロンプトをそのまま貼れる）。
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

pdfmetrics.registerFont(TTFont('G', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'))
OUT = sys.argv[1] if len(sys.argv) > 1 else '.tmpwork/listening_redo_illustrations.pdf'

STYLE = ('Flat, clean children\'s-textbook illustration with thin black outlines and FLAT FULL-COLOR fills '
         '(colors must be clearly different and easy to name). White background. 2x2 grid of four equal square panels '
         'separated by thin gray borders. Put a bold circled number ①, ②, ③, ④ in the top-left corner of each panel '
         '(left-to-right, top-to-bottom). No other text unless stated.')

ITEMS = [
    dict(id='q_el1_B_set1_2', where='第1問B 第1回 問2', file='public/listening_q1b/el1B_set1_q2.jpg', ans='③',
         script='"I\'ll take this red shoulder bag with the long strap, please."',
         opts=['① 長いストラップの青いショルダーバッグ', '② 短い持ち手の赤いハンドバッグ', '③ 長いストラップの赤いショルダーバッグ（正解）', '④ 赤いリュックサック'],
         issue='①と③は色（青／赤）だけの違い。白黒では「しま模様のストラップ」「黒いストラップ」にしか見えず、どちらが赤か分からない（レビューで指摘された問題）。',
         prompt='① a BLUE shoulder bag with a long strap, ② a RED handbag with short handles, ③ a RED shoulder bag with a long strap, ④ a RED backpack. Bags ① and ③ have exactly the same shape; only the color differs.'),
    dict(id='q_el1_B_set9_3', where='第1問B 第9回 問3', file='public/listening_q1b/el1B_set9_q3.jpg', ans='④',
         script='"I\'m wearing my new blue hat today, not the yellow one."',
         opts=['① 青い帽子を手に持つ女の子', '② 帽子をかぶっていない女の子', '③ 黄色い帽子をかぶる女の子', '④ 青い帽子をかぶる女の子（正解）'],
         issue='③と④は帽子の色（黄／青）だけの違い。白黒では「星の柄」「水玉の柄」になっていて、どちらが青か分からない。',
         prompt='The same smiling girl (shoulder-length hair) in each panel. ① holding a BLUE bucket hat in her hands (not wearing it), ② wearing no hat, ③ wearing a YELLOW bucket hat, ④ wearing a BLUE bucket hat. The hats in ①, ③, ④ have the same plain design; only the color differs.'),
    dict(id='q_el1_B_set12_3', where='第1問B 第12回 問3', file='public/listening_q1b/el1B_set12_q3.jpg', ans='②',
         script='"Put the apples in the green bowl and the oranges in the white one, please."',
         opts=['① 白いボウルにりんご、緑のボウルにみかん', '② 緑のボウルにりんご、白いボウルにみかん（正解）', '③ りんごはかご、みかんは白いボウル', '④ 全部が緑のボウル'],
         issue='①と②はボウルの色（緑／白）の入れ替えだけ。白黒では「網目のボウル」「無地のボウル」で、どちらが緑か分からない。りんごとみかんも白黒では見分けにくい。',
         prompt='Two bowls side by side in panels ①-③. ① RED apples in a WHITE bowl and ORANGE oranges in a GREEN bowl, ② RED apples in a GREEN bowl and ORANGE oranges in a WHITE bowl, ③ RED apples in a brown wicker basket and ORANGE oranges in a WHITE bowl, ④ apples and oranges all together in one GREEN bowl. Apples and oranges must look clearly different.'),
    dict(id='q_el1_B_set14_2', where='第1問B 第14回 問2', file='public/listening_q1b/el1B_set14_q2.jpg', ans='②',
         script='"There are two balls under the chair. The red one is bigger than the blue one."',
         opts=['① 椅子の下に小さい赤いボールと大きい青いボール', '② 椅子の下に大きい赤いボールと小さい青いボール（正解）', '③ 椅子の上にボール2つ', '④ 椅子の下にボール1つ'],
         issue='①と②は「どちらの色が大きいか」だけの違い。白黒では斜線のボールと無地のボールになっていて、赤・青が分からない。',
         prompt='The same simple wooden chair in each panel. ① under the chair: a SMALL RED ball and a LARGE BLUE ball, ② under the chair: a LARGE RED ball and a SMALL BLUE ball, ③ a red ball and a blue ball ON the chair seat, ④ only one ball under the chair.'),
    dict(id='q_el1_B_set15_4', where='第1問B 第15回 問4', file='public/listening_q1b/el1B_set15_q4.jpg', ans='④',
         script='"I bought the pencil case with the blue stars, not the one with the red hearts."',
         opts=['① 赤いハート柄の筆箱', '② 赤い星柄の筆箱', '③ 青いハート柄の筆箱', '④ 青い星柄の筆箱（正解）'],
         issue='柄（星／ハート）は見えるが、色（赤／青）が白黒では分からず、①と③、②と④が区別できない。',
         prompt='The same white zip pencil case in each panel. ① covered with RED hearts, ② covered with RED stars, ③ covered with BLUE hearts, ④ covered with BLUE stars.'),
    dict(id='q_el2_set1_3', where='第2問 第1回 問3', file='public/listening_q2/el2_set1_q3.jpg', ans='①',
         script="W: Do you have this shirt in a smaller size?\nM: We have small and extra-small. Which would you like?\nW: Small, please. And in blue if possible.\nM: Sure, here's a small blue one.\nQuestion: Which shirt did the woman get?",
         opts=['① 青のSサイズのシャツ（正解）', '② 青のXSサイズのシャツ', '③ 白のSサイズのシャツ', '④ 青のMサイズのシャツ'],
         issue='①と③は色（青／白）だけの違い。白黒では「斜線のシャツ」「無地のシャツ」になっていて、どちらが青か分からない。',
         prompt='A neatly folded button-up shirt with a hanging size tag in each panel. Tag text: ① "S", ② "XS", ③ "S", ④ "M". Shirt colors: ① BLUE, ② BLUE, ③ WHITE, ④ BLUE.'),
    dict(id='q_el2_set12_3', where='第2問 第12回 問3', file='public/listening_q2/el2_set12_q3.jpg', ans='②',
         script="W: I'd like a doll with long hair and a red dress.\nM: We have long hair with pink dress or short hair with red dress.\nW: Any long hair with red dress?\nM: Not now. How about long hair, pink dress? It's the closest.\nQuestion: Which doll will the woman likely take?",
         opts=['① 長い髪・赤いドレス', '② 長い髪・ピンクのドレス（正解）', '③ 短い髪・赤いドレス', '④ 短い髪・ピンクのドレス'],
         issue='髪の長さは見えるが、ドレスの色（赤／ピンク）が白黒では「濃い点々」「うすい点々」でしか表せず、どちらが赤か分からない。',
         prompt='The same toy doll standing in each panel. ① LONG hair, RED dress, ② LONG hair, light PINK dress, ③ SHORT bob hair, RED dress, ④ SHORT bob hair, light PINK dress. Red and pink must be clearly different.'),
]

REF = [
    ('第1問B 第5回 問4（白い車・黒い車）', '黒はベタ塗りで見分けられる。作り直さなくてよい。'),
    ('第1問B 第7回 問2（白い犬・黒い犬）', '同上。'),
    ('第1問B 第3回 問3（白いシャツの女の子）', '答えは左右の位置で決まる。色は不要。'),
    ('第1問B 第2回 問4（茶色の犬）', '答えは「しっぽを追いかける」動作で決まる。'),
    ('第1問B 第11回 問1・問2（赤いバラ・青い自転車）', '答えは本数・台数で決まる（解説にも「色は不要」とある）。'),
    ('第2問 第2回 問3（しまのシャツ）', 'しま模様は白黒でも見える。'),
    ('第2問 第16回 問3（ラケットの色）', '絵は水色のカラー。答えは軽さとヘッドの大きさで決まる。'),
    ('第4問・第5問の色の語（Green Wheels・white bicycles など）', '店名・話の中身で、図の読み取りには関係しない。'),
]

def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=12*mm, bottomMargin=12*mm,
                            title='作り直すリスニングのイラスト（白黒なのに色で答える問）', author='マナトビ')
    H1 = ParagraphStyle('h1', fontName='G', fontSize=16, leading=22, spaceAfter=4)
    H2 = ParagraphStyle('h2', fontName='G', fontSize=13, leading=18, spaceBefore=2, spaceAfter=3, textColor=colors.HexColor('#7a4b12'))
    B = ParagraphStyle('b', fontName='G', fontSize=9.5, leading=14)
    S = ParagraphStyle('s', fontName='G', fontSize=8.5, leading=12, textColor=colors.HexColor('#555555'))
    MONO = ParagraphStyle('m', fontName='G', fontSize=9.5, leading=14, backColor=colors.HexColor('#f4f6f8'),
                          borderColor=colors.HexColor('#c9d2da'), borderWidth=0.6, borderPadding=5, spaceBefore=2, spaceAfter=6)
    esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')
    st = [Paragraph('作り直すリスニングのイラスト（白黒なのに色で答える問）', H1),
          Paragraph('2026-11-04 ／ ストアのレビュー「白黒のイラストなのに赤色のバッグはどれか」を受けて、全リスニング問題（絵つき 333問）を調べました。'
                    'スクリプトに色の語がある問を機械で拾い、絵が白黒で、しかも<b>色でしか選択肢を区別できない</b>ものを目で確認して <b>7問</b> を選びました。', B),
          Spacer(1, 4),
          Paragraph('各ページの「スクリプト」「作り直し用プロンプト（英語）」はそのままコピーして貼れます。'
                    '正解の位置（①〜④）は今のデータと同じにしてください（番号が絵に焼き込まれているため、並びを変えると正解がずれます）。'
                    '差し替えるときは、同じファイル名・900×900px の JPG で上書きすれば、アプリのデータは変えずに済みます。', B),
          Spacer(1, 6)]
    rows = [['#', '問題', 'ファイル', '正解']] + [[str(k + 1), it['where'], it['file'].replace('public', ''), it['ans']] for k, it in enumerate(ITEMS)]
    t = Table(rows, colWidths=[8*mm, 48*mm, 100*mm, 14*mm])
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'G', 9), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fff3d6')),
                           ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    st += [t, Spacer(1, 8), Paragraph('作り直さなくてよいもの（色の語はあるが、答えは色以外で決まる）', H2)]
    for a, b in REF: st.append(Paragraph(f'・{esc(a)}：{esc(b)}', S))
    st += [Spacer(1, 6), Paragraph('共通の画風（各プロンプトの前に付ける）', H2), Paragraph(esc(STYLE), MONO)]
    for k, it in enumerate(ITEMS):
        st.append(PageBreak())
        img = Image(it['file'], width=72*mm, height=72*mm)
        left = [Paragraph(f'{k + 1}. {esc(it["where"])}　<font size="9">正解 {it["ans"]}</font>', H2),
                Paragraph(f'問題ID：{it["id"]}', S), Paragraph(f'ファイル：{it["file"]}', S), Spacer(1, 4),
                Paragraph('<b>何がおかしいか</b>', B), Paragraph(esc(it['issue']), B), Spacer(1, 4),
                Paragraph('<b>選択肢の絵（あるべき内容）</b>', B)] + [Paragraph(esc(o), B) for o in it['opts']]
        top = Table([[left, img]], colWidths=[108*mm, 74*mm])
        top.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0)]))
        st += [top, Spacer(1, 6), Paragraph('<b>スクリプト（読み上げる英文）</b>', B), Paragraph(esc(it['script']), MONO),
               KeepTogether([Paragraph('<b>作り直し用プロンプト（英語・共通の画風＋この中身）</b>', B),
                             Paragraph(esc(STYLE + ' ' + it['prompt']), MONO)])]
    doc.build(st)
    print(OUT)

if __name__ == '__main__':
    build()
