import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { gachaItemRate, gachaItems } from '../src/battle/core/arenaEconomy';
import { gachaRarityOf } from '../src/battle/core/growth';
import { availableCollectionRarities, filterCollectionByRarity } from '../src/components/gacha/collectionFilters';

const pools = ['kyotsu', 'niji'] as const;

describe('提供割合のPDFレアリティ絞り込み', () => {
  it.each(pools)('%s：PDFに実在するLR・UR・SRを自動で選べ、表示件数と確率が整合する', (pool) => {
    const pdfs = gachaItems(pool).filter((item) => item.kind === 'print');
    const rarities = availableCollectionRarities(pdfs);

    expect(rarities).toEqual(expect.arrayContaining(['LR', 'UR', 'SR']));
    expect(rarities).not.toContain('R');
    expect(rarities).not.toContain('N');

    const visible = rarities.flatMap((rarity) => {
      const filtered = filterCollectionByRarity(pdfs, rarity);
      expect(filtered.length).toBe(pdfs.filter((item) => gachaRarityOf(item) === rarity).length);
      expect(filtered.every((item) => item.kind === 'print' && gachaRarityOf(item) === rarity)).toBe(true);
      expect(filtered.every((item) => gachaItemRate(item, 'N', pool) > 0)).toBe(true);
      return filtered;
    });
    expect(visible.map((item) => item.id).sort()).toEqual(pdfs.map((item) => item.id).sort());
    expect(filterCollectionByRarity(pdfs, 'all')).toHaveLength(pdfs.length);
  });

  it('PDFを選んだ時だけレアリティ切り替えを表示し、選択レアリティの個別提供割合を出す', () => {
    const ui = readFileSync('src/components/gacha/GachaCollectionModal.tsx', 'utf8');
    expect(ui).toContain("collectionKind === 'print'");
    expect(ui).toContain('PDFのレアリティで絞り込む');
    expect(ui).toContain('rarityOptions.map');
    expect(ui).toContain('filterCollectionByRarity(collectionList, rarity)');
    expect(ui).toContain('pct(gachaItemRate(item, \'N\', pool))');
  });
});
