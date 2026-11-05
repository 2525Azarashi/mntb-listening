import { describe, expect, it } from 'vitest';
import { bothPicked, chooseLobbyPick, lobbyIdFor, type LobbyPick } from '../src/battle/data/battleLobby';

// F10（2026-11-05）対戦の部屋：2人の希望からどちらかをランダムに選ぶ
const A = 'uid_a', B = 'uid_b';
const pa: LobbyPick = { subject: 'english_vocab', chapterId: '', count: 10, title: '全単元' };
const pb: LobbyPick = { subject: 'english_grammar', chapterId: 'eg1_1', count: 5, title: '時制' };

describe('F10 対戦の部屋の抽選', () => {
  it('2人ともえらぶまでは選ばない', () => {
    expect(chooseLobbyPick({ players: [A, B], picks: {} }, 0.1)).toBeNull();
    expect(chooseLobbyPick({ players: [A, B], picks: { [A]: pa } }, 0.9)).toBeNull();
    expect(bothPicked({ players: [A, B], picks: { [A]: pa } })).toBe(false);
    expect(bothPicked({ players: [A, B], picks: { [A]: pa, [B]: pb } })).toBe(true);
  });
  it('乱数で、どちらかの希望がそのまま選ばれる（だれの希望かも残る）', () => {
    const lobby = { players: [A, B], picks: { [A]: pa, [B]: pb } };
    expect(chooseLobbyPick(lobby, 0.2)).toEqual({ uid: A, ...pa });
    expect(chooseLobbyPick(lobby, 0.7)).toEqual({ uid: B, ...pb });
  });
  it('おおよそ半々（偏らない）', () => {
    const lobby = { players: [A, B], picks: { [A]: pa, [B]: pb } };
    let a = 0;
    for (let i = 0; i < 1000; i += 1) if (chooseLobbyPick(lobby, i / 1000)?.uid === A) a += 1;
    expect(a).toBe(500);
  });
  it('部屋IDは待っていた側の検索IDから決まる', () => {
    expect(lobbyIdFor('abc')).toBe('lb_abc');
  });
});
