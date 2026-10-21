// リスニングの和訳を作る（2026-10-21）。node scripts/listening-translation/make.mjs <tracks.json> <out.json>
//   tracks.json は .tmpwork/dump_tracks.ts の出力。既にある訳は使い回す（何度でも続きから）
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const [,, inFile, outFile] = process.argv;
const cfg = fs.readFileSync(path.join(os.homedir(), '.genspark_llm.yaml'), 'utf8');
const key = process.env.OPENAI_API_KEY || /api_key:\s*(\S+)/.exec(cfg)?.[1];
const base = process.env.OPENAI_BASE_URL || /base_url:\s*(\S+)/.exec(cfg)?.[1];
const tracks = JSON.parse(fs.readFileSync(inFile, 'utf8'));
const out = fs.existsSync(outFile) ? JSON.parse(fs.readFileSync(outFile, 'utf8')) : {};
const SYS = `あなたは大学入試英語の講師です。共通テスト英語リスニングのスクリプトを、高校生が復習で読む「自然で正確な日本語訳」にします。
- 入力は JSON 配列（英文のまとまり）。同じ数・同じ順の日本語の JSON 配列だけを返す（説明文なし）
- 直訳すぎず意訳しすぎない。数字・時刻・曜日・固有名詞は正確に。話し言葉は自然な会話調
- 話者名や記号は付けない`;
async function tr(segs) {
  for (let a = 0; a < 4; a++) {
    try {
      const r = await fetch(base.replace(/\/$/, '') + '/chat/completions', { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${key}` },
        body: JSON.stringify({ model: 'gpt-5-mini', messages: [{ role: 'system', content: SYS }, { role: 'user', content: JSON.stringify(segs) }] }) });
      const j = await r.json();
      const txt = j.choices?.[0]?.message?.content ?? '';
      const arr = JSON.parse(txt.slice(txt.indexOf('['), txt.lastIndexOf(']') + 1));
      if (Array.isArray(arr) && arr.length === segs.length && arr.every(x => typeof x === 'string' && x.trim())) return arr.map(x => x.trim());
    } catch (e) { /* retry */ }
  }
  return null;
}
const todo = tracks.filter(t => !out[t.key] || out[t.key].length !== t.segs.length);
console.log('todo', todo.length, '/', tracks.length);
let done = 0;
const worker = async () => { for (;;) { const t = todo.shift(); if (!t) return; const r = await tr(t.segs.map(s => s.text)); if (r) out[t.key] = r; else console.log('FAIL', t.key); done++; if (done % 10 === 0) { fs.writeFileSync(outFile, JSON.stringify(out)); console.log('done', done); } } };
await Promise.all(Array.from({ length: 6 }, worker));
fs.writeFileSync(outFile, JSON.stringify(out));
console.log('finished', Object.keys(out).length);
