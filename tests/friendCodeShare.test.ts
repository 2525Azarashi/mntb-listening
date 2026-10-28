import { describe, expect, it } from 'vitest';
import { buildFriendCodeShareText } from '../src/utils/friendCodeShare';

describe('フレンドコード共有', () => {
  it('共有文面にフレンドコードと申請方法を含める', () => {
    expect(buildFriendCodeShareText('MNTB-AB12-CD34')).toBe(
      'マナトビでフレンドになろう！\nフレンドコード：MNTB-AB12-CD34\nアプリの「フレンド」画面でコードを入力して申請してください。',
    );
  });
});
