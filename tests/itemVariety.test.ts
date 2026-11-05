import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import { ITEMS, shopPriceOf } from '../src/battle/core/growth';
import { gachaItems } from '../src/battle/core/arenaEconomy';
import { COMPANIONS, STAGES, WALLPAPERS, parseAccessory, type AccessorySlot } from '../src/battle/core/tobiraParts';

// F7（2026-11-04）「お供とかで『この条件のアイテムはありません』と出る」→ どの種類もショップ・ガチャに十分並ぶ
const KINDS = ['pose', 'frame', 'hat', 'glasses', 'cheek', 'aura', 'wallpaper', 'stage', 'companion'] as const;

describe('F7 アイテムの増量', () => {
  it('ショップ（マナコインで交換）に、どの種類も並ぶ', () => {
    for (const k of KINDS) {
      const n = ITEMS.filter((i) => i.kind === k && shopPriceOf(i) != null).length;
      expect(n, k).toBeGreaterThanOrEqual(2);
    }
    for (const k of ['hat', 'glasses', 'cheek', 'aura', 'wallpaper', 'companion'] as const) {
      expect(ITEMS.filter((i) => i.kind === k && shopPriceOf(i) != null).length, k).toBeGreaterThanOrEqual(5);
    }
  });
  it('ガチャのお供・ホーム背景が増えている', () => {
    const g = gachaItems('kyotsu');
    expect(g.filter((i) => i.kind === 'companion' && i.gacha).length).toBeGreaterThanOrEqual(18);
    expect(g.filter((i) => i.kind === 'stage' && i.gacha).length).toBeGreaterThanOrEqual(11);
  });
  it('追加した物はすべて描ける（お供の色・背景・壁紙・アクセサリの形）', () => {
    const companionCss = fs.readFileSync('src/battle/ui/companion.css', 'utf8');
    const stageCss = fs.readFileSync('src/styles/home-stage.css', 'utf8');
    for (const i of ITEMS) {
      if (i.kind === 'companion') {
        expect(COMPANIONS[i.value], i.id).toBeTruthy();
        if (i.value !== 'key_gold') expect(companionCss, i.id).toContain(`[data-companion=${i.value}]`);
      }
      if (i.kind === 'stage') {
        expect(STAGES[i.value], i.id).toBeTruthy();
        expect(stageCss, i.id).toContain(`[data-stage=${i.value}]`);
        expect(stageCss, i.id).toContain(`[data-stage-swatch=${i.value}]`);
      }
      if (i.kind === 'wallpaper') expect(WALLPAPERS[i.value], i.id).toBeTruthy();
      if (['hat', 'glasses', 'cheek', 'aura'].includes(i.kind)) expect(parseAccessory(i.kind as AccessorySlot, i.value), i.id).not.toBeNull();
    }
  });
  it('id が重複していない・ショップの値段は 60〜400 枚（PDF を除く）', () => {
    const ids = ITEMS.map((i) => i.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const i of ITEMS) {
      if (i.kind === 'print') continue;
      const p = shopPriceOf(i);
      if (p != null) { expect(p, i.id).toBeGreaterThanOrEqual(60); expect(p, i.id).toBeLessThanOrEqual(400); }
    }
  });
});
