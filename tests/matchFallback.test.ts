import { describe, expect, it } from 'vitest';
import {
  GHOST_AFTER_SEC,
  QUEUE_STALE_MS,
  QUOTA_COOLDOWN_MS,
  fallbackDecision,
  isStaleQueueTicket,
  quotaBlockedUntil,
} from '../src/battle/core/matchFallback';
import { ghostProfileFor, decideAiMove, GHOST_RATING_SPREAD } from '../src/battle/core/aiOpponent';

const base = { elapsedSec: 0, failures: 0, lastErrorCode: null, online: true, quotaBlocked: false };

describe('全国対戦：相手がいない／サーバーが使えないときは AI プレイヤー', () => {
  it('人を待つのは GHOST_AFTER_SEC 秒まで', () => {
    expect(fallbackDecision({ ...base, elapsedSec: GHOST_AFTER_SEC - 1 })).toBeNull();
    expect(fallbackDecision({ ...base, elapsedSec: GHOST_AFTER_SEC })).toBe('empty');
  });
  it('無料枠の上限・失敗の連続・圏外は待たずに切り替える', () => {
    expect(fallbackDecision({ ...base, lastErrorCode: 'resource-exhausted' })).toBe('server');
    expect(fallbackDecision({ ...base, quotaBlocked: true })).toBe('server');
    expect(fallbackDecision({ ...base, failures: 3 })).toBe('server');
    expect(fallbackDecision({ ...base, failures: 2 })).toBeNull();
    expect(fallbackDecision({ ...base, online: false })).toBe('offline');
  });
  it('全国対戦で組まれた相手の名前・紹介文に「AI」と出さない', () => {
    for (let i = 0; i < 40; i++) {
      const p = ghostProfileFor(1500, `seed-${i}`);
      expect(p.name).not.toMatch(/AI/);
      expect(p.tagline).not.toMatch(/AI/);
    }
  });
  it('マッチング画面・試合画面のソースに AI だと分かる表示が残っていない', async () => {
    const { readFileSync } = await import('node:fs');
    const matching = readFileSync('src/battle/ui/BattleMatching.tsx', 'utf8');
    expect(matching).not.toContain('AIプレイヤーが相手です');
    expect(matching).not.toMatch(/label: 'AIプレイヤー/);
    expect(matching).not.toMatch(/detail: `[^`]*AIプレイヤー/);
    const room = readFileSync('src/battle/ui/BattleAiRoomScreen.tsx', 'utf8');
    expect(room).not.toContain('（AI）');
    expect(room).not.toContain('data-ghost-badge');
    expect(room).toContain('2人がそろいました。まもなくスタート');
  });
  it('古い待機票は相手にしない（作成時刻が未確定の票は新しい扱い）', () => {
    const now = 1_000_000_000;
    expect(isStaleQueueTicket(now - QUEUE_STALE_MS - 1, now)).toBe(true);
    expect(isStaleQueueTicket(now - 5_000, now)).toBe(false);
    expect(isStaleQueueTicket(null, now)).toBe(false);
  });
  it('無料枠の上限は15分だけ覚える（おかしな値は捨てる）', () => {
    const now = 5_000_000;
    expect(quotaBlockedUntil(String(now + 60_000), now)).toBe(now + 60_000);
    expect(quotaBlockedUntil(String(now - 1), now)).toBeNull();
    expect(quotaBlockedUntil(String(now + QUOTA_COOLDOWN_MS * 3), now)).toBeNull();
    expect(quotaBlockedUntil(null, now)).toBeNull();
  });
});

describe('AI プレイヤーの強さ・名前', () => {
  it('同じ種なら同じ相手（試合中に名前や強さが変わらない）', () => {
    expect(ghostProfileFor(1500, 'x')).toEqual(ghostProfileFor(1500, 'x'));
  });
  // B7（2026-10-29）：弱い人〜強い人まで出るよう ±90 → ±320 に広げた（近い相手ほど出やすい三角分布）
  it('レートは自分の ±320 以内・近い相手が多い・名前は毎回いろいろ', () => {
    const names = new Set<string>();
    const diffs: number[] = [];
    for (let i = 0; i < 400; i += 1) {
      const p = ghostProfileFor(1600, `s${i}`);
      const d = Math.abs(p.displayRating - 1600);
      expect(d).toBeLessThanOrEqual(GHOST_RATING_SPREAD);
      expect(p.speedRange[0]).toBeLessThanOrEqual(p.speedRange[1]);
      expect(p.human).toBeTruthy();
      diffs.push(d);
      names.add(p.name);
    }
    expect(names.size).toBeGreaterThan(30);
    expect(diffs.filter(d => d > 200).length).toBeGreaterThan(5);          // たまに格上・格下
    expect(diffs.filter(d => d <= 120).length).toBeGreaterThan(diffs.length / 3); // 近い相手が多い
  });
  it('レートが高い相手ほど正解率が高い（0.30〜0.97）', () => {
    const avg = (r: number) => Array.from({ length: 100 }, (_, i) => ghostProfileFor(r, `a${i}`).accuracy).reduce((a, b) => a + b) / 100;
    expect(avg(1100)).toBeLessThan(avg(1500));
    expect(avg(1500)).toBeLessThan(avg(2000));
    expect(avg(900)).toBeGreaterThanOrEqual(0.3);
    expect(avg(2600)).toBeLessThanOrEqual(0.97);
  });
  it('人間らしい間：同じ相手でも問題ごとに答える時間がばらつく', () => {
    const p = ghostProfileFor(1500, 'human');
    const q = { id: 'q1', format: 'choice', prompt: 'apple の意味は？', options: ['りんご', 'みかん', 'ぶどう', 'もも'], answerIndex: 0, panelOrder: [] } as never;
    const ms = Array.from({ length: 30 }, (_, i) => decideAiMove(p, q, 20, 'seed', i).delayMs);
    expect(Math.max(...ms) - Math.min(...ms)).toBeGreaterThan(3000);
  });
  it('AI プレイヤーの解答は制限時間内', () => {
    const p = ghostProfileFor(1500, 'q');
    const q = { id: 'q1', format: 'choice', prompt: 'apple の意味は？', options: ['りんご', 'みかん', 'ぶどう', 'もも'], answerIndex: 0, panelOrder: [] } as never;
    for (let i = 0; i < 20; i += 1) {
      const m = decideAiMove(p, q, 10, 'seed', i);
      expect(m.delayMs).toBeLessThanOrEqual(10_000 * 0.92 + 1);
      expect(m.delayMs).toBeGreaterThan(0);
    }
  });
});
