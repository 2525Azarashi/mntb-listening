import { describe, expect, it } from 'vitest';
import {
  getChaptersOfSubject,
  miniTestProblemsOf,
} from '../src/data/allChapters';
import type { BattleQuestion } from '../src/battle/core/types';
import {
  exerciseQuestionExplanation,
  loadReviewExplanation,
  subQuestionExplanation,
} from '../src/battle/ui/BattleReviewDetails';

const grammarChapters = getChaptersOfSubject('english_grammar');
const grammarCases = grammarChapters.flatMap((chapter) => {
  const problems = [...(chapter.practiceProblems || []), ...miniTestProblemsOf(chapter)];
  return problems.flatMap((problem) =>
    (problem.subQuestions || []).map((sub, subIndex) => ({
      chapter,
      problem,
      sub,
      subIndex,
    })),
  );
});

function battleQuestionOf({ chapter, problem, sub }: (typeof grammarCases)[number]): BattleQuestion {
  return {
    id: `${chapter.id}:${problem.id}:${sub.id}`,
    subject: 'english_grammar',
    chapterId: chapter.id,
    problemId: problem.id,
    subQuestionId: sub.id,
  } as BattleQuestion;
}

describe('Battle English grammar explanations', () => {
  it('extracts the requested exercise question block without neighboring questions or the set summary', () => {
    const source = [
      '導入',
      '',
      '問1　正解は ②',
      '【ポイント】1問目の詳しい説明。',
      '選択肢の理由。',
      '',
      '問2　正解は ③',
      '【ポイント】2問目の詳しい説明。',
      '',
      '【第1回のまとめ】',
      'まとめは含めない。',
    ].join('\n');

    expect(exerciseQuestionExplanation(source, 2)).toBe('【ポイント】2問目の詳しい説明。');
    expect(exerciseQuestionExplanation(source, 1)).toBe('【ポイント】1問目の詳しい説明。\n選択肢の理由。');
    expect(exerciseQuestionExplanation(source, 3)).toBe('');
  });

  it('uses the matching exercise-side detail for every English grammar practice sub-question', async () => {
    expect(grammarCases.length).toBeGreaterThan(0);
    const results = await Promise.all(grammarCases.map((item) => loadReviewExplanation(battleQuestionOf(item))));

    let detailedBlocks = 0;
    grammarCases.forEach(({ chapter, problem, sub, subIndex }, index) => {
      const exerciseDetail = chapter.id.startsWith('eg')
        ? exerciseQuestionExplanation(problem.explanation, subIndex + 1)
        : '';
      const expected = exerciseDetail || subQuestionExplanation(sub);
      if (exerciseDetail) detailedBlocks += 1;
      const label = `${chapter.id}/${problem.id}/${sub.id}`;
      expect(expected, `${label} must have an exercise explanation`).not.toBe('');
      expect(results[index], `${label} should resolve its own exercise explanation`).toBe(expected);
    });
    expect(detailedBlocks).toBeGreaterThan(0);
  });

  it('shows the full exercise explanation for the reported soccer-game question', async () => {
    const sample = grammarCases.find(({ problem }) =>
      typeof problem.text === 'string' && problem.text.includes('The soccer game last night was very'),
    );
    if (!sample || typeof sample.problem.text !== 'string') {
      throw new Error('Could not find the reported soccer-game question in the exercise bank');
    }

    const promptIndex = sample.problem.text.indexOf('The soccer game last night was very');
    const markers = Array.from(sample.problem.text.slice(0, promptIndex).matchAll(/^問(\d+)[\s　]/gmu));
    const questionNumber = Number(markers[markers.length - 1]?.[1]);
    const sub = sample.problem.subQuestions?.[questionNumber - 1];
    if (!sub) throw new Error('Could not map the reported question to its practice sub-question');

    const detail = await loadReviewExplanation(battleQuestionOf({ ...sample, sub }));
    expect(detail).toContain('着眼点');
    expect(detail).toContain('選択肢');
    expect(detail).toContain('Everyone was excited.');
    expect(detail).toContain('入試ではここ');
  });
});
