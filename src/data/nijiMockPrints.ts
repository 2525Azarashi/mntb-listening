/**
 * LR（レジェンドレア）：2次試験ガチャの大当たり＝国公立2次 英語 予想問題（名古屋大学 前期の形式に沿った書き下ろし）。
 *   1冊＝問題編＋解答・解説編（大問Ⅰ〜Ⅳ・105分・100点）。3回分。
 *   ★過去問ではない★ 英文・設問・図表・解答はすべて書き下ろし。過去問・解答速報・講評の文章は引用していない
 *   （英語5語以上・日本語12字以上の連続一致がないことを機械で確認済み）。表紙と奥付に「大学とは関係がない」旨を明記。
 *
 * PDF は問題編と解答・解説編を pdfunite でつないだもの。pages / kb は実物の値（tests/nijiGacha.test.ts が照合）。
 */
import type { GachaPrintDef } from './gachaPrints.generated';

const nagoya = (n: number, pages: number, kb: number): GachaPrintDef => ({
  id: `print_lr_niji_nagoya_en_${n}`,
  label: `国公立2次 英語 予想問題 名古屋大学 前期対策 第${n}回（問題＋解答・解説）`,
  subject: 'english_reading',
  category: '演習プリント',
  file: `/prints/print_lr_niji_nagoya_en_${n}.pdf`,
  thumb: `/prints/thumbs/print_lr_niji_nagoya_en_${n}.webp`,
  pages,
  kb,
});

export const NIJI_MOCK_PRINTS: readonly GachaPrintDef[] = [
  nagoya(1, 28, 2026),
  nagoya(2, 30, 2033),
  nagoya(3, 30, 1983),
];

/** 予想問題に必ず添える注意書き（ガチャの詳細・ピックアップでも同じ文を出す） */
export const NIJI_DISCLAIMER = '名古屋大学の過去問・公式問題ではありません。予想問題であり、大学とは関係がありません。';
