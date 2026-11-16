/**
 * TOEIC（リスニング・Part 5・Part 6・Part 7）専用：2段構成の結果＆解説画面
 *
 * ■ 流れ
 *   1. 結果画面（`step === 'summary'`・初期表示）：
 *      ・`ResultInsight`（正答率リング・正解数・所要時間・挑戦回数・前回比・自己ベスト・満点3回目標・回の棒グラフ）
 *      ・分野別正答数＋設問ごとの正誤ジャンプチップ（タップで該当問のカード解説へ直接移動）
 *      ・`ResultStage`（とびら君イラスト／全問正解動画・吹き出し・獲得マナコイン＆XP）
 *      ・主ボタン「詳しい解説・答え合わせを見る」＋「単元一覧」「誤答だけ解き直す」「次の回へ」
 *   2. 詳しい解説・答え合わせ（`step === 'detail'`）：
 *      ・演習画面そのままの白カード一覧・インライン `[誤答 → 正解]` 空所・番号つき手がかりマーカー `¹` `²`・各肢理由
 *      ・「← 結果へ」でいつでも結果画面へ戻れる
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft,
  BookOpen,
  Bookmark,
  BookmarkCheck,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Clock,
  Coins,
  Flag,
  Home,
  MinusCircle,
  RotateCcw,
  XCircle,
} from 'lucide-react';
import { auth } from '../../firebase';
import { QUESTION_REPORT_FORM_URL } from '../../features/legal/legalText';
import type { Chapter, Problem, SubQuestion } from '../../types/curriculum';
import type { ReviewTargetItem } from '../../utils/reviewFocus';
import { isAnswerCorrect } from '../../utils/answerJudge';
import { notify } from '../../utils/dialog';
import { formatText } from '../../utils/textFormatter';
import { logRejection } from '../../utils/reportError';
import { ResultInsight } from '../explanation/ResultInsight';
import { ResultStage } from '../explanation/ResultSummary';
import { StemWithBlank, ToeicExplanationPanel } from './ToeicExplanationPanel';
import { isToeicNoteSaved, saveToeicNote } from './toeicNote';
import {
  isToeicListeningChapter,
  isToeicPart6Chapter,
  isToeicPart7Chapter,
  p6Snippet,
  p7Stem,
  prefersSingleColumn,
  toeicExplanationFor,
} from './toeicPageModel';
import {
  toeicListeningChoiceTexts,
  toeicListeningStem,
} from '../../data/toeic/toeicListeningPage';
import '../step-explanation.css';
import './toeic-page.css';
import '../grammar/grammar-page.css';

export interface ToeicResultViewProps {
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
  initialStep?: 'summary' | 'detail';
}

const markLetter = (mark: string) => mark.replace(/[()]/g, '');

function fmtDuration(sec?: number): string {
  if (!sec || sec <= 0) return '';
  const s = Math.max(1, Math.round(sec));
  if (s < 60) return `${s}秒`;
  return `${Math.floor(s / 60)}分${String(s % 60).padStart(2, '0')}秒`;
}

function questionNumber(sq: SubQuestion, fallback: number): number {
  const m = String(sq.label || '').match(/(\d+)/);
  return m ? Number(m[1]) : fallback;
}

function stemForResult(problem: Problem, sq: SubQuestion, chapterId: string): string {
  if (isToeicListeningChapter(chapterId)) {
    const tpl = toeicListeningStem(sq, true);
    if (tpl) return tpl;
  }
  const p7 = p7Stem(sq);
  if (p7) return p7;
  const p6 = p6Snippet(sq);
  if (p6) return p6;
  const ex = toeicExplanationFor(sq);
  if (ex) return ex.sentence;
  const label = String(sq.label || '');
  const line = String(problem.text || '').split('\n').find((l) => l.startsWith(`${label}　`));
  return line ? line.slice(label.length + 1) : label;
}

interface ToeicResultEntry {
  problem: Problem;
  problemIndex: number;
  sq: SubQuestion;
  no: number;
  chosen: string;
  status: 'correct' | 'wrong' | 'blank';
}

export function ToeicResultView({
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
  initialStep = 'summary',
}: ToeicResultViewProps) {
  const [step, setStep] = useState<'summary' | 'detail'>(initialStep);

  const allQuestions: Problem[] =
    mode === 'mini_test' ? chapter.miniTest || [] : chapter.practiceProblems || [];

  const singleIndex = useMemo(() => {
    if (!questionRange || questionRange.startIndex !== questionRange.endIndex) return null;
    if (allQuestions.length === 0) return null;
    return Math.min(Math.max(0, questionRange.startIndex), allQuestions.length - 1);
  }, [questionRange, allQuestions.length]);

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

  const entries: ToeicResultEntry[] = useMemo(() => {
    const out: ToeicResultEntry[] = [];
    let serial = 1;
    for (const { problem, problemIndex } of scopedQuestions) {
      for (const sq of problem.subQuestions || []) {
        const chosen = answers[sq.id] || '';
        const ok = Boolean(chosen) && isAnswerCorrect(sq, chosen);
        const status: 'correct' | 'wrong' | 'blank' = !chosen ? 'blank' : ok ? 'correct' : 'wrong';
        out.push({
          problem,
          problemIndex,
          sq,
          no: questionNumber(sq, serial),
          chosen,
          status,
        });
        serial += 1;
      }
    }
    return out;
  }, [scopedQuestions, answers]);

  const isListening = isToeicListeningChapter(chapter.id);
  const isP6 = isToeicPart6Chapter(chapter.id);
  const isP7 = isToeicPart7Chapter(chapter.id);

  const totalCount = entries.length || resultTotalJudgeable || 0;
  const computedCorrect = entries.filter((e) => e.status === 'correct').length;
  const correctCount = entries.length > 0 ? computedCorrect : resultTotalCorrect ?? 0;
  const wrongEntries = entries.filter((e) => e.status !== 'correct');
  const wrongCount = wrongEntries.length;
  const pct = totalCount > 0 ? Math.round((correctCount / totalCount) * 100) : 0;

  const skillSummary = useMemo(() => {
    const map = new Map<string, { c: number; n: number }>();
    for (const e of entries) {
      const k = String(e.sq.skill || toeicExplanationFor(e.sq)?.skill || 'その他');
      const row = map.get(k) || { c: 0, n: 0 };
      row.n += 1;
      if (e.status === 'correct') row.c += 1;
      map.set(k, row);
    }
    return [...map.entries()];
  }, [entries]);

  const [studyReward, setStudyReward] = useState<{
    coins: number;
    xp: number;
    count: number;
  } | null>(null);
  useEffect(() => {
    let off = () => {};
    let alive = true;
    void import('../../battle/data/growthStore')
      .then(({ currentStudySession, subscribeStudySession }) => {
        if (!alive) return;
        setStudyReward(currentStudySession());
        off = subscribeStudySession(setStudyReward);
      })
      .catch(logRejection('toeicResult.subscribeStudySession'));
    return () => {
      alive = false;
      off();
    };
  }, []);

  const [filter, setFilter] = useState<'all' | 'wrong'>('all');
  const [openEx, setOpenEx] = useState<Record<string, boolean>>({});
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const noteUid = auth.currentUser?.uid || 'guest';
  const [savedNotes, setSavedNotes] = useState<Record<string, boolean>>({});
  const isSaved = (id: string) => savedNotes[id] ?? isToeicNoteSaved(noteUid, id);

  const saveNote = (entry: ToeicResultEntry) => {
    const ex = toeicExplanationFor(entry.sq);
    if (!ex || isSaved(entry.sq.id)) return;
    const m = String(entry.problem.id || '').match(/_r(\d+)$/);
    const roundNo = m ? Number(m[1]) : entry.problemIndex + 1;
    try {
      saveToeicNote({
        uid: noteUid,
        chapter,
        problem: entry.problem,
        sq: entry.sq,
        ex,
        questionNo: entry.no,
        roundNo,
      });
      setSavedNotes((prev) => ({ ...prev, [entry.sq.id]: true }));
      notify(
        isGuest
          ? 'ノートに保存しました！（ゲスト利用のため、この端末にだけ保存されます）'
          : 'ノートに保存しました！',
      );
    } catch (e) {
      logRejection('toeicResult.saveNote')(e);
      notify('保存に失敗しました。');
    }
  };

  const retryTargets: ReviewTargetItem[] = useMemo(() => {
    const byProblem = new Map<string, string[]>();
    for (const e of wrongEntries) {
      const arr = byProblem.get(e.problem.id) || [];
      arr.push(e.sq.id);
      byProblem.set(e.problem.id, arr);
    }
    return [...byProblem.entries()].map(([questionId, subQuestionIds]) => ({
      questionId,
      subQuestionIds,
    }));
  }, [wrongEntries]);

  const setAllOpen = (open: boolean) => {
    const next: Record<string, boolean> = {};
    for (const e of entries) next[e.sq.id] = open;
    setOpenEx(next);
  };

  const openDetailScreen = (targetSqId?: string) => {
    if (targetSqId && filter === 'wrong') {
      const hit = entries.find((e) => e.sq.id === targetSqId);
      if (hit?.status === 'correct') setFilter('all');
    }
    setStep('detail');
    window.requestAnimationFrame(() => {
      if (targetSqId) {
        const el = document.getElementById(`tp-res-item-${targetSqId}`);
        if (el) {
          el.scrollIntoView({
            block: 'start',
            behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
              ? 'auto'
              : 'smooth',
          });
          return;
        }
      }
      scrollRef.current?.scrollTo({ top: 0 });
    });
  };

  const backToSummaryScreen = () => {
    setStep('summary');
    window.requestAnimationFrame(() => {
      scrollRef.current?.scrollTo({ top: 0 });
    });
  };

  const jumpToQuestion = (sqId: string) => {
    if (filter === 'wrong') {
      const hit = entries.find((e) => e.sq.id === sqId);
      if (hit?.status === 'correct') setFilter('all');
    }
    window.requestAnimationFrame(() => {
      const el = document.getElementById(`tp-res-item-${sqId}`);
      el?.scrollIntoView({
        block: 'start',
        behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
          ? 'auto'
          : 'smooth',
      });
    });
  };

  const visibleEntries = filter === 'wrong' ? entries.filter((e) => e.status !== 'correct') : entries;
  const durationText = fmtDuration(resultTotalTimeSec);
  const roundSubTitle =
    scopedQuestions.length === 1
      ? scopedQuestions[0].problem.category || `第${scopedQuestions[0].problemIndex + 1}回`
      : `全${scopedQuestions.length}回`;

  return (
    <div className="gp-root" data-toeic-result data-result-step={step}>
      {onReturnToBattle && (
        <button type="button" onClick={onReturnToBattle} className="gp-battle-return">
          バトル結果・解説に戻る
        </button>
      )}

      <header className="gp-head" data-quiz-header>
        {step === 'detail' ? (
          <button
            type="button"
            className="gp-back-summary"
            data-back-to-summary
            onClick={backToSummaryScreen}
            aria-label="結果画面に戻る"
          >
            <ChevronLeft size={16} aria-hidden="true" />
            <span>結果へ</span>
          </button>
        ) : (
          <button
            type="button"
            className="gp-back"
            onClick={onBack}
            aria-label="単元一覧に戻る"
            title="単元一覧に戻る"
          >
            <ArrowLeft size={18} aria-hidden="true" />
          </button>
        )}
        <span className="gp-mode gp-mode-done">
          {step === 'summary' ? '演習結果' : '答え合わせ'}
        </span>
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

      {step === 'summary' ? (
        <>
          <div ref={scrollRef} className="gp-scroll">
            <div className="gp-result-summary-body">
              <ResultInsight
                chapterId={chapter.id}
                allQuestions={allQuestions}
                singleIndex={singleIndex}
                correct={correctCount}
                judgeable={totalCount}
                timeSec={resultTotalTimeSec ?? 0}
              />

              {(skillSummary.length > 0 || entries.length > 0) && (
                <section className="gp-result-qcard" aria-label="分野別・設問ごとの正誤">
                  {skillSummary.length > 0 && (
                    <p className="tp-result-skills" data-toeic-result-skills>
                      {skillSummary.map(([k, v]) => (
                        <span key={k} className="tp-result-skill">
                          <span>{k}</span>
                          <b>
                            {v.c}/{v.n}
                          </b>
                        </span>
                      ))}
                    </p>
                  )}
                  {entries.length > 1 && (
                    <>
                      <div className="gp-result-qcard-head">
                        <span>設問ごとの結果</span>
                        <span className="gp-result-qcard-hint">番号を押すとその解説へ移動</span>
                      </div>
                      <ol className="gp-jump-strip" aria-label="設問ごとの正誤">
                        {entries.map((entry) => {
                          const sym =
                            entry.status === 'correct'
                              ? '○'
                              : entry.status === 'wrong'
                              ? '×'
                              : '−';
                          return (
                            <li key={entry.sq.id}>
                              <button
                                type="button"
                                className="gp-jump-chip"
                                data-result={entry.status}
                                onClick={() => openDetailScreen(entry.sq.id)}
                                aria-label={`問${entry.no}の解説を見る`}
                              >
                                <span>{entry.no}</span>
                                <b aria-hidden="true">{sym}</b>
                              </button>
                            </li>
                          );
                        })}
                      </ol>
                    </>
                  )}
                </section>
              )}

              <ResultStage
                resultTotalJudgeable={totalCount}
                resultTotalCorrect={correctCount}
                studyReward={studyReward}
                isGuest={isGuest}
              />

              <a
                className="practice-report-link"
                data-practice-report
                href={QUESTION_REPORT_FORM_URL}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Flag size={15} aria-hidden="true" />
                この問題の不具合を報告する
              </a>
            </div>
          </div>

          <footer className="gp-summary-foot" data-practice-summary-actions>
            <div className="gp-summary-foot-inner">
              <button
                type="button"
                className="gp-btn-detail"
                data-practice-open-detail
                onClick={() => openDetailScreen()}
              >
                <BookOpen size={18} aria-hidden="true" />
                <span>
                  詳しい解説・答え合わせを見る
                  {wrongCount > 0 ? `（まちがい${wrongCount}問）` : ''}
                </span>
                <ChevronRight size={18} aria-hidden="true" />
              </button>

              <div className="gp-summary-subactions">
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
                    data-summary-next
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
              </div>
            </div>
          </footer>
        </>
      ) : (
        <>
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
                  <button type="button" className="gp-bulk-btn" onClick={() => setAllOpen(true)}>
                    解説をすべて開く
                  </button>
                  <button type="button" className="gp-bulk-btn" onClick={() => setAllOpen(false)}>
                    すべて閉じる
                  </button>
                </div>
              </div>

              {skillSummary.length > 0 && (
                <p className="tp-result-skills" data-toeic-result-skills>
                  {skillSummary.map(([k, v]) => (
                    <span key={k} className="tp-result-skill">
                      <span>{k}</span>
                      <b>
                        {v.c}/{v.n}
                      </b>
                    </span>
                  ))}
                </p>
              )}

              {entries.length > 1 && (
                <ol className="gp-jump-strip" aria-label="設問ごとの正誤">
                  {entries.map((entry) => {
                    const sym =
                      entry.status === 'correct' ? '○' : entry.status === 'wrong' ? '×' : '−';
                    return (
                      <li key={entry.sq.id}>
                        <button
                          type="button"
                          className="gp-jump-chip"
                          data-result={entry.status}
                          onClick={() => jumpToQuestion(entry.sq.id)}
                          aria-label={`問${entry.no}へ移動`}
                        >
                          <span>{entry.no}</span>
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
              {visibleEntries.map((entry) => {
                const { problem, sq, no, chosen, status } = entry;
                const texts = isListening
                  ? toeicListeningChoiceTexts(sq, true)
                  : sq.optionTexts || [];
                const ex = toeicExplanationFor(sq);
                const filled = chosen ? texts[sq.options.indexOf(chosen)] ?? '' : '';
                const correctText =
                  ex?.choices.find((c) => c.correct)?.text ??
                  texts[sq.options.indexOf(sq.correctAnswer)] ??
                  '';
                const labelId = `tp-res-q-${sq.id}`;

                return (
                  <article
                    key={sq.id}
                    id={`tp-res-item-${sq.id}`}
                    className="tp-item"
                    data-status={status}
                    data-toeic-question={no}
                  >
                    <p className="tp-sentence" id={labelId}>
                      <span className="tp-no" aria-hidden="true">
                        {no}
                      </span>
                      <span className="tp-sr">問{no}　</span>
                      <StemWithBlank
                        stem={stemForResult(problem, sq, chapter.id)}
                        filled={status === 'correct' ? correctText : filled}
                        correctWord={correctText}
                        result={
                          status === 'correct'
                            ? 'right'
                            : status === 'wrong'
                            ? 'wrong'
                            : 'blank'
                        }
                        cues={isP6 || isP7 || isListening ? undefined : ex?.cues}
                      />
                      {status === 'blank' && <span className="tp-tag">未回答</span>}
                    </p>

                    <div
                      role="group"
                      aria-labelledby={labelId}
                      aria-disabled="true"
                      className={`tp-choices is-scored${
                        prefersSingleColumn(texts) ? ' is-single' : ''
                      }`}
                    >
                      {sq.options.map((mark, i) => {
                        const checked = chosen === mark;
                        const isRight = mark === sq.correctAnswer;
                        const isWrongPick = checked && !isRight;
                        return (
                          <div
                            key={mark}
                            className="tp-choice"
                            data-checked={checked || undefined}
                            data-result={
                              isRight ? 'right' : isWrongPick ? 'wrong' : undefined
                            }
                          >
                            <span className="tp-bubble" aria-hidden="true">
                              {markLetter(mark)}
                            </span>
                            <span className="tp-choice-body">
                              <span className="tp-choice-text">
                                {formatText(texts[i] ?? mark, [], {
                                  prose: true,
                                  noMath: true,
                                })}
                              </span>
                            </span>
                            {(isRight || isWrongPick) && (
                              <span
                                className="tp-choice-badge"
                                data-tone={isRight ? 'right' : 'wrong'}
                              >
                                {isRight && checked
                                  ? 'あなた・正解'
                                  : isRight
                                  ? '正解'
                                  : 'あなた'}
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    <div className="tp-meta">
                      <p className="tp-judge" data-result={status}>
                        {status === 'correct' ? (
                          <CheckCircle2 size={17} aria-hidden="true" />
                        ) : status === 'wrong' ? (
                          <XCircle size={17} aria-hidden="true" />
                        ) : (
                          <MinusCircle size={17} aria-hidden="true" />
                        )}
                        <span>
                          {status === 'correct'
                            ? '正解'
                            : status === 'wrong'
                            ? `不正解（正解 ${sq.correctAnswer}）`
                            : `未回答（正解 ${sq.correctAnswer}）`}
                        </span>
                      </p>
                      {ex && (
                        <span className="tp-skill">
                          {ex.skill}
                          <small>{ex.subType}</small>
                        </span>
                      )}
                      {ex && (
                        <button
                          type="button"
                          className="tp-save"
                          data-saved={isSaved(sq.id) || undefined}
                          onClick={() => saveNote(entry)}
                          disabled={isSaved(sq.id)}
                        >
                          {isSaved(sq.id) ? (
                            <BookmarkCheck size={15} aria-hidden="true" />
                          ) : (
                            <Bookmark size={15} aria-hidden="true" />
                          )}
                          <span>{isSaved(sq.id) ? '保存済み' : '保存'}</span>
                        </button>
                      )}
                    </div>

                    {ex && (
                      <ToeicExplanationPanel
                        ex={ex}
                        correctText={correctText}
                        open={openEx[sq.id] ?? status !== 'correct'}
                        onToggle={(next) =>
                          setOpenEx((prev) => ({ ...prev, [sq.id]: next }))
                        }
                      />
                    )}
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
        </>
      )}
    </div>
  );
}
