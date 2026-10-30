import { describe, expect, it } from 'vitest';
import { STUDY_CATALOG } from '../src/data/studyCatalog';

describe('TOEIC spotlight card', () => {
  it('presents Part 5 as the first experimental TOEIC offering', () => {
    const card = STUDY_CATALOG.find((subject) => subject.id === 'english')?.contents
      .find((content) => content.id === 'english_toeic');

    expect(card?.title).toBe('TOEIC');
    expect(card?.description).toBe('まずはPart 5を試験導入');
  });
});
