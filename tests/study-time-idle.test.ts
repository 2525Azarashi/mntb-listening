import { describe, it, expect } from 'vitest';
import { activeStudySeconds, STUDY_IDLE_MS } from '../src/utils/studyTime';
import { daysUntil, getDaysUntilExam, getDaysUntilSecondExam } from '../src/utils/examCountdown';

describe('学習時間：1分操作がなければ数えない（2026-10-11）', () => {
  const t0 = 1_000_000;
  it('操作が続いていれば、その区間をそのまま数える', () => {
    expect(activeStudySeconds(t0, t0 + 15000, t0 + 14000)).toBe(15);
  });
  it('最後の操作から1分を超えた分は切り捨てる', () => {
    // 最後の操作が t0、区間は t0+50s〜t0+65s → 数えるのは t0+60s まで（10秒）
    expect(activeStudySeconds(t0 + 50000, t0 + 65000, t0)).toBe(10);
  });
  it('1分以上放置した区間はゼロ', () => {
    expect(activeStudySeconds(t0 + STUDY_IDLE_MS + 1000, t0 + STUDY_IDLE_MS + 16000, t0)).toBe(0);
  });
});

describe('本番までの日数', () => {
  it('共通テスト・2次(前期)', () => {
    const from = new Date(2026, 9, 11);
    expect(getDaysUntilExam(from)).toBe(97);
    expect(getDaysUntilSecondExam(from)).toBe(137);
    expect(daysUntil(new Date(2026, 0, 1), from)).toBe(0);
  });
});
