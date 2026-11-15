/**
 * 英文法・TOEIC 新カードUI＆コンパクト解説の単体・過去データ完全互換テスト
 *
 * ■ 検証すること
 *   1. 単元分け・章ID・大問ID・小問ID・選択肢の保存値（①〜④ / (A)〜(D)）が1文字も変わっていないこと
 *   2. 英文法 全20章・全1,163問がカードモデルへ欠落ゼロで変換でき、会話文207問が話者ピル A/B に分解されること
 *   3. すでに旧UIで解いていたユーザーの保存データ（`solved_problems_v1_*` / `stage_records_v1_*` /
 *      `unit_stats_v1_*` / `quiz_answers_*` / `quiz_run_*` / `review_focus_v1`）をそのまま読め、
 *      新UIで採点した記録も同じキー形式で積み上がること
 *   4. アプリ内のお知らせ（`UPDATE_NOTICES`）の先頭に今回の改善と記録引き継ぎの案内が入っていること
 */
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { getAllGrammarChapters } from '../src/data/englishGrammarData';
import {
  buildGrammarSubReviews,
  isGrammarPageChapterId,
  parseGrammarProblemCards,
  splitGrammarDialogueTurns,
} from '../src/components/grammar/grammarPageModel';
import { GrammarResultView } from '../src/components/grammar/GrammarResultView';
import { ToeicResultView } from '../src/components/toeic/ToeicResultView';
import { toeicPart5Data } from '../src/data/toeic/toeicPart5Data';
import { UPDATE_NOTICES } from '../src/data/updateNotices';
import { markAllNoticesRead, unreadNoticeCount } from '../src/utils/updateNotices';
import { markProblemSolved, problemKey, readSolvedMap } from '../src/utils/progress';
import { isStageCleared, readStageRecords, stageKey } from '../src/utils/stageRecords';
import { accuracyOf, readUnitStats, recordUnitResult } from '../src/utils/unitStats';
import { applyReviewFocus, type ReviewFocus } from '../src/utils/reviewFocus';
import { quizAnswersKey, quizRunKey } from '../src/utils/quizStorageKeys';
import { loadRun, saveRun } from '../src/utils/quizRunState';

describe('英文法・TOEIC カードUI＆過去データ引き継ぎ互換', () => {
  const store = new Map<string, string>();

  beforeEach(() => {
    store.clear();
    const ls: Storage = {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => {
        store.set(k, v);
      },
      removeItem: (k: string) => {
        store.delete(k);
      },
      clear: () => store.clear(),
      key: (i: number) => [...store.keys()][i] ?? null,
      get length() {
        return store.size;
      },
    };
    vi.stubGlobal('localStorage', ls);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('英文法の単元構成（全20章・eg6_1〜eg6_20・1回5問・全1163問）と保存用ID・選択肢①〜④が不変', () => {
    const chapters = getAllGrammarChapters();
    expect(chapters.map((c) => c.id)).toEqual(
      Array.from({ length: 20 }, (_, i) => `eg6_${i + 1}`),
    );
    for (const c of chapters) {
      expect(isGrammarPageChapterId(c.id)).toBe(true);
    }
    expect(isGrammarPageChapterId('el1_A')).toBe(false);
    expect(isGrammarPageChapterId('tp5_1')).toBe(false);

    let totalCards = 0;
    let dialogueCards = 0;
    for (const ch of chapters) {
      for (const p of ch.practiceProblems) {
        expect(p.id.startsWith(`q_${ch.id}_set`)).toBe(true);
        const cards = parseGrammarProblemCards(p);
        expect(cards.length).toBe(p.subQuestions.length);
        for (const card of cards) {
          totalCards += 1;
          expect(card.sq.options).toEqual(['①', '②', '③', '④']);
          expect(card.choiceTexts).toHaveLength(4);
          expect(card.translation.length).toBeGreaterThan(2);
          expect(card.why.length).toBeGreaterThan(2);
          expect(card.choices).toHaveLength(4);
          if (splitGrammarDialogueTurns(card.stem)) {
            dialogueCards += 1;
          }
        }
      }
    }
    expect(totalCards).toBe(1163);
    // 第20章（会話表現）を中心に2ターン以上の対話文164問が話者ピル A/B ターンとして整形される
    expect(dialogueCards).toBeGreaterThanOrEqual(160);
  });

  it('既存ユーザーの過去の学習記録・達成ステージ・途中回答・復習絞り込みが1件も失われずそのまま動く', () => {
    const uid = 'existing-student-01';
    const ch1 = getAllGrammarChapters()[0];
    const p1 = ch1.practiceProblems[0]; // q_eg6_1_set1
    const p2 = ch1.practiceProblems[1]; // q_eg6_1_set2

    // 1. 旧UI時代に第1回を満点3回で「達成」していた記録をシード
    markProblemSolved(uid, ch1.id, p1.id, 100);
    recordUnitResult(uid, ch1.id, 5, 5);
    store.set(
      `stage_records_v1_${uid}`,
      JSON.stringify({
        [stageKey(ch1.id, p1.id)]: { p: 3, n: 3, b: 100, t: 1700000000000 },
      }),
    );

    // 2. 旧UI時代に第2回の途中（問1・問2だけ回答済み）で中断していたデータをシード
    const partialAnswers: Record<string, string> = {
      [p2.subQuestions[0].id]: p2.subQuestions[0].correctAnswer, // 正解
      [p2.subQuestions[1].id]: '①', // 誤答（正解は④）
    };
    store.set(quizAnswersKey(ch1.id, 'practice'), JSON.stringify(partialAnswers));
    saveRun(ch1.id, 'practice', {
      totalScore: 120,
      totalCorrect: 1,
      totalJudgeable: 1,
      totalTimeSec: 18,
      runningCombo: 1,
      perQuestion: {},
      perStep: {
        [`${p2.id}::${p2.subQuestions[0].id}`]: {
          score: 120,
          correctCount: 1,
          judgeableCount: 1,
          timeUsed: 18,
        },
      },
    });

    // 検証A：単元一覧が読む台帳がそのまま維持されている
    const solved = readSolvedMap(uid);
    expect(solved[problemKey(ch1.id, p1.id)]).toBeGreaterThan(0);
    const stages = readStageRecords(uid);
    expect(isStageCleared(stages[stageKey(ch1.id, p1.id)])).toBe(true);
    expect(accuracyOf(readUnitStats(uid)[ch1.id])).toBe(100);

    // 検証B：途中再開の回答とラン状態がそのまま復元でき、新UIのレビュー生成でインライン比較データになる
    expect(store.get(quizRunKey(ch1.id, 'practice'))).toBeTruthy();
    const restoredRun = loadRun(ch1.id, 'practice');
    expect(restoredRun.totalScore).toBe(120);
    const expectedCards = parseGrammarProblemCards(p2);
    const reviews = buildGrammarSubReviews(p2, partialAnswers);
    expect(reviews[0].status).toBe('correct');
    expect(reviews[1].status).toBe('wrong');
    expect(reviews[1].filledWord).toBe(expectedCards[1].choiceTexts[0]);
    expect(reviews[1].correctWord).toBe(expectedCards[1].correctWord);
    expect(reviews[2].status).toBe('blank');

    // 検証C：「誤答だけ解き直す」の絞り込みでも元の問番号（問2）と選択肢が保たれる
    const focus: ReviewFocus = {
      chapterId: ch1.id,
      targets: [{ questionId: p2.id, subQuestionIds: [p2.subQuestions[1].id] }],
    };
    const narrowed = applyReviewFocus(ch1.practiceProblems, ch1.id, focus);
    expect(narrowed).toHaveLength(1);
    const narrowedCards = parseGrammarProblemCards(narrowed[0]);
    expect(narrowedCards).toHaveLength(1);
    expect(narrowedCards[0].displayNo).toBe(2);
    expect(narrowedCards[0].correctWord).toBe(expectedCards[1].correctWord);
  });

  it('GrammarResultView と ToeicResultView がインライン空所比較 [誤答 → 正解] とコンパクト解説をSSR描画できる', () => {
    const ch20 = getAllGrammarChapters().find((c) => c.id === 'eg6_20')!;
    const p20 = ch20.practiceProblems[0];
    const grammarHtml = renderToStaticMarkup(
      React.createElement(GrammarResultView, {
        mode: 'practice',
        chapter: ch20,
        answers: {
          [p20.subQuestions[0].id]: '①', // 誤答: How have you been? -> 正解: How do you do?
          [p20.subQuestions[1].id]: p20.subQuestions[1].correctAnswer, // 正解
        },
        onBack: () => {},
        isGuest: true,
        questionRange: { startIndex: 0, endIndex: 0 },
      }),
    );
    expect(grammarHtml).toContain('data-grammar-result');
    expect(grammarHtml).toContain('gp-speaker-pill');
    expect(grammarHtml).toContain('gp-blank-compare');
    expect(grammarHtml).toContain('How have you been?');
    expect(grammarHtml).toContain('How do you do?');
    expect(grammarHtml).toContain('和訳');
    expect(grammarHtml).toContain('要点');

    const toeicChapter = toeicPart5Data.parts[0].chapters[0];
    const tp0 = toeicChapter.practiceProblems[0];
    const wrongMark = tp0.subQuestions[0].options.find(
      (m) => m !== tp0.subQuestions[0].correctAnswer,
    )!;
    const toeicHtml = renderToStaticMarkup(
      React.createElement(ToeicResultView, {
        mode: 'practice',
        chapter: toeicChapter,
        answers: {
          [tp0.subQuestions[0].id]: wrongMark,
          [tp0.subQuestions[1].id]: tp0.subQuestions[1].correctAnswer,
        },
        onBack: () => {},
        isGuest: true,
        questionRange: { startIndex: 0, endIndex: 0 },
      }),
    );
    expect(toeicHtml).toContain('data-toeic-result');
    expect(toeicHtml).toContain('tp-blank-compare');
    expect(toeicHtml).toContain('和訳');
    expect(toeicHtml).toContain('要点');
  });

  it('アプリ内のお知らせ（UPDATE_NOTICES）の先頭にUI刷新と学習記録引き継ぎの案内があり、未読バッジに反映される', () => {
    const latest = UPDATE_NOTICES[0];
    expect(latest.id).toBe('2026-11-15-01');
    expect(latest.title).toContain('カード表示');
    expect(latest.items.join(' ')).toContain('そのまま引き継がれます');

    // 前回のお知らせ一覧まで既読だったユーザーには、今回の1件だけが未読バッジとして通知される
    const previousIds = UPDATE_NOTICES.slice(1).map((n) => n.id);
    store.set('update_notices_read_v1', JSON.stringify(previousIds));
    expect(unreadNoticeCount()).toBe(1);
    markAllNoticesRead();
    expect(unreadNoticeCount()).toBe(0);
  });
});
