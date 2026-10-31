/**
 * 英文解釈：英文→和訳を1文ずつ交互に（2026-10-31 E10）
 *   ・英文/和訳の文分割（略語・引用符・かぎかっこで切らない）
 *   ・1-1 / 1-2 / 2-1 の対応づけ
 *   ・全60題・全段落で訳が欠けない（組の和訳をつなぐと段落の和訳に戻る）
 *   ・構文のヒントは形で分かるものだけ、1文に最大2つ
 *   ・ReadingQuiz の配線
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { READING_PASSAGES } from '../src/data/reading';
import { READING_TRANSLATIONS } from '../src/data/reading/ja';
import { alignSentences, pairParagraph, splitEnSentences, splitJaSentences, structureHints } from '../src/utils/readingAlign';

describe('文分割', () => {
  it('英文：Mr. や引用符の中で切らない', () => {
    expect(splitEnSentences('Mr. Smith said, "Wait. Stop." Then he left. It rained.')).toEqual([
      'Mr. Smith said, "Wait. Stop."', 'Then he left.', 'It rained.',
    ]);
  });
  it('和訳：かぎかっこの中で切らない', () => {
    expect(splitJaSentences('彼は「待て。止まれ。」と言った。そして去った。')).toEqual([
      '彼は「待て。止まれ。」と言った。', 'そして去った。',
    ]);
  });
});

describe('対応づけ', () => {
  it('数が同じなら1対1', () => {
    expect(alignSentences(['A b.', 'C d.'], ['あ。', 'い。'])).toEqual([{ en: 'A b.', ja: 'あ。' }, { en: 'C d.', ja: 'い。' }]);
  });
  it('英文1文＝和訳2文 を許す（並びは崩さない）', () => {
    const r = alignSentences(
      ['This is a very long sentence about many different things and ideas: it goes on and on.', 'Short.'],
      ['これはさまざまな物事や考えについての、とても長い文だ。それはどこまでも続く。', '短い。'],
    );
    expect(r).toHaveLength(2);
    expect(r![0].ja).toContain('続く。');
    expect(r![1]).toEqual({ en: 'Short.', ja: '短い。' });
  });
  it('どちらかが空なら null、和訳が無い段落は英文だけの1組', () => {
    expect(alignSentences([], ['あ。'])).toBeNull();
    expect(pairParagraph('Hello there.', null)).toEqual([{ en: 'Hello there.', ja: '' }]);
  });
});

describe('全文章で訳が欠けない', () => {
  it('組の英文・和訳をつなぐと段落に戻る', () => {
    const bad: string[] = [];
    for (const p of READING_PASSAGES) {
      const ja = READING_TRANSLATIONS[p.id] ?? [];
      p.paragraphs.forEach((en, i) => {
        const pairs = pairParagraph(en, ja[i]);
        const jaJoined = pairs.map((x) => x.ja).join('').replace(/\s/g, '');
        const enJoined = pairs.map((x) => x.en).join(' ').replace(/\s/g, '');
        if (jaJoined !== (ja[i] ?? '').replace(/\s/g, '') || enJoined !== en.replace(/\s/g, '')) bad.push(`${p.id}#${i + 1}`);
      });
    }
    expect(bad).toEqual([]);
  });
});

describe('構文のヒント', () => {
  it('形で分かるものを拾う', () => {
    expect(structureHints('He was so tired that he fell asleep.').map((h) => h.label)).toContain('so ~ that …');
    expect(structureHints('It is not money but time that matters.').map((h) => h.label)).toContain('not A but B');
  });
  it('not only を拾ったら not A but B は重ねない／最大2つ', () => {
    const l = structureHints('Not only she but also he came, although it was late, which surprised us.').map((h) => h.label);
    expect(l).not.toContain('not A but B');
    expect(l.length).toBeLessThanOrEqual(2);
  });
  it('普通の文には何も付けない', () => {
    expect(structureHints('I like apples.')).toEqual([]);
  });
});

describe('画面の配線', () => {
  const src = readFileSync('src/components/ReadingQuiz.tsx', 'utf8');
  it('解説と結果画面で PairedParagraph（英文→和訳・構文）を使う', () => {
    expect(src).toContain('pairParagraph');
    expect(src).toContain('structureHints');
    expect((src.match(/<PairedParagraph/g) ?? []).length).toBeGreaterThanOrEqual(2);
  });
});
