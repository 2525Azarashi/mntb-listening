import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { KYOTSU_MOCK_AUDIO, kyotsuAudioLabel } from '../src/data/kyotsuMockAudio';
import { KYOTSU_MOCK_PRINTS } from '../src/data/kyotsuMockPrints';

const ffprobe = (() => { try { execFileSync('ffprobe', ['-version'], { stdio: 'ignore' }); return true; } catch { return false; } })();

describe('共通テスト予想問題 リスニング音声（第1〜5回）', () => {
  const tracks = KYOTSU_MOCK_AUDIO.print_lr_kyotsu_l_1;
  const all = Object.values(KYOTSU_MOCK_AUDIO).flat();
  it('F2（2026-11-04）：第1〜5回すべてに音声がある（リスニングの回はすべて）', () => {
    const ids = KYOTSU_MOCK_PRINTS.filter((p) => p.subject === 'english_listening').map((p) => p.id).sort();
    expect(Object.keys(KYOTSU_MOCK_AUDIO).sort()).toEqual(ids);
    for (const id of ids) {
      const ts = KYOTSU_MOCK_AUDIO[id];
      expect(ts.map((t) => t.q), id).toEqual(tracks.map((t) => t.q));
      expect(ts.map((t) => t.part), id).toEqual(tracks.map((t) => t.part));
      for (const t of ts) expect(t.file, id).toContain(`kyotsu_l${id.split('_').pop()}_q`);
    }
  });
  it('音声のある回は LR のリスニングだけ', () => {
    const ids = new Set(KYOTSU_MOCK_PRINTS.filter((p) => p.subject === 'english_listening').map((p) => p.id));
    for (const id of Object.keys(KYOTSU_MOCK_AUDIO)) expect(ids.has(id)).toBe(true);
  });
  it('問1〜問37 を漏れなく・重なりなく覆う（24トラック）', () => {
    expect(tracks).toHaveLength(24);
    const qs = tracks.flatMap((t) => { const [a, b = a] = t.q.split('-').map(Number); return Array.from({ length: b - a + 1 }, (_, i) => a + i); });
    expect(qs).toEqual(Array.from({ length: 37 }, (_, i) => i + 1));
  });
  it('第1問・第2問（問1〜11）だけ2回読み', () => {
    for (const t of tracks) expect(t.twice).toBe(Number(t.q.split('-')[0]) <= 11);
  });
  it('mp3 の実物があり、フォルダに余分なファイルがない', () => {
    for (const t of all) expect(existsSync(`public${t.file}`), t.file).toBe(true);
    expect(readdirSync('public/prints/kyotsu_assets/audio').filter((f) => f.endsWith('.mp3')).length).toBe(all.length);
  });
  it.skipIf(!ffprobe)('書いてある秒数が実物の長さと合う（±1秒）', () => {
    for (const t of all) {
      const sec = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `public${t.file}`]).toString());
      expect(Math.abs(sec - t.sec), t.q).toBeLessThanOrEqual(1);
    }
  }, 120_000); // 120本を ffprobe するので、全テストを並べて走らせると20秒を超えることがある
  it('元のファイルを audio_sources に残している（第1回6本・第2〜5回16本＋案内1本）', () => {
    expect(readdirSync('audio_sources/commercial/elevenlabs_2026-10-26_kyotsu_l1').filter((f) => f.endsWith('.mp3')).length).toBe(6);
    expect(readdirSync('audio_sources/commercial/elevenlabs_2026-11-03_kyotsu_l2-5').filter((f) => f.endsWith('.mp3')).length).toBe(17); // 英語16本＋日本語の案内1本（F8）
  });
  it('374本の台帳には入れていない', () => {
    const ledger = readFileSync('scripts/data/listening_audio_ledger.json', 'utf8');
    for (const n of [1, 2, 3, 4, 5]) expect(ledger).not.toContain(`kyotsu_l${n}`);
  });
  it('問番号の表示', () => {
    expect(kyotsuAudioLabel('01')).toBe('問1');
    expect(kyotsuAudioLabel('18-21')).toBe('問18〜21');
  });
  it('マイPDFにプレーヤーがつながっている', () => {
    expect(readFileSync('src/components/MyCollection.tsx', 'utf8')).toContain('<KyotsuAudioPlayer printId={item.id}/>');
  });
});

describe('F8（2026-11-04）通し音声と QR', () => {
  it('回ごとに通し音声と再生ページがあり、プレーヤーから通しで聞ける', async () => {
    const { kyotsuFullAudioOf } = await import('../src/data/kyotsuMockAudio');
    for (const n of [1, 2, 3, 4, 5]) {
      const full = kyotsuFullAudioOf(`print_lr_kyotsu_l_${n}`);
      expect(full).toBe(`/prints/kyotsu_assets/full/kyotsu_l${n}_full.mp3`);
      expect(existsSync(`public${full}`)).toBe(true);
      const html = readFileSync(`public/prints/kyotsu_assets/full/l${n}.html`, 'utf8');
      expect(html).toContain(`kyotsu_l${n}_full.mp3`);
      expect(html).toContain(`../audio/kyotsu_l${n}_q36-37.mp3`);
      expect(html).not.toContain('<script');
    }
    expect(kyotsuFullAudioOf('print_lr_kyotsu_r_1')).toBeNull();
    expect(readFileSync('src/components/gacha/KyotsuAudioPlayer.tsx', 'utf8')).toContain('通しで聞く');
  });
  it.skipIf(!ffprobe)('通し音声は本番と同じくらいの長さ（15〜22分）', () => {
    for (const n of [1, 2, 3, 4, 5]) {
      const sec = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `public/prints/kyotsu_assets/full/kyotsu_l${n}_full.mp3`]).toString());
      expect(sec).toBeGreaterThan(15 * 60);
      expect(sec).toBeLessThan(22 * 60);
    }
  });
  it('PDF の表紙に QR の案内がある（音声なしの注意書きは消した）', () => {
    const src = readFileSync('scripts/gacha-prints/kyotsu_mock/build.py', 'utf8');
    expect(src).toContain('qr=(f\'{AUDIO_BASE}/l{n}.html\'');
    expect(src).not.toContain('音声は付いていません');
  });
});
