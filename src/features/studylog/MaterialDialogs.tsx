/**
 * 教材の登録・編集・削除の窓と、学習目標の窓（2026-10-27 第3段階）。
 *   教材を消しても過去の記録は消えない（記録は教材名を持っている）。
 */
import { useMemo, useState } from 'react';
import {
  MATERIAL_ISSUE_TEXT, MATERIAL_NAME_MAX, MATERIAL_TYPES, MEMO_MAX, STUDY_SUBJECTS, byMaterial, deleteMaterial, goalRatio,
  linkRecordsToMaterial, setGoals, upsertMaterial, validateMaterial, type Material,
} from './manualLogCore';
import { readManualLog, updateManualLog } from './manualLogStore';
import { Meter, SlogDialog, fmtSec } from './ui';

export function MaterialDialog({ material, prefill, onClose, onSaved, onRecord }: {
  material?: Material; prefill?: { name: string; subject: string };
  onClose: () => void; onSaved?: (msg: string) => void; onRecord?: (materialId: string) => void;
}) {
  const store = useMemo(() => readManualLog(), []);
  const stat = material ? byMaterial(store).find(s => s.materialId === material.id) : undefined;
  const [name, setName] = useState(material?.name ?? prefill?.name ?? '');
  const [subject, setSubject] = useState(material?.subject ?? prefill?.subject ?? '');
  const [type, setType] = useState(material?.type ?? '参考書');
  const [goalHours, setGoalHours] = useState(material?.goalMinutes ? String(Math.round((material.goalMinutes / 60) * 10) / 10) : '');
  const [memo, setMemo] = useState(material?.memo ?? '');
  const [tried, setTried] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [error, setError] = useState('');
  const goalMinutes = goalHours.trim() === '' ? null : Math.round(Number(goalHours) * 60);
  const input = { name, subject, type, goalMinutes, memo };
  const issue = validateMaterial(input, store, material?.id);

  const save = () => {
    setTried(true);
    if (issue) return;
    try {
      updateManualLog(s => {
        const r = upsertMaterial(s, input, Date.now(), material?.id);
        // 名前だけで記録していた分を、新しく登録した教材にまとめる
        return material ? r.store : linkRecordsToMaterial(r.store, r.material.id);
      });
      onSaved?.(material ? '教材を保存しました' : '教材を登録しました');
      onClose();
    } catch { setError('保存できませんでした（端末の空き容量が足りない可能性があります）。'); }
  };
  const remove = () => {
    if (!material) return;
    try { updateManualLog(s => deleteMaterial(s, material.id)); onSaved?.('教材を削除しました（過去の記録は残っています）'); onClose(); }
    catch { setError('削除できませんでした。'); }
  };

  return (
    <SlogDialog title={material ? '教材' : '教材を登録'} onClose={onClose} data="material">
      <form className="slog-form" onSubmit={e => { e.preventDefault(); save(); }} noValidate>
        {stat && <div className="slog-goalrow">
          <span>
            {stat.goalMinutes ? `目標 ${fmtSec(stat.goalMinutes * 60)} のうち ${fmtSec(stat.seconds)}（${Math.round((goalRatio(stat.seconds, stat.goalMinutes) ?? 0) * 100)}%）` : `これまで ${fmtSec(stat.seconds)}・${stat.count}回`}
            {stat.goalMinutes ? <Meter ratio={goalRatio(stat.seconds, stat.goalMinutes) ?? 0} label={`${material?.name}の目標の進み具合`} /> : null}
          </span>
          {onRecord && <button type="button" className="mt-btn mt-btn-secondary" onClick={() => { onClose(); onRecord(material!.id); }} data-material-record>この教材で記録</button>}
        </div>}
        <label className="f"><span>教材名</span>
          <input value={name} maxLength={MATERIAL_NAME_MAX} onChange={e => setName(e.target.value)} placeholder="例 青チャート数学IA" aria-invalid={(tried && (issue === 'name' || issue === 'name_long' || issue === 'duplicate')) || undefined} data-material-name />
        </label>
        <div className="row">
          <label className="f"><span>教科</span>
            <select value={subject} onChange={e => setSubject(e.target.value)} aria-invalid={(tried && issue === 'subject') || undefined} data-material-subject>
              <option value="">選ぶ…</option>
              {STUDY_SUBJECTS.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
            </select>
          </label>
          <label className="f"><span>種類</span>
            <select value={type} onChange={e => setType(e.target.value)}>{MATERIAL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}</select>
          </label>
        </div>
        <div className="row">
          <label className="f"><span>目標時間（任意・時間）</span>
            <input type="number" inputMode="decimal" min={0.1} max={1666} step={0.5} value={goalHours} onChange={e => setGoalHours(e.target.value)} placeholder="例 30" aria-invalid={(tried && issue === 'goal') || undefined} />
          </label>
          <label className="f"><span>メモ（任意）</span>
            <input value={memo} maxLength={MEMO_MAX} onChange={e => setMemo(e.target.value)} placeholder="例 1日2題" aria-invalid={(tried && issue === 'memo') || undefined} />
          </label>
        </div>
        <p className={tried && issue ? 'slog-error' : 'slog-note'} role={tried && issue ? 'alert' : undefined}>
          {tried && issue ? MATERIAL_ISSUE_TEXT[issue] : '教材は自分だけに見えます。消しても、これまでの記録は残ります。'}
        </p>
        {error && <p className="slog-error" role="alert">{error}</p>}
        <div className="slog-actions">
          {material && (confirmDelete
            ? <button type="button" className="mt-btn mt-btn-secondary" data-danger onClick={remove} data-material-delete-confirm>本当に削除</button>
            : <button type="button" className="mt-btn mt-btn-secondary" data-danger onClick={() => setConfirmDelete(true)} data-material-delete>削除</button>)}
          <button type="submit" className="mt-btn mt-btn-primary" data-material-save>{material ? '保存' : '登録する'}</button>
        </div>
      </form>
    </SlogDialog>
  );
}

const DAILY_CHIPS = [30, 60, 90, 120, 180];
export function GoalDialog({ onClose, onSaved }: { onClose: () => void; onSaved?: (msg: string) => void }) {
  const goals = useMemo(() => readManualLog().goals, []);
  const [daily, setDaily] = useState(goals.dailyMinutes ? String(goals.dailyMinutes) : '');
  const [weekly, setWeekly] = useState(goals.weeklyMinutes ? String(Math.round((goals.weeklyMinutes / 60) * 10) / 10) : '');
  const [error, setError] = useState('');
  const d = daily.trim() === '' ? null : Number(daily);
  const w = weekly.trim() === '' ? null : Math.round(Number(weekly) * 60);
  const bad = (d != null && !(d >= 1 && d <= 1440)) || (w != null && !(w >= 1 && w <= 10080));
  const save = () => {
    if (bad) { setError('1日は1〜1440分、1週間は168時間までで入れてください。'); return; }
    try { updateManualLog(s => setGoals(s, { dailyMinutes: d, weeklyMinutes: w })); onSaved?.('目標を保存しました'); onClose(); }
    catch { setError('保存できませんでした。'); }
  };
  return (
    <SlogDialog title="学習の目標" onClose={onClose} data="goal">
      <form className="slog-form" onSubmit={e => { e.preventDefault(); save(); }} noValidate>
        <label className="f"><span>1日の目標（分・空にすると目標なし）</span>
          <input type="number" inputMode="numeric" min={1} max={1440} value={daily} onChange={e => setDaily(e.target.value)} placeholder="例 90" data-goal-daily />
        </label>
        <div className="slog-chips" role="group" aria-label="1日の目標をえらぶ">
          {DAILY_CHIPS.map(m => <button type="button" key={m} aria-pressed={Number(daily) === m} onClick={() => setDaily(String(m))}>{fmtSec(m * 60)}</button>)}
        </div>
        <label className="f"><span>1週間の目標（時間・任意）</span>
          <input type="number" inputMode="decimal" min={0.5} max={168} step={0.5} value={weekly} onChange={e => setWeekly(e.target.value)} placeholder="例 10" data-goal-weekly />
        </label>
        <p className={error ? 'slog-error' : 'slog-note'} role={error ? 'alert' : undefined}>{error || 'アプリで計った時間と自分で記録した時間の合計で数えます。届かない日があっても大丈夫です。'}</p>
        <div className="slog-actions"><button type="submit" className="mt-btn mt-btn-primary" data-goal-save>保存</button></div>
      </form>
    </SlogDialog>
  );
}
