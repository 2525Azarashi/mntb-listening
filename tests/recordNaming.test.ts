import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

/**
 * 「記録」の言葉の住み分け（2026-10-28 ご要望：ホームの復習・記録とマイページの記録が混ざる）
 *   ホーム「復習」  … まちがえた問題を解きなおす（復習ノート／解いた問題 3日分）
 *   マイページ「カレンダー」… 勉強カレンダー（2026-10-29 B9：「記録」から改名。日付を押して最大7日をグラフで比べる）
 */
const home = readFileSync('src/components/Home.tsx', 'utf8');
const hub = readFileSync('src/components/StudyHub.tsx', 'utf8');
const rec = readFileSync('src/components/StudyRecord.tsx', 'utf8');
const growth = readFileSync('src/components/GrowthHub.tsx', 'utf8');

describe('「記録」はマイページだけ・ホームは「復習」', () => {
  it('ホームの入口は「復習」（記録の字を使わない）', () => {
    expect(home).toContain('<strong>復習</strong>');
    expect(home).not.toContain('<strong>復習・記録</strong>');
  });
  it('復習の画面の見出しは「復習」、切替は「復習ノート／解いた問題」', () => {
    expect(hub).toContain('<KineticText text="復習" />');
    expect(hub).toContain('解いた問題<small>3日分</small>');
    expect(hub).not.toContain('学習記録<small>');
    expect(rec).toContain('<KineticText text="解いた問題" />');
  });
  it('マイページのタブは「カレンダー」（B9：「記録」から改名・アイコンつき）', () => {
    expect(growth).toContain("['log','カレンダー',CalendarDays]");
    expect(growth).not.toContain("['log','記録'");
  });
});
