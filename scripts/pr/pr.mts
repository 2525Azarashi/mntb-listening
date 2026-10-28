/**
 * PR を作る・最新にする道具（2026-10-28）
 *   「既存の PR があったら、その PR との競合を解消したうえで PR を作る」ための入口。
 *
 *   npm run pr:check                         いまの枝が main・開いている PR と競合するかを見るだけ（何も変えない）
 *   npm run pr:sync                          最新の main を取り込む（UI_CHANGELOG の追記どうしは自動で両方残す）
 *   npm run pr:sync -- --pr 116              PR #116 の変更もこの枝に取り込む（#116 が先にマージされる前提の PR にする）
 *   npm run pr:create -- --title "…" --body-file /tmp/body.md [--include 116] [--allow-conflict] [--skip-verify] [--base main]
 *
 *   pr:create の流れ
 *     1. 未コミットの変更が無いか、main の上で作業していないかを確かめる
 *     2. origin を取り直し、最新の main を取り込む（追記だけのファイルの競合は自動解消。ほかの競合は止める）
 *     3. --include の PR を取り込む（同じく自動解消できない競合は止める）
 *     4. 開いている他の PR と1つずつ競合を調べる
 *          - 競合なし → そのまま
 *          - UI_CHANGELOG の追記だけ → 説明に「あとからマージする方で pr:sync」と書いて続ける
 *          - それ以外 → 止める（--include でその PR を取り込むか、--allow-conflict で承知のうえ作る）
 *     5. tsc --noEmit（--skip-verify で省略）
 *     6. push → PR を作る（すでにあれば説明を更新）。説明の末尾に「競合の確認」欄を自動で足す
 *     説明（--body-file）に「リスニング納品の判断」が無いと作らない（CLAUDE.md の決まり）
 */
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  REQUIRED_BODY_HEADING, conflictSection, conflictsWithOpenPrs, existingPrFor, fetchPrHead, git, listOpenPrs,
  mergeConflicts, mergeWithAutoResolve, run, classify,
} from './prCore.mts';

type Args = { cmd: string; title?: string; bodyFile?: string; include: number[]; prs: number[]; allowConflict: boolean; skipVerify: boolean; base: string; draft: boolean };

function parse(argv: string[]): Args {
  const a: Args = { cmd: argv[0] || 'check', include: [], prs: [], allowConflict: false, skipVerify: false, base: 'main', draft: false };
  for (let i = 1; i < argv.length; i++) {
    const k = argv[i]; const v = () => { const x = argv[++i]; if (x === undefined) throw new Error(`${k} の値がありません`); return x; };
    if (k === '--title') a.title = v();
    else if (k === '--body-file') a.bodyFile = v();
    else if (k === '--include') a.include.push(...v().split(',').map(Number));
    else if (k === '--pr') a.prs.push(...v().split(',').map(Number));
    else if (k === '--allow-conflict') a.allowConflict = true;
    else if (k === '--skip-verify') a.skipVerify = true;
    else if (k === '--draft') a.draft = true;
    else if (k === '--base') a.base = v();
    else throw new Error(`知らないオプション: ${k}`);
  }
  for (const n of [...a.include, ...a.prs]) if (!Number.isInteger(n) || n <= 0) throw new Error(`PR 番号が正しくありません: ${n}`);
  return a;
}

const say = (s: string) => process.stdout.write(s + '\n');
const branch = () => git(['rev-parse', '--abbrev-ref', 'HEAD']).out;

function assertClean(base: string) {
  const b = branch();
  if (b === base || b === 'HEAD') throw new Error(`${b} の上では作れません。作業用の枝を切ってください（git checkout -b feat/…）`);
  const dirty = git(['status', '--porcelain', '--untracked-files=no']).out;
  if (dirty) throw new Error(`コミットしていない変更があります。先にコミットしてください:\n${dirty}`);
  return b;
}

/** main と --include の PR を取り込む。自動で解消できない競合があれば止める */
function syncInto(base: string, include: readonly number[]): string[] {
  git(['fetch', '-q', 'origin', base]);
  const auto: string[] = [];
  const m = mergeWithAutoResolve(`origin/${base}`, `merge: 最新の ${base} を取り込み`);
  if ('manual' in m) throw new Error(`最新の ${base} と競合しています（自動では決められないファイル）:\n  ${m.manual.join('\n  ')}\n→ git merge origin/${base} で手で直してから、もう一度実行してください`);
  if (m.merged) say(`✓ 最新の ${base} を取り込みました` + (m.autoResolved.length ? `（自動解消: ${m.autoResolved.join('・')}）` : ''));
  else say(`✓ ${base} は取り込み済み`);
  auto.push(...m.autoResolved);
  for (const n of include) {
    const ref = fetchPrHead(n);
    const r = mergeWithAutoResolve(ref, `merge: PR #${n} を取り込み（#${n} を先にマージする前提）`);
    if ('manual' in r) throw new Error(`PR #${n} と競合しています（自動では決められないファイル）:\n  ${r.manual.join('\n  ')}\n→ git merge ${ref} で手で直してから、もう一度実行してください`);
    say(`✓ PR #${n} を取り込みました` + (r.autoResolved.length ? `（自動解消: ${r.autoResolved.join('・')}）` : ''));
  }
  return auto;
}

function report(base: string, self: string) {
  git(['fetch', '-q', 'origin', base]);
  const withMain = mergeConflicts('HEAD', `origin/${base}`);
  const k = classify(withMain);
  say(`${base}: ` + (k === 'none' ? '競合なし' : k === 'auto' ? `追記だけの競合（pr:sync で自動解消）: ${withMain.join('・')}` : `⚠ 競合: ${withMain.join('・')}`));
  const reports = conflictsWithOpenPrs('HEAD', listOpenPrs(base), self);
  if (!reports.length) say('開いている他の PR: なし');
  for (const r of reports) say(`#${r.pr.number} ${r.pr.title.slice(0, 50)}: ` + (r.kind === 'none' ? '競合なし' : r.kind === 'auto' ? `追記だけ（自動解消できる）: ${r.files.join('・')}` : `⚠ 競合: ${r.files.join('・')}`));
  return { withMain, reports };
}

function main() {
  const a = parse(process.argv.slice(2));
  if (a.cmd === 'check') { report(a.base, branch()); return; }
  if (a.cmd === 'sync') { assertClean(a.base); syncInto(a.base, a.prs); report(a.base, branch()); return; }
  if (a.cmd !== 'create') throw new Error(`使い方: check | sync [--pr N] | create --title … --body-file …`);

  if (!a.title || !a.bodyFile) throw new Error('--title と --body-file が必要です');
  const body0 = readFileSync(a.bodyFile, 'utf8');
  if (!body0.includes(REQUIRED_BODY_HEADING)) throw new Error(`説明に「${REQUIRED_BODY_HEADING}」の欄がありません（CLAUDE.md の決まり：判断・理由・影響ファイル・引き継ぎ）`);
  const self = assertClean(a.base);

  const autoWithMain = syncInto(a.base, a.include);
  const reports = conflictsWithOpenPrs('HEAD', listOpenPrs(a.base), self).filter((r) => !a.include.includes(r.pr.number));
  const manual = reports.filter((r) => r.kind === 'manual');
  for (const r of reports) say(`#${r.pr.number}: ` + (r.kind === 'none' ? '競合なし' : r.kind === 'auto' ? `追記だけ（${r.files.join('・')}）` : `⚠ ${r.files.join('・')}`));
  if (manual.length && !a.allowConflict) {
    throw new Error('開いている PR と競合しています:\n' + manual.map((r) => `  #${r.pr.number} ${r.pr.title.slice(0, 40)}: ${r.files.join('・')}`).join('\n')
      + `\n→ その PR を先にマージする前提なら --include ${manual.map((r) => r.pr.number).join(',')}（その PR の変更をこの枝に取り込んで競合を解消）`
      + '\n→ 承知のうえ別々に出すなら --allow-conflict');
  }

  if (!a.skipVerify) { say('… tsc --noEmit'); run('npx', ['tsc', '--noEmit', '-p', '.']); say('✓ 型チェック成功'); }

  git(['push', '-u', 'origin', `HEAD:${self}`]);
  const body = body0.trimEnd() + '\n' + conflictSection(a.base, reports, a.include, autoWithMain);
  const tmp = join(mkdtempSync(join(tmpdir(), 'pr-')), 'body.md'); writeFileSync(tmp, body);
  const existing = existingPrFor(self);
  if (existing) {
    run('gh', ['pr', 'edit', String(existing), '--title', a.title, '--body-file', tmp]);
    say(`✓ 既存の PR #${existing} を更新しました`);
  } else {
    const r = run('gh', ['pr', 'create', '--base', a.base, '--head', self, '--title', a.title, '--body-file', tmp, ...(a.draft ? ['--draft'] : [])]);
    say(`✓ PR を作りました: ${r.out.split('\n').pop()}`);
  }
}

try { main(); } catch (e) { process.stderr.write(`✗ ${(e as Error).message}\n`); process.exit(1); }
