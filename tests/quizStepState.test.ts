/**
 * 演習画面の「いまどの問を表示しているか」の計算（utils/quizStepState.ts）。
 *
 * Phase 5 / A2 で Quiz.tsx の描画中にあった式をこの関数へ移した。
 * ここでは「移す前の式」をテストの中にそのまま書き写し、
 * 全教科・全大問・いろいろなステップ位置・範囲・解説表示の有無で
 * 新しい関数と結果が完全に一致することを確かめる。
 */
import { describe, expect, it } from 'vitest';
import { SUBJECTS, getChaptersOfSubject } from '../src/data/allChapters';
import {
  buildListeningSteps,
  buildProgressPill,
  isPerSubQuestionListening,
  stepSubQuestions,
} from '../src/utils/listeningSteps';
import { resolveQuizRange } from '../src/utils/quizRange';
import { deriveQuizStepState, type QuizStepInput } from '../src/utils/quizStepState';
import type { Problem, SubQuestion } from '../src/types/curriculum';

/** 移す前に Quiz.tsx に書かれていた式（1文字も変えずに書き写したもの） */
function legacy(input: QuizStepInput) {
  const {
    currentQuestion, currentQuestionIndex, stepIndex, showingExplanation,
    rangeStart, rangeEnd, rangeCount, rangePosition,
  } = input;
  const perStep = isPerSubQuestionListening(currentQuestion as Problem);
  const listeningSteps = perStep ? buildListeningSteps(currentQuestion as Problem) : [];
  const safeStepIndex = perStep
    ? Math.min(Math.max(0, stepIndex), Math.max(0, listeningSteps.length - 1))
    : 0;
  const activeStepSubs: SubQuestion[] = perStep
    ? stepSubQuestions(currentQuestion as Problem, listeningSteps[safeStepIndex])
    : [];
  const activeStepSub = perStep ? (activeStepSubs[0] ?? null) : null;
  const isLastStep = !perStep || safeStepIndex >= listeningSteps.length - 1;
  const progressPill = buildProgressPill({
    perStep, steps: listeningSteps, stepIndex: safeStepIndex, rangeCount, rangePosition,
  });
  const canGoPrevious = showingExplanation
    ? false
    : (perStep && safeStepIndex > 0) || currentQuestionIndex > rangeStart;
  const isLastQuestion = currentQuestionIndex >= rangeEnd && isLastStep;
  return {
    perStep, listeningSteps, safeStepIndex, activeStepSubs, activeStepSub,
    isLastStep, progressPill, canGoPrevious, isLastQuestion,
  };
}

describe('deriveQuizStepState は移す前の Quiz.tsx の式と同じ結果を返す', () => {
  it('全教科・全大問・ステップ位置・範囲・解説表示の組み合わせで一致する', () => {
    let checked = 0;
    let perStepSeen = 0;
    for (const subject of SUBJECTS) {
      for (const chapter of getChaptersOfSubject(subject.id)) {
        for (const questions of [chapter.practiceProblems || [], chapter.miniTest || []]) {
          if (questions.length === 0) continue;
          const ranges = [null, { startIndex: 0, endIndex: 0 }, { startIndex: 1, endIndex: questions.length - 1 }];
          for (let qi = 0; qi <= questions.length; qi += 1) { // 範囲外（undefined）も1つ含める
            for (const range of ranges) {
              const r = resolveQuizRange(questions.length, range, qi);
              for (const stepIndex of [-1, 0, 1, 2, 5, 99]) {
                for (const showingExplanation of [false, true]) {
                  const input: QuizStepInput = {
                    currentQuestion: questions[qi], currentQuestionIndex: qi, stepIndex, showingExplanation,
                    rangeStart: r.rangeStart, rangeEnd: r.rangeEnd, rangeCount: r.rangeCount, rangePosition: r.rangePosition,
                  };
                  const now = deriveQuizStepState(input);
                  expect(now).toEqual(legacy(input));
                  if (now.perStep) perStepSeen += 1;
                  checked += 1;
                }
              }
            }
          }
        }
      }
    }
    // 1問ずつモード（リスニング）と通常モードの両方を実際に通っていること
    expect(checked).toBeGreaterThan(1000);
    expect(perStepSeen).toBeGreaterThan(0);
    expect(perStepSeen).toBeLessThan(checked);
  });

  it('範囲の最後の回・最後の問で isLastQuestion が true、先頭では「前へ」を押せない', () => {
    const listening = getChaptersOfSubject('english_listening').find((c) =>
      (c.practiceProblems || []).some((p) => isPerSubQuestionListening(p)));
    expect(listening).toBeDefined();
    const questions = (listening as { practiceProblems: Problem[] }).practiceProblems;
    const last = questions.length - 1;
    const steps = buildListeningSteps(questions[last] as Problem);
    const r = resolveQuizRange(questions.length, null, last);
    const end = deriveQuizStepState({
      currentQuestion: questions[last], currentQuestionIndex: last, stepIndex: steps.length - 1,
      showingExplanation: false, ...r,
    });
    expect(end.isLastQuestion).toBe(true);

    const r0 = resolveQuizRange(questions.length, null, 0);
    const first = deriveQuizStepState({
      currentQuestion: questions[0], currentQuestionIndex: 0, stepIndex: 0, showingExplanation: false, ...r0,
    });
    expect(first.canGoPrevious).toBe(false);
  });
});
