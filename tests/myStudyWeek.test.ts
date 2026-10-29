import { describe, expect, it } from 'vitest';
import { emptyStore, upsertRecord, weekByMaterial, dayOf } from '../src/features/studylog/manualLogCore';

describe('マイページの「この7日」（2026-10-28 A1）', () => {
  const now = new Date(2026, 9, 28, 12).getTime();
  it('教材ごとに7日ぶんの秒数を並べ、アプリ内の時間は最後に1行', () => {
    let s = emptyStore();
    s = upsertRecord(s, { day: dayOf(now), subject: 'math', materialName: 'チャート', minutes: 30 }, now).store;
    s = upsertRecord(s, { day: dayOf(now - 86_400_000), subject: 'eng', materialName: '単語帳', minutes: 20 }, now).store;
    const w = weekByMaterial(s, { total: 600, days: { [dayOf(now)]: 600 } }, now);
    expect(w.days).toHaveLength(7);
    expect(w.days[6]).toBe(dayOf(now));
    expect(w.rows[0].label).toBe('チャート');
    expect(w.rows[0].seconds[6]).toBe(1800);
    expect(w.rows[1].seconds[5]).toBe(1200);
    expect(w.rows.at(-1)!.key).toBe('app');
    expect(w.rows.at(-1)!.seconds[6]).toBe(600);
  });
  it('記録がなければ行はない', () => {
    expect(weekByMaterial(emptyStore(), { total: 0, days: {} }, now).rows).toEqual([]);
  });
});
