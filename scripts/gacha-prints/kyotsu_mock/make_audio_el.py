"""共通テスト予想問題（リスニング）の音声を ElevenLabs（Eleven v4・Text to Dialogue API）で作る。
課金は ELEVENLABS_API_KEY の持ち主の ElevenLabs アカウント（有料プラン）にかかる。

  export ELEVENLABS_API_KEY=...
  cp scripts/gacha-prints/kyotsu_mock/el_voices.example.json scripts/gacha-prints/kyotsu_mock/el_voices.json
  #   ↑ を開いて、Voice Library で選んだ声の voice_id を役ごとに書く（制作指示書「音声」の章の表と同じ役名）
  python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py --dry-run   # API を呼ばずに台本・役・文字数だけ表示
  python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py 1           # 第1回だけ
  python3 scripts/gacha-prints/kyotsu_mock/make_audio_el.py             # 5回分すべて

出力：public/prints/kyotsu_assets/audio/kyotsu_l{n}_q{NN}.mp3（1問ごと）と kyotsu_l{n}_full.mp3（通し）。
流れ：日本語の案内 →（第4〜6問は先読みの間）→ 英語（対話は1回の生成で） →（第1・2問は同じ音声をもう一度）→ 解答の間。
v4 は SSML の <break> が使えないので、長い無音は ffmpeg で足す。必要なもの：ffmpeg。
生成済みの部品は .tmpwork/el_cache/ に保存し、やり直しても同じ台本は再生成しない（課金を抑える）。
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assets_plan as A  # noqa: E402

ROOT = HERE.parent.parent.parent
OUT = ROOT / A.ASSET_DIR / 'audio'
CACHE = ROOT / '.tmpwork' / 'el_cache'
VOICES = HERE / 'el_voices.json'
API = 'https://api.elevenlabs.io/v1/text-to-dialogue?output_format=mp3_44100_128'


def load_voices(dry):
    ids = {k: v['voice_id'] for k, v in A.EL_CAST.items()}
    if VOICES.exists():
        ids.update({k: v for k, v in json.loads(VOICES.read_text()).items() if v})
    missing = [k for k, v in ids.items() if not v]
    if missing and not dry:
        sys.exit(f'el_voices.json に voice_id がない役：{", ".join(missing)}（el_voices.example.json を参照）')
    return ids


def dialogue(inputs, path, lang):
    """inputs = [(voice_id, text)] を1回の生成で音声にする"""
    body = json.dumps({'model_id': A.EL_MODEL, 'language_code': lang, 'settings': A.EL_SETTINGS,
                       'inputs': [{'voice_id': v, 'text': t} for v, t in inputs]}).encode()
    req = urllib.request.Request(API, data=body, headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'],
                                                           'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        path.write_bytes(r.read())


def cached(inputs, lang, dry, stats):
    key = hashlib.sha1(json.dumps([inputs, lang, A.EL_MODEL, A.EL_SETTINGS]).encode()).hexdigest()[:16]
    p = CACHE / f'{key}.mp3'
    if not p.exists() and key not in stats['seen']:
        stats['seen'].add(key)
        stats['chars'] += sum(len(t) for _, t in inputs)
        stats['calls'] += 1
        if not dry:
            dialogue(inputs, p, lang)
    return p


def silence(sec, d):
    p = d / f'gap_{sec}.mp3'
    if not p.exists():
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                        '-t', str(sec), '-b:a', '128k', str(p)], check=True)
    return p


def concat(files, out):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        for p in files:
            f.write(f"file '{p}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f.name,
                    '-ar', '44100', '-ac', '1', '-b:a', '128k', str(out)], check=True)


def main(args):
    dry = '--dry-run' in args
    nums = [int(a) for a in args if a.isdigit()] or A.SETS
    if not dry and not os.environ.get('ELEVENLABS_API_KEY'):
        sys.exit('ELEVENLABS_API_KEY を設定してください（課金は設定したアカウントにかかります）')
    ids = load_voices(dry)
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    stats = {'chars': 0, 'calls': 0, 'seen': set()}
    ja = lambda text: cached([(ids['JA'], text)], 'ja', dry, stats)  # noqa: E731
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for n in nums:
            done = []
            for t in A.tracks(n):
                lines = A.el_track(t)
                if dry:
                    print(f'■ {t["file"]}  {t["times"]}回読み')
                    for role, sp, text in lines:
                        print(f'   {role:6} {sp:14} {text[:100]}')
                eng = cached([(ids[role], text) for role, _, text in lines], 'en', dry, stats)
                seq = [ja(t['intro_ja'])]
                pre = A.PAUSE_PREVIEW.get(t['part'])
                if pre and t['intro_ja'].startswith('第'):
                    seq.append(silence(pre, d) if not dry else None)
                for k in range(t['times']):
                    seq.append(eng)
                    if k + 1 < t['times']:
                        seq += [silence(A.PAUSE_REPEAT, d) if not dry else None, ja('もう一度読みます。'),
                                silence(1, d) if not dry else None]
                seq.append(silence(A.PAUSE_ANSWER[t['part']], d) if not dry else None)
                if not dry:
                    concat(seq, OUT / t['file'])
                    print('作成', t['file'])
                done.append(OUT / t['file'])
            head = ja(f'大学入学共通テスト予想問題、第{n}回、英語リスニング。これから音声が流れます。')
            tail = ja('これでリスニングの問題は終わりです。')
            if not dry:
                concat([head, silence(4, d)] + done + [tail], OUT / f'kyotsu_l{n}_full.mp3')
                print(f'作成 kyotsu_l{n}_full.mp3')
    print(f'生成回数 {stats["calls"]} 回・文字数 約{stats["chars"]:,} 字（キャッシュ済みを除く）')


if __name__ == '__main__':
    main(sys.argv[1:])
