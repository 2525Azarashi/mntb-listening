// 英文解釈 レベル1〜3 の本文・設問（アプリと同じ選択肢の並び）・全訳と、英文法（アプリの4択）を JSON に書き出す
// build.py（熟語＋英文解釈）と ../grammar_b4/build.py（文法）が読む
import { mkdirSync, writeFileSync } from 'node:fs';
import { READING_PASSAGES, shuffledOptions } from '../../../src/data/reading/index';
import { READING_TRANSLATIONS } from '../../../src/data/reading/ja/index';
import { EG_V3_ITEMS } from '../../../src/data/egV3Items.generated';

mkdirSync('.tmpwork/idiom_reading', { recursive: true });
for (const level of [1, 2, 3]) {
  const passages = READING_PASSAGES.filter((p) => p.level === level).map((p) => ({
    ...p,
    questions: p.questions.map((q) => ({ ...q, shuffled: shuffledOptions(q) })),
  }));
  const ja = Object.fromEntries(passages.map((p) => [p.id, READING_TRANSLATIONS[p.id] ?? []]));
  writeFileSync(`.tmpwork/idiom_reading/reading${level}.json`, JSON.stringify({ passages, ja }));
  console.log(`reading level ${level}:`, passages.length);
}
writeFileSync('.tmpwork/idiom_reading/grammar.json', JSON.stringify(EG_V3_ITEMS));
console.log('grammar items:', EG_V3_ITEMS.length);
