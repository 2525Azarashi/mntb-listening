"""共通テスト予想問題（リスニング）の音声を OpenAI TTS で作る（実行した人の OpenAI アカウントに課金）。

  export OPENAI_API_KEY=sk-...
  python3 scripts/gacha-prints/kyotsu_mock/make_audio.py            # 5回分すべて
  python3 scripts/gacha-prints/kyotsu_mock/make_audio.py 1          # 第1回だけ
  python3 scripts/gacha-prints/kyotsu_mock/make_audio.py --dry-run  # API を呼ばずに台本と字数だけ表示

出力：public/prints/kyotsu_assets/audio/kyotsu_l{n}_q{NN}.mp3（1問ごと）と kyotsu_l{n}_full.mp3（通し）。
流れ：日本語の案内 →（第4〜6問は先読みの間）→ 英語 →（第1・2問はもう一度）→ 解答の間。
必要なもの：ffmpeg。話し手の声・なまりは assets_plan.py の割り当てどおり（制作指示書 PDF と同じ）。
"""
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
MODEL = 'gpt-4o-mini-tts'


def tts(text, voice, accent, path):
    body = json.dumps({'model': MODEL, 'voice': voice, 'input': text, 'instructions': A.ACCENT[accent],
                       'response_format': 'mp3'}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/audio/speech', data=body, headers={
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        path.write_bytes(r.read())


def silence(sec, path):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono',
                    '-t', str(sec), '-q:a', '4', str(path)], check=True)


def concat(files, out):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        for p in files:
            f.write(f"file '{p}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f.name,
                    '-ar', '24000', '-ac', '1', '-q:a', '4', str(out)], check=True)


def plan(t):
    """1トラックの部品 [(kind, text|秒, voice, accent)]"""
    seq = [('say', t['intro_ja'], A.JA_NARRATOR['voice'], 'ja')]
    pre = A.PAUSE_PREVIEW.get(t['part'])
    if pre and t['intro_ja'].startswith('第'):
        seq.append(('gap', pre))
    for k in range(t['times']):
        for ln in t['lines']:
            seq += [('say', ln['text'], ln['voice'], ln['accent']), ('gap', A.PAUSE_LINE)]
        if k + 1 < t['times']:
            seq += [('say', 'もう一度読みます。', A.JA_NARRATOR['voice'], 'ja'), ('gap', A.PAUSE_REPEAT)]
    seq.append(('gap', A.PAUSE_ANSWER[t['part']]))
    return seq


def main(args):
    dry = '--dry-run' in args
    nums = [int(a) for a in args if a.isdigit()] or A.SETS
    if not dry and not os.environ.get('OPENAI_API_KEY'):
        sys.exit('OPENAI_API_KEY を設定してください（課金は設定したアカウントにかかります）')
    OUT.mkdir(parents=True, exist_ok=True)
    total_chars = 0
    for n in nums:
        tr = A.tracks(n)
        done = []
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            cache = {}
            for t in tr:
                parts = []
                for i, step in enumerate(plan(t)):
                    if step[0] == 'gap':
                        key = ('gap', step[1])
                        if key not in cache:
                            cache[key] = d / f'gap_{step[1]}.mp3'
                            if not dry:
                                silence(step[1], cache[key])
                        parts.append(cache[key]); continue
                    _, text, voice, acc = step
                    key = (text, voice, acc)
                    if key not in cache:
                        total_chars += len(text)
                        cache[key] = d / f'say_{len(cache)}.mp3'
                        if dry:
                            print(f'  [{voice}/{acc}] {text[:90]}')
                        else:
                            tts(text, voice, acc, cache[key])
                    parts.append(cache[key])
                if not dry:
                    concat(parts, OUT / t['file'])
                done.append(OUT / t['file'])
                print(('（台本）' if dry else '作成 ') + t['file'])
            if not dry:
                head = d / 'head.mp3'
                tts(f'大学入学共通テスト予想問題、第{n}回、英語リスニング。これから音声が流れます。', A.JA_NARRATOR['voice'], 'ja', head)
                tail = d / 'tail.mp3'
                tts('これでリスニングの問題は終わりです。', A.JA_NARRATOR['voice'], 'ja', tail)
                concat([head, cache.get(('gap', 4)) or head] + done + [tail], OUT / f'kyotsu_l{n}_full.mp3')
                print(f'作成 kyotsu_l{n}_full.mp3')
    print(f'読み上げる文字数（重複を除く）：約{total_chars:,}字')


if __name__ == '__main__':
    main(sys.argv[1:])
