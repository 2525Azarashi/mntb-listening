import { it, expect } from 'vitest';
import { emptyProgress, claimMission, localDateKey } from '../src/battle/core/growth';

// 2026-10-11：対戦後のトースト「報酬を受け取る」はその場で受け取る。
//   ミッション画面と両方で押しても、二重には払わない（トーストはこの関数に任せている）。
it('達成したミッションは1回だけ受け取れる（2回目は報酬なし）', () => {
  const today = localDateKey();
  const p0 = emptyProgress('u');
  const p = { ...p0, daily: { date: today, progress: { m_win1: 1 }, claimed: [] as string[] } };
  const first = claimMission(p, 'm_win1', today);
  expect(first.reward).toEqual({ xp: 50, coins: 25 });
  expect(first.next.coins).toBe(p.coins + 25);
  const second = claimMission(first.next, 'm_win1', today);
  expect(second.reward).toBeNull();
  expect(second.next.coins).toBe(first.next.coins);
});
