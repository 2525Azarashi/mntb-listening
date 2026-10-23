import { describe, expect, it } from 'vitest';
import { emptyProgress, itemById, badgeById, evaluateUnlocks, withAchievements } from '../src/battle/core/growth';
import { exchangeShards, gachaItems, rollGacha, shardCostOf } from '../src/battle/core/arenaEconomy';
import { GACHA_SETS, SHARDS_PER_DUPLICATE, completedSetCount } from '../src/battle/core/gachaSets';
import { parseAccessory } from '../src/battle/core/tobiraParts';
import { wallpaperOf } from '../src/battle/core/tobiraParts';
import { mergeGrowthEnvelope } from '../src/utils/userDataSyncCore';

describe('ガチャのセット収集', () => {
  it('セットの部品はすべてガチャで出る景品で、報酬フレームと称号が実在する', () => {
    const pool = new Set(gachaItems().filter((i) => i.gacha).map((i) => i.id));
    for (const s of GACHA_SETS) {
      expect(s.items).toHaveLength(4);
      for (const id of s.items) expect(pool.has(id), `${s.id}:${id}`).toBe(true);
      expect(itemById(s.reward)?.kind, s.reward).toBe('frame');
      expect(badgeById(s.badge), s.badge).toBeTruthy();
      // 報酬はガチャ・ショップに出ない
      expect(gachaItems().some((i) => i.id === s.reward)).toBe(false);
    }
  });
  it('4つそろえると称号と限定フレームが手に入り、3セットでコレクター', () => {
    let p = emptyProgress('u');
    p = withAchievements({ ...p, owned: [...p.owned, ...GACHA_SETS[0].items] });
    expect(p.badges[GACHA_SETS[0].badge]).toBeTypeOf('number');
    expect(p.owned).toContain(GACHA_SETS[0].reward);
    p = withAchievements({ ...p, owned: [...p.owned, ...GACHA_SETS[1].items, ...GACHA_SETS[2].items] });
    expect(completedSetCount(p.owned)).toBe(3);
    expect(p.owned).toContain('frame_set_collector');
    expect(evaluateUnlocks(p)).toEqual([]);
  });
  it('新しいアクセサリ・壁紙は見た目の定義がある', () => {
    for (const i of gachaItems()) {
      if (['hat', 'glasses', 'cheek', 'aura'].includes(i.kind)) expect(parseAccessory(i.kind as 'hat', i.value), i.id).not.toBeNull();
      if (i.kind === 'wallpaper') expect(wallpaperOf(i.value), i.id).not.toBeNull();
    }
  });
});

describe('とびらのかけら', () => {
  it('ダブるとかけらが貯まる（無料の動画ガチャでも）', () => {
    const p = { ...emptyProgress('u'), coins: 0 };
    const first = rollGacha(p, 0, 'N', { cost: 0, refundDuplicates: false })!;
    expect(first.shards).toBe(0);
    const again = rollGacha(first.next, 0, 'N', { cost: 0, refundDuplicates: false })!;
    expect(again.duplicate).toBe(true);
    expect(again.next.shards).toBe(SHARDS_PER_DUPLICATE[again.rarity]);
    expect(again.next.coins).toBe(0);
  });
  it('未所持のガチャ景品と交換できる。プリント・所持済み・足りないときは不可', () => {
    const target = gachaItems().find((i) => i.gacha && i.kind === 'hat')!;
    const cost = shardCostOf(target);
    const p = { ...emptyProgress('u'), shards: cost };
    const ok = exchangeShards(p, target.id);
    expect(ok.ok).toBe(true);
    expect(ok.next.shards).toBe(0);
    expect(ok.next.owned).toContain(target.id);
    expect(exchangeShards(ok.next, target.id).ok).toBe(false);
    expect(exchangeShards({ ...p, shards: cost - 1 }, target.id).ok).toBe(false);
    const print = gachaItems().find((i) => i.kind === 'print')!;
    expect(exchangeShards({ ...p, shards: 9999 }, print.id).ok).toBe(false);
    expect(exchangeShards({ ...p, shards: 9999 }, 'frame_set_sprout').ok).toBe(false);
  });
  it('2台で同期すると、かけらの増減が両方反映される', () => {
    const env = (shards: number) => ({ version: 1, progress: { ...emptyProgress('u'), shards }, receipts: [], day: '' });
    const merged = mergeGrowthEnvelope(env(15), env(3), env(5)) as { progress: { shards: number } };
    expect(merged.progress.shards).toBe(13); // 片方で +10、もう片方で -2
  });
});
