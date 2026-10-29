/**
 * TOEIC Part 5 の演習画面：1ページに複数問・マーク式（2026-10-28）
 *
 * 紙の問題集に近い並び（問題番号・英文・(A)〜(D) を2×2）で、各選択肢の頭のマーク（丸）を塗って答える。
 * 採点はページ単位（「このページを採点する」）。最後のページを採点したら既存の結果画面へ進む。
 *
 * 既存の仕組みをそのまま使う（新しい保存形式は作らない）
 *   ・選んだ答え      … quizAnswersKey（Quiz と同じ保存先）。離脱しても消さない＝再開で復元する
 *   ・ページ位置      … quizStepKey（ページ先頭の問の番号を入れる）
 *   ・採点記録・XP    … createScoreCurrentQuestion（リスニング第4問以降の「1つの採点に複数の小問」と同じ使い方）
 *                       キーは「大問ID::ページ先頭の小問ID」。採点済みのページはここから分かる
 *   ・結果画面へ      … createQuizStepActions の終了処理（ステージ記録・章ベスト送信・onFinish）
 * 共通の ProblemPane / AnswerPane / MultipleChoiceControl / QuizHeader は使わない（リスニング・英文法に影響させない）。
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useMountEffect } from '../../hooks/useMountEffect';
import { ArrowLeft, Check, CheckCircle2, ChevronLeft, ChevronRight, FileText, ListChecks, MinusCircle, XCircle } from 'lucide-react';
import type { Chapter, Problem, SubQuestion } from '../../types/curriculum';
import type { ScoreBreakdown } from '../../utils/scoring';
import { QuizTimerBar } from '../QuizTimerBar';
import { FloatingScoreAnimation } from '../FloatingScoreAnimation';
import { createScoreCurrentQuestion } from '../../utils/quizScoring';
import { createQuizStepActions } from '../../utils/quizNavigationActions';
import { loadRun, type ChapterRunState } from '../../utils/quizRunState';
import { resolveQuizRange } from '../../utils/quizRange';
import { quizAnswersKey, quizIndexKey, quizStepKey } from '../../utils/quizStorageKeys';
import { parseStoredNonNegativeInteger, parseStoredStringRecord } from '../../utils/progress';
import { safeGetItem, safeRemoveItem } from '../../utils/safeLocalStorage';
import { safeSetItem } from '../../utils/storageGuard';
import { isAnswerCorrect } from '../../utils/answerJudge';
import { confirmAction } from '../../utils/dialog';
import { formatText } from '../../utils/textFormatter';
import {
  QUESTIONS_PER_PAGE, countUnanswered, pageFromStoredStep, pageScoreKey, prefersSingleColumn, splitPages, toeicExplanationFor,
} from './toeicPageModel';
import './toeic-page.css';

export interface ToeicPageQuizProps {
  mode: 'mini_test' | 'practice';
  chapter: Chapter;
  onFinish: (answers: Record<string, string>, result?: ChapterRunState) => void;
  onBack: () => void;
  onReturnToBattle?: () => void;
  isGuest: boolean;
  onExplanationChange?: (isExplanation: boolean) => void;
  onScored?: (breakdown: ScoreBreakdown, meta: { timeLimit: number; timeUsed: number; questionId: string }) => void;
  questionRange?: { startIndex: number; endIndex: number } | null;
}

/** キー → 選択肢の位置（A〜D と 1〜4） */
const MARK_KEYS: Record<string, number> = { a: 0, b: 1, c: 2, d: 3, '1': 0, '2': 1, '3': 2, '4': 3 };
const markLetter = (mark: string) => mark.replace(/[()]/g, '');
const noop = () => undefined;

/** 問の英文（空所 ______ のまま）。元データから引けないときは問題文の「問N　…」の行から取る */
function stemOf(problem: Problem, sq: SubQuestion): string {
  const ex = toeicExplanationFor(sq);
  if (ex) return ex.sentence;
  const label = String(sq.label || '');
  const line = String(problem.text || '').split('\n').find((l) => l.startsWith(`${label}　`));
  return line ? line.slice(label.length + 1) : '';
}

/**
 * 英文の空所 ______ を「太い下線の枠」にして描く。選んだ語があれば空所に入れて見せる（紙ではできない確認）。
 * 読み上げでは「空所」または選んだ語として読む。
 */
function StemWithBlank({ stem, filled, result }: { stem: string; filled: string; result?: 'right' | 'wrong' }) {
  const [before, after] = stem.split('______');
  if (after === undefined) return <>{formatText(stem, [], { prose: true })}</>;
  return (
    <>
      {before && formatText(before, [], { prose: true })}
      <span className="tp-blank" data-filled={filled ? true : undefined} data-result={result} data-toeic-blank>
        {filled ? formatText(filled, [], { prose: true }) : <span className="tp-sr">空所</span>}
      </span>
      {after && formatText(after, [], { prose: true })}
    </>
  );
}

/** 問題番号（1〜30）。復習ノートの解き直しで間違えた問だけに絞られても、元の番号（問N）を出す */
function questionNumber(sq: SubQuestion, fallback: number): number {
  const m = String(sq.label || '').match(/(\d+)/);
  return m ? Number(m[1]) : fallback;
}

export function ToeicPageQuiz({
  mode, chapter, onFinish, onBack, onReturnToBattle, isGuest, onExplanationChange, onScored, questionRange,
}: ToeicPageQuizProps) {
  const questions: Problem[] = mode === 'mini_test' ? (chapter.miniTest || []) : (chapter.practiceProblems || []);
  const [run, setRun] = useState<ChapterRunState>(() => loadRun(chapter.id, mode));
  const [answers, setAnswers] = useState<Record<string, string>>(() =>
    parseStoredStringRecord(safeGetItem(quizAnswersKey(chapter.id, mode))));
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(() =>
    parseStoredNonNegativeInteger(safeGetItem(quizIndexKey(chapter.id, mode)), Math.max(0, questions.length - 1)));
  const { rangeStart, rangeEnd } = resolveQuizRange(questions.length, questionRange, currentQuestionIndex);
  const currentQuestion = questions[currentQuestionIndex];
  const subs: SubQuestion[] = useMemo(() => currentQuestion?.subQuestions || [], [currentQuestion]);
  const pages = useMemo(() => splitPages(subs, QUESTIONS_PER_PAGE), [subs]);
  const [pageIndex, setPageIndex] = useState(() => pageFromStoredStep(
    parseStoredNonNegativeInteger(safeGetItem(quizStepKey(chapter.id, mode))),
    Math.ceil(Math.max(1, subs.length) / QUESTIONS_PER_PAGE),
  ));
  const safePage = Math.min(Math.max(0, pageIndex), Math.max(0, pages.length - 1));
  const page = useMemo(() => pages[safePage] || [], [pages, safePage]);
  const isScored = (i: number) => !!(currentQuestion && pages[i] && run.perStep?.[pageScoreKey(currentQuestion, pages[i])]);
  const pageScored = isScored(safePage);
  const allScored = pages.length > 0 && pages.every((_, i) => isScored(i));
  const isLastPage = safePage >= pages.length - 1;
  const hasNextRound = currentQuestionIndex < rangeEnd;
  const answeredCount = subs.filter((sq) => !!answers[sq.id]).length;
  const unanswered = countUnanswered(page, answers);
  const pageCorrect = page.filter((sq) => isAnswerCorrect(sq, answers[sq.id] || '')).length;

  // 保存（Quiz と同じキー）
  useEffect(() => { safeSetItem(quizAnswersKey(chapter.id, mode), JSON.stringify(answers)); }, [answers, chapter.id, mode]);
  useEffect(() => { safeSetItem(quizStepKey(chapter.id, mode), String(safePage * QUESTIONS_PER_PAGE)); }, [safePage, chapter.id, mode]);
  useEffect(() => { safeSetItem(quizIndexKey(chapter.id, mode), String(currentQuestionIndex)); }, [currentQuestionIndex, chapter.id, mode]);
  // App 側の「解説表示中」は使わない（この画面の中で解説を開く）。開いた時に1回だけ伝える
  //   親の関数は描画ごとに作り直されるので、マウント時の1回だけでよい（useMountEffect＝useEffect(fn, []) と同じ動き・R-23）
  useMountEffect(() => { onExplanationChange?.(false); });

  // 時間：上には回の通し（現行の10分）を出す。ページの採点には「前の採点からの経過」を渡す
  const elapsedRef = useRef(0);
  const pageStartRef = useRef(0);
  const timeUsedRef = useRef(0);
  const lastScoredQuestionRef = useRef<string | null>(null);
  const roundLimit = Number(currentQuestion?.timeLimitSec) > 0 ? Math.round(Number(currentQuestion?.timeLimitSec)) : 600;
  const pageLimit = Math.max(30, Math.round(roundLimit * (page.length / Math.max(1, subs.length))));

  // 点数の演出（従来の1問ごとの演出を、ページを採点するたびに1回出す）
  const [scoreFx, setScoreFx] = useState<{ breakdown: ScoreBreakdown; totalScore: number } | null>(null);
  const [showFx, setShowFx] = useState(false);
  useEffect(() => {
    if (!showFx) return undefined;
    const t = window.setTimeout(() => setShowFx(false), 3500);
    return () => window.clearTimeout(t);
  }, [showFx]);

  // 「未回答」の印は、採点ボタンを押したあとだけ出す（開いた直後に全問へ警告が並ばないように）
  const [attempted, setAttempted] = useState<Record<number, boolean>>({});
  const listRef = useRef<HTMLDivElement | null>(null);
  const groupRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const scrollTop = () => listRef.current?.scrollTo({ top: 0 });

  const scorePage = createScoreCurrentQuestion({
    currentQuestion, perStep: true, activeStepSub: page[0] ?? null, activeStepSubs: page,
    run, setRun, lastScoredQuestionRef, timeUsedRef, answers, questionTimeLimit: pageLimit,
    chapter, mode, isGuest, currentQuestionIndex, onScored,
  });

  // 結果画面へ（既存の終了処理をそのまま使う：ステージ記録・章ベスト送信・ランの片づけ・onFinish）
  const { handleNext: finishRound } = createQuizStepActions({
    chapter, mode, isGuest, questions, answers, questionRange, rangeStart, rangeEnd,
    currentQuestionIndex, perStep: false, isLastStep: true, isLastQuestion: true, safeStepIndex: 0, showingExplanation: true,
    scoreCurrentQuestionIfNeeded: () => null, setScoreAnimationData: noop, setShowScoreAnimation: noop,
    setShowingExplanation: noop, setStepIndex: noop, setCurrentQuestionIndex, onExplanationChange,
    onFinish: (finalAnswers, result) => {
      // 同じ回をもう一度開いたとき、終わった回の答えとページが残らないようにする
      safeRemoveItem(quizAnswersKey(chapter.id, mode));
      safeRemoveItem(quizStepKey(chapter.id, mode));
      onFinish(finalAnswers, result);
    },
  });

  const select = (sq: SubQuestion, mark: string) => {
    if (pageScored) return; // 採点後は変えられない
    setAnswers((prev) => {
      const next = { ...prev };
      if (next[sq.id] === mark) delete next[sq.id]; // 選んだ答えをもう一度押すと外す
      else next[sq.id] = mark;
      return next;
    });
  };

  const handleScore = () => {
    if (pageScored || page.length === 0) return;
    setAttempted((prev) => ({ ...prev, [safePage]: true }));
    if (unanswered > 0 && !confirmAction(`未回答が${unanswered}問あります。採点しますか？`)) return;
    timeUsedRef.current = Math.max(0, elapsedRef.current - pageStartRef.current);
    const scored = scorePage();
    pageStartRef.current = elapsedRef.current;
    if (scored) {
      setScoreFx({ breakdown: scored.breakdown, totalScore: scored.addedScore });
      setShowFx(true);
    }
    scrollTop();
  };

  const goPage = (i: number) => {
    setPageIndex(Math.min(Math.max(0, i), Math.max(0, pages.length - 1)));
    scrollTop();
  };

  const handleForward = () => {
    if (!pageScored) { handleScore(); return; }
    if (!isLastPage) { goPage(safePage + 1); return; }
    if (hasNextRound) {
      // 範囲が複数の回にまたがるとき（復習ノートからの解き直しなど）は次の回の1ページ目へ
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setPageIndex(0);
      lastScoredQuestionRef.current = null;
      scrollTop();
      return;
    }
    finishRound();
  };

  // キーボード：問題の枠にフォーカスがあるとき A〜D（1〜4）で選ぶ／↑↓で前後の問題へ
  const onGroupKeyDown = (e: React.KeyboardEvent<HTMLDivElement>, sq: SubQuestion, idx: number) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key.toLowerCase();
    if (k in MARK_KEYS) {
      const mark = sq.options[MARK_KEYS[k]];
      if (mark) { e.preventDefault(); select(sq, mark); }
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      const target = page[idx + (e.key === 'ArrowDown' ? 1 : -1)];
      if (target) { e.preventDefault(); groupRefs.current[target.id]?.focus(); }
    }
  };

  if (!currentQuestion || subs.length === 0) {
    return (
      <div className="tp-root" data-toeic-page-quiz>
        <p className="tp-empty">この回の問題は準備中です。</p>
        <button type="button" className="tp-btn tp-btn-sub" onClick={onBack}>戻る</button>
      </div>
    );
  }

  const forwardLabel = !pageScored ? 'このページを採点する' : !isLastPage ? '次のページ' : hasNextRound ? '次の回へ' : '結果を見る';

  return (
    <div className="tp-root" data-toeic-page-quiz>
      {onReturnToBattle && <button type="button" onClick={onReturnToBattle} className="tp-battle-return">バトル結果・解説に戻る</button>}
      <header className="tp-head" data-quiz-header>
        <button type="button" className="tp-back" onClick={onBack} aria-label="単元選択に戻る" title="単元選択に戻る">
          <ArrowLeft size={18} aria-hidden="true" />
        </button>
        <span className="tp-mode">{mode === 'mini_test' ? '小テスト' : '演習'}</span>
        <h2 className="tp-title">{chapter.abstractTitle}</h2>
        <dl className="tp-stats">
          <div title="いまのページ／全ページ">
            <dt><FileText size={14} aria-hidden="true" /><span className="tp-sr">ページ</span></dt>
            <dd data-toeic-page-pos><b>{safePage + 1}</b>/{pages.length}<small>ページ</small></dd>
          </div>
          <div title="答えた問題／全問題">
            <dt><ListChecks size={14} aria-hidden="true" /><span className="tp-sr">回答済み</span></dt>
            <dd data-toeic-answered><b>{answeredCount}</b>/{subs.length}<small>問</small></dd>
          </div>
        </dl>
      </header>
      <div className="tp-timer">
        <QuizTimerBar timeLimit={roundLimit} running={!allScored} onTick={(e) => { elapsedRef.current = e; }}
          resetKey={`${chapter.id}_${currentQuestionIndex}`} />
      </div>

      <div className="tp-scroll" ref={listRef}>
        {pageScored && (
          <p className="tp-page-result" role="status" data-toeic-page-result data-perfect={pageCorrect === page.length || undefined}>
            <CheckCircle2 size={20} aria-hidden="true" />
            <span>このページの正解</span>
            <b>{pageCorrect}</b><span>/{page.length}問</span>
          </p>
        )}
        <div className="tp-list" data-toeic-page={safePage + 1}>
          {page.map((sq, idx) => {
            const no = questionNumber(sq, subs.indexOf(sq) + 1);
            const chosen = answers[sq.id] || '';
            const texts = sq.optionTexts || [];
            const ok = pageScored && isAnswerCorrect(sq, chosen);
            const status = !pageScored
              ? (chosen ? 'answered' : attempted[safePage] ? 'unanswered' : 'todo')
              : !chosen ? 'blank' : ok ? 'correct' : 'wrong';
            const filled = chosen ? (texts[sq.options.indexOf(chosen)] ?? '') : '';
            const ex = pageScored ? toeicExplanationFor(sq) : null;
            const labelId = `tp-q-${sq.id}`;
            return (
              <article key={sq.id} className="tp-item" data-status={status} data-toeic-question={no}>
                <p className="tp-sentence" id={labelId}>
                  <span className="tp-no" aria-hidden="true">{no}</span>
                  <span className="tp-sr">問{no}　</span>
                  <StemWithBlank stem={stemOf(currentQuestion, sq)} filled={filled}
                    result={pageScored && chosen ? (ok ? 'right' : 'wrong') : undefined} />
                  {(status === 'unanswered' || status === 'blank') && <span className="tp-tag" data-toeic-unanswered>未回答</span>}
                </p>
                <div
                  role="radiogroup"
                  aria-labelledby={labelId}
                  aria-disabled={pageScored || undefined}
                  tabIndex={0}
                  ref={(el) => { groupRefs.current[sq.id] = el; }}
                  onKeyDown={(e) => onGroupKeyDown(e, sq, idx)}
                  className={`tp-choices${prefersSingleColumn(texts) ? ' is-single' : ''}`}
                >
                  {sq.options.map((mark, i) => {
                    const checked = chosen === mark;
                    const isRight = pageScored && mark === sq.correctAnswer;
                    const isWrongPick = pageScored && checked && !isRight;
                    return (
                      <div
                        key={mark}
                        role="radio"
                        aria-checked={checked}
                        aria-disabled={pageScored || undefined}
                        aria-label={`${mark} ${texts[i] ?? ''}`}
                        tabIndex={-1}
                        className="tp-choice"
                        data-checked={checked || undefined}
                        data-result={isRight ? 'right' : isWrongPick ? 'wrong' : undefined}
                        onClick={() => select(sq, mark)}
                      >
                        <span className="tp-bubble" aria-hidden="true">{markLetter(mark)}</span>
                        {/* 「正解」「あなたの答え」は選択肢の下の行に出す（横に並べると長い語が1文字ずつ折れて縦に伸びるため） */}
                        <span className="tp-choice-body" aria-hidden="true">
                          <span className="tp-choice-text">{formatText(texts[i] ?? mark, [], { prose: true })}</span>
                          {isRight && <span className="tp-choice-note">正解</span>}
                          {isWrongPick && <span className="tp-choice-note">あなたの答え</span>}
                        </span>
                        {checked && !pageScored && <Check size={18} strokeWidth={3} className="tp-choice-check" aria-hidden="true" />}
                      </div>
                    );
                  })}
                </div>
                {pageScored && (
                  <p className="tp-judge" data-result={status}>
                    {status === 'correct' ? <CheckCircle2 size={18} aria-hidden="true" /> : status === 'wrong' ? <XCircle size={18} aria-hidden="true" /> : <MinusCircle size={18} aria-hidden="true" />}
                    <span>{status === 'correct' ? '○ 正解' : status === 'wrong' ? `× 不正解（正解は ${sq.correctAnswer}）` : `× 未回答（正解は ${sq.correctAnswer}）`}</span>
                  </p>
                )}
                {ex && (
                  <details className="tp-ex" data-toeic-explanation>
                    <summary>解説を見る</summary>
                    <p className="tp-ex-completed">{formatText(ex.completed, [], { prose: true })}</p>
                    <h4>正解の理由</h4>
                    <p>{ex.why}</p>
                    <h4>選択肢</h4>
                    <ul className="tp-ex-choices">
                      {ex.choices.map((c) => (
                        <li key={c.mark} data-correct={c.correct || undefined}>
                          <b>{c.mark} {c.text}</b>　{c.correct ? '○ 正解' : `× ${c.reason}`}
                        </li>
                      ))}
                    </ul>
                    <h4>和訳</h4>
                    <p>{ex.translation}</p>
                    {ex.keywords.length > 0 && <>
                      <h4>重要語句</h4>
                      <ul className="tp-ex-words">{ex.keywords.map((w) => <li key={w.en}><b>{w.en}</b>　{w.ja}</li>)}</ul>
                    </>}
                  </details>
                )}
              </article>
            );
          })}
        </div>
      </div>

      <footer className="tp-foot">
        <button type="button" className="tp-btn tp-btn-sub" onClick={() => goPage(safePage - 1)} disabled={safePage === 0}>
          <ChevronLeft size={18} aria-hidden="true" /><span>前のページ</span>
        </button>
        {!pageScored ? (
          <span className="tp-unanswered" aria-live="polite" data-toeic-unanswered-count>
            {unanswered > 0 ? `未回答 ${unanswered}問` : 'すべて回答済み'}
          </span>
        ) : (
          <span className="tp-foot-score" data-toeic-page-correct>正解 <b>{pageCorrect}</b>/{page.length}問</span>
        )}
        <button type="button" className="tp-btn tp-btn-main" onClick={handleForward} data-toeic-forward>
          <span>{forwardLabel}</span><ChevronRight size={18} aria-hidden="true" />
        </button>
      </footer>

      {scoreFx && <FloatingScoreAnimation breakdown={scoreFx.breakdown} totalScore={scoreFx.totalScore} isVisible={showFx} />}
    </div>
  );
}
