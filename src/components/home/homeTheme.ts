/**
 * ホームの「空」と「受験までの熱量」を決める純粋関数（2026-10-19）。
 *   - 時間帯：朝（5〜10時）・昼（10〜16時）・夕（16〜19時）・夜（19〜5時）
 *   - 共通テストまでの残り日数：90日超＝ふだん／〜90日／〜30日／〜7日／当日
 * 画面に依存しないので、テストから時刻・日数を渡して確かめられる。
 */
export type HomeSky = 'morning' | 'day' | 'evening' | 'night';
export type ExamHeat = 'calm' | 'd90' | 'd30' | 'd7' | 'today';

export function skyOf(date: Date = new Date()): HomeSky {
  const h = date.getHours();
  if (h >= 5 && h < 10) return 'morning';
  if (h >= 10 && h < 16) return 'day';
  if (h >= 16 && h < 19) return 'evening';
  return 'night';
}

export function examHeatOf(days: number): ExamHeat {
  if (days <= 0) return 'today';
  if (days <= 7) return 'd7';
  if (days <= 30) return 'd30';
  if (days <= 90) return 'd90';
  return 'calm';
}

