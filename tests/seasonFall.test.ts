import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { seasonOf } from '../src/components/SakuraPetals';

describe('D9：季節で降るものが変わる（2026-10-30）', () => {
  it('月から季節を決める（秋＝9〜11月は紅葉）', () => {
    const at = (m: number) => seasonOf(new Date(2026, m - 1, 15));
    expect([3, 4, 5].map(at)).toEqual(['spring', 'spring', 'spring']);
    expect([6, 7, 8].map(at)).toEqual(['summer', 'summer', 'summer']);
    expect([9, 10, 11].map(at)).toEqual(['autumn', 'autumn', 'autumn']);
    expect([12, 1, 2].map(at)).toEqual(['winter', 'winter', 'winter']);
  });
  it('季節ごとの形が CSS にある', () => {
    const css = readFileSync('src/styles/surfaces.css', 'utf8');
    for (const s of ['summer', 'autumn', 'winter']) expect(css).toContain(`.sakura-container[data-season=${s}]`);
    expect(readFileSync('src/components/SakuraPetals.tsx', 'utf8')).toContain('data-season={current}');
  });
});
