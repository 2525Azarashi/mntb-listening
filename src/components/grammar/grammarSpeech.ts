/**
 * 英文法コンパクト解説での音声再生ユーティリティ
 *   1. `audioUrl`（`/grammar_audio/<subId>.mp3`）があれば HTMLAudioElement で再生
 *   2. 無ければ Web Speech API（`en-US`）にフォールバック
 */
import { logRejection } from '../../utils/reportError';

let activeAudio: HTMLAudioElement | null = null;

export function stopGrammarSpeech(): void {
  if (activeAudio) {
    try {
      activeAudio.pause();
      activeAudio.currentTime = 0;
    } catch {
      // 破棄済みの Audio 要素の停止エラーは無視（意図して捨てている）
    }
    activeAudio = null;
  }
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    try {
      window.speechSynthesis.cancel();
    } catch {
      // Web Speech API 非対応環境の cancel 例外は無視（意図して捨てている）
    }
  }
}

export function isGrammarSpeechAvailable(audioUrl?: string): boolean {
  if (audioUrl) return true;
  return typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';
}

export function playGrammarSentenceAudio({
  audioUrl,
  text,
  rate = 1,
  onStart,
  onEnd,
}: {
  audioUrl?: string;
  text: string;
  rate?: number;
  onStart?: () => void;
  onEnd?: () => void;
}): void {
  stopGrammarSpeech();

  if (audioUrl && typeof Audio !== 'undefined') {
    const audio = new Audio(audioUrl);
    audio.playbackRate = rate;
    activeAudio = audio;
    const finish = () => {
      if (activeAudio === audio) activeAudio = null;
      onEnd?.();
    };
    audio.addEventListener('ended', finish, { once: true });
    audio.addEventListener('error', finish, { once: true });
    onStart?.();
    void audio.play().catch((err) => {
      logRejection('grammarAudio.play')(err);
      finish();
    });
    return;
  }

  if (typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined') {
    const clean = String(text || '').replace(/\s+/g, ' ').trim();
    if (!clean) return;
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'en-US';
    utter.rate = rate;
    utter.onstart = () => onStart?.();
    utter.onend = () => onEnd?.();
    utter.onerror = () => onEnd?.();
    try {
      window.speechSynthesis.speak(utter);
    } catch {
      onEnd?.(); // Web Speech API 発話失敗時は状態だけ戻す（意図して捨てている）
    }
  }
}
