/**
 * 英文法（第1〜20章）：1回（通常5問）を1ページのカード一覧で解き、一括採点・その場解説する画面
 *
 * ■ 既存データの完全引き継ぎ（記録を1件も消さない）
 *   ・章ID（`eg6_1`〜`eg6_20`）、大問ID（`q_eg6_1_set1`）、小問ID（`q_eg6_1_set1_1`）、
 *     選択肢の保存値（`①`/`②`/`③`/`④`）は従来と100%同一。
 *   ・選んだ答えは `quizAnswersKey(chapter.id, mode)`、消去法メモは `quizElimKey(chapter.id, mode)`、
 *     回位置は `quizIndexKey(chapter.id, mode)`、採点記録は `quizRunKey(chapter.id, mode)` に保存。
 *   ・採点は既存の `createScoreCurrentQuestion`、終了処理は `createQuizStepActions` をそのまま通すため、
 *     `solved_problems_v1_*` / `unit_stats_v1_*` / `stage_records_v1_*` / `review_list_*` /
 *     マナコイン・XP・章称号のすべてが従来どおり積み上がる。
 *   ・旧UIで途中（問2まで採点済みなど）だったユーザーがアップデート後に開いた場合も、
 *     すでに入力済みの答えをそのままカードに復元し、残りの問から続けて一括採点できる。
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useMountEffect } from '../../hooks/useMountEffect';
import {
  ArrowLeft,
  Check,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Clock,
  FileText,
  ListChecks,
  Slash,
  X,
} from 'lucide-react';
import type { Chapter, Problem, SubQuestion } from '../../types/curriculum';
import type { ScoreBreakdown } from '../../utils/scoring';
import { auth } from '../../firebase';
import { notify } from '../../utils/dialog';
import { FloatingScoreAnimation } from '../FloatingScoreAnimation';
import { CorrectBurst } from '../fx/CorrectBurst';
import { createScoreCurrentQuestion } from '../../utils/quizScoring';
import { createQuizStepActions } from '../../utils/quizNavigationActions';
import { loadRun, type ChapterRunState } from '../../utils/quizRunState';
import { resolveQuizRange } from '../../utils/quizRange';
import { readReviewFocus } from '../../utils/reviewFocus';
import {
  quizAnswersKey,
  quizElimKey,
  quizExplKey,
  quizIndexKey,
  quizStepKey,
} from '../../utils/quizStorageKeys';
import {
  parseStoredNonNegativeInteger,
  parseStoredStringRecord,
} from '../../utils/progress';
import { saveQuestionNote } from '../../utils/questionNote';
import {
  readJsonArray,
  safeGetItem,
  safeParseJson,
  safeRemoveItem,
} from '../../utils/safeLocalStorage';
import { safeSetItem } from '../../utils/storageGuard';
import { isAnswerCorrect } from '../../utils/answerJudge';
import { stepScoreKey } from '../../utils/listeningSteps';
import { formatText } from '../../utils/textFormatter';
import { logRejection } from '../../utils/reportError';
import {
  buildGrammarSubReviews,
  prefersMobileSingleColumnGrammarChoices,
  prefersSingleColumnGrammarChoices,
} from './grammarPageModel';
import {
  GrammarCompactReview,
  GrammarQuestionStem,
} from './GrammarQuestionCardParts';
import { stopGrammarSpeech } from './grammarSpeech';
import './grammar-page.css';

export interface GrammarPageQuizProps {
  mode: 'mini_test' | 'practice';
  chapter: Chapter;
  onFinish: (answers: Record<string, string>, result?: ChapterRunState) => void;
  onBack: () => void;
  onReturnToBattle?: () => void;
  isGuest: boolean;
  onExplanationChange?: (isExplanation: boolean) => void;
  onScored?: (
    breakdown: ScoreBreakdown,
    meta: { timeLimit: number; timeUsed: number; questionId: string },
  ) => void;
  questionRange?: { startIndex: number; endIndex: number } | null;
}

const MARK_KEYS: Record<string, number> = {
  '1': 0,
  '2': 1,
  '3': 2,
  '4': 3,
  a: 0,
  b: 1,
  c: 2,
  d: 3,
};

const noop = () => undefined;

function fmtClock(sec: number): string {
  const s = Math.max(0, Math.floor(sec));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}

export function GrammarPageQuiz({
  mode,
  chapter,
  onFinish,
  onBack,
  onReturnToBattle,
  isGuest,
  onExplanationChange,
  onScored,
  questionRange,
}: GrammarPageQuizProps) {
  const questions: Problem[] =
    mode === 'mini_test' ? chapter.miniTest || [] : chapter.practiceProblems || [];

  const [run, setRun] = useState<ChapterRunState>(() => loadRun(chapter.id, mode));
  const [answers, setAnswers] = useState<Record<string, string>>(() =>
    parseStoredStringRecord(safeGetItem(quizAnswersKey(chapter.id, mode))),
  );
  const [eliminated, setEliminated] = useState<Record<string, string[]>>(() => {
    const raw = safeParseJson<Record<string, unknown>>(
      safeGetItem(quizElimKey(chapter.id, mode)),
      {},
    );
    const out: Record<string, string[]> = {};
    if (raw && typeof raw === 'object') {
      for (const [k, v] of Object.entries(raw)) {
        if (Array.isArray(v)) out[k] = v.map(String);
      }
    }
    return out;
  });

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(() =>
    parseStoredNonNegativeInteger(
      safeGetItem(quizIndexKey(chapter.id, mode)),
      Math.max(0, questions.length - 1),
    ),
  );

  const hasReviewFocus = useMemo(() => {
    const f = readReviewFocus();
    return Boolean(f && f.chapterId === chapter.id);
  }, [chapter.id]);

  // 英文法は「1回（5問）＝1ステージ」。範囲未指定で開かれても復習ノートの絞り込み中でなければ1回ごとに区切る
  const effectiveRange = useMemo(
    () =>
      questionRange ??
      (hasReviewFocus
        ? null
        : { startIndex: currentQuestionIndex, endIndex: currentQuestionIndex }),
    [questionRange, hasReviewFocus, currentQuestionIndex],
  );

  const { rangeStart, rangeEnd } = resolveQuizRange(
    questions.length,
    effectiveRange,
    currentQuestionIndex,
  );

  useEffect(() => {
    if (currentQuestionIndex < rangeStart || currentQuestionIndex > rangeEnd) {
      setCurrentQuestionIndex(rangeStart);
    }
  }, [currentQuestionIndex, rangeStart, rangeEnd]);

  const currentQuestion = questions[currentQuestionIndex];
  const subs: SubQuestion[] = useMemo(
    () => currentQuestion?.subQuestions || [],
    [currentQuestion],
  );

  const reviews = useMemo(
    () => (currentQuestion ? buildGrammarSubReviews(currentQuestion, answers, 1) : []),
    [currentQuestion, answers],
  );

  // この回が採点済みか：
  // 1) 一括採点で先頭キーに記録済み、または 2) 全小問が個別に perStep 記録済み、または 3) perQuestion 記録済み
  const isQuestionScored = (q: Problem | undefined) => {
    if (!q || !q.subQuestions?.length) return false;
    if (run.perQuestion?.[q.id]) return true;
    const firstKey = stepScoreKey(q.id, q.subQuestions[0].id);
    if (subs.length > 0 && q.id === currentQuestion?.id) {
      // 旧UIで問1だけ採点して問2以降が未採点の途中データは、まだ未採点として残りを解けるようにする
      const allSubsRecorded = q.subQuestions.every(
        (sq) => Boolean(run.perStep?.[stepScoreKey(q.id, sq.id)]),
      );
      if (allSubsRecorded) return true;
      // 新UIで一括採点したときは batch マーク（全小問採点分が firstKey に入る）
      const rec = run.perStep?.[firstKey];
      if (rec && rec.judgeableCount >= q.subQuestions.length) return true;
      return false;
    }
    const rec = run.perStep?.[firstKey];
    return Boolean(rec && rec.judgeableCount >= q.subQuestions.length);
  };

  const pageScored = isQuestionScored(currentQuestion);
  const hasPrevRound = currentQuestionIndex > rangeStart;
  const hasNextRound = currentQuestionIndex < rangeEnd;
  const totalRoundsInScope = Math.max(1, rangeEnd - rangeStart + 1);
  const currentRoundOffset = Math.max(0, currentQuestionIndex - rangeStart);

  // 旧UIで既に採点済みだった小問（二重採点防止のため未採点分だけを scorePage に渡す）
  const unrecordedSubs = useMemo(() => {
    if (!currentQuestion) return [];
    return subs.filter(
      (sq) => !run.perStep?.[stepScoreKey(currentQuestion.id, sq.id)],
    );
  }, [currentQuestion, subs, run.perStep]);

  const answeredCount = subs.filter((sq) => Boolean(answers[sq.id])).length;
  const unansweredCount = subs.length - answeredCount;
  const correctCount = subs.filter((sq) =>
    isAnswerCorrect(sq, answers[sq.id] || ''),
  ).length;
  const wrongOrBlankCount = subs.length - correctCount;

  // 目安時間：各小問の battleTimeLimit 合計（無ければ 1問25秒）
  const roundLimitSec = useMemo(() => {
    const sum = subs.reduce((acc, sq) => acc + (Number(sq.battleTimeLimit) || 25), 0);
    return Math.max(60, sum);
  }, [subs]);

  const [elapsedSec, setElapsedSec] = useState(0);
  const timeUsedRef = useRef(0);
  const lastScoredQuestionRef = useRef<string | null>(null);

  useEffect(() => {
    if (pageScored || subs.length === 0) return undefined;
    const id = window.setInterval(() => {
      setElapsedSec((prev) => {
        const next = prev + 1;
        timeUsedRef.current = next;
        return next;
      });
    }, 1000);
    return () => window.clearInterval(id);
  }, [pageScored, subs.length, currentQuestion?.id]);

  // localStorage 保存（既存の Quiz と100%同じキー）
  useEffect(() => {
    safeSetItem(quizAnswersKey(chapter.id, mode), JSON.stringify(answers));
  }, [answers, chapter.id, mode]);

  useEffect(() => {
    safeSetItem(quizElimKey(chapter.id, mode), JSON.stringify(eliminated));
  }, [eliminated, chapter.id, mode]);

  useEffect(() => {
    safeSetItem(quizIndexKey(chapter.id, mode), String(currentQuestionIndex));
    safeSetItem(quizStepKey(chapter.id, mode), '0');
    safeSetItem(quizExplKey(chapter.id, mode), 'false');
  }, [currentQuestionIndex, chapter.id, mode]);

  useMountEffect(() => {
    onExplanationChange?.(false);
    void import('../../battle/data/growthStore')
      .then(({ resetStudySession }) => resetStudySession())
      .catch(logRejection('growth.resetStudySession'));
  });

  const [attemptedRound, setAttemptedRound] = useState<Record<string, boolean>>({});
  const [scoredFilter, setScoredFilter] = useState<'all' | 'wrong'>('all');
  const [openEx, setOpenEx] = useState<Record<string, boolean>>({});
  const [speakingKey, setSpeakingKey] = useState<string | null>(null);

  useEffect(() => {
    setScoredFilter('all');
    setSpeakingKey(null);
    stopGrammarSpeech();
    return () => stopGrammarSpeech();
  }, [currentQuestion?.id, chapter.id]);

  // 点数アニメーション
  const [scoreFx, setScoreFx] = useState<{
    breakdown: ScoreBreakdown;
    totalScore: number;
  } | null>(null);
  const [showFx, setShowFx] = useState(false);
  useEffect(() => {
    if (!showFx) return undefined;
    const t = window.setTimeout(() => setShowFx(false), 3200);
    return () => window.clearTimeout(t);
  }, [showFx]);

  // ノート保存状態
  const noteUid = auth.currentUser?.uid || 'guest';
  const [savedNotes, setSavedNotes] = useState<Record<string, boolean>>(() => {
    const existing = readJsonArray<{ chapterId?: string; questionId?: string }>(
      `notes_${noteUid}`,
    );
    const map: Record<string, boolean> = {};
    for (const n of existing) {
      if (n.chapterId === chapter.id && n.questionId) {
        map[n.questionId] = true;
      }
    }
    return map;
  });

  const scrollRef = useRef<HTMLDivElement | null>(null);
  const groupRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const scrollTop = () => scrollRef.current?.scrollTo({ top: 0 });

  const targetSubsForScore = unrecordedSubs.length > 0 ? unrecordedSubs : subs;
  const scoreRound = createScoreCurrentQuestion({
    currentQuestion,
    perStep: true,
    activeStepSub: targetSubsForScore[0] ?? null,
    activeStepSubs: targetSubsForScore,
    run,
    setRun,
    lastScoredQuestionRef,
    timeUsedRef,
    answers,
    questionTimeLimit: roundLimitSec,
    chapter,
    mode,
    isGuest,
    currentQuestionIndex,
    onScored,
  });

  const { handleNext: finishAllRounds } = createQuizStepActions({
    chapter,
    mode,
    isGuest,
    questions,
    answers,
    questionRange: effectiveRange,
    rangeStart,
    rangeEnd,
    currentQuestionIndex,
    perStep: false,
    isLastStep: true,
    isLastQuestion: true,
    safeStepIndex: 0,
    showingExplanation: true,
    scoreCurrentQuestionIfNeeded: () => null,
    setScoreAnimationData: noop,
    setShowScoreAnimation: noop,
    setShowingExplanation: noop,
    setStepIndex: noop,
    setCurrentQuestionIndex,
    onExplanationChange,
    onFinish: (finalAnswers, result) => {
      safeRemoveItem(quizAnswersKey(chapter.id, mode));
      safeRemoveItem(quizStepKey(chapter.id, mode));
      safeRemoveItem(quizExplKey(chapter.id, mode));
      onFinish(finalAnswers, result);
    },
  });

  const selectChoice = (sq: SubQuestion, mark: string) => {
    if (pageScored) return;
    setEliminated((prev) => {
      const cur = prev[sq.id] || [];
      if (!cur.includes(mark)) return prev;
      return { ...prev, [sq.id]: cur.filter((m) => m !== mark) };
    });
    setAnswers((prev) => {
      const next = { ...prev };
      if (next[sq.id] === mark) delete next[sq.id];
      else next[sq.id] = mark;
      return next;
    });
  };

  const toggleEliminate = (sq: SubQuestion, mark: string) => {
    if (pageScored) return;
    setEliminated((prev) => {
      const cur = prev[sq.id] || [];
      const exists = cur.includes(mark);
      const nextList = exists ? cur.filter((m) => m !== mark) : [...cur, mark];
      return { ...prev, [sq.id]: nextList };
    });
    if (answers[sq.id] === mark) {
      setAnswers((prev) => {
        const next = { ...prev };
        delete next[sq.id];
        return next;
      });
    }
  };

  const handleScore = () => {
    if (!currentQuestion || pageScored || subs.length === 0) return;
    setAttemptedRound((prev) => ({ ...prev, [currentQuestion.id]: true }));
    const scored = scoreRound();
    if (scored) {
      setScoreFx({ breakdown: scored.breakdown, totalScore: scored.addedScore });
      setShowFx(true);
    }
    scrollTop();
  };

  const handleForward = () => {
    if (!pageScored) {
      if (!hasNextRound) {
        // 1回（5問）完結：採点と同時に結果画面（ResultInsight + ResultStage）へ進む
        if (!currentQuestion || subs.length === 0) return;
        setAttemptedRound((prev) => ({ ...prev, [currentQuestion.id]: true }));
        scoreRound();
        finishAllRounds();
        return;
      }
      handleScore();
      return;
    }
    if (hasNextRound) {
      setElapsedSec(0);
      timeUsedRef.current = 0;
      lastScoredQuestionRef.current = null;
      setCurrentQuestionIndex((idx) => idx + 1);
      scrollTop();
      return;
    }
    finishAllRounds();
  };

  const handlePrevRound = () => {
    if (!hasPrevRound) return;
    setElapsedSec(0);
    timeUsedRef.current = 0;
    lastScoredQuestionRef.current = null;
    setCurrentQuestionIndex((idx) => Math.max(rangeStart, idx - 1));
    scrollTop();
  };

  const jumpToQuestion = (sqId: string) => {
    if (pageScored && scoredFilter === 'wrong') {
      const target = subs.find((s) => s.id === sqId);
      if (target && isAnswerCorrect(target, answers[sqId] || '')) {
        setScoredFilter('all');
      }
    }
    window.requestAnimationFrame(() => {
      const el = document.getElementById(`gp-item-${sqId}`);
      el?.scrollIntoView({
        block: 'start',
        behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
          ? 'auto'
          : 'smooth',
      });
      groupRefs.current[sqId]?.focus({ preventScroll: true });
    });
  };

  const setAllExplanationsOpen = (open: boolean) => {
    setOpenEx((prev) => {
      const next = { ...prev };
      for (const r of reviews) {
        next[r.sq.id] = open;
      }
      return next;
    });
  };

  const handleSaveNote = (sqId: string) => {
    if (!currentQuestion || savedNotes[currentQuestion.id]) return;
    try {
      saveQuestionNote({
        uid: noteUid,
        question: currentQuestion,
        chapter,
        questionIndex: currentQuestionIndex + 1,
      });
      setSavedNotes((prev) => ({ ...prev, [currentQuestion.id]: true }));
      notify(
        isGuest
          ? 'ノートに保存しました！（ゲスト利用のため、この端末に保存されます）'
          : 'ノートに保存しました！',
      );
      void sqId;
    } catch (e) {
      logRejection('grammarPage.saveNote')(e);
      notify('保存に失敗しました。');
    }
  };

  const onGroupKeyDown = (
    e: React.KeyboardEvent<HTMLDivElement>,
    sq: SubQuestion,
    idx: number,
  ) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key.toLowerCase();
    if (k in MARK_KEYS) {
      const mark = sq.options[MARK_KEYS[k]];
      if (mark) {
        e.preventDefault();
        selectChoice(sq, mark);
      }
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      const target = subs[idx + (e.key === 'ArrowDown' ? 1 : -1)];
      if (target) {
        e.preventDefault();
        groupRefs.current[target.id]?.focus();
      }
    }
  };

  if (!currentQuestion || subs.length === 0) {
    return (
      <div className="gp-root" data-grammar-page-quiz>
        <p className="gp-empty">この回の問題は準備中です。</p>
        <button type="button" className="gp-btn gp-btn-sub" onClick={onBack}>
          戻る
        </button>
      </div>
    );
  }

  const timerRatio = Math.min(100, (elapsedSec / roundLimitSec) * 100);
  const timerState = pageScored
    ? 'done'
    : elapsedSec > roundLimitSec
    ? 'over'
    : elapsedSec > roundLimitSec * 0.8
    ? 'low'
    : 'normal';

  const visibleReviews =
    pageScored && scoredFilter === 'wrong'
      ? reviews.filter((r) => r.status !== 'correct')
      : reviews;

  const roundLabel = String(currentQuestion.category || `第${currentQuestionIndex + 1}回`);
  const forwardLabel = !pageScored
    ? hasNextRound
      ? `この${subs.length}問を採点する`
      : '採点して結果を見る'
    : hasNextRound
    ? '次の回へ'
    : '結果を見る';

  return (
    <div className="gp-root" data-grammar-page-quiz>
      {onReturnToBattle && (
        <button type="button" onClick={onReturnToBattle} className="gp-battle-return">
          バトル結果・解説に戻る
        </button>
      )}

      <header className="gp-head" data-quiz-header>
        <button
          type="button"
          className="gp-back"
          onClick={onBack}
          aria-label="単元選択に戻る"
          title="単元選択に戻る"
        >
          <ArrowLeft size={18} aria-hidden="true" />
        </button>
        <span className="gp-mode">{mode === 'mini_test' ? '小テスト' : '演習'}</span>
        <div className="gp-title-wrap">
          <h2 className="gp-title">{chapter.abstractTitle}</h2>
          <p className="gp-sub">{roundLabel}</p>
        </div>
        <dl className="gp-stats">
          {totalRoundsInScope > 1 && (
            <div title="いまの回／範囲内の回数">
              <dt>
                <FileText size={14} aria-hidden="true" />
                <span className="gp-sr">回</span>
              </dt>
              <dd>
                <b>{currentRoundOffset + 1}</b>/{totalRoundsInScope}
                <small>回</small>
              </dd>
            </div>
          )}
          <div title="答えた問題／この回の問題数">
            <dt>
              <ListChecks size={14} aria-hidden="true" />
              <span className="gp-sr">回答済み</span>
            </dt>
            <dd data-grammar-answered>
              <b>{answeredCount}</b>/{subs.length}
              <small>問</small>
            </dd>
          </div>
        </dl>
      </header>

      <div className="gp-subbar" data-state={timerState}>
        <div className="gp-subbar-row">
          <p className="gp-timer-label">
            <Clock size={13} aria-hidden="true" />
            <span>{fmtClock(elapsedSec)}</span>
            <span className="gp-timer-limit">／{fmtClock(roundLimitSec)}</span>
          </p>

          <ol className="gp-q-dots" aria-label="この回の問題へ移動">
            {reviews.map((rev) => {
              const qState = pageScored
                ? rev.status
                : rev.chosen
                ? 'answered'
                : (eliminated[rev.sq.id]?.length || 0) > 0
                ? 'working'
                : 'todo';
              const markSym = pageScored
                ? rev.status === 'correct'
                  ? '○'
                  : rev.status === 'wrong'
                  ? '×'
                  : '−'
                : rev.chosen
                ? rev.chosen
                : '';
              return (
                <li key={rev.sq.id}>
                  <button
                    type="button"
                    className="gp-q-dot"
                    data-qstate={qState}
                    onClick={() => jumpToQuestion(rev.sq.id)}
                    aria-label={`問${rev.displayNo}へ移動`}
                  >
                    <span>{rev.displayNo}</span>
                    {markSym && <em aria-hidden="true">{markSym}</em>}
                  </button>
                </li>
              );
            })}
          </ol>

          {!pageScored && (
            <span className="gp-elim-tip">
              <Slash size={12} aria-hidden="true" />
              <span>×ボタン・右クリックで消去線</span>
            </span>
          )}
        </div>

        <div className="gp-timer-track" aria-hidden="true">
          <div className="gp-timer-fill" style={{ width: `${timerRatio}%` }} />
        </div>
      </div>

      <div ref={scrollRef} className="gp-scroll">
        {pageScored && (
          <section
            className="gp-summary"
            data-perfect={correctCount === subs.length || undefined}
            aria-label="この回の採点結果"
          >
            <div className="gp-summary-top">
              <div className="gp-score-row">
                <CheckCircle2 size={18} aria-hidden="true" />
                <span>採点完了</span>
                <span className="gp-score-fraction">
                  <b>{correctCount}</b>
                  <small>/{subs.length}問正解</small>
                </span>
                <span className="gp-score-pct">
                  {Math.round((correctCount / Math.max(1, subs.length)) * 100)}%
                </span>
              </div>
              <div className="gp-bulk-btns">
                <button
                  type="button"
                  className="gp-bulk-btn"
                  onClick={() => setAllExplanationsOpen(true)}
                >
                  解説をすべて開く
                </button>
                <button
                  type="button"
                  className="gp-bulk-btn"
                  onClick={() => setAllExplanationsOpen(false)}
                >
                  すべて閉じる
                </button>
              </div>
            </div>

            {wrongOrBlankCount > 0 && (
              <div className="gp-toolbar">
                <div className="gp-filter-pills" role="group" aria-label="表示の絞り込み">
                  <button
                    type="button"
                    className="gp-filter-pill"
                    data-active={scoredFilter === 'all' || undefined}
                    onClick={() => setScoredFilter('all')}
                  >
                    全問 ({subs.length})
                  </button>
                  <button
                    type="button"
                    className="gp-filter-pill"
                    data-active={scoredFilter === 'wrong' || undefined}
                    onClick={() => setScoredFilter('wrong')}
                  >
                    誤答・未回答のみ ({wrongOrBlankCount})
                  </button>
                </div>
              </div>
            )}
          </section>
        )}

        <div className={`gp-list${pageScored ? ' is-scored' : ''}`}>
          {visibleReviews.map((rev, idx) => {
            const {
              sq,
              displayNo,
              focusLabel,
              stem,
              choices,
              cues,
              chosen,
              status: scoredStatus,
              filledWord,
              correctWord,
            } = rev;

            const cardStatus = !pageScored
              ? chosen
                ? 'answered'
                : attemptedRound[currentQuestion.id]
                ? 'unanswered'
                : 'todo'
              : scoredStatus;

            const choiceTextsList = choices.map((c) => c.text);
            const singleCol = prefersSingleColumnGrammarChoices(choiceTextsList);
            const mobileSingleCol = prefersMobileSingleColumnGrammarChoices(choiceTextsList);
            const labelId = `gp-q-${sq.id}`;
            const exOpen = openEx[sq.id] ?? scoredStatus !== 'correct';
            const sqElims = eliminated[sq.id] || [];

            return (
              <article
                key={sq.id}
                id={`gp-item-${sq.id}`}
                className="gp-item"
                data-status={cardStatus}
                data-grammar-question={displayNo}
              >
                <GrammarQuestionStem
                  displayNo={displayNo}
                  stem={stem}
                  filled={
                    pageScored && scoredStatus === 'correct' ? correctWord : filledWord
                  }
                  correctWord={pageScored ? correctWord : undefined}
                  result={
                    pageScored
                      ? scoredStatus === 'correct'
                        ? 'right'
                        : scoredStatus === 'wrong'
                        ? 'wrong'
                        : 'blank'
                      : undefined
                  }
                  unansweredTag={
                    cardStatus === 'unanswered' || cardStatus === 'blank'
                  }
                  focusLabel={focusLabel}
                  labelId={labelId}
                  cues={pageScored ? cues : undefined}
                />

                <div
                  role="radiogroup"
                  aria-labelledby={labelId}
                  aria-disabled={pageScored || undefined}
                  tabIndex={0}
                  ref={(el) => {
                    groupRefs.current[sq.id] = el;
                  }}
                  onKeyDown={(e) => onGroupKeyDown(e, sq, idx)}
                  className={`gp-choices${singleCol ? ' is-single' : ''}${
                    mobileSingleCol ? ' is-mobile-single' : ''
                  }${pageScored ? ' is-scored' : ''}`}
                >
                  {choices.map((c) => {
                    const checked = chosen === c.mark;
                    const isRight = pageScored && c.correct;
                    const isWrongPick = pageScored && checked && !isRight;
                    const isEliminated =
                      !pageScored && !checked && sqElims.includes(c.mark);
                    return (
                      <div
                        key={c.mark}
                        role="radio"
                        aria-checked={checked}
                        aria-disabled={pageScored || undefined}
                        aria-label={`${c.mark} ${c.text}${
                          isRight && checked
                            ? '（あなたの答え・正解）'
                            : isRight
                            ? '（正解）'
                            : isWrongPick
                            ? '（あなたの答え）'
                            : isEliminated
                            ? '（消去法で除外中）'
                            : ''
                        }`}
                        tabIndex={-1}
                        className="gp-choice"
                        data-checked={checked || undefined}
                        data-eliminated={isEliminated || undefined}
                        data-result={
                          isRight ? 'right' : isWrongPick ? 'wrong' : undefined
                        }
                        onClick={() => selectChoice(sq, c.mark)}
                        onContextMenu={(e) => {
                          if (pageScored) return;
                          e.preventDefault();
                          toggleEliminate(sq, c.mark);
                        }}
                      >
                        <span className="gp-bubble" aria-hidden="true">
                          {c.numberLabel}
                        </span>
                        <span className="gp-choice-body" aria-hidden="true">
                          <span className="gp-choice-text" lang="en">
                            {formatText(c.text, [], { prose: true, noMath: true })}
                          </span>
                        </span>
                        {(isRight || isWrongPick) && (
                          <span
                            className="gp-choice-badge"
                            data-tone={isRight ? 'right' : 'wrong'}
                            aria-hidden="true"
                          >
                            {isRight && checked
                              ? 'あなた・正解'
                              : isRight
                              ? '正解'
                              : 'あなた'}
                          </span>
                        )}
                        {!pageScored && !checked && (
                          <button
                            type="button"
                            className="gp-elim-btn"
                            data-active={isEliminated || undefined}
                            title={
                              isEliminated
                                ? '消去線を取り消す'
                                : '消去法でこの選択肢に斜線を引く'
                            }
                            aria-label={
                              isEliminated
                                ? `選択肢${c.mark}の消去線を外す`
                                : `選択肢${c.mark}を消去法で除外する`
                            }
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleEliminate(sq, c.mark);
                            }}
                          >
                            <X size={13} aria-hidden="true" />
                          </button>
                        )}
                        {checked && !pageScored && (
                          <Check
                            size={18}
                            strokeWidth={3}
                            className="gp-choice-check"
                            aria-hidden="true"
                          />
                        )}
                      </div>
                    );
                  })}
                </div>

                {pageScored && (
                  <GrammarCompactReview
                    review={rev}
                    isOpen={exOpen}
                    onToggleOpen={(next) =>
                      setOpenEx((prev) => ({ ...prev, [sq.id]: next }))
                    }
                    saved={Boolean(savedNotes[currentQuestion.id])}
                    onSaveNote={() => handleSaveNote(sq.id)}
                    speakingKey={speakingKey}
                    setSpeakingKey={setSpeakingKey}
                  />
                )}
              </article>
            );
          })}
        </div>
      </div>

      <footer className="gp-foot">
        {hasPrevRound ? (
          <button
            type="button"
            className="gp-btn gp-btn-sub"
            onClick={handlePrevRound}
          >
            <ChevronLeft size={18} aria-hidden="true" />
            <span>前の回</span>
          </button>
        ) : (
          <button type="button" className="gp-btn gp-btn-sub" onClick={onBack}>
            <ArrowLeft size={16} aria-hidden="true" />
            <span>一覧</span>
          </button>
        )}

        {!pageScored && unansweredCount > 0 && (
          <span className="gp-unanswered-count">あと{unansweredCount}問</span>
        )}

        <button
          type="button"
          className="gp-btn gp-btn-main"
          data-grammar-forward
          onClick={handleForward}
        >
          <span>{forwardLabel}</span>
          {(pageScored || !hasNextRound) && (
            <ChevronRight size={18} aria-hidden="true" />
          )}
        </button>
      </footer>

      {scoreFx && showFx && scoreFx.breakdown.basePoints > 0 && (
        <CorrectBurst
          burstKey={`${currentQuestion.id}:${run.totalScore}`}
          combo={run.runningCombo ?? 0}
        />
      )}
      {scoreFx && (
        <FloatingScoreAnimation
          breakdown={scoreFx.breakdown}
          totalScore={scoreFx.totalScore}
          isVisible={showFx}
        />
      )}
    </div>
  );
}
