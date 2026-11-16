/**
 * ===================================================================
 * 英文法カード演習・コンパクト結果解説用の非破壊変換アダプタ
 * ===================================================================
 *
 * ■ 最重要の設計原則（既存ユーザーの学習記録を100%保護）
 *   ・単元ID（`eg6_1`〜`eg6_20` 等）、大問ID（`q_eg6_1_set1` 等）、
 *     小問ID（`q_eg6_1_set1_1` 等）、選択肢の保存値（`①`/`②`/`③`/`④`）を
 *     1文字も変えない。
 *   ・教材データ本体（`englishGrammarData.ts` / `egV3Items.generated.ts`）も書き換えず、
 *     既存の `Problem` / `SubQuestion` / `explanationTracks` / `explanation` から
 *     描画用のカードモデルを純関数で取り出す。
 */
import type { AudioTrack, Problem, SubQuestion } from '../../types/curriculum';
import { isAnswerCorrect } from '../../utils/answerJudge';

const GRAMMAR_CHAPTER_RE = /^eg\d+_\d+$/;
const LONG_CHOICE_CHARS = 24;

export interface DialogueTurn {
  speaker: string;
  text: string;
}

export interface GrammarChoiceDetail {
  mark: string;
  numberLabel: string;
  text: string;
  correct: boolean;
  reason: string;
}

export interface GrammarResolvedCue {
  n: number;
  phrase: string;
  /** 問題文（空所 `______` を残した stem）の中での開始位置 */
  start: number;
  /** 要点（`why`）の中で対応する語句とその開始位置 */
  anchor: string;
  whyStart: number;
}

export interface GrammarMarkedPiece {
  text: string;
  cue?: number;
}

export interface GrammarParsedCard {
  sq: SubQuestion;
  displayNo: number;
  focusLabel: string;
  stem: string;
  choiceTexts: string[];
  correctAnswerMark: string;
  correctWord: string;
  completedSentence: string;
  translation: string;
  audioUrl?: string;
  keyPhrase?: { phrase: string; meaning: string };
  why: string;
  hint: string;
  rule: string;
  plus: string;
  examTip: string;
  memorizeSet: string;
  choices: GrammarChoiceDetail[];
  cues: GrammarResolvedCue[];
}

export interface GrammarSubReview extends GrammarParsedCard {
  chosen: string;
  status: 'correct' | 'wrong' | 'blank';
  filledWord: string;
}

export function isGrammarPageChapterId(chapterId: string | null | undefined): boolean {
  return Boolean(chapterId && GRAMMAR_CHAPTER_RE.test(chapterId));
}

export function prefersSingleColumnGrammarChoices(texts: readonly string[]): boolean {
  return texts.some((t) => String(t || '').trim().length > LONG_CHOICE_CHARS);
}

/**
 * 対話形式の英文を話者ピル（A / B 等）付きのターン配列に分解する。
 *
 * 対応パターン：
 *   1) `A: ... \n B: ...` の明示話者形式
 *   2) `“Hello. ...” “______ I'm Emma.”` の引用符2ターン以上の会話形式（英文法第1〜20章に207問収録）
 */
export function splitGrammarDialogueTurns(stem: string): DialogueTurn[] | null {
  const trimmed = String(stem || '').trim();
  if (!trimmed) return null;

  // パターン1: 行頭の `A: ...` / `B: ...`
  const lines = trimmed
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);
  if (lines.length >= 2) {
    const colonTurns: DialogueTurn[] = [];
    let allColon = true;
    for (const line of lines) {
      const m = line.match(/^([A-Z][a-zA-Z]{0,7})\s*[:：]\s*(.+)$/);
      if (!m) {
        allColon = false;
        break;
      }
      colonTurns.push({ speaker: m[1], text: m[2].trim() });
    }
    if (allColon && colonTurns.length >= 2) {
      return colonTurns;
    }
  }

  // パターン2: 引用符で囲まれた複数発話 `“...” “...”` または `"..." "..."`
  // 文の全体が引用符の連続で構成されているときだけ対話ターンとみなす（地の文の引用 `told us “...”` を誤判定しない）
  const quoteSegments: string[] = [];
  const quoteRe = /[“"]([^”"]+)[”"]/g;
  let cursor = 0;
  let match: RegExpExecArray | null = quoteRe.exec(trimmed);
  while (match !== null) {
    const gap = trimmed.slice(cursor, match.index).trim();
    if (gap.length > 0) {
      return null;
    }
    quoteSegments.push(match[1].trim());
    cursor = match.index + match[0].length;
    match = quoteRe.exec(trimmed);
  }
  if (quoteSegments.length >= 2 && trimmed.slice(cursor).trim().length === 0) {
    const speakers = ['A', 'B', 'A', 'B'];
    return quoteSegments.map((text, idx) => ({
      speaker: speakers[idx % speakers.length],
      text,
    }));
  }

  return null;
}

function unescapeHtmlText(raw: string): string {
  return raw
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .trim();
}

function markToNumberLabel(mark: string, index: number): string {
  const map: Record<string, string> = { '①': '1', '②': '2', '③': '3', '④': '4' };
  const trimmed = String(mark || '').trim();
  return map[trimmed] || trimmed.replace(/[()]/g, '') || String(index + 1);
}

/**
 * `problem.text` 内の `問N　... \n ① ... \n ② ... \n ③ ... \n ④ ...` ブロックを問番号ごとに抽出する。
 */
function parseProblemTextBlocks(problemText: string): Map<number, { stem: string; choices: string[] }> {
  const out = new Map<number, { stem: string; choices: string[] }>();
  const raw = String(problemText || '');
  const sections = raw.split(/─{4,}/);
  for (const sec of sections) {
    const lines = sec
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean);
    if (lines.length === 0) continue;
    const headMatch = lines[0].match(/^問\s*(\d+)[\s　]+(.+)$/);
    if (!headMatch) continue;
    const qNo = Number(headMatch[1]);
    const stemLines = [headMatch[2].trim()];
    const choices: string[] = [];
    for (let i = 1; i < lines.length; i += 1) {
      const choiceMatch = lines[i].match(/^(?:[①②③④]|\([1-4A-D]\)|[1-4]\.)\s*(.+)$/);
      if (choiceMatch) {
        choices.push(choiceMatch[1].trim());
      } else if (choices.length === 0) {
        stemLines.push(lines[i]);
      }
    }
    out.set(qNo, { stem: stemLines.join('\n'), choices });
  }
  return out;
}

function findTrackForSub(problem: Problem, sq: SubQuestion, qNo: number): AudioTrack | undefined {
  const tracks = problem.explanationTracks || problem.audioTracks || [];
  return (
    tracks.find((t) => t.subId === sq.id) ||
    tracks.find((t) => t.label === `問${qNo}`) ||
    tracks[qNo - 1]
  );
}

/**
 * `problem.explanation` 内の `<!--sq:subId-->` スライスから、
 * ポイント・着眼点・選択肢ごとの理由・入試のコツ・セット表現を構造化して取り出す。
 */
function parseGrammarExplanationSlice(
  explanationHtml: string,
  sqId: string,
  options: readonly string[],
  choiceTexts: readonly string[],
  correctAnswer: string,
): {
  hint: string;
  rule: string;
  plus: string;
  examTip: string;
  memorizeSet: string;
  choices: GrammarChoiceDetail[];
  fallbackTranslation: string;
} {
  const marker = `<!--sq:${sqId}-->`;
  const rawSlice = explanationHtml.includes(marker)
    ? (explanationHtml.split(marker)[1] || '').split('<!--sq:')[0]
    : explanationHtml;

  let fallbackTranslation = '';
  const trMatch = rawSlice.match(/border-top:1px dashed[^>]*>([\s\S]*?)<\/div>\s*<\/div>/);
  if (trMatch) {
    fallbackTranslation = unescapeHtmlText(trMatch[1]);
  }

  const afterScript = rawSlice.includes('<!--sqb-->') ? rawSlice.split('<!--sqb-->')[1] || rawSlice : rawSlice;
  // scriptBox ブロックを除いた解説行を解析
  const withoutScriptBox = afterScript.replace(
    /<!--lsn-script-first--><div[\s\S]*?<\/div><\/div>/,
    '',
  );

  let hint = '';
  let rule = '';
  let plus = '';
  let examTip = '';
  let memorizeSet = '';
  const choiceReasons = new Map<number, string>();

  const rawLines = withoutScriptBox
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean);

  for (const rawLine of rawLines) {
    const plain = unescapeHtmlText(rawLine);
    if (!plain || plain === '解説' || /^問\d+\s*正解は/.test(plain) || plain === '選択肢') continue;

    if (/^(?:【着眼点】|着眼点)/.test(plain)) {
      hint = plain.replace(/^(?:【着眼点】|着眼点)\s*/, '').trim();
      continue;
    }
    if (/^(?:【ポイント】|ポイント)/.test(plain)) {
      rule = plain.replace(/^(?:【ポイント】|ポイント)\s*/, '').trim();
      continue;
    }
    if (/^(?:【プラス】|プラス)/.test(plain)) {
      plus = plain.replace(/^(?:【プラス】|プラス)\s*/, '').trim();
      continue;
    }
    if (/^(?:【入試ではここ】|入試ではここ)/.test(plain)) {
      examTip = plain.replace(/^(?:【入試ではここ】|入試ではここ)\s*/, '').trim();
      continue;
    }
    if (/^(?:【セットで覚える】|セットで覚える)/.test(plain)) {
      memorizeSet = plain.replace(/^(?:【セットで覚える】|セットで覚える)\s*/, '').trim();
      continue;
    }

    const optMatch = plain.match(/^([①②③④])\s*(.+?)\s*[○×]\s*(.+)$/);
    if (optMatch) {
      const idx = ['①', '②', '③', '④'].indexOf(optMatch[1]);
      if (idx >= 0) {
        choiceReasons.set(idx, optMatch[3].trim());
      }
    }
  }

  const choices: GrammarChoiceDetail[] = options.map((mark, idx) => ({
    mark,
    numberLabel: markToNumberLabel(mark, idx),
    text: choiceTexts[idx] ?? mark,
    correct: mark === correctAnswer,
    reason: choiceReasons.get(idx) || '',
  }));

  return {
    hint,
    rule,
    plus,
    examTip,
    memorizeSet,
    choices,
    fallbackTranslation,
  };
}

const GRAMMAR_BLANK_RE = /_{3,}|\(\s*_{0,6}\s*\)/;

/**
 * 英文（`stem`）と要点解説（`why`）の両方に共通して現れる英語手がかり語句を最大2つ特定し、
 * 問題文と要点の双方に番号つきマーカー（`¹` `²`）を引ける座標へ変換する。
 */
export function resolveGrammarCues(stem: string, why: string): GrammarResolvedCue[] {
  if (!stem || !why) return [];
  const blankMatch = stem.match(GRAMMAR_BLANK_RE);
  const blankStart = blankMatch && blankMatch.index !== undefined ? blankMatch.index : -1;
  const blankEnd = blankStart >= 0 && blankMatch ? blankStart + blankMatch[0].length : -1;
  const jpHeadEnd =
    stem.includes('【並べかえ】') && stem.includes('」') ? stem.indexOf('」') + 1 : 0;

  const candidates: { phrase: string; whyStart: number; anchor: string }[] = [];
  const quoteRe = /[“"]([^”"]{1,42})[”"]|「([A-Za-z][^」]{0,42})」/g;
  let qm: RegExpExecArray | null = quoteRe.exec(why);
  while (qm !== null) {
    const raw = (qm[1] || qm[2] || '').trim().replace(/[.,]+$/, '');
    if (raw) {
      const innerStart = qm.index + qm[0].indexOf(raw);
      candidates.push({ phrase: raw, whyStart: innerStart, anchor: raw });
    }
    qm = quoteRe.exec(why);
  }

  const enRe = /[A-Za-z][A-Za-z0-9'’-]*(?:\s+[A-Za-z0-9'’-]+){0,4}/g;
  let em: RegExpExecArray | null = enRe.exec(why);
  while (em !== null) {
    const p = em[0].trim();
    if (p.length >= 2) {
      candidates.push({ phrase: p, whyStart: em.index, anchor: p });
    }
    em = enRe.exec(why);
  }

  const out: GrammarResolvedCue[] = [];
  for (const cand of candidates) {
    if (out.length >= 2) break;
    const p = cand.phrase;
    if (!p || /^(?:SV|SVO|SVC|SVOO|SVOC)$/.test(p)) continue;

    let searchFrom = jpHeadEnd;
    let foundAt = -1;
    while (true) {
      let idx = stem.indexOf(p, searchFrom);
      if (idx < 0) {
        idx = stem.toLowerCase().indexOf(p.toLowerCase(), searchFrom);
      }
      if (idx < 0) break;
      const end = idx + p.length;
      const overlapsBlank = blankStart >= 0 && idx < blankEnd && end > blankStart;
      const prevCh = idx > 0 ? stem[idx - 1] : '';
      const nextCh = end < stem.length ? stem[end] : '';
      const wordOk =
        !(/[A-Za-z]/.test(p[0]) && /[A-Za-z]/.test(prevCh)) &&
        !(/[A-Za-z]/.test(p[p.length - 1]) && /[A-Za-z]/.test(nextCh));
      const overlapsPrev = out.some((c) => idx < c.start + c.phrase.length && end > c.start);
      if (!overlapsBlank && wordOk && !overlapsPrev) {
        foundAt = idx;
        break;
      }
      searchFrom = idx + 1;
    }
    if (foundAt < 0) continue;

    const whyIdx = cand.whyStart;
    const overlapsWhy = out.some(
      (c) => whyIdx < c.whyStart + c.anchor.length && whyIdx + cand.anchor.length > c.whyStart,
    );
    if (overlapsWhy) continue;

    out.push({
      n: out.length + 1,
      phrase: stem.slice(foundAt, foundAt + p.length),
      start: foundAt,
      anchor: cand.anchor,
      whyStart: whyIdx,
    });
  }

  return out;
}

/** 文字列を通常部分と番号つき手がかり（`cue`）に分割する */
export function splitGrammarByMarks(
  text: string,
  marks: readonly { start: number; length: number; n: number }[],
): GrammarMarkedPiece[] {
  const sorted = marks
    .filter((m) => m.start >= 0 && m.length > 0 && m.start + m.length <= text.length)
    .slice()
    .sort((a, b) => a.start - b.start);
  const out: GrammarMarkedPiece[] = [];
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

export function grammarCueMarksInWhy(cues: readonly GrammarResolvedCue[]) {
  return cues.map((c) => ({ start: c.whyStart, length: c.anchor.length, n: c.n }));
}

/**
 * 1つの `GrammarProblem`（通常5問・復習フォーカス時は対象小問のみ）をカード一覧データへ変換する。
 */
export function parseGrammarProblemCards(
  problem: Problem,
  fallbackStartNo = 1,
): GrammarParsedCard[] {
  const blocks = parseProblemTextBlocks(problem.text || '');
  const subs = problem.subQuestions || [];

  return subs.map((sq, idx) => {
    const labelStr = String(sq.label || '');
    const noMatch = labelStr.match(/問\s*(\d+)/);
    const displayNo = noMatch ? Number(noMatch[1]) : fallbackStartNo + idx;
    const focusLabel = labelStr.replace(/^問\s*\d+\s*/, '').trim();

    const textBlock = blocks.get(displayNo) || blocks.get(idx + 1);
    const stem = textBlock?.stem || labelStr;
    const choiceTexts =
      sq.optionTexts && sq.optionTexts.length === sq.options.length
        ? [...sq.optionTexts]
        : textBlock?.choices && textBlock.choices.length === sq.options.length
        ? textBlock.choices
        : [...sq.options];

    const correctIdx = Math.max(0, sq.options.indexOf(sq.correctAnswer));
    const correctWord = choiceTexts[correctIdx] ?? sq.correctAnswer;

    const track = findTrackForSub(problem, sq, displayNo);
    const parsedExp = parseGrammarExplanationSlice(
      String(problem.explanation || ''),
      sq.id,
      sq.options,
      choiceTexts,
      sq.correctAnswer,
    );

    const completedSentence =
      track?.script?.trim() ||
      (stem.includes('______') ? stem.replace('______', correctWord) : stem);
    const translation = track?.translation?.trim() || parsedExp.fallbackTranslation || '';
    const keyPhrase = track?.keyPhrases?.[0];

    const correctChoiceReason = parsedExp.choices.find((c) => c.correct)?.reason || '';
    const oneLineClean = sq.oneLine
      ? sq.oneLine.replace(/^[^。]+。\s*/, '').trim()
      : '';
    const why = parsedExp.rule || correctChoiceReason || oneLineClean || parsedExp.hint;
    const cues = resolveGrammarCues(stem, why);

    return {
      sq,
      displayNo,
      focusLabel,
      stem,
      choiceTexts,
      correctAnswerMark: sq.correctAnswer,
      correctWord,
      completedSentence,
      translation,
      audioUrl: track?.audioUrl,
      keyPhrase: keyPhrase?.phrase ? { phrase: keyPhrase.phrase, meaning: keyPhrase.meaning || '' } : undefined,
      why,
      hint: parsedExp.hint,
      rule: parsedExp.rule,
      plus: parsedExp.plus,
      examTip: parsedExp.examTip,
      memorizeSet: parsedExp.memorizeSet,
      choices: parsedExp.choices,
      cues,
    };
  });
}

/**
 * 採点後の回答マップを突き合わせて `GrammarSubReview[]` を生成する。
 */
export function buildGrammarSubReviews(
  problem: Problem,
  answers: Record<string, string>,
  fallbackStartNo = 1,
): GrammarSubReview[] {
  return parseGrammarProblemCards(problem, fallbackStartNo).map((card) => {
    const chosen = answers[card.sq.id] || '';
    const ok = Boolean(chosen) && isAnswerCorrect(card.sq, chosen);
    const status: 'correct' | 'wrong' | 'blank' = !chosen ? 'blank' : ok ? 'correct' : 'wrong';
    const chosenIdx = chosen ? card.sq.options.indexOf(chosen) : -1;
    const filledWord = chosenIdx >= 0 ? card.choiceTexts[chosenIdx] ?? chosen : '';
    return {
      ...card,
      chosen,
      status,
      filledWord,
    };
  });
}
