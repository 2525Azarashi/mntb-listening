/**
 * 学習記録ページの「カレンダー」（2026-10-27）
 *   上：その月の学習カレンダー（色の濃さ＝学習時間、点＝自分で記録した日）。見るだけの表なので押せない
 *       （押せる大きさ 44px を7列で取ると小さいスマホに収まらないため。日付は記録の窓で選ぶ）。
 *   下：その月に学習した日の一覧。日ごとの合計と、自分で記録した分（押すと直す・消す）。一覧の中だけ動く。
 */
import { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { addMonths, dayOf, monthGrid, monthOf, subjectLabel, type ManualLogStore, type ManualRecord } from './manualLogCore';
import { fmtDay, fmtMin, fmtSec } from './ui';

const WD = ['月', '火', '水', '木', '金', '土', '日'];
const level = (sec: number) => (sec <= 0 ? 0 : sec < 1800 ? 1 : sec < 3600 ? 2 : sec < 7200 ? 3 : 4);

export function CalendarTab({ store, app, onEdit, onAdd }: {
  store: ManualLogStore; app: { days: Record<string, number> }; onEdit: (r: ManualRecord) => void; onAdd: () => void;
}) {
  const today = dayOf(Date.now());
  const [month, setMonth] = useState(monthOf(today));
  const cells = monthGrid(month);
  const byDay = useMemo(() => {
    const m = new Map<string, ManualRecord[]>();
    for (const r of store.records) if (!r.deleted) m.set(r.day, [...(m.get(r.day) ?? []), r]);
    return m;
  }, [store]);
  const selfSec = (d: string) => (byDay.get(d) ?? []).reduce((n, r) => n + r.minutes * 60, 0);
  const total = (d: string) => (app.days[d] ?? 0) + selfSec(d);
  const days = cells.filter((d): d is string => !!d && d <= today && total(d) > 0).reverse();
  const [y, mo] = month.split('-').map(Number);
  const minMonth = monthOf(dayOf(Date.now() - 730 * 86_400_000));
  return <>
    <div className="slog-month">
      <button type="button" onClick={() => setMonth(addMonths(month, -1))} disabled={month <= minMonth} aria-label="前の月"><ChevronLeft size={20} aria-hidden="true" /></button>
      <h3 aria-live="polite">{y}年{mo}月<small>　学習した日 {days.length}日</small></h3>
      <button type="button" onClick={() => setMonth(addMonths(month, 1))} disabled={month >= monthOf(today)} aria-label="次の月"><ChevronRight size={20} aria-hidden="true" /></button>
    </div>
    <ol className="slog-cal" aria-label={`${y}年${mo}月の学習カレンダー`} data-slog-calendar>
      {WD.map(w => <li key={w} aria-hidden="true"><span>{w}</span></li>)}
      {cells.map((d, i) => d
        ? <li key={d} className="slog-cell" data-lv={level(total(d)) || undefined} data-today={d === today || undefined} data-self={byDay.has(d) || undefined} data-future={d > today || undefined} data-day={d}
            aria-label={`${fmtDay(d)} ${total(d) > 0 ? `学習 ${fmtSec(total(d))}` : '記録なし'}${byDay.has(d) ? '（自分で記録あり）' : ''}`}>{Number(d.slice(8))}</li>
        : <li key={`x${i}`} aria-hidden="true" />)}
    </ol>
    <p className="slog-legend" aria-hidden="true"><span>色が濃いほど長く学習</span><span><i />自分で記録した日</span><span className="slog-legend-today">今日</span></p>
    <div className="slog-scroll" tabIndex={0} aria-label={`${y}年${mo}月に学習した日`} data-slog-days>
      {days.length === 0
        ? <div className="slog-empty"><p>この月の記録はまだありません。参考書・学校の課題・塾など、アプリの外の勉強も記録できます。</p>
            {month === monthOf(today) && <button type="button" className="mt-btn mt-btn-primary" onClick={onAdd}>学習を記録する</button>}</div>
        : days.map(d => <section key={d} className="slog-dayblock" aria-label={fmtDay(d)}>
            <h4>{fmtDay(d)}<small>合計 {fmtSec(total(d))}{app.days[d] ? `（アプリ ${fmtSec(app.days[d])}）` : ''}</small></h4>
            {(byDay.get(d) ?? []).length > 0 && <ul className="slog-rows">{(byDay.get(d) ?? []).sort((a, b) => b.createdAt - a.createdAt).map(r =>
              <li key={r.id}><button type="button" className="slog-row" onClick={() => onEdit(r)} data-record-row={r.id} aria-label={`${subjectLabel(r.subject)} ${r.materialName || ''} ${fmtMin(r.minutes)} を直す`}>
                <span><strong>{r.materialName || subjectLabel(r.subject)}</strong><small>{subjectLabel(r.subject)}{r.amount != null ? `・${r.amount}${r.amountUnit ?? ''}` : ''}{r.comment ? `・${r.comment}` : ''}</small></span>
                {r.postId && <span className="slog-tag">共有中</span>}
                <b>{fmtMin(r.minutes)}</b>
              </button></li>)}</ul>}
          </section>)}
    </div>
  </>;
}
