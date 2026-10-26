# 英語リスニング版の告知動画用：実際のアプリを操作して録画する（2026-10-26）
#   python3 store-assets/_tools/record_listening.py <出力dir> [場面名...]
#   REC_DEVICE=pc で PC 版（1920×1080）。既定はスマホ実寸（430×932・2倍密度 → 860×1864）
#
# 場面（1本の道筋：解く → 聞き直す → 音読 → 対戦）
#   units    学習 → 英語リスニング → 大問タブ Q1A〜Q6B を順に押す（全6大問・9単元）
#   q3       第3問 第1回 問1：再生 → 対話を最後まで聞く → ③ One week → 解答・解説 → 解説の再生（読まれた単語が光る）
#   studio   同じ問題の解説 → 音読練習：聞きながら見る（強弱・区切り・つながり）→ 音読する
#   battle   AI と対戦（英語リスニング・第3問・5問・マナボ（受験生））：音声を聞き終えてから正解を押す
# ・録画は無音（--mute-audio）。アプリの中で実際に鳴った音源と、その再生・停止の時刻を json の audio に残す
#   → 編集で同じ音源を同じ時刻に重ねる（問題の英語は本物の音）。
# ・広告なし（?no_ads=1）・ゲスト（個人情報なし）。
import asyncio, base64, json, os, re, subprocess, sys, time, random
from playwright.async_api import async_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BASE = os.environ.get('APP_URL', 'http://localhost:4175')
DEVICE = os.environ.get('REC_DEVICE', 'phone')
VIEW = {'phone': dict(width=430, height=932, scale=2, mobile=True), 'pc': dict(width=1920, height=1080, scale=1, mobile=False)}[DEVICE]
OUT = sys.argv[1]; ONLY = set(sys.argv[2:]); os.makedirs(OUT, exist_ok=True)
random.seed(11)

# 対戦の正解：出題プール（選択肢の並び → 正解の文字）
_pool = open(os.path.join(ROOT, 'src/battle/data/pool.english_listening.generated.ts')).read()
ANS = {}
for r in re.findall(r'\n  (\[.*?\]),?(?=\n)', _pool[_pool.index('export const POOL'):]):
  row = json.loads(r); opts = row[7]
  ANS['|'.join(sorted(opts))] = opts[row[8]]

TAP_CSS = """
.__tap{position:fixed;z-index:2147483647;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;
 background:rgba(255,255,255,.55);border:3px solid rgba(34,74,140,.9);pointer-events:none;animation:__tap .55s ease-out forwards}
@keyframes __tap{0%{transform:scale(.4);opacity:1}100%{transform:scale(1.35);opacity:0}}
"""
DEMO_STORAGE = {'hasCompletedOnboarding': 'true', 'savedIsGuest': 'true'}
# 音源の再生・停止を時刻つきで記録（performance.now）
AUDIO_LOG = """window.__alog=[];for(const ev of ['playing','pause','ended','seeked']){document.addEventListener(ev,e=>{const a=e.target;
 if(a&&a.currentSrc) window.__alog.push([performance.now(),ev,a.currentSrc,a.currentTime,a.playbackRate])},true)}"""

def now(pg): return round(asyncio.get_event_loop().time() - pg._t0, 3)

async def tap_box(pg, box, pause):
  await pg.evaluate("""([x,y]) => { const d=document.createElement('div'); d.className='__tap'; d.style.left=x+'px'; d.style.top=y+'px';
    document.body.appendChild(d); setTimeout(()=>d.remove(), 700); }""", [box['x'], box['y']])
  await pg.wait_for_timeout(180)
  pg._taps.append(now(pg))
  await pg.mouse.click(box['x'], box['y'])
  await pg.wait_for_timeout(pause)

async def tap(pg, js, pause=900, scroll=True):
  box = await pg.evaluate("""([js, sc]) => { const el = (new Function('return ' + js))(); if (!el) return null;
    if (sc === 'center') el.scrollIntoView({block:'center'}); else if (sc) el.scrollIntoView({block:'nearest'}); const r = el.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2}; }""", [js, scroll])
  if not box: raise RuntimeError('not found: ' + js[:140])
  await tap_box(pg, box, pause)

def btn(text, sel='button,[role=tab],[role=radio],a', exact=False):
  t = json.dumps(text)
  cond = f"b.innerText.replace(/\\s+/g,' ').trim()==={t}" if exact else f"b.innerText.replace(/\\s+/g,' ').includes({t})"
  return f"[...document.querySelectorAll('{sel}')].filter(b=>b.offsetParent&&{cond})[0]"

PLAY = "[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&(b.innerText.trim()==='再生'||/^問1\\s/.test(b.innerText.trim())))[0]"

async def open_q3(pg):
  await tap(pg, btn('学習'), 1000)
  await tap(pg, btn('英語リスニング'), 1300)
  await tap(pg, btn('第3問'), 1100)
  await tap(pg, btn('第1回演習'), 1300)
  await tap(pg, btn('問題をはじめる'), 1600)

async def wait_audio_end(pg, limit=25000):
  for _ in range(limit // 200):
    if await pg.evaluate("()=>{const a=[...document.querySelectorAll('audio')].find(a=>!a.paused);return !a}"): return
    await pg.wait_for_timeout(200)

# ---------------- 場面 ----------------
async def scene_units(pg):
  await tap(pg, btn('学習'), 1000)
  pg._mark = now(pg)
  await tap(pg, btn('英語リスニング'), 1500)
  for t in ['第1問 B', '第2問', '第3問', '第4問 A', '第4問 B', '第5問', '第6問 A', '第6問 B']:
    await tap(pg, btn(t), 750)
  await pg.wait_for_timeout(600)

async def scene_q3(pg):
  await open_q3(pg)
  pg._mark = now(pg)
  await pg.wait_for_timeout(900)
  pg._play = now(pg)
  await tap(pg, PLAY, 400)
  await wait_audio_end(pg)
  await pg.wait_for_timeout(700)
  pg._answers = [now(pg) + 0.18]
  await tap(pg, btn('③ One week'), 1100)
  pg._ex = now(pg)
  await tap(pg, btn('解答と解説を見る'), 2600)
  pg._play2 = now(pg)
  await tap(pg, PLAY, 400, scroll=False)
  await wait_audio_end(pg)
  await pg.wait_for_timeout(900)

async def scene_studio(pg):
  await open_q3(pg)
  await tap(pg, btn('③ One week'), 700)
  await tap(pg, btn('解答と解説を見る'), 2200)
  pg._mark = now(pg)
  await tap(pg, btn('音読練習'), 1600, scroll='center')
  pg._play = now(pg)
  await tap(pg, "document.querySelector('.ra-play')", 400, scroll=False)
  await wait_audio_end(pg)
  await pg.wait_for_timeout(700)
  pg._speak = now(pg)
  await tap(pg, btn('音読する', '[role=tab]'), 1100)
  await tap(pg, btn('いっしょに読む'), 900)
  await tap(pg, "document.querySelector('.ra-play')", 5200, scroll=False)

BATTLE_PICK = """(ans)=>{
  const bs=[...document.querySelectorAll('.grid button')].filter(b=>b.offsetParent&&!b.disabled); if(bs.length<2) return null;
  const opts=bs.map(b=>b.innerText.trim()); const a=ans[[...opts].sort().join('|')];
  const i=opts.indexOf(a); return i<0?0:i }"""

async def scene_battle(pg):
  await tap(pg, btn('対戦'), 1400)
  pg._mark = now(pg)
  await tap(pg, btn('AIと対戦'), 1200)
  await tap(pg, btn('5 さっと'), 800)
  await tap(pg, btn('英語リスニング'), 1200)
  await tap(pg, btn('第3問'), 1200)
  await tap(pg, btn('マナボ（受験生）'), 1100)
  await tap(pg, btn('はじめる'), 400)
  pg._start = now(pg)
  await pg.wait_for_timeout(8300)
  pg._answers = []
  for q in range(5):
    for _ in range(60):
      if await pg.evaluate("()=>[...document.querySelectorAll('.grid button')].filter(b=>b.offsetParent&&!b.disabled).length>=2"): break
      await pg.wait_for_timeout(200)
    await pg.wait_for_timeout(1500)
    await wait_audio_end(pg, 22000)            # 聞き終えてから答える（アプリの注意書きどおり）
    await pg.wait_for_timeout(500 + random.randint(0, 500))
    i = await pg.evaluate(BATTLE_PICK, ANS)
    if i is None: break
    pg._answers.append(now(pg) + 0.18)
    await tap(pg, f"[...document.querySelectorAll('.grid button')].filter(b=>b.offsetParent&&!b.disabled)[{i}]", 2400)
  await pg.wait_for_timeout(11000)

SCENES = [('units', scene_units), ('q3', scene_q3), ('studio', scene_studio), ('battle', scene_battle)]

async def record(b, name, fn):
  ctx = await b.new_context(viewport={'width': VIEW['width'], 'height': VIEW['height']}, device_scale_factor=VIEW['scale'],
                            is_mobile=VIEW['mobile'], has_touch=VIEW['mobile'])
  await ctx.add_init_script("try{" + "".join(f"localStorage.setItem({json.dumps(k)},{json.dumps(v)});" for k, v in DEMO_STORAGE.items()) + "}catch(e){}" + AUDIO_LOG)
  pg = await ctx.new_page(); pg.set_default_timeout(30000)
  await pg.goto(BASE + '/?no_ads=1&screenshot=1', wait_until='domcontentloaded', timeout=240000)
  await pg.wait_for_function('!!window.__ENTER_APP__', timeout=240000)
  await pg.evaluate("window.__ENTER_APP__()"); await pg.add_style_tag(content=TAP_CSS)
  await pg.wait_for_timeout(2200)
  fdir = f'{OUT}/_frames_{name}'; os.makedirs(fdir, exist_ok=True)
  for f in os.listdir(fdir): os.remove(os.path.join(fdir, f))
  stamps = []; cdp = await ctx.new_cdp_session(pg); live = {'on': True}
  async def on_frame(ev):
    if not live['on']: return
    i = len(stamps); stamps.append(ev['metadata']['timestamp'])
    open(f'{fdir}/{i:05d}.jpg', 'wb').write(base64.b64decode(ev['data']))
    try: await cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
    except Exception: pass
  cdp.on('Page.screencastFrame', lambda ev: asyncio.ensure_future(on_frame(ev)))
  await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 90, 'everyNthFrame': 1})
  await pg.wait_for_timeout(400)
  pg._t0 = asyncio.get_event_loop().time(); wall0 = time.time(); pg._taps = []
  perf0 = await pg.evaluate("performance.now()")
  ok = True
  try: await fn(pg)
  except Exception as e: ok = False; print('FAIL', name, str(e)[:300], flush=True)
  await pg.wait_for_timeout(300)
  end = now(pg)
  alog = [[round((p - perf0) / 1000, 3), ev, src.split(BASE)[-1], round(ct, 3), rate] for p, ev, src, ct, rate in await pg.evaluate("window.__alog")]
  live['on'] = False
  try: await cdp.send('Page.stopScreencast')
  except Exception: pass
  await ctx.close()
  rows = [(st - wall0, f'{fdir}/{i:05d}.jpg') for i, st in enumerate(stamps)]
  before = [r for r in rows if r[0] < 0]
  rows = ([(0.0, before[-1][1])] if before else []) + [r for r in rows if r[0] >= 0]
  lst = f'{OUT}/_frames_{name}.txt'
  with open(lst, 'w') as fh:
    for k, (st, path) in enumerate(rows):
      nxt = rows[k + 1][0] if k + 1 < len(rows) else end
      fh.write(f"file '{os.path.abspath(path)}'\nduration {max(0.001, nxt - st):.4f}\n")
    fh.write(f"file '{os.path.abspath(rows[-1][1])}'\n")
  subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,format=yuv420p',
                  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', f'{OUT}/{name}.mp4'], check=True)
  meta = {k[1:]: getattr(pg, k) for k in ('_mark', '_play', '_ex', '_play2', '_speak', '_start', '_answers') if hasattr(pg, k)}
  meta.update(ok=ok, end=end, taps=pg._taps, audio=[a for a in alog if not a[2].endswith(('tanjou.mp3',)) and '/bgm/' not in a[2] and '/sfx/' not in a[2]],
              frames=len(rows), device=DEVICE, size=[VIEW['width'] * VIEW['scale'], VIEW['height'] * VIEW['scale']])
  json.dump(meta, open(f'{OUT}/{name}.json', 'w'))
  print('rec', name, ok, round(end, 2), len(rows), 'frames', json.dumps(meta)[:500], flush=True)

async def main():
  async with async_playwright() as p:
    b = await p.chromium.launch(args=['--disable-dev-shm-usage', '--disable-gpu', '--mute-audio', '--renderer-process-limit=1',
                                      f'--force-device-scale-factor={VIEW["scale"]}', '--autoplay-policy=no-user-gesture-required'])
    for name, fn in SCENES:
      if ONLY and name not in ONLY: continue
      await record(b, name, fn)
    await b.close()

asyncio.run(main())
