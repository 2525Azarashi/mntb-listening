/**
 * 英文解釈（長文の内容一致 4択）2026-10-21
 *
 * ■ 形
 *   1つの文章（スマホ1画面に収まるくらい）＋ 設問 2〜3問（内容一致・理由・主旨・語句の意味）
 *   レベル1（基礎）〜5（最難関）。共通テストから早慶・東大・京大まで。
 *
 * ■ 作り方の決まり（tests/reading.test.ts で全問を確かめる）
 *   - 選択肢は4つ。正解は書くときは先頭に置き、出題のときに設問IDから決まる順でならべ替える
 *     （正解の位置が偏らない・何度解いても同じ並び）
 *   - evidence（根拠）は本文の文をそのまま写す。答えたあと本文の該当部分に色を付ける
 *   - 本文は英文のオリジナル。実在の入試問題・市販教材の文章は使わない
 */
export type ReadingLevel = 1 | 2 | 3 | 4 | 5;

export interface ReadingQuestion {
  id: string;
  /** 問い（日本語。レベル4・5は英語） */
  prompt: string;
  /** [正解, 誤り, 誤り, 誤り] の順で書く（出題時にならべ替える） */
  options: readonly [string, string, string, string];
  /** なぜそれが正解か（日本語） */
  explanation: string;
  /** 根拠になる本文の一節（本文の文字どおり） */
  evidence: string;
}

export interface ReadingPassage {
  id: string;
  level: ReadingLevel;
  /** 英語のタイトル */
  title: string;
  /** 話題（日本語） */
  topic: string;
  /** 本文（段落は空行で区切る） */
  text: string;
  questions: readonly ReadingQuestion[];
}

export function q(id: string, prompt: string, options: readonly [string, string, string, string], explanation: string, evidence: string): ReadingQuestion {
  return { id, prompt, options, explanation, evidence };
}

export function p(id: string, level: ReadingLevel, title: string, topic: string, text: string, questions: readonly ReadingQuestion[]): ReadingPassage {
  return { id, level, title, topic, text: text.trim(), questions };
}
