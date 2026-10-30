import { describe, expect, it } from 'vitest';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { GACHA_PREVIEWS } from '../src/data/gachaPreviews.generated';
import { gachaItems } from '../src/battle/core/arenaEconomy';
import { gachaRarityOf, printOf } from '../src/battle/core/growth';
import { FEATURED_UR_IDS } from '../src/components/GachaParts';
import { pickupItems } from '../src/components/gacha/GachaPickupModal';

describe('ガチャのピックアップ（中身を少し見る）', () => {
  const items = gachaItems();
  it('LR 全種と厳選UR 10種が並ぶ（LR が先）', () => {
    const list = pickupItems(items);
    const lr = items.filter((i) => gachaRarityOf(i) === 'LR');
    expect(list.slice(0, lr.length).map((i) => i.id).sort()).toEqual(lr.map((i) => i.id).sort());
    expect(list.slice(lr.length).map((i) => i.id)).toEqual([...FEATURED_UR_IDS]);
    for (const i of list.slice(lr.length)) expect(gachaRarityOf(i)).toBe('UR');
  });
  it('プレビュー画像は実在し、1枚 30KB 以下・各2枚まで（全部は見せない）', () => {
    for (const [id, files] of Object.entries(GACHA_PREVIEWS)) {
      expect(printOf(id), id).toBeTruthy();
      expect(files.length).toBeGreaterThanOrEqual(1);
      expect(files.length).toBeLessThanOrEqual(2);
      for (const f of files) {
        expect(existsSync(`public${f}`), f).toBe(true);
        expect(statSync(`public${f}`).size).toBeLessThanOrEqual(30 * 1024);
      }
    }
    const listed = new Set(Object.values(GACHA_PREVIEWS).flat().map((f) => f.split('/').pop()));
    expect(readdirSync('public/prints/previews').filter((f) => !listed.has(f))).toEqual([]);
  });
  it('ガチャ画面は下のボタンからダイアログで開く（画面に一覧を並べない）', () => {
    const room = readFileSync('src/components/GachaRoom.tsx', 'utf8');
    // 2026-10-29：バナー（ピックアップ一覧のボタンを含む）は左右スワイプの部品 GachaPoolCarousel に移した
    const banner = readFileSync('src/components/gacha/GachaPoolCarousel.tsx', 'utf8');
    expect(room).toContain('<GachaPoolCarousel');
    expect(banner).toContain('data-gacha-pickup-open');
    expect(banner).not.toContain('data-gacha-featured-item');
    expect(room).toContain('<GachaPickupModal');
    expect(room).not.toContain('data-gacha-featured-item');
  });
});
