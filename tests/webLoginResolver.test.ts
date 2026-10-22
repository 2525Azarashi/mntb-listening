/**
 * Web 版の Google / Apple ログインで auth/argument-error が出ていた件（2026-10-21）。
 * firebase.ts はアプリ版のために initializeAuth を使っていて popup/redirect の resolver を入れていない。
 * Web の popup / redirect には resolver を毎回渡す。アプリ版（nativeSignIn）と firebase.ts は変えない。
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const g = readFileSync('src/utils/googleAuth.ts', 'utf8');
const fb = readFileSync('src/firebase.ts', 'utf8');

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
