import React, { useEffect, useState } from 'react';

/**
 * 数字が縦に回って止まるカウンター（オドメーター）。2026-10-19。
 *   ・1桁ずつ 0〜9 の帯を translateY で動かす（transform だけなので軽い）
 *   ・読み上げは全体の数字1回だけ（aria-label）。帯は aria-hidden
 *   ・動きを減らす設定では最初から止まった完成形（CSS 側で transition を切る）
 *   ・from を渡すと「前日の数字 → 今日の数字」と1つだけ回る（日替わりの演出）
 */
export function Odometer({ value, from, className = '', delay = 250 }: { value: number; from?: number; className?: string; delay?: number }) {
  const target = Math.max(0, Math.floor(value));
  const [shown, setShown] = useState(from ?? target);
  useEffect(() => {
    if (shown === target) return;
    const t = window.setTimeout(() => setShown(target), delay);
    return () => window.clearTimeout(t);
  }, [target, delay, shown]);
  const digits = String(shown).split('');
  const width = Math.max(String(target).length, digits.length);
  const padded = digits.join('').padStart(width, ' ').split('');
  return (
    <span className={`odo ${className}`} aria-label={String(target)} role="img">
      {padded.map((d, i) => (
        <span key={i} className="odo-digit" aria-hidden="true" data-blank={d === ' ' || undefined}>
          <span className="odo-strip" style={{ transform: `translateY(-${d === ' ' ? 0 : Number(d) * 10}%)` } as React.CSSProperties}>
            {'0123456789'.split('').map(n => <span key={n}>{n}</span>)}
          </span>
        </span>
      ))}
    </span>
  );
}
