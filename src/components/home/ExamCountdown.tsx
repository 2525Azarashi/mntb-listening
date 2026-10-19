import { useMemo } from 'react';
import { getDaysUntilExam, getDaysUntilSecondExam, EXAM_DATE_LABEL, SECOND_EXAM_DATE_LABEL } from '../../utils/examCountdown';
import { examHeatOf } from './homeTheme';
import { Odometer } from './Odometer';

/**
 * 共通テストまでのカウントダウン（2026-10-19）。
 *   chip … スマホのヘッダーに置く小さな札（「共テ 89日」）
 *   hero … PC の右列の主役。数字はオドメーター、下に残り日数ぶんの点（90個まで）。今日の点だけ点滅
 * 残り 90／30／7日・当日で data-heat が変わり、色と演出の強さが上がる（CSS）。
 */
export function ExamCountdown({ variant }: { variant: 'chip' | 'hero' }) {
  const days = useMemo(() => getDaysUntilExam(), []);
  const second = useMemo(() => getDaysUntilSecondExam(), []);
  const heat = examHeatOf(days);
  if (variant === 'chip') {
    return (
      <p className="exam-chip" data-heat={heat} title={`共通テスト ${EXAM_DATE_LABEL}`} aria-label={`共通テストまで${days}日`} data-home-countdown>
        <span aria-hidden="true">共テ</span><b aria-hidden="true">{days}</b><span aria-hidden="true">日</span>
      </p>
    );
  }
  const dots = Math.min(90, days);
  return (
    <section className="exam-hero" data-heat={heat} aria-label="本番までの日数" data-home-countdown>
      <p className="exam-hero-kicker">共通テストまで</p>
      <p className="exam-hero-days" title={EXAM_DATE_LABEL}>
        {days > 0 ? <><Odometer value={days} from={days + 1} className="exam-hero-num" /><span>日</span></> : <strong className="exam-hero-num">当日</strong>}
      </p>
      <p className="exam-hero-date">{EXAM_DATE_LABEL}</p>
      {dots > 0 && (
        <div className="exam-hero-dots" role="img" aria-label={`残り${days}日。点1つが1日`}>
          {Array.from({ length: dots }, (_, i) => <i key={i} data-today={i === 0 || undefined} />)}
        </div>
      )}
      <p className="exam-hero-second" title={`2次試験（前期） ${SECOND_EXAM_DATE_LABEL}`}>2次（前期）まで <b>{second}</b>日</p>
    </section>
  );
}
