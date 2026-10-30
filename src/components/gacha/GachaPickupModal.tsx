/**
 * 「ピックアップ」ダイアログ（2026-10-27）。
 *   LR（共通テスト予想問題）全10種と、厳選UR 10種の「中身を少しだけ」見せる。
 *   画像は scripts/gacha-prints/build-previews.py が作る（ページの上半分だけ・下はぼかし）。
 *   リスニングの第1回は音声の試聴（問1だけ）もできる。
 *   ガチャの画面は1画面に収める決まりなので、一覧は画面には並べず、下のボタンからこのダイアログで開く。
 */
import { useEffect, type RefObject } from 'react';
import { gachaRarityOf, printOf, type GrowthProgress, type ItemDef } from '../../battle/core/growth';
import { gachaItemRate } from '../../battle/core/arenaEconomy';
import { GACHA_PREVIEWS } from '../../data/gachaPreviews.generated';
import { kyotsuAudioOf } from '../../data/kyotsuMockAudio';
import { RarityTag, pct } from '../GachaParts';
import { DEFAULT_GACHA_POOL, gachaPoolOf, type GachaPoolId } from '../../battle/core/gachaPools';
import { NIJI_DISCLAIMER } from '../../data/nijiMockPrints';

/** ピックアップに出すアイテム（LR → UR の順。画像があるものだけ） */
export function pickupItems(items: readonly ItemDef[]): ItemDef[] {
  const ids = Object.keys(GACHA_PREVIEWS);
  const list = ids.map((id) => items.find((i) => i.id === id)).filter((i): i is ItemDef => !!i);
  return [...list.filter((i) => gachaRarityOf(i) === 'LR'), ...list.filter((i) => gachaRarityOf(i) !== 'LR')];
}

export function GachaPickupModal({ dialog, items, progress, pool = DEFAULT_GACHA_POOL }: {
  dialog: RefObject<HTMLDialogElement | null>;
  items: readonly ItemDef[];
  progress: GrowthProgress | null;
  pool?: GachaPoolId;
}) {
  const list = pickupItems(items);
  const def = gachaPoolOf(pool);
  // 閉じたら試聴を止める（B案から採用：閉じても裏で鳴り続けないように）
  useEffect(() => {
    const d = dialog.current;
    if (!d) return;
    const stop = () => d.querySelectorAll('audio').forEach((a) => a.pause());
    d.addEventListener('close', stop);
    return () => d.removeEventListener('close', stop);
  }, [dialog]);
  const groups = [
    { id: 'LR', title: `LR ${def.lrName}`, note: def.lrNote, list: list.filter((i) => gachaRarityOf(i) === 'LR') },
    { id: 'UR', title: '厳選UR 完全版の本', note: `大当たり（その一冊で完成する本）から、${def.title}で出るもの。`, list: list.filter((i) => gachaRarityOf(i) !== 'LR') },
  ];
  return (
    <dialog ref={dialog} className="game-details-dialog mt-dialog" aria-labelledby="gacha-pickup-title" data-gacha-pickup>
      <header>
        <h2 id="gacha-pickup-title">{def.title} ピックアップ（中身を少し見る）</h2>
        <button type="button" autoFocus onClick={() => dialog.current?.close()}>
          閉じる
        </button>
      </header>
      <div className="game-details-body gacha-pickup">
        <p className="gacha-pickup-lead">ページの一部だけ見られます。全部は、ガチャで当てて「マイPDF」から。</p>
        {pool === 'niji' && <p className="gacha-detail-disclaimer" data-niji-disclaimer>※ {NIJI_DISCLAIMER}</p>}
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
                            {print ? `${print.pages}ページ` : ''} · {pct(gachaItemRate(item, 'N', pool))}%{owned ? ' · 所持済み' : ''}
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
