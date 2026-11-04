import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import { OSAKA_MOCK_PRINTS } from '../src/data/osakaMockPrints';
import { gachaItemsByRarity } from '../src/battle/core/arenaEconomy';
import { ITEMS, gachaRarityOf, normalizeProgress, printOf } from '../src/battle/core/growth';
import { GACHA_PREVIEWS } from '../src/data/gachaPreviews.generated';

const hasPdf = (() => { try { execFileSync('pdftotext', ['-v'], { stdio: 'ignore' }); return true; } catch { return false; } })();
const text = (file: string) => execFileSync('pdftotext', [`public${file}`, '-'], { encoding: 'utf8', maxBuffer: 64 << 20 }).replace(/\s+/g, '');

describe('LR：大阪大学 前期 英語 予想問題', () => {
  it('3回分を各1アイテムにまとめ、各PDFに問題・解答解説を順に収録する', () => {
    expect(OSAKA_MOCK_PRINTS).toHaveLength(3);
    for (const [index, p] of OSAKA_MOCK_PRINTS.entries()) {
      const n = index + 1;
      expect(p.id).toBe(`print_lr_osaka_${n}`);
      expect(p.label).toContain('問題＋解答・解説');
      expect(existsSync(`public${p.file}`), p.id).toBe(true);
      expect(existsSync(`public${p.thumb}`), p.id).toBe(true);
      expect(Math.abs(statSync(`public${p.file}`).size / 1024 - p.kb), p.id).toBeLessThan(2);
      expect(GACHA_PREVIEWS[p.id]?.length, p.id).toBeGreaterThan(0);
      if (hasPdf) {
        const t = text(p.file);
        expect(t, p.id).toContain('解答用紙');
        expect(t, p.id).toContain('採点基準');
        expect(t, p.id).toContain('全訳');
        expect(t, p.id).toContain('大阪大学の過去問・公式問題ではありません');
        expect(t, p.id).toContain('大学とは関係がありません');
        expect(t, p.id).toContain('150点');
      }
    }
  });
  it('LRの抽選対象かつ従来の問題・解答の所持を統合アイテムへ引き継ぐ', () => {
    const lr = gachaItemsByRarity('niji').LR.map(i => i.id);
    for (const p of OSAKA_MOCK_PRINTS) {
      const item = ITEMS.find(i => i.id === p.id)!;
      expect(item.kind).toBe('print');
      expect(gachaRarityOf(item)).toBe('LR');
      expect(lr).toContain(p.id);
      expect(printOf(p.id)?.file).toBe(p.file);
      const n = p.id.split('_').at(-1);
      expect(normalizeProgress('test', { owned: [`print_lr_osaka_q_${n}`, `print_lr_osaka_a_${n}`] }).owned).toContain(p.id);
    }
  });
});
