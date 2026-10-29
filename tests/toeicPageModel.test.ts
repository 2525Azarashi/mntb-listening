import { describe, expect, it } from 'vitest';
import { toeicPart5Data } from '../src/data/toeic/toeicPart5Data';
import {
  LONG_CHOICE_CHARS, QUESTIONS_PER_PAGE, countUnanswered, isToeicPageChapter, pageFromStoredStep, pageScoreKey,
  prefersSingleColumn, splitPages, toeicExplanationFor,
} from '../src/components/toeic/toeicPageModel';

/**
 * TOEIC Part 5 の「1ページに複数問・マーク式」演習の計算部分（2026-10-28）
 * 画面の見た目はブラウザで確かめる。ここでは「ページ分け・採点キー・解説の引き当て」が崩れないことを止める。
 */
const problems = toeicPart5Data.parts[0].chapters[0].practiceProblems;

describe('ページ分け', () => {
  it('1ページ6問・30問で5ページ', () => {
    expect(QUESTIONS_PER_PAGE).toBe(6);
    const pages = splitPages(problems[0].subQuestions);
    expect(pages.map((p) => p.length)).toEqual([6, 6, 6, 6, 6]);
  });

  it('端数は最後のページに入る・定数を変えればページ数も変わる', () => {
    expect(splitPages([1, 2, 3, 4, 5, 6, 7], 3).map((p) => p.length)).toEqual([3, 3, 1]);
    expect(splitPages([1, 2, 3], 0).length).toBe(3); // 0以下は1問ずつ扱い（壊れない）
  });

  it('保存したページ位置（ページ先頭の問の番号）からページを戻す。範囲外は丸める', () => {
    expect(pageFromStoredStep(0, 5)).toBe(0);
    expect(pageFromStoredStep(12, 5)).toBe(2);
    expect(pageFromStoredStep(29, 5)).toBe(4);
    expect(pageFromStoredStep(999, 5)).toBe(4);
  });

  it('採点キーは既存と同じ「大問ID::ページ先頭の小問ID」', () => {
    const pages = splitPages(problems[0].subQuestions);
    expect(pageScoreKey(problems[0], pages[1])).toBe(`${problems[0].id}::${pages[1][0].id}`);
  });

  it('未回答数を数える', () => {
    const page = splitPages(problems[0].subQuestions)[0];
    expect(countUnanswered(page, {})).toBe(6);
    expect(countUnanswered(page, { [page[0].id]: '(A)', [page[3].id]: '(C)' })).toBe(4);
  });

  it('TOEIC の単元だけがページ式になる', () => {
    expect(isToeicPageChapter('tp5_1')).toBe(true);
    expect(isToeicPageChapter('el1_A')).toBe(false);
    expect(isToeicPageChapter(undefined)).toBe(false);
  });
});

describe('選択肢の並び', () => {
  it(`いちばん長い選択肢が ${LONG_CHOICE_CHARS} 文字を超える問題だけ1列`, () => {
    expect(prefersSingleColumn(['her', 'she', 'hers', 'herself'])).toBe(false);
    expect(prefersSingleColumn(['will be introduced', 'introduced', 'has introduced', 'introducing'])).toBe(false);
    expect(prefersSingleColumn(['would have arrived', 'will arrive', 'arrives', 'has arrived x long one'])).toBe(true);
  });
});

describe('解説の引き当て（問題データは読むだけ）', () => {
  const all = problems.flatMap((p) => p.subQuestions);

  it('450問すべてで、正解の理由・他の3つの理由・和訳・重要語句が引ける', () => {
    expect(all.length).toBe(450);
    for (const sq of all) {
      const ex = toeicExplanationFor(sq);
      expect(ex, sq.id).not.toBeNull();
      if (!ex) continue;
      expect(ex.sentence).toContain('______');
      expect(ex.completed).not.toContain('______');
      expect(ex.why.length, sq.id).toBeGreaterThan(5);
      expect(ex.translation.length, sq.id).toBeGreaterThan(5);
      expect(ex.keywords.length, sq.id).toBeGreaterThan(0);
      expect(ex.skill).toBe(sq.skill);
      // 画面の選択肢（optionTexts）と解説の選択肢が同じ並び・正解はちょうど1つ
      expect(ex.choices.map((c) => c.text)).toEqual(sq.optionTexts);
      expect(ex.choices.filter((c) => c.correct).map((c) => c.mark)).toEqual([sq.correctAnswer]);
      ex.choices.filter((c) => !c.correct).forEach((c) => expect(c.reason.length, `${sq.id} ${c.mark}`).toBeGreaterThan(3));
    }
  });

  it('想定外のIDでは null（画面は解説を出さずに続ける）', () => {
    expect(toeicExplanationFor({ ...all[0], id: 'unknown' })).toBeNull();
  });
});
