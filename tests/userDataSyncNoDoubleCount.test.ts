/**
 * コイン・XP が同期のたびに増えていく不具合の再発防止（2026-10-21）。
 * 本物の reconcile と、userDataSync.ts と同じ順番（状態 → 端末 → 送信 → base 確定）を
 * 小さなシミュレーターで回し、途中で止まる・送信に失敗する場合も確かめる。
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import {
  applyLocalWrites, GROWTH_KEY, parseSyncState, reconcile, resolvePendingBase, sectionField, serializeSyncState,
  stateBeforeUpload, type KV, type SyncState,
} from '../src/utils/userDataSyncCore';
import { levelOf } from '../src/battle/core/growthLevel';

const UID = 'u1';
type Dev = KV & { state: string | null };
const dev = (): Dev => {
  const m = new Map<string, string>();
  return { state: null, getItem: k => m.get(k) ?? null, setItem: (k, v) => { m.set(k, v); }, removeItem: k => { m.delete(k); } };
};
const env = (coins: number, xp: number) => ({ version: 1, progress: { uid: UID, coins, xp }, receipts: [], day: '' });
const setGrowth = (d: Dev, coins: number, xp: number) => d.setItem(GROWTH_KEY(UID), JSON.stringify(env(coins, xp)));
const growth = (d: Dev) => { const p = JSON.parse(d.getItem(GROWTH_KEY(UID))!).progress as { coins: number; xp: number }; return { coins: p.coins, xp: p.xp }; };
const earn = (d: Dev, coins: number, xp = 0) => { const g = growth(d); setGrowth(d, g.coins + coins, g.xp + xp); };

/** userDataSync.syncUserData と同じ順番。stopAfter で「そこでアプリが閉じられた」を再現 */
function sync(d: Dev, cloud: Record<string, unknown>, opt: { stopAfter?: 'local' | 'upload'; failUpload?: boolean } = {}) {
  const state: SyncState = parseSyncState(d.state);
  const remote = Object.keys(cloud).length ? { ...cloud } : null;
  const base = resolvePendingBase(state, remote);
  const r = reconcile(d, UID, remote, base, { apply: false });
  const hasUpload = Object.keys(r.upload).length > 0;
  d.state = serializeSyncState(hasUpload ? stateBeforeUpload(base, r) : { base: r.base, pending: null });
  applyLocalWrites(d, UID, r.localWrites);
  if (opt.stopAfter === 'local' || !hasUpload) return;
  if (opt.failUpload) return;
  Object.assign(cloud, r.upload);
  if (opt.stopAfter === 'upload') return; // 届いたが base を確定する前に閉じられた
  d.state = serializeSyncState({ base: r.base, pending: null });
}
const cloudCoins = (cloud: Record<string, unknown>) => JSON.parse(String(cloud[sectionField('growth')])).progress.coins as number;

describe('同期でコイン・XP が二重に増えない', () => {
  it('2台を何度行き来しても、増えた分だけ（増殖しない）', () => {
    const cloud: Record<string, unknown> = {}; const web = dev(); const app = dev();
    setGrowth(app, 100, 50);
    sync(app, cloud); sync(web, cloud);
    earn(app, 10, 5); sync(app, cloud);
    earn(web, 7, 3); sync(web, cloud);
    for (let i = 0; i < 6; i++) { sync(app, cloud); sync(web, cloud); }
    expect(growth(app)).toEqual({ coins: 117, xp: 58 });
    expect(growth(web)).toEqual({ coins: 117, xp: 58 });
    expect(cloudCoins(cloud)).toBe(117);
  });

  it('送信は届いたのに base を保存する前に閉じられても、次の同期で二重に足さない', () => {
    const cloud: Record<string, unknown> = {}; const app = dev();
    setGrowth(app, 100, 50); sync(app, cloud);
    earn(app, 10, 10);
    sync(app, cloud, { stopAfter: 'upload' });
    for (let i = 0; i < 5; i++) sync(app, cloud);
    expect(growth(app)).toEqual({ coins: 110, xp: 60 });
    expect(cloudCoins(cloud)).toBe(110);
  });

  it('送信に失敗しても、ほかの端末の分を二重に足さない', () => {
    const cloud: Record<string, unknown> = {}; const web = dev(); const app = dev();
    setGrowth(app, 100, 0); sync(app, cloud); sync(web, cloud);
    earn(web, 20); sync(web, cloud);           // クラウド 120
    earn(app, 5); sync(app, cloud, { failUpload: true }); // app は 125 を取り込んだが送れなかった
    for (let i = 0; i < 4; i++) { sync(app, cloud); sync(web, cloud); }
    expect(growth(app).coins).toBe(125);
    expect(growth(web).coins).toBe(125);
  });

  it('端末へ書いた直後（送る前）に閉じられても増えない', () => {
    const cloud: Record<string, unknown> = {}; const web = dev(); const app = dev();
    setGrowth(app, 100, 0); sync(app, cloud); sync(web, cloud);
    earn(web, 30); sync(web, cloud);
    earn(app, 1); sync(app, cloud, { stopAfter: 'local' });
    for (let i = 0; i < 4; i++) { sync(app, cloud); sync(web, cloud); }
    expect(growth(app).coins).toBe(131);
    expect(growth(web).coins).toBe(131);
  });

  it('ガチャで使ったコインもほかの端末へ伝わる（減る操作を消さない）', () => {
    const cloud: Record<string, unknown> = {}; const web = dev(); const app = dev();
    setGrowth(app, 500, 0); sync(app, cloud); sync(web, cloud);
    earn(app, -300); sync(app, cloud); sync(web, cloud);
    expect(growth(web).coins).toBe(200);
  });

  it('レベル（XP から計算）も、閉じられたあと何度同期しても上がらない', () => {
    const cloud: Record<string, unknown> = {}; const app = dev();
    setGrowth(app, 0, 1000); sync(app, cloud);
    earn(app, 0, 200);
    sync(app, cloud, { stopAfter: 'upload' });
    for (let i = 0; i < 8; i++) sync(app, cloud);
    expect(levelOf(growth(app).xp).level).toBe(levelOf(1200).level);
    expect(growth(app).xp).toBe(1200);
  });

  it('学習時間も二重に足さない', () => {
    const d = dev(); const st = (t: number) => JSON.stringify({ total: t, days: { '2026-10-21': t } });
    d.setItem('study_time_v1_u1', st(600));
    for (let i = 0; i < 5; i++) reconcile(d, UID, { [sectionField('studyTime')]: st(600) }, { studyTime: st(300) });
    expect(JSON.parse(d.getItem('study_time_v1_u1')!).total).toBe(600);
  });

  it('端末とクラウドが同じなら、古い base が残っていても足さない', () => {
    const d = dev(); setGrowth(d, 110, 60);
    const same = JSON.stringify(env(110, 60));
    const r = reconcile(d, UID, { [sectionField('growth')]: same }, { growth: JSON.stringify(env(100, 50)) });
    expect(growth(d)).toEqual({ coins: 110, xp: 60 });
    expect(r.upload).toEqual({});
  });
});

describe('既存ユーザーの記録を消さない（古い形式からの読み替え）', () => {
  it('2026-10-20 までの base（id → 文字列）をそのまま base として読む', () => {
    const old = JSON.stringify({ growth: JSON.stringify(env(1, 2)) });
    expect(parseSyncState(old)).toEqual({ base: { growth: JSON.stringify(env(1, 2)) }, pending: null });
  });
  it('壊れた状態は「base なし」（大きい方で合わせる＝減らない）', () => {
    expect(parseSyncState('{oops')).toEqual({ base: {}, pending: null });
    const d = dev(); setGrowth(d, 300, 900);
    reconcile(d, UID, { [sectionField('growth')]: JSON.stringify(env(120, 100)) }, {});
    expect(growth(d)).toEqual({ coins: 300, xp: 900 });
  });
});

describe('userDataSync.ts の順番', () => {
  const src = readFileSync('src/utils/userDataSync.ts', 'utf8');
  it('キャッシュの古い値では合わせない・別タブと同時に走らない', () => {
    expect(src).toContain('if (snap.metadata?.fromCache) return;');
    expect(src).toContain('locks.request(`user-data-sync-${uid}`, run)');
  });
  it('状態 → 端末 → 送信 → base 確定 の順', () => {
    const a = src.indexOf('stateBeforeUpload(base, r)');
    const b = src.indexOf('applyLocalWrites(store, uid, r.localWrites)');
    const c = src.indexOf('await setDoc(ref');
    const d = src.indexOf("serializeSyncState({ base: r.base, pending: null })", c);
    expect(a).toBeGreaterThan(0); expect(b).toBeGreaterThan(a); expect(c).toBeGreaterThan(b); expect(d).toBeGreaterThan(c);
  });
});
