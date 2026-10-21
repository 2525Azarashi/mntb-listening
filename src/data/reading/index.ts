/**
 * 英文解釈（内容一致 4択）の問題集と記録（2026-10-21）
 *   - 全レベルの文章をまとめ、出題時の選択肢の並びを設問IDから決める（何度解いても同じ・正解位置が偏らない）
 *   - 記録は端末（localStorage）に保存し、アカウント同期（userDataSyncCore の 'reading'）でほかの端末にもそろえる
 */
import { LEVEL1 } from './level1';
import { LEVEL2 } from './level2';
import { LEVEL3 } from './level3';
import { LEVEL4 } from './level4';
import { LEVEL5 } from './level5';
import { safeGetItem } from '../../utils/safeLocalStorage';
import { safeSetItem } from '../../utils/storageGuard';
import type { ReadingLevel, ReadingPassage, ReadingQuestion } from './types';

export type { ReadingLevel, ReadingPassage, ReadingQuestion } from './types';

export const READING_PASSAGES: readonly ReadingPassage[] = [...LEVEL1, ...LEVEL2, ...LEVEL3, ...LEVEL4, ...LEVEL5];

export const READING_LEVELS: readonly { level: ReadingLevel; name: string; target: string }[] = [
  { level: 1, name: 'Lv1 基礎', target: '高1・共通テスト基礎' },
  { level: 2, name: 'Lv2 標準', target: '共通テスト・日東駒専・産近甲龍' },
  { level: 3, name: 'Lv3 応用', target: 'GMARCH・関関同立・地方国立' },
  { level: 4, name: 'Lv4 難関', target: '早慶・旧帝大・難関国立' },
  { level: 5, name: 'Lv5 最難関', target: '東大・京大・医学部' },
];

export const passagesOf = (level: ReadingLevel) => READING_PASSAGES.filter(x => x.level === level);
export const findPassage = (id: string) => READING_PASSAGES.find(x => x.id === id);
export const wordCount = (text: string) => text.split(/\s+/).filter(w => /[A-Za-z0-9]/.test(w)).length;

/** 文字列 → 32bit の数（FNV-1a）。並び替えの種に使う */
function hash(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return h >>> 0;
}

/** 出題時の選択肢（正解は先頭に書いてある）。設問IDから決まる順にならべ替える */
export function shuffledOptions(q: ReadingQuestion): { options: string[]; answerIndex: number } {
  let s = hash(q.id) || 1;
  const rnd = () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 0x100000000; };
  const idx = [0, 1, 2, 3];
  for (let i = idx.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [idx[i], idx[j]] = [idx[j]!, idx[i]!]; }
  return { options: idx.map(i => q.options[i]!), answerIndex: idx.indexOf(0) };
}

/** 本文を「根拠の前・根拠・後ろ」に分ける（答えたあとに根拠へ色を付ける） */
export function splitEvidence(text: string, evidence: string | null): { before: string; mark: string; after: string } {
  const i = evidence ? text.indexOf(evidence) : -1;
  if (!evidence || i < 0) return { before: text, mark: '', after: '' };
  return { before: text.slice(0, i), mark: evidence, after: text.slice(i + evidence.length) };
}

// -------------------------------------------------------------------
// 記録
// -------------------------------------------------------------------

export interface ReadingBest { score: number; total: number; at: number }
export interface ReadingRecord {
  version: 1;
  /** 文章ごとの最高点 */
  best: Record<string, ReadingBest>;
  /** 間違えたままの設問ID（正解すると外れる） */
  missed: string[];
}

export const READING_KEY = (uid: string) => 'reading_quiz_v1_' + encodeURIComponent(uid);
const empty = (): ReadingRecord => ({ version: 1, best: {}, missed: [] });

export function isReadingRecord(v: unknown): v is ReadingRecord {
  return !!v && typeof v === 'object' && (v as ReadingRecord).version === 1
    && !!(v as ReadingRecord).best && typeof (v as ReadingRecord).best === 'object' && Array.isArray((v as ReadingRecord).missed);
}

export function readReadingRecord(uid: string): ReadingRecord {
  try {
    const v = JSON.parse(safeGetItem(READING_KEY(uid)) || 'null');
    return isReadingRecord(v) ? { version: 1, best: { ...v.best }, missed: v.missed.filter(x => typeof x === 'string') } : empty();
  } catch { return empty(); }
}

export function writeReadingRecord(uid: string, rec: ReadingRecord) {
  safeSetItem(READING_KEY(uid), JSON.stringify(rec)); // 容量不足などで保存できなくても解き続けられる
}

/** 1つの文章を解き終えたときの記録の更新 */
export function applyReadingResult(rec: ReadingRecord, passageId: string, results: readonly { questionId: string; correct: boolean }[], at = Date.now()): ReadingRecord {
  const score = results.filter(r => r.correct).length;
  const prev = rec.best[passageId];
  const best = !prev || score >= prev.score ? { ...rec.best, [passageId]: { score, total: results.length, at } } : rec.best;
  const missed = new Set(rec.missed);
  for (const r of results) { if (r.correct) missed.delete(r.questionId); else missed.add(r.questionId); }
  return { version: 1, best, missed: [...missed] };
}

export const isCleared = (rec: ReadingRecord, p: ReadingPassage) => {
  const b = rec.best[p.id];
  return !!b && b.score >= p.questions.length;
};
