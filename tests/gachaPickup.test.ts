import { describe, expect, it } from 'vitest';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { GACHA_PREVIEWS } from '../src/data/gachaPreviews.generated';
import { gachaItems, gachaItemsByRarity } from '../src/battle/core/arenaEconomy';
import { gachaRarityOf, printOf } from '../src/battle/core/growth';
import { FEATURED_UR_IDS } from '../src/components/GachaParts';
import { pickupItems } from '../src/components/gacha/GachaPickup';

describe('ガチャのピックアップ（B案：画面に並べる）', () => {
  const items = gachaItems();
  const tiers = gachaItemsByRarity();
  const ur = FEATURED_UR_IDS.map((id) => items.find((i) => i.id === id)!);
  it('LR 全種 → 厳選UR 10種の順', () => {
    const list = pickupItems(tiers.LR, ur);
    expect(list.slice(0, tiers.LR.length).every((i) => gachaRarityOf(i) === 'LR')).toBe(true);
    expect(list.slice(tiers.LR.length).map((i) => i.id)).toEqual([...FEATURED_UR_IDS]);
  });
  it('プレビュー画像は実在し、1枚 30KB 以下・各2枚まで', () => {
    for (const [id, files] of Object.entries(GACHA_PREVIEWS)) {
      expect(printOf(id), id).toBeTruthy();
      expect(files.length).toBeLessThanOrEqual(2);
      for (const f of files) {
        expect(existsSync(`public${f}`), f).toBe(true);
        expect(statSync(`public${f}`).size).toBeLessThanOrEqual(30 * 1024);
      }
    }
    const listed = new Set(Object.values(GACHA_PREVIEWS).flat().map((f) => f.split('/').pop()));
    expect(readdirSync('public/prints/previews').filter((f) => !listed.has(f))).toEqual([]);
  });
  it('GachaRoom に欄が入り、目玉カードは1つのまま', () => {
    const room = readFileSync('src/components/GachaRoom.tsx', 'utf8');
    expect(room).toContain('<GachaPickup ');
    expect(room).not.toContain('data-gacha-featured-item');
  });
});
