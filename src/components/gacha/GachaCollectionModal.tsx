/**
 * 「装飾コレクション・提供割合」のダイアログ（C-06）。
 * GachaRoom.tsx から JSX をそのまま移した。2026-10-19 に提供割合の説明だけ要点ごとの形に組み直した（数字は同じ）。
 *
 * ★種類・所持状況の切り替え（collectionKind / collectionFilter）はここで持つ★
 *   どちらもこのダイアログの中でしか使わない。ダイアログは常に描画されている（開閉は showModal / close）ので、
 *   親で持っていたときと同じく、閉じて開き直しても選んだ切り替えは残る。
 */
import { useState, type RefObject } from 'react';
import {
  GACHA_DUPLICATE_REFUND_BY_RARITY,
  GACHA_RARITY_RATES,
  gachaItemRate,
} from '../../battle/core/arenaEconomy';
import { gachaRarityOf, type GachaRarity, type GrowthProgress, type ItemDef } from '../../battle/core/growth';
import { COLLECTION_KINDS, ItemArt, PrintLinks, RarityTag, pct, type CollectionKind } from '../GachaParts';

export function GachaCollectionModal({ oddsDialog, items, tiers, progress }: {
  oddsDialog: RefObject<HTMLDialogElement | null>;
  items: ItemDef[];
  tiers: Record<GachaRarity, ItemDef[]>;
  progress: GrowthProgress | null;
}) {
  const [collectionFilter, setCollectionFilter] = useState<'all' | 'owned' | 'missing'>('all');
  const [collectionKind, setCollectionKind] = useState<CollectionKind>('body');
  const collectionList = items.filter(COLLECTION_KINDS.find((k) => k.id === collectionKind)!.match);
  return (
    <dialog ref={oddsDialog} className="game-details-dialog mt-dialog" aria-labelledby="gacha-odds-title">
      <header>
        <h2 id="gacha-odds-title">装飾コレクション・提供割合</h2>
        <button type="button" autoFocus onClick={() => oddsDialog.current?.close()}>
          閉じる
        </button>
      </header>
      <div className="game-details-body gacha-odds">
        {/* ★説明は要点ごとに分けて短く（2026-10-19 ご要望「とにかく見にくい」）★ 数字は抽選表の値そのまま */}
        <div className="gacha-odds-summary">
          <p className="gacha-odds-lead">全{items.length}種類。まずレア度を抽選し、同じレア度の中から等確率で1つ出ます。</p>
          <ul className="gacha-odds-rates" aria-label="レア度ごとの確率">
            <li data-rarity="UR"><b>UR</b><span>{pct(GACHA_RARITY_RATES.UR)}%</span></li>
            <li data-rarity="SR"><b>SR</b><span>{pct(GACHA_RARITY_RATES.SR)}%</span></li>
            <li data-rarity="R"><b>R</b><span>{pct(GACHA_RARITY_RATES.R)}%</span></li>
            <li data-rarity="N"><b>N</b><span>{pct(GACHA_RARITY_RATES.N)}%</span></li>
          </ul>
          <ul className="gacha-odds-points">
            <li><strong>UR（大当たり）</strong>は学習プリント{tiers.UR.length}種。1種あたり約{pct(GACHA_RARITY_RATES.UR / Math.max(1, tiers.UR.length))}%</li>
            <li><strong>10＋1連</strong>は最後の1回が「R以上確定」<br /><small>（それまでにR以上が無ければ UR {pct(GACHA_RARITY_RATES.UR / (1 - GACHA_RARITY_RATES.N))}%・SR {pct(GACHA_RARITY_RATES.SR / (1 - GACHA_RARITY_RATES.N))}%・R {pct(GACHA_RARITY_RATES.R / (1 - GACHA_RARITY_RATES.N))}%）</small></li>
            <li><strong>重複</strong>はコインで返還：N {GACHA_DUPLICATE_REFUND_BY_RARITY.N}・R {GACHA_DUPLICATE_REFUND_BY_RARITY.R}・SR {GACHA_DUPLICATE_REFUND_BY_RARITY.SR}・UR {GACHA_DUPLICATE_REFUND_BY_RARITY.UR}枚</li>
            <li>課金・換金なし／天井なし。UR・SR はガチャ限定</li>
          </ul>
          <details className="gacha-odds-more">
            <summary>ショップとの違い・プリントについて</summary>
            <p>ショップは欲しい装飾を選んでコイン交換、ガチャはランダム抽選です。どちらで手に入れたものもマイページに集まり、PDFは「マイPDF」で開けます。</p>
            <p>フレームや一部ポーズはショップ交換・レベル・称号でも獲得できます。学習プリントの問題・正解はアプリ内の問題（確認済み）から作っています。</p>
          </details>
        </div>
        <div
          className="gacha-collection-filters gacha-collection-kinds"
          role="group"
          aria-label="種類で切り替える"
        >
          {COLLECTION_KINDS.map((k) => (
            <button
              key={k.id}
              type="button"
              aria-pressed={collectionKind === k.id}
              onClick={() => setCollectionKind(k.id)}
            >
              {k.label} {items.filter(k.match).length}
            </button>
          ))}
        </div>
        <div className="gacha-collection-filters" role="group" aria-label="所持状況で絞り込む">
          {(
            [
              ['all', 'すべて'],
              ['owned', '所持済み'],
              ['missing', '未所持'],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              aria-pressed={collectionFilter === id}
              onClick={() => setCollectionFilter(id)}
            >
              {label}
            </button>
          ))}
        </div>
        <ul className="gacha-collection-grid" data-kind={collectionKind}>
          {collectionList
            .filter(
              (item) =>
                collectionFilter === 'all' ||
                (collectionFilter === 'owned') === !!progress?.owned.includes(item.id),
            )
            .map((item) => {
              const owned = !!progress?.owned.includes(item.id);
              return (
                <li key={item.id} data-owned={owned}>
                  <ItemArt item={item} progress={progress} size={item.kind === 'print' ? 64 : 76} />
                  <strong>
                    <RarityTag rarity={gachaRarityOf(item)} /> {item.label}
                  </strong>
                  <span>
                    {owned ? '所持済み' : '未所持'} · {pct(gachaItemRate(item))}%
                  </span>
                  {owned && item.kind === 'print' && <PrintLinks item={item} compact />}
                </li>
              );
            })}
        </ul>
        {(() => {
          const list = collectionList;
          const n = list.filter((item) => progress?.owned.includes(item.id)).length;
          return (
            <>
              {collectionFilter === 'missing' && n === list.length && <p>全種類コレクション済みです。</p>}
              {collectionFilter === 'owned' && n === 0 && (
                <p>
                  {collectionKind === 'print'
                    ? 'まだ学習プリントを持っていません。大当たり（UR）で出ます。'
                    : 'まだガチャ対象の装飾を持っていません。'}
                </p>
              )}
            </>
          );
        })()}
        <p>
          プレビューは装備・コインを変更しません。装飾はこのブラウザのアカウントごとに保存されます。強さは変わりません。
        </p>
      </div>
    </dialog>
  );
}
