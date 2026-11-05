"""F8（2026-11-04）共通テスト予想リスニングの通し音声と再生ページを作る。
  1) 日本語の案内（audio_sources/commercial/elevenlabs_2026-11-03_kyotsu_l2-5/ の Chihiro）を英語を差し込む所で区切る
  2) 問題ごとの mp3（public/prints/kyotsu_assets/audio/）とつないで public/prints/kyotsu_assets/full/kyotsu_l{n}_full.mp3
  3) QR の行き先の再生ページ public/prints/kyotsu_assets/full/l{n}.html
  使い方：python3 scripts/gacha-prints/kyotsu_mock/make_full_audio.py（リポジトリの直下で）"""
import json, subprocess, re, os
NARR = {"src": "audio_sources/commercial/elevenlabs_2026-11-03_kyotsu_l2-5/ElevenLabs_2026-11-04T05_54_23_Chihiro - Calm Mid-Low Female_pvc_sp100_s50_sb75_v4.mp3", "dur": 345.155875, "cuts": [[56.24, "go:1A"], [81.02, "go:1B"], [112.93, "go:2"], [148.05, "go:3"], [182.44, "read"], [184.38, "go:4A1"], [192.55, "read"], [194.53, "go:4A2"], [217.93, "read"], [219.89, "go:4B"], [257.04, "read"], [258.98, "go:5L"], [262.42, "go:5Q32"], [265.95, "go:5Q33"], [301.49, "read"], [303.44, "go:6A"], [327.77, "read"], [329.73, "go:6B"]]}
import json, subprocess, re, os
N=NARR; SRC=N['src']; C=dict((k,t) for t,k in N['cuts']); END=N['dur']
A='public/prints/kyotsu_assets/audio'; OUT='public/prints/kyotsu_assets/full'; os.makedirs(OUT,exist_ok=True)
def vol(f, a=None, b=None):
    cmd=['ffmpeg','-i',f]+(['-af',f'atrim={a}:{b},volumedetect'] if a is not None else ['-af','volumedetect'])+['-f','null','-']
    r=subprocess.run(cmd,capture_output=True,text=True).stderr
    return float(re.search(r'mean_volume: (-?[\d.]+)',r).group(1))
def build(n):
    parts=[]  # ('n',a,b) narration / ('t',q) track / ('s',sec) silence
    T=lambda *qs:[('t',q) for q in qs]
    S=lambda s:('s',s)
    def tracks(qs, gap):
        out=[]
        for i,q in enumerate(qs): out += [('t',q), S(gap)]
        return out
    parts += [('n',0,C['go:1A']), S(1)] + tracks(['01','02','03','04'],5)
    parts += [('n',C['go:1A'],C['go:1B']), S(1)] + tracks(['05','06','07'],5)
    parts += [('n',C['go:1B'],C['go:2']), S(1)] + tracks(['08','09','10','11'],6)
    parts += [('n',C['go:2'],C['go:3']), S(1)] + tracks(['12','13','14','15','16','17'],6)
    r=[t for t,k in N['cuts'] if k=='read']
    parts += [('n',C['go:3'],r[0]), S(10), ('n',r[0],C['go:4A1']), S(1)] + tracks(['18-21'],6)
    parts += [('n',C['go:4A1'],r[1]), S(10), ('n',r[1],C['go:4A2']), S(1)] + tracks(['22-25'],6)
    parts += [('n',C['go:4A2'],r[2]), S(15), ('n',r[2],C['go:4B']), S(1)] + tracks(['26'],8)
    parts += [('n',C['go:4B'],r[3]), S(30), ('n',r[3],C['go:5L']), S(1)] + tracks(['27-32'],6)
    parts += [('n',C['go:5L'],C['go:5Q32']), S(8), ('n',C['go:5Q32'],C['go:5Q33']), S(1)] + tracks(['33'],8)
    parts += [('n',C['go:5Q33'],r[4]), S(15), ('n',r[4],C['go:6A']), S(1)] + tracks(['34-35'],8)
    parts += [('n',C['go:6A'],r[5]), S(15), ('n',r[5],C['go:6B']), S(1)] + tracks(['36-37'],8)
    parts += [('n',C['go:6B'],END)]
    # 音量をそろえる：英語の平均に日本語を合わせる
    en=sum(vol(f'{A}/kyotsu_l{n}_q{q}.mp3') for q in ['01','12','27-32'])/3
    ja=vol(SRC,0,60); gain=round(en-ja,1)
    inputs=[]; fc=[]; idx={}
    def inp(path):
        if path not in idx: idx[path]=len(idx); inputs.extend(['-i',path])
        return idx[path]
    labels=[]
    for i,p in enumerate(parts):
        L=f'p{i}'
        if p[0]=='n':
            fc.append(f"[{inp(SRC)}:a]atrim={p[1]}:{p[2]},asetpts=PTS-STARTPTS,volume={gain}dB,aformat=sample_rates=44100:channel_layouts=mono[{L}]")
        elif p[0]=='t':
            fc.append(f"[{inp(f'{A}/kyotsu_l{n}_q{p[1]}.mp3')}:a]asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[{L}]")
        else:
            fc.append(f"anullsrc=r=44100:cl=mono,atrim=0:{p[1]}[{L}]")
        labels.append(f'[{L}]')
    fc.append(''.join(labels)+f'concat=n={len(labels)}:v=0:a=1[o]')
    out=f'{OUT}/kyotsu_l{n}_full.mp3'
    subprocess.run(['ffmpeg','-y','-loglevel','error',*inputs,'-filter_complex',';'.join(fc),'-map','[o]','-c:a','libmp3lame','-b:a','40k','-ac','1','-ar','44100',out],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    print(n, f'{d/60:.1f}min', f'{os.path.getsize(out)/1e6:.1f}MB', 'gain', gain)
    return round(d)
res={n:build(n) for n in [1,2,3,4,5]}
FULL_SEC=res

# ---- 再生ページ ----
import json, re
src = open('src/data/kyotsuMockAudio.ts').read()
full = {str(k): v for k, v in FULL_SEC.items()}
CSS = """body{margin:0;font-family:system-ui,-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;background:#fdfbf7;color:#2c3e50}
main{max-width:560px;margin:0 auto;padding:20px 16px 40px}h1{font-size:20px;margin:0 0 4px}p{font-size:14px;line-height:1.7;margin:6px 0}
.full{background:#fff;border:2px solid #f1d58a;border-radius:16px;padding:14px;margin:16px 0}.full h2{font-size:16px;margin:0 0 8px}
audio{width:100%;min-height:44px}h3{font-size:15px;margin:20px 0 6px;border-bottom:1px solid #e2d6c1;padding-bottom:4px}
.q{display:grid;gap:4px;margin:10px 0}.q span{font-size:14px;font-weight:700}small{color:#6e6455;font-size:12px}footer{margin-top:28px;font-size:12px;color:#6e6455}"""
for n in range(1, 6):
    block = re.search(rf"print_lr_kyotsu_l_{n}: (.*?)(?=\n  print_lr_kyotsu_l_|\n}};)", src, re.S).group(1)
    tracks = re.findall(r"t\('([^']+)', '([^']+)', (\d+)\)", block)
    rows, cur = [], None
    for part, q, sec in tracks:
        if part != cur:
            rows.append(f'<h3>{part}</h3>'); cur = part
        a, b = (q.split('-') + [None])[:2]
        label = f'問{int(a)}〜{int(b)}' if b else f'問{int(a)}'
        rows.append(f'<div class="q"><span>{label} <small>{sec}秒{"・2回流れます" if int(a) <= 11 else ""}</small></span>'
                    f'<audio controls preload="none" src="../audio/kyotsu_l{n}_q{q}.mp3"></audio></div>')
    m, s = divmod(full[str(n)], 60)
    html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>共通テスト 英語リスニング 予想問題 第{n}回 音声｜マナトビ</title><style>{CSS}</style></head>
<body><main><h1>共通テスト 英語リスニング 予想問題 第{n}回</h1><p>マナトビ オリジナル予想問題の音声です（大学入試センターの過去問ではありません）。</p>
<section class="full"><h2>通しで聞く（本番と同じ流れ・約{m}分）</h2><p>日本語の案内 → 問題の音声の順に、本番と同じく続けて流れます。第1・2問は2回、第3〜6問は1回です。問題冊子を開いてから再生してください。</p>
<audio controls preload="none" src="kyotsu_l{n}_full.mp3"></audio></section>
<p>1問ずつ聞き直すときは、下から選んでください。</p>
{''.join(rows)}
<footer>音声：ElevenLabs で作成。アプリ「マナトビ」のマイPDFからも聞けます。</footer></main></body></html>"""
    open(f'public/prints/kyotsu_assets/full/l{n}.html', 'w').write(html)
print('ok')
