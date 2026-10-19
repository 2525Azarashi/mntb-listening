import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { examHeatOf, skyOf } from '../src/components/home/homeTheme';
import { tobiraMood } from '../src/data/tobiraMood';

const read = (p: string) => readFileSync(p, 'utf8');

describe('ホーム v2（2026-10-19）', () => {
  it('空は時間帯で朝・昼・夕・夜に変わる', () => {
    const at = (h: number) => skyOf(new Date(2026, 9, 19, h, 0));
    expect([at(6), at(12), at(17), at(21), at(2)]).toEqual(['morning', 'day', 'evening', 'night', 'night']);
  });
  it('共通テストまでの日数で熱量が上がる（90/30/7日・当日）', () => {
    expect([examHeatOf(120), examHeatOf(90), examHeatOf(30), examHeatOf(7), examHeatOf(0)]).toEqual(['calm', 'd90', 'd30', 'd7', 'today']);
  });
  it('吹き出しは本番が近いと口調が変わる（初回・節目・久しぶりより後、7日前は復習より先）', () => {
    expect(tobiraMood({ screen: 'home', streak: 1, solved: 3, examDays: 20 }).line).toContain('共テまで20日');
    expect(tobiraMood({ screen: 'home', streak: 1, solved: 3, examDays: 5, dueCount: 4 }).line).toContain('本番まであと5日');
    expect(tobiraMood({ screen: 'home', streak: 1, solved: 3, examDays: 20, dueCount: 4 }).line).toContain('4問');
    expect(tobiraMood({ screen: 'home', firstVisit: true, examDays: 5 }).mood).toBe('first');
    expect(tobiraMood({ screen: 'home', streak: 1, solved: 3, examDays: 89 }).line).not.toContain('共テ');
  });
  it('ホームの入口を整理：サイドの4ボタン・使い方・学びの扉はホームに置かない', () => {
    const home = read('src/components/Home.tsx');
    for (const gone of ['stage-shop', 'stage-outfit', 'stage-badges', 'stage-gacha', '>使い方<', 'data-open-philosophy', 'MY TOBIRA']) expect(home).not.toContain(gone);
    expect(home).toContain('マイとびら');
    expect(home).toContain('data-home-practice');
    expect(home).toContain('data-home-battle');
    expect(home).toContain('data-home-review');
  });
  it('統合先：きせかえ・称号・ショップはマイページ、ランキングは対戦、使い方・学びの扉は設定、学習記録は復習ノート', () => {
    const hub = read('src/components/GrowthHub.tsx');
    for (const id of ['outfit', 'badges', 'shop']) expect(hub).toContain(`data-mypage-entry="${id}"`);
    expect(hub).not.toContain('aria-label="部位ごとに着がえる"');
    expect(read('src/battle/ui/BattleHome.tsx')).toContain("onChoose('ranking')");
    const safety = read('src/features/account/AccountSafetySection.tsx');
    expect(safety).toContain('アプリの使い方');
    expect(safety).toContain('学びの扉');
    expect(read('src/components/StudyHub.tsx')).toContain('<StudyRecord');
  });
  it('設定には広告を出さない', async () => {
    const { AD_CONFIG } = await import('../src/ads/adConfig');
    expect(AD_CONFIG.banner.hiddenOn).toContain('settings');
  });
  it('対戦の名前は設定のニックネーム（Google の表示名ではない）', () => {
    const src = read('src/battle/ui/BattleHome.tsx');
    expect(src).toContain('resolveNickname()');
    expect(src).not.toContain('user.displayName');
  });
  it('ガチャの UR は絵文字の王冠を使わない', () => {
    expect(read('src/styles/system.css')).not.toMatch(/[\u{1F451}]/u);
  });
});
