/**
 * ===================================================================
 * 学習記録ページ（マイページの「記録」タブ。2026-10-27 第2〜5段階）
 * ===================================================================
 *   カレンダー … 学習した日が分かる月のカレンダー。日を押すとその日の記録（直す・消す・その日に記録）
 *   集計       … 今日・今週・今月・累計（アプリで計測／自分で記録 を分けて）・目標・7日のグラフ・教科別
 *   教材       … 自分の教材（検索・教科で絞る）・教材ごとの時間と目標
 *   フレンド   … フレンドが共有した記録とリアクション
 * 画面全体はスクロールさせず、一覧の中だけ動かす（ランキングと同じ作り）。右上の「＋記録」はどのタブからも同じ。
 */
import { useEffect, useMemo, useState } from 'react';
import { Plus } from 'lucide-react';
import { readStudyTime } from '../../utils/studyTime';
import { summarize, type ManualRecord, type Material } from './manualLogCore';
import { useManualLog } from './manualLogStore';
import { RecordDialog, type RecordDraft } from './RecordDialog';
import { GoalDialog, MaterialDialog } from './MaterialDialogs';
import { CalendarTab } from './CalendarTab';
import { SummaryTab } from './SummaryTab';
import { MaterialsTab } from './MaterialsTab';
import { FriendFeed } from './FriendFeed';
import './studylog.css';

export type StudyLogTab = 'calendar' | 'summary' | 'materials' | 'friends';
const TABS: [StudyLogTab, string][] = [['calendar', 'カレンダー'], ['summary', '集計'], ['materials', '教材'], ['friends', 'フレンド']];

export function StudyLogPage({ initialTab = 'calendar', openNew = false, onStudy, onReview, onOpenFriends }: {
  initialTab?: StudyLogTab; openNew?: boolean; onStudy?: () => void; onReview?: () => void; onOpenFriends?: () => void;
  /** 開き直しのための key（このプロジェクトの型では props に書く必要がある） */
  key?: string;
}) {
  const [store, uid] = useManualLog();
  const [tab, setTab] = useState<StudyLogTab>(initialTab);
  const [editing, setEditing] = useState<{ record?: ManualRecord; draft?: RecordDraft } | null>(openNew ? {} : null);
  const [matDialog, setMatDialog] = useState<{ material?: Material; prefill?: { name: string; subject: string } } | null>(null);
  const [goalOpen, setGoalOpen] = useState(false);
  const [toast, setToast] = useState('');
  useEffect(() => { if (!toast) return; const t = setTimeout(() => setToast(''), 2600); return () => clearTimeout(t); }, [toast]);
  const app = useMemo(() => readStudyTime(uid), [uid, store]);
  const sum = useMemo(() => summarize(store, app), [store, app]);

  return (
    <section className="slog" aria-label="学習記録" data-study-log>
      <div className="slog-top">
        <div className="mt-tabs" role="tablist" aria-label="学習記録の表示">
          {TABS.map(([id, label]) => <button key={id} type="button" role="tab" aria-selected={tab === id} onClick={() => setTab(id)} data-slog-tab={id}>{label}</button>)}
        </div>
        <button type="button" className="mt-btn mt-btn-primary slog-add" onClick={() => setEditing({})} data-slog-add><Plus size={16} aria-hidden="true" />記録</button>
      </div>
      <div className="slog-body">
        {tab === 'calendar' && <CalendarTab store={store} app={app} onEdit={r => setEditing({ record: r })} onAdd={() => setEditing({})} />}
        {tab === 'summary' && <SummaryTab sum={sum} store={store} app={app} onGoal={() => setGoalOpen(true)} onStudy={onStudy} onReview={onReview} />}
        {tab === 'materials' && <MaterialsTab store={store} onOpen={m => setMatDialog({ material: m })} onNew={() => setMatDialog({})}
          onAdopt={(name, subject) => setMatDialog({ prefill: { name, subject } })} onRecord={materialId => setEditing({ draft: { materialId } })} />}
        {tab === 'friends' && <FriendFeed onOpenFriends={onOpenFriends} onToast={setToast} />}
      </div>
      {editing && <RecordDialog record={editing.record} draft={editing.draft} onClose={() => setEditing(null)} onSaved={setToast} />}
      {matDialog && <MaterialDialog material={matDialog.material} prefill={matDialog.prefill} onClose={() => setMatDialog(null)} onSaved={setToast}
        onRecord={materialId => setEditing({ draft: { materialId } })} />}
      {goalOpen && <GoalDialog onClose={() => setGoalOpen(false)} onSaved={setToast} />}
      {toast && <p className="mt-toast" role="status" data-slog-toast>{toast}</p>}
    </section>
  );
}
