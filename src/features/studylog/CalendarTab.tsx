/**
 * マイページの「カレンダー」タブ（2026-10-29 B8 作り直し・StudyPlus 風）。
 *   日付を押すと黒くなり、その日の勉強時間がすぐ下のグラフに加わる。別の日を押すとその日も並ぶ（最大7日）。
 *   もう一度押すとその日はグラフから消える。7日を超えたら、いちばん前に押した日を外す。
 *   グラフ＝日ごとの積み上げ棒（アプリで計った時間＋自分で記録した分を教科の色で）。合計・平均・いちばん長い日も出す。
 *   ボタンは増やさない（カレンダーの日付だけで操作）。最後に押した日の記録は下に並び、自分で記録した行は押すと直す・消す。
 */
import { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { addMonths, dayOf, monthGrid, monthOf, subjectLabel, type ManualLogStore, type ManualRecord } from './manualLogCore';
import { fmtDay, fmtMin, fmtSec } from './ui';

const WD = ['月', '火', '水', '木', '金', '土', '日'];
const WD_SUN = ['日', '月', '火', '水', '木', '金', '土'];
export const PICK_MAX = 7;
const PALETTE = ['#e8a33d', '#4f9d69', '#d9644a', '#7a6bc4', '#3f8fc0', '#c2577d', '#8a6d3b', '#5aa6a0'];
const level = (sec: number) => (sec <= 0 ? 0 : sec < 1800 ? 1 : sec < 3600 ? 2 : sec < 7200 ? 3 : 4);
const short = (d: string) => { const t = new Date(`${d}T12:00:00`); return { md: `${t.getMonth() + 1}/${t.getDate()}`, wd: WD_SUN[t.getDay()] }; };

/** 押した日の並び（押した順）を切りかえる。もう一度押すと外す。7日を超えたら最初に押した日を外す */
export function togglePick(picks: string[], day: string, max = PICK_MAX): string[] {
  if (picks.includes(day)) return picks.filter(d => d !== day);
  const next = [...picks, day];
  return next.length > max ? next.slice(next.length - max) : next;
}

export function CalendarTab({ store, app, onEdit }: {
  store: ManualLogStore; app: { days: Record<string, number> }; onEdit: (r: ManualRecord) => void;
}) {
  const today = dayOf(Date.now());
  const [month, setMonth] = useState(monthOf(today));
  /** 押した順。グラフは日付の順に並べる */
  const [picks, setPicks] = useState<string[]>([today]);
  const cells = monthGrid(month);
  const byDay = useMemo(() => {
    const m = new Map<string, ManualRecord[]>();
    for (const r of store.records) if (!r.deleted) m.set(r.day, [...(m.get(r.day) ?? []), r]);
    return m;
  }, [store]);
  const selfSec = (d: string) => (byDay.get(d) ?? []).reduce((n, r) => n + r.minutes * 60, 0);
  const total = (d: string) => (app.days[d] ?? 0) + selfSec(d);
  const studied = cells.filter((d): d is string => !!d && d <= today && total(d) > 0).length;
  const [y, mo] = month.split('-').map(Number);
  const minMonth = monthOf(dayOf(Date.now() - 730 * 86_400_000));
  const move = (n: number) => setMonth(addMonths(month, n));

  // ── グラフ：日付の順。教科ごとに色を分けて積み上げる（アプリ内はブランド色） ──
  const sorted = picks.slice().sort();
  const subjects = useMemo(() => {
    const ids: string[] = [];
    for (const d of sorted) for (const r of byDay.get(d) ?? []) if (!ids.includes(r.subject)) ids.push(r.subject);
    return ids;
  }, [sorted.join(), byDay]);
  const color = (s: string) => PALETTE[subjects.indexOf(s) % PALETTE.length];
  const parts = (d: string) => {
    const list: { key: string; label: string; sec: number; color: string }[] = [];
    if ((app.days[d] ?? 0) > 0) list.push({ key: 'app', label: 'マナトビ', sec: app.days[d], color: 'var(--mt-brand)' });
    for (const s of subjects) {
      const sec = (byDay.get(d) ?? []).filter(r => r.subject === s).reduce((n, r) => n + r.minutes * 60, 0);
      if (sec > 0) list.push({ key: s, label: subjectLabel(s), sec, color: color(s) });
    }
    return list;
  };
  const totals = sorted.map(total);
  const sum = totals.reduce((a, b) => a + b, 0);
  const peak = Math.max(1800, ...totals);
  const best = sorted.length > 1 && sum > 0 ? sorted[totals.indexOf(Math.max(...totals))] : null;
  const legend = [...((sorted.some(d => (app.days[d] ?? 0) > 0)) ? [{ key: 'app', label: 'マナトビ', color: 'var(--mt-brand)' }] : []),
    ...subjects.map(s => ({ key: s, label: subjectLabel(s), color: color(s) }))];

  // ── 最後に押した日の記録（直す・消す用） ──
  const focus = picks[picks.length - 1] ?? null;
  const rows = focus ? (byDay.get(focus) ?? []).slice().sort((a, b) => b.createdAt - a.createdAt) : [];

  return <>
    <div className="slog-month">
      <button type="button" onClick={() => move(-1)} disabled={month <= minMonth} aria-label="前の月"><ChevronLeft size={20} aria-hidden="true" /></button>
      <h3 aria-live="polite">{y}年{mo}月<small>　勉強した日 {studied}日</small></h3>
      <button type="button" onClick={() => move(1)} disabled={month >= monthOf(today)} aria-label="次の月"><ChevronRight size={20} aria-hidden="true" /></button>
    </div>
    <ol className="slog-cal" aria-label={`${y}年${mo}月の勉強カレンダー（日付を押すとグラフに加わる・最大${PICK_MAX}日）`} data-slog-calendar>
      {WD.map(w => <li key={w} aria-hidden="true"><span>{w}</span></li>)}
      {cells.map((d, i) => d
        ? <li key={d}><button type="button" className="slog-cell" disabled={d > today} aria-pressed={picks.includes(d)}
            data-lv={level(total(d)) || undefined} data-today={d === today || undefined} data-self={byDay.has(d) || undefined} data-future={d > today || undefined} data-day={d}
            onClick={() => setPicks(p => togglePick(p, d))}
            aria-label={`${fmtDay(d)} ${total(d) > 0 ? `勉強 ${fmtSec(total(d))}` : '記録なし'}`}>{Number(d.slice(8))}</button></li>
        : <li key={`x${i}`} aria-hidden="true" />)}
    </ol>
    <section className="slog-compare" aria-live="polite" aria-label="選んだ日の勉強時間グラフ" data-slog-compare data-count={sorted.length}>
      {sorted.length === 0
        ? <p className="slog-note">カレンダーの日付を押すと、その日の勉強時間がここにグラフで出ます（最大{PICK_MAX}日まで並べて比べられます）。</p>
        : <>
          <header className="slog-compare-head">
            <strong>{sorted.length}日分</strong>
            <span>合計 <b>{fmtSec(sum)}</b></span>
            {sorted.length > 1 && <span>平均 <b>{fmtSec(Math.round(sum / sorted.length))}</b></span>}
            {best && <span>最長 <b>{short(best).md}</b></span>}
          </header>
          <ol className="slog-bars" data-slog-bars>
            {sorted.map((d, i) => {
              const s = short(d);
              return <li key={d} data-day={d} data-focus={d === focus || undefined} data-best={d === best || undefined}>
                <em>{totals[i] > 0 ? fmtSec(totals[i]) : '0分'}</em>
                <div className="slog-bar-track" aria-hidden="true">
                  {parts(d).map(p => <i key={p.key} style={{ height: `${(p.sec / peak) * 100}%`, background: p.color }} title={`${p.label} ${fmtSec(p.sec)}`} />)}
                </div>
                <span>{s.md}<small>{s.wd}</small></span>
              </li>;
            })}
          </ol>
          {legend.length > 0 && <p className="slog-compare-legend" aria-hidden="true">{legend.map(l => <span key={l.key}><i style={{ background: l.color }} />{l.label}</span>)}</p>}
        </>}
    </section>
    {focus && <section className="slog-scroll slog-picked" tabIndex={0} aria-label={`${fmtDay(focus)}の勉強記録`} data-slog-day={focus}>
      <h4>{fmtDay(focus)}<small>合計 {fmtSec(total(focus))}</small></h4>
      {total(focus) === 0
        ? <p className="slog-note">この日の記録はありません。</p>
        : <ul className="slog-rows">
            {(app.days[focus] ?? 0) > 0 && <li><div className="slog-row" data-app-row>
              <span><strong>マナトビ（アプリ内）</strong><small>演習・解説の画面で計った時間</small></span><b>{fmtSec(app.days[focus])}</b>
            </div></li>}
            {rows.map(r => <li key={r.id}><button type="button" className="slog-row" onClick={() => onEdit(r)} data-record-row={r.id} aria-label={`${subjectLabel(r.subject)} ${r.materialName || ''} ${fmtMin(r.minutes)} を直す`}>
              <span><strong>{r.materialName || subjectLabel(r.subject)}</strong><small>{subjectLabel(r.subject)}{r.amount != null ? `・${r.amount}${r.amountUnit ?? ''}` : ''}{r.comment ? `・${r.comment}` : ''}</small></span>
              {r.postId && <span className="slog-tag">共有中</span>}
              <b>{fmtMin(r.minutes)}</b>
            </button></li>)}
          </ul>}
    </section>}
  </>;
}
