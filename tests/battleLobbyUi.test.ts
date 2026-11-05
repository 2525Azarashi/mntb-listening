/**
 * F10（2026-11-05）対戦の部屋の画面のつなぎ（ソースの見張り＋単元名の作り方）。
 *   全国対戦 → 教科を決めずにマッチ → 対戦の部屋（2人が単元をえらぶ → どちらかで試合）
 *   → 結果の「対戦の部屋に戻る」で同じ部屋（同じ相手）に戻ってもう1回。
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { lobbyPickTitle, lobbyUnitTitle } from '../src/battle/ui/lobbyPickTitle';

const mode = readFileSync('src/battle/ui/BattleMode.tsx', 'utf8');
const room = readFileSync('src/battle/ui/BattleRoomScreen.tsx', 'utf8');
const lobby = readFileSync('src/battle/ui/BattleLobbyRoom.tsx', 'utf8');
const matching = readFileSync('src/battle/ui/BattleMatching.tsx', 'utf8');
const css = readFileSync('src/battle/ui/battle-lobby-room.css', 'utf8');

describe('F10 対戦の部屋：画面のつなぎ', () => {
  it('全国対戦ボタンは教科選びを飛ばして、対戦の部屋へのマッチに進む', () => {
    expect(mode).toMatch(/case 'national':[\s\S]{0,200}setScreen\('matching'\)/);
    expect(mode).toMatch(/<BattleMatching\s+subject=""\s+lobby/);
    expect(mode).toMatch(/setLobbyId\(id\);[\s\S]{0,60}setScreen\('lobby'\)/);
  });
  it('マッチング画面は対戦の部屋の待機列（findOrEnqueueLobby / watchLobbyCreated）を使う', () => {
    expect(matching).toContain('findOrEnqueueLobby(searchId, controller.signal)');
    expect(matching).toContain('watchLobbyCreated(searchId');
    // 画面を離れたら待機票を消す（従来どおり）
    expect(matching).toMatch(/if \(lobby\) \{[\s\S]*?if \(!doneRef\.current\) void leaveQueue\(searchId\);/);
  });
  it('部屋では各自が単元と問題数をえらび、えらんだ名前を相手にも見せる', () => {
    expect(lobby).toContain('allowQuestionCount');
    expect(lobby).toContain('setLobbyPick(lobbyId, pick)');
    expect(lobby).toContain('title: lobbyPickTitle(subject, chapterId)');
    expect(lobby).toContain('data-lobby-seat="opponent"');
  });
  it('2人ともえらんだら部屋主の端末だけが抽選して試合を作る', () => {
    expect(lobby).toMatch(/if \(!isHost \|\| !ready/);
    expect(lobby).toContain('startLobbyRound(snapshot)');
  });
  it('試合に入る合図は「開いたときより round が進んだこと」（戻った瞬間にさっきの試合へ入り直さない）', () => {
    expect(lobby).toMatch(/lobby\.round <= entryRound\.current/);
    expect(lobby).toMatch(/onEnterRef\.current\(roomId\)/);
  });
  it('部屋を出ると部屋を閉じ、相手には「相手が部屋を出ました」と出る', () => {
    expect(lobby).toContain('void leaveLobby(lobbyId)');
    expect(lobby).toContain('相手が部屋を出ました。');
    expect(mode).toMatch(/const leaveRoom = useCallback\(\(message\?: string\) => \{\s*closeLobby\(\);/);
  });
  it('結果の「対戦の部屋に戻る」は教科選びではなく、同じ対戦の部屋へ戻る', () => {
    expect(room).toMatch(/lobbyOfRoom \? \(\) => onBackToLobby\?\.\(lobbyOfRoom\)/);
    expect(room).toContain("'対戦の部屋に戻る（同じ相手ともう1回）'");
    expect(mode).toMatch(/onBackToLobby=\{\(id\) => \{ setRoomId\(null\); setLobbyId\(id\); setScreen\('lobby'\); \}\}/);
  });
  it('人が見つからず AI プレイヤーになったときも、希望の単元をえらんでから始める', () => {
    expect(mode).toMatch(/onGhostMatch=\{\(g\) => \{[\s\S]{0,120}setScreen\('subject-national'\)/);
  });
  it('部屋の見た目は色トークンだけ（新しい色の直書きなし）・文字は12px以上', () => {
    expect(css).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    for (const m of css.matchAll(/font-size:\s*(\d+)px/g)) expect(Number(m[1])).toBeGreaterThanOrEqual(12);
    expect(lobby).not.toContain('style={{');
  });
});

describe('F10 対戦の部屋：えらんだ単元の名前', () => {
  it('単元を決めていなければ「全単元」', () => {
    expect(lobbyUnitTitle('english_grammar')).toBe('全単元');
    expect(lobbyPickTitle('english_grammar', '')).toMatch(/・全単元$/);
  });
  it('英単語の範囲は「教材名 N〜M語」', () => {
    expect(lobbyUnitTitle('english_vocab', 'vocab:lv1:1:100')).toBe('単語　共通テスト6割〜 1〜100語');
    expect(lobbyPickTitle('english_vocab', 'lv2')).toBe('英単語・英熟語・単語　共通テスト8割〜');
  });
  it('名前は部屋に保存できる長さ（80文字以内）に収める', () => {
    expect(lobbyPickTitle('english_vocab', `x${'あ'.repeat(200)}`).length).toBeLessThanOrEqual(80);
  });
});
