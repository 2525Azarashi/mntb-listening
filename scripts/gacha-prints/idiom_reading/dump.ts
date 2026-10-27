// 英文解釈 レベル1 の本文・設問（アプリと同じ選択肢の並び）・全訳を JSON に書き出す（build.py が読む）
import { mkdirSync, writeFileSync } from 'node:fs';
import { READING_PASSAGES, shuffledOptions } from '../../../src/data/reading/index';
import { JA_LEVEL1 } from '../../../src/data/reading/ja/level1';
const passages = READING_PASSAGES.filter(p => p.level === 1).map(p => ({ ...p, questions: p.questions.map(q => ({ ...q, shuffled: shuffledOptions(q) })) }));
mkdirSync('.tmpwork/idiom_reading', { recursive: true });
writeFileSync('.tmpwork/idiom_reading/reading.json', JSON.stringify({ passages, ja: JA_LEVEL1 }));
console.log('reading passages:', passages.length);
