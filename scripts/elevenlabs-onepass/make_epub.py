#!/usr/bin/env python3
"""ElevenLabs Studio に1回アップロードするだけで全部読ませる EPUB を作る。
Studio の上限（公式FAQ）：1プロジェクト500章／1章400段落／1段落5000文字。
EPUB の Heading 1（h1）ごとに章が自動で分かれる（公式）。
・1文（1語）＝1段落。<break> タグは入れない（Studio では手入力タグが効くか公式に記載がないため）
・目次ページ・表紙・説明文は入れない（読まれてしまうため）。見出しは短い英語だけ。"""
import json, os, re, sys, uuid, zipfile, html
from make import grammar_batches
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vocab-audio'))
from spoken import line_for_prompt

MAXP = 400
def esc(s): return html.escape(s, quote=False)

def write_epub(path, title, chapters):
    """chapters: [(heading, [paragraph,...])]"""
    for h, ps in chapters:
        assert len(ps) + 1 <= MAXP, (h, len(ps))
        assert all(len(p) <= 5000 for p in ps)
    assert len(chapters) <= 500
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, title))
    z = zipfile.ZipFile(path, 'w')
    z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    D = zipfile.ZIP_DEFLATED
    z.writestr('META-INF/container.xml', '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', D)
    items, spine, nav = [], [], []
    for i, (h, ps) in enumerate(chapters, 1):
        fn = f'c{i:03d}.xhtml'
        body = f'<h1>{esc(h)}</h1>\n' + '\n'.join(f'<p>{esc(p)}</p>' for p in ps)
        z.writestr('OEBPS/' + fn, f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"><head><title>{esc(h)}</title></head><body>\n{body}\n</body></html>', D)
        items.append(f'<item id="c{i}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="c{i}"/>')
        nav.append(f'<li><a href="{fn}">{esc(h)}</a></li>')
    z.writestr('OEBPS/nav.xhtml', f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en"><head><title>Contents</title></head><body><nav epub:type="toc"><ol>{"".join(nav)}</ol></nav></body></html>', D)
    z.writestr('OEBPS/content.opf', f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">urn:uuid:{uid}</dc:identifier><dc:title>{esc(title)}</dc:title><dc:language>en</dc:language><dc:creator>Manatobi</dc:creator><meta property="dcterms:modified">2026-11-03T00:00:00Z</meta></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>{"".join(items)}</manifest>
<spine>{"".join(spine)}</spine></package>''', D)
    z.close()
    n = sum(len(p) for _, p in chapters); c = sum(len(x) for _, ps in chapters for x in ps)
    print(f'{path}: {len(chapters)}章 {n}段落 {c:,}文字 最大段落数/章={max(len(p) for _, p in chapters)}')

# ---- 英文法：アプリの章ごと（最大 175文＜400）----
g = grammar_batches()
gch, order = {}, []
for b in g:
    ch = int(b['ids'][0].split('_')[2])
    if ch not in gch: gch[ch] = []; order.append(ch)
    gch[ch] += b['texts']
assert sum(len(v) for v in gch.values()) == 1163
write_epub('Studio_英文法_全1163文.epub', 'Manatobi English Grammar 1163 Sentences',
           [(f'Chapter {ch}', gch[ch]) for ch in order])
json.dump({f'Chapter {ch}': [i for b in g if int(b['ids'][0].split('_')[2]) == ch for i in b['ids']] for ch in order},
          open('Studio_英文法_章とID.json', 'w'), indent=0)

# ---- 英単語：レベルの中を300語ずつ（＝400未満）に均等割り ----
words = json.load(open(os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'data', 'listeningVocabulary.json')))['words']
LV = ['lv1', 'lv2', 'lv3', 'lv4', 'ilv1', 'ilv2', 'ilv3']
vch, vmap, part = [], {}, 0
for lv in LV:
    ws = [w for w in words if w['level'] == lv]
    k = -(-len(ws) // 300); base, extra = divmod(len(ws), k); p = 0
    for j in range(k):
        n = base + (1 if j < extra else 0); chunk = ws[p:p + n]; p += n; part += 1
        vch.append((f'Part {part}', [line_for_prompt(w['word']) for w in chunk]))
        vmap[f'Part {part}'] = {'level': lv, 'from': p - n + 1, 'to': p, 'ids': [w['id'] for w in chunk]}
assert sum(len(p) for _, p in vch) == 5713
write_epub('Studio_英単語熟語_全5713語.epub', 'Manatobi Vocabulary 5713 Words', vch)
json.dump(vmap, open('Studio_英単語熟語_章とID.json', 'w'), indent=0)
