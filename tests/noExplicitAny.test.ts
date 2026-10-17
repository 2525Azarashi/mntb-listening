import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';

/**
 * 手書きのコードに `any` を増やさないための見張り（監査 #25 の仕上げ）。
 *
 * `any` は型検査を黙って素通りさせるため、フィールド名の打ち間違いや
 * null の読み忘れに気づけなくなる。src/ の手書きコードからは全部取り除いたので、
 * 新しく入ったらこのテストが落ちる。
 *
 * 代わりに使うもの：
 *   ・catch の例外 … 型を書かない（unknown になる）＋ utils/errorLike.ts の asErrorLike
 *   ・教材データ   … types/curriculum.ts の Problem / SubQuestion（部分的なら ProblemLike / SubQuestionLike）
 *   ・形が分からない値 … unknown にして、読む前に確かめる
 *
 * 対象外：*.generated.ts（スクリプトが書き出すデータ。中の文字列に "any" が出てくる）
 */
const ROOT = join(__dirname, '..', 'src');

function walk(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) return walk(p);
    return /\.(ts|tsx)$/.test(name) && !/\.generated\./.test(name) ? [p] : [];
  });
}

/** `: any` / `as any` / `<any>` / `any[]` / `, any>` の形 */
const EXPLICIT_ANY = /(:\s*any\b|\bas\s+any\b|<any>|\bany\[\]|,\s*any>)/;

function explicitAnys(): string[] {
  const hits: string[] = [];
  for (const file of walk(ROOT)) {
    readFileSync(file, 'utf8').split('\n').forEach((line, i) => {
      const t = line.trim();
      if (t.startsWith('*') || t.startsWith('//')) return; // 説明文の中の例
      if (EXPLICIT_ANY.test(line)) hits.push(`${file.slice(ROOT.length + 1)}:${i + 1}  ${t.slice(0, 100)}`);
    });
  }
  return hits;
}

describe('手書きコードに any が無い', () => {
  it('src/ の .ts / .tsx（生成ファイル以外）に明示的な any が無い', () => {
    expect(explicitAnys()).toEqual([]);
  });
});
