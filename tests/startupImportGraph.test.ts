/**
 * 起動時に読み込まれるファイルの見張り（Phase 4 / A4・A13）。
 *
 * ■ 何を守っているか
 *   起動直後（main.tsx から静的 import でたどれる範囲）に、
 *   教科データ本体（allChapters・英語リスニング・英文法など 約2.6MB）が
 *   入っていないこと。
 *   いまは単元選択（ChapterSelection）と演習画面（QuizScreens）を
 *   React.lazy で「開いたときに読む」ようにしてあり、
 *   起動時に読む src/data は索引などの軽いファイルだけになっている。
 *
 * ■ なぜテストにするのか
 *   vite.config.ts の manualChunks は src/data をひとつの data チャンクにまとめている。
 *   そのため、どこか1か所でも静的に allChapters を import すると
 *   ★data チャンク全体（数MB）が起動時に落ちてくる★。
 *   見た目は何も変わらないので、人の目では気づけない。
 *   ここで import のつながりを機械的にたどって止める。
 *
 * ■ 数え方
 *   - `import type` や、全部が `type` 指定の `{ type A }` は実行時に消えるので数えない
 *   - `import('...')`（動的 import）は「開いたときに読む」なので数えない
 *   - 相対パス（./ ../）の import だけをたどる（npm パッケージは対象外）
 */
import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';
import { describe, expect, it } from 'vitest';

const SRC = path.resolve(__dirname, '../src');
const ENTRY = path.join(SRC, 'main.tsx');
const EXTS = ['.ts', '.tsx', '.js', '.mjs', '/index.ts', '/index.tsx'];

function resolveSpec(from: string, spec: string): string | null {
  if (!spec.startsWith('.')) return null;
  const base = path.resolve(path.dirname(from), spec);
  if (fs.existsSync(base) && fs.statSync(base).isFile()) return base;
  for (const ext of EXTS) {
    if (fs.existsSync(base + ext)) return base + ext;
  }
  return null;
}

/** 実行時に残る（型だけではない）静的 import / export from の行き先 */
function runtimeImports(file: string): string[] {
  const text = fs.readFileSync(file, 'utf8');
  const sf = ts.createSourceFile(file, text, ts.ScriptTarget.Latest, false);
  const out: string[] = [];
  for (const st of sf.statements) {
    if (ts.isImportDeclaration(st)) {
      const clause = st.importClause;
      if (clause?.isTypeOnly) continue;
      if (clause && !clause.name && clause.namedBindings && ts.isNamedImports(clause.namedBindings)) {
        const els = clause.namedBindings.elements;
        if (els.length > 0 && els.every((e) => e.isTypeOnly)) continue;
      }
      if (ts.isStringLiteral(st.moduleSpecifier)) out.push(st.moduleSpecifier.text);
    } else if (ts.isExportDeclaration(st) && st.moduleSpecifier && ts.isStringLiteral(st.moduleSpecifier)) {
      if (st.isTypeOnly) continue;
      if (st.exportClause && ts.isNamedExports(st.exportClause)) {
        const els = st.exportClause.elements;
        if (els.length > 0 && els.every((e) => e.isTypeOnly)) continue;
      }
      out.push(st.moduleSpecifier.text);
    }
  }
  return out;
}

/** main.tsx から静的にたどれるファイルと、そこへ来た経路（親） */
function startupGraph(): Map<string, string | null> {
  const parent = new Map<string, string | null>([[ENTRY, null]]);
  const stack = [ENTRY];
  while (stack.length > 0) {
    const file = stack.pop() as string;
    for (const spec of runtimeImports(file)) {
      const next = resolveSpec(file, spec);
      if (next && !parent.has(next)) {
        parent.set(next, file);
        stack.push(next);
      }
    }
  }
  return parent;
}

function chainOf(graph: Map<string, string | null>, file: string): string {
  const chain: string[] = [];
  let cur: string | null | undefined = file;
  while (cur) {
    chain.push(path.relative(SRC, cur));
    cur = graph.get(cur);
  }
  return chain.reverse().join(' → ');
}

/** 起動時に入ってはいけない重い教科データ（ファイル名の先頭で判定） */
const HEAVY_DATA = [
  'data/allChapters.ts',
  'data/englishListeningData.ts',
  'data/englishGrammarData.ts',
  'data/egV3Items.generated.ts',
  'data/englishListeningQ',
  'data/listeningVocabularySource.json',
];

/**
 * 起動時に読む src/data の合計バイト数の上限。
 * 2026-10-28 時点の実測は約 78KB（16 ファイル）。
 * 新しい軽いデータを足す余地として 200KB にしてある。
 * これを超えたら「重いデータを静的に import していないか」をまず疑うこと。
 */
const STARTUP_DATA_BYTE_LIMIT = 200_000;

describe('起動時に読み込まれるファイル', () => {
  const graph = startupGraph();
  const files = [...graph.keys()];

  it('main.tsx から実際にたどれている（たどり方が壊れていない）', () => {
    expect(files.length).toBeGreaterThan(100);
    expect(files.some((f) => f.endsWith(path.join('src', 'App.tsx')))).toBe(true);
  });

  it('教科データ本体（allChapters など）が起動時に入っていない', () => {
    const offenders = files.filter((f) => {
      const rel = path.relative(SRC, f).split(path.sep).join('/');
      return HEAVY_DATA.some((h) => rel.startsWith(h));
    });
    expect(offenders.map((f) => chainOf(graph, f))).toEqual([]);
  });

  it(`起動時に読む src/data の合計が ${STARTUP_DATA_BYTE_LIMIT} バイト以下`, () => {
    const dataFiles = files.filter((f) => f.includes(`${path.sep}src${path.sep}data${path.sep}`));
    const total = dataFiles.reduce((sum, f) => sum + fs.statSync(f).size, 0);
    expect(total).toBeLessThanOrEqual(STARTUP_DATA_BYTE_LIMIT);
  });

  it('単元選択・演習画面は遅延読み込みのまま（App.tsx から静的 import しない）', () => {
    const app = files.find((f) => f.endsWith(path.join('src', 'App.tsx'))) as string;
    const specs = runtimeImports(app);
    expect(specs).not.toContain('./components/ChapterSelection');
    expect(specs).not.toContain('./components/QuizScreens');
  });
});
