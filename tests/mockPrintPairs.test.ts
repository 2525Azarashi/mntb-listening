import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import { gachaItemsByRarity } from '../src/battle/core/arenaEconomy';
import { normalizeProgress, printOf } from '../src/battle/core/growth';
import { GACHA_PREVIEWS } from '../src/data/gachaPreviews.generated';
import { KOBE_MOCK_PRINTS } from '../src/data/kobeMockPrints';
import { OSAKA_MOCK_PRINTS } from '../src/data/osakaMockPrints';
import { RITSU_MOCK_PRINTS } from '../src/data/ritsuMockPrints';
import { HOKUDAI_MOCK_PRINTS } from '../src/data/hokudaiMockPrints';
import { TOHOKU_MOCK_PRINTS } from '../src/data/tohokuMockPrints';
import { HIROSAKI_MOCK_PRINTS } from '../src/data/hirosakiMockPrints';
import { IWATE_MOCK_PRINTS } from '../src/data/iwateMockPrints';
import { AKITA_MOCK_PRINTS } from '../src/data/akitaMockPrints';
import { YAMAGATA_MOCK_PRINTS } from '../src/data/yamagataMockPrints';
import { FUKUSHIMA_MOCK_PRINTS } from '../src/data/fukushimaMockPrints';
import { UTSUNOMIYA_MOCK_PRINTS } from '../src/data/utsunomiyaMockPrints';
import { GUNMA_MOCK_PRINTS } from '../src/data/gunmaMockPrints';

const universities = [
  ['kobe', KOBE_MOCK_PRINTS], ['osaka', OSAKA_MOCK_PRINTS], ['ritsu', RITSU_MOCK_PRINTS],
  ['hokudai', HOKUDAI_MOCK_PRINTS], ['tohoku', TOHOKU_MOCK_PRINTS], ['hirosaki', HIROSAKI_MOCK_PRINTS],
  ['iwate', IWATE_MOCK_PRINTS], ['akita', AKITA_MOCK_PRINTS], ['yamagata', YAMAGATA_MOCK_PRINTS],
  ['fukushima', FUKUSHIMA_MOCK_PRINTS], ['utsunomiya', UTSUNOMIYA_MOCK_PRINTS],
  ['gunma', GUNMA_MOCK_PRINTS],
] as const;
const text = (file: string) => execFileSync('pdftotext', [`public${file}`, '-'], { encoding: 'utf8', maxBuffer: 64 << 20 }).replace(/\s+/g, '');

describe('大学別の問題＋解答・解説プリントは一回一冊', () => {
  it.each(universities)('%s：3回分が各1カードになり、PDFとサムネイルが実在する', (_slug, prints) => {
    expect(prints).toHaveLength(3);
    for (const [index, print] of prints.entries()) {
      const n = index + 1;
      expect(print.id).toMatch(new RegExp(`_${n}$`));
      expect(print.label).toContain('問題＋解答・解説');
      expect(existsSync(`public${print.file}`)).toBe(true);
      expect(existsSync(`public${print.thumb}`)).toBe(true);
      expect(Math.abs(statSync(`public${print.file}`).size / 1024 - print.kb)).toBeLessThan(2);
      expect(GACHA_PREVIEWS[print.id]?.length).toBeGreaterThan(0);
      expect(printOf(print.id)?.file).toBe(print.file);
      const pdfText = text(print.file);
      expect(pdfText).toContain('解答用紙');
      expect(pdfText).toMatch(/解答・解説|解答解説|解答一覧/);
    }
  });
  it('問題側・解答側の旧所持IDは、同じ回の新しい1冊アイテムにまとめて引き継ぐ', () => {
    const all = universities.flatMap(([slug, prints]) => prints.map((print, index) => ({ slug, print, n: index + 1 })));
    for (const { slug, print, n } of all) {
      const migrated = normalizeProgress('test', { owned: [`print_lr_${slug}_q_${n}`, `print_lr_${slug}_a_${n}`] }).owned;
      expect(migrated.filter((id) => id === print.id)).toHaveLength(1);
    }
  });
  it('36冊すべてが2次試験ガチャのLRとして扱われる', () => {
    const lrIds = new Set(gachaItemsByRarity('niji').LR.map((item) => item.id));
    for (const [, prints] of universities) for (const print of prints) expect(lrIds.has(print.id)).toBe(true);
  });
});
