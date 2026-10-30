import { expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

// 2026-10-30：intro.css の @media の閉じかっこを消してしまい、Vercel のビルドだけが落ちた（tsc・vitest は通っていた）。
// CSS の { と } の数がそろっているかを、ビルドの前に見つける。
function walk(dir: string): string[] {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p) : p.endsWith('.css') ? [p] : [];
  });
}

it('src の CSS は { と } の数がそろっている', () => {
  const bad: string[] = [];
  for (const f of walk('src')) {
    const s = fs.readFileSync(f, 'utf8')
      .replace(/\/\*[\s\S]*?\*\//g, '')
      .replace(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'/g, '');
    let depth = 0;
    let min = 0;
    for (const c of s) {
      if (c === '{') depth++;
      else if (c === '}') { depth--; min = Math.min(min, depth); }
    }
    if (depth !== 0 || min < 0) bad.push(`${f}: 差 ${depth}`);
  }
  expect(bad).toEqual([]);
});
