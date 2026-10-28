import { afterEach, describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { classify, conflictSection, hasConflictMarkers, mergeConflicts, mergeWithAutoResolve, resolveUnion } from '../scripts/pr/prCore.mts';

/** PR を作る前の競合チェック（scripts/pr）。2026-10-28 ご要望「既存PRとの競合を解消したうえでPRを作る」 */
describe('競合の判定と、追記だけのファイルの自動解消', () => {
  it('競合なし／UI_CHANGELOG だけ（自動）／ほかのファイル（人が決める）', () => {
    expect(classify([])).toBe('none');
    expect(classify(['docs/UI_CHANGELOG.md'])).toBe('auto');
    expect(classify(['docs/UI_CHANGELOG.md', 'src/App.tsx'])).toBe('manual');
  });

  it('両方の追記を残す：自分が上、相手が下、間に区切り線', () => {
    const text = ['# 記録', '', '---', '', '<<<<<<< HEAD', '## 自分の追記', '', '=======', '## 相手の追記', '', '>>>>>>> origin/main', '## 前からある記録', ''].join('\n');
    const out = resolveUnion(text, '---');
    expect(hasConflictMarkers(out)).toBe(false);
    expect(out.indexOf('## 自分の追記')).toBeLessThan(out.indexOf('## 相手の追記'));
    expect(out.indexOf('## 相手の追記')).toBeLessThan(out.indexOf('## 前からある記録'));
    expect(out).toContain('## 自分の追記\n\n---\n\n## 相手の追記');
  });

  it('同じ中身は1つだけ残す・diff3 形式の元の文は捨てる・閉じていない印はエラー', () => {
    expect(resolveUnion(['<<<<<<< a', 'x', '=======', 'x', '>>>>>>> b'].join('\n'))).toBe('x');
    expect(resolveUnion(['<<<<<<< a', 'x', '||||||| base', 'old', '=======', 'y', '>>>>>>> b'].join('\n'))).toBe('x\n\ny');
    expect(() => resolveUnion(['<<<<<<< a', 'x', '======='].join('\n'))).toThrow();
  });

  it('説明に「競合の確認」欄：取り込んだ PR と、他の PR との関係を書く', () => {
    const pr = (number: number) => ({ number, title: `PR${number}`, headRefName: `b${number}`, baseRefName: 'main', isCrossRepository: false, author: 'x' });
    const s = conflictSection('main', [
      { pr: pr(1), files: [], kind: 'none' },
      { pr: pr(2), files: ['docs/UI_CHANGELOG.md'], kind: 'auto' },
      { pr: pr(3), files: ['src/App.tsx'], kind: 'manual' },
    ], [4], ['docs/UI_CHANGELOG.md']);
    expect(s).toContain('#4：この PR に取り込み済み');
    expect(s).toContain('#1（PR1）：競合なし');
    expect(s).toContain('#2：docs/UI_CHANGELOG.md の追記が重なる');
    expect(s).toContain('#3：⚠ src/App.tsx が競合');
  });
});

describe('本物の git で：merge-tree で競合を見つけ、追記だけなら自動で合わせる', () => {
  let dir = '';
  const g = (...args: string[]) => execFileSync('git', args, { cwd: dir, encoding: 'utf8' }).trim();
  const put = (p: string, s: string) => { mkdirSync(join(dir, p, '..'), { recursive: true }); writeFileSync(join(dir, p), s); };
  const commit = (m: string) => { g('add', '-A'); g('commit', '-q', '-m', m); };
  afterEach(() => { if (dir) rmSync(dir, { recursive: true, force: true }); });

  function setup() {
    dir = mkdtempSync(join(tmpdir(), 'prtool-'));
    g('init', '-q', '-b', 'main'); g('config', 'user.email', 't@example.com'); g('config', 'user.name', 't'); g('config', 'commit.gpgsign', 'false');
    put('docs/UI_CHANGELOG.md', '# 記録\n\n---\n\n## 古い記録\n');
    put('src/a.ts', 'export const a = 1;\n');
    commit('init');
    // 他の PR（main に先に入った）：記録に追記
    g('checkout', '-q', '-b', 'other');
    put('docs/UI_CHANGELOG.md', '# 記録\n\n---\n\n## 相手の追記\n\n---\n\n## 古い記録\n'); commit('other');
    g('checkout', '-q', 'main'); g('merge', '-q', '--no-ff', '-m', 'merge other', 'other');
    // 自分の枝（古い main から）：記録に追記
    g('checkout', '-q', '-b', 'mine', 'HEAD~1');
    put('docs/UI_CHANGELOG.md', '# 記録\n\n---\n\n## 自分の追記\n\n---\n\n## 古い記録\n'); commit('mine');
  }

  it('UI_CHANGELOG だけの競合は自動解消してコミット（両方の追記が残る）', () => {
    setup();
    expect(mergeConflicts('mine', 'main', dir)).toEqual(['docs/UI_CHANGELOG.md']);
    const r = mergeWithAutoResolve('main', 'merge: main', { cwd: dir });
    expect(r).toMatchObject({ ok: true, merged: true, autoResolved: ['docs/UI_CHANGELOG.md'] });
    const t = readFileSync(join(dir, 'docs/UI_CHANGELOG.md'), 'utf8');
    expect(hasConflictMarkers(t)).toBe(false);
    expect(t).toContain('## 自分の追記'); expect(t).toContain('## 相手の追記'); expect(t).toContain('## 古い記録');
    expect(g('status', '--porcelain')).toBe('');
    expect(mergeConflicts('HEAD', 'main', dir)).toEqual([]);
  });

  it('ソースの競合は自動では決めない：merge を取り消して、ファイル名を返す（作業フォルダは元のまま）', () => {
    setup();
    put('src/a.ts', 'export const a = 2;\n'); commit('mine src');
    g('checkout', '-q', 'main'); put('src/a.ts', 'export const a = 3;\n'); commit('main src'); g('checkout', '-q', 'mine');
    const head = g('rev-parse', 'HEAD');
    const r = mergeWithAutoResolve('main', 'merge: main', { cwd: dir });
    expect(r).toEqual({ ok: false, manual: ['src/a.ts'] });
    expect(g('rev-parse', 'HEAD')).toBe(head);
    expect(g('status', '--porcelain')).toBe('');
  });
});
