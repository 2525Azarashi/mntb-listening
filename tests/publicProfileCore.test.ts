import { describe, expect, it } from 'vitest';
import { barPercents, buildWeek, dayKey, normalizeBio, normalizeGrade, parseWeek, weekLabels, weekSummary, BIO_MAX, DAY_SECONDS_MAX } from '../src/utils/publicProfileCore';
import { parsePublicStudyProfile } from '../src/utils/publicStudyProfile';

const NOW = new Date(2026, 9, 26, 15, 0, 0).getTime(); // 月曜

describe('週の記録', () => {
  it('古い日→今日の7日分。無い日は0、上限で切る', () => {
    const days = { [dayKey(NOW)]: 600, [dayKey(NOW - 86_400_000)]: 99999, [dayKey(NOW - 10 * 86_400_000)]: 50 };
    const w = buildWeek(days, NOW);
    expect(w).toHaveLength(7);
    expect(w[6]).toBe(600);
    expect(w[5]).toBe(DAY_SECONDS_MAX);
    expect(w.slice(0, 5)).toEqual([0, 0, 0, 0, 0]);
    expect(weekLabels(NOW)[6]).toBe('月');
  });
  it('集計と棒の高さ（最長の日が100%、少しでもあれば最低6%）', () => {
    expect(weekSummary([0, 30, 60, 600, 0, 0, 1200])).toEqual({ total: 1890, activeDays: 3, max: 1200 });
    expect(barPercents([0, 10, 600, 1200, 0, 0, 0])).toEqual([0, 6, 50, 100, 0, 0, 0]);
    expect(barPercents([0, 0, 0, 0, 0, 0, 0])).toEqual([0, 0, 0, 0, 0, 0, 0]);
  });
  it('読んだ値の形チェック', () => {
    expect(parseWeek([1, 2, 3, 4, 5, 6, 7])).toEqual([1, 2, 3, 4, 5, 6, 7]);
    expect(parseWeek([1, 2, 3])).toBeNull();
    expect(parseWeek([1, 2, 3, 4, 5, 6, -1])).toBeNull();
    expect(parseWeek([1, 2, 3, 4, 5, 6, 0.5])).toBeNull();
  });
});

describe('学年・自己紹介', () => {
  it('学年は選択肢だけ', () => {
    expect(normalizeGrade('高校2年')).toBe('高校2年');
    expect(normalizeGrade('○○高校2年A組')).toBe('');
    expect(normalizeGrade(3)).toBe('');
  });
  it('自己紹介は整えて160文字まで', () => {
    expect(normalizeBio('  a\r\n\n\n\nb  ')).toBe('a\n\nb');
    expect(normalizeBio('あ'.repeat(300))).toHaveLength(BIO_MAX);
  });
});

describe('公開プロフィールの読み込み', () => {
  it('古い文書（新しい項目なし）も読める', () => {
    const p = parsePublicStudyProfile({ public: true, targetSchool: 'A大', studySeconds: 60 });
    expect(p?.week).toBeNull();
    expect(p?.grade).toBe('');
    expect(p?.look).toEqual({ pose: '', frame: '', hat: '', glasses: '' });
  });
  it('新しい項目を読み、形の悪い値は捨てる', () => {
    const p = parsePublicStudyProfile({
      public: true, targetSchool: 'A大', studySeconds: 60, nickname: 'たろう', grade: '高校3年', bio: 'よろしく',
      week: [0, 0, 0, 0, 0, 60, 120], weekEnd: '2026-10-26', streak: 5, solved: 40, badges: 3, title: 'b_first_win',
      lookPose: 'pose_x', lookFrame: 'bad id!', lookHat: '', lookGlasses: 'g1',
    });
    expect(p).toMatchObject({ nickname: 'たろう', grade: '高校3年', bio: 'よろしく', streak: 5, solved: 40, badges: 3, title: 'b_first_win', weekEnd: '2026-10-26' });
    expect(p?.look).toEqual({ pose: 'pose_x', frame: '', hat: '', glasses: 'g1' });
  });
  it('public: true でなければ読まない', () => {
    expect(parsePublicStudyProfile({ public: false, targetSchool: '', studySeconds: 0 })).toBeNull();
  });
});
