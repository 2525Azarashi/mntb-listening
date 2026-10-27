/**
 * LR（レジェンドレア）：共通テスト 英語 予想問題（2025年度〜 新課程の形式）。
 *   リーディング（80分・100点・大問8・解答数44）とリスニング（30分・100点・大問6・37問）を各5回分。
 *   すべて書き下ろしのオリジナル問題（センターの過去問ではない）。リスニングは全スクリプト＋全訳つき（イラスト・地図入り。音声は ElevenLabs v4 で作る：make_audio_el.py）。リーディングは図・写真入り、英文量は本番並み（約5,000〜5,400語）。
 *
 * PDF は scripts/gacha-prints/kyotsu_mock/build.py で作る。pages / kb は .tmpwork/kyotsu-mock.json の値を写す
 * （tests/kyotsuMockPrints.test.ts が実物と照合する）。
 */
import type { GachaPrintDef } from './gachaPrints.generated';

const r = (n: number, pages: number, kb: number): GachaPrintDef => ({
  id: `print_lr_kyotsu_r_${n}`,
  label: `共通テスト 英語リーディング 予想問題 第${n}回（80分・100点）`,
  subject: 'english_reading',
  category: '演習プリント',
  file: `/prints/print_lr_kyotsu_r_${n}.pdf`,
  thumb: `/prints/thumbs/print_lr_kyotsu_r_${n}.webp`,
  pages,
  kb,
});
const l = (n: number, pages: number, kb: number): GachaPrintDef => ({
  id: `print_lr_kyotsu_l_${n}`,
  label: `共通テスト 英語リスニング 予想問題 第${n}回（スクリプト・全訳つき）`,
  subject: 'english_listening',
  category: '演習プリント',
  file: `/prints/print_lr_kyotsu_l_${n}.pdf`,
  thumb: `/prints/thumbs/print_lr_kyotsu_l_${n}.webp`,
  pages,
  kb,
});

export const KYOTSU_MOCK_PRINTS: readonly GachaPrintDef[] = [
  r(1, 28, 1395), l(1, 22, 1338),
  r(2, 26, 1129), l(2, 21, 1375),
  r(3, 27, 1300), l(3, 20, 1295),
  r(4, 26, 1624), l(4, 19, 1462),
  r(5, 26, 1256), l(5, 21, 1184),
];
