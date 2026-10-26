# 宣伝動画の共通部品（テーマに依存しない）2026-10-26
#   英単語版（promo_vocab.py）で作った「上に道のり＋見出し、下にアプリ画面のカード」の形を、どのテーマでも使えるようにしたもの。
#   新しい台本は `from promo_parts import *` して、ROAD（道のりの4語）と場面を書くだけでよい。
#   使い方は store-assets/VIDEO_PLAYBOOK.md の「4. 編集エンジンの使い方」。
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from promo_engine import *  # noqa: F401,F403

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
REC = os.environ.get('PROMO_REC') or os.path.join(ROOT, 'store-assets', '_footage')
A = lambda *p: os.path.join(ROOT, *p)
SFX = lambda n: A('public/sfx/battle', n + '.mp3')
TANJOU, WAITING, TRAIN, CANARY = A('public/tanjou.mp3'), A('public/bgm/battle/waiting.mp3'), A('public/bgm/battle/battle.mp3'), A('public/bgm/battle/battle2.mp3')
PHONE_SRC, PC_SRC = (860, 1864), (1920, 1080)
GREEN = (46, 160, 96)
def mp4(d, n): return os.path.join(d, n + '.mp4')
def meta(d, n): return json.load(open(os.path.join(d, n + '.json')))

LAYOUTS = {
  # 縦は「上に道のり＋見出しの帯、その下にアプリの画面（角丸のカード）」。見出しが画面の文字にかぶらない
  'reel': dict(W=1080, H=1920, road_y=56, cap_y=196, cap=52, card=92, screen=(40, 400, 1000, 1480)),
  'story': dict(W=1080, H=1920, road_y=250, cap_y=384, cap=50, card=92, screen=(70, 560, 940, 1130)),
  'youtube': dict(W=1920, H=1080, road_y=20, cap_y=118, cap=46, card=86, screen=(249, 140, 1422, 800)),
}

def fit(roi, dw, dh, sw, sh):
  x0, y0, x1, y1 = roi; a = dw / dh
  cw = min(max(x1 - x0, (y1 - y0) * a), sw, sh * a); ch = cw / a
  cx = min(max((x0 + x1) / 2, cw / 2), sw - cw / 2); cy = min(max((y0 + y1) / 2, ch / 2), sh - ch / 2)
  return (cx, cy, cw)
def cams(keys, dest, src): return [(t, fit(r, dest[2], dest[3], *src)) for t, r in keys]
def to_out(t, t0, speed=1.0): return (t - t0) / speed

_BG = {}
def _bg(L, key, top, bottom, glow):
  k = (key, L['W'], L['H'])
  if k not in _BG: _BG[k] = gradient(L['W'], L['H'], top, bottom, glow=(L['W'] * 0.5, L['H'] * glow[0], max(L['W'], L['H']) * glow[1], glow[2], glow[3]))
  return _BG[k]
def bg_navy(L): return _bg(L, 'navy', (20, 34, 58), (12, 20, 36), (0.42, 0.45, BLUE, 0.55))
def bg_blue(L): return _bg(L, 'blue', BLUE, BLUE_D, (0.40, 0.50, (80, 140, 225), 0.55))
def bg_dusk(L): return _bg(L, 'dusk', (38, 42, 56), (16, 18, 26), (0.62, 0.38, (70, 76, 100), 0.5))
def bg_teal(L): return _bg(L, 'teal', (28, 110, 104), (14, 58, 62), (0.40, 0.50, (70, 170, 160), 0.5))
def bg_cream(L): return _bg(L, 'cream', CREAM, CREAM_D, (0.5, 0.5, CREAM, 0.0))

def cap_img(text, size, hl=None, step=None):
  t = Image.fromarray(cv2.cvtColor(text_img(text, size, WHITE, hl=hl, hl_mode='color', pad=round(size * 0.42)), cv2.COLOR_BGRA2RGBA))
  sp = Image.fromarray(cv2.cvtColor(pill_img(step, round(size * 0.5), fg=NAVY, bg=ORANGE), cv2.COLOR_BGRA2RGBA)) if step else None
  top = sp.height // 2 + 4 if sp else 0
  W = max(t.width, sp.width if sp else 0) + 8; H = t.height + top + 4
  im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x = (W - t.width) // 2
  ImageDraw.Draw(im).rounded_rectangle([x, top, x + t.width - 1, top + t.height - 1], round(size * 0.45), fill=(16, 28, 46, 226))
  im.alpha_composite(t, (x, top))
  if sp: im.alpha_composite(sp, ((W - sp.width) // 2, 0))
  return pil_to_bgra(im)

def caption(L, text, at=0.15, until=None, hl=None, step=None, y=None, size=None, x=None):
  return Sprite(cap_img(text, size or L['cap'], hl, step), x or L['W'] / 2, y if y is not None else L['cap_y'], at=at, until=until, anim='up', dur=0.4, anchor='top')

_ROAD = {}
def road_img(L, road_words, k):
  """1本の道（4つ）。k 番目がいま（オレンジ）、それより前は済み（✓）"""
  key = (L['W'], tuple(road_words), k)
  if key in _ROAD: return _ROAD[key]
  wide = L['W'] > L['H']; w = 760 if wide else 900; h = 104 if wide else 118; r = 22 if wide else 26
  im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
  d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=(14, 24, 40, 215))
  xs = [w * (0.14 + 0.24 * i) for i in range(4)]; cy = h * 0.38
  d.line([xs[0], cy, xs[-1], cy], fill=(90, 104, 130, 255), width=6)
  if k > 0: d.line([xs[0], cy, xs[min(k, 3)], cy], fill=ORANGE + (255,), width=6)
  f = font(FONT_BLACK, 22 if wide else 25)
  for i, x in enumerate(xs):
    col = ORANGE if i == k else (GREEN if i < k else (90, 104, 130))
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=col + (255,), outline=(255, 255, 255, 255) if i == k else None, width=4)
    t = '✓' if i < k else str(i + 1)
    ff = font(FONT_BLACK, 22 if wide else 26); tw = d.textlength(t, font=ff); d.text((x - tw / 2, cy - r * 0.66), t, font=ff, fill=WHITE if i != k else NAVY)
    tw = d.textlength(road_words[i], font=f); d.text((x - tw / 2, h - (34 if wide else 38)), road_words[i], font=f, fill=WHITE if i <= k else (150, 160, 180))
  _ROAD[key] = pil_to_bgra(im); return _ROAD[key]

def road(L, road_words, k, at=0.0, anim='fade', x=None):
  return Sprite(road_img(L, road_words, k), x or L['W'] / 2, L['road_y'], at=at, anim=anim, dur=0.35, anchor='top')

def label(text, x, y, orange=False, at=0.1, size=30):
  return Sprite(pill_img(text, size, fg=NAVY if orange else WHITE, bg=ORANGE if orange else (16, 28, 46)), x, y, at=at, anim='fade', dur=0.3, anchor='tl')

def V(path, t0, dest, src, roi=None, speed=1.0, at=0.0, until=None, device=None, ev=(), voice=None, **kw):
  """録画の層。ev=[(元の時刻, 効果音名, 音量)]、voice=[(元の時刻, 音源ファイル, 音源の何秒から, 長さ)]（その時刻にアプリで鳴っていた音）"""
  v = Video(path, t0, dest, cam=cams(roi, dest, src) if roi else None, speed=speed, at=at, until=until, device=device, **kw)
  v.ev = list(ev); v.voice = list(voice or []); return v

_SHADOW = {}
def screen_shadow(w, h, r):
  k = (w, h, r)
  if k not in _SHADOW:
    pad = 40; im = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0)); m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([pad, pad + 14, pad + w, pad + h + 14], r, fill=170)
    im.paste((4, 8, 18, 255), (0, 0), m.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(im).rounded_rectangle([pad - 3, pad - 3, pad + w + 3, pad + h + 3], r + 3, outline=(255, 255, 255, 60), width=3)
    _SHADOW[k] = (pil_to_bgra(im), pad)
  return _SHADOW[k]

def full(L, path, t0, t1, src, roi=None, speed=1.0, ev=(), voice=None, layers=(), under=(), xin=0.25, kind='fade', punch=(), flash=(), shake=(), zoom=None, name='', freeze=None):
  """1ショット＝録画1本。縦はカードに入れ（上に道のりと見出し）、横は画面いっぱい。under はカードより下に敷く層"""
  rk = [(0, roi)] if roi and not isinstance(roi, list) else roi
  rk = rk or [(0, (0, 0, src[0], src[1]))]
  if 'screen' in L:
    x, y, w, h = L['screen']; r = 40; sh, pad = screen_shadow(w, h, r)
    v = V(path, t0, (x, y, w, h), src, roi=rk, speed=speed, ev=ev, voice=voice, freeze=freeze, radius=r)
    return Shot((t1 - t0) / speed, [*under, Sprite(sh, x - pad, y - pad, anim=None, anchor='tl'), v, *layers], bg_navy(L), xin=xin, kind=kind,
                punch=punch, flash=flash, shake=shake, zoom=zoom, name=name)
  v = V(path, t0, (0, 0, L['W'], L['H']), src, roi=rk, speed=speed, ev=ev, voice=voice, freeze=freeze)
  return Shot((t1 - t0) / speed, [*under, v, *layers], bg_cream(L), xin=xin, kind=kind, punch=punch, flash=flash, shake=shake, zoom=zoom, name=name)

def mascot(path, h, x, y, at=0.1, anim='pop', bob=(9, 2.6), alpha=1.0):
  return Sprite(load_sprite(path, h=h), x, y, at=at, anim=anim, dur=0.7, bob=bob, alpha=alpha)

def lines_up(L, lines, y, size, hl=None, at=0.25, step=0.55, cx=None, color=WHITE, fnt=FONT_BLACK):
  out = []; cx = cx or L['W'] / 2
  for i, ln in enumerate(lines):
    img = text_img(ln, size, color, fnt=fnt, hl=hl, hl_mode='color', shadow=(0, 5, (8, 14, 30, 130)))
    out.append(Sprite(img, cx, y, at=at + i * step, anim='up', dur=0.55, anchor='top', drift=(0, -4, 0))); y += img.shape[0] * 0.9
  return out, y

def logo_pill(width):
  lg = Image.open(A('public/brand/manatobi-logo.png')).convert('RGBA'); s = width / lg.width
  lg = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS); pad = round(width * 0.09)
  pill = Image.new('RGBA', (lg.width + pad * 2, lg.height + pad * 2), (0, 0, 0, 0))
  ImageDraw.Draw(pill).rounded_rectangle([0, 0, pill.width - 1, pill.height - 1], pill.height // 2, fill=WHITE)
  pill.alpha_composite(lg, (pad, pad)); return pil_to_bgra(pill)

def sc_steps(L, dur, title, hl, steps, bottom, bottom_hl, name='roadmap', xin=0.3):
  """1本の道：steps=[(大きい語, 小さい語), ×4]"""
  W, H = L['W'], L['H']; wide = W > H; S = L['card']
  lay, y = lines_up(L, title, H * (0.13 if not wide else 0.10), round(S * 0.86), hl=hl, at=0.1, step=0.4)
  for i, (a, b) in enumerate(steps):
    cw = 360 if not wide else 330
    card = Image.new('RGBA', (cw, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, cw - 1, 149], 30, fill=(255, 255, 255, 242))
    d.ellipse([18, 37, 94, 113], fill=ORANGE + (255,)); fn = font(FONT_BLACK, 40); n = str(i + 1); d.text((56 - d.textlength(n, font=fn) / 2, 44), n, font=fn, fill=NAVY)
    fa = font(FONT_BLACK, 48 if len(a) <= 4 else 40)
    d.text((112, 22), a, font=fa, fill=NAVY); d.text((114, 92), b, font=font(FONT_BOLD, 28), fill=(90, 100, 120))
    img = pil_to_bgra(card)
    if wide: x, yy = W * (0.13 + 0.248 * i), H * 0.52
    else: x, yy = W * (0.30 if i % 2 == 0 else 0.70), y + 110 + i * 190
    lay.append(Sprite(img, x, yy, at=0.6 + i * 0.32, anim='pop', dur=0.45))
    if i < 3:
      ar = text_img('→' if wide else ('↘' if i % 2 == 0 else '↙'), 54, ORANGE)
      lay.append(Sprite(ar, (x + W * 0.124) if wide else W * 0.5, yy if wide else yy + 96, at=0.75 + i * 0.32, anim='fade', dur=0.3))
  bt = text_img(bottom, round(S * 0.62), WHITE, hl=bottom_hl, hl_mode='color')
  lay.append(Sprite(bt, W / 2, H * (0.86 if not wide else 0.80), at=0.6 + 4 * 0.32, anim='up', dur=0.5))
  return Shot(dur, lay, bg_navy(L), xin=xin, kind='zoom', name=name)

def outro(L, dur, kicker, line, line_hl, qr=False, credits=None, name='outro', xin=0.6):
  """しめ：小見出し → ひとこと → ロゴ → ストア検索 → 無料（広告表示あり）（YouTube は QR とクレジット）"""
  W, H = L['W'], L['H']; wide = W > H; S = L['card']; lay = []
  cx = W * (0.5 if not wide else 0.36)
  y = H * (0.17 if not wide else 0.10)
  t = text_img(kicker, round(S * 0.6), (255, 230, 190), fnt=FONT_BOLD)
  lay.append(Sprite(t, cx, y, at=0.1, anim='up', dur=0.5, anchor='top')); y += t.shape[0] + 6
  t = text_img(line, round(S * 0.78), WHITE, hl=line_hl, hl_mode='color')
  lay.append(Sprite(t, cx, y, at=0.25, anim='up', dur=0.5, anchor='top')); y += t.shape[0] + 30
  lp = logo_pill(round(W * (0.46 if not wide else 0.27)))
  lay.append(Sprite(lp, cx, y + lp.shape[0] / 2, at=0.45, anim='zoom', dur=0.7)); y += lp.shape[0] + 40
  t2 = text_img('App Store・Google Play で\n「マナトビ」と検索', round(S * 0.5), WHITE, fnt=FONT_BOLD, hl='マナトビ', hl_mode='color')
  lay.append(Sprite(t2, cx, y, at=0.9, anim='up', dur=0.5, anchor='top')); y += t2.shape[0] + 6
  lay.append(Sprite(pill_img('無料（広告表示あり）', round(S * 0.36), fg=NAVY, bg=WHITE), cx, y + 8, at=1.2, anim='fade', dur=0.5, anchor='top'))
  if qr:
    qs = round(H * 0.22)
    for i, (p, lab) in enumerate((('docs/business_overview/img/qr_appstore.png', 'App Store'), ('docs/business_overview/img/qr_googleplay.png', 'Google Play'))):
      q = Image.open(A(p)).convert('RGBA').resize((qs, qs), Image.LANCZOS)
      bx = Image.new('RGBA', (qs + 24, qs + 64), (0, 0, 0, 0)); ImageDraw.Draw(bx).rounded_rectangle([0, 0, bx.width - 1, bx.height - 1], 18, fill=WHITE)
      bx.alpha_composite(q, (12, 12)); d = ImageDraw.Draw(bx); f = font(FONT_BOLD, 26); tw = d.textlength(lab, font=f); d.text(((bx.width - tw) / 2, qs + 18), lab, font=f, fill=NAVY)
      lay.append(Sprite(pil_to_bgra(bx), W * 0.70 + i * (qs + 60), H * 0.30, at=1.4 + i * 0.15, anim='pop', dur=0.5))
    lay.append(mascot(A('public/mascots/trophy.webp'), round(H * 0.30), W * 0.80, H * 0.66, at=0.5))
  else:
    lay.append(mascot(A('public/mascots/trophy.webp'), round(H * 0.20), W * 0.5, H * 0.80, at=0.5))
  if credits:
    c = text_img(credits, 22 if wide else 24, (220, 228, 240), fnt=FONT_BOLD, line_gap=1.45, pad=10)
    lay.append(Sprite(c, W / 2, H - c.shape[0] - 6, at=1.6, anim='fade', dur=0.6, anchor='top'))
  return Shot(dur, lay, bg_blue(L), xin=xin, name=name)

def message(L, lines, dur, hl, name='message', xin=0.6, sub=None, mascot_file='happy.webp'):
  W, H = L['W'], L['H']; wide = W > H
  lay, y = lines_up(L, lines, H * (0.28 if not wide else 0.26), L['card'], hl=hl, at=0.3, step=0.7, cx=W * (0.5 if not wide else 0.40))
  if sub: lay.append(Sprite(text_img(sub, round(L['card'] * 0.42), (255, 230, 190), fnt=FONT_BOLD), W * (0.5 if not wide else 0.40), y + 24, at=0.3 + len(lines) * 0.7, anim='fade', dur=0.6, anchor='top'))
  lay.append(mascot(A('public/mascots', mascot_file), round(H * (0.24 if not wide else 0.52)), W * (0.5 if not wide else 0.80), H * (0.76 if not wide else 0.56), at=0.2))
  return Shot(dur, lay, bg_navy(L), xin=xin, name=name)

def ev_battle(b, answers):
  """対戦の効果音。b=dict(ticks, start, ok, final, finish, win, mission)（元の時刻）"""
  e = [(t, 'countdown', 0.5) for t in b['ticks']] + [(b['start'], 'start', 0.8)]
  e += [(a, 'tap', 0.45) for a in answers] + [(t, 'correct', 0.85) for t in b['ok']] + [(t + 0.05, 'combo', 0.45) for t in b['ok'][1:]]
  e += [(b['final'], 'final', 0.65), (b['finish'], 'timeup', 0.5), (b['win'], 'win', 0.8)]
  if b.get('mission'): e.append((b['mission'], 'badge', 0.6))
  return e

def voice_from_log(alog, skip=('tanjou.mp3',)):
  """録画 json の audio（[時刻, 'playing'|'pause'|'ended'|'seeked', src, 音源内の秒, 速さ]）→ [(元の時刻, ファイル, 音源の何秒から, 長さ)]"""
  out, cur = [], {}
  for t, ev, src, ct, rate in alog:
    if any(src.endswith(s) for s in skip) or '/bgm/' in src or '/sfx/' in src: continue
    f = A('public', src.lstrip('/').split('?')[0])
    if ev == 'playing': cur[src] = (t, ct)
    elif ev in ('pause', 'ended', 'seeked') and src in cur:
      t0, c0 = cur.pop(src)
      if t - t0 > 0.05: out.append((t0, f, c0, t - t0))
  for src, (t0, c0) in cur.items():   # 録画が終わった時点でまだ鳴っていた音は、音源の終わりまで（ショットの長さで切られる）
    out.append((t0, A('public', src.lstrip('/').split('?')[0]), c0, 60.0))
  return sorted(out)

def collect(shots):
  """ショットの層から効果音・音声（voice）を出力の時刻に並べる"""
  sfx, voice = [], []
  for s in shots:
    for (lt, f, g) in getattr(s, 'sfx', []): sfx.append((s.start + lt, f, g))
    for Lr in s.layers:
      if not isinstance(Lr, Video): continue
      end_local = Lr.until if Lr.until is not None else s.dur
      src_end = Lr.t0 + (end_local - Lr.at) * Lr.speed
      for (st, n, g) in getattr(Lr, 'ev', []):
        if Lr.t0 <= st < src_end: sfx.append((s.start + Lr.at + (st - Lr.t0) / Lr.speed, SFX(n) if not os.path.isabs(n) else n, g))
      if abs(Lr.speed - 1.0) > 1e-3: continue   # 速さを変えた所には声を重ねない（声の高さ・長さが合わなくなる）
      stop = min(src_end, Lr.freeze) if getattr(Lr, 'freeze', None) is not None else src_end   # 止めた所から先も鳴らさない
      for (pt, f, c0, d) in getattr(Lr, 'voice', []):
        a = max(Lr.t0, pt); b = min(stop, pt + d)
        if b - a > 0.05:
          voice.append(dict(f=f, src=c0 + (a - pt), at=s.start + Lr.at + (a - Lr.t0), dur=b - a, gain=1.0, fi=0.02, fo=0.12))
  return sorted(sfx), voice

def by(shots, name): return next(s for s in shots if s.name == name)

def sheet(TMP, name, L, shots, step=1.0):
  total = layout(shots); ims = []; T = 0.0; w = 216
  while T < total:
    act = [s for s in shots if s.start <= T < s.start + s.dur][-1]
    fr = act.render(T - act.start, L['W'], L['H']); h = round(L['H'] * w / L['W'])
    im = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA); cv2.putText(im, f'{T:.1f}', (4, 22), 0, 0.7, (0, 0, 255), 2)
    ims.append(im); T += step
  cols = 10 if L['H'] > L['W'] else 8; rows = (len(ims) + cols - 1) // cols; h = ims[0].shape[0]
  out = np.full((rows * h, cols * w, 3), 128, np.uint8)
  for i, im in enumerate(ims): out[(i // cols) * h:(i // cols + 1) * h, (i % cols) * w:(i % cols + 1) * w] = im
  cv2.imwrite(os.path.join(TMP, name + '_sheet.jpg'), out, [cv2.IMWRITE_JPEG_QUALITY, 80])
  for s in shots: s.close()
  print('sheet', name, f'{total:.1f}s', ' '.join(f'{s.name}@{s.start:.1f}' for s in shots), flush=True)

def frames(TMP, key, L, shots, ts):
  layout(shots); out = []
  for T in ts:
    act = [s for s in shots if s.start <= T < s.start + s.dur][-1]
    out.append(cv2.resize(act.render(T - act.start, L['W'], L['H']), (L['W'] // 2, L['H'] // 2), interpolation=cv2.INTER_AREA))
  for s in shots: s.close()
  cv2.imwrite(os.path.join(TMP, key + '_frames.jpg'), np.hstack(out), [cv2.IMWRITE_JPEG_QUALITY, 85])

def build(OUT, TMP, name, kind, L, shots, music_plan, chapter_titles=None, draft=False):
  """書き出し：--sheet で静止画一覧だけ、--audio-only で音だけ作り直し。YouTube はチャプターも書く"""
  if '--sheet' in sys.argv: return sheet(TMP, name, L, shots, float(os.environ.get('SHEET_STEP', '1')))
  total = layout(shots)
  print(name, f'{total:.1f}s', ' '.join(f'{s.name}@{s.start:.1f}' for s in shots), flush=True)
  sfx, voice = collect(shots); music = music_plan(shots, total)
  vid = os.path.join(TMP, name + '_v.mp4'); aud = os.path.join(TMP, name + '_a.m4a')
  if '--audio-only' in sys.argv and os.path.exists(vid): print('  映像はそのまま（音だけ作り直し）', flush=True)
  else: render_video(shots, L['W'], L['H'], vid, crf=21 if draft else 17, preset='veryfast' if draft else 'medium')
  js = mix_audio(total, music, voice, sfx, aud, TMP)
  final = os.path.join(OUT, name + '.mp4'); mux(vid, aud, final)
  if kind == 'youtube' and chapter_titles:
    rows = [(s.start, chapter_titles[s.name]) for s in shots if s.name in chapter_titles]; rows[0] = (0.0, rows[0][1]); keep = [rows[0]]
    for r in rows[1:]:
      if r[0] - keep[-1][0] >= 10 and total - r[0] >= 10: keep.append(r)
    open(os.path.join(OUT, name + '_CHAPTERS.txt'), 'w').write(''.join(f'{int(t // 60)}:{int(t % 60):02d} {n}\n' for t, n in keep))
  json.dump(dict(total=total, chapters=[(s.start, s.name) for s in shots], music=music, voice=[dict(v, f=os.path.basename(v['f'])) for v in voice],
                 sfx=[(a, os.path.basename(f), g) for a, f, g in sfx], loudness=js),
            open(os.path.join(TMP, name + '_timeline.json'), 'w'), ensure_ascii=False, indent=1)
  print('done', final, round(total, 2), flush=True)
