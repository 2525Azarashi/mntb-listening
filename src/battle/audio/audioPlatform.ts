/**
 * 音の鳴らし方を端末ごとに変えるための判定（2026-10-16「Android 版で BGM が音割れする」）。
 *
 * ■ なぜ Android だけ分けるのか
 *   Android の WebView（Chrome）は、AudioContext を既定の latencyHint='interactive' で作ると
 *   出力バッファをとても小さく取る。画面の切り替え・アニメーション・React の再描画で
 *   メインスレッドが少し詰まるだけでバッファが空になり（アンダーラン）、
 *   「バチバチ・ザザッ」という音割れになる。音源ファイルの音量は原因ではない
 *   （全曲ピーク -5.9dBFS 以下・効果音と重ねても 0dBFS を超えない。ffmpeg で実測）。
 *
 *   ・Android：バッファを大きく取る 'playback' にする（BGM が主役で、数十ms の遅れは気にならない）
 *   ・Android：タイトル曲（<audio>）は Web Audio に通さず、<audio>.volume で音量を変える。
 *     Web Audio に通しているのは「iOS Safari が volume を無視する」ためで、Android には不要。
 *     通さなければ、タイトル曲はメディアプレーヤー側の大きなバッファで鳴り、音割れしない。
 *   ・iOS・PC：これまでどおり（iOS の音量対策・効果音の反応の速さを変えない）
 */
export function isAndroidAudio(): boolean {
  try {
    const ua = typeof navigator !== 'undefined' ? navigator.userAgent || '' : '';
    return /Android/i.test(ua);
  } catch {
    return false; // 判定できないときは従来どおりの鳴らし方にする
  }
}
