/**
 * LR（レジェンドレア）：大阪大学 前期日程 外国語（英語）対策の書き下ろし予想問題。
 * 各回を問題・解答解説の順に連結した1冊にし、ガチャ・マイPDFでも1アイテムとして扱う。
 * PDF は scripts/gacha-prints/osaka_mock/render.py で問題・解答を生成後、pdfunite で連結する。
 */
import type { GachaPrintDef } from './gachaPrints.generated';

const round = (n: number, pages: number, kb: number): GachaPrintDef => ({
  id: `print_lr_osaka_${n}`,
  label: `大阪大学 前期 英語 予想問題 第${n}回（問題＋解答・解説・150点・大学とは無関係のオリジナル）`,
  subject: 'english_reading',
  category: '演習プリント',
  file: `/prints/print_lr_osaka_${n}.pdf`,
  thumb: `/prints/thumbs/print_lr_osaka_${n}.webp`,
  pages,
  kb,
});

export const OSAKA_MOCK_PRINTS: readonly GachaPrintDef[] = [
  round(1, 27, 1544),
  round(2, 26, 1563),
  round(3, 27, 1550),
];
