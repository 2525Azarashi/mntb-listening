/**
 * F10（2026-11-05）対戦の部屋（battle_lobbies）と、部屋から始める試合（battle_rooms の mode:'lobby'）のルールテスト。
 *   全国対戦でマッチした2人が部屋に入り、それぞれ単元をえらぶ → 部屋主がどちらかをランダムに選んで試合を作る
 *   → 終わったら同じ部屋に戻って再戦。
 * 実行： npm run test:rules
 */
import { afterAll, beforeAll, beforeEach, describe, it } from 'vitest';
import { assertFails, assertSucceeds, initializeTestEnvironment, type RulesTestEnvironment } from '@firebase/rules-unit-testing';
import { deleteField, deleteDoc, doc, getDoc, serverTimestamp, setDoc, updateDoc, writeBatch } from 'firebase/firestore';
import { mergedRules } from './helpers/battleRules';

const HOST = 'uid_host';
const GUEST = 'uid_guest';
const OUTSIDER = 'uid_outsider';
const SESSION = 'sess-guest-1';
const LOBBY = `lb_${SESSION}`;
const ROOM = 'room_lobby_1';
const SUBJECT = 'english_vocab';
const OTHER_SUBJECT = 'english_grammar';
const FRIEND_LOBBY = 'friend_lobby_test';
const FRIEND_CODE = 'ABCD';

let testEnv: RulesTestEnvironment;
const dbCache = new Map<string, ReturnType<RulesTestEnvironment['authenticatedContext']>>();
const ctxFor = (uid: string) => {
  let c = dbCache.get(uid);
  if (!c) { c = testEnv.authenticatedContext(uid); dbCache.set(uid, c); }
  return c.firestore();
};

beforeAll(async () => {
  testEnv = await initializeTestEnvironment({ projectId: 'mntb-lobby-rules-test', firestore: { rules: mergedRules(), host: '127.0.0.1', port: 8080 } });
});
afterAll(async () => { await testEnv?.cleanup(); });
beforeEach(async () => { await testEnv.clearFirestore(); });

async function seed(path: [string, string], data: Record<string, unknown>) {
  await testEnv.withSecurityRulesDisabled(async (ctx) => { await setDoc(doc(ctx.firestore(), ...path), data); });
}
const profile = (uid: string) => ({ uid, nickname: uid, photoURL: '', rating: 1500 });
const ticket = (uid: string, session: string) => ({ uid, subject: 'lobby:v1', profile: { ...profile(uid), matchSessionId: session }, createdAt: new Date() });
const lobbyPayload = (over: Record<string, unknown> = {}) => ({
  id: LOBBY, status: 'open', players: [HOST, GUEST],
  profiles: { [HOST]: profile(HOST), [GUEST]: profile(GUEST) },
  picks: {}, round: 0, roomId: '', chosen: null,
  createdAt: serverTimestamp(), updatedAt: serverTimestamp(), ...over,
});
const pick = (subject = SUBJECT, over: Record<string, unknown> = {}) => ({ subject, chapterId: '', count: 10, title: '全単元', ...over });
const friendLobbyPayload = (over: Record<string, unknown> = {}) => ({
  id: FRIEND_LOBBY, status: 'open', kind: 'friend', hostUid: HOST, joinCode: FRIEND_CODE,
  players: [HOST], profiles: { [HOST]: profile(HOST) }, picks: {}, round: 0, roomId: '', chosen: null,
  createdAt: new Date(), updatedAt: new Date(), ...over,
});
const friendCodePayload = (over: Record<string, unknown> = {}) => ({
  lobbyId: FRIEND_LOBBY, kind: 'friend_lobby', hostUid: HOST, subject: 'lobby:v1', createdAt: new Date(), ...over,
});
async function seedFriendPair(a = HOST, b = GUEST) {
  await testEnv.withSecurityRulesDisabled(async (ctx) => {
    const db = ctx.firestore();
    await Promise.all([
      setDoc(doc(db, 'friends', a, 'items', b), { uid: b, nickname: b, photoURL: '', addedAt: new Date() }),
      setDoc(doc(db, 'friends', b, 'items', a), { uid: a, nickname: a, photoURL: '', addedAt: new Date() }),
    ]);
  });
}
const seededLobby = (over: Record<string, unknown> = {}) => ({ ...lobbyPayload(), createdAt: new Date(), updatedAt: new Date(), ...over });
const roomPayload = (over: Record<string, unknown> = {}) => ({
  id: ROOM, status: 'waiting', mode: 'lobby', subject: SUBJECT, joinCode: '', hostUid: HOST,
  players: [HOST, GUEST], profiles: { [HOST]: profile(HOST), [GUEST]: profile(GUEST) },
  questionIds: ['q1', 'q2', 'q3', 'q4', 'q5'],
  rules: { questionCount: 5, pointsCorrect: 60, pointsSpeedMax: 240, pointsStreak: 5 },
  currentIndex: 0, deadlineAt: null, answers: { [HOST]: {}, [GUEST]: {} }, attest: {},
  lobbyId: LOBBY, lobbyRound: 1, createdAt: serverTimestamp(), updatedAt: serverTimestamp(), ...over,
});
const chosen = (uid = GUEST, subject = SUBJECT) => ({ uid, subject, chapterId: '', count: 10, title: '全単元' });
function startBatch(uid: string, room: Record<string, unknown> = roomPayload(), lobbyUpd: Record<string, unknown> = {}) {
  const db = ctxFor(uid);
  const b = writeBatch(db);
  b.set(doc(db, 'battle_rooms', ROOM), room);
  b.update(doc(db, 'battle_lobbies', LOBBY), { round: 1, picks: {}, roomId: ROOM, chosen: chosen(), updatedAt: serverTimestamp(), ...lobbyUpd });
  return b.commit();
}

describe('battle_lobbies — 部屋を作る（マッチ）', () => {
  it('★並んでいない相手を入れた部屋は作れない★', async () => {
    await assertFails(setDoc(doc(ctxFor(HOST), 'battle_lobbies', LOBBY), lobbyPayload()));
  });
  it('相手の票を同じ書き込みで消せば作れる（部屋IDは lb_＋相手の検索ID）', async () => {
    await seed(['battle_queue', GUEST], ticket(GUEST, SESSION));
    await seed(['battle_queue', HOST], ticket(HOST, 'sess-host'));
    const db = ctxFor(HOST);
    const b = writeBatch(db);
    b.delete(doc(db, 'battle_queue', HOST));
    b.delete(doc(db, 'battle_queue', GUEST));
    b.set(doc(db, 'battle_lobbies', LOBBY), lobbyPayload());
    await assertSucceeds(b.commit());
  });
  it('★部屋IDが相手の検索IDと違うと作れない★', async () => {
    await seed(['battle_queue', GUEST], ticket(GUEST, SESSION));
    const db = ctxFor(HOST);
    const b = writeBatch(db);
    b.delete(doc(db, 'battle_queue', GUEST));
    b.set(doc(db, 'battle_lobbies', 'lb_other'), lobbyPayload({ id: 'lb_other' }));
    await assertFails(b.commit());
  });
  it('★全国対戦（教科つき）の票では作れない★', async () => {
    await seed(['battle_queue', GUEST], { ...ticket(GUEST, SESSION), subject: `${SUBJECT}:speed2` });
    const db = ctxFor(HOST);
    const b = writeBatch(db);
    b.delete(doc(db, 'battle_queue', GUEST));
    b.set(doc(db, 'battle_lobbies', LOBBY), lobbyPayload());
    await assertFails(b.commit());
  });
});

describe('battle_lobbies — 読む', () => {
  it('2人は読める・第三者は読めない・まだ無い部屋は待つために読める', async () => {
    await assertSucceeds(getDoc(doc(ctxFor(GUEST), 'battle_lobbies', LOBBY)));
    await seed(['battle_lobbies', LOBBY], seededLobby());
    await assertSucceeds(getDoc(doc(ctxFor(HOST), 'battle_lobbies', LOBBY)));
    await assertSucceeds(getDoc(doc(ctxFor(GUEST), 'battle_lobbies', LOBBY)));
    await assertFails(getDoc(doc(ctxFor(OUTSIDER), 'battle_lobbies', LOBBY)));
  });
});

describe('battle_lobbies — 単元をえらぶ', () => {
  beforeEach(async () => { await seed(['battle_lobbies', LOBBY], seededLobby()); });
  it('自分の単元はえらべる・えらび直せる・取り消せる', async () => {
    const ref = doc(ctxFor(GUEST), 'battle_lobbies', LOBBY);
    await assertSucceeds(updateDoc(ref, { [`picks.${GUEST}`]: pick(), updatedAt: serverTimestamp() }));
    await assertSucceeds(updateDoc(ref, { [`picks.${GUEST}`]: pick(OTHER_SUBJECT, { chapterId: 'eg1_1', title: '時制' }), updatedAt: serverTimestamp() }));
    await assertSucceeds(updateDoc(ref, { [`picks.${GUEST}`]: deleteField(), updatedAt: serverTimestamp() }));
  });
  it('★相手の単元は書き換えられない★', async () => {
    await assertFails(updateDoc(doc(ctxFor(GUEST), 'battle_lobbies', LOBBY), { [`picks.${HOST}`]: pick(), updatedAt: serverTimestamp() }));
  });
  it('★変な問題数・余計な項目は入れられない★', async () => {
    const ref = doc(ctxFor(GUEST), 'battle_lobbies', LOBBY);
    await assertFails(updateDoc(ref, { [`picks.${GUEST}`]: pick(SUBJECT, { count: 20 }), updatedAt: serverTimestamp() }));
    await assertFails(updateDoc(ref, { [`picks.${GUEST}`]: { ...pick(), extra: 1 }, updatedAt: serverTimestamp() }));
  });
  it('★第三者はえらべない★', async () => {
    await assertFails(updateDoc(doc(ctxFor(OUTSIDER), 'battle_lobbies', LOBBY), { [`picks.${OUTSIDER}`]: pick(), updatedAt: serverTimestamp() }));
  });
});

describe('battle_lobbies — 試合を始める（部屋主が2人の単元からどちらかを選ぶ）', () => {
  const bothPicked = () => seededLobby({ picks: { [HOST]: pick(OTHER_SUBJECT), [GUEST]: pick(SUBJECT) } });
  it('2人ともえらんでいれば、部屋主は試合を作って部屋を次の回に進められる', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertSucceeds(startBatch(HOST));
  });
  it('部屋主の単元が選ばれた場合も始められる', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertSucceeds(startBatch(HOST, roomPayload({ subject: OTHER_SUBJECT }), { chosen: chosen(HOST, OTHER_SUBJECT) }));
  });
  it('★抽選結果の単元・問題数・名前を選択内容からすり替えられない★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertFails(startBatch(HOST, roomPayload(), { chosen: { ...chosen(), chapterId: 'other_chapter' } }));
    await assertFails(startBatch(HOST, roomPayload(), { chosen: { ...chosen(), count: 5 } }));
    await assertFails(startBatch(HOST, roomPayload(), { chosen: { ...chosen(), title: '別の単元' } }));
  });
  it('★2人のどちらもえらんでいない教科では始められない★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertFails(startBatch(HOST, roomPayload({ subject: 'math_1a' }), { chosen: chosen(GUEST, 'math_1a') }));
  });
  it('★片方しかえらんでいないと始められない★', async () => {
    await seed(['battle_lobbies', LOBBY], seededLobby({ picks: { [GUEST]: pick() } }));
    await assertFails(startBatch(HOST));
  });
  it('★相手（部屋主でない人）は始められない★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    const room = roomPayload({ hostUid: GUEST, players: [GUEST, HOST] });
    await assertFails(startBatch(GUEST, room));
  });
  it('★部屋を進めずに試合だけ作ることはできない（試合を何度も作れない）★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertFails(setDoc(doc(ctxFor(HOST), 'battle_rooms', ROOM), roomPayload()));
  });
  it('★何戦目かがずれていると始められない★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertFails(startBatch(HOST, roomPayload({ lobbyRound: 2 }), { round: 2 }));
  });
  it('★部屋の外の人を入れた試合は作れない★', async () => {
    await seed(['battle_lobbies', LOBBY], bothPicked());
    await assertFails(startBatch(HOST, roomPayload({ players: [HOST, OUTSIDER], profiles: { [HOST]: profile(HOST), [OUTSIDER]: profile(OUTSIDER) }, answers: {} })));
  });
});

describe('battle_lobbies — 部屋を出る', () => {
  beforeEach(async () => { await seed(['battle_lobbies', LOBBY], seededLobby()); });
  it('出ると閉じる。閉じた部屋では、えらぶことも始めることもできない', async () => {
    await assertSucceeds(updateDoc(doc(ctxFor(HOST), 'battle_lobbies', LOBBY), { status: 'closed', [`left.${HOST}`]: serverTimestamp(), updatedAt: serverTimestamp() }));
    await assertFails(updateDoc(doc(ctxFor(GUEST), 'battle_lobbies', LOBBY), { [`picks.${GUEST}`]: pick(), updatedAt: serverTimestamp() }));
  });
  it('★相手の名前で出たことにはできない★', async () => {
    await assertFails(updateDoc(doc(ctxFor(HOST), 'battle_lobbies', LOBBY), { status: 'closed', [`left.${GUEST}`]: serverTimestamp(), updatedAt: serverTimestamp() }));
  });
  it('部屋は消せない', async () => {
    await testEnv.withSecurityRulesDisabled(async () => undefined);
    const { deleteDoc } = await import('firebase/firestore');
    await assertFails(deleteDoc(doc(ctxFor(HOST), 'battle_lobbies', LOBBY)));
  });
});

describe('battle_lobbies — フレンド対戦の単元選択ロビー', () => {
  it('ホストはロビーと4文字コードを同じ書き込みで作れる', async () => {
    const db = ctxFor(HOST);
    const b = writeBatch(db);
    b.set(doc(db, 'battle_lobbies', FRIEND_LOBBY), friendLobbyPayload({ createdAt: serverTimestamp(), updatedAt: serverTimestamp() }));
    b.set(doc(db, 'battle_codes', FRIEND_CODE), friendCodePayload({ createdAt: serverTimestamp() }));
    await assertSucceeds(b.commit());
  });
  it('ホストは友達が入る前に自分の単元を選べる', async () => {
    await seed(['battle_lobbies', FRIEND_LOBBY], friendLobbyPayload());
    await assertSucceeds(updateDoc(doc(ctxFor(HOST), 'battle_lobbies', FRIEND_LOBBY), {
      [`picks.${HOST}`]: pick(), updatedAt: serverTimestamp(),
    }));
  });
  it('相互フレンドは読み取り・2人目参加でき、自分のプロフィールを登録できる', async () => {
    await seedFriendPair();
    await seed(['battle_lobbies', FRIEND_LOBBY], friendLobbyPayload());
    const ref = doc(ctxFor(GUEST), 'battle_lobbies', FRIEND_LOBBY);
    await assertSucceeds(getDoc(ref));
    await assertSucceeds(updateDoc(ref, {
      players: [HOST, GUEST], profiles: { [HOST]: profile(HOST), [GUEST]: profile(GUEST) }, updatedAt: serverTimestamp(),
    }));
  });
  it('相互フレンドでない利用者はロビーを読めず、2人目として入れない', async () => {
    await seed(['battle_lobbies', FRIEND_LOBBY], friendLobbyPayload());
    const ref = doc(ctxFor(OUTSIDER), 'battle_lobbies', FRIEND_LOBBY);
    await assertFails(getDoc(ref));
    await assertFails(updateDoc(ref, {
      players: [HOST, OUTSIDER], profiles: { [HOST]: profile(HOST), [OUTSIDER]: profile(OUTSIDER) }, updatedAt: serverTimestamp(),
    }));
  });
  it('相手はロビーを閉じた後に古い4文字コードを片付けられる', async () => {
    await seedFriendPair();
    await seed(['battle_lobbies', FRIEND_LOBBY], friendLobbyPayload({ players: [HOST, GUEST], profiles: { [HOST]: profile(HOST), [GUEST]: profile(GUEST) } }));
    await seed(['battle_codes', FRIEND_CODE], friendCodePayload());
    await assertSucceeds(updateDoc(doc(ctxFor(GUEST), 'battle_lobbies', FRIEND_LOBBY), {
      status: 'closed', [`left.${GUEST}`]: serverTimestamp(), updatedAt: serverTimestamp(),
    }));
    await assertSucceeds(deleteDoc(doc(ctxFor(GUEST), 'battle_codes', FRIEND_CODE)));
  });
});
