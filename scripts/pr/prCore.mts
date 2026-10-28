/**
 * PR を作る前に「main」と「開いている他の PR」との競合を調べて解消する道具の中身（2026-10-28）
 *
 *   使い方は scripts/pr/pr.mts（npm run pr:check / pr:create / pr:sync）。ここは中身だけ（テストしやすいように分けた）。
 *
 *   ■ 競合の調べ方
 *     git merge-tree --write-tree で「2つの枝を合わせたらどうなるか」を作業フォルダを触らずに計算する。
 *     → 終了コード 1 なら競合あり。--name-only で競合したファイルの一覧が取れる。
 *
 *   ■ 自動で解消してよいファイル（APPEND_ONLY）
 *     docs/UI_CHANGELOG.md のように「先頭に追記していくだけ」のファイルは、両方の追記を残せば正しい。
 *     自分の追記を上（新しい方）、相手の追記を下にし、間に区切り線 --- を入れる。
 *     それ以外のファイルの競合は機械では決めない（止めて、どの PR のどのファイルかを出す）。
 */
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

/** 先頭に追記していくだけのファイル。競合しても両方残せばよい */
export const APPEND_ONLY: readonly string[] = ['docs/UI_CHANGELOG.md'];

/** PR の説明に必ず入れる見出し（CLAUDE.md：リスニング納品の判断） */
export const REQUIRED_BODY_HEADING = 'リスニング納品の判断';

export type ConflictKind = 'none' | 'auto' | 'manual';

/** 競合したファイルの一覧から「なし／自動で解消できる／人が決める」を判定 */
export function classify(files: readonly string[], appendOnly: readonly string[] = APPEND_ONLY): ConflictKind {
  if (!files.length) return 'none';
  return files.every((f) => appendOnly.includes(f)) ? 'auto' : 'manual';
}

/**
 * 競合の印（<<<<<<< ======= >>>>>>>）が入った文章を「両方残す」形にする。
 *   - 自分（ours）の塊を上、相手（theirs）の塊を下。中身が同じなら1つだけ残す
 *   - diff3 形式（||||||| 元の文）は元の文を捨てる
 *   - separator を渡すと、2つの塊の間にそれを入れる（UI_CHANGELOG は '---'）
 *   印が壊れている（閉じていない）ときは例外を投げる
 */
export function resolveUnion(text: string, separator = ''): string {
  const lines = text.split('\n');
  const out: string[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i]!;
    if (!line.startsWith('<<<<<<< ') && line !== '<<<<<<<') { out.push(line); i++; continue; }
    const ours: string[] = []; const theirs: string[] = [];
    let part: 'ours' | 'base' | 'theirs' = 'ours';
    i++;
    let closed = false;
    for (; i < lines.length; i++) {
      const l = lines[i]!;
      if (l.startsWith('||||||| ') || l === '|||||||') { part = 'base'; continue; }
      if (l === '=======') { part = 'theirs'; continue; }
      if (l.startsWith('>>>>>>> ') || l === '>>>>>>>') { closed = true; i++; break; }
      if (part === 'ours') ours.push(l); else if (part === 'theirs') theirs.push(l);
    }
    if (!closed) throw new Error('競合の印が閉じていません（>>>>>>> が無い）');
    const trimEnd = (xs: string[]) => { const ys = xs.slice(); while (ys.length && ys[ys.length - 1]!.trim() === '') ys.pop(); return ys; };
    const a = trimEnd(ours); const b = trimEnd(theirs);
    if (a.join('\n') === b.join('\n') || !b.length) { out.push(...ours); continue; }
    if (!a.length) { out.push(...theirs); continue; }
    out.push(...a, '');
    // 区切り線：どちらかの塊がすでに区切り線で終わる／始まるなら足さない
    if (separator && a[a.length - 1]!.trim() !== separator && b[0]!.trim() !== separator) out.push(separator, '');
    out.push(...theirs);
  }
  return out.join('\n');
}

export function hasConflictMarkers(text: string): boolean {
  return /^(<<<<<<<|=======|>>>>>>>)( |$)/m.test(text);
}

// ---------------- git / gh の呼び出し ----------------

export interface Runner { (cmd: string, args: readonly string[], opts?: { cwd?: string; allowFail?: boolean }): { code: number; out: string; err: string } }

export const run: Runner = (cmd, args, opts = {}) => {
  const r = spawnSync(cmd, args as string[], { cwd: opts.cwd, encoding: 'utf8', maxBuffer: 64 << 20 });
  const res = { code: r.status ?? 1, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
  if (res.code !== 0 && !opts.allowFail) throw new Error(`${cmd} ${args.join(' ')} が失敗しました（${res.code}）\n${res.err || res.out}`);
  return res;
};

export const git = (args: readonly string[], opts: { cwd?: string; allowFail?: boolean } = {}) => run('git', args, opts);

/**
 * a と b を合わせたときに競合するファイルの一覧（作業フォルダは触らない）
 *   git merge-tree --write-tree --name-only --no-messages a b
 *   → 1行目は合わせた結果の tree、2行目以降が競合したファイル。競合が無ければ終了コード 0
 */
export function mergeConflicts(a: string, b: string, cwd?: string): string[] {
  const r = git(['merge-tree', '--write-tree', '--name-only', '--no-messages', a, b], { cwd, allowFail: true });
  if (r.code === 0) return [];
  if (r.code !== 1) throw new Error(`git merge-tree が失敗しました: ${r.err || r.out}`);
  return [...new Set(r.out.split('\n').slice(1).map((s) => s.trim()).filter(Boolean))];
}

/**
 * いまの枝に ref を取り込む（git merge）。APPEND_ONLY の競合は両方残して自動で解消し、コミットする。
 * それ以外の競合が残ったら merge を取り消して、そのファイル一覧を返す（作業フォルダは元のまま）。
 */
export function mergeWithAutoResolve(ref: string, message: string, opts: { cwd?: string; appendOnly?: readonly string[] } = {}):
  { ok: true; merged: boolean; autoResolved: string[] } | { ok: false; manual: string[] } {
  const appendOnly = opts.appendOnly ?? APPEND_ONLY;
  const before = git(['rev-parse', 'HEAD'], { cwd: opts.cwd }).out;
  const r = git(['merge', '--no-ff', '--no-edit', '-m', message, ref], { cwd: opts.cwd, allowFail: true });
  if (r.code === 0) {
    const after = git(['rev-parse', 'HEAD'], { cwd: opts.cwd }).out;
    return { ok: true, merged: after !== before, autoResolved: [] };
  }
  const conflicted = git(['diff', '--name-only', '--diff-filter=U'], { cwd: opts.cwd, allowFail: true }).out.split('\n').filter(Boolean);
  if (!conflicted.length) { // 競合ではない失敗（未コミットの変更がある など）
    git(['merge', '--abort'], { cwd: opts.cwd, allowFail: true });
    throw new Error(`git merge ${ref} が失敗しました: ${r.err || r.out}`);
  }
  const manual = conflicted.filter((f) => !appendOnly.includes(f));
  if (manual.length) { git(['merge', '--abort'], { cwd: opts.cwd, allowFail: true }); return { ok: false, manual }; }
  const root = git(['rev-parse', '--show-toplevel'], { cwd: opts.cwd }).out;
  for (const f of conflicted) {
    const p = `${root}/${f}`;
    const fixed = resolveUnion(readFileSync(p, 'utf8'), f.endsWith('UI_CHANGELOG.md') ? '---' : '');
    if (hasConflictMarkers(fixed)) { git(['merge', '--abort'], { cwd: opts.cwd, allowFail: true }); return { ok: false, manual: [f] }; }
    writeFileSync(p, fixed);
    git(['add', '--', f], { cwd: opts.cwd });
  }
  git(['commit', '--no-edit', '-m', `${message}（${conflicted.join('・')} の追記どうしの競合は両方残して自動解消）`], { cwd: opts.cwd });
  return { ok: true, merged: true, autoResolved: conflicted };
}

export interface OpenPr { number: number; title: string; headRefName: string; baseRefName: string; isCrossRepository: boolean; author: string }

export function listOpenPrs(base: string, cwd?: string): OpenPr[] {
  const r = run('gh', ['pr', 'list', '--state', 'open', '--base', base, '--limit', '100', '--json', 'number,title,headRefName,baseRefName,isCrossRepository,author'], { cwd });
  return (JSON.parse(r.out || '[]') as (Omit<OpenPr, 'author'> & { author: { login: string } })[]).map((p) => ({ ...p, author: p.author?.login ?? '' }));
}

/** PR の先端を refs/remotes/origin/pr/<番号> に取ってくる（フォークからの PR も取れる） */
export function fetchPrHead(n: number, cwd?: string): string {
  const ref = `refs/remotes/origin/pr/${n}`;
  git(['fetch', '-q', 'origin', `+refs/pull/${n}/head:${ref}`], { cwd });
  return ref;
}

/** この枝の PR がすでにあれば番号を返す */
export function existingPrFor(branch: string, cwd?: string): number | null {
  const r = run('gh', ['pr', 'list', '--state', 'open', '--head', branch, '--json', 'number', '-q', '.[0].number'], { cwd, allowFail: true });
  const n = Number(r.out);
  return r.code === 0 && Number.isInteger(n) && n > 0 ? n : null;
}

export interface PrConflictReport { pr: OpenPr; files: string[]; kind: ConflictKind }

/** head と、開いている各 PR（自分の PR は除く）との競合 */
export function conflictsWithOpenPrs(head: string, prs: readonly OpenPr[], selfBranch: string, cwd?: string): PrConflictReport[] {
  return prs.filter((p) => p.headRefName !== selfBranch || p.isCrossRepository).map((pr) => {
    const ref = fetchPrHead(pr.number, cwd);
    const files = mergeConflicts(head, ref, cwd);
    return { pr, files, kind: classify(files) };
  });
}

/** PR の説明に付け足す「競合の確認」欄 */
export function conflictSection(base: string, reports: readonly PrConflictReport[], included: readonly number[], autoWithMain: readonly string[]): string {
  const lines = ['', '## 競合の確認（npm run pr:create が自動で記入）', `- ${base}：最新の ${base} を取り込み済み・競合なし` + (autoWithMain.length ? `（${autoWithMain.join('・')} の追記どうしは両方残して自動解消）` : '')];
  for (const n of included) lines.push(`- #${n}：この PR に取り込み済み（**#${n} を先に、または一緒にマージ**）`);
  const others = reports.filter((r) => !included.includes(r.pr.number));
  if (!others.length) lines.push('- 開いている他の PR：なし');
  for (const r of others) {
    if (r.kind === 'none') lines.push(`- #${r.pr.number}（${r.pr.title.slice(0, 40)}）：競合なし`);
    else if (r.kind === 'auto') lines.push(`- #${r.pr.number}：${r.files.join('・')} の追記が重なる。あとからマージする方で \`npm run pr:sync -- --pr <番号>\` を実行すれば自動で解消`);
    else lines.push(`- #${r.pr.number}：⚠ ${r.files.join('・')} が競合（--allow-conflict で作成。どちらを先にマージするか要判断）`);
  }
  return lines.join('\n') + '\n';
}

export const readText = (p: string) => readFileSync(p, 'utf8');
export const sh = (cmd: string) => execFileSync('bash', ['-lc', cmd], { encoding: 'utf8' });
