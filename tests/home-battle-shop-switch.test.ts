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
    expect(leaderboard).toContain('とびらバトル');
    expect(leaderboard).toContain('league-top-switch');
    expect(battleHome).not.toContain('>ホームへ</button>');
  });

  // 2026-10-28 A6：どちらの画面でも 左＝とびらバトル・右＝ランキング（切り替えてもボタンが入れ替わらない）
  it('切替ボタンの並びは両画面とも「とびらバトル → ランキング」', () => {
    const order = (src: string, cls: string) => {
      const seg = src.slice(src.indexOf(cls), src.indexOf(cls) + 900);
      return seg.indexOf('とびらバトル') < seg.indexOf('ランキング</button>');
    };
    expect(order(battleHome, 'arena-top-switch')).toBe(true);
    expect(order(leaderboard, 'league-top-switch')).toBe(true);
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
