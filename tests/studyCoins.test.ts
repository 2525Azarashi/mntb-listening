import { describe, expect, it } from 'vitest';
import { applyStudySolved, emptyProgress, studyCoinsFor, STUDY_COINS_MIN, STUDY_COINS_MAX } from '../src/battle/core/growth';

// F3（2026-11-04）：正解ごとのマナコインを 2〜5枚で上下（速さ・れんぞく正解）
describe('正解のマナコイン 2〜5枚', () => {
  it('遅くて連続なし → 2枚、速くて連続あり → 5枚', () => {
    expect(studyCoinsFor({ timeUsed: 90, timeLimit: 100, streak: 0 })).toBe(2);
    expect(studyCoinsFor({ timeUsed: 30, timeLimit: 100, streak: 3 })).toBe(5);
  });
  it('速さの段階：40%以内 +2・70%以内 +1', () => {
    expect(studyCoinsFor({ timeUsed: 40, timeLimit: 100 })).toBe(4);
    expect(studyCoinsFor({ timeUsed: 70, timeLimit: 100 })).toBe(3);
    expect(studyCoinsFor({ timeUsed: 71, timeLimit: 100 })).toBe(2);
  });
  it('時間の記録がない問題は「ふつう」（3枚、連続なら4枚）', () => {
    expect(studyCoinsFor({})).toBe(3);
    expect(studyCoinsFor({ streak: 5 })).toBe(4);
    expect(studyCoinsFor({ timeUsed: 10, timeLimit: 0 })).toBe(3);
  });
  it('どんな値でも 2〜5枚に収まる', () => {
    for (const t of [-5, 0, 1, 50, 999, NaN]) for (const s of [0, 2, 3, 100]) {
      const c = studyCoinsFor({ timeUsed: t, timeLimit: 60, streak: s });
      expect(c).toBeGreaterThanOrEqual(STUDY_COINS_MIN);
      expect(c).toBeLessThanOrEqual(STUDY_COINS_MAX);
    }
  });
  it('applyStudySolved のコインと記録が一致する（XPは15のまま）', () => {
    const p = emptyProgress('u');
    const r = applyStudySolved(p, '2026-11-04', 0, 4, { timeUsed: 10, timeLimit: 100 });
    expect(r.reward).toEqual({ xp: 15, coins: 5 });
    expect(r.next.coins - p.coins).toBe(5);
  });
});
