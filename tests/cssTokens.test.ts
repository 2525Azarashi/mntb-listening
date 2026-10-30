/**
 * CSS の色トークンと、増やしたくない書き方の見張り（Phase 6 / A5・A6）。
 *
 * ■ ① トークンと同じ色を 16 進数で直書きしない
 *   src/styles/tokens.css の :root にある --mt-* と「まったく同じ色」を
 *   別の CSS に #xxxxxx で書くと、トークンを直したときにそこだけ取り残される。
 *   Phase 6 で 30 ファイル・220 か所を var(--mt-*) に置き換えた（色の値は1つも変えていない）。
 *   ここで、また直書きが増えたら止める。
 *
 *   対象外にしているもの：
 *   - tokens.css 自身（定義している場所）
 *   - philosophy-page.css（別ページ message/index.html 専用で tokens.css を読み込まない）
 *   - 複数のトークンが同じ色を持つもの（#ffffff など）。どれに置き換えるか意味で決める必要があるため
 *   - コメントと url(...)・文字列の中
 *
 * ■ ② !important と style={{ }} を今より増やさない
 *   どちらも一度に減らすと見た目が変わる危険が大きいので、今回は「数を増やさない」見張りだけにする。
 *   減らしたらここの上限も下げること（上げるときは理由を書く）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');

function walk(dir: string, ext: string[], out: string[] = []): string[] {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, ext, out);
    else if (ext.some((x) => p.endsWith(x))) out.push(p);
  }
  return out;
}
const rel = (p: string) => path.relative(ROOT, p).split(path.sep).join('/');

const norm = (h: string): string | null => {
  let v = h.toLowerCase().slice(1);
  if (v.length === 3) v = [...v].map((c) => c + c).join('');
  return v.length === 6 ? `#${v}` : null;
};

/** tokens.css の :root にある「1つのトークンだけが持つ色」→ トークン名 */
function uniqueTokenColors(): Map<string, string> {
  const tok = fs.readFileSync(path.join(SRC, 'styles/tokens.css'), 'utf8');
  const start = tok.indexOf(':root {');
  const end = tok.indexOf('@media (min-width: 1100px)');
  expect(start).toBeGreaterThanOrEqual(0);
  expect(end).toBeGreaterThan(start);
  const byVal = new Map<string, string[]>();
  for (const m of tok.slice(start, end).matchAll(/(--mt-[a-z0-9-]+):\s*(#[0-9a-fA-F]{3,8})\s*;/g)) {
    const v = norm(m[2] as string);
    if (!v) continue;
    byVal.set(v, [...(byVal.get(v) ?? []), m[1] as string]);
  }
  return new Map(
    [...byVal].filter(([v, ns]) => ns.length === 1 && v !== '#ffffff' && v !== '#000000')
      .map(([v, ns]) => [v, ns[0] as string]),
  );
}

const SKIP = new Set(['src/styles/tokens.css', 'src/components/philosophy-page.css']);
const blank = (s: string) => ' '.repeat(s.length);

describe('CSS の色トークン', () => {
  it('--mt-* は tokens.css 以外で定義し直していない（var に置き換えても色が変わらない前提）', () => {
    const offenders = walk(SRC, ['.css', '.ts', '.tsx'])
      .filter((f) => rel(f) !== 'src/styles/tokens.css')
      .filter((f) => /--mt-[a-z0-9-]+\s*:/.test(fs.readFileSync(f, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')))
      .map(rel);
    expect(offenders).toEqual([]);
  });

  it('トークンと同じ色を 16 進数で直書きしていない', () => {
    const uniq = uniqueTokenColors();
    expect(uniq.size).toBeGreaterThan(20);
    const found: string[] = [];
    for (const f of walk(SRC, ['.css'])) {
      if (SKIP.has(rel(f))) continue;
      const text = fs.readFileSync(f, 'utf8')
        .replace(/\/\*[\s\S]*?\*\//g, blank)
        .replace(/url\([^)]*\)|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g, blank);
      for (const m of text.matchAll(/#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])/g)) {
        const name = uniq.get(norm(m[0]) ?? '');
        if (name) found.push(`${rel(f)}: ${m[0]} → var(${name})`);
      }
    }
    expect(found).toEqual([]);
  });
});

/**
 * 減らしたら下げる。上げるときは理由を書く。
 *   986 / 508 … Phase 6（#131）を作った時点
 *   1022 / 512 … 2026-10-29 統合時。#127・#129（マイページ・ガチャ）と #132（C1〜C7 の設定・カレンダー）で増えた分、
 *                C12 の称号のお祝い（紙ふぶきの --i）1か所。どれもマージ済み・統合済みの見た目の変更で、今回は減らさない。
 */
const IMPORTANT_LIMIT = 1022;
const INLINE_STYLE_LIMIT = 512;

describe('増やしたくない書き方', () => {
  it(`CSS の !important は ${IMPORTANT_LIMIT} か所以下`, () => {
    const n = walk(SRC, ['.css'])
      .map((f) => (fs.readFileSync(f, 'utf8').match(/!important/g) ?? []).length)
      .reduce((a, b) => a + b, 0);
    expect(n).toBeLessThanOrEqual(IMPORTANT_LIMIT);
  });

  it(`style={{ }} の直書きは ${INLINE_STYLE_LIMIT} か所以下`, () => {
    const n = walk(SRC, ['.tsx'])
      .map((f) => (fs.readFileSync(f, 'utf8').match(/style=\{\{/g) ?? []).length)
      .reduce((a, b) => a + b, 0);
    expect(n).toBeLessThanOrEqual(INLINE_STYLE_LIMIT);
  });
});
