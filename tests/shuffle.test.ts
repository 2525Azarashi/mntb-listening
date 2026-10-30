import { describe, expect, it, vi } from 'vitest';
import { shuffleSecure, shuffleWith } from '../src/utils/shuffle';
import { rng } from '../src/data/vocabQuiz';

/** 2026-10-28 リファクタリング A8：4か所にあったシャッフルを1つにした。並びが以前と同じかを、以前の書き方と比べて確かめる */
describe('shuffle（共通化しても並びは変わらない）', () => {
  // 以前 vocabQuiz.ts / reading/index.ts にあった書き方（その場で入れ替える）
  const oldInPlace = <T,>(a: T[], r: () => number) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j]!, a[i]!]; } return a; };

  it('同じ乱数なら以前と同じ並び（seed を変えて100通り）', () => {
    const items = Array.from({ length: 37 }, (_, i) => i);
    for (let seed = 1; seed <= 100; seed++) {
      expect(shuffleWith(items, rng(seed))).toEqual(oldInPlace(items.slice(), rng(seed)));
    }
  });

  it('元の配列は変えない・中身は同じ（重複・欠けなし）', () => {
    const items = ['a', 'b', 'c', 'd', 'e'];
    const out = shuffleWith(items, rng(7));
    expect(items).toEqual(['a', 'b', 'c', 'd', 'e']);
    expect([...out].sort()).toEqual(items);
  });

  it('暗号用の乱数版：以前の ManaRush と同じ計算（乱数を固定して比べる）', () => {
    const fixed = [5, 99, 3, 18, 77, 1, 42, 8];
    const spy = vi.spyOn(crypto, 'getRandomValues').mockImplementation(((arr: Uint32Array) => { arr.set(fixed.slice(0, arr.length)); return arr; }) as typeof crypto.getRandomValues);
    const items = [10, 11, 12, 13, 14, 15, 16, 17];
    const old = [...items]; for (let i = old.length - 1; i > 0; i -= 1) { const j = fixed[i]! % (i + 1); [old[i], old[j]] = [old[j]!, old[i]!]; }
    expect(shuffleSecure(items)).toEqual(old);
    expect(items).toEqual([10, 11, 12, 13, 14, 15, 16, 17]);
    spy.mockRestore();
  });
});
