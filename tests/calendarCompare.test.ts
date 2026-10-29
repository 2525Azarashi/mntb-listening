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
    expect(src).toContain('aria-pressed={picks.includes(d)}');
    expect(src).not.toMatch(/クリア|すべて外す/);
  });
});
