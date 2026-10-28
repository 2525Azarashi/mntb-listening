/** TOEIC Part 5 の回の並び（第1回〜）。回を足したらここに1行足す */
import type { ToeicP5Item } from './toeicPart5Kit';
import { ROUND_01 } from './toeicPart5Round01';
import { ROUND_02 } from './toeicPart5Round02';
import { ROUND_03 } from './toeicPart5Round03';
import { ROUND_04 } from './toeicPart5Round04';

export const TOEIC_P5_ROUNDS: readonly ToeicP5Item[][] = [
  ROUND_01,
  ROUND_02,
  ROUND_03,
  ROUND_04,
];
