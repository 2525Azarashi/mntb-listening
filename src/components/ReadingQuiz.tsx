import { useEffect, useMemo, useRef, useState } from 'react';
import { Check, ChevronRight, ListChecks, Play, RotateCcw, X } from 'lucide-react';
import { CorrectBurst } from './fx/CorrectBurst';
import { TobiraBuddy } from './TobiraBuddy';
import { play, primeAudio } from '../battle/ui/feedback';
import { recordVocabActivity } from '../battle/data/growthStore';
import { trackEvent } from '../utils/analytics';
import { safeGetItem } from '../utils/safeLocalStorage';
import { safeSetItem } from '../utils/storageGuard';
import {
  applyReadingResult, isCleared, passagesOf, READING_LEVELS, readReadingRecord, shuffledOptions, splitEvidence, wordCount, writeReadingRecord,
  type ReadingLevel, type ReadingPassage, type ReadingQuestion, type ReadingRecord,
} from '../data/reading';

/**
 * 英文解釈（内容一致の4択）2026-10-21
 *   ［一覧］レベル（Lv1〜5）→ 文章を選ぶ（または「次の文章」）
 *   ［出題］上に本文（カードの中だけスクロール）、下に設問と4択。答えると本文の根拠に色が付き、解説が出る
 *   ［結果］設問ごとの○× と解説 → 間違えた問題だけもう一度／次の文章へ
 * UI は英単語の4択（VocabQuiz）と同じ部品（vq-* / fd-*）。1画面に収め、スクロールは本文・一覧の中だけ。
 */
type Phase =
  | { kind: 'pick' }
  | { kind: 'play'; passage: ReadingPassage; qs: readonly ReadingQuestion[]; i: number; picks: (number | null)[] }
  | { kind: 'done'; passage: ReadingPassage; qs: readonly ReadingQuestion[]; picks: number[] };

const LEVEL_KEY = 'reading_quiz_level_v1';
const readLevel = (): ReadingLevel => { const n = Number(safeGetItem(LEVEL_KEY)); return (n >= 1 && n <= 5 ? n : 1) as ReadingLevel; };

export function ReadingQuiz({ uid }: { uid: string }) {
  const [level, setLevel] = useState<ReadingLevel>(readLevel);
  const [rec, setRec] = useState<ReadingRecord>(() => readReadingRecord(uid));
  const [phase, setPhase] = useState<Phase>({ kind: 'pick' });
  const textRef = useRef<HTMLDivElement>(null);
  const qRef = useRef<HTMLDivElement>(null);
  /** スマホ（幅899px以下）だけ：本文を広げて読む／設問を解く の切り替え。PC は常に左右に並べる */
  const [pane, setPane] = useState<'text' | 'q'>('text');

  useEffect(() => { safeSetItem(LEVEL_KEY, String(level)); }, [level]);
  useEffect(() => { setRec(readReadingRecord(uid)); }, [uid]);

  const list = useMemo(() => passagesOf(level), [level]);
  const missed = useMemo(() => new Set(rec.missed), [rec.missed]);
  const nextOf = (lv: ReadingLevel, after?: string) => {
    const ps = passagesOf(lv);
    const start = after ? ps.findIndex(x => x.id === after) + 1 : 0;
    const rest = [...ps.slice(start), ...ps.slice(0, start)];
    return rest.find(x => !isCleared(rec, x) && x.id !== after) ?? (after ? ps[start % ps.length] : ps[0]);
  };

  const begin = (passage: ReadingPassage, qs: readonly ReadingQuestion[] = passage.questions) => {
    if (!qs.length) return;
    primeAudio();
    trackEvent('reading_start', { lv: passage.level });
    setLevel(passage.level);
    setPhase({ kind: 'play', passage, qs, i: 0, picks: qs.map(() => null) });
    // はじめて読む文章は本文から。間違えた問題の解き直しは設問から
    setPane(qs.length === passage.questions.length ? 'text' : 'q');
  };

  // 答えたら根拠の一節までスクロールする
  const playKey = phase.kind === 'play' ? `${phase.passage.id}:${phase.i}:${phase.picks[phase.i] ?? ''}` : '';
  useEffect(() => {
    if (phase.kind !== 'play') return;
    const box = textRef.current; if (!box) return;
    const mark = box.querySelector('mark');
    if (mark) {
      const top = (mark as HTMLElement).offsetTop - box.offsetTop - 12;
      box.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
    }
    // 解説が設問の欄の下に隠れないように
    const ex = qRef.current?.querySelector('[data-reading-explain]');
    if (ex && qRef.current) qRef.current.scrollTo({ top: qRef.current.scrollHeight, behavior: 'smooth' });
  }, [playKey]); // eslint-disable-line react-hooks/exhaustive-deps

  if (phase.kind === 'play') {
    const { passage, qs, i, picks } = phase;
    const q = qs[i]!;
    const view = shuffledOptions(q);
    const pick = picks[i];
    const answered = pick !== null;
    const ok = pick === view.answerIndex;
    const ans = (j: number) => shuffledOptions(qs[j]!).answerIndex;
    const quit = () => {
      const results = qs.flatMap((x, j) => picks[j] === null ? [] : [{ questionId: x.id, correct: picks[j] === ans(j) }]);
      // 途中でやめたときは「間違えた設問」だけ記録し、最高点は変えない
      if (results.length) { const r = { ...applyReadingResult(rec, passage.id, results), best: rec.best }; writeReadingRecord(uid, r); setRec(r); }
      setPhase({ kind: 'pick' });
    };
    const choose = (k: number) => {
      if (answered) return;
      const good = k === view.answerIndex;
      play(good ? 'correct' : 'wrong', !good);
      const next = picks.slice(); next[i] = k;
      setPhase({ ...phase, picks: next });
    };
    const next = () => {
      if (i + 1 < qs.length) { setPhase({ ...phase, i: i + 1 }); setPane('q'); qRef.current?.scrollTo({ top: 0 }); return; }
      const all = picks as number[];
      const results = qs.map((x, j) => ({ questionId: x.id, correct: all[j] === ans(j) }));
      const full = qs.length === passage.questions.length;
      // 一部の設問だけ解き直したときは、最高点は更新せず「間違えた設問」だけ直す
      const r0 = applyReadingResult(rec, passage.id, results);
      const r = full ? r0 : { ...r0, best: rec.best };
      writeReadingRecord(uid, r); setRec(r);
      const score = results.filter(x => x.correct).length;
      void recordVocabActivity('vocab_quiz');
      trackEvent('reading_done', { lv: passage.level, ok: score });
      play(score === qs.length ? 'win' : score >= qs.length / 2 ? 'levelup' : 'tap', false);
      setPhase({ kind: 'done', passage, qs, picks: all });
    };
    const ev = splitEvidence(passage.text, answered ? q.evidence : null);
    return <section className="fd-panel vq-play rq-play" aria-label="英文解釈" data-reading="play">
      <div className="vq-top">
        <button type="button" className="fd-chip" onClick={quit} aria-label="やめて文章の一覧にもどる（答えた分は記録する）"><X size={16} aria-hidden="true" />やめる</button>
        <ol className="vq-dots" aria-label={`${i + 1}問目 / 全${qs.length}問`}>{qs.map((x, j) => {
          const pk = picks[j];
          return <li key={x.id} data-now={j === i || undefined} data-state={pk === null ? undefined : pk === ans(j) ? 'ok' : 'ng'} />;
        })}</ol>
        <b className="vq-count">{i + 1}<small>/{qs.length}</small></b>
      </div>
      <div className="vq-seg rq-view" role="radiogroup" aria-label="表示">
        <button type="button" role="radio" aria-checked={pane === 'text'} onClick={() => setPane('text')} data-reading-view="text">本文を読む</button>
        <button type="button" role="radio" aria-checked={pane === 'q'} onClick={() => setPane('q')} data-reading-view="q">問{passage.questions.indexOf(q) + 1}を解く</button>
      </div>
      <div className="rq-body" data-view={pane}>
        <article className="rq-passage" aria-label="本文">
          <header className="rq-passage-head"><b lang="en">{passage.title}</b><small>{READING_LEVELS[passage.level - 1]!.name}・{wordCount(passage.text)}語</small></header>
          <div className="rq-text" ref={textRef} lang="en" tabIndex={0} aria-label="本文（この中をスクロール）" data-reading-text>
            {renderText(ev.before)}{ev.mark && <mark data-reading-evidence>{ev.mark}</mark>}{renderText(ev.after)}
          </div>
        </article>
        <div className="rq-q" ref={qRef}>
          <p className="rq-prompt" key={q.id} lang={/[ぁ-んァ-ン一-龥]/.test(q.prompt) ? 'ja' : 'en'}><span className="rq-qno">問{passage.questions.indexOf(q) + 1}</span>{q.prompt}</p>
          <div className="vq-options rq-options" role="group" aria-label="選択肢">{view.options.map((o, k) => <button key={k} type="button" disabled={answered} onClick={() => choose(k)}
            lang={/[ぁ-んァ-ン一-龥]/.test(o) ? 'ja' : 'en'}
            data-correct={answered && k === view.answerIndex ? true : undefined} data-wrong={answered && pick === k && k !== view.answerIndex ? true : undefined}>
            <i aria-hidden="true">{'①②③④'[k]}</i><span>{o}</span>{answered && k === view.answerIndex && <Check size={18} aria-hidden="true" />}
          </button>)}</div>
          {answered && <p className="rq-explain" data-reading-explain><b>{ok ? '正解！' : `正解は ${'①②③④'[view.answerIndex]}`}</b>{q.explanation}</p>}
        </div>
      </div>
      {answered && ok && <CorrectBurst burstKey={q.id} combo={streakAt(qs, picks, i)} />}
      <div className="vq-foot" aria-live="polite">
        {answered ? <>
          <p className="vq-judge" data-ok={ok || undefined}>{ok ? '正解！' : '根拠を本文で確認'}</p>
          <button type="button" className="vq-next" onClick={next} autoFocus data-reading-next>{i + 1 < qs.length ? '次の問題' : '結果を見る'}<ChevronRight size={18} aria-hidden="true" /></button>
        </> : pane === 'text'
          ? <><p className="vq-hint rq-hint-wide">本文を読んで、内容に合うものを選ぼう</p><button type="button" className="vq-next rq-to-q" onClick={() => setPane('q')} data-reading-to-q>読めたら 問{passage.questions.indexOf(q) + 1} へ<ChevronRight size={18} aria-hidden="true" /></button></>
          : <p className="vq-hint">本文を読んで、内容に合うものを選ぼう</p>}
      </div>
    </section>;
  }

  if (phase.kind === 'done') {
    const { passage, qs, picks } = phase;
    const ans = (j: number) => shuffledOptions(qs[j]!).answerIndex;
    const good = (j: number) => picks[j] === ans(j);
    const score = qs.filter((_, j) => good(j)).length;
    const wrong = qs.filter((_, j) => !good(j));
    const nx = nextOf(passage.level, passage.id);
    const leftInLevel = passagesOf(passage.level).filter(x => !isCleared(rec, x)).length;
    const line = score === qs.length
      ? (leftInLevel === 0 ? `${READING_LEVELS[passage.level - 1]!.name} はぜんぶ満点！ 次のレベルへ` : `満点！ このレベルのまだの文章は あと${leftInLevel}題`)
      : score === 0 ? '根拠の一文を見直して、もう一度やってみよう' : 'おしい！ 間違えた問題の根拠を見直そう';
    return <section className="fd-panel vq-done rq-done" aria-label="結果" data-reading="done">
      <div className="vq-score" data-perfect={score === qs.length || undefined}>
        <strong>{score}<small>/{qs.length}</small></strong>
        <span className="vq-score-body"><b className="vq-score-title" lang="en">{passage.title}</b><TobiraBuddy size="sm" input={{ screen: 'study' }} line={line} /></span>
      </div>
      <ul className="rq-result" aria-label="設問ごとの結果">{qs.map((x, j) => {
        const v = shuffledOptions(x);
        return <li key={x.id} data-ok={good(j) || undefined}>
          <p className="rq-result-q">{good(j) ? <Check size={16} aria-label="正解" /> : <X size={16} aria-label="不正解" />}<span>問{passage.questions.indexOf(x) + 1}　{x.prompt}</span></p>
          <p className="rq-result-a">正解：{v.options[v.answerIndex]}</p>
          <p className="rq-result-e">{x.explanation}</p>
        </li>;
      })}</ul>
      <div className="vq-done-actions">
        {wrong.length > 0 && <button type="button" className="vq-next" onClick={() => begin(passage, wrong)} data-reading-retry><RotateCcw size={17} aria-hidden="true" />間違えた{wrong.length}問だけもう一度</button>}
        {nx && nx.id !== passage.id && <button type="button" className={wrong.length ? 'fd-secondary' : 'vq-next'} onClick={() => begin(nx)} data-reading-continue>次の文章へ（{nx.title}）<ChevronRight size={16} aria-hidden="true" /></button>}
        {leftInLevel === 0 && passage.level < 5 && <button type="button" className="fd-secondary" onClick={() => { setLevel((passage.level + 1) as ReadingLevel); setPhase({ kind: 'pick' }); }}>次のレベル（{READING_LEVELS[passage.level]!.name}）へ<ChevronRight size={16} aria-hidden="true" /></button>}
        <button type="button" className="fd-secondary" onClick={() => setPhase({ kind: 'pick' })}><ListChecks size={16} aria-hidden="true" />文章の一覧へ</button>
      </div>
    </section>;
  }

  // ---------------- 文章の一覧 ----------------
  const meta = READING_LEVELS[level - 1]!;
  const cleared = list.filter(x => isCleared(rec, x)).length;
  const first = nextOf(level);
  return <section className="fd-panel vq-setup rq-pick" aria-label="文章を選ぶ" data-reading="pick">
    <div className="fd-levels" role="tablist" aria-label="レベル">{READING_LEVELS.map(l => {
      const ps = passagesOf(l.level); const got = ps.filter(x => isCleared(rec, x)).length;
      return <button key={l.level} type="button" role="tab" aria-selected={level === l.level} onClick={() => setLevel(l.level)} data-reading-level={l.level}>
        <span>{l.name}</span><small>{got}/{ps.length}題</small><i aria-hidden="true" style={{ ['--p' as string]: `${ps.length ? got / ps.length * 100 : 0}%` }} />
      </button>;
    })}</div>
    <p className="rq-target">目安：{meta.target}</p>
    <ul className="rq-list vq-set-scroll" aria-label={`${meta.name}の文章`}>{list.map((x, k) => {
      const b = rec.best[x.id]; const done = isCleared(rec, x);
      const miss = x.questions.filter(qq => missed.has(qq.id)).length;
      return <li key={x.id}><button type="button" onClick={() => begin(x)} data-reading-passage={x.id} data-state={done ? 'clear' : b ? 'part' : undefined}>
        <i className="rq-no" aria-hidden="true">{k + 1}</i>
        <span className="rq-item-main"><b lang="en">{x.title}</b><small>{x.topic}・{wordCount(x.text)}語・{x.questions.length}問</small></span>
        <span className="rq-item-score">{done ? <><Check size={15} aria-hidden="true" />満点</> : b ? `${b.score}/${b.total}` : 'まだ'}{miss > 0 && <em>×{miss}</em>}</span>
      </button></li>;
    })}</ul>
    <div className="vq-start-box">
      <p className="vq-start-sum" aria-live="polite">{meta.name}：満点 <b>{cleared}</b>/{list.length}題{first && <>　・次は「{first.title}」</>}</p>
      <button type="button" className="vq-next vq-start" onClick={() => first && begin(first)} disabled={!first} data-reading-start><Play size={18} aria-hidden="true" />{cleared === list.length ? 'もう一度はじめから解く' : '次の文章を解く'}</button>
    </div>
  </section>;
}

/** 段落（空行区切り）を <p> にする */
function renderText(s: string) {
  if (!s) return null;
  const parts = s.split(/\n\s*\n/);
  return parts.map((t, k) => <span key={k} className="rq-para">{t}{k < parts.length - 1 && <><br /><br /></>}</span>);
}

function streakAt(qs: readonly ReadingQuestion[], picks: readonly (number | null)[], i: number): number {
  let n = 0;
  for (let j = i; j >= 0; j--) { if (picks[j] !== null && picks[j] === shuffledOptions(qs[j]!).answerIndex) n++; else break; }
  return n;
}
