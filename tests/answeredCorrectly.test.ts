import { beforeEach, describe, expect, it } from 'vitest';
import { captureWrongAnswers, isAnsweredCorrectly, loadReviewList, markReviewedCorrect, markReviewedWrong, noteCorrectAnswers, reviewKeyOf } from '../src/utils/reviewList';
import { fixedLaterIds, type StudyLogEntry } from '../src/utils/studyLog';
import { toSyncableReviewItem } from '../src/utils/studySyncCore';

// F9（2026-11-04）：復習ノート・解いた問題で、正解した問題は「正解した」に変わる
const store = new Map<string, string>();
beforeEach(() => {
  store.clear();
  (globalThis as unknown as { localStorage: Storage }).localStorage = {
    getItem: (k: string) => store.get(k) ?? null, setItem: (k: string, v: string) => { store.set(k, String(v)); },
    removeItem: (k: string) => { store.delete(k); }, clear: () => store.clear(), key: () => null, length: 0,
  } as Storage;
});
const wrong = (sub: string) => ({ chapterId: 'c1', questionId: 'q1', subQuestionId: sub, correctAnswer: '1', wrongAnswer: '2' });

describe('復習ノート', () => {
  it('間違えた直後は「正解した」ではない → 演習で正解すると「正解した」・予定は動かない', () => {
    captureWrongAnswers('u', [wrong('s1')]);
    const [before] = loadReviewList('u');
    expect(isAnsweredCorrectly(before)).toBe(false);
    noteCorrectAnswers('u', [reviewKeyOf('c1', 'q1', 's1')]);
    const [after] = loadReviewList('u');
    expect(isAnsweredCorrectly(after)).toBe(true);
    expect(after.box).toBe(before.box);
    expect(after.dueAt).toBe(before.dueAt);
  });
  it('「できた」で正解した・「まだ苦手」や次の誤答で元に戻る', () => {
    captureWrongAnswers('u', [wrong('s1')]);
    const key = reviewKeyOf('c1', 'q1', 's1');
    markReviewedCorrect('u', key);
    expect(isAnsweredCorrectly(loadReviewList('u')[0])).toBe(true);
    markReviewedWrong('u', key);
    expect(isAnsweredCorrectly(loadReviewList('u')[0])).toBe(false);
    noteCorrectAnswers('u', [key]);
    captureWrongAnswers('u', [wrong('s1')]);
    expect(isAnsweredCorrectly(loadReviewList('u')[0])).toBe(false);
  });
  it('ノートにない小問は増やさない・古い記録（lastResult なし）は今までどおり', () => {
    noteCorrectAnswers('u', [reviewKeyOf('c1', 'q1', 'zz')]);
    expect(loadReviewList('u')).toEqual([]);
    expect(isAnsweredCorrectly({})).toBe(false);
  });
  it('同期の形に lastResult が入る', () => {
    captureWrongAnswers('u', [wrong('s1')]);
    noteCorrectAnswers('u', [reviewKeyOf('c1', 'q1', 's1')]);
    expect(toSyncableReviewItem(loadReviewList('u')[0])).toMatchObject({ lastResult: 'correct' });
  });
});

describe('解いた問題（直近3日）', () => {
  const e = (at: number, ok: boolean): StudyLogEntry => ({ key: `k${at}`, kind: 'study', at, chapterId: 'c1', questionId: 'q1', title: 't', items: [{ id: 's1', label: '問1', correct: ok }] });
  it('まちがえたあとの記録で正解していれば「正解した」', () => {
    const fixed = fixedLaterIds([e(2, true), e(1, false)]);
    expect(fixed.has('k1|s1')).toBe(true);
  });
  it('あとで正解していなければそのまま×', () => {
    expect(fixedLaterIds([e(1, false)]).size).toBe(0);
    expect(fixedLaterIds([e(2, false), e(1, true)]).size).toBe(0);
  });
  it('復習ノートで正解した時刻がまちがえた時刻より後なら「正解した」', () => {
    expect(fixedLaterIds([e(1, false)], new Map([['c1::q1::s1', 5]])).has('k1|s1')).toBe(true);
    expect(fixedLaterIds([e(10, false)], new Map([['c1::q1::s1', 5]])).size).toBe(0);
  });
});
