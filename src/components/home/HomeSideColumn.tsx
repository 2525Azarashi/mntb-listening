import { useEffect, useState } from 'react';
import { ChevronRight, Target, Trophy, Check } from 'lucide-react';
import { auth } from '../../firebase';
import { useGrowthProgress } from '../../hooks/useGrowthProgress';
import { localDateKey, missionsForDate, canClaimMission } from '../../battle/core/growth';
import { fetchMyRankingRow, ratingProgress, ratingTitle } from '../../battle/data/battleRanking';
import { logRejection } from '../../utils/reportError';
import { ExamCountdown } from './ExamCountdown';

/**
 * PC ホームの右列（2026-10-19）。幅広を活かして「動機づけ」をまとめる。
 *   1) 共通テストまでのカウントダウン（主役級）
 *   2) きょうのミッション（3つ・進み具合）
 *   3) 対戦ランク（いまのリーグと次まで）→ ランキングを見る
 * スマホでは描かない（CSS で隠す）。スマホのミッションはホームの2段目、ランキングは対戦の中。
 */
export function HomeSideColumn({ onMissions, onLeaderboard }: { onMissions?: () => void; onLeaderboard?: () => void }) {
  const { progress } = useGrowthProgress();
  const today = localDateKey();
  const missions = missionsForDate(today);
  const user = auth.currentUser;
  const [rating, setRating] = useState<number | null>(null);
  useEffect(() => {
    let alive = true;
    if (user) void fetchMyRankingRow().then(r => { if (alive && r) setRating(r.rating); }).catch(logRejection('home.fetchRanking'));
    return () => { alive = false; };
  }, [user]);
  const daily = progress && progress.daily.date === today ? progress.daily : null;
  return (
    <aside className="home-side" aria-label="本番までの日数・ミッション・ランク">
      <ExamCountdown variant="hero" />
      {onMissions && (
        <section className="home-side-card home-side-missions" aria-label="きょうのミッション">
          <h2><Target size={18} aria-hidden="true" />きょうのミッション</h2>
          <ul>
            {missions.map(m => {
              const got = Math.min(m.goal, daily?.progress[m.id] ?? 0);
              const claimed = !!daily?.claimed.includes(m.id);
              const ready = !!progress && canClaimMission(progress, m.id, today);
              return (
                <li key={m.id} data-done={claimed || undefined} data-ready={ready || undefined}>
                  <span className="home-side-mission-label">{m.label}</span>
                  <span className="home-side-mission-bar" aria-hidden="true"><i style={{ width: `${(got / m.goal) * 100}%` }} /></span>
                  <b>{claimed ? <Check size={15} aria-label="受け取り済み" /> : `${got}/${m.goal}`}</b>
                </li>
              );
            })}
          </ul>
          <button type="button" onClick={onMissions}>ミッションを開く<ChevronRight size={16} aria-hidden="true" /></button>
        </section>
      )}
      {onLeaderboard && (
        <section className="home-side-card home-side-rank" aria-label="対戦ランク">
          <h2><Trophy size={18} aria-hidden="true" />対戦ランク</h2>
          {rating !== null ? (
            <>
              <p className="home-side-rank-now"><b style={{ background: ratingTitle(rating).color }}>{ratingTitle(rating).label}</b><span>{rating.toLocaleString()} RP</span></p>
              <div className="home-side-rank-bar" role="progressbar" aria-label="次のリーグまで" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(ratingProgress(rating).ratio * 100)}>
                <i style={{ width: `${Math.round(ratingProgress(rating).ratio * 100)}%`, background: ratingTitle(rating).color }} />
              </div>
              <small>{ratingProgress(rating).remain > 0 ? `${ratingProgress(rating).next}まで あと${ratingProgress(rating).remain}` : '最高リーグ'}</small>
            </>
          ) : <p className="home-side-rank-empty">{user ? '全国対戦でランクが決まります' : 'ログインすると全国ランクに参加できます'}</p>}
          <button type="button" onClick={onLeaderboard}>ランキングを見る<ChevronRight size={16} aria-hidden="true" /></button>
        </section>
      )}
    </aside>
  );
}
