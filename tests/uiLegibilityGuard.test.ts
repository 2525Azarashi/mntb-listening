import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';

/*
 * CLAUDE.md の UI 原則（文字 12px 以上・タップ 44px 以上）と、
 * 2026-10-18 のご要望で直した画面が、後の変更で元に戻らないための見張り。
 * 実画面の検査は Playwright（/tmp/pw/walk.mjs 相当）で行い、ここでは
 * ソースに「12px 未満の Tailwind 指定」が再び入らないことだけを機械的に見る。
 */
const root = join(__dirname, '..');
const read = (p: string) => readFileSync(join(root, p), 'utf8');
const walk = (dir: string): string[] => readdirSync(join(root, dir)).flatMap((name) => {
  const rel = `${dir}/${name}`;
  return statSync(join(root, rel)).isDirectory() ? walk(rel) : [rel];
});

describe('文字の大きさ（12px 以上）', () => {
  it('src の TSX に text-[9〜11.xpx] の指定が無い', () => {
    const hits = walk('src')
      .filter((f) => f.endsWith('.tsx'))
      .flatMap((f) => [...read(f).matchAll(/text-\[(\d+(?:\.\d+)?)px\]/g)]
        .filter((m) => Number(m[1]) < 12)
        .map((m) => `${f}: ${m[0]}`));
    expect(hits).toEqual([]);
  });

  it('科目選択（listening-home.css）に 12px 未満の font-size が無い', () => {
    const sizes = [...read('src/components/listening-home.css').matchAll(/font-size:\s*(\d+(?:\.\d+)?)px/g)]
      .map((m) => Number(m[1]));
    expect(sizes.filter((v) => v < 12)).toEqual([]);
  });

  it('学習モード選択（.mode-*）に 12px 未満の font-size が無い', () => {
    const bad = read('src/index.css').split('\n')
      .filter((l) => /^\s*\.(mode-|mode-desk)/.test(l) || l.includes('.mode-desk '))
      .flatMap((l) => [...l.matchAll(/font-size:\s*(\d+(?:\.\d+)?)px/g)].filter((m) => Number(m[1]) < 12).map(() => l.trim().slice(0, 60)));
    expect(bad).toEqual([]);
  });
});

describe('2026-10-18 のご要望（リスニングの資料・フレンド）', () => {
  const materials = read('src/components/ListeningMaterials.tsx');
  it('第4問A：図は横スクロールにせず幅いっぱいで全体を見せ、タップで拡大できる', () => {
    expect(materials).not.toContain('横にスクロールして図全体を確認できます');
    expect(materials).not.toMatch(/style=\{\{\s*minWidth:\s*image\.minWidth/);
    expect(materials).toContain('data-material-zoom');
  });
  it('第4問B：条件表の空欄は ○ → × → 空欄 とタップで切り替えられる（44px）', () => {
    expect(materials).toContain("const NEXT_MARK: Record<string, string> = { '': '○', '○': '×', '×': '' };");
    expect(materials).toMatch(/data-material-mark[\s\S]{0,400}h-11/);
  });
  it('第6問B：長い設問文は小問バーで切らずに全文を出す', () => {
    const answer = read('src/components/AnswerPane.tsx');
    expect(answer).toContain('data-answer-prompt');
    expect(answer).toContain('!isLongBlankHint(cur.blankHint)');
  });
  it('フレンド：外枠はスクロールさせず、一覧だけが残りの高さを使う', () => {
    const friend = read('src/components/FriendPanel.tsx');
    expect(friend).toMatch(/h-full min-h-0 overflow-hidden flex flex-col friend-panel/);
    expect(friend).toMatch(/data-friend-list className="min-h-\[160px\] flex-1/);
  });
  it('通報・ブロック（…）ボタンは 44px 以上', () => {
    expect(read('src/index.css')).toMatch(/\.user-safety-trigger \{[^}]*min-width:44px; min-height:44px;/);
  });
});
