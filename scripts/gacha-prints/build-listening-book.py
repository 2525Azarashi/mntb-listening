#!/usr/bin/env python3
"""
UR（大当たり）「共通テスト 英語リスニング 大問別演習 完全版」を作る（2026-10-26）。

  アプリの英語リスニングの問題・音声をそのまま使う（問題・スクリプトはアプリと同じオリジナル）。
  各音声に QR コード（アプリの公開サイトの mp3）と「アプリのどこで聞けるか」を印刷する＝本とアプリの音声が連動。
  中身：表紙 → 使い方・全体像 → 大問ごとに「特徴と聞き方 → 問題（3回分）→ 解答・スクリプト・解説」→ 丸つけ表・得点記録表
  第k回 = 各単元から1セットずつ＝100点・本番と同じ形の1回分（易しめ → 標準 → やや難）

  使い方:
    npx tsx scripts/gacha-prints/dump-listening.ts /tmp/listening.json
    python3 scripts/gacha-prints/build-listening-book.py [/tmp/listening.json]
"""
import json, re, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, CondPageBreak, KeepTogether, Image as RLImage)
from reportlab.platypus.doctemplate import NextPageTemplate

sys.path.insert(0, str(Path(__file__).parent))
from book_common import (ROOT, F, FB, st, esc, on_page, bar, box, cover_stats, grid, make_thumb, page_count,
                         GOLD, GOLD_SOFT, LINE, GREEN, BLUE, PAPER, MINT, SKY, SUB)
from listening_guide import LGUIDE, GROUPS, APP_TAB

PID = 'print_book_listening_all'
TITLE = '共通テスト 英語リスニング\n大問別演習 完全版'
SITE = 'https://mntb-listening.vercel.app'  # アプリの公開サイト（public/ の音声をそのまま配信）
FOOTER = 'マナトビ ／ 問題・スクリプトはアプリと同じオリジナル。QR で音声が流れます'
ROUNDS = 3
IMG_CACHE = Path('/tmp/listening_book_img')
CH_ORDER = [c for _, cs, _, _ in GROUPS for c in cs]

def strip_html(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h or '')).strip()

def pick_sets(problems):
    """易しめ・標準・やや難が並ぶように、最初・真ん中・最後の3セット"""
    n = len(problems)
    return [problems[0], problems[n // 2], problems[n - 1]]

def app_round(p):
    m = re.match(r'(第\d+回)', p['category']); return m.group(1) if m else ''

def level(p):
    m = re.search(r'（([^（）]+)）$', p['category']); return m.group(1) if m else ''

# ── 画像（アプリの絵・図表を縮小して埋め込む）──────────────────
def img(src, width):
    from PIL import Image
    IMG_CACHE.mkdir(exist_ok=True)
    dst = IMG_CACHE / (src.strip('/').replace('/', '_').rsplit('.', 1)[0] + '.jpg')
    if not dst.exists():
        im = Image.open(ROOT / 'public' / src.lstrip('/'))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert('RGB'); im.thumbnail((640, 640), Image.LANCZOS); im.save(dst, "JPEG", quality=50, optimize=True, progressive=True)
    from PIL import Image as I2
    w, h = I2.open(dst).size
    return RLImage(str(dst), width=width, height=width * h / w)

# ── 音声：QR とアプリ内の場所 ─────────────────────────────
def qr(url, size=19 * mm):
    w = QrCodeWidget(url); w.barLevel = 'M'
    x1, y1, x2, y2 = w.getBounds(); d = Drawing(size, size, transform=[size / (x2 - x1), 0, 0, size / (y2 - y1), 0, 0]); d.add(w)
    return d

def audio_strip(ch, p, read):
    cells = []
    for t in p['audioTracks']:
        url = SITE + t['audioUrl']
        txt = [Paragraph(f'<b>{esc(t["label"])}</b>', st['cell']),
               Paragraph(f'<font size="7" color="#6b5d45">{esc(t["audioUrl"].rsplit("/", 1)[1])}</font>', st['cell'])]
        cells.append([qr(url), txt])
    per = 4 if len(cells) > 3 else len(cells)
    rows = []
    for i in range(0, len(cells), per):
        r = []
        for c in cells[i:i + per]: r += c
        r += [''] * (2 * per - len(r)); rows.append(r)
    t = Table(rows, colWidths=[21 * mm, 178 * mm / per - 21 * mm] * per)
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 1), ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]))
    head = Paragraph(f'<font color="#2458a6"><b>♪ 音声</b></font>　QR をスマホで読むと流れます（{read}）。'
                     f'アプリでは <b>英語リスニング ＞ {esc(APP_TAB[ch])} ＞ {esc(app_round(p))}</b> で同じ音声・解説', st['small'])
    return box([head, Spacer(1, 2), t], bg=SKY, border=BLUE, pad=5)

# ── 問題文（アプリの問題文から、画面操作の説明を除いて使う）──────
def problem_blocks(p):
    text = p['text']
    blocks = re.split(r'\n─{6,}\n', text)
    head = [ln for ln in blocks[0].split('\n')[1:] if ln.strip()]
    keep, skip = [], False
    for ln in head:
        if ln.startswith('【音源の聞き方】') or ln.startswith('【解き方のコツ】'): skip = True; continue
        if ln.startswith('【'): skip = False
        if skip: continue
        keep.append(ln)
    return keep, blocks[1:]

def block_qnums(block):
    first = block.strip().split('\n')[0]
    return [int(x) for x in re.findall(r'問(\d+)', first)]

def line_flow(ln):
    s = ln.strip()
    if not s: return None
    if s.startswith('| ---'): return None
    if s.startswith('|'):
        return Paragraph(esc('　'.join(c.strip() for c in s.strip('|').split('|'))), st['enc'])
    if re.match(r'^[①②③④⑤⑥]', s): return Paragraph(esc(s), st['enc'])
    if s.startswith('■') or re.match(r'^問\d+', s): return Paragraph(f'<font color="#b8860b"><b>{esc(s)}</b></font>', st['body'])
    ascii_ratio = sum(c.isascii() for c in s) / len(s)
    return Paragraph(esc(s), st['enq'] if ascii_ratio > 0.7 else st['body'])

def images_for(p, nums, used):
    out = []
    for sq in p['subQuestions']:
        m = re.match(r'問(\d+)', sq['label'])
        if not m or int(m.group(1)) not in nums: continue
        srcs = [sq['imageUrl']] if sq.get('imageUrl') else []
        srcs += sq.get('optionImages') or []
        for s in srcs:
            if s not in used: used.add(s); out.append(s)
    for t in p['audioTracks']:
        tn = [int(x) for x in re.findall(r'\d+', t['label'])]
        if tn and (set(range(tn[0], tn[-1] + 1)) & set(nums)):
            for im in (t.get('material') or {}).get('images') or []:
                if im['src'] not in used: used.add(im['src']); out.append(im['src'])
    return out

def image_flow(srcs):
    if not srcs: return []
    if len(srcs) >= 4 and all('q37' in s or 'opt' in s for s in srcs):
        cells = [img(s, 86 * mm) for s in srcs]
        t = Table([cells[i:i + 2] for i in range(0, len(cells), 2)], colWidths=[90 * mm] * 2)
        return [t, Spacer(1, 3)]
    return [x for s in srcs for x in (img(s, 120 * mm if 'q1b' in s or 'q2/' in s else 140 * mm), Spacer(1, 3))]

def problem_flow(ch, p, k):
    keep, blocks = problem_blocks(p)
    read = '2回読み：2回続けて再生' if p.get('readCount') == 2 else '1回読み：1回だけ再生'
    out = [Paragraph(f'<b>第{k}回</b>　{esc(re.sub(r"^第\d+回\s*", "", p["category"]))}', st['h3']), Spacer(1, 2), audio_strip(ch, p, read), Spacer(1, 3)]
    for ln in keep:
        f = line_flow(ln)
        if f and not ln.startswith(f'第'): out.append(f)
    used = set()
    for b in blocks:
        part = [f for f in (line_flow(ln) for ln in b.split('\n')) if f]
        part += image_flow(images_for(p, block_qnums(b), used))
        out += [Spacer(1, 3)] + ([KeepTogether(part)] if len(part) < 14 else part)
    rest = images_for(p, list(range(1, 60)), used)
    out += image_flow(rest)
    return out

# ── 解答・スクリプト・解説 ─────────────────────────────────
def explain_segments(p):
    t = strip_html(p.get('explanation', ''))
    seg = {}
    for m in re.finditer(r'問(\d+)\s*正解は\s*\S+(.*?)(?=問\d+\s*正解は|$)', t):
        body = m.group(2); i = body.find('解答の道すじ')
        seg[int(m.group(1))] = body[i + 6:].strip() if i >= 0 else ''
    return seg

def clip(s, n=520):
    if len(s) <= n: return s
    cut = s[:n]; j = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:j + 1] if j > n * 0.5 else cut + '…'

def points_of(ch, sq):
    if sq.get('examPoints') is not None: return int(sq['examPoints'])
    return LGUIDE[ch][2] or 0

def answer_flow(ch, p, k):
    seg = explain_segments(p)
    out = [Paragraph(f'<b>第{k}回</b>　{esc(re.sub(r"^第\d+回\s*", "", p["category"]))}', st['h3'])]
    for t in p['audioTracks']:
        lines = [Paragraph(f'<font color="#2458a6"><b>SCRIPT {esc(t["label"])}</b></font>', st['cell'])]
        for ln in (t.get('script') or '').split('\n'):
            if ln.strip(): lines.append(Paragraph(esc(ln.strip().strip('"')), st['enc']))
        if t.get('translation'): lines.append(Paragraph('訳：' + esc(t['translation']), st['small']))
        kp = [x['phrase'] + (f'＝{x["meaning"]}' if x.get('meaning') else '') for x in t.get('keyPhrases') or []][:4]
        if kp: lines.append(Paragraph('<b>聞き取りの決め手</b>　' + esc(' ／ '.join(kp)), st['small']))
        out += [box(lines, bg=PAPER, border=LINE, pad=5), Spacer(1, 2)]
    groups = {}
    for sq in p['subQuestions']:
        g = sq.get('allOrNothingGroup')
        if g: groups.setdefault(g, []).append(sq)
    shown = set()
    for sq in p['subQuestions']:
        m = re.match(r'問(\d+)', sq['label']); no = int(m.group(1)) if m else 0
        g = sq.get('allOrNothingGroup'); pts = points_of(ch, sq)
        if g and groups[g][0] is not sq: continue
        if g:
            ans = ' → '.join(x['correctAnswer'] for x in groups[g]) if 'step' in sq['label'] or ch == 'el4_A' else '・'.join(x['correctAnswer'] for x in groups[g])
            nos = [re.match(r'問(\d+)', x['label']).group(1) for x in groups[g]]
            head = f'問{nos[0]}〜{nos[-1]}　正解 {ans}　（完答 {sum(points_of(ch, x) for x in groups[g])}点）'
            body = sq.get('explainJa') or seg.get(no, '')
        else:
            head = f'{sq["label"][:48]}　正解 {sq["correctAnswer"]}　（{pts}点）'
            body = sq.get('explainJa') or seg.get(no, '')
        parts = [Paragraph(f'<b>{esc(head)}</b>', st['ans'])]
        if body and body in shown: parts.append(Paragraph('（解説は上の問と共通）', st['small']))
        elif body: parts.append(Paragraph(esc(clip(body)), st['ex'])); shown.add(body)
        for d in (sq.get('distractors') or [])[:3]:
            parts.append(Paragraph(f'<font color="#6b5d45">✕{"①②③④⑤⑥"[d["no"] - 1]}</font>　' + esc(clip(d['why'], 160)), st['ex']))
        t = Table([[parts]], colWidths=[182 * mm])
        t.setStyle(TableStyle([('LINEBEFORE', (0, 0), (0, -1), 2.2, GOLD), ('LEFTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
        out += [KeepTogether(t), Spacer(1, 1.5)]
    return out

def sheet_rows(ch, p):
    rows, seen = [], set()
    for sq in p['subQuestions']:
        g = sq.get('allOrNothingGroup')
        if g in seen: continue
        if g:
            seen.add(g); mem = [x for x in p['subQuestions'] if x.get('allOrNothingGroup') == g]
            lab = f'{mem[0]["label"].split()[0]}〜{mem[-1]["label"].split()[0][1:]}'
            rows.append((lab, ' '.join(x['correctAnswer'] for x in mem) + '（完答）', sum(points_of(ch, x) for x in mem)))
        else:
            rows.append((sq['label'].split()[0], sq['correctAnswer'], points_of(ch, sq)))
    return rows

# ── 本の組み立て ─────────────────────────────────────────
def build(data):
    rounds = {ch: pick_sets(data[ch]['problems']) for ch in CH_ORDER}
    totals = []
    for k in range(ROUNDS):
        tot = sum(pts for ch in CH_ORDER for _, _, pts in sheet_rows(ch, rounds[ch][k]))
        assert tot == 100, (k + 1, tot)
        totals.append(tot)
    n_tracks = sum(len(rounds[ch][k]['audioTracks']) for ch in CH_ORDER for k in range(ROUNDS))
    n_q = sum(len(rounds[ch][k]['subQuestions']) for ch in CH_ORDER for k in range(ROUNDS))
    flat = TITLE.replace('\n', ' ')
    story = [NextPageTemplate('body'), Spacer(1, 30 * mm), Paragraph('KYOTSU TEST ENGLISH LISTENING ／ COMPLETE EDITION', st['eyebrow']), Spacer(1, 4 * mm),
             Paragraph(esc(TITLE).replace('\n', '<br/>'), st['h1']), Spacer(1, 6 * mm),
             Paragraph('アプリの音声と連動。QR を読めばその場で本番と同じ音声が流れる。大問ごとの聞き方 → 3回分の演習 → スクリプトつき解説で、この1冊で仕上げる。', st['h1s']),
             Spacer(1, 20 * mm),
             cover_stats([('全6大問', '本番と同じ構成'), (f'{ROUNDS}回分', '各100点・易→難'), (f'{n_q}問', '全問スクリプトつき'),
                          (f'{n_tracks}音声', 'QR でアプリの音声'), ('約30分', '1回分の目安')]),
             Spacer(1, 12 * mm), Paragraph('第1問・第2問は2回読み、第3問から先は1回読み。音声の前に設問を読む「先読み」が勝負を決める。', st['h1s']), PageBreak()]

    story += [Paragraph('この本の使い方（アプリの音声と連動）', st['h2']),
              box([Paragraph('<b>① 音声の出し方</b>　各問題の上の <b>QR</b> をスマホのカメラで読むと、アプリと同じ音声が流れます。'
                             'アプリでは <b>英語リスニング ＞ 第○問 ＞ 第○回</b>（本の各問題に書いてある場所）で、同じ音声をスクリプト・和訳つきで聞き直せます。', st['body']),
                   Paragraph('<b>② 大問別に（1日1大問）</b>　「特徴と聞き方」を読む → 先読み → 音声（2回読み／1回読みを守る）→ 解答 → スクリプトで聞きのがした所に線。', st['body']),
                   Paragraph('<b>③ 1回分を通しで（約30分）</b>　第1問〜第6問の「第1回」を続けて解くと本番と同じ100点分になります（第2回・第3回も同じ）。', st['body']),
                   Paragraph('<b>④ 復習</b>　スクリプトを見ながらもう一度聞く → 見ないで聞く → 音声に重ねて声に出す（シャドーイング）。', st['body'])]),
              Spacer(1, 4 * mm), Paragraph('リスニングの全体像（2025・2026年度の本試験：100点・約30分・37マーク）', st['h2'])]
    rows = [['大問', '形式', '読み上げ', 'マーク', '配点', 'アプリの単元']]
    for g, cs, form, rd in GROUPS:
        rows.append([g, form, rd, str(sum(data[c]['marks'] for c in cs)), str(data[cs[0]]['points']), '・'.join(APP_TAB[c] for c in cs)])
    rows.append(['合計', '', '', '37', '100', ''])
    story += [grid(rows, [16 * mm, 70 * mm, 18 * mm, 15 * mm, 13 * mm, 50 * mm]), Spacer(1, 3 * mm),
              Paragraph('配点は大問ごと。第4問Aの並べ替え（問18〜21）、第5問の問28・29／問30・31は完答で得点。'
                        'QR の音声はアプリの公開サイト（' + esc(SITE) + '）にある mp3 で、アプリの中で流れるものと同じです。', st['small']), PageBreak()]

    sheet = []
    for g, cs, form, rd in GROUPS:
        for ch in cs:
            head, tips, _ = LGUIDE[ch]
            meta = data[ch]
            story += [bar(f'{APP_TAB[ch]}　{head}', f'{meta["marks"]}マーク／大問{meta["points"]}点・{rd}読み'), Spacer(1, 3 * mm),
                      box([Paragraph(f'<b>特徴と聞き方（{esc(meta["speakers"])}）</b>', st['h3'])] + [Paragraph('・' + esc(x), st['body']) for x in tips]), Spacer(1, 3 * mm)]
            for k in range(ROUNDS):
                p = rounds[ch][k]
                story += problem_flow(ch, p, k + 1) + [Spacer(1, 4 * mm)]
                if k < ROUNDS - 1: story.append(CondPageBreak(90 * mm))
            story += [PageBreak(), bar(f'{APP_TAB[ch]}　解答・スクリプト・解説', f'{ROUNDS}回分'), Spacer(1, 3 * mm)]
            for k in range(ROUNDS):
                p = rounds[ch][k]
                story += answer_flow(ch, p, k + 1) + [Spacer(1, 3 * mm)]
                for lab, ans, pts in sheet_rows(ch, p): sheet.append((k + 1, APP_TAB[ch], lab, ans, pts))
            story.append(PageBreak())

    story += [bar('丸つけ表（回ごと・本番と同じ100点）', '「正解」の列は解く前に紙で隠す'), Spacer(1, 3 * mm)]
    for k in range(1, ROUNDS + 1):
        rows = [['単元', '問', 'あなたの解答', '正解', '配点', '得点']]
        rows += [[c, lab, '', Paragraph(f'<font color="#2f7a52">{esc(a)}</font>', st['cell']), str(pts), ''] for kk, c, lab, a, pts in sheet if kk == k]
        story += [Paragraph(f'第{k}回（100点）', st['h2']), grid(rows, [24 * mm, 26 * mm, 40 * mm, 54 * mm, 16 * mm, 22 * mm], size=8, pad=1.6), Spacer(1, 3 * mm)]
    story += [CondPageBreak(60 * mm), Paragraph('得点記録表（大問別）', st['h2'])]
    rows = [['', *[g for g, *_ in GROUPS], '合計'], ['満点', *[str(data[cs[0]]['points']) for _, cs, _, _ in GROUPS], '100']]
    rows += [[f'第{k}回'] + [''] * 7 for k in range(1, ROUNDS + 1)]
    t = Table(rows, colWidths=[20 * mm] + [23 * mm] * 6 + [24 * mm])
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), F, 9), ('GRID', (0, 0), (-1, -1), 0.4, LINE), ('BACKGROUND', (0, 0), (-1, 0), GOLD_SOFT),
                           ('ALIGN', (1, 0), (-1, -1), 'CENTER'), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story += [t, Spacer(1, 3), Paragraph('7割未満の大問は、その大問の「特徴と聞き方」を読み直し、アプリで同じ単元の別の回を解く（アプリには各単元14〜16回分あります）。', st['small'])]

    out = ROOT / f'public/prints/{PID}.pdf'
    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=13 * mm,
                          title=f'{flat}（UR 完全版）', author='マナトビ')
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate(id='cover', frames=[fr], onPage=on_page(flat, FOOTER)), PageTemplate(id='body', frames=[fr], onPage=on_page(flat, FOOTER))])
    doc.build(story)
    make_thumb(out, PID)
    return out


if __name__ == '__main__':
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/listening.json')
    out = build(json.loads(src.read_text(encoding='utf-8')))
    print(out.name, page_count(out), 'pages', out.stat().st_size // 1024, 'KB')
