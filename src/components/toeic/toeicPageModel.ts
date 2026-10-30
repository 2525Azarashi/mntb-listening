/**
 * TOEIC Part 5「1ページに複数問・マーク式」演習の計算部分（2026-10-28）
 *
 * 画面（ToeicPageQuiz.tsx）から React を使わない計算だけを分けた。テストはここを直接たたく。
 *   ・ページ分け（QUESTIONS_PER_PAGE 問ずつ）
 *   ・選択肢を2×2にするか1列にするか
 *   ・解説の中身（正解の理由・他の選択肢の理由・和訳・重要語句）を問題データの元から引く
 *     ※ 問題データ（450問）は読むだけで、書き換えない
 */
import type { Problem, SubQuestion } from '../../types/curriculum';
import { answerPositions, fillBlank, placeChoices, TOEIC_P5_CHAPTER_ID, type ToeicP5Item } from '../../data/toeic/toeicPart5Kit';
import { TOEIC_P5_ROUNDS } from '../../data/toeic/toeicPart5Rounds';
import { toeicNoteAt } from '../../data/toeic/toeicPart5Notes';
import type { ToeicCue } from '../../data/toeic/toeicPart5NoteTypes';
import { stepScoreKey } from '../../utils/listeningSteps';

/** 1ページに並べる問題の数。変えるとページ数も自動で変わる（30問 ÷ 6 = 5ページ） */
export const QUESTIONS_PER_PAGE = 6;

/** 選択肢がこの文字数を超えたら、その問題だけ1列にする（2×2だと折り返して読みにくい） */
export const LONG_CHOICE_CHARS = 18;

/** TOEIC Part 5 の単元か（演習画面をこのページ式に切り替える条件） */
export function isToeicPageChapter(chapterId: string | undefined | null): boolean {
  return chapterId === TOEIC_P5_CHAPTER_ID;
}

/** 小問をページに分ける。最後のページは端数でもよい */
export function splitPages<T>(items: readonly T[], perPage = QUESTIONS_PER_PAGE): T[][] {
  const size = Math.max(1, Math.floor(perPage));
  const pages: T[][] = [];
  for (let i = 0; i < items.length; i += size) pages.push(items.slice(i, i + size));
  return pages;
}

/** その問題の選択肢を1列にするか（いちばん長い選択肢で決める） */
export function prefersSingleColumn(texts: readonly string[] | undefined): boolean {
  return (texts || []).some((t) => String(t).length > LONG_CHOICE_CHARS);
}

/** ページの採点記録のキー。既存の「大問ID::小問ID」と同じ形（ページ先頭の小問IDを使う） */
export function pageScoreKey(problem: Pick<Problem, 'id'>, page: readonly Pick<SubQuestion, 'id'>[]): string {
  return stepScoreKey(problem.id, page[0]?.id ?? '');
}

/** ページの未回答数 */
export function countUnanswered(page: readonly Pick<SubQuestion, 'id'>[], answers: Record<string, string>): number {
  return page.filter((sq) => !answers[sq.id]).length;
}

/** 保存しているページ位置（ページ先頭の問の番号）→ ページ番号。範囲外は丸める */
export function pageFromStoredStep(step: number, pageCount: number, perPage = QUESTIONS_PER_PAGE): number {
  const p = Math.floor(Math.max(0, step) / Math.max(1, perPage));
  return Math.min(Math.max(0, p), Math.max(0, pageCount - 1));
}

export interface ToeicChoiceNote {
  mark: string;
  text: string;
  correct: boolean;
  /** 不正解の選択肢が合わない理由（正解の選択肢は空） */
  reason: string;
}

export interface ToeicExplanation {
  /** 問題文（空所は ______ のまま） */
  sentence: string;
  /** 空所を埋めた完成文 */
  completed: string;
  /** 正解の理由 */
  why: string;
  choices: ToeicChoiceNote[];
  /** 和訳 */
  translation: string;
  /** 重要語句 */
  keywords: { en: string; ja: string }[];
  /** 分野（結果画面の集計と同じラベル） */
  skill: string;
  /** 小分類（例：名詞・時制）。分野タグに添える */
  subType: string;
  /** 着眼点・ポイント・TOEICでのコツ（任意。空なら画面に出さない） */
  hint: string;
  rule: string;
  tip: string;
  /** 手がかり（問題文と正解の理由の両方で位置が分かったものだけ。番号は1から） */
  cues: ResolvedCue[];
}

export interface ResolvedCue {
  n: number;
  phrase: string;
  /** 問題文（空所 ______ のまま）の中の位置 */
  start: number;
  /** 正解の理由の中で対応する語句と、その位置（最初に出てくるところ） */
  anchor: string;
  whyStart: number;
}

const BLANK = '______';

/** text の中で phrase が occurrence 回目に出てくる位置（無ければ -1） */
export function nthIndexOf(text: string, phrase: string, occurrence: number): number {
  let from = 0;
  let at = -1;
  for (let k = 0; k < Math.max(1, occurrence); k += 1) {
    at = text.indexOf(phrase, from);
    if (at < 0) return -1;
    from = at + phrase.length;
  }
  return at;
}

/**
 * 手がかりを問題文・正解の理由の中の位置に直す。
 * 次のどれかに当たるものは捨てる（画面では引かない。検証スクリプトでは失敗にする）
 *   ・問題文に無い／空所にかかる／他の手がかりと重なる
 *   ・正解の理由に対応する語句（w。省略時は p）が無い／理由の中で他の手がかりと重なる
 *     （理由で述べた根拠と対応しないマーカーは引かない）
 */
export function resolveCues(sentence: string, why: string, cues: readonly ToeicCue[] | undefined): ResolvedCue[] {
  const blankAt = sentence.indexOf(BLANK);
  const out: ResolvedCue[] = [];
  for (const cue of cues || []) {
    const phrase = cue?.p || '';
    const occ = cue?.o ?? 1;
    const anchor = cue?.w || phrase;
    if (!phrase.trim() || !anchor.trim()) continue;
    const start = nthIndexOf(sentence, phrase, occ);
    if (start < 0) continue;
    const end = start + phrase.length;
    if (blankAt >= 0 && start < blankAt + BLANK.length && end > blankAt) continue;
    if (out.some((c) => start < c.start + c.phrase.length && end > c.start)) continue;
    const whyStart = why.indexOf(anchor);
    if (whyStart < 0) continue;
    if (out.some((c) => whyStart < c.whyStart + c.anchor.length && whyStart + anchor.length > c.whyStart)) continue;
    out.push({ n: out.length + 1, phrase, start, anchor, whyStart });
  }
  return out;
}

/** 文を「ふつうの文字」と「手がかり（番号つき）」に分ける */
export interface MarkedPiece { text: string; cue?: number }
export function splitByMarks(text: string, marks: readonly { start: number; length: number; n: number }[]): MarkedPiece[] {
  const sorted = marks.filter((m) => m.start >= 0 && m.start + m.length <= text.length).slice().sort((a, b) => a.start - b.start);
  const out: MarkedPiece[] = [];
  let pos = 0;
  for (const m of sorted) {
    if (m.start < pos) continue;
    if (m.start > pos) out.push({ text: text.slice(pos, m.start) });
    out.push({ text: text.slice(m.start, m.start + m.length), cue: m.n });
    pos = m.start + m.length;
  }
  if (pos < text.length) out.push({ text: text.slice(pos) });
  return out;
}

/** 問題文の中の手がかりの位置を、空所に答えを入れた完成文の中の位置に直す */
export function cueMarksInCompleted(sentence: string, answer: string, cues: readonly ResolvedCue[]) {
  const blankAt = sentence.indexOf(BLANK);
  const shift = answer.length - BLANK.length;
  return cues.map((c) => ({ start: blankAt >= 0 && c.start > blankAt ? c.start + shift : c.start, length: c.phrase.length, n: c.n }));
}

/** 正解の理由の中の手がかりの位置 */
export function cueMarksInWhy(cues: readonly ResolvedCue[]) {
  return cues.map((c) => ({ start: c.whyStart, length: c.anchor.length, n: c.n }));
}

const SUB_ID = /_r(\d+)_(\d+)$/;

/**
 * 小問IDから、その問の英文と解説を問題データの元（ToeicP5Item）から引く。
 * 選択肢の並びはデータを作ったときと同じ決まり（answerPositions / placeChoices）で再現する。
 * 引けないとき（想定外のID）は null。画面は解説を出さずに続ける。
 */
export function toeicExplanationFor(sq: SubQuestion): ToeicExplanation | null {
  const m = String(sq.id).match(SUB_ID);
  if (!m) return null;
  const round = Number(m[1]);
  const index = Number(m[2]) - 1;
  const items: readonly ToeicP5Item[] | undefined = TOEIC_P5_ROUNDS[round - 1];
  const note = toeicNoteAt(round, index);
  const item = items?.[index];
  if (!items || !item) return null;
  const pos = answerPositions(round, items.length)[index];
  const placed = placeChoices(item, pos);
  const marks = sq.options || [];
  const texts = sq.optionTexts && sq.optionTexts.length === marks.length ? sq.optionTexts : placed.texts;
  return {
    sentence: item.s,
    completed: fillBlank(item.s, item.c),
    why: item.why,
    choices: marks.map((mark, i) => ({
      mark,
      text: texts[i] ?? '',
      correct: mark === sq.correctAnswer,
      reason: mark === sq.correctAnswer ? '' : (placed.reasons[i] || ''),
    })),
    translation: item.tr,
    keywords: item.kw.map(([en, ja]) => ({ en, ja })),
    skill: item.k,
    subType: item.t,
    hint: (note.h || '').trim(),
    rule: (note.r || '').trim(),
    tip: (note.tip || '').trim(),
    cues: resolveCues(item.s, item.why, note.cues),
  };
}
