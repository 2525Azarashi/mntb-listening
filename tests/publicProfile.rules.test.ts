/**
 * public_study_profiles のプロフィール拡張（2026-10-26）のルールテスト。
 *   本人だけ・公開のときだけ・決まった形と大きさだけ書ける。サーバーが書く level / stagesCleared は本人が変えられない。
 * 実行: npm run test:rules
 */
import { readFileSync } from 'node:fs';
import { afterAll, beforeAll, beforeEach, describe, it } from 'vitest';
import { assertFails, assertSucceeds, initializeTestEnvironment, type RulesTestEnvironment } from '@firebase/rules-unit-testing';
import { deleteDoc, doc, getDoc, serverTimestamp, setDoc, updateDoc } from 'firebase/firestore';

let env: RulesTestEnvironment;
beforeAll(async () => {
  env = await initializeTestEnvironment({ projectId: 'mntb-public-profile-test', firestore: { rules: readFileSync('firestore.rules', 'utf8'), host: '127.0.0.1', port: 8080 } });
});
afterAll(async () => { await env?.cleanup(); });
beforeEach(async () => { await env.clearFirestore(); });

const as = (uid: string) => env.authenticatedContext(uid).firestore();
const base = () => ({ public: true, targetSchool: 'A大学', studySeconds: 3600, updatedAt: serverTimestamp() });
const rich = () => ({
  ...base(), motto: '医者になる', nickname: 'たろう', grade: '高校2年', bio: '毎朝15分。\nよろしく',
  week: [0, 60, 0, 1200, 600, 0, 300], weekEnd: '2026-10-26', streak: 4, solved: 120, badges: 6,
  title: 'b_first_win', lookPose: 'pose_basic', lookFrame: 'frame_default', lookHat: '', lookGlasses: '',
});
const ref = (uid: string, me = uid) => doc(as(me), 'public_study_profiles', uid);

describe('public_study_profiles（プロフィール拡張）', () => {
  it('本人は新しい項目つきで公開できる・ほかの人は読める', async () => {
    await assertSucceeds(setDoc(ref('alice'), rich()));
    await assertSucceeds(getDoc(ref('alice', 'bob')));
  });

  it('古い形（新しい項目なし）も今までどおり保存できる', async () => {
    await assertSucceeds(setDoc(ref('alice'), base()));
  });

  it('他人の文書は書けない・消せない', async () => {
    await assertFails(setDoc(ref('alice', 'bob'), rich()));
    await env.withSecurityRulesDisabled(async (ctx) => { await setDoc(doc(ctx.firestore(), 'public_study_profiles', 'alice'), { ...rich(), updatedAt: new Date() }); });
    await assertFails(deleteDoc(ref('alice', 'bob')));
  });

  it('学年は選択肢だけ（在籍校のような自由入力は不可）', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), grade: '○○高校2年A組' }));
    await assertSucceeds(setDoc(ref('alice'), { ...rich(), grade: '' }));
  });

  it('自己紹介は160文字まで・名前は24文字まで', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), bio: 'あ'.repeat(161) }));
    await assertFails(setDoc(ref('alice'), { ...rich(), nickname: 'あ'.repeat(25) }));
    await assertSucceeds(setDoc(ref('alice'), { ...rich(), bio: 'あ'.repeat(160) }));
  });

  it('週の記録は7日分の整数・1日12時間まで', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), week: [1, 2, 3] }));
    await assertFails(setDoc(ref('alice'), { ...rich(), week: [0, 0, 0, 0, 0, 0, 43201] }));
    await assertFails(setDoc(ref('alice'), { ...rich(), week: [0, 0, 0, 0, 0, 0, -1] }));
    await assertFails(setDoc(ref('alice'), { ...rich(), week: [0, 0, 0, 0, 0, 0, 1.5] }));
    await assertFails(setDoc(ref('alice'), { ...rich(), weekEnd: '10/26' }));
  });

  it('数の項目は範囲内の整数だけ', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), streak: -1 }));
    await assertFails(setDoc(ref('alice'), { ...rich(), solved: 1_000_001 }));
    await assertFails(setDoc(ref('alice'), { ...rich(), badges: '6' }));
  });

  it('見た目・称号は ID の形だけ（URL などは入れられない）', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), lookPose: 'https://evil.example/x.png' }));
    await assertFails(setDoc(ref('alice'), { ...rich(), title: '<b>' }));
  });

  it('決まっていない項目（メールなど）は入れられない', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), email: 'a@example.com' }));
    await assertFails(setDoc(ref('alice'), { ...rich(), realName: '山田太郎' }));
  });

  it('レベル・達成ステージは本人が書き換えられない（サーバー専用）', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), level: 99 }));
    await env.withSecurityRulesDisabled(async (ctx) => { await setDoc(doc(ctx.firestore(), 'public_study_profiles', 'alice'), { ...base(), updatedAt: new Date(), level: 5, stagesCleared: 3 }); });
    await assertFails(updateDoc(ref('alice'), { level: 99, updatedAt: serverTimestamp() }));
    await assertSucceeds(updateDoc(ref('alice'), { week: [0, 0, 0, 0, 0, 0, 60], weekEnd: '2026-10-26', streak: 2, updatedAt: serverTimestamp() }));
  });

  it('非公開（public:false）にはできない＝公開をやめるときは消す', async () => {
    await assertFails(setDoc(ref('alice'), { ...rich(), public: false }));
    await assertSucceeds(setDoc(ref('alice'), rich()));
    await assertSucceeds(deleteDoc(ref('alice')));
  });

  it('ログインしていない人は読めない', async () => {
    await assertSucceeds(setDoc(ref('alice'), rich()));
    await assertFails(getDoc(doc(env.unauthenticatedContext().firestore(), 'public_study_profiles', 'alice')));
  });
});
