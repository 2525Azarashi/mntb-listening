import { describe, expect, it } from 'vitest';
import { checkShareable, looksLikeContact, mergeFeedPages, parsePost, postIdOf, type StudyPost } from '../src/features/studylog/studyFeed';

const post = (id: string, createdAt: number): StudyPost => ({ id, uid: 'u', nickname: 'た', kind: 'manual', day: '2026-10-27', subject: 'math', materialName: '', minutes: 30, createdAt });

describe('学習記録の共有：送る前のチェック', () => {
  it('URL・@・電話番号・長い数字は連絡先とみなす', () => {
    for (const s of ['https://x.jp', 'www.example.com', 'LINE @abc', 'abc＠gmail', '090-1234-5678', '09012345678', '１２３４５６７'])
      expect(looksLikeContact(s), s).toBe(true);
    for (const s of ['青チャート 例題12〜20', '2026年の過去問', '英単語1900'])
      expect(looksLikeContact(s), s).toBe(false);
  });
  it('ふつうの記録は共有できる・連絡先入りのコメントは止める', () => {
    expect(checkShareable({ materialName: '青チャート', comment: '二次関数おわり' }, 'たろう')).toBeNull();
    expect(checkShareable({ materialName: '青チャート', comment: 'インスタ @taro' }, 'たろう')).toMatch(/コメント/);
    expect(checkShareable({ materialName: 'https://x.jp', comment: '' }, 'たろう')).toMatch(/教材/);
  });
});

describe('フィードのまとめ方', () => {
  it('新しい順・重複なし・ページの大きさで切り、続きがあるかを返す', () => {
    const a = [post('a1', 50), post('a2', 30)];
    const b = [post('b1', 40), post('a1', 50)];
    const r = mergeFeedPages([a, b], 2);
    expect(r.posts.map(p => p.id)).toEqual(['a1', 'b1']);
    expect(r.hasMore).toBe(true);
    expect(mergeFeedPages([[post('x', 1)]], 2)).toEqual({ posts: [post('x', 1)], hasMore: false });
  });
  it('壊れた投稿は捨てる・投稿IDは uid_記録ID', () => {
    expect(parsePost('p', { uid: 'u', nickname: 'た', day: '2026-10-27', subject: 'math', minutes: 0 })).toBeNull();
    expect(parsePost('p', { uid: 'u', nickname: 'た', day: '2026-10-27', subject: 'xx', minutes: 30 })).toBeNull();
    expect(parsePost('p', { uid: 'u', nickname: 'た', day: '2026-10-27', subject: 'math', minutes: 30, materialName: '青' })?.minutes).toBe(30);
    expect(postIdOf('u1', 'r1')).toBe('u1_r1');
  });
});
