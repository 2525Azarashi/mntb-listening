import { describe, expect, it } from 'vitest';
import { MOCK_BLUEPRINT, PART7_BLUEPRINT, TOEIC_PARTS } from '../src/features/toeic/format';
import { validateMock, validateSet } from '../src/features/toeic/validate';
import { SAMPLE_P2, SAMPLE_P5 } from '../src/features/toeic/samples';
import { TOEIC_STUDY_CONTENTS } from '../src/features/toeic/catalog';
import type { Part5Set, ToeicMockExam } from '../src/features/toeic/types';

describe('TOEIC 拡張の型と構造チェック（2026-10-25）', () => {
  it('本番の形式：L100問・R100問・計200問、問題番号が切れ目なく続く', () => {
    const total = (s: 'listening' | 'reading') => Object.entries(MOCK_BLUEPRINT)
      .filter(([p]) => TOEIC_PARTS[Number(p) as 1].section === s)
      .reduce((n, [, b]) => n + b.questions, 0);
    expect(total('listening')).toBe(100);
    expect(total('reading')).toBe(100);
    const parts = Object.values(TOEIC_PARTS);
    parts.forEach((spec, i) => {
      expect(spec.numbers[1] - spec.numbers[0] + 1).toBe(MOCK_BLUEPRINT[spec.part].questions);
      if (i > 0) expect(spec.numbers[0]).toBe(parts[i - 1].numbers[1] + 1);
    });
    const p7 = PART7_BLUEPRINT.single.questions + PART7_BLUEPRINT.double.questions + PART7_BLUEPRINT.triple.questions;
    expect(p7).toBe(MOCK_BLUEPRINT[7].questions);
  });

  it('見本データは構造チェックを通る', () => {
    expect([...validateSet(SAMPLE_P5), ...validateSet(SAMPLE_P2)]).toEqual([]);
  });

  it('壊れたデータを見つける（正解が選択肢にない・解説が空）', () => {
    const broken: Part5Set = {
      ...SAMPLE_P5,
      questions: [{ ...SAMPLE_P5.questions[0], choices: SAMPLE_P5.questions[0].choices.slice(0, 3), explanation: { reason: ' ' } }],
    };
    const messages = validateSet(broken).map(i => i.message);
    expect(messages.some(m => m.includes('選択肢'))).toBe(true);
    expect(messages.some(m => m.includes('解説が空'))).toBe(true);
  });

  it('模試の構成が本番と違えば知らせる', () => {
    const exam: ToeicMockExam = {
      id: 'toeic-mock-test', title: 'テスト', band: 600,
      setIds: { 1: [], 2: [SAMPLE_P2.id], 3: [], 4: [], 5: [SAMPLE_P5.id], 6: [], 7: [] },
    };
    const lookup = (id: string) => [SAMPLE_P2, SAMPLE_P5].find(s => s.id === id);
    expect(validateMock(exam, lookup).length).toBe(7);
  });

  it('学習カタログ用のカードは NEW 付き・ID が重複しない', () => {
    expect(TOEIC_STUDY_CONTENTS.every(c => c.badge === 'NEW')).toBe(true);
    expect(new Set(TOEIC_STUDY_CONTENTS.map(c => c.id)).size).toBe(TOEIC_STUDY_CONTENTS.length);
  });
});
