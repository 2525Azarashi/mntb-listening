import { describe, expect, it } from 'vitest';
import { TOEIC_P5_ROUNDS } from '../src/data/toeic/toeicPart5Rounds';
import { answerPositions, TOEIC_MARKS, TOEIC_P5_QUESTIONS_PER_ROUND, type ToeicP5Item } from '../src/data/toeic/toeicPart5Kit';
import { toeicPart5Data } from '../src/data/toeic/toeicPart5Data';
import { optionCircledMark } from '../src/utils/questionDisplay';

/**
 * TOEIC Part 5 の問題データの検査（2026-10-28）
 * 中身の英語の正しさは人が確かめる。ここでは「形が壊れていない」「偏っていない」を機械で止める。
 */
const all: { round: number; no: number; item: ToeicP5Item }[] = TOEIC_P5_ROUNDS.flatMap((items, r) =>
  items.map((item, i) => ({ round: r + 1, no: i + 1, item })));
const tag = (x: { round: number; no: number }) => `第${x.round}回 問${x.no}`;

describe('TOEIC Part 5：1問ずつの形', () => {
  it('各回30問', () => {
    TOEIC_P5_ROUNDS.forEach((items, r) => expect(items.length, `第${r + 1}回`).toBe(TOEIC_P5_QUESTIONS_PER_ROUND));
  });

  it('空所 ______ がちょうど1つ・選択肢4つが互いに違う・正解は誤答に含まれない', () => {
    for (const x of all) {
      const { s, c, w } = x.item;
      expect(s.split('______').length - 1, tag(x)).toBe(1);
      const choices = [c, ...w.map(([t]) => t)];
      expect(new Set(choices.map((t) => t.toLowerCase())).size, tag(x)).toBe(4);
      choices.forEach((t) => expect(t.trim(), tag(x)).toBe(t));
    }
  });

  it('解説がそろっている（正解の理由・誤答3つそれぞれの理由・和訳・重要語句）', () => {
    for (const x of all) {
      const { why, w, tr, kw } = x.item;
      expect(why.length, tag(x)).toBeGreaterThan(10);
      w.forEach(([, reason]) => expect(reason.length, tag(x)).toBeGreaterThan(5));
      expect(tr.length, tag(x)).toBeGreaterThan(8);
      expect(kw.length, tag(x)).toBeGreaterThan(0);
    }
  });

  it('問題文は自然な長さ（8〜30語）で、文末が句読点', () => {
    for (const x of all) {
      const words = x.item.s.split(/\s+/).filter(Boolean).length;
      expect(words, tag(x)).toBeGreaterThanOrEqual(8);
      expect(words, tag(x)).toBeLessThanOrEqual(30);
      expect(/[.?!]$/.test(x.item.s), tag(x)).toBe(true);
    }
  });

  it('米国式表記（英国式の綴りが混ざっていない）', () => {
    const british = /\b(colour|favour|honour|labour|centre|theatre|organis|realis|recognis|apologis|analys(e|ing)\b|cancelled|travelled|licence|catalogue|programme|cheque|enrol\b|behaviour|neighbour)/i;
    for (const x of all) {
      const text = [x.item.s, x.item.c, ...x.item.w.map(([t]) => t)].join(' ');
      expect(british.test(text), tag(x)).toBe(false);
    }
  });
});

describe('TOEIC Part 5：回ごと・全体の偏り', () => {
  it('正解の位置は各回で A〜D がそれぞれ6〜9回、同じ位置が3問続かない', () => {
    TOEIC_P5_ROUNDS.forEach((items, r) => {
      const pos = answerPositions(r + 1, items.length);
      const counts = [0, 1, 2, 3].map((p) => pos.filter((v) => v === p).length);
      counts.forEach((n) => { expect(n, `第${r + 1}回`).toBeGreaterThanOrEqual(6); expect(n, `第${r + 1}回`).toBeLessThanOrEqual(9); });
      expect(pos.some((v, i) => i >= 2 && v === pos[i - 1] && v === pos[i - 2]), `第${r + 1}回`).toBe(false);
    });
  });

  it('組み立てた結果の正解マークと、データの正解が一致する', () => {
    const problems = toeicPart5Data.parts[0].chapters[0].practiceProblems;
    expect(problems.length).toBe(TOEIC_P5_ROUNDS.length);
    problems.forEach((p, r) => p.subQuestions.forEach((sq, i) => {
      const idx = TOEIC_MARKS.indexOf(sq.correctAnswer as (typeof TOEIC_MARKS)[number]);
      expect(sq.optionTexts?.[idx], `第${r + 1}回 問${i + 1}`).toBe(TOEIC_P5_ROUNDS[r][i].c);
    }));
  });

  it('各回の分野配分（語彙＋句動詞 8〜12・品詞 5〜8・残りは文法）と難易度（易・中・難がすべて入る）', () => {
    TOEIC_P5_ROUNDS.forEach((items, r) => {
      const vocab = items.filter((x) => x.k === '語彙' || x.k === '句動詞・コロケーション').length;
      const pos = items.filter((x) => x.k === '品詞').length;
      expect(vocab, `第${r + 1}回 語彙`).toBeGreaterThanOrEqual(8);
      expect(vocab, `第${r + 1}回 語彙`).toBeLessThanOrEqual(12);
      expect(pos, `第${r + 1}回 品詞`).toBeGreaterThanOrEqual(5);
      expect(pos, `第${r + 1}回 品詞`).toBeLessThanOrEqual(8);
      [1, 2, 3].forEach((d) => expect(items.some((x) => x.d === d), `第${r + 1}回 難易度${d}`).toBe(true));
    });
  });

  it('同じ英文が2回出ない・同じ正解語が全体で3回以上出ない', () => {
    const sentences = new Set<string>();
    const answers = new Map<string, string[]>();
    for (const x of all) {
      const key = x.item.s.toLowerCase();
      expect(sentences.has(key), tag(x)).toBe(false);
      sentences.add(key);
      const a = x.item.c.toLowerCase();
      answers.set(a, [...(answers.get(a) || []), tag(x)]);
    }
    const over = [...answers.entries()].filter(([, at]) => at.length >= 3).map(([a, at]) => `${a}: ${at.join('、')}`);
    expect(over).toEqual([]);
  });

  it('(A)〜(D) の選択肢には丸数字を重ねない（解説で「①(A)」にならない）', () => {
    TOEIC_MARKS.forEach((m, i) => expect(optionCircledMark(m, i)).toBe(''));
    // 既存の教科（丸数字なしの選択肢）には今までどおり付く
    expect(optionCircledMark('NaCl', 0)).toBe('①');
  });
});
