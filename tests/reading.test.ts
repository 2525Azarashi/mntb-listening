import { describe, expect, it } from 'vitest';
import { applyReadingResult, isCleared, READING_LEVELS, READING_PASSAGES, passagesOf, shuffledOptions, splitEvidence, wordCount, type ReadingRecord } from '../src/data/reading';
import { READING_PASSAGE_COUNT } from '../src/data/reading/meta';
import { STUDY_CATALOG } from '../src/data/studyCatalog';
import { SYNC_SECTIONS, sectionField } from '../src/utils/userDataSyncCore';
import { readFileSync } from 'node:fs';

/** 英文解釈の問題データを全問チェックする（2026-10-21） */
describe('英文解釈：問題データ', () => {
  it('題数の表示（meta）が実際の数と一致する', () => {
    expect(READING_PASSAGES.length).toBe(READING_PASSAGE_COUNT);
  });

  it('5レベルすべてに文章があり、どのレベルにも12題以上', () => {
    for (const l of READING_LEVELS) expect(passagesOf(l.level).length, l.name).toBeGreaterThanOrEqual(12);
  });

  it('文章・設問のIDが重複しない（記録のキーになる）', () => {
    const ids = READING_PASSAGES.flatMap(p => [p.id, ...p.questions.map(q => q.id)]);
    expect(new Set(ids).size).toBe(ids.length);
    for (const p of READING_PASSAGES) for (const q of p.questions) expect(q.id.startsWith(p.id + '-'), q.id).toBe(true);
  });

  it('文章の長さはスマホ1画面ほど（レベルが上がるほど長く、最長でも 300 語以内）', () => {
    const range: Record<number, [number, number]> = { 1: [50, 140], 2: [90, 190], 3: [120, 230], 4: [160, 280], 5: [180, 300] };
    for (const p of READING_PASSAGES) {
      const n = wordCount(p.text); const [lo, hi] = range[p.level]!;
      expect(n, `${p.id} ${n}語`).toBeGreaterThanOrEqual(lo);
      expect(n, `${p.id} ${n}語`).toBeLessThanOrEqual(hi);
    }
  });

  it('各設問：選択肢は4つで重複なし・根拠は本文の文字どおり・解説がある', () => {
    for (const p of READING_PASSAGES) {
      expect(p.questions.length, p.id).toBeGreaterThanOrEqual(2);
      for (const q of p.questions) {
        expect(q.options.length).toBe(4);
        expect(new Set(q.options.map(o => o.trim())).size, q.id).toBe(4);
        for (const o of q.options) expect(o.trim().length, q.id).toBeGreaterThan(0);
        expect(p.text.includes(q.evidence), `${q.id} の根拠が本文に無い：${q.evidence}`).toBe(true);
        expect(q.evidence.length, q.id).toBeGreaterThanOrEqual(15);
        expect(q.explanation.length, q.id).toBeGreaterThan(8);
        expect(q.prompt.length, q.id).toBeGreaterThan(5);
      }
    }
  });

  it('出題時の並び：毎回同じで、正解の位置が偏らない', () => {
    const pos = [0, 0, 0, 0];
    for (const p of READING_PASSAGES) for (const q of p.questions) {
      const a = shuffledOptions(q); const b = shuffledOptions(q);
      expect(a).toEqual(b);
      expect(a.options[a.answerIndex]).toBe(q.options[0]);
      expect([...a.options].sort()).toEqual([...q.options].sort());
      pos[a.answerIndex]!++;
    }
    const total = pos.reduce((s, n) => s + n, 0);
    for (const n of pos) expect(n / total).toBeGreaterThan(0.15);
  });

  it('根拠の切り出し', () => {
    expect(splitEvidence('aa BB cc', 'BB')).toEqual({ before: 'aa ', mark: 'BB', after: ' cc' });
    expect(splitEvidence('aa', null)).toEqual({ before: 'aa', mark: '', after: '' });
    expect(splitEvidence('aa', 'zz')).toEqual({ before: 'aa', mark: '', after: '' });
  });
});

describe('英文解釈：記録', () => {
  const p = READING_PASSAGES[0]!;
  const empty: ReadingRecord = { version: 1, best: {}, missed: [] };
  it('最高点は下がらず、間違えた設問は正解すると外れる', () => {
    const r1 = applyReadingResult(empty, p.id, p.questions.map((q, i) => ({ questionId: q.id, correct: i === 0 })), 1);
    expect(r1.best[p.id]).toEqual({ score: 1, total: p.questions.length, at: 1 });
    expect(r1.missed).toEqual(p.questions.slice(1).map(q => q.id));
    const r2 = applyReadingResult(r1, p.id, p.questions.map(q => ({ questionId: q.id, correct: true })), 2);
    expect(isCleared(r2, p)).toBe(true);
    expect(r2.missed).toEqual([]);
    const r3 = applyReadingResult(r2, p.id, p.questions.map(q => ({ questionId: q.id, correct: false })), 3);
    expect(r3.best[p.id]!.score).toBe(p.questions.length);
  });
});

describe('英文解釈：アプリへの組み込み', () => {
  it('学習カタログで「英単語・英熟語」のすぐ下に NEW つきで並ぶ', () => {
    const en = STUDY_CATALOG.find(s => s.id === 'english')!;
    const practice = en.contents.filter(c => c.section !== 'memorize').map(c => c.id);
    expect(practice.indexOf('english_reading')).toBe(practice.indexOf('english_vocab_quiz') + 1);
    const c = en.contents.find(x => x.id === 'english_reading')!;
    expect(c.badge).toBe('NEW');
    expect(c.action).toEqual({ kind: 'reading' });
  });

  it('記録はアカウント同期の対象で、Firestore ルールも s_reading を許可する', () => {
    const s = SYNC_SECTIONS.find(x => x.id === 'reading')!;
    expect(s.keys('u1')).toEqual(['reading_quiz_v1_u1']);
    const merged = s.merge(
      { version: 1, best: { a: { score: 1, total: 2, at: 5 } }, missed: ['a-2', 'x-1'] },
      { version: 1, best: { a: { score: 2, total: 2, at: 1 }, b: { score: 1, total: 3, at: 2 } }, missed: ['a-2'] },
      { version: 1, best: {}, missed: ['a-2', 'x-1'] },
    ) as ReadingRecord;
    expect(merged.best.a!.score).toBe(2);
    expect(merged.best.b!.score).toBe(1);
    expect(merged.missed).toEqual(['a-2']);
    const rules = readFileSync('firestore.rules', 'utf8');
    expect(rules).toContain(`'${sectionField('reading')}'`);
    expect(rules).toContain(`sec(data, 's_reading')`);
  });
});
