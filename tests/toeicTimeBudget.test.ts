import { describe, expect, it } from 'vitest';
import {
  buildToeicPageBudgets,
  classifyToeicSkill,
  formatToeicBudgetTime,
  TOEIC_TIME_PRESETS,
} from '../src/components/toeic/toeicTimeBudget';

describe('TOEIC Part 5 page time budgets', () => {
  it('calculates target and limit lines from each page composition', () => {
    const pageKinds = [
      ['語彙', '語彙', '品詞', '文法', '文法', '文法'],
      ['語彙', '語彙', '品詞', '文法', '文法', '文法'],
      ['語彙', '語彙', '品詞', '品詞', '文法', '文法'],
      ['語彙', '語彙', '品詞', '文法', '文法', '文法'],
      ['語彙', '語彙', '品詞', '文法', '文法', '文法'],
    ];
    const budgets = buildToeicPageBudgets(pageKinds.map((page) => page.map((skill) => ({ skill }))));

    expect(budgets.map((page) => page.targetSec)).toEqual([104, 104, 100, 104, 104]);
    expect(budgets.map((page) => formatToeicBudgetTime(page.targetRemainingSec))).toEqual(['8:16', '6:32', '4:52', '3:08', '1:24']);
    expect(budgets.map((page) => formatToeicBudgetTime(page.limitRemainingSec))).toEqual(['8:00', '6:00', '4:00', '2:00', '0:00']);
    expect(budgets.reduce((sum, page) => sum + page.counts.語彙, 0)).toBe(10);
    expect(budgets.reduce((sum, page) => sum + page.counts.品詞, 0)).toBe(6);
    expect(budgets.reduce((sum, page) => sum + page.counts.文法, 0)).toBe(14);
  });

  it('treats missing and other existing labels as grammar', () => {
    expect(classifyToeicSkill(undefined)).toBe('文法');
    expect(classifyToeicSkill('未登録の分類')).toBe('文法');
    for (const label of ['動詞の形', '前置詞', '接続詞', '代名詞', '関係詞', '比較']) {
      expect(classifyToeicSkill(label)).toBe('文法');
    }
    expect(classifyToeicSkill('句動詞・コロケーション')).toBe('語彙');
  });

  it('keeps the configured standard rates and labels provisional presets clearly', () => {
    expect(TOEIC_TIME_PRESETS.standard.seconds).toEqual({ 品詞: 8, 文法: 12, 語彙: 30 });
    expect(TOEIC_TIME_PRESETS.standard.label).toContain('800点前後を想定した目安');
    expect(TOEIC_TIME_PRESETS.slow.label).toContain('仮');
    expect(TOEIC_TIME_PRESETS.advanced.label).toContain('仮');
  });
});
