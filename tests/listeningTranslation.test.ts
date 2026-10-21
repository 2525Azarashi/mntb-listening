/**
 * リスニングのスクリプトの和訳（2026-10-21）
 *   ご要望：「リスニングの解説で英語スクリプトの日本語訳も書いてくれるとありがたい。
 *   短いスクリプトの大問はスクリプトの下に添える形、長い大問は英文→和訳→英文→和訳」
 * - すべての音源に和訳があり、英文のまとまりの数とそろっている
 * - 長い大問は交互表示、短い大問は下にまとめる
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import * as Q1A from '../src/data/englishListeningQ1AProblems';
import * as Q1AS from '../src/data/englishListeningQ1ASets';
import * as Q1B from '../src/data/englishListeningQ1BProblems';
import * as Q2 from '../src/data/englishListeningQ2Problems';
import * as Q3 from '../src/data/englishListeningQ3Problems';
import * as Q46 from '../src/data/englishListeningQ4to6Problems';
import { isLongTrack, segmentBreaks, segmentsOf, trackKey, type SegTrack } from '../src/features/listeningTranslation/segments';

const tracks = new Map<string, SegTrack>();
const walk = (o: unknown, depth = 0): void => {
  if (!o || typeof o !== 'object' || depth > 8) return;
  if (Array.isArray(o)) { o.forEach(x => walk(x, depth + 1)); return; }
  const r = o as Record<string, unknown>;
  if (typeof r.script === 'string' && typeof r.subId === 'string' && 'translation' in r) { tracks.set(trackKey(r as unknown as SegTrack), r as unknown as SegTrack); return; }
  Object.values(r).forEach(v => walk(v, depth + 1));
};
[Q1A, Q1AS, Q1B, Q2, Q3, Q46].forEach(m => Object.values(m).forEach(v => { if (typeof v !== 'function') walk(v); }));
const data = JSON.parse(readFileSync('public/data/listeningTranslations.json', 'utf8')) as Record<string, string[]>;

describe('リスニングの和訳', () => {
  it('すべての音源に和訳があり、英文のまとまりと数がそろう', () => {
    expect(tracks.size).toBeGreaterThan(300);
    const missing = [...tracks.entries()].filter(([k, t]) => data[k]?.length !== segmentsOf(t).length).map(([k]) => k);
    expect(missing).toEqual([]);
    for (const k of tracks.keys()) for (const line of data[k]) { expect(line.trim().length).toBeGreaterThan(0); expect(line).toMatch(/[ぁ-んァ-ヶ一-龠]/); }
  });
  it('第1問のような短いものは下にまとめ、第4・6問や講義のような長いものは交互に出す', () => {
    const all = [...tracks.values()];
    expect(all.filter(t => /listening_q[46]\//.test(t.audioUrl ?? '')).every(isLongTrack)).toBe(true);
    expect(all.filter(t => t.script.split(/\s+/).length > 150).every(isLongTrack)).toBe(true); // 第5問の講義など
    expect(all.filter(t => t.script.split(/\s+/).length < 30).some(isLongTrack)).toBe(false);
  });
  it('独り語りでも、まとまりの最後の語で区切れる', () => {
    const t: SegTrack = { subId: 'x', script: 'One two three. Four five six.', };
    const words = 'One two three. Four five six.'.split(' ').map((text, i) => ({ i, text, line: 0 }));
    // 35語までは1まとまり → 区切りは最後の語だけ
    expect([...segmentBreaks(t, words, 1).entries()]).toEqual([[5, 0]]);
  });
  it('解説のスクリプト表示が和訳を使う', () => {
    const src = readFileSync('src/components/ListeningEvidenceScript.tsx', 'utf8');
    expect(src).toContain('loadListeningTranslations');
    expect(src).toContain('isLongTrack');
    expect(src).toContain('listening-tr-line');
  });
});
