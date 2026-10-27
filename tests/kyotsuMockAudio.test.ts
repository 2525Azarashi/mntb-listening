import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { KYOTSU_MOCK_AUDIO, kyotsuAudioLabel } from '../src/data/kyotsuMockAudio';
import { KYOTSU_MOCK_PRINTS } from '../src/data/kyotsuMockPrints';

const ffprobe = (() => { try { execFileSync('ffprobe', ['-version'], { stdio: 'ignore' }); return true; } catch { return false; } })();

describe('共通テスト予想問題 リスニング音声（第1回）', () => {
  const tracks = KYOTSU_MOCK_AUDIO.print_lr_kyotsu_l_1;
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
    for (const t of tracks) expect(existsSync(`public${t.file}`), t.file).toBe(true);
    expect(readdirSync('public/prints/kyotsu_assets/audio').filter((f) => f.endsWith('.mp3')).length).toBe(tracks.length);
  });
  it.skipIf(!ffprobe)('書いてある秒数が実物の長さと合う（±1秒）', () => {
    for (const t of tracks) {
      const sec = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', `public${t.file}`]).toString());
      expect(Math.abs(sec - t.sec), t.q).toBeLessThanOrEqual(1);
    }
  });
  it('元の6ファイルを audio_sources に残している', () => {
    expect(readdirSync('audio_sources/commercial/elevenlabs_2026-10-26_kyotsu_l1').filter((f) => f.endsWith('.mp3')).length).toBe(6);
  });
  it('374本の台帳には入れていない', () => {
    expect(readFileSync('scripts/data/listening_audio_ledger.json', 'utf8')).not.toContain('kyotsu_l1');
  });
  it('問番号の表示', () => {
    expect(kyotsuAudioLabel('01')).toBe('問1');
    expect(kyotsuAudioLabel('18-21')).toBe('問18〜21');
  });
  it('マイPDFにプレーヤーがつながっている', () => {
    expect(readFileSync('src/components/MyCollection.tsx', 'utf8')).toContain('<KyotsuAudioPlayer printId={item.id}/>');
  });
});
