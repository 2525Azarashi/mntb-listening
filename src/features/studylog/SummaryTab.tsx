/** 学習記録ページの「集計」：今日・今週・今月・累計（アプリ計測／自分で記録を分けて）、目標、7日のグラフ、今月の教科別 */
import { Target } from 'lucide-react';
import { bySubject, dayOf, goalRatio, monthOf, type ManualLogStore, type StudySummary } from './manualLogCore';
import { Meter, fmtDay, fmtMin, fmtSec } from './ui';

const WD = ['月', '火', '水', '木', '金', '土', '日'];

export function SummaryTab({ sum, store, app, onGoal, onStudy, onReview }: {
  sum: StudySummary; store: ManualLogStore; app: { days: Record<string, number> };
  onGoal: () => void; onStudy?: () => void; onReview?: () => void;
}) {
  const today = dayOf(Date.now());
  const monthFrom = `${monthOf(today)}-01`;
  const monthApp = Object.entries(app.days).filter(([d]) => d >= monthFrom && d <= today).reduce((n, [, s]) => n + s, 0);
  const subjects = bySubject(store, monthApp, { from: monthFrom, to: today });
  const top = Math.max(1, ...subjects.map(s => s.seconds));
  const peak = Math.max(1800, ...sum.last7.map(d => d.app + d.self));
  const dGoal = goalRatio(sum.today.total, sum.goals.dailyMinutes);
  const wGoal = goalRatio(sum.week.total, sum.goals.weeklyMinutes);
  return <>
    <dl className="slog-sum" data-slog-summary>
      <div><dt>今日</dt><dd>{fmtSec(sum.today.total)}</dd></div>
      <div><dt>今週</dt><dd>{fmtSec(sum.week.total)}</dd></div>
      <div><dt>今月</dt><dd>{fmtSec(sum.month.total)}</dd></div>
    </dl>
    <p className="slog-note slog-total" data-slog-total>累計 <b>{fmtSec(sum.all.total)}</b>　<span className="slog-tag" data-tone="app"><i aria-hidden="true" />アプリで計測 {fmtSec(sum.all.app)}</span> <span className="slog-tag" data-tone="self"><i aria-hidden="true" />自分で記録 {fmtSec(sum.all.self)}</span></p>
    <div className="slog-goalrow">
      {dGoal != null || wGoal != null ? <span>
        {dGoal != null && <>今日 {fmtSec(sum.today.total)} / {fmtMin(sum.goals.dailyMinutes!)}{dGoal >= 1 ? '　達成！' : ''}<Meter ratio={dGoal} label="今日の目標の進み具合" /></>}
        {wGoal != null && <>今週 {fmtSec(sum.week.total)} / {fmtMin(sum.goals.weeklyMinutes!)}{wGoal >= 1 ? '　達成！' : ''}<Meter ratio={wGoal} label="今週の目標の進み具合" /></>}
      </span> : <span>目標を決めると、ここに進み具合が出ます。</span>}
      <button type="button" className="mt-btn mt-btn-secondary" onClick={onGoal} data-slog-goal><Target size={16} aria-hidden="true" />目標</button>
    </div>
    <ol className="slog-chart" aria-label="この7日間の学習時間" data-slog-chart>
      {sum.last7.map(d => <li key={d.day} aria-label={`${fmtDay(d.day, true)} アプリ ${fmtSec(d.app)}・自分で記録 ${fmtSec(d.self)}`}>
        <span className="bar" style={{ height: `${Math.max(4, Math.round(((d.app + d.self) / peak) * 100))}%` }}>
          {d.app > 0 && <i data-k="app" style={{ flex: d.app }} />}{d.self > 0 && <i data-k="self" style={{ flex: d.self }} />}
        </span>
        <small>{d.day === today ? '今日' : WD[(new Date(`${d.day}T12:00:00`).getDay() + 6) % 7]}</small>
      </li>)}
    </ol>
    <section className="slog-day mt-card" aria-label="今月の教科別">
      <header><h4>今月の教科別</h4>
        {onStudy && <button type="button" className="mt-btn mt-btn-secondary" onClick={onStudy} data-slog-study>演習</button>}
        {onReview && <button type="button" className="mt-btn mt-btn-secondary" onClick={onReview} data-slog-review>復習</button>}
      </header>
      <div className="slog-scroll" tabIndex={0} aria-label="教科別の学習時間">
        {subjects.length === 0 ? <p className="slog-note">今月の記録はまだありません。</p>
          : <ul className="slog-subjects">{subjects.map(s => <li key={s.key}><span>{s.label}</span><Meter ratio={s.seconds / top} kind={s.key === 'app' ? 'app' : 'self'} label={`${s.label} ${fmtSec(s.seconds)}`} /><b>{fmtSec(s.seconds)}</b></li>)}</ul>}
        <p className="slog-note">「マナトビ（アプリ内）」は演習・解説の画面で計った時間です。教科ごとの時間は自分で記録した分だけです。</p>
      </div>
    </section>
  </>;
}
