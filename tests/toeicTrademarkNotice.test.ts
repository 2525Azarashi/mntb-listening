import { describe, expect, it } from 'vitest';
import { TOEIC_DISCLAIMER } from '../src/features/legal/toeicTrademarkNotice';
import { STUDY_CATALOG } from '../src/data/studyCatalog';

describe('TOEIC商標表示とリーディング導線', () => {
  it('ETSが示す免責文を英語で含み、日本語でも意味を伝える', () => {
    expect(TOEIC_DISCLAIMER).toContain(
      'TOEIC® is a registered trademark of ETS. This product is not endorsed or approved by ETS.',
    );
    expect(TOEIC_DISCLAIMER).toContain(
      'TOEIC®はETSの登録商標です。本アプリはETSの承認・推奨を受けたものではありません。',
    );
  });

  it('TOEIC入口に登録商標記号・一般名称・リーディング説明がある', () => {
    const toeic = STUDY_CATALOG.find(subject => subject.id === 'english')?.contents
      .find(content => content.id === 'english_toeic');
    expect(toeic?.title).toBe('TOEIC® L&R TEST');
    expect(toeic?.description).toContain('リーディング');
    expect(toeic?.title).not.toMatch(/Part\s*[567]/i);
    expect(toeic?.description).not.toMatch(/Part\s*[567]/i);
  });
});
