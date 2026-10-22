/**
 * Web 版の Google / Apple ログインで auth/argument-error が出ていた件（2026-10-21）。
 * firebase.ts はアプリ版のために initializeAuth を使っていて popup/redirect の resolver を入れていない。
 * Web の popup / redirect には resolver を毎回渡す。アプリ版（nativeSignIn）と firebase.ts の初期化（保存の仕方）は変えない。
 *
 * 2026-10-22 追記：Web で「連携中…」のまま止まる件。
 *   ・vercel.json で /__/auth/* を firebaseapp.com へ中継（同じドメインでログインを完結させる）
 *   ・firebase.ts の authDomain は VITE_AUTH_SAME_ORIGIN=true のときだけ今のドメインに（アプリ版・localhost は今までどおり）
 *   ・ポップアップの結果が届かなくても止まらない見張り（popupWithWatchdog）
 *   手順書：docs/WEB_LOGIN_SAME_ORIGIN.md
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const g = readFileSync('src/utils/googleAuth.ts', 'utf8');
const fb = readFileSync('src/firebase.ts', 'utf8');
const vercel = JSON.parse(readFileSync('vercel.json', 'utf8')) as {
  rewrites: { source: string; destination: string }[];
  headers: { source: string; headers: { key: string; value: string }[] }[];
};

describe('Web ログインに resolver を渡す', () => {
  it('popup・redirect・結果の受け取りの3か所すべて', () => {
    expect(g).toContain('signInWithPopup(auth, p, browserPopupRedirectResolver)');
    expect(g).toContain('signInWithRedirect(auth, p, browserPopupRedirectResolver)');
    expect(g).toContain('getRedirectResult(auth, browserPopupRedirectResolver)');
  });
  it('アプリ版は今までどおり nativeSignIn（popup より前で分かれる）', () => {
    expect(g.indexOf('return nativeSignIn(method);')).toBeGreaterThan(0);
    expect(g.indexOf('return nativeSignIn(method);')).toBeLessThan(g.indexOf('signInWithPopup(auth, p'));
  });
  it('firebase.ts の初期化（アプリ版のログイン保存）は変えない', () => {
    expect(fb).toContain('persistence: [indexedDBLocalPersistence, browserLocalPersistence]');
    expect(fb).not.toContain('popupRedirectResolver');
  });
});

describe('Web ログインを同じドメインで（連携中…で止まらない）', () => {
  it('vercel.json：/__/auth を firebaseapp.com へ中継し、SPA の書き換えより前にある', () => {
    const auth = vercel.rewrites.findIndex((r) => r.source === '/__/auth/:path*');
    const spa = vercel.rewrites.findIndex((r) => r.destination === '/index.html');
    expect(auth).toBeGreaterThanOrEqual(0);
    expect(vercel.rewrites[auth].destination).toBe('https://mntb-listening.firebaseapp.com/__/auth/:path*');
    expect(auth).toBeLessThan(spa);
    // SPA 側は __/ を飲み込まない
    expect(vercel.rewrites[spa].source).toContain('__/');
  });
  it('vercel.json：アプリの CSP は /__/ に付けない（Firebase のログイン画面が壊れないように）', () => {
    expect(vercel.headers[0].source).toBe('/((?!__/).*)');
    expect(vercel.headers[0].headers.some((h) => h.key === 'Content-Security-Policy')).toBe(true);
    const authHeaders = vercel.headers.find((h) => h.source === '/__/(.*)');
    expect(authHeaders).toBeTruthy();
    expect(authHeaders!.headers.some((h) => h.key === 'Content-Security-Policy')).toBe(false);
    expect(authHeaders!.headers.find((h) => h.key === 'Cache-Control')?.value).toBe('no-store');
  });
  it('firebase.ts：authDomain の切り替えはスイッチ（環境変数）とアプリ版の判定つき', () => {
    expect(fb).toContain("env.VITE_AUTH_SAME_ORIGIN !== 'true'");
    expect(fb).toContain('isNativePlatform');
    expect(fb).toContain("hostname === 'localhost'");
    expect(fb).toContain("protocol !== 'https:'");
    expect(fb).toContain('resolveAuthDomain(env.VITE_FIREBASE_AUTH_DOMAIN)');
  });
  it('googleAuth.ts：ポップアップは見張りつき（裏でログイン済みなら成功／時間切れで案内）', () => {
    expect(g).toContain('const credential = await popupWithWatchdog(p);');
    expect(g).toContain('onAuthStateChanged(auth');
    expect(g).toContain("errorCode: 'login_popup_timeout'");
    expect(g).toMatch(/finally \{ stop\(\); \}/);
  });
});
