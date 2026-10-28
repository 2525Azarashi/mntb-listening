/**
 * LR リスニング予想問題の音声プレーヤー（マイPDF で、持っている人だけ）。2026-10-27
 *   問題を選んで再生。トラックの中身は src/data/kyotsuMockAudio.ts。
 */
import { useRef, useState } from 'react';
import { Headphones } from 'lucide-react';
import { kyotsuAudioOf } from '../data/kyotsuMockAudio';

export function KyotsuAudioPlayer({ printId }: { printId: string }) {
  const tracks = kyotsuAudioOf(printId);
  const [index, setIndex] = useState(0);
  const audio = useRef<HTMLAudioElement>(null);
  if (!tracks.length) return null;
  const track = tracks[index];
  return (
    <details className="kyotsu-audio" data-kyotsu-audio={printId}>
      <summary><Headphones size={16} aria-hidden /> 音声を聞く（{tracks.length}トラック）</summary>
      <label className="sr-only" htmlFor={`kyotsu-audio-${printId}`}>問題を選ぶ</label>
      <select
        id={`kyotsu-audio-${printId}`}
        value={index}
        onChange={(e) => {
          const wasPlaying = !!audio.current && !audio.current.paused;
          setIndex(Number(e.target.value));
          if (wasPlaying) requestAnimationFrame(() => void audio.current?.play().catch(() => undefined));
        }}
      >
        {tracks.map((t, i) => (
          <option key={t.file} value={i}>{t.label}{t.twice ? '（2回読み）' : ''}</option>
        ))}
      </select>
      <audio ref={audio} controls preload="none" src={track.file} onEnded={() => { if (index < tracks.length - 1) setIndex(index + 1); }} />
    </details>
  );
}
