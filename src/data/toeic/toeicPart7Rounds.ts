/**
 * TOEIC Part 7 の回の並び（第1回〜）。1回＝セット7つ（1つの文書5・2つの文書1・3つの文書1）。
 * 回を足したら toeicPart7RoundNN.ts を作り、ここに1行足す（Part 5・6 の Rounds と同じ）。
 *
 * 2026-11-02：始めた。
 */
import type { ToeicP7Set } from './toeicPart7Kit';
import { P7_ROUND_01 } from './toeicPart7Round01';

export const TOEIC_P7_ROUNDS: readonly ToeicP7Set[][] = [
  P7_ROUND_01,
];
