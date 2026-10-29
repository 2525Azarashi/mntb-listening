import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { togglePick, PICK_MAX } from '../src/features/studylog/CalendarTab';

/** B8（2026-10-29）：カレンダーで日付を押すと黒くなりグラフに加わる。もう一度押すと外れる。最大7日 */
describe('カレンダーの日付選び（最大7日）', () => {
  it('押すと加わり、もう一度押すと外れる', () => {
    let p = togglePick([], '2026-10-01');
    expect(p).toEqual(['2026-10-01']);
    p = togglePick(p, '2026-10-03');
    expect(p).toEqual(['2026-10-01', '2026-10-03']);
    p = togglePick(p, '2026-10-01');
    expect(p).toEqual(['2026-10-03']);
  });
  it('7日を超えたら、いちばん前に押した日を外す', () => {
    expect(PICK_MAX).toBe(7);
    let p: string[] = [];
    for (let d = 1; d <= 8; d++) p = togglePick(p, `2026-10-0${d}`.replace('-010', '-10'));
    expect(p).toHaveLength(7);
    expect(p).not.toContain('2026-10-01');
    expect(p[6]).toBe('2026-10-08');
  });
  it('グラフはカレンダーのすぐ下・ボタンを増やさない（日付だけで操作）', () => {
    const src = readFileSync('src/features/studylog/CalendarTab.tsx', 'utf8');
    expect(src).toContain('data-slog-compare');
    // C5：改訂前の「その日の記録リスト」は消して、マイページと同じ「何を何分」の表に
    expect(src).toContain('data-slog-what');
    expect(src).not.toContain('slog-picked');
    expect(src).toContain('aria-pressed={picks.includes(d)}');
    expect(src).not.toMatch(/クリア|すべて外す/);
  });
});

import { emptyStore, materialsByDays, upsertRecord } from '../src/features/studylog/manualLogCore';
describe('C5 選んだ日ごとの「何を何分」', () => {
  it('教材ごとに、選んだ日の列で分を数える（アプリ内は最後の行）', () => {
    let store = emptyStore();
    const now = new Date('2026-10-20T12:00:00+09:00').getTime();
    const add = (day: string, minutes: number, name: string) => { store = upsertRecord(store, { day, minutes, subject: 'english', materialName: name } as never, now).store; };
    add('2026-10-18', 30, '単語帳'); add('2026-10-20', 45, '単語帳'); add('2026-10-20', 20, '長文');
    const rows = materialsByDays(store, { total: 600, days: { '2026-10-18': 600 } }, ['2026-10-18', '2026-10-20']);
    const words = rows.find(r => r.label === '単語帳')!;
    expect(words.seconds).toEqual([1800, 2700]);
    expect(words.recordIds?.[1]).toHaveLength(1);
    expect(rows[rows.length - 1].key).toBe('app');
    expect(rows[rows.length - 1].seconds).toEqual([600, 0]);
  });
});
