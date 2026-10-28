# 英語リスニング版の告知動画（リール 9:16 ／ ストーリーズ 9:16 ／ YouTube 16:9）2026-10-26
#   python3 store-assets/_tools/promo_listening.py <出力dir> [reel] [story] [youtube] [--draft] [--sheet] [--audio-only]
#   FRAMES=10,22.5 python3 store-assets/_tools/promo_listening.py <出力dir> reel   # 指定時刻の静止画だけ
#
# ■ 伝えること（英単語版と同じ組み立て：悩み → 迷い → 答え → 1本の道 → 実際の画面 → しめ）
#   ・英語リスニングは「聞き取れない」。スクリプトを読む？何度も聞く？ と練習のしかたにも迷う
#   ・マナトビは共通テストと同じ形式の全6大問（9単元）・135回分。1回ずつ完結
#   ・解く → 聞き直す（読まれている単語が光る）→ 音読（強弱・区切り・つながり）→ 対戦 までが「1本の道」
# ■ 素材：record_listening.py で録った本物のアプリ画面だけ（動画生成AIは使わない）。
#   問題の英語は、録画中にアプリが実際に鳴らした音源を同じ時刻に重ねたもの（録画 json の audio）
# ■ BGM：アプリに入っている4曲すべて（夕凪 → 誕生 → 風の列車 → カナリアスキップ → 誕生）。英語が鳴る間は自動で下がる
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from promo_parts import *  # noqa: F401,F403

args = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = args[0]; WHICH = args[1:] or ['reel', 'story', 'youtube']
DRAFT = '--draft' in sys.argv
TMP = os.path.join(OUT, '_work'); os.makedirs(TMP, exist_ok=True)
PH, PC = os.path.join(REC, 'lrec_ph'), os.path.join(REC, 'lrec_pc')
ROAD = ['解く', '聞き直す', '音読', '対戦']

# ---------------- 録画の中の時刻（record_listening.py の json と、measure.py で画面の変化から測ったもの） ----------------
UN, Q3, ST, BT = meta(PH, 'units'), meta(PH, 'q3'), meta(PH, 'studio'), meta(PH, 'battle')
UNp, Q3p, STp, BTp = meta(PC, 'units'), meta(PC, 'q3'), meta(PC, 'studio'), meta(PC, 'battle')
VQ3, VST, VBT = voice_from_log(Q3['audio']), voice_from_log(ST['audio']), voice_from_log(BT['audio'])
VQ3p, VSTp, VBTp = voice_from_log(Q3p['audio']), voice_from_log(STp['audio']), voice_from_log(BTp['audio'])
P1, P1p = VQ3[0][0], VQ3p[0][0]                    # 問題の音声が鳴りはじめた時刻
P2, P2p = VQ3[1][0], VQ3p[1][0]                    # 解説で「再生」した時刻
Q_OK, Q_OKp = 28.40, 28.33                         # 解答・解説が開いて「正解！」が出た時刻
SP, SPp = VST[0][0], VSTp[0][0]                    # 音読練習：聞きながら見る の再生
SP2 = VST[1][0] if len(VST) > 1 else 33.65         # 音読する の再生
SP2p = VSTp[1][0] if len(VSTp) > 1 else 33.65
_dd = [6.25, 5.21, 4.18, 3.15, 2.15, 1.11]          # START! の何秒前にカウントダウンの数字が変わるか（7→2）
B = dict(start=16.38, ok=[40.53, 69.97, 99.83, 129.23, 155.83], final=131.5, finish=160.53, win=162.27)
Bp = dict(start=16.2, ok=[42.77, 72.03, 102.17, 126.73, 156.97], final=130.0, finish=161.73, win=163.43)
B['ticks'] = [B['start'] - d for d in _dd]; Bp['ticks'] = [Bp['start'] - d for d in _dd]

# 第3問 第1回 問1 の英語（単語の時刻：public/read_along/listening_audio/el3_set1_q1.json、和訳：アプリの public/data/listeningTranslations.json）
_ra = json.load(open(A('public/read_along/listening_audio/el3_set1_q1.json')))
_jp = json.load(open(A('public/data/listeningTranslations.json')))['/listening_audio/el3_set1_q1.mp3|q_el3_set1_1']
KARAOKE = [(ln['who'], [(w[0], w[1] / 1000, w[2] / 1000) for w in ln['w']], _jp[i]) for i, ln in enumerate(_ra['lines'])]
LINE_END = [ln['w'][-1][2] / 1000 for ln in _ra['lines']]   # 各行が読み終わる時刻（音源の中）

# 収録の数（src/data/englishListeningData.ts の getListeningStats() と、各単元の practiceProblems＋miniTest を数えた値。2026-10-26）
N_SECTIONS, N_UNITS, N_ROUNDS, N_QS = 6, 9, 135, 554
UNIT_ROWS = [('第1問 A', '短い発話 → 合う英文', 14, '2回'), ('第1問 B', '短い発話 → 合う絵', 15, '2回'), ('第2問', '短い対話 → 合う絵', 16, '2回'),
             ('第3問', '短い対話 → 質問に答える', 15, '1回'), ('第4問 A', '発話を聞いて情報を整理', 15, '1回'), ('第4問 B', '複数の発話を比べる', 15, '1回'),
             ('第5問', '講義 ＋ ワークシート', 15, '1回'), ('第6問 A', '2人の会話', 15, '1回'), ('第6問 B', '3人の議論・図表', 15, '1回')]

# ---------------- 場面（どの形でも使う部品） ----------------
def sc_pain(L, dur, name='pain'):
  """聞き取れない：暗い背景・流れていく英語・ねむるとびら君"""
  W, H = L['W'], L['H']; wide = W > H; S = L['card']
  cx = W * (0.40 if wide else 0.5)
  lay, y = lines_up(L, ['英語リスニング、', '聞き取れない。'], H * (0.26 if wide else 0.27), S, hl='聞き取れない', cx=cx, at=0.2, step=0.6)
  rnd = np.random.RandomState(5)
  ws = ['Can I borrow this book?', 'Usually two weeks is the limit', "Then it's one week.", 'renew it once online',
        'How much will the man pay?', 'with your student ID card', "I'll do that if I need more time.", 'What did the woman decide?',
        'published last month', 'Are you a student?', 'Change to a van', 'the 8:20 bus']
  for i, wd in enumerate(ws):
    img = text_img(wd, int(rnd.randint(30, 44)), (150, 162, 190), fnt=FONT_BOLD)
    x0 = rnd.uniform(0.15, 0.85) * W; y0 = rnd.uniform(0.04, 0.95) * H
    lay.insert(0, Sprite(img, x0, y0, at=0.05 + i * 0.1, anim='fade', dur=0.5, alpha=0.45, drift=(rnd.uniform(-90, -50), 0, 0)))
  mh = round(H * (0.22 if not wide else 0.36))
  lay.append(mascot(A('public/mascots/sleeping.webp'), mh, W * (0.5 if not wide else 0.80), H * (0.72 if not wide else 0.64), at=0.5, anim='up', bob=(5, 3.2)))
  return Shot(dur, lay, bg_dusk(L), xin=0, name=name)

def sc_debate(L, dur, name='debate', xin=0.3):
  """迷い：スクリプトを読む vs とにかく何度も聞く"""
  W, H = L['W'], L['H']; wide = W > H; S = L['card']
  lay, _ = lines_up(L, ['どう練習するのが正解？'], H * (0.14 if not wide else 0.12), round(S * (0.72 if not wide else 0.8)), hl='正解', at=0.1)
  a = pill_img('スクリプトを読んで理解', round(S * 0.5), fg=NAVY, bg=WHITE, padx=40, pady=22)
  b = pill_img('とにかく何度も聞く', round(S * 0.5), fg=WHITE, bg=(200, 70, 70), padx=40, pady=22)
  vs = pill_img('VS', round(S * 0.6), fg=NAVY, bg=ORANGE, padx=26, pady=10)
  if wide:
    lay += [Sprite(a, W * 0.27, H * 0.44, at=0.45, anim='left', dur=0.5), Sprite(b, W * 0.73, H * 0.44, at=0.75, anim='right', dur=0.5),
            Sprite(vs, W * 0.5, H * 0.44, at=1.0, anim='pop', dur=0.4)]
    qs = [('どこが聞き取れなかった？', 0.20, 0.68), ('速くて追いつかない…', 0.50, 0.77), ('本番だと緊張する…', 0.80, 0.68)]
  else:
    lay += [Sprite(a, W * 0.5, H * 0.33, at=0.45, anim='left', dur=0.5), Sprite(vs, W * 0.5, H * 0.415, at=1.0, anim='pop', dur=0.4),
            Sprite(b, W * 0.5, H * 0.50, at=0.75, anim='right', dur=0.5)]
    qs = [('どこが聞き取れなかった？', 0.40, 0.61), ('速くて追いつかない…', 0.62, 0.66), ('本番だと緊張する…', 0.36, 0.71)]
  for i, (t, x, yy) in enumerate(qs):
    lay.append(Sprite(text_img(t, round(S * 0.42), (205, 214, 232), fnt=FONT_BOLD), W * x, H * yy, at=1.35 + i * 0.25, anim='pop', dur=0.4, bob=(5, 2.2 + i * 0.3)))
  lay.append(mascot(A('public/mascots/thinking.webp'), round(H * (0.16 if not wide else 0.26)), W * (0.78 if not wide else 0.91), H * (0.85 if not wide else 0.84), at=0.6, anim='up'))
  return Shot(dur, lay, bg_dusk(L), xin=xin, kind='fade', name=name)

def sc_answer(L, dur, name='answer', xin=0.12, table=False):
  """答え：共通テストと同じ形式の全6大問・135回分（カウンター）"""
  W, H = L['W'], L['H']; wide = W > H; S = L['card']
  cx = W * (0.30 if (wide and table) else 0.5)
  lay = []
  kick = pill_img('マナトビのリスニング', round(S * 0.42), fg=NAVY, bg=ORANGE)
  y = H * (0.15 if not wide else 0.12)
  lay.append(Sprite(kick, cx, y, at=0.05, anim='pop', dur=0.4, anchor='top')); y += kick.shape[0] + 26
  t, y = lines_up(L, ['共通テストと同じ形式で、', f'全{N_SECTIONS}大問。'], y, round(S * (0.74 if not wide else 0.64)), hl=f'全{N_SECTIONS}大問', at=0.2, step=0.45, cx=cx)
  lay += t; y += 30
  num_y = y; big = round(S * (2.3 if not wide else 1.7)); unit = text_img('回分', round(big * 0.36), WHITE)
  cache = {}
  def counter(cv, lt):
    u = ease_out(clamp01((lt - 0.9) / 1.4)); n = int(round(N_ROUNDS * u))
    if n not in cache: cache.clear(); cache[n] = text_img(f'{n}', big, ORANGE, shadow=(0, 8, (6, 10, 24, 150)), pad=10)
    img = cache[n]; tw = img.shape[1] + unit.shape[1]; x0 = cx - tw / 2
    a = smooth((lt - 0.8) / 0.3); blit(cv, img, x0, num_y, a); blit(cv, unit, x0 + img.shape[1] - 6, num_y + img.shape[0] - unit.shape[0] - big * 0.12, a)
  lay.append(Func(counter))
  y = num_y + big * 1.35
  sub = text_img(f'{N_UNITS}単元・全{N_QS}問　1回ずつ完結', round(S * 0.42), (255, 230, 190), fnt=FONT_BOLD)
  lay.append(Sprite(sub, cx, y, at=2.2, anim='fade', dur=0.5, anchor='top')); y += sub.shape[0] + 14
  sub2 = text_img('読み上げも本番どおり（前半2回・後半1回）', round(S * 0.36), (220, 228, 244), fnt=FONT_BOLD)
  lay.append(Sprite(sub2, cx, y, at=2.5, anim='fade', dur=0.5, anchor='top'))
  if table:
    tx = W * 0.73; ty = H * 0.08; f = round(S * 0.31)
    for i, (nm, desc, n, rd) in enumerate(UNIT_ROWS):
      row = Image.new('RGBA', (640, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
      d.rounded_rectangle([0, 0, 639, 73], 18, fill=(255, 255, 255, 238))
      d.rounded_rectangle([12, 14, 132, 60], 12, fill=(222, 234, 252, 255) if rd == '2回' else (220, 244, 238, 255))
      fk = font(FONT_BLACK, 24); d.text((72 - d.textlength(nm, font=fk) / 2, 21), nm, font=fk, fill=BLUE if rd == '2回' else (30, 120, 110))
      d.text((148, 20), desc, font=font(FONT_BOLD, f), fill=NAVY)
      s = f'{n}回'; fb = font(FONT_BLACK, f); d.text((622 - d.textlength(s, font=fb), 18), s, font=fb, fill=NAVY)
      lay.append(Sprite(pil_to_bgra(row), tx, ty + i * 82, at=1.0 + i * 0.12, anim='right', dur=0.4, anchor='top'))
  else:
    lay.append(mascot(A('public/mascots/listening.webp'), round(H * 0.19), W * 0.5, H * 0.85, at=0.6))
  return Shot(dur, lay, bg_blue(L), xin=xin, kind='flash', flash=[0.0], name=name)

def roadmap(L, dur):
  return sc_steps(L, dur, ['1問ずつ、', 'こなすだけ。'], '1問ずつ', [('解く', '本番形式'), ('聞き直す', '光る英文'), ('音読', '強弱・区切り'), ('対戦', 'AI・全国')],
                  '1本の道で、「聞き取れた！」へ。', '聞き取れた！')

def kara(L, audio_at, audio_from=0.0, y=1330, cx=None, maxw=None, size=None):
  wide = L['W'] > L['H']
  return Karaoke(KARAOKE, audio_at=audio_at, audio_from=audio_from, cx=cx or L['W'] / 2, y=y,
                 maxw=maxw or (960 if not wide else 1000), size=size or (44 if not wide else 40), jp_size=30 if not wide else 28)

def outro_l(L, dur, **kw):
  return outro(L, dur, f'共通テスト英語リスニング 全{N_SECTIONS}大問', '聞いて、解いて、競って。', '競って', **kw)

def ev_q(taps=(), ok=None):
  e = [(t, 'tap', 0.45) for t in taps]
  if ok: e.append((ok, 'correct', 0.85))
  return e

# ---------------- 台本：リール（9:16・約80秒） ----------------
def reel(L):
  S = []
  S.append(sc_pain(L, 4.2))
  S.append(sc_debate(L, 4.1))
  S.append(sc_answer(L, 4.6))
  S.append(roadmap(L, 4.0))
  un, q3, st, bt = mp4(PH, 'units'), mp4(PH, 'q3'), mp4(PH, 'studio'), mp4(PH, 'battle')
  # STEP1 解く：大問タブ → 第3問を聞く（英語の字幕は読まれた単語から光る＋和訳）→ 答える → 正解
  S.append(full(L, un, 2.3, 11.2, PHONE_SRC, roi=[(0, (0, 60, 860, 1500))], speed=2.2, ev=ev_q(UN['taps'][2:]),
                layers=[road(L, ROAD, 0), caption(L, f'全{N_SECTIONS}大問・{N_UNITS}単元から選ぶ', hl=f'全{N_SECTIONS}大問', step='STEP 1  解く')], xin=0.25, kind='slide', name='s1a'))
  t0 = P1 - 0.8; t1 = P1 + LINE_END[1] + 0.4   # 2行目まで聞かせて、答える場面へ
  S.append(full(L, q3, t0, t1, PHONE_SRC, roi=[(0, (0, 140, 860, 1700))], voice=VQ3, ev=ev_q([Q3['taps'][5]]),
                layers=[road(L, ROAD, 0, anim=None), caption(L, 'イヤホンで、本番形式の英語を', hl='本番形式', step='STEP 1  解く', at=-1),
                        kara(L, P1 - t0)], xin=0.2, name='s1b'))
  S.append(full(L, q3, 25.9, 29.9, PHONE_SRC, roi=[(0, (0, 140, 860, 1700)), (1.6, (0, 140, 860, 1700)), (2.4, (0, 300, 860, 1864))],
                ev=ev_q([Q3['taps'][6], Q3['taps'][7]], Q_OK), punch=[to_out(Q_OK, 25.9)],
                layers=[road(L, ROAD, 0, anim=None), caption(L, '答えたら、すぐ採点', hl='すぐ採点', step='STEP 1  解く', at=-1)], xin=0.12, name='s1c'))
  # STEP2 聞き直す：解説で再生 → 読まれている単語が光る
  S.append(full(L, q3, P2 + 2.9, P2 + 8.6, PHONE_SRC, roi=[(0, (0, 560, 860, 1864))], voice=VQ3,   # 採点の札が消えてから（2行目から）
                layers=[road(L, ROAD, 1), caption(L, '読まれている単語が、光る', hl='光る', step='STEP 2  聞き直す')], xin=0.25, kind='slide', name='s2'))
  # STEP3 音読：強弱・区切り・つながり → 音読する
  S.append(full(L, st, SP + 2.9, SP + 7.4, PHONE_SRC, roi=[(0, (0, 90, 860, 1500))], voice=VST,
                layers=[road(L, ROAD, 2), caption(L, '強弱・区切り・つながりが見える', hl='見える', step='STEP 3  音読')], xin=0.25, kind='slide', name='s3a'))
  S.append(full(L, st, 32.2, SP2 + 3.0, PHONE_SRC, roi=[(0, (0, 90, 860, 1500))], voice=VST, ev=ev_q(ST['taps'][9:12]),
                layers=[road(L, ROAD, 2, anim=None), caption(L, '声に出して、いっしょに読む', hl='声に出して', step='STEP 3  音読', at=-1)], xin=0.15, name='s3b'))
  # STEP4 対戦：リスニングで AI と（START! で曲のサビ）
  evb = ev_battle(B, BT['answers'])
  S.append(full(L, bt, 1.9, 9.4, PHONE_SRC, roi=[(0, (0, 100, 860, 1700))], speed=2.0, ev=ev_q(BT['taps'][1:7]),
                layers=[road(L, ROAD, 3), caption(L, 'リスニングで、対戦', hl='対戦', step='STEP 4  対戦')], xin=0.25, kind='slide', name='s4a'))
  S.append(full(L, bt, 12.9, B['start'] + 0.05, PHONE_SRC, roi=[(0, (0, 150, 860, 1400))], ev=evb, layers=[road(L, ROAD, 3, anim=None)], xin=0.15, name='countdown'))
  broi = (0, 0, 860, 1560)
  S.append(full(L, bt, B['start'] + 0.5, 22.4, PHONE_SRC, roi=[(0, broi), (5.5, (20, 60, 840, 1400))], voice=VBT, ev=evb, kind='flash', xin=0.12, flash=[0.0], punch=[0.0],
                layers=[road(L, ROAD, 3, anim=None), caption(L, '聞き終えてから、早押し4択', hl='早押し', step='STEP 4  対戦')], name='b1'))
  S.append(full(L, bt, 38.7, 41.4, PHONE_SRC, roi=[(0, broi)], ev=evb, punch=[to_out(B['ok'][0], 38.7)], xin=0.1, name='b1ok'))
  for i, (a, b) in enumerate([(69.0, 70.9), (98.9, 100.7)]):
    S.append(full(L, bt, a, b, PHONE_SRC, roi=[(0, broi), (b - a, (40, 40, 820, 1400))], ev=evb, xin=0.08, kind='flash' if i == 0 else 'fade',
                  punch=[to_out(B['ok'][i + 1], a)], name=f'mont{i}'))
  S.append(full(L, bt, 131.3, 135.3, PHONE_SRC, roi=[(0, broi)], voice=VBT, ev=evb, xin=0.1, kind='flash', flash=[0.0],
                layers=[road(L, ROAD, 3, anim=None), caption(L, 'ラスト1問', hl='ラスト', step='STEP 4  対戦')], name='finalq'))
  S.append(full(L, bt, 154.7, 156.9, PHONE_SRC, roi=[(0, broi)], ev=evb, punch=[to_out(B['ok'][4], 154.7)], xin=0.1, name='finalok'))
  S.append(full(L, bt, 160.2, 162.3, PHONE_SRC, roi=[(0, broi)], ev=evb, xin=0.1, shake=[to_out(B['finish'], 160.2)], flash=[to_out(B['finish'], 160.2)], name='finish'))
  S.append(full(L, bt, 162.3, 167.2, PHONE_SRC, roi=[(0, (0, 0, 860, 1700)), (4.9, (40, 0, 820, 1450))], ev=evb, xin=0.15,
                layers=[road(L, ROAD, 4, anim=None), caption(L, '勝てたら、レベルアップ', hl='レベルアップ', at=1.6)], name='victory'))
  S.append(message(L, ['「聞き取れた！」を、', '毎日ひとつずつ。'], 4.8, '毎日ひとつずつ', sub='どこが聞き取れなかったか、もう迷わない。', mascot_file='listening.webp'))
  S.append(outro_l(L, 5.8, xin=0.5))
  return S

# ---------------- 台本：ストーリーズ（9:16・約28秒・上下は UI の分だけあける） ----------------
def story(L):
  S = []
  S.append(sc_pain(L, 2.9))
  S.append(sc_answer(L, 3.9))
  q3, st, bt = mp4(PH, 'q3'), mp4(PH, 'studio'), mp4(PH, 'battle')
  t0 = P1 - 0.4
  S.append(full(L, q3, t0, P1 + LINE_END[0] + 0.6, PHONE_SRC, roi=[(0, (0, 140, 860, 1700))], voice=VQ3,
                layers=[road(L, ROAD, 0), caption(L, '本番形式で解く', hl='本番形式', step='STEP 1'), kara(L, P1 - t0, y=1320, maxw=900, size=40)],
                xin=0.2, kind='slide', name='s1'))
  S.append(full(L, q3, P2 + 3.0, P2 + 6.2, PHONE_SRC, roi=[(0, (0, 560, 860, 1864))], voice=VQ3,
                layers=[road(L, ROAD, 1), caption(L, '光る英文で聞き直す', hl='光る英文', step='STEP 2')], xin=0.12, name='s2'))
  S.append(full(L, st, SP + 3.0, SP + 6.0, PHONE_SRC, roi=[(0, (0, 90, 860, 1500))], voice=VST,
                layers=[road(L, ROAD, 2), caption(L, '音読で口になじませる', hl='音読', step='STEP 3')], xin=0.12, name='s3'))
  evb = ev_battle(B, BT['answers'])
  S.append(full(L, bt, 14.4, B['start'] + 0.05, PHONE_SRC, roi=[(0, (0, 150, 860, 1400))], ev=evb,
                layers=[road(L, ROAD, 3), caption(L, 'リスニングで対戦', hl='対戦', step='STEP 4')], xin=0.12, name='countdown'))
  S.append(full(L, bt, 154.9, 156.7, PHONE_SRC, roi=[(0, (0, 0, 860, 1560))], ev=evb, xin=0.08, kind='flash', flash=[0.0], punch=[to_out(B['ok'][4], 154.9)], name='b1'))
  S.append(full(L, bt, 160.25, 162.3, PHONE_SRC, roi=[(0, (0, 0, 860, 1560))], ev=evb, xin=0.08, shake=[to_out(B['finish'], 160.25)], flash=[to_out(B['finish'], 160.25)], name='finish'))
  S.append(full(L, bt, 162.3, 164.9, PHONE_SRC, roi=[(0, (0, 0, 860, 1700))], ev=evb, xin=0.12, name='victory'))
  S.append(outro_l(L, 4.8, xin=0.4))
  return S

# ---------------- 台本：YouTube（16:9・パソコン版を中心に） ----------------
def youtube(L):
  W, H = L['W'], L['H']; S = []
  S.append(sc_pain(L, 4.6))
  S.append(sc_debate(L, 5.0))
  S.append(sc_answer(L, 6.6, table=True))
  S.append(roadmap(L, 4.6))
  pu, pq, ps, pb = mp4(PC, 'units'), mp4(PC, 'q3'), mp4(PC, 'studio'), mp4(PC, 'battle')
  cy = H - 128
  # STEP1 解く
  S.append(full(L, pu, 2.0, 11.1, PC_SRC, roi=[(0, (180, 30, 1600, 620)), (5.0, (180, 30, 1500, 560))], speed=1.5, ev=ev_q(UNp['taps'][2:]),
                layers=[road(L, ROAD, 0), caption(L, f'共通テストと同じ全{N_SECTIONS}大問・{N_UNITS}単元', hl=f'全{N_SECTIONS}大問', step='STEP 1  解く', y=cy)], xin=0.3, kind='slide', name='s1a'))
  t0 = P1p - 1.0; t1 = P1p + LINE_END[3] + 0.35
  S.append(full(L, pq, t0, t1, PC_SRC, roi=[(0, (0, 60, 1900, 560)), (3.0, (0, 60, 1900, 560)), (5.5, (0, 90, 1090, 380))], voice=VQ3p, ev=ev_q([Q3p['taps'][5]]),
                layers=[road(L, ROAD, 0, anim=None), kara(L, P1p - t0, y=640, cx=W / 2, maxw=1200, size=42),
                        caption(L, 'イヤホンで、本番形式の英語を聞く', hl='本番形式', step='STEP 1  解く', at=-1, y=cy)], xin=0.2, name='s1b'))
  S.append(full(L, pq, 25.9, 30.2, PC_SRC, roi=[(0, (0, 60, 1900, 560)), (1.7, (0, 60, 1900, 560)), (2.6, (20, 80, 1380, 840))],
                ev=ev_q([Q3p['taps'][6], Q3p['taps'][7]], Q_OKp), punch=[to_out(Q_OKp, 25.9)],
                layers=[road(L, ROAD, 0, anim=None), caption(L, '答えたら、すぐ採点', hl='すぐ採点', step='STEP 1  解く', at=-1, y=cy)], xin=0.12, name='s1c'))
  # STEP2 聞き直す（復習用の音源：読まれている単語が光る・和訳つき）
  S.append(full(L, pq, P2p + 2.9, P2p + 11.0, PC_SRC, roi=[(0, (20, 180, 980, 680)), (3.0, (20, 230, 980, 730)), (6.0, (20, 200, 1380, 960))], voice=VQ3p,
                layers=[road(L, ROAD, 1), caption(L, '読まれている単語が光る。和訳と「聞き取りの決め手」も', hl='光る', step='STEP 2  聞き直す', y=cy)],
                xin=0.3, kind='slide', name='s2'))
  # STEP3 音読
  sroi = (540, 140, 1380, 620)
  S.append(full(L, ps, SPp + 2.9, SPp + 8.6, PC_SRC, roi=[(0, sroi)], voice=VSTp,
                layers=[road(L, ROAD, 2), caption(L, '強弱・区切り・つながりが見える音読練習', hl='音読練習', step='STEP 3  音読', y=cy)], xin=0.3, kind='slide', name='s3a'))
  S.append(full(L, ps, 30.9, SP2p + 3.8, PC_SRC, roi=[(0, sroi)], voice=VSTp, ev=ev_q(STp['taps'][9:12]),
                layers=[road(L, ROAD, 2, anim=None), caption(L, 'いっしょに読む・追いかける・語群ごとに止まる', hl='いっしょに読む', step='STEP 3  音読', at=-1, y=cy)], xin=0.15, name='s3b'))
  # STEP4 対戦
  app = (430, 0, 1490, 1080); evb = ev_battle(Bp, BTp['answers'])
  S.append(full(L, pb, 1.9, 9.4, PC_SRC, roi=[(0, (1090, 0, 1340, 460))], speed=1.8, ev=ev_q(BTp['taps'][1:7]),
                layers=[road(L, ROAD, 3), caption(L, 'リスニングで、AI・友だち・全国と対戦', hl='対戦', step='STEP 4  対戦', y=cy)], xin=0.3, kind='slide', name='s4a'))
  S.append(full(L, pb, 12.8, Bp['start'] + 0.05, PC_SRC, roi=[(0, (560, 100, 1360, 560))], ev=evb, layers=[road(L, ROAD, 3, anim=None)], xin=0.15, name='countdown'))
  qroi = (370, 200, 1470, 840)
  S.append(full(L, pb, Bp['start'] + 0.5, 23.6, PC_SRC, roi=[(0, (370, 120, 1480, 860)), (6.0, qroi)], voice=VBTp, ev=evb, kind='flash', xin=0.12, flash=[0.0], punch=[0.0],
                layers=[caption(L, '音声を聞き終えてから、早押し4択', hl='早押し', y=cy)], name='b1'))
  S.append(full(L, pb, 41.6, 44.2, PC_SRC, roi=[(0, qroi)], ev=evb, punch=[to_out(Bp['ok'][0], 41.6)], xin=0.1, name='b1ok'))
  for i, (a, b) in enumerate([(71.2, 73.4), (101.3, 103.5)]):
    S.append(full(L, pb, a, b, PC_SRC, roi=[(0, qroi), (b - a, (400, 220, 1440, 820))], ev=evb, xin=0.08, kind='flash' if i == 0 else 'fade',
                  punch=[to_out(Bp['ok'][i + 1], a)], name=f'mont{i}'))
  S.append(full(L, pb, 129.8, 134.6, PC_SRC, roi=[(0, qroi)], voice=VBTp, ev=evb, xin=0.1, kind='flash', flash=[0.0],
                layers=[caption(L, 'ラスト1問', hl='ラスト', y=cy)], name='finalq'))
  S.append(full(L, pb, 155.8, 158.2, PC_SRC, roi=[(0, qroi)], ev=evb, punch=[to_out(Bp['ok'][4], 155.8)], xin=0.1, name='finalok'))
  S.append(full(L, pb, 161.4, 163.5, PC_SRC, roi=[(0, (420, 160, 1660, 900))], ev=evb, xin=0.1, shake=[to_out(Bp['finish'], 161.4)], flash=[to_out(Bp['finish'], 161.4)], name='finish'))
  pv = V(pb, 163.5, (90, 180, 1180, 664), PC_SRC, roi=[(0, app)], device='pc', ev=evb)
  phv = V(mp4(PH, 'battle'), 162.3, (1390, 150, 390, 845), PHONE_SRC, device='phone')
  S.append(Shot(5.4, [pv, phv, caption(L, 'パソコンでも、スマホでも。勝てたらレベルアップ', hl='レベルアップ', y=H - 110, at=1.4)], bg_navy(L), xin=0.15, name='victory'))
  S.append(message(L, ['「聞き取れた！」を、', '毎日ひとつずつ。'], 5.2, '毎日ひとつずつ', sub='どこが聞き取れなかったか、もう迷わない。', mascot_file='listening.webp'))
  S.append(outro_l(L, 10.5, qr=True, credits=CREDITS_LINE, xin=0.5))
  return S

CREDITS_LINE = ('BGM：「誕生」（マナトビ）／「夕凪」作曲 やっすん・「風の列車」作曲 坂田白　配布元：創作堂さくら紅葉 https://yukizakura.net/\n'
                '「カナリアスキップ」作曲 まんぼう二等兵（OpenTracks）　効果音・英語音声：マナトビ')

# ---------------- 音 ----------------
def music_plan(shots, total):
  """4曲：夕凪（聞き取れない）→ 誕生（答え）→ 風の列車（解く〜音読。英語が鳴る間は自動で下がる）→ カナリアスキップ（対戦）→ 誕生（しめ）"""
  m = []
  ans = by(shots, 'answer'); first_step = next(s for s in shots if s.name.startswith('s1'))
  cd = by(shots, 'countdown'); start_at = cd.start + cd.dur
  fin = by(shots, 'finish'); out = by(shots, 'outro')
  m.append(dict(f=WAITING, src=0.0, at=0.0, dur=ans.start + 0.7, gain=1.5, fi=0.4, fo=1.1))   # 白く光る所で重ねて受け渡す
  t_end1 = first_step.start + 0.6
  m.append(dict(f=TANJOU, src=22.95 - 0.25, at=ans.start - 0.25, dur=t_end1 - ans.start + 0.25, gain=0.85, fi=0.3, fo=0.8))
  tr_at = first_step.start - 1.6; tr_end = cd.start + 0.4
  m.append(dict(f=TRAIN, src=7.0 - 1.6, at=tr_at, dur=tr_end - tr_at, gain=1.25, fi=1.2, fo=0.9))
  c_at = max(cd.start, start_at - 7.0); c_end = fin.start + fin.dur + 0.6
  m.append(dict(f=CANARY, src=7.0 - (start_at - c_at), at=c_at, dur=c_end - c_at, gain=1.6, fi=0.5, fo=1.0))
  s_at = c_end - 1.2; src2 = max(0.0, 123.1 - (out.start + 0.45 - s_at))
  m.append(dict(f=TANJOU, src=src2, at=s_at, dur=min(total - s_at, 134.8 - src2), gain=0.75, fi=1.2, fo=1.6))
  return m

TITLES = {'pain': 'オープニング：リスニング、聞き取れない？', 'answer': '共通テストと同じ全6大問・135回分', 's1a': 'STEP1 解く（本番形式）',
          's2': 'STEP2 聞き直す（光る英文）', 's3a': 'STEP3 音読（強弱・区切り・つながり）', 's4a': 'STEP4 対戦（リスニング）', 'message': 'エンディング'}

FR = os.environ.get('FRAMES')
JOBS = (('reel', reel, 'listening_reel_9x16'), ('story', story, 'listening_story_9x16'), ('youtube', youtube, 'listening_youtube_16x9'))
for k, fn, nm in JOBS:
  if k not in WHICH: continue
  L = LAYOUTS[k]
  if FR: frames(TMP, k, L, fn(L), [float(x) for x in FR.split(',')]); continue
  build(OUT, TMP, nm, k, L, fn(L), music_plan, TITLES, draft=DRAFT)
