import { expect, it } from 'vitest';
import fs from 'node:fs';
import { emptyProgress, normalizeProgress, equippedStage, unequipKind, canUnequip, ITEMS } from '../src/battle/core/growth';
import { STAGES, stageOf } from '../src/battle/core/tobiraParts';

// 2026-10-30 D7：ホームの背景（宇宙だけだった）をガチャで当てて選べるように
const stages = ITEMS.filter((i) => i.kind === 'stage');

it('ホーム背景はガチャに入っていて、どれも見た目の定義がある', () => {
  expect(stages.length).toBeGreaterThanOrEqual(6);
  for (const s of stages) {
    expect(s.gacha).toBe(true);
    expect(stageOf(s.value!)).not.toBeNull();
  }
  expect(Object.keys(STAGES).length).toBeGreaterThanOrEqual(stages.length);
});

it('持っていて付けている背景だけが反映され、外すと宇宙（空文字）に戻る', () => {
  const s = stages[0];
  const p0 = emptyProgress('u');
  expect(equippedStage(p0)).toBe('');
  // 持っていないのに付けた状態（古いデータなど）は無視
  expect(equippedStage({ ...p0, equipped: { ...p0.equipped, stage: s.id } })).toBe('');
  const p = { ...p0, owned: [...p0.owned, s.id], equipped: { ...p0.equipped, stage: s.id } };
  expect(equippedStage(p)).toBe(s.value);
  expect(canUnequip(p, s)).toBe(true);
  expect(equippedStage(unequipKind(p, 'stage'))).toBe('');
});

it('古い保存データ（stage なし）を読んでも壊れない', () => {
  const p = normalizeProgress('u', { equipped: { pose: 'x' } });
  expect(p.equipped.stage).toBe('');
});

it('CSS に全部の背景の色がある（付けたのに宇宙のまま、を防ぐ）', () => {
  const css = fs.readFileSync('src/styles/home-stage.css', 'utf8');
  for (const s of stages) expect(css).toContain(`[data-stage=${s.value}]`);
});
