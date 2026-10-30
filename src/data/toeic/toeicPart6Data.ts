/**
 * ===================================================================
 * TOEIC® L&R Part 6（長文穴埋め）データ（2026-10-30 準備）
 * ===================================================================
 *
 * Part 5（toeicPart5Data.ts）と同じ「parts → chapters → practiceProblems」の形。
 * 単元は1つ（tp6_1）で、その中に「第1回〜」（1回＝文書4つ・16問）を並べる。
 *
 * ★まだ教科の登録簿（subjects.ts）・allChapters.ts にはつないでいない★
 *   問題が0回のうちにつなぐと、空の教科が画面に出るため。つなぐ手順は docs/TOEIC_DESIGN.md §9。
 *
 * ■ 問題は音を出さない（Part 5・英文法と同じ扱い）
 *   完成文・全訳・語句は、解説の表示用に文字だけ持つ（explanationTracks）。
 */
import type { Problem } from '../../types/curriculum';
import { countProblemsInChapters } from '../problemCount';
import type { ToeicChapter, ToeicPart } from './toeicPart5Data';
import { buildToeicP6Round, TOEIC_P6_CHAPTER_ID, type ToeicP6Set } from './toeicPart6Kit';
import { TOEIC_P6_ROUNDS } from './toeicPart6Rounds';

function buildProblems(rounds: readonly (readonly ToeicP6Set[])[]): Problem[] {
  return rounds.map((sets, i) => {
    const problem = buildToeicP6Round({ round: i + 1 }, sets) as unknown as Problem;
    problem.explanationTracks = problem.audioTracks;
    delete problem.audioTracks;
    problem.stepwise = true;
    return problem;
  });
}

export const toeicPart6Data: { parts: ToeicPart[] } = {
  parts: [
    {
      id: 'tp6',
      title: 'TOEIC Part 6 長文穴埋め',
      chapters: [
        {
          id: TOEIC_P6_CHAPTER_ID,
          abstractTitle: 'Part 6 長文穴埋め',
          realTitle: 'Part 6',
          questionGroup: 'Part 6',
          topics: ['1回 文書4つ・16問・4択', '文法・語彙・つなぎの語句・文挿入'],
          practiceProblems: buildProblems(TOEIC_P6_ROUNDS),
          miniTest: [],
        },
      ],
    },
  ],
};

export function getAllToeicPart6Chapters(): ToeicChapter[] {
  return toeicPart6Data.parts.flatMap((p) => p.chapters);
}

/** 収録状況（単元数・回数・問題数）。データから数える */
export function getToeicPart6Stats() {
  const chapters = getAllToeicPart6Chapters();
  const questions = countProblemsInChapters(chapters);
  const marks = chapters.reduce(
    (sum, c) => sum + c.practiceProblems.reduce((n, p) => n + (Array.isArray(p?.subQuestions) ? p.subQuestions.length : 0), 0),
    0,
  );
  return { chapters: chapters.length, questions, marks };
}
