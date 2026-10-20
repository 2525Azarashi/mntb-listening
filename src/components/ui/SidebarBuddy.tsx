import { useEffect, useState } from 'react';
import { auth } from '../../firebase';
import { useGrowthProgress } from '../../hooks/useGrowthProgress';
import { equippedPoseSrc, levelOf } from '../../battle/core/growth';
import { streakKey } from '../../utils/userStorageKeys';
import { safeLocalStorage } from '../../utils/safeLocalStorage';
import { streakDoors } from '../../data/tobiraMood';

/**
 * PC サイドバーの下半分（2026-10-19 ご要望「サイドバー下半分が空」）。
 *   とびら君の小窓＋レベル＋連続学習（扉7枚）。画面が切り替わるたびに連続日数を読み直す。
 *   スマホの下ナビでは表示しない（nav.css）。
 */
export function SidebarBuddy({ screen, onOpen }: { screen: string; onOpen?: () => void }) {
  const { progress } = useGrowthProgress();
  const [streak, setStreak] = useState(0);
  useEffect(() => {
    const uid = auth.currentUser?.uid || 'guest';
    setStreak(parseInt(safeLocalStorage()?.getItem(streakKey(uid)) || '0', 10) || 0);
  }, [screen]);
  if (!progress) return null;
  const doors = streakDoors(streak);
  return (
    <button type="button" className="sidebar-buddy" onClick={onOpen} aria-label={`マイページを開く（レベル${levelOf(progress.xp).level}・連続学習${streak}日）`}>
      <span className="sidebar-buddy-window" aria-hidden="true"><img src={equippedPoseSrc(progress)} alt="" draggable={false} /></span>
      <span className="sidebar-buddy-text">
        <b>Lv.{levelOf(progress.xp).level}</b>
        <span>連続 <strong>{streak}</strong>日</span>
      </span>
      <span className="sidebar-buddy-doors" aria-hidden="true">{Array.from({ length: 7 }, (_, i) => <i key={i} data-open={i < doors.doors || undefined} />)}</span>
    </button>
  );
}
