#!/usr/bin/env python3
"""ElevenLabs にそのまま貼れる原稿PDF（英文法 1163文／英単語帳 5713語）を作る。
枠の中＝英語と間の指定だけ。和訳・問題番号・IDは入れない。1回分＝1ページ、行の途中で折り返さない。"""
import json, re, subprocess, os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('JA', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
pdfmetrics.registerFont(TTFont('EN', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
W, H = A4; ML = 14*mm; BOXW = W - 2*ML
GBREAK = '<break time="1.5s" />'
TEAL = colors.HexColor('#0f5c63'); GREY = colors.HexColor('#5d6d7e')

# ---------- 英文法：元PDFのテキストから英文とIDを取り出す ----------
def grammar_batches():
    L = open(os.path.join(os.path.dirname(__file__), 'grammar_readaloud_source.txt')).read().split('\n')
    cjk = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
    items, cur, state, chap = [], None, None, None
    for l in L:
        s = l.strip()
        m = re.match(r'^第(\d+)章 (\S+)$', s)
        if m: chap = (int(m.group(1)), m.group(2)); continue
        m = re.match(r'^問\d+ (.*)$', s)
        if m: cur = {'ch': chap, 'en': m.group(1)}; items.append(cur); state = 'en'; continue
        if state == 'en':
            if not s or cjk.search(s): state = 'id' if s else 'en2'
            else: cur['en'] += ' ' + s; continue
        m = re.match(r'^(q_eg6_\d+_set(\d+)_\d+)\s', s)
        if m and cur and 'id' not in cur: cur['id'] = m.group(1); cur['set'] = int(m.group(2))
    assert len(items) == 1163 and all('id' in i for i in items)
    for i in items:
        i['en'] = re.sub(r'\s*※.*$', '', i['en']).strip()
        i['en'] = re.sub(r'\s+', ' ', i['en'])
        assert not cjk.search(i['en']), i
    out = []
    chs = sorted({i['ch'] for i in items})
    for ch in chs:
        its = [i for i in items if i['ch'] == ch]
        sets = sorted({i['set'] for i in its})
        k = -(-len(sets) // 4); base, extra = divmod(len(sets), k)
        p = 0
        for j in range(k):
            g = sets[p:p + base + (1 if j < extra else 0)]; p += len(g)
            chunk = [i for i in its if i['set'] in g]
            cid = chunk[0]['id'].split('_set')[0][2:]
            name = f'{cid}_set{g[0]}-{g[-1]}' if len(g) > 1 else f'{cid}_set{g[0]}'
            lines = []
            for n, i in enumerate(chunk):
                lines.append(i['en'])
                if n < len(chunk) - 1: lines.append(GBREAK)
            out.append({'name': name, 'meta': f'第{ch[0]}章 {ch[1]}　第{g[0]}〜{g[-1]}回（{len(chunk)}文）',
                        'lines': lines, 'ids': [i['id'] for i in chunk], 'texts': [i['en'] for i in chunk]})
    return out

def vocab_batches():
    man = json.load(open('vocab_manifest.json'))
    lab = {'lv1': '単語 Lv1', 'lv2': '単語 Lv2', 'lv3': '単語 Lv3', 'lv4': '単語 Lv4', 'ilv1': '熟語 Lv1', 'ilv2': '熟語 Lv2', 'ilv3': '熟語 Lv3'}
    out = []
    for name, m in man.items():
        lines = open(f'vocab_batches/{name}.txt').read().rstrip('\n').split('\n')
        out.append({'name': name, 'meta': f'{lab[m["level"]]}　No.{m["from"]}〜{m["to"]}（{len(m["ids"])}語）', 'lines': lines})
    return out

def _font_for(ch):
    return 'EN' if ord(ch) < 0x2000 or ch in '—“”’‘…' else 'JA'

def runs(text):
    out = []
    for ch in text:
        f = _font_for(ch)
        if out and out[-1][0] == f: out[-1][1] += ch
        else: out.append([f, ch])
    return out

def mwidth(text, size):
    return sum(pdfmetrics.stringWidth(t, f, size) for f, t in runs(text))

def mdraw(c, x, y, text, size, right=False):
    if right: x -= mwidth(text, size)
    for f, t in runs(text):
        c.setFont(f, size); c.drawString(x, y, t); x += pdfmetrics.stringWidth(t, f, size)

def fit_size(lines, maxsize, minsize=6.5):
    s = maxsize
    while s > minsize and max(pdfmetrics.stringWidth(l, 'EN', s) for l in lines) > BOXW - 8*mm: s -= 0.25
    assert max(pdfmetrics.stringWidth(l, 'EN', s) for l in lines) <= BOXW - 8*mm, lines
    return s

def intro(c, title, paras):
    c.setFillColor(TEAL); mdraw(c, ML, H - 22*mm, title, 17)
    y = H - 34*mm; c.setFillColor(colors.black)
    for p in paras:
        size = 10.5 if not p.startswith('■') else 11.5
        c.setFillColor(TEAL if p.startswith('■') else colors.black)
        if p.startswith('■'): y -= 3*mm
        # 日本語は文字幅で折り返す
        line = ''
        for ch in p:
            if mwidth(line + ch, size) > BOXW: mdraw(c, ML, y, line, size); y -= size*1.6; line = '　' + ch if p.startswith('・') else ch
            else: line += ch
        mdraw(c, ML, y, line, size); y -= size*1.7
    c.showPage()

def build(path, title, paras, batches, maxsize, footer):
    c = canvas.Canvas(path, pagesize=A4); c.setTitle(title); c.setAuthor('まなとび')
    intro(c, title, paras)
    n = len(batches)
    for k, b in enumerate(batches, 1):
        c.setFillColor(TEAL); c.setFont('EN', 14); c.drawString(ML, H - 18*mm, b['name'] + '.mp3')
        c.setFillColor(GREY); mdraw(c, W - ML, H - 18*mm, f'{k} / {n} 回目', 9, right=True)
        mdraw(c, ML, H - 24*mm, b['meta'] + '　↓ 点線の枠の中だけを全部コピーして貼る', 9)
        size = fit_size(b['lines'], maxsize); lead = size * 1.55
        top = H - 29*mm; hgt = lead * len(b['lines']) + 7*mm
        assert top - hgt > 14*mm, (b['name'], hgt)
        c.setStrokeColor(TEAL); c.setDash(4, 3); c.setLineWidth(1.3)
        c.roundRect(ML, top - hgt, BOXW, hgt, 3*mm); c.setDash()
        c.setFillColor(colors.black); c.setFont('EN', size); y = top - 4*mm - size
        for l in b['lines']:
            c.setFillColor(GREY if l.startswith('<break') else colors.black)
            c.drawString(ML + 4*mm, y, l); y -= lead
        c.setFillColor(GREY); mdraw(c, ML, 9*mm, footer, 8)
        c.showPage()
    c.save()

def verify(path, batches):
    t = subprocess.run(['pdftotext', '-raw', path, '-'], capture_output=True, text=True).stdout
    flat = re.sub(r'\s+', ' ', t)
    bad = [b['name'] for b in batches if re.sub(r'\s+', ' ', '\n'.join(b['lines'])) not in flat]
    lig = [ch for ch in ('ﬁ', 'ﬂ', 'ﬀ') if ch in t]
    pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout).group(1)
    print(path, pages, 'pages', len(batches), 'batches', 'NG:', bad[:5], lig)
    assert not bad and not lig

COMMON = [
 '■ ElevenLabs の設定（全回で同じにする）',
 '・Text to Speech ／ モデル：Eleven Multilingual v2（v3 は <break> が使えないので不可）',
 '・声：アメリカ英語のはっきりした声を1つ決めて最後まで変えない',
 '・Stability 60〜70% ／ Similarity 75% ／ Style 0% ／ Speaker boost オン',
 '■ 1回ごとの手順',
 '・次のページの点線の枠の中を全部コピー → 入力欄を空にしてから貼る → 生成',
 '・ページ上の「ファイル名.mp3」の名前で保存（後で1つずつに切るときの目印）',
 '・<break … /> は「間」の指定です。消さずにそのまま貼ってください（この無音で1つずつに切ります）',
]

if __name__ == '__main__':
    g = grammar_batches(); v = vocab_batches()
    json.dump({b['name']: {'ids': b['ids'], 'texts': b['texts']} for b in g}, open('grammar_manifest.json', 'w'), ensure_ascii=False, indent=1)
    os.makedirs('grammar_batches', exist_ok=True)
    for b in g: open(f'grammar_batches/{b["name"]}.txt', 'w').write('\n'.join(b['lines']) + '\n')
    gp = [f'英文法 第1〜20章の完成文 全1163文・全{len(g)}回。1回＝4回分（約20文）、文と文の間に1.5秒の間。',
          '枠の中は英文と間の指定だけです（和訳・問題番号・IDは入れていません）。'] + COMMON + [
          '・Speed 0.95〜1.0（文なので普通の速さ）',
          '■ 注意',
          '・第10章 第3回 問2（This is the friend with that I often talk.）は「最も不適切なもの」を選ぶ問題の誤文です。',
          '　アプリの読み上げ文と同じにしてありますが、音読用には with whom に直すのがおすすめです。']
    build('ElevenLabs_英文法_原稿.pdf', 'ElevenLabs 読み上げ原稿　英文法 音読文 全1163文', gp, g, 10.5, 'まなとび 英文法 ElevenLabs原稿')
    verify('ElevenLabs_英文法_原稿.pdf', g)
    vp = [f'英単語・英熟語の単語帳 全5713語・全{len(v)}回。1回＝約30語、語と語の間に1.2秒の間。',
          '枠の中は英語と間の指定だけです（意味・番号は入れていません）。'] + COMMON + [
          '・Speed 0.9（単語帳なので少しゆっくり）',
          '■ 読み方の決まり',
          '・— は「ここに語句が入る」場所（例 so — that.）。someone / something / doing は単語帳の「人」「物」「～ing」']
    build('ElevenLabs_英単語熟語_原稿.pdf', 'ElevenLabs 読み上げ原稿　英単語・英熟語 全5713語', vp, v, 10.5, 'まなとび 英単語・英熟語 ElevenLabs原稿')
    verify('ElevenLabs_英単語熟語_原稿.pdf', v)
