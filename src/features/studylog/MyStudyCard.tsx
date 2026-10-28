/**
 * マイページの「自分の学習ページ」（2026-10-27 第1段階・閲覧用）。
 *   名前・学年・志望校・志 ／ 今日・今週・今月・累計 ／ 連続日数・解いた大問・バッジ・対戦成績。
 *   数字は端末に保存された実際の記録から計算する（ダミーは出さない）。編集は「編集」で別の画面へ。
 */
import { useMemo } from 'react';
import { BookOpen, Flame, GraduationCap, Medal, Pencil, Plus, School, Swords } from 'lucide-react';
import { auth } from '../../firebase';
import { BADGES } from '../../battle/core/growth';
import { useGrowthProgress } from '../../hooks/useGrowthProgress';
import { readSolvedMap } from '../../utils/progress';
import { readStudyTime } from '../../utils/studyTime';
import { profileKey } from '../../utils/userStorageKeys';
import { safeLocalStorage } from '../../utils/safeLocalStorage';
import { normalizeGrade } from '../../utils/publicProfileCore';
import { currentStreak, summarize } from './manualLogCore';
import { useManualLog } from './manualLogStore';
import { fmtSec } from './ui';
import './studylog.css';

function readProfile(uid: string) {
  try {
    const p = JSON.parse(safeLocalStorage()?.getItem(profileKey(uid)) || '{}');
    const s = (v: unknown) => (typeof v === 'string' ? v.trim() : '');
    return { name: s(p.name), grade: normalizeGrade(s(p.grade)), school: s(p.targetSchool), motto: s(p.motto) };
  } catch { return { name: '', grade: '', school: '', motto: '' }; }
}

export function MyStudyCard({ onRecord, onLog, onEdit }: { onRecord: () => void; onLog: () => void; onEdit: () => void }) {
  const [store, uid] = useManualLog();
  const { progress } = useGrowthProgress();
  const profile = useMemo(() => readProfile(uid), [uid]);
  const sum = useMemo(() => summarize(store, readStudyTime(uid)), [store, uid]);
  const streak = currentStreak(sum.activeDays);
  const solved = useMemo(() => Object.keys(readSolvedMap(uid)).length, [uid]);
  const badges = progress ? BADGES.filter(b => b.id in progress.badges).length : null;
  const matches = progress?.matches ?? 0;
  const winRate = matches > 0 ? Math.round(((progress?.wins ?? 0) / matches) * 100) : null;
  const name = profile.name || auth.currentUser?.displayName || (auth.currentUser ? 'なまえ未設定' : 'ゲスト');
  return (
    <section className="mt-card mystudy" aria-label="自分の学習ページ" data-my-study>
      <div className="mystudy-head">
        <div>
          <h2>{name}</h2>
          {(profile.grade || profile.school) && <p>
            {profile.grade && <span><GraduationCap size={14} aria-hidden="true" />{profile.grade}</span>}
            {profile.school && <span><School size={14} aria-hidden="true" />{profile.school}</span>}
          </p>}
        </div>
        <button type="button" className="mt-btn mt-btn-secondary" onClick={onEdit} data-my-study-edit><Pencil size={15} aria-hidden="true" />編集</button>
      </div>
      {profile.motto && <p className="mystudy-motto">「{profile.motto}」</p>}
      <dl className="slog-sum" aria-label="学習時間（アプリで計測＋自分で記録）">
        <div><dt>今日</dt><dd>{fmtSec(sum.today.total)}</dd></div>
        <div><dt>今週</dt><dd>{fmtSec(sum.week.total)}</dd></div>
        <div><dt>今月</dt><dd>{fmtSec(sum.month.total)}</dd></div>
        <div><dt>累計</dt><dd>{fmtSec(sum.all.total)}</dd></div>
      </dl>
      <p className="mystudy-meta">
        <span><Flame size={14} aria-hidden="true" />連続 {streak}日</span>
        <span><BookOpen size={14} aria-hidden="true" />解いた大問 {solved}</span>
        {badges != null && <span><Medal size={14} aria-hidden="true" />バッジ {badges}/{BADGES.length}</span>}
        {progress && <span><Swords size={14} aria-hidden="true" />対戦 {matches}戦{matches > 0 ? ` ${progress.wins}勝${progress.losses}敗（勝率${winRate}%）` : ''}</span>}
      </p>
      <div className="mystudy-actions">
        <button type="button" className="mt-btn mt-btn-primary" onClick={onRecord} data-my-study-record><Plus size={16} aria-hidden="true" />学習を記録</button>
        <button type="button" className="mt-btn mt-btn-secondary" onClick={onLog} data-my-study-log>記録・集計を見る</button>
      </div>
    </section>
  );
}
