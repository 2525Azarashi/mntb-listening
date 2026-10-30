import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const battleHome = readFileSync('src/battle/ui/BattleHome.tsx', 'utf8');
const leaderboard = readFileSync('src/components/Leaderboard.tsx', 'utf8');
const gacha = readFileSync('src/components/GachaRoom.tsx', 'utf8');
const collection = readFileSync('src/components/MyCollection.tsx', 'utf8');
const studyCatalog = readFileSync('src/components/StudyCatalog.tsx', 'utf8');

describe('ホーム周辺の切替導線', () => {
  it('対戦ロビーとランキングを上部で切り替えられる', () => {
    expect(battleHome).toContain('とびらバトル');
    expect(battleHome).toContain('ランキング');
    expect(leaderboard).toContain('<BattleRankSwitch current="ranking"');
    expect(battleHome).toContain('<BattleRankSwitch current="battle"');
    expect(battleHome).not.toContain('>ホームへ</button>');
  });

  // 2026-10-29 B5：ガチャの「装飾ガチャ／ショップ」と同じく、切替は両画面で同じ部品（並び・形が変わらない）。ランキングの上に ← は置かない
  it('切替は共通部品で、並びは「とびらバトル → ランキング」・ランキングに ← なし', () => {
    const sw = readFileSync('src/components/BattleRankSwitch.tsx', 'utf8');
    expect(sw.indexOf('とびらバトル</button>')).toBeLessThan(sw.indexOf('ランキング</button>'));
    expect(battleHome).not.toContain('arena-top-switch');
    expect(leaderboard).not.toContain('league-top-switch');
    const rankingBranch = leaderboard.slice(leaderboard.indexOf('{onBattle'), leaderboard.indexOf(': <header className="league-header">'));
    expect(rankingBranch).not.toContain('ArrowLeft');
  });

  // 2026-10-20 30045bd「remove duplicate gacha shop switch」で上部の切替ボタンは重複として撤去した
  // （UI の決まり「同じ操作を1画面に2つ置かない」）。行き来はガチャ説明文のリンクとショップ側の onGacha で残っている
  it('装飾ガチャとショップを行き来でき、重複の切替ボタンは置かない', () => {
    // 2026-10-28 A10：ガチャ画面の説明文は削除（モンスト風のバナーに）。ショップへは上の「装飾ガチャ／ショップ」切替で行く
    expect(readFileSync('src/components/GrowthHub.tsx', 'utf8')).toContain("onPage('gacha-shop')");
    expect(gacha).not.toContain('collection-mode-switch');
    expect(collection).toContain('onGacha');
    expect(collection).not.toContain('collection-mode-switch');
  });

  it('単一科目の演習画面には左上のホーム戻るボタンを置かない', () => {
    expect(studyCatalog).toContain('{!single && <button');
  });
});
