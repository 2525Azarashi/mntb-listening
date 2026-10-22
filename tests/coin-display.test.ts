import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const growthHome = readFileSync('src/battle/ui/GrowthHomeStrip.tsx', 'utf8');

describe('マナコイン残高表示', () => {
  it('画面に戻るたび既存の残高を0から数え直さない', () => {
    expect(growthHome).toContain('<CountUp value={progress.coins} duration=');
    expect(growthHome).not.toContain('<CountUp value={progress.coins} fromZero');
  });
});
