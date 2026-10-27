/**
 * 「ピックアップ」ダイアログ（2026-10-27）。
 *   LR（共通テスト予想問題）全10種と、厳選UR 10種の「中身を少しだけ」見せる。
 *   画像は scripts/gacha-prints/build-previews.py が作る（ページの上半分だけ・下はぼかし）。
 *   リスニングの第1回は音声の試聴（問1だけ）もできる。
 *   ガチャの画面は1画面に収める決まりなので、一覧は画面には並べず、下のボタンからこのダイアログで開く。
 */
import type { RefObject } from 'react';
import { gachaRarityOf, printOf, type GrowthProgress, type ItemDef } from '../../battle/core/growth';
import { gachaItemRate } from '../../battle/core/arenaEconomy';
import { GACHA_PREVIEWS } from '../../data/gachaPreviews.generated';
import { kyotsuAudioOf } from '../../data/kyotsuMockAudio';
import { RarityTag, pct } from '../GachaParts';

/** ピックアップに出すアイテム（LR → UR の順。画像があるものだけ） */
export function pickupItems(items: readonly ItemDef[]): ItemDef[] {
  const ids = Object.keys(GACHA_PREVIEWS);
  const list = ids.map((id) => items.find((i) => i.id === id)).filter((i): i is ItemDef => !!i);
  return [...list.filter((i) => gachaRarityOf(i) === 'LR'), ...list.filter((i) => gachaRarityOf(i) !== 'LR')];
}

export function GachaPickupModal({ dialog, items, progress }: {
  dialog: RefObject<HTMLDialogElement | null>;
  items: readonly ItemDef[];
  progress: GrowthProgress | null;
}) {
  const list = pickupItems(items);
  const groups = [
    { id: 'LR', title: 'LR 共通テスト英語 予想問題', note: 'リーディング・リスニング 各5回分。本番と同じ形式・分量のオリジナル問題。', list: list.filter((i) => gachaRarityOf(i) === 'LR') },
    { id: 'UR', title: '厳選UR 学習プリント', note: '大当たりの中から人気の10種。', list: list.filter((i) => gachaRarityOf(i) !== 'LR') },
  ];
  return (
    <dialog ref={dialog} className="game-details-dialog mt-dialog" aria-labelledby="gacha-pickup-title" data-gacha-pickup>
      <header>
        <h2 id="gacha-pickup-title">ピックアップ（中身を少し見る）</h2>
        <button type="button" autoFocus onClick={() => dialog.current?.close()}>
          閉じる
        </button>
      </header>
      <div className="game-details-body gacha-pickup">
        <p className="gacha-pickup-lead">ページの一部だけ見られます。全部は、ガチャで当てて「マイPDF」から。</p>
        {groups.map((g) => (
          <section key={g.id} className="gacha-pickup-group" aria-labelledby={`gacha-pickup-${g.id}`}>
            <h3 id={`gacha-pickup-${g.id}`}>{g.title}</h3>
            <p>{g.note}</p>
            <ul>
              {g.list.map((item) => {
                const print = printOf(item.id);
                const owned = !!progress?.owned.includes(item.id);
                const sample = kyotsuAudioOf(item.id)[0];
                return (
                  <li key={item.id}>
                    <details className="gacha-pickup-item" data-gacha-pickup-item={item.id}>
                      <summary>
                        {print && <img src={print.thumb} alt="" loading="lazy" width={40} height={56} />}
                        <span>
                          <span className="gacha-pickup-meta">
                            <RarityTag rarity={gachaRarityOf(item)} />
                            {print ? `${print.pages}ページ` : ''} · {pct(gachaItemRate(item))}%{owned ? ' · 所持済み' : ''}
                            {sample ? ' · 音声つき' : ''}
                          </span>
                          <strong>{item.label}</strong>
                        </span>
                        <em aria-hidden="true">少し見る</em>
                      </summary>
                      <div className="gacha-pickup-pages">
                        {(GACHA_PREVIEWS[item.id] ?? []).map((src) => (
                          <img key={src} src={src} alt={`${item.label} の一部（${src.match(/_p(\d+)\.webp$/)?.[1] ?? ''}ページ目の上半分）`} loading="lazy" />
                        ))}
                      </div>
                      {sample && (
                        <p className="gacha-pickup-audio">
                          <span>試聴（問1）</span>
                          <audio controls preload="none" src={sample.file} />
                        </p>
                      )}
                    </details>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
      </div>
    </dialog>
  );
}
