/**
 * C9（2026-10-29）：英文法「セットで覚える」。
 * 問題にできなかった仲間の表現を、解説で触れていないものだけ1行で足す。
 */
import { describe, expect, it } from 'vitest';
import { memorizeSetLine } from '../src/data/grammarMemorizeSets';

describe('セットで覚える', () => {
  it('Frankly speaking の問題には、ほかの慣用的な分詞構文を出す（文に出た表現は出さない）', () => {
    const line = memorizeSetLine("Frankly speaking, I don't like his idea very much.", '');
    expect(line).toContain('【セットで覚える】慣用的な分詞構文');
    expect(line).toContain('generally speaking');
    expect(line).toContain('strictly speaking');
    expect(line).not.toContain('frankly speaking');
  });

  it('解説ですでに触れている表現は出さない。全部触れていれば何も足さない', () => {
    const some = memorizeSetLine('As far as I can tell, he is right.', '');
    expect(some).toContain('as long as');
    expect(memorizeSetLine('As far as I can tell, he is right.', 'as long as と区別する')).toBe('');
  });

  it('当てはまらない文には何も足さない', () => {
    expect(memorizeSetLine('My father takes a walk every morning.', '')).toBe('');
    expect(memorizeSetLine('', '')).toBe('');
  });
});
