import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { gachaItems } from '../src/battle/core/arenaEconomy';
import { gachaRarityOf } from '../src/battle/core/growth';
import { weekEndLabel, weeklyPickup } from '../src/components/gacha/GachaItemDetail';

describe('ガチャのバナー（2026-10-28 A10・モンスト風）', () => {
  const items = gachaItems();
  it('今週のピックアップは LR 2つ＋UR 3つ。目玉とは重ならない', () => {
    const p = weeklyPickup(items, 42, 'print_book_listening_all');
    expect(p.map((i) => gachaRarityOf(i))).toEqual(['LR', 'LR', 'UR', 'UR', 'UR']);
    expect(p.some((i) => i.id === 'print_book_listening_all')).toBe(false);
  });
  it('週が変わると入れ替わる（いつも同じ UR にならない）', () => {
    const ids = new Set(Array.from({ length: 6 }, (_, w) => weeklyPickup(items, 40 + w).map((i) => i.id).join(',')));
    expect(ids.size).toBeGreaterThan(1);
  });
  it('期限の表示は日曜', () => {
    expect(weekEndLabel(0)).toBe('1/11（日）まで');
  });
  it('セット・かけらはガチャ画面から外し、ショップの「種類」に入れた', () => {
    const room = readFileSync('src/components/GachaRoom.tsx', 'utf8');
    const shop = readFileSync('src/components/MyCollection.tsx', 'utf8');
    expect(room).not.toContain('data-gacha-sets-open');
    expect(shop).toContain("['sets','セット収集']");
    expect(shop).toContain('<GachaSetsPanel');
  });
});
