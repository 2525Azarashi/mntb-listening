import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { CLASSROOM_PREVIEW_EMAILS, SOCIAL_FEATURES, isClassroomEnabledFor } from '../src/config/features';

/** クラス機能の先行確認（2026-10-28）：公開前でも決めたアカウントだけ入れる */
describe('クラス機能の先行確認', () => {
  it('公開フラグは false のまま', () => {
    expect(SOCIAL_FEATURES.classroom).toBe(false);
  });
  it('決めた2アカウントだけ入れる（大文字・前後の空白は同じとみなす）', () => {
    expect(CLASSROOM_PREVIEW_EMAILS).toEqual(['hirokingz0927@gmail.com', 'mntobira@gmail.com']);
    expect(isClassroomEnabledFor({ email: 'hirokingz0927@gmail.com', emailVerified: true })).toBe(true);
    expect(isClassroomEnabledFor({ email: ' MNTOBIRA@gmail.com ', emailVerified: true })).toBe(true);
  });
  it('ほかの人・未ログイン・メール未確認は入れない', () => {
    expect(isClassroomEnabledFor({ email: 'someone@gmail.com', emailVerified: true })).toBe(false);
    expect(isClassroomEnabledFor({ email: 'mntobira@gmail.com', emailVerified: false })).toBe(false);
    expect(isClassroomEnabledFor({ email: 'mntobira@gmail.com.evil.jp', emailVerified: true })).toBe(false);
    expect(isClassroomEnabledFor(null)).toBe(false);
    expect(isClassroomEnabledFor({})).toBe(false);
  });
  it('設定のクラスタブと解説の「選んだ理由」は同じ判定を使う', () => {
    for (const f of ['src/components/ProfileModal.tsx', 'src/components/explanation/ReasonBox.tsx']) {
      const src = readFileSync(f, 'utf8');
      expect(src).toContain('isClassroomEnabledFor');
      expect(src).not.toContain('SOCIAL_FEATURES.classroom');
    }
  });
});
