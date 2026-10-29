import { afterEach, describe, expect, it, vi } from 'vitest';
import { TOEIC_P5_ROUNDS } from '../src/data/toeic/toeicPart5Rounds';
import { TOEIC_P5_NOTES } from '../src/data/toeic/toeicPart5Notes';
import type { ToeicP5Item } from '../src/data/toeic/toeicPart5Kit';
import type { ToeicP5Note } from '../src/data/toeic/toeicPart5NoteTypes';
import { cueMarksInCompleted, resolveCues, splitByMarks, toeicExplanationFor } from '../src/components/toeic/toeicPageModel';
import { saveToeicNote, isToeicNoteSaved } from '../src/components/toeic/toeicNote';
import { toeicPart5Data } from '../src/data/toeic/toeicPart5Data';

/**
 * TOEIC Part 5 解説の追加項目（着眼点 h・ポイント r・TOEICでのコツ tip・手がかり cues）の検証（2026-10-29）
 * 決まりは docs/TOEIC_P5_GLOSSARY.md。空の項目は許す（画面は見出しごと出さない）。
 * 他の文章との5語連続一致は重いので scripts/check-toeic-notes.mts で確かめる。
 */
export const BANNED = /必ず|絶対|頻出|よく出る|定番|確実|間違いなく|合格|満点|スコアが上が|点が上が|得点アップ|毎回出る/;
/** スマホ幅（360px・14px）で3行に収まる長さ。全角1・半角0.5で数える */
export const MAX_WIDTH = 62;
export const textWidth = (s: string) => [...s].reduce((n, ch) => n + (/[\u0000-\u00ff]/.test(ch) ? 0.5 : 1), 0);

type Row = { round: number; index: number; item: ToeicP5Item; note: ToeicP5Note };
const rows: Row[] = TOEIC_P5_ROUNDS.flatMap((items, r) =>
  items.map((item, i) => ({ round: r + 1, index: i, item, note: TOEIC_P5_NOTES[r]?.[i] ?? {} })));
const id = (x: Row) => `第${x.round}回 問${x.index + 1}`;
const filled = rows.filter((x) => x.note.h || x.note.r || x.note.tip || (x.note.cues || []).length > 0);

/** 品詞の問題で「〜が入る」と言っている品詞が、問題の小分類と食い違っていないか */
function posConflict(x: Row): string | null {
  if (x.item.k !== '品詞') return null;
  const want = ['名詞', '形容詞', '副詞'].find((p) => x.item.t.startsWith(p));
  if (!want) return null;
  for (const text of [x.note.h, x.note.r]) {
    const said = [...String(text || '').matchAll(/(形容詞|副詞|名詞|動詞)(?:の|が|を)(?:入る|選ぶ|正解)/g)].map((m) => m[1]);
    const bad = said.find((p) => p !== want);
    if (bad) return `${bad} と書いている（正しくは ${want}）`;
  }
  return null;
}

/** 分野ごとに、ポイント（r）に入っているべき用語（どれか1つ） */
const SKILL_TERMS: Record<string, RegExp> = {
  品詞: /名詞|形容詞|副詞|動詞|分詞/,
  動詞の形: /時制|過去|現在|未来|完了|受動|能動|動名詞|不定詞|原形|分詞|主語|単数|複数|態|-ing|to/,
  前置詞: /前置詞|節|名詞|時|場所|期間|by|until|on|in|at|for|during|within/,
  接続詞: /接続詞|節|前置詞|理由|譲歩|条件|逆接|対比|順接|目的/,
  代名詞: /格|代名詞|主語|目的語|単数|複数|名詞/,
  関係詞: /関係|先行詞|節/,
  比較: /比較|最上級|原級|倍|強調/,
};

describe('TOEIC Part 5 解説の追加項目', () => {
  it('回と問の数がデータと合う（多すぎない）', () => {
    expect(TOEIC_P5_NOTES.length).toBe(TOEIC_P5_ROUNDS.length);
    TOEIC_P5_NOTES.forEach((notes, r) => expect(notes.length).toBeLessThanOrEqual(TOEIC_P5_ROUNDS[r].length));
  });

  it('手がかりは問題文の中にあり、空所にかからず、正解の理由の語句と対応している', () => {
    const bad = filled.flatMap((x) => {
      const cues = x.note.cues || [];
      const ok = resolveCues(x.item.s, x.item.why, cues);
      return ok.length === cues.length ? [] : [`${id(x)}: ${cues.length - ok.length}件が対応しない`];
    });
    expect(bad).toEqual([]);
  });

  it('着眼点・ポイント・TOEICでのコツはスマホ幅で3行以内（全角換算62以下）', () => {
    const bad = filled.flatMap((x) => (['h', 'r', 'tip'] as const)
      .filter((k) => textWidth(String(x.note[k] || '')) > MAX_WIDTH)
      .map((k) => `${id(x)} ${k}: ${textWidth(String(x.note[k]))}`));
    expect(bad).toEqual([]);
  });

  it('使わない表現（必ず・頻出・合格できる など）が入っていない', () => {
    const bad = filled.flatMap((x) => (['h', 'r', 'tip'] as const)
      .filter((k) => BANNED.test(String(x.note[k] || ''))).map((k) => `${id(x)} ${k}`));
    expect(bad).toEqual([]);
  });

  it('同じ文面を使い回さない（3項目どれも全問で重複なし）', () => {
    for (const k of ['h', 'r', 'tip'] as const) {
      const seen = new Map<string, string>();
      const dup: string[] = [];
      for (const x of filled) {
        const v = String(x.note[k] || '').trim();
        if (!v) continue;
        if (seen.has(v)) dup.push(`${k}: ${seen.get(v)} と ${id(x)}`);
        else seen.set(v, id(x));
      }
      expect(dup).toEqual([]);
    }
  });

  it('正解の理由と矛盾しない：品詞の食い違い・分野の用語・誤答を正解と書いていないか（全問を機械的に照合）', () => {
    const bad: string[] = [];
    for (const x of filled) {
      const conflict = posConflict(x);
      if (conflict) bad.push(`${id(x)}: ${conflict}`);
      const term = SKILL_TERMS[x.item.k];
      if (term && x.note.r && !term.test(x.note.r)) bad.push(`${id(x)}: ポイントに分野（${x.item.k}）の用語が無い`);
      for (const [wrong] of x.item.w) {
        const esc = wrong.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const claim = new RegExp(`(^|[^A-Za-z])${esc}(?![A-Za-z])\\s*(が入る|を選ぶ|が正解|で決まり)`);
        for (const k of ['h', 'r', 'tip'] as const) if (claim.test(String(x.note[k] || ''))) bad.push(`${id(x)} ${k}: 誤答 ${wrong} を正解と書いている`);
      }
      // 正解の語を、誤答の理由として「入らない」と書いていないか
      const escC = x.item.c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      if (new RegExp(`(^|[^A-Za-z])${escC}(?![A-Za-z])\\s*は(入らない|使えない|合わない)`).test(`${x.note.h || ''}${x.note.r || ''}`)) bad.push(`${id(x)}: 正解 ${x.item.c} を否定している`);
    }
    expect(bad).toEqual([]);
  });

  it('解説の引き当てに追加項目と手がかりの位置が載る（画面で使う形）', () => {
    const problems = toeicPart5Data.parts[0].chapters[0].practiceProblems;
    for (const x of filled) {
      const sq = problems[x.round - 1].subQuestions[x.index];
      const ex = toeicExplanationFor(sq)!;
      expect(ex.hint).toBe((x.note.h || '').trim());
      expect(ex.rule).toBe((x.note.r || '').trim());
      expect(ex.tip).toBe((x.note.tip || '').trim());
      expect(ex.cues.length).toBe((x.note.cues || []).length);
      // 完成文（空所に正解）の中でも同じ語句を指す
      for (const m of cueMarksInCompleted(ex.sentence, x.item.c, ex.cues)) {
        const cue = ex.cues.find((c) => c.n === m.n)!;
        expect(ex.completed.slice(m.start, m.start + m.length)).toBe(cue.phrase);
      }
    }
  });
});

describe('手がかりの計算', () => {
  const s = 'Each of the managers ______ a copy of the revised schedule.';
  it('問題文の位置・何回目・正解の理由の日本語との対応', () => {
    const cues = resolveCues(s, '主語 Each of 〜 は単数扱い。改訂版の予定表。', [{ p: 'Each of', w: 'Each of' }, { p: 'revised schedule', w: '改訂版の予定表' }, { p: 'of', o: 3 }]);
    expect(cues.map((c) => [c.phrase, c.start, c.anchor])).toEqual([['Each of', 0, 'Each of'], ['revised schedule', 42, '改訂版の予定表']]);
  });
  it('空所にかかる・問題文に無い・他と重なる手がかりは捨てる', () => {
    expect(resolveCues(s, 'managers ______ a', [{ p: 'managers ______ a' }])).toEqual([]);
    expect(resolveCues(s, 'xyz', [{ p: 'xyz' }])).toEqual([]);
    expect(resolveCues(s, 'Each of the', [{ p: 'Each of the' }, { p: 'of the' }]).length).toBe(1);
  });
  it('文を「ふつうの文字」と「手がかり」に分ける', () => {
    expect(splitByMarks('abcdef', [{ start: 2, length: 2, n: 1 }])).toEqual([{ text: 'ab' }, { text: 'cd', cue: 1 }, { text: 'ef' }]);
  });
});

describe('ノートに保存（1問ずつ・同じ問題は1件だけ）', () => {
  afterEach(() => vi.unstubAllGlobals());
  it('2回押しても1件。復習リスト（review_list_*）には書かない', () => {
    const store: Record<string, string> = { notes_u1: JSON.stringify([{ id: 'old' }]) };
    vi.stubGlobal('localStorage', { getItem: (k: string) => store[k] ?? null, setItem: (k: string, v: string) => { store[k] = v; } });
    const problem = toeicPart5Data.parts[0].chapters[0].practiceProblems[0];
    const sq = problem.subQuestions[1];
    const ex = toeicExplanationFor(sq)!;
    const args = { uid: 'u1', chapter: { id: 'tp5_1', abstractTitle: 'Part 5 短文穴埋め', realTitle: 'Part 5' }, problem, sq, ex, questionNo: 2, roundNo: 1 };
    expect(saveToeicNote(args)).toBe(true);
    expect(saveToeicNote(args)).toBe(false);
    const notes = JSON.parse(store.notes_u1);
    expect(notes.map((n: { id: string }) => n.id)).toEqual(['old', `toeic_${sq.id}`]);
    expect(Object.keys(notes[1])).toEqual(['id', 'uid', 'question', 'answer', 'explanation', 'chapterTitle', 'questionIndex', 'chapterId', 'questionId', 'memo', 'createdAt', 'isImportant', 'reviewCount', 'tags', 'lastReviewedAt']);
    expect(notes[1].explanation).toContain('【正解の理由】');
    expect(isToeicNoteSaved('u1', sq.id)).toBe(true);
    expect(Object.keys(store).some((k) => k.startsWith('review_list_'))).toBe(false);
  });
});

describe('入力状況（失敗にはしない）', () => {
  it('追加項目のある問題の数を出す', () => {
    const count = (k: keyof ToeicP5Note) => rows.filter((x) => k === 'cues' ? (x.note.cues || []).length > 0 : !!x.note[k]).length;
    console.info(`[TOEIC notes] 全${rows.length}問 h:${count('h')} r:${count('r')} tip:${count('tip')} cues:${count('cues')}`);
    expect(rows.length).toBe(450);
  });
});
