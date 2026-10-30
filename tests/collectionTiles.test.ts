import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

/** B4（2026-10-29）：称号・もっているもの・マイPDF をタイル＋タップで詳細に。種類の選択はアプリ風のチップ */
describe('B4 タイルと詳細の窓', () => {
  const collection = readFileSync('src/components/MyCollection.tsx', 'utf8');
  const badges = readFileSync('src/battle/ui/BattleProfileTabs.tsx', 'utf8');
  it('種類・所有状況はネイティブの select ではなくチップ／切替', () => {
    expect(collection).not.toContain('<select');
    expect(collection).toContain('data-collection-kinds');
    expect(collection).toContain('aria-pressed={kind === id}');
  });
  it('一覧はタイル、押すと詳細の窓（装備・保存はその中）', () => {
    expect(collection).toContain('className="collection-tile"');
    expect(collection).toContain('data-collection-detail');
    expect(collection).toContain('<div className="collection-detail-actions">{actions(detail)}</div>');
  });
  it('称号は1つの一覧で、達成がひと目でわかる（印・色）。押すと詳細', () => {
    expect(badges).toContain('data-badges-tiles');
    expect(badges).toContain('data-earned={got || undefined}');
    expect(badges).toContain("'達成'");
    expect(badges).toContain('data-badge-detail');
    expect(badges).toContain('この称号をつける');
  });
});
