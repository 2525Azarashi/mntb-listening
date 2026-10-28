/**
 * 公開プロフィールに載せる「記録」を端末から集める（2026-10-26）。
 *   連続学習日数・解いた大問の数・称号の数・身につけている称号・とびら君の見た目。
 *   utils/publicStudyProfile.ts が battle 側に依存しないよう、ここで集めて差し込む
 *   （setPublicProfileStatsProvider）。どれも本人が「公開」にしているときだけ送られる。
 */
import { auth } from '../../firebase';
import { cachedGrowth } from '../../battle/data/growthStore';
import { equippedTitleLabel } from '../../battle/core/growth';
import { readSolvedMap } from '../../utils/progress';
import { streakKey } from '../../utils/userStorageKeys';
import { safeLocalStorage } from '../../utils/safeLocalStorage';
import { setPublicProfileStatsProvider, type PublicProfileStats } from '../../utils/publicStudyProfile';

export function collectProfileStats(): PublicProfileStats {
  const uid = auth.currentUser?.uid || 'guest';
  const streak = parseInt(safeLocalStorage()?.getItem(streakKey(uid)) || '0', 10);
  const solved = Object.keys(readSolvedMap(uid)).length;
  const growth = cachedGrowth();
  const out: PublicProfileStats = {
    streak: Number.isFinite(streak) && streak > 0 ? streak : 0,
    solved,
  };
  if (growth) {
    out.badges = Object.keys(growth.badges || {}).length;
    // 身につけていて、本当に持っている称号だけ
    out.title = equippedTitleLabel(growth) ? growth.equipped.title : '';
    out.look = {
      pose: growth.owned.includes(growth.equipped.pose) ? growth.equipped.pose : '',
      frame: growth.owned.includes(growth.equipped.frame) ? growth.equipped.frame : '',
      hat: growth.equipped.hat && growth.owned.includes(growth.equipped.hat) ? growth.equipped.hat : '',
      glasses: growth.equipped.glasses && growth.owned.includes(growth.equipped.glasses) ? growth.equipped.glasses : '',
    };
  }
  return out;
}

let installed = false;
/** アプリ起動時に1回呼ぶ */
export function installProfileStatsProvider(): void {
  if (installed) return;
  installed = true;
  setPublicProfileStatsProvider(collectProfileStats);
}
