/**
 * 章の満点で称号（C12・2026-10-29）。
 * - 称号の一覧（battle/core/chapterTitles.ts）が英文法の教科データの章と1対1でずれていない
 * - 「全部の回で満点をとったことがある」の判定
 * - 称号はバッジの一覧に入っていて、進捗から勝手に付かない（演習の結果でだけ付く）
 */
import { describe, expect, it } from 'vitest';
import { getChaptersOfSubject } from '../src/data/allChapters';
import { CHAPTER_TITLES, chapterTitleBadgeId, chapterTitleOf } from '../src/battle/core/chapterTitles';
import { BADGES, emptyProgress, evaluateBadges } from '../src/battle/core/growth';
import { isChapterAllPerfect } from '../src/utils/chapterTitleAward';
import { stageKey } from '../src/utils/stageRecords';

describe('章の称号', () => {
  it('英文法の全章ぶんあり、章ID・章名が教科データと一致する', () => {
    const chapters = getChaptersOfSubject('english_grammar');
    expect(CHAPTER_TITLES.map((t) => t.chapterId)).toEqual(chapters.map((c) => c.id));
    for (const c of chapters) expect(chapterTitleOf(c.id)?.chapterTitle).toBe(c.abstractTitle);
  });

  it('称号はバッジの一覧に入っていて、進捗からは勝手に付かない', () => {
    for (const t of CHAPTER_TITLES) expect(BADGES.some((b) => b.id === chapterTitleBadgeId(t.chapterId))).toBe(true);
    const ids = new Set(evaluateBadges(emptyProgress('u')));
    for (const t of CHAPTER_TITLES) expect(ids.has(chapterTitleBadgeId(t.chapterId))).toBe(false);
  });

  it('全部の回で最高 100% のときだけ「満点そろった」', () => {
    const qs = ['q1', 'q2', 'q3'];
    const rec = (b: number) => ({ p: b === 100 ? 1 : 0, n: 1, b, t: 0 });
    const all = Object.fromEntries(qs.map((q) => [stageKey('eg6_1', q), rec(100)]));
    expect(isChapterAllPerfect(all, 'eg6_1', qs)).toBe(true);
    expect(isChapterAllPerfect({ ...all, [stageKey('eg6_1', 'q2')]: rec(80) }, 'eg6_1', qs)).toBe(false);
    const missing = { ...all }; delete missing[stageKey('eg6_1', 'q3')];
    expect(isChapterAllPerfect(missing, 'eg6_1', qs)).toBe(false);
    expect(isChapterAllPerfect(all, 'eg6_1', [])).toBe(false);
  });
});
