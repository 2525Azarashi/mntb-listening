/**
 * ピックアップの「中身を少し見る」ダイアログ（2026-10-27）。
 *   LR（共通テスト予想問題）と厳選UR の PDF から、2ページぶんの上半分だけを見せる（下はぼかしで消してある）。
 *   画像は scripts/gacha-prints/build-previews.py が作る（public/prints/previews）。
 *   音声つきのLR（いまはリスニング第1回）は、最初の1問だけ試しに聞ける。
 */
import { useEffect, useRef, useState, type RefObject } from 'react';
import { Pause, Play } from 'lucide-react';
import { gachaRarityOf, printOf, type GrowthProgress, type ItemDef } from '../../battle/core/growth';
import { GACHA_PREVIEWS } from '../../data/gachaPreviews.generated';
import { kyotsuAudioOf } from '../../data/kyotsuMockAudio';
import { RarityTag } from '../GachaParts';

export function hasGachaPreview(id: string): boolean {
  return (GACHA_PREVIEWS[id]?.length ?? 0) > 0;
}

export function GachaPreviewModal({ dialogRef, item, progress }: {
  dialogRef: RefObject<HTMLDialogElement | null>;
  item: ItemDef | null;
  progress: GrowthProgress | null;
}) {
  const print = item ? printOf(item.id) : undefined;
  const pages = item ? GACHA_PREVIEWS[item.id] ?? [] : [];
  const sample = item ? kyotsuAudioOf(item.id)[0] : undefined;
  const audio = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const owned = !!item && !!progress?.owned.includes(item.id);

  // 別のアイテムに切り替えたら・閉じたら止める
  useEffect(() => {
    const stop = () => { audio.current?.pause(); setPlaying(false); };
    stop();
    const d = dialogRef.current;
    d?.addEventListener('close', stop);
    return () => d?.removeEventListener('close', stop);
  }, [item?.id, dialogRef]);

  return (
    <dialog ref={dialogRef} className="game-details-dialog mt-dialog gacha-peek-dialog" aria-labelledby="gacha-peek-title" data-gacha-peek>
      <header>
        <h2 id="gacha-peek-title">中身を少し見る</h2>
        <button type="button" autoFocus onClick={() => dialogRef.current?.close()}>閉じる</button>
      </header>
      {item && print && (
        <div className="game-details-body gacha-peek-body">
          <p className="gacha-peek-name">
            <RarityTag rarity={gachaRarityOf(item)} /> <strong>{item.label}</strong>
          </p>
          <p className="gacha-peek-meta">
            {print.category} · 全{print.pages}ページ{sample ? ' · 音声つき' : ''}{owned ? ' · 所持済み（マイPDFで保存できます）' : ''}
          </p>
          <ul className="gacha-peek-pages" aria-label="ページの一部">
            {pages.map((src) => (
              <li key={src}>
                <img src={src} alt={`${print.label} の一部（${src.match(/_p(\d+)\.webp$/)?.[1] ?? ''}ページ目の上半分）`} loading="lazy" width={360} height={264} />
              </li>
            ))}
          </ul>
          {sample && (
            <div className="gacha-peek-audio">
              <audio ref={audio} src={sample.file} preload="none" onEnded={() => setPlaying(false)} />
              <button
                type="button"
                aria-pressed={playing}
                onClick={() => {
                  const a = audio.current;
                  if (!a) return;
                  if (playing) { a.pause(); setPlaying(false); return; }
                  void a.play().then(() => setPlaying(true)).catch(() => setPlaying(false));
                }}
              >
                {playing ? <Pause size={18} aria-hidden /> : <Play size={18} aria-hidden />}
                {playing ? '止める' : `音声を試し聞き（${sample.label}）`}
              </button>
            </div>
          )}
          <p className="gacha-peek-note">見られるのは一部の上半分だけ。全部はガチャで当てると「マイPDF」で保存できます。</p>
        </div>
      )}
    </dialog>
  );
}
