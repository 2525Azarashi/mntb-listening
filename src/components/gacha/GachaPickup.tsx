/**
 * ガチャ画面の「ピックアップ」欄（2026-10-27）。
 *   LR（共通テスト予想問題）全種 ＋ 厳選UR のうち、ちら見せ画像があるものを横に並べる。
 *   「少し見る」で GachaPreviewModal を開く（PDF の一部の上半分だけ）。
 *   並び：LR → UR。アイテム名はデータから出す（GachaRoom にラベルを直書きしない）。
 */
import { useRef, useState } from 'react';
import { Eye, Headphones } from 'lucide-react';
import { gachaRarityOf, printOf, type GrowthProgress, type ItemDef } from '../../battle/core/growth';
import { kyotsuAudioOf } from '../../data/kyotsuMockAudio';
import { RarityTag } from '../GachaParts';
import { GachaPreviewModal, hasGachaPreview } from './GachaPreviewModal';

export function pickupItems(lr: readonly ItemDef[], featuredUr: readonly ItemDef[]): ItemDef[] {
  return [...lr, ...featuredUr].filter((i) => hasGachaPreview(i.id));
}

export function GachaPickup({ items, progress, disabled }: {
  items: readonly ItemDef[];
  progress: GrowthProgress | null;
  disabled?: boolean;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [current, setCurrent] = useState<ItemDef | null>(null);
  if (!items.length) return null;
  return (
    <section className="gacha-pickup" aria-labelledby="gacha-pickup-title" data-gacha-pickup>
      <h2 id="gacha-pickup-title" className="gacha-step">
        ピックアップ<small>LR・URの中身を少しだけ</small>
      </h2>
      <ul className="gacha-pickup-list">
        {items.map((item) => {
          const print = printOf(item.id);
          const rarity = gachaRarityOf(item);
          const owned = !!progress?.owned.includes(item.id);
          return (
            <li key={item.id} className="gacha-pickup-card" data-rarity={rarity} data-gacha-pickup-item={item.id}>
              {print && <img src={print.thumb} alt="" loading="lazy" width={44} height={62} />}
              <span className="gacha-pickup-text">
                <span className="gacha-pickup-top">
                  <RarityTag rarity={rarity} />
                  {kyotsuAudioOf(item.id).length > 0 && <Headphones size={14} aria-label="音声つき" />}
                  {owned && <em>所持</em>}
                </span>
                <strong>{item.label}</strong>
              </span>
              <button
                type="button"
                disabled={disabled}
                aria-label={`${item.label} の中身を少し見る`}
                onClick={() => { setCurrent(item); requestAnimationFrame(() => dialog.current?.showModal()); }}
              >
                <Eye size={16} aria-hidden />少し見る
              </button>
            </li>
          );
        })}
      </ul>
      <GachaPreviewModal dialogRef={dialog} item={current} progress={progress} />
    </section>
  );
}
