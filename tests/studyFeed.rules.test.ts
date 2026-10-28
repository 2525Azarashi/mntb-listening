/**
 * 学習記録の共有（study_posts）とリアクションのルールテスト（2026-10-27）。
 *   読めるのは本人とフレンドだけ・書けるのは本人だけ・連絡先の形は拒否・リアクションはフレンドだけ。
 * 実行: npm run test:rules
 */
import { readFileSync } from 'node:fs';
import { afterAll, beforeAll, beforeEach, describe, it } from 'vitest';
import { assertFails, assertSucceeds, initializeTestEnvironment, type RulesTestEnvironment } from '@firebase/rules-unit-testing';
import { collection, deleteDoc, doc, getDoc, getDocs, query, serverTimestamp, setDoc, Timestamp, where, orderBy } from 'firebase/firestore';

let env: RulesTestEnvironment;
beforeAll(async () => {
  env = await initializeTestEnvironment({ projectId: 'mntb-study-feed-test', firestore: { rules: readFileSync('firestore.rules', 'utf8'), host: '127.0.0.1', port: 8080 } });
});
afterAll(async () => { await env?.cleanup(); });
beforeEach(async () => {
  await env.clearFirestore();
  // alice と bob はフレンド。carol は他人
  await env.withSecurityRulesDisabled(async (ctx) => {
    const f = ctx.firestore();
    await setDoc(doc(f, 'friends', 'alice', 'items', 'bob'), { uid: 'bob', nickname: 'ぼぶ', photoURL: '', addedAt: new Date() });
    await setDoc(doc(f, 'friends', 'bob', 'items', 'alice'), { uid: 'alice', nickname: 'ありす', photoURL: '', addedAt: new Date() });
  });
});

const as = (uid: string) => env.authenticatedContext(uid).firestore();
const post = (uid = 'alice', over: Record<string, unknown> = {}) => ({
  uid, nickname: 'ありす', kind: 'manual', day: '2026-10-27', subject: 'math', materialName: '青チャート', minutes: 45,
  amount: 12, amountUnit: 'ページ', comment: '二次関数おわり', createdAt: Timestamp.fromMillis(Date.now() - 1000), updatedAt: serverTimestamp(), ...over,
});
const postRef = (me: string, id = 'alice_r1') => doc(as(me), 'study_posts', id);
const seed = async (id = 'alice_r1', uid = 'alice') => env.withSecurityRulesDisabled(async (ctx) => {
  await setDoc(doc(ctx.firestore(), 'study_posts', id), { ...post(uid), updatedAt: new Date() });
});

describe('study_posts（学習記録の共有）', () => {
  it('本人は自分のIDで共有できる・直せる・消せる', async () => {
    await assertSucceeds(setDoc(postRef('alice'), post()));
    await assertSucceeds(setDoc(postRef('alice'), post('alice', { minutes: 60 })));
    await assertSucceeds(deleteDoc(postRef('alice')));
  });

  it('他人のIDで書けない・uid をなりすませない', async () => {
    await assertFails(setDoc(postRef('bob', 'alice_r1'), post('alice')));
    await assertFails(setDoc(postRef('bob', 'bob_r1'), post('alice')));
    await assertFails(setDoc(postRef('alice', 'alice_r1_x'), post()));
  });

  it('フレンドは読める・他人とログインなしは読めない', async () => {
    await seed();
    await assertSucceeds(getDoc(postRef('bob')));
    await assertSucceeds(getDoc(postRef('alice')));
    await assertFails(getDoc(postRef('carol')));
    await assertFails(getDoc(doc(env.unauthenticatedContext().firestore(), 'study_posts', 'alice_r1')));
  });

  it('フィードのクエリ：フレンドの uid だけなら通る・他人が混ざると拒否', async () => {
    await seed();
    await assertSucceeds(getDocs(query(collection(as('bob'), 'study_posts'), where('uid', 'in', ['alice', 'bob']), orderBy('createdAt', 'desc'))));
    await assertFails(getDocs(query(collection(as('bob'), 'study_posts'), where('uid', 'in', ['alice', 'carol']), orderBy('createdAt', 'desc'))));
  });

  it('連絡先（URL・@・長い数字）や長すぎる内容は拒否', async () => {
    await assertFails(setDoc(postRef('alice'), post('alice', { comment: 'LINE @abc で' })));
    await assertFails(setDoc(postRef('alice'), post('alice', { comment: 'https://example.com' })));
    await assertFails(setDoc(postRef('alice'), post('alice', { comment: '09012345678' })));
    await assertFails(setDoc(postRef('alice'), post('alice', { materialName: 'x'.repeat(41) })));
    await assertFails(setDoc(postRef('alice'), post('alice', { comment: 'あ'.repeat(141) })));
  });

  it('形が違うものは拒否（時間0分・知らない教科・知らない欄）', async () => {
    await assertFails(setDoc(postRef('alice'), post('alice', { minutes: 0 })));
    await assertFails(setDoc(postRef('alice'), post('alice', { minutes: 721 })));
    await assertFails(setDoc(postRef('alice'), post('alice', { subject: 'xx' })));
    await assertFails(setDoc(postRef('alice'), post('alice', { email: 'a' })));
  });

  it('他人の投稿は直せない・消せない', async () => {
    await seed();
    await assertFails(setDoc(postRef('bob'), post('alice', { minutes: 1 })));
    await assertFails(deleteDoc(postRef('bob')));
  });
});

describe('study_posts/{id}/reactions（リアクション）', () => {
  const rRef = (me: string, reactor = me, id = 'alice_r1') => doc(as(me), 'study_posts', id, 'reactions', reactor);
  const r = (uid: string, type = 'cheer') => ({ uid, type, at: serverTimestamp() });

  it('フレンドは送れる・付け替えられる・取り消せる', async () => {
    await seed();
    await assertSucceeds(setDoc(rRef('bob'), r('bob')));
    await assertSucceeds(setDoc(rRef('bob'), r('bob', 'nice')));
    await assertSucceeds(deleteDoc(rRef('bob')));
  });

  it('他人・本人（自分の投稿）・なりすまし・知らない種類は送れない', async () => {
    await seed();
    await assertFails(setDoc(rRef('carol'), r('carol')));
    await assertFails(setDoc(rRef('alice'), r('alice')));
    await assertFails(setDoc(rRef('bob', 'carol'), r('carol')));
    await assertFails(setDoc(rRef('bob'), r('bob', 'love')));
  });

  it('読めるのは投稿の本人とフレンドだけ・投稿の本人は後片付けで消せる', async () => {
    await seed();
    await setDoc(rRef('bob'), r('bob'));
    await assertSucceeds(getDocs(collection(as('alice'), 'study_posts', 'alice_r1', 'reactions')));
    await assertSucceeds(getDocs(collection(as('bob'), 'study_posts', 'alice_r1', 'reactions')));
    await assertFails(getDocs(collection(as('carol'), 'study_posts', 'alice_r1', 'reactions')));
    await assertSucceeds(deleteDoc(rRef('alice', 'bob')));
  });

  it('無い投稿にはリアクションできない', async () => {
    await assertFails(setDoc(rRef('bob', 'bob', 'alice_none'), r('bob')));
  });
});

describe('user_data の s_manualLog（手動の学習記録の同期）', () => {
  it('本人は s_manualLog を保存できる・他人は読めない', async () => {
    const ref = doc(as('alice'), 'user_data', 'alice');
    await assertSucceeds(setDoc(ref, { uid: 'alice', s_manualLog: '{"version":1,"records":[],"materials":[],"goals":{}}', updatedAt: serverTimestamp() }));
    await assertFails(getDoc(doc(as('bob'), 'user_data', 'alice')));
  });
});
