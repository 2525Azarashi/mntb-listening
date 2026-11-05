import { describe, expect, it } from 'vitest';
import { questionInScope, vocabScope } from '../src/battle/core/vocabRanges';
import type { BattleQuestion } from '../src/battle/core/types';

const question = (subject: string, chapterId: string, subQuestionId: string): BattleQuestion =>
  ({ subject, chapterId, subQuestionId } as unknown as BattleQuestion);

describe('AI battle selected-unit scope', () => {
  it('a normal unit contains only questions from the selected chapter', () => {
    const selected = question('english_grammar', 'eg1_1', '1');
    const another = question('english_grammar', 'eg1_2', '2');
    expect(questionInScope(selected, 'eg1_1')).toBe(true);
    expect(questionInScope(another, 'eg1_1')).toBe(false);
  });

  it('a vocabulary range contains only the selected book and inclusive word range', () => {
    const first = question('english_vocab', 'booka', '1');
    const last = question('english_vocab', 'booka', '50');
    const outsideRange = question('english_vocab', 'booka', '51');
    const anotherBook = question('english_vocab', 'bookb', '25');
    const scope = vocabScope('booka', 1, 50);
    expect(questionInScope(first, scope)).toBe(true);
    expect(questionInScope(last, scope)).toBe(true);
    expect(questionInScope(outsideRange, scope)).toBe(false);
    expect(questionInScope(anotherBook, scope)).toBe(false);
  });
});
