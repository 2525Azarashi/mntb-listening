import { describe, expect, it } from 'vitest';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { GACHA_PREVIEWS } from '../src/data/gachaPreviews.generated';
import { gachaItems } from '../src/battle/core/arenaEconomy';
import { gachaRarityOf, printOf } from '../src/battle/core/growth';
import { FEATURED_UR_IDS } from '../src/components/GachaParts';
import { pickupItems, pickupLrSummary, pickupShelves, pickupUnivLabel } from '../src/components/gacha/GachaPickupModal';

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

describe('ピックアップ一覧の整理（2026-11-04：PDF が増えても縦に長くならない）', () => {
  const items = gachaItems();
  const lr = pickupItems(items).filter((i) => gachaRarityOf(i) === 'LR');
  it('LR はどれか1つの棚に入り、棚の合計＝LR 全部（落ちるものがない）', () => {
    const shelves = pickupShelves(lr);
    expect(shelves.reduce((n, s) => n + s.count, 0)).toBe(lr.length);
    for (const s of shelves) expect(s.groups.reduce((n, g) => n + g.items.length, 0), s.id).toBe(s.count);
    expect(shelves.find((s) => s.id === 'other')).toBeUndefined();
  });
  it('2次の予想問題は大学ごとにまとまる（同じ大学が2つに分かれない）', () => {
    for (const s of pickupShelves(lr)) {
      const labels = s.groups.map((g) => g.label);
      expect(new Set(labels).size, s.id).toBe(labels.length);
    }
    expect(pickupUnivLabel('print_lr_niji_kochim_en_1')).toBe('高知大学（医学部医学科）');
    expect(pickupUnivLabel('print_lr_hokudai_q_1')).toBe('北海道大学');
    expect(pickupUnivLabel('print_lr_kyotsu_r_1')).toBeNull();
  });
  it('LR の説明は大学名を並べず「◯大学・◯冊」の短い文', () => {
    const niji = lr.filter((i) => pickupUnivLabel(i.id));
    const text = pickupLrSummary(niji)!;
    expect(text).toMatch(/^\d+大学・\d+冊。/);
    expect(text.length).toBeLessThan(40);
  });
});
