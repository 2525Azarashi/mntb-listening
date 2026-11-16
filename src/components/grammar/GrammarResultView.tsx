/**
 * 英文法（第1〜20章）専用：問題画面と完全一体型のコンパクト結果・解説画面
 *
 * ■ 特徴
 *   ・演習画面（GrammarPageQuiz）そのままの白カード＋話者ピル A/B＋インライン `[誤答 → 正解]` 空所＋2×2選択肢＋Inter統一書体
 *   ・スリムなサマリー帯（正解数・正答率・所要時間・獲得マナコイン・番号ジャンプチップ・`全問` / `誤答のみ` フィルタ・一括解説開閉）
 *   ・下部高さ56pxの1行フッター（`単元一覧` / `誤答だけ解き直す` / `第N+1回へ >`）で縦幅を圧迫しない
 *   ・既存の `onRetryWrong` / `onNextRound` / `onNextChapter` / `saveQuestionNote` と100%同一のデータ形式で連携
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft,
  CheckCircle2,
  ChevronRight,
  Clock,
  Coins,
  Home,
  RotateCcw,
} from 'lucide-react';
import { auth } from '../../firebase';
import type { Chapter, Problem } from '../../types/curriculum';
import type { ReviewTargetItem } from '../../utils/reviewFocus';
import { saveQuestionNote } from '../../utils/questionNote';
import { notify } from '../../utils/dialog';
import { formatText } from '../../utils/textFormatter';
import { logRejection } from '../../utils/reportError';
import { readJsonArray } from '../../utils/safeLocalStorage';
import {
  buildGrammarSubReviews,
  prefersSingleColumnGrammarChoices,
  type GrammarSubReview,
} from './grammarPageModel';
import {
  GrammarCompactReview,
  GrammarQuestionStem,
} from './GrammarQuestionCardParts';
import { stopGrammarSpeech } from './grammarSpeech';
import './grammar-page.css';

export interface GrammarResultViewProps {
  mode: 'mini_test' | 'practice';
  chapter: Chapter;
  answers: Record<string, string>;
  onBack: () => void;
  onReturnToBattle?: () => void;
  isGuest: boolean;
  resultTotalCorrect?: number;
  resultTotalJudgeable?: number;
  resultTotalTimeSec?: number;
  questionRange?: { startIndex: number; endIndex: number } | null;
  onRetryWrong?: (targets: ReviewTargetItem[]) => void;
  onNextAction?: () => void;
  nextActionLabel?: string;
  onHome?: () => void;
}

function fmtDuration(sec?: number): string {
  if (!sec || sec <= 0) return '';
  const s = Math.max(1, Math.round(sec));
  if (s < 60) return `${s}秒`;
  return `${Math.floor(s / 60)}分${String(s % 60).padStart(2, '0')}秒`;
}

interface ScopedReviewEntry {
  problem: Problem;
  problemIndex: number;
  rev: GrammarSubReview;
}

export function GrammarResultView({
  mode,
  chapter,
  answers,
  onBack,
  onReturnToBattle,
  isGuest,
  resultTotalCorrect,
  resultTotalJudgeable,
  resultTotalTimeSec,
  questionRange,
  onRetryWrong,
  onNextAction,
  nextActionLabel,
  onHome,
}: GrammarResultViewProps) {
  const allQuestions: Problem[] =
    mode === 'mini_test' ? chapter.miniTest || [] : chapter.practiceProblems || [];

  const scopedQuestions = useMemo(() => {
    if (!questionRange) {
      return allQuestions.map((problem, problemIndex) => ({ problem, problemIndex }));
    }
    const last = Math.max(0, allQuestions.length - 1);
    const start = Math.min(Math.max(0, questionRange.startIndex), last);
    const end = Math.min(Math.max(start, questionRange.endIndex), last);
    return allQuestions.slice(start, end + 1).map((problem, offset) => ({
      problem,
      problemIndex: start + offset,
    }));
  }, [allQuestions, questionRange]);

  const entries: ScopedReviewEntry[] = useMemo(() => {
    const out: ScopedReviewEntry[] = [];
    let serial = 1;
    for (const { problem, problemIndex } of scopedQuestions) {
      const revs = buildGrammarSubReviews(problem, answers, serial);
      for (const rev of revs) {
        out.push({ problem, problemIndex, rev });
        serial += 1;
      }
    }
    return out;
  }, [scopedQuestions, answers]);

  const totalCount = entries.length || resultTotalJudgeable || 0;
  const computedCorrect = entries.filter((e) => e.rev.status === 'correct').length;
  const correctCount = entries.length > 0 ? computedCorrect : resultTotalCorrect ?? 0;
  const wrongEntries = entries.filter((e) => e.rev.status !== 'correct');
  const wrongCount = wrongEntries.length;
  const pct = totalCount > 0 ? Math.round((correctCount / totalCount) * 100) : 0;

  const [studyReward, setStudyReward] = useState<{ coins: number; xp: number } | null>(
    null,
  );
  useEffect(() => {
    let off = () => {};
    let alive = true;
    void import('../../battle/data/growthStore')
      .then(({ currentStudySession, subscribeStudySession }) => {
        if (!alive) return;
        setStudyReward(currentStudySession());
        off = subscribeStudySession(setStudyReward);
      })
      .catch(logRejection('grammarResult.subscribeStudySession'));
    return () => {
      alive = false;
      off();
    };
  }, []);

  const [filter, setFilter] = useState<'all' | 'wrong'>('all');
  const [openEx, setOpenEx] = useState<Record<string, boolean>>({});
  const [speakingKey, setSpeakingKey] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    return () => stopGrammarSpeech();
  }, []);

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

  const handleSaveNote = (problem: Problem, problemIndex: number) => {
    if (savedNotes[problem.id]) return;
    try {
      saveQuestionNote({
        uid: noteUid,
        question: problem,
        chapter,
        questionIndex: problemIndex + 1,
      });
      setSavedNotes((prev) => ({ ...prev, [problem.id]: true }));
      notify(
        isGuest
          ? 'ノートに保存しました！（ゲスト利用のため、この端末に保存されます）'
          : 'ノートに保存しました！',
      );
    } catch (e) {
      logRejection('grammarResult.saveNote')(e);
      notify('保存に失敗しました。');
    }
  };

  const retryTargets: ReviewTargetItem[] = useMemo(() => {
    const byProblem = new Map<string, string[]>();
    for (const e of wrongEntries) {
      const arr = byProblem.get(e.problem.id) || [];
      arr.push(e.rev.sq.id);
      byProblem.set(e.problem.id, arr);
    }
    return [...byProblem.entries()].map(([questionId, subQuestionIds]) => ({
      questionId,
      subQuestionIds,
    }));
  }, [wrongEntries]);

  const setAllOpen = (open: boolean) => {
    const next: Record<string, boolean> = {};
    for (const e of entries) {
      next[e.rev.sq.id] = open;
    }
    setOpenEx(next);
  };

  const jumpToQuestion = (sqId: string) => {
    if (filter === 'wrong') {
      const hit = entries.find((e) => e.rev.sq.id === sqId);
      if (hit?.rev.status === 'correct') setFilter('all');
    }
    window.requestAnimationFrame(() => {
      const el = document.getElementById(`gp-res-item-${sqId}`);
      el?.scrollIntoView({
        block: 'start',
        behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
          ? 'auto'
          : 'smooth',
      });
    });
  };

  const visibleEntries =
    filter === 'wrong' ? entries.filter((e) => e.rev.status !== 'correct') : entries;
  const durationText = fmtDuration(resultTotalTimeSec);
  const roundSubTitle =
    scopedQuestions.length === 1
      ? scopedQuestions[0].problem.category || `第${scopedQuestions[0].problemIndex + 1}回`
      : `全${scopedQuestions.length}回`;

  return (
    <div className="gp-root" data-grammar-result>
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
          aria-label="単元一覧に戻る"
          title="単元一覧に戻る"
        >
          <ArrowLeft size={18} aria-hidden="true" />
        </button>
        <span className="gp-mode gp-mode-done">結果・解説</span>
        <div className="gp-title-wrap">
          <h2 className="gp-title">{chapter.abstractTitle || chapter.realTitle}</h2>
          <p className="gp-sub">{roundSubTitle}</p>
        </div>
        {onHome && (
          <button
            type="button"
            className="gp-home-btn"
            onClick={onHome}
            aria-label="ホームへ戻る"
            title="ホームへ戻る"
          >
            <Home size={17} aria-hidden="true" />
          </button>
        )}
      </header>

      <div ref={scrollRef} className="gp-scroll">
        <section
          className="gp-summary"
          data-perfect={wrongCount === 0 && totalCount > 0 ? true : undefined}
          aria-label="演習結果サマリー"
        >
          <div className="gp-summary-top">
            <div className="gp-score-row">
              <CheckCircle2 size={18} aria-hidden="true" />
              <span className="gp-score-fraction">
                <b>{correctCount}</b>
                <small>/{totalCount}問正解</small>
              </span>
              <span className="gp-score-pct">{pct}%</span>
              {durationText && (
                <span className="gp-pill-meta">
                  <Clock size={12} aria-hidden="true" />
                  <span>{durationText}</span>
                </span>
              )}
              {!isGuest && studyReward && studyReward.coins > 0 && (
                <span className="gp-pill-meta gp-pill-coin">
                  <Coins size={12} aria-hidden="true" />
                  <span>+{studyReward.coins}</span>
                </span>
              )}
            </div>

            <div className="gp-bulk-btns">
              <button
                type="button"
                className="gp-bulk-btn"
                onClick={() => setAllOpen(true)}
              >
                解説をすべて開く
              </button>
              <button
                type="button"
                className="gp-bulk-btn"
                onClick={() => setAllOpen(false)}
              >
                すべて閉じる
              </button>
            </div>
          </div>

          {entries.length > 1 && (
            <ol className="gp-jump-strip" aria-label="設問ごとの正誤">
              {entries.map(({ rev }) => {
                const sym =
                  rev.status === 'correct'
                    ? '○'
                    : rev.status === 'wrong'
                    ? '×'
                    : '−';
                return (
                  <li key={rev.sq.id}>
                    <button
                      type="button"
                      className="gp-jump-chip"
                      data-result={rev.status}
                      onClick={() => jumpToQuestion(rev.sq.id)}
                      aria-label={`問${rev.displayNo}（${
                        rev.status === 'correct'
                          ? '正解'
                          : rev.status === 'wrong'
                          ? '不正解'
                          : '未回答'
                      }）へ移動`}
                    >
                      <span>{rev.displayNo}</span>
                      <b aria-hidden="true">{sym}</b>
                    </button>
                  </li>
                );
              })}
            </ol>
          )}

          {wrongCount > 0 && (
            <div className="gp-toolbar">
              <div className="gp-filter-pills" role="group" aria-label="問題の絞り込み">
                <button
                  type="button"
                  className="gp-filter-pill"
                  data-active={filter === 'all' || undefined}
                  onClick={() => setFilter('all')}
                >
                  全問 ({entries.length})
                </button>
                <button
                  type="button"
                  className="gp-filter-pill"
                  data-active={filter === 'wrong' || undefined}
                  onClick={() => setFilter('wrong')}
                >
                  誤答・未回答のみ ({wrongCount})
                </button>
              </div>
            </div>
          )}
        </section>

        <div className="gp-list is-scored">
          {visibleEntries.map(({ problem, problemIndex, rev }) => {
            const {
              sq,
              displayNo,
              focusLabel,
              stem,
              choices,
              chosen,
              status,
              filledWord,
              correctWord,
            } = rev;
            const singleCol = prefersSingleColumnGrammarChoices(
              choices.map((c) => c.text),
            );
            const labelId = `gp-res-q-${sq.id}`;
            const isOpen = openEx[sq.id] ?? status !== 'correct';

            return (
              <article
                key={sq.id}
                id={`gp-res-item-${sq.id}`}
                className="gp-item"
                data-status={status}
                data-grammar-question={displayNo}
              >
                <GrammarQuestionStem
                  displayNo={displayNo}
                  stem={stem}
                  filled={status === 'correct' ? correctWord : filledWord}
                  correctWord={correctWord}
                  result={
                    status === 'correct'
                      ? 'right'
                      : status === 'wrong'
                      ? 'wrong'
                      : 'blank'
                  }
                  unansweredTag={status === 'blank'}
                  focusLabel={focusLabel}
                  labelId={labelId}
                />

                <div
                  role="group"
                  aria-labelledby={labelId}
                  aria-disabled="true"
                  className={`gp-choices is-scored${singleCol ? ' is-single' : ''}`}
                >
                  {choices.map((c) => {
                    const checked = chosen === c.mark;
                    const tone = c.correct ? 'right' : checked ? 'wrong' : undefined;
                    return (
                      <div
                        key={c.mark}
                        className="gp-choice"
                        data-checked={checked || undefined}
                        data-result={tone}
                      >
                        <span className="gp-bubble" aria-hidden="true">
                          {c.numberLabel}
                        </span>
                        <span className="gp-choice-body">
                          <span className="gp-choice-text" lang="en">
                            {formatText(c.text, [], { prose: true, noMath: true })}
                          </span>
                        </span>
                        {(c.correct || checked) && (
                          <span
                            className="gp-choice-badge"
                            data-tone={c.correct ? 'right' : 'wrong'}
                          >
                            {c.correct && checked
                              ? 'あなた・正解'
                              : c.correct
                              ? '正解'
                              : 'あなた'}
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>

                <GrammarCompactReview
                  review={rev}
                  isOpen={isOpen}
                  onToggleOpen={(next) =>
                    setOpenEx((prev) => ({ ...prev, [sq.id]: next }))
                  }
                  saved={Boolean(savedNotes[problem.id])}
                  onSaveNote={() => handleSaveNote(problem, problemIndex)}
                  speakingKey={speakingKey}
                  setSpeakingKey={setSpeakingKey}
                />
              </article>
            );
          })}
        </div>
      </div>

      <footer className="gp-foot">
        <button type="button" className="gp-btn gp-btn-sub" onClick={onBack}>
          <ArrowLeft size={16} aria-hidden="true" />
          <span>単元一覧</span>
        </button>

        {retryTargets.length > 0 && onRetryWrong && (
          <button
            type="button"
            className="gp-btn gp-btn-retry"
            onClick={() => onRetryWrong(retryTargets)}
          >
            <RotateCcw size={15} aria-hidden="true" />
            <span>誤答だけ解き直す ({wrongCount})</span>
          </button>
        )}

        {onNextAction ? (
          <button
            type="button"
            className="gp-btn gp-btn-main"
            onClick={onNextAction}
          >
            <span>{nextActionLabel ? `${nextActionLabel}へ` : '次へ進む'}</span>
            <ChevronRight size={18} aria-hidden="true" />
          </button>
        ) : (
          onHome && (
            <button type="button" className="gp-btn gp-btn-main" onClick={onHome}>
              <Home size={16} aria-hidden="true" />
              <span>ホームへ</span>
            </button>
          )
        )}
      </footer>
    </div>
  );
}
