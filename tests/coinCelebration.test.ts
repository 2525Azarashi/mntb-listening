import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

describe('D10：マナコインを手に入れたら派手な演出（2026-10-30）', () => {
  const store = readFileSync('src/battle/data/growthStore.ts', 'utf8');
  const cele = readFileSync('src/components/CoinCelebration.tsx', 'utf8');
  it('増えたときだけ知らせる（使ったとき・同期では知らせない）', () => {
    expect(store).toContain('const gained = result.next.coins - current.progress.coins;');
    expect(store).toContain('if (gained > 0) announceCoinGain(gained);');
    expect(store).toContain('export function subscribeCoinGain(');
  });
  it('どの画面でも出る（App に置く）・少しなら控えめ、たくさんなら光の輪', () => {
    expect(readFileSync('src/App.tsx', 'utf8')).toContain('<CoinCelebration />');
    expect(cele).toContain("data-size={big ? 'big' : 'small'}");
    expect(cele).toContain('coin-cele-ring');
    expect(readFileSync('src/components/coin-celebration.css', 'utf8')).toContain('prefers-reduced-motion: reduce');
  });
});
