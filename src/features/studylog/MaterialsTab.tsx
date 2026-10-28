/** 学習記録ページの「教材」：自分の教材の一覧（検索・教科で絞る）と教材ごとの時間・目標 */
import { useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { STUDY_SUBJECTS, byMaterial, goalRatio, liveMaterials, subjectLabel, type ManualLogStore, type Material } from './manualLogCore';
import { Meter, fmtDay, fmtSec } from './ui';

export function MaterialsTab({ store, onOpen, onNew, onAdopt, onRecord }: {
  store: ManualLogStore; onOpen: (m: Material) => void; onNew: () => void;
  onAdopt: (name: string, subject: string) => void; onRecord: (materialId: string) => void;
}) {
  const [q, setQ] = useState('');
  const [subject, setSubject] = useState('');
  const mats = new Map(liveMaterials(store).map(m => [m.id, m]));
  const list = byMaterial(store).filter(s => (!subject || s.subject === subject) && (!q.trim() || s.label.includes(q.trim())));
  return <>
    <div className="slog-filter">
      <label className="slog-search"><span className="sr-only">教材を検索</span>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="教材名で検索" data-material-search />
        <Search size={16} aria-hidden="true" />
      </label>
      <label className="slog-subject-filter"><span className="sr-only">教科で絞る</span>
        <select value={subject} onChange={e => setSubject(e.target.value)} data-material-filter>
          <option value="">全教科</option>{STUDY_SUBJECTS.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
        </select>
      </label>
      <button type="button" className="mt-btn mt-btn-secondary" onClick={onNew} data-material-new><Plus size={16} aria-hidden="true" />登録</button>
    </div>
    <div className="slog-scroll" tabIndex={0} aria-label="教材の一覧" data-material-list>
      {list.length === 0
        ? <div className="slog-empty"><p>{q || subject ? '当てはまる教材がありません。' : '参考書・問題集・授業などを登録すると、記録のときに選べて、教材ごとの時間が分かります。'}</p>
            {!q && !subject && <button type="button" className="mt-btn mt-btn-primary" onClick={onNew}>教材を登録する</button>}</div>
        : <ul className="slog-rows">{list.map(s => {
            const mat = s.materialId ? mats.get(s.materialId) : undefined;
            const ratio = goalRatio(s.seconds, s.goalMinutes);
            return <li key={s.key}><div className="slog-row" data-material-row={s.materialId || s.label}>
              <span>
                <strong>{s.label}</strong>
                <small>{subjectLabel(s.subject)}{mat ? `・${mat.type}` : '・未登録'}{s.lastDay ? `・最後 ${fmtDay(s.lastDay, true)}` : '・まだ記録なし'}{ratio != null ? `・目標の${Math.round(ratio * 100)}%` : ''}</small>
                {ratio != null && <Meter ratio={ratio} label={`${s.label}の目標の進み具合`} />}
              </span>
              <b>{fmtSec(s.seconds)}</b>
              <span className="slog-row-actions">
                {mat ? <>
                  <button type="button" className="mt-btn mt-btn-secondary" onClick={() => onRecord(mat.id)} aria-label={`${s.label}で記録`}><Plus size={16} aria-hidden="true" /></button>
                  <button type="button" className="mt-btn mt-btn-secondary" onClick={() => onOpen(mat)} aria-label={`${s.label}の詳細`}>詳細</button>
                </> : s.label !== '教材なし' && <button type="button" className="mt-btn mt-btn-secondary" onClick={() => onAdopt(s.label, s.subject)} aria-label={`${s.label}を教材に登録`}>登録</button>}
              </span>
            </div></li>;
          })}</ul>}
    </div>
  </>;
}
