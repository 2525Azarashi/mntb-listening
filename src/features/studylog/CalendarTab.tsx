/**
 * マイページの「記録」タブ＝カレンダーだけ（2026-10-28 作り直し・A1②）。
 *   日付を押すと、その日の勉強記録（合計・アプリで計った時間・自分で記録した分）が下に出る。
 *   色の濃さ＝その日の勉強時間。記録を書くのはマイページの「学習を記録」1か所だけ（ここには置かない）。
 *   自分で記録した行を押すと、直す・消すの窓が開く。
 */
import { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { addMonths, dayOf, monthGrid, monthOf, subjectLabel, type ManualLogStore, type ManualRecord } from './manualLogCore';
import { fmtDay, fmtMin, fmtSec } from './ui';

const WD = ['月', '火', '水', '木', '金', '土', '日'];
const level = (sec: number) => (sec <= 0 ? 0 : sec < 1800 ? 1 : sec < 3600 ? 2 : sec < 7200 ? 3 : 4);

export function CalendarTab({ store, app, onEdit }: {
  store: ManualLogStore; app: { days: Record<string, number> }; onEdit: (r: ManualRecord) => void;
}) {
  const today = dayOf(Date.now());
  const [month, setMonth] = useState(monthOf(today));
  const [picked, setPicked] = useState(today);
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
  const rows = (byDay.get(picked) ?? []).slice().sort((a, b) => b.createdAt - a.createdAt);
  const move = (n: number) => { const m = addMonths(month, n); setMonth(m); setPicked(m === monthOf(today) ? today : `${m}-01`); };
  return <>
    <div className="slog-month">
      <button type="button" onClick={() => move(-1)} disabled={month <= minMonth} aria-label="前の月"><ChevronLeft size={20} aria-hidden="true" /></button>
      <h3 aria-live="polite">{y}年{mo}月<small>　勉強した日 {studied}日</small></h3>
      <button type="button" onClick={() => move(1)} disabled={month >= monthOf(today)} aria-label="次の月"><ChevronRight size={20} aria-hidden="true" /></button>
    </div>
    <ol className="slog-cal" aria-label={`${y}年${mo}月の勉強カレンダー（日付を押すとその日の記録）`} data-slog-calendar>
      {WD.map(w => <li key={w} aria-hidden="true"><span>{w}</span></li>)}
      {cells.map((d, i) => d
        ? <li key={d}><button type="button" className="slog-cell" disabled={d > today} aria-pressed={d === picked}
            data-lv={level(total(d)) || undefined} data-today={d === today || undefined} data-self={byDay.has(d) || undefined} data-future={d > today || undefined} data-day={d}
            onClick={() => setPicked(d)}
            aria-label={`${fmtDay(d)} ${total(d) > 0 ? `勉強 ${fmtSec(total(d))}` : '記録なし'}`}>{Number(d.slice(8))}</button></li>
        : <li key={`x${i}`} aria-hidden="true" />)}
    </ol>
    <p className="slog-legend" aria-hidden="true"><span>色が濃いほど長く勉強</span><span><i />自分で記録した日</span><span className="slog-legend-today">今日</span></p>
    <section className="slog-scroll slog-picked" tabIndex={0} aria-live="polite" aria-label={`${fmtDay(picked)}の勉強記録`} data-slog-day={picked}>
      <h4>{fmtDay(picked)}<small>合計 {fmtSec(total(picked))}</small></h4>
      {total(picked) === 0
        ? <p className="slog-note">この日の記録はありません。</p>
        : <ul className="slog-rows">
            {(app.days[picked] ?? 0) > 0 && <li><div className="slog-row" data-app-row>
              <span><strong>マナトビ（アプリ内）</strong><small>演習・解説の画面で計った時間</small></span><b>{fmtSec(app.days[picked])}</b>
            </div></li>}
            {rows.map(r => <li key={r.id}><button type="button" className="slog-row" onClick={() => onEdit(r)} data-record-row={r.id} aria-label={`${subjectLabel(r.subject)} ${r.materialName || ''} ${fmtMin(r.minutes)} を直す`}>
              <span><strong>{r.materialName || subjectLabel(r.subject)}</strong><small>{subjectLabel(r.subject)}{r.amount != null ? `・${r.amount}${r.amountUnit ?? ''}` : ''}{r.comment ? `・${r.comment}` : ''}</small></span>
              {r.postId && <span className="slog-tag">共有中</span>}
              <b>{fmtMin(r.minutes)}</b>
            </button></li>)}
          </ul>}
    </section>
  </>;
}
