/**
 * 英文法カード共通パーツ：
 *   - `GrammarMarkedText`：手がかり語句に番号つき黄色マーカー（`¹` `²`）を描画
 *   - `GrammarInlineBlank`：英文中の `______` を下線空所ボックスに変換し、採点後は `[誤答 → 正解]` 比較＋手がかりマーカーを表示
 *   - `GrammarQuestionStem`：`A` / `B` 話者ピル付きの会話ターン、`(a)/(b)` 等の複数行書き換え、または番号バッジ付き1文表示
 *   - `GrammarCompactReview`：正解時は1行折りたたみ、誤答・未回答時は「和訳」「要点（手がかりマーカー連動）」「音声」「着眼点・4択すべての理由・補足・入試ポイント」を表示
 */
import React, { useState } from 'react';
import {
  Bookmark,
  BookmarkCheck,
  CheckCircle2,
  ChevronDown,
  MinusCircle,
  Square,
  Volume2,
  XCircle,
} from 'lucide-react';
import { formatText } from '../../utils/textFormatter';
import {
  grammarCueMarksInWhy,
  splitGrammarByMarks,
  splitGrammarDialogueTurns,
  type GrammarResolvedCue,
  type GrammarSubReview,
} from './grammarPageModel';
import {
  isGrammarSpeechAvailable,
  playGrammarSentenceAudio,
  stopGrammarSpeech,
} from './grammarSpeech';

export function GrammarMarkedText({
  text,
  marks,
}: {
  text: string;
  marks?: readonly { start: number; length: number; n: number }[];
}) {
  if (!text) return null;
  if (!marks || marks.length === 0) {
    return <span>{formatText(text, [], { prose: true, noMath: true })}</span>;
  }
  return (
    <>
      {splitGrammarByMarks(text, marks).map((piece, i) =>
        piece.cue ? (
          <mark
            key={i}
            className="gp-cue"
            data-grammar-cue={piece.cue}
            aria-label={`手がかり${piece.cue}`}
          >
            <sup aria-hidden="true">{piece.cue}</sup>
            {piece.text}
          </mark>
        ) : (
          <span key={i}>{formatText(piece.text, [], { prose: true, noMath: true })}</span>
        ),
      )}
    </>
  );
}

export function GrammarInlineBlank({
  line,
  filled,
  correctWord,
  result,
  marks,
}: {
  line: string;
  filled: string;
  correctWord?: string;
  result?: 'right' | 'wrong' | 'blank';
  marks?: readonly { start: number; length: number; n: number }[];
}) {
  const match = line.match(/_{3,}|\(\s*_{0,6}\s*\)/);
  if (!match || match.index === undefined) {
    return <GrammarMarkedText text={line} marks={marks} />;
  }
  const blankStart = match.index;
  const blankLen = match[0].length;
  const before = line.slice(0, blankStart);
  const after = line.slice(blankStart + blankLen);
  const afterMarks = (marks || []).map((m) => ({
    ...m,
    start: m.start - blankStart - blankLen,
  }));
  const showCorrection = (result === 'wrong' || result === 'blank') && Boolean(correctWord);

  return (
    <>
      {before && <GrammarMarkedText text={before} marks={marks} />}
      {showCorrection ? (
        <span className="gp-blank-compare" data-grammar-blank>
          {result === 'wrong' && filled && (
            <>
              <span className="gp-blank" data-filled data-result="wrong">
                {formatText(filled, [], { prose: true, noMath: true })}
              </span>
              <span className="gp-blank-arrow" aria-hidden="true">
                →
              </span>
            </>
          )}
          <span className="gp-blank" data-filled data-result="right">
            {formatText(correctWord || '', [], { prose: true, noMath: true })}
          </span>
        </span>
      ) : (
        <span
          className="gp-blank"
          data-filled={filled ? true : undefined}
          data-result={result === 'blank' ? undefined : result}
          data-grammar-blank
        >
          {filled ? formatText(filled, [], { prose: true, noMath: true }) : <span className="gp-sr">空所</span>}
        </span>
      )}
      {after && <GrammarMarkedText text={after} marks={afterMarks} />}
    </>
  );
}

function sliceMarksForSubstring(
  fullStem: string,
  subText: string,
  fromOffset: number,
  cues?: readonly GrammarResolvedCue[],
): { nextOffset: number; marks: { start: number; length: number; n: number }[] } {
  if (!cues || cues.length === 0) {
    return { nextOffset: fromOffset + subText.length, marks: [] };
  }
  const foundIdx = fullStem.indexOf(subText, fromOffset);
  const base = foundIdx >= 0 ? foundIdx : fromOffset;
  const marks = cues
    .map((c) => ({
      start: c.start - base,
      length: c.phrase.length,
      n: c.n,
    }))
    .filter((m) => m.start >= 0 && m.start + m.length <= subText.length);
  return { nextOffset: base + subText.length, marks };
}

export function GrammarQuestionStem({
  displayNo,
  stem,
  filled,
  correctWord,
  result,
  unansweredTag,
  focusLabel,
  labelId,
  cues,
}: {
  displayNo: number;
  stem: string;
  filled: string;
  correctWord?: string;
  result?: 'right' | 'wrong' | 'blank';
  unansweredTag?: boolean;
  focusLabel?: string;
  labelId: string;
  cues?: readonly GrammarResolvedCue[];
}) {
  const activeCues = result ? cues : undefined;
  const turns = splitGrammarDialogueTurns(stem);
  if (turns) {
    let cursor = 0;
    return (
      <div className="gp-dialogue-wrap" id={labelId}>
        <div className="gp-dialogue-head">
          <span className="gp-no" aria-hidden="true">
            {displayNo}
          </span>
          <span className="gp-sr">問{displayNo}　</span>
          <span className="gp-dialogue-kicker">{focusLabel || '会話表現'}</span>
          {unansweredTag && (
            <span className="gp-unanswered-tag" data-grammar-unanswered>
              未回答
            </span>
          )}
        </div>
        <div className="gp-dialogue-turns">
          {turns.map((turn, idx) => {
            const sliced = sliceMarksForSubstring(stem, turn.text, cursor, activeCues);
            cursor = sliced.nextOffset;
            return (
              <div key={idx} className="gp-turn" data-speaker={turn.speaker}>
                <span className="gp-speaker-pill" data-speaker={turn.speaker} aria-hidden="true">
                  {turn.speaker}
                </span>
                <span className="gp-sr">{turn.speaker}: </span>
                <p className="gp-turn-text" lang="en">
                  <GrammarInlineBlank
                    line={turn.text}
                    filled={filled}
                    correctWord={correctWord}
                    result={result}
                    marks={sliced.marks}
                  />
                </p>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // `(a) ... \n (b) ...` などの複数行問題文は行ごとに見やすく整形して描画する
  const stemLines = stem.includes('\n')
    ? stem
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
    : null;

  if (stemLines && stemLines.length >= 2) {
    let lineCursor = 0;
    return (
      <div className="gp-stem-block" id={labelId}>
        <div className="gp-dialogue-head">
          <span className="gp-no" aria-hidden="true">
            {displayNo}
          </span>
          <span className="gp-sr">問{displayNo}　</span>
          {focusLabel && result && <span className="gp-focus-tag">{focusLabel}</span>}
          {unansweredTag && (
            <span className="gp-unanswered-tag" data-grammar-unanswered>
              未回答
            </span>
          )}
        </div>
        <div className="gp-multiline-stem">
          {stemLines.map((line, i) => {
            const sliced = sliceMarksForSubstring(stem, line, lineCursor, activeCues);
            lineCursor = sliced.nextOffset;
            return (
              <p key={i} className="gp-sentence gp-sentence-line" lang="en">
                <GrammarInlineBlank
                  line={line}
                  filled={filled}
                  correctWord={correctWord}
                  result={result}
                  marks={sliced.marks}
                />
              </p>
            );
          })}
        </div>
      </div>
    );
  }

  const fullMarks = (activeCues || []).map((c) => ({
    start: c.start,
    length: c.phrase.length,
    n: c.n,
  }));

  return (
    <div className="gp-stem-block" id={labelId}>
      <p className="gp-sentence">
        <span className="gp-no" aria-hidden="true">
          {displayNo}
        </span>
        <span className="gp-sr">問{displayNo}　</span>
        <span lang="en">
          <GrammarInlineBlank
            line={stem}
            filled={filled}
            correctWord={correctWord}
            result={result}
            marks={fullMarks}
          />
        </span>
        {focusLabel && result && <span className="gp-focus-tag">{focusLabel}</span>}
        {unansweredTag && (
          <span className="gp-unanswered-tag" data-grammar-unanswered>
            未回答
          </span>
        )}
      </p>
    </div>
  );
}

export function GrammarCompactReview({
  review,
  isOpen,
  onToggleOpen,
  saved,
  onSaveNote,
  speakingKey,
  setSpeakingKey,
}: {
  review: GrammarSubReview;
  isOpen: boolean;
  onToggleOpen: (open: boolean) => void;
  saved: boolean;
  onSaveNote: () => void;
  speakingKey: string | null;
  setSpeakingKey: React.Dispatch<React.SetStateAction<string | null>>;
}) {
  const [reasonsOpen, setReasonsOpen] = useState(false);
  const {
    sq,
    displayNo,
    status,
    translation,
    why,
    hint,
    examTip,
    memorizeSet,
    plus,
    choices,
    cues,
    audioUrl,
    completedSentence,
    keyPhrase,
  } = review;

  const canPlay = isGrammarSpeechAvailable(audioUrl);
  const normalKey = `${sq.id}:normal`;
  const slowKey = `${sq.id}:slow`;

  const togglePlay = (key: string, rate: number) => {
    if (speakingKey === key) {
      stopGrammarSpeech();
      setSpeakingKey(null);
      return;
    }
    playGrammarSentenceAudio({
      audioUrl,
      text: completedSentence,
      rate,
      onStart: () => setSpeakingKey(key),
      onEnd: () => setSpeakingKey((cur) => (cur === key ? null : cur)),
    });
  };

  const hasChoiceReasons = choices.some((c) => Boolean(c.reason));
  const showHintInDetail = Boolean(hint && hint !== why);
  const whyMarks = grammarCueMarksInWhy(cues || []);

  return (
    <div className="gp-compact-review" data-grammar-explanation>
      <div className="gp-review-bar">
        <button
          type="button"
          className="gp-disclosure-btn"
          aria-expanded={isOpen}
          onClick={() => onToggleOpen(!isOpen)}
        >
          <span className="gp-judge" data-result={status}>
            {status === 'correct' ? (
              <CheckCircle2 size={16} aria-hidden="true" />
            ) : status === 'wrong' ? (
              <XCircle size={16} aria-hidden="true" />
            ) : (
              <MinusCircle size={16} aria-hidden="true" />
            )}
            <span>
              {status === 'correct'
                ? '正解'
                : status === 'wrong'
                ? `不正解（正解 ${sq.correctAnswer}）`
                : `未回答（正解 ${sq.correctAnswer}）`}
            </span>
          </span>
          <span className="gp-ex-toggle-hint">{isOpen ? '閉じる' : '解説を見る'}</span>
          <ChevronDown size={16} className={`gp-chev${isOpen ? ' is-open' : ''}`} aria-hidden="true" />
        </button>

        <button
          type="button"
          className="gp-save-btn"
          data-saved={saved || undefined}
          disabled={saved}
          onClick={onSaveNote}
          aria-label={saved ? `問${displayNo}はノート保存済み` : `問${displayNo}をノートに保存`}
        >
          {saved ? <BookmarkCheck size={14} aria-hidden="true" /> : <Bookmark size={14} aria-hidden="true" />}
          <span>{saved ? '保存済' : '保存'}</span>
        </button>
      </div>

      {isOpen && (
        <div className="gp-ex-body">
          {translation && (
            <p className="gp-ex-line" data-role="tr">
              <span className="gp-ex-pill">和訳</span>
              <span>{formatText(translation, [], { prose: true, noMath: true })}</span>
            </p>
          )}
          {why && (
            <p className="gp-ex-line gp-ex-line-key" data-role="key">
              <span className="gp-ex-pill gp-ex-pill-key">要点</span>
              <span>
                <GrammarMarkedText text={why} marks={whyMarks} />
              </span>
            </p>
          )}
          {memorizeSet && (
            <p className="gp-ex-line gp-ex-line-tip" data-role="set">
              <span className="gp-ex-pill gp-ex-pill-tip">セット</span>
              <span>{formatText(memorizeSet, [], { prose: true, noMath: true })}</span>
            </p>
          )}

          {(canPlay || keyPhrase) && (
            <div className="gp-ex-subtools">
              {canPlay && (
                <>
                  <button
                    type="button"
                    className="gp-speak-btn"
                    data-speaking={speakingKey === normalKey || undefined}
                    onClick={() => togglePlay(normalKey, 1)}
                    aria-label={speakingKey === normalKey ? '音声を停止' : '完成文の音声を再生'}
                  >
                    {speakingKey === normalKey ? (
                      <Square size={12} aria-hidden="true" />
                    ) : (
                      <Volume2 size={13} aria-hidden="true" />
                    )}
                    <span>{speakingKey === normalKey ? '停止' : '音声'}</span>
                  </button>
                  <button
                    type="button"
                    className="gp-speak-btn is-slow"
                    data-speaking={speakingKey === slowKey || undefined}
                    onClick={() => togglePlay(slowKey, 0.8)}
                    aria-label="完成文の音声をゆっくり再生"
                  >
                    <span>ゆっくり</span>
                  </button>
                </>
              )}
              {keyPhrase && (
                <span className="gp-key-chip">
                  <strong lang="en">{keyPhrase.phrase}</strong>
                  {keyPhrase.meaning && <span>{keyPhrase.meaning}</span>}
                </span>
              )}
            </div>
          )}

          {(showHintInDetail || hasChoiceReasons || examTip || plus) && (
            <div className="gp-reasons-fold">
              <button
                type="button"
                className="gp-reasons-btn"
                aria-expanded={reasonsOpen}
                onClick={() => setReasonsOpen((prev) => !prev)}
              >
                <span>{reasonsOpen ? '選択肢の理由・補足を閉じる' : '他の選択肢の理由・入試ポイントを見る'}</span>
                <ChevronDown size={14} className={`gp-chev${reasonsOpen ? ' is-open' : ''}`} aria-hidden="true" />
              </button>
              {reasonsOpen && (
                <div className="gp-ex-body">
                  {showHintInDetail && !why.includes(hint.replace(/。$/, '')) && (
                    <p className="gp-ex-line gp-ex-line-hint" data-role="hint">
                      <span className="gp-ex-pill gp-ex-pill-hint">着眼点</span>
                      <span>{formatText(hint, [], { prose: true, noMath: true })}</span>
                    </p>
                  )}
                  {hasChoiceReasons && (
                    <ul className="gp-ex-choices">
                      {choices.map((c) => (
                        <li key={c.mark} data-correct={c.correct || undefined}>
                          <span className="gp-ex-mark" aria-hidden="true">
                            {c.correct ? '○' : '×'}
                          </span>
                          <span className="gp-ex-choice-body">
                            <b className="gp-ex-choice-word" lang="en">
                              {c.mark} {formatText(c.text, [], { prose: true, noMath: true })}
                            </b>
                            <span className="gp-ex-choice-reason">
                              {c.reason ? formatText(c.reason, [], { prose: true, noMath: true }) : c.correct ? '正解' : ''}
                            </span>
                          </span>
                        </li>
                      ))}
                    </ul>
                  )}
                  {plus && (
                    <p className="gp-ex-line" data-role="plus">
                      <span className="gp-ex-pill">補足</span>
                      <span>{formatText(plus, [], { prose: true, noMath: true })}</span>
                    </p>
                  )}
                  {examTip && (
                    <p className="gp-ex-line gp-ex-line-tip" data-role="tip">
                      <span className="gp-ex-pill gp-ex-pill-tip">入試</span>
                      <span>{formatText(examTip, [], { prose: true, noMath: true })}</span>
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
