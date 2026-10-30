import { useEffect, useMemo, useRef, useState } from 'react';
import { Gift, Coins, ArrowLeft, PlayCircle, Target, Info, Sparkles } from 'lucide-react';
import { RewardVideo } from './RewardVideo';
import { rewardedAdAvailable, preloadRewardedAd, showRewardedAd } from '../ads/rewardedAd';
import { GachaReveal } from './GachaReveal';
import { gachaFeatured } from '../battle/core/gachaFeatured';
import './gacha.css';
import { useGrowthProgress } from '../hooks/useGrowthProgress';
import {
  VIDEO_GACHA_DAILY_LIMIT,
  GACHA_COST,
  GACHA_MULTI_COST,
  gachaItems,
  gachaItemsByRarity,
  gachaItemRate,
} from '../battle/core/arenaEconomy';
import {
  completedVideoToken,
  drawVideoGacha,
  videoGachaPlaysLeft,
  drawGacha,
  drawGachaMulti,
  GACHA_MULTI_COUNT,
} from '../battle/data/growthStore';
import { gachaRarityOf, type ItemDef, type GachaRarity } from '../battle/core/growth';
import { primeAudio } from '../battle/ui/feedback';
import {
  ItemArt,
  RarityTag,
  bestOf,
  pct,
} from './GachaParts';
import { trackEvent } from '../utils/analytics';
import { GachaMultiResult, GachaSingleResult, type GachaDrawResult } from './gacha/GachaResultStage';
import { GachaCollectionModal } from './gacha/GachaCollectionModal';
import { GachaItemDetail, weekEndLabel, weeklyHero, weeklyPickup } from './gacha/GachaItemDetail';
import { GachaPickupModal } from './gacha/GachaPickupModal';
import { TobiraBuddy } from './TobiraBuddy';

type GachaProps = {
  onBack: () => void;
  onMissions: () => void;
  embedded?: boolean;
};

// GachaDrawResult は gacha/GachaResultStage.tsx へ移した（結果表示と同じ所に置く）

export function GachaRoom(props: GachaProps) {
  const { uid } = useGrowthProgress();
  return <GachaRoomContent key={uid} owner={uid} {...props} />;
}

function GachaRoomContent({
  onBack,
  onMissions,
  owner,
  embedded = false,
}: GachaProps & { owner: string; key?: string }) {
  const { progress } = useGrowthProgress();
  const lock = useRef(false);
  const [busy, setBusy] = useState(false);
  const oddsDialog = useRef<HTMLDialogElement>(null);
  const detailDialog = useRef<HTMLDialogElement>(null);
  const [detailItem, setDetailItem] = useState<ItemDef | null>(null);
  const openDetail = (item: ItemDef) => { setDetailItem(item); requestAnimationFrame(() => detailDialog.current?.showModal()); };
  const pickupDialog = useRef<HTMLDialogElement>(null);

  const items = gachaItems();
  const tiers = gachaItemsByRarity();
  const ownedCount = items.filter((item) => progress?.owned.includes(item.id)).length;

  const [confirm, setConfirm] = useState(false);
  const [error, setError] = useState('');
  const [revealing, setRevealing] = useState(false);
  const [revealKey, setRevealKey] = useState(0);
  const [result, setResult] = useState<GachaDrawResult | null>(null);
  const [multi, setMulti] = useState<GachaDrawResult[] | null>(null);
  const bestRarity: GachaRarity | null = result ? result.rarity : multi ? bestOf(multi) : null;

  const [confirmMulti, setConfirmMulti] = useState(false);
  const multiCost = GACHA_MULTI_COST;
  const [videoOpen, setVideoOpen] = useState(false);
  const [freeResult, setFreeResult] = useState(false);
  const videoLeft = videoGachaPlaysLeft();

  /*
   * ★「動画で1回」＝ アプリ公開後はリワード広告（2026-10-05）★
   *   広告が使えるとき（src/ads/adConfig.ts で ON・SDK 登録済み）は広告を見せ、最後まで見たら1回引く。
   *   使えないとき（今の Web 版・広告の在庫切れ・読み込み失敗）は、これまでどおりアプリ内の応援動画を出す。
   *   どちらでも「途中で閉じたら回数を消費しない」「1日5回まで」は同じ。抽選は drawVideoGacha 1か所。
   */
  const adMode = rewardedAdAvailable();
  useEffect(() => {
    preloadRewardedAd();
  }, []);

  const drawFree = async (token: object) => {
    if (lock.current) return;
    lock.current = true;
    setBusy(true);
    try {
      const r = await drawVideoGacha(token, owner);
      if (!r?.result) {
        setError('今日の上限に達したか、保存できませんでした。');
        return;
      }
      setFreeResult(true);
      setMulti(null);
      setResult(r.result);
      setRevealKey((k) => k + 1);
      setRevealing(true);
    } finally {
      lock.current = false;
      setBusy(false);
    }
  };

  const startFree = async () => {
    setError('');
    if (!adMode) {
      setVideoOpen(true);
      return;
    }
    setBusy(true);
    const r = await showRewardedAd();
    setBusy(false);
    if (r.status === 'rewarded') {
      await drawFree(completedVideoToken());
      return;
    }
    if (r.status === 'dismissed') {
      setError('最後まで見ると1回引けます。回数は消費していません。');
      return;
    }
    setVideoOpen(true); // 広告が出せないときは応援動画で代わりに
  };

  const drawMulti = async () => {
    if (lock.current) return;
    lock.current = true;
    setBusy(true);
    setError('');
    setFreeResult(false);
    setConfirmMulti(false);
    primeAudio();
    try {
      const r = await drawGachaMulti(crypto.randomUUID(), owner);
      if (r) trackEvent('gacha_draw11');
      if (!r?.results) {
        setError('抽選できませんでした。残高や保存設定を確認してください。');
        return;
      }
      setResult(null);
      setMulti(r.results);
      setRevealKey((k) => k + 1);
      setRevealing(true);
    } catch {
      setError('抽選できませんでした。再度お試しください。');
    } finally {
      lock.current = false;
      setBusy(false);
    }
  };

  const draw = async () => {
    if (lock.current) return;
    lock.current = true;
    setBusy(true);
    setError('');
    setFreeResult(false);
    setConfirm(false);
    primeAudio();
    try {
      const r = await drawGacha(crypto.randomUUID(), owner);
      if (r) trackEvent('gacha_draw');
      if (!r?.result) {
        setError('抽選できませんでした。残高や保存設定を確認してください。');
        return;
      }
      setMulti(null);
      setResult(r.result);
      setRevealKey((k) => k + 1);
      setRevealing(true);
    } catch {
      setError('抽選できませんでした。再度お試しください。');
    } finally {
      lock.current = false;
      setBusy(false);
    }
  };

  const featured = useMemo(
    () => gachaFeatured({ preferSubjects: ['english_listening', 'english_vocab', 'english_grammar'], srCount: 0, rCount: 0 }),
    [],
  );
  // 目玉は週ごとに LR と UR を交互に（いつも UR にならない）。割合は本物の抽選表の値
  const hero = useMemo(() => weeklyHero(items, featured.week, featured.hero?.item ?? null), [items, featured]);
  const pickup = useMemo(() => weeklyPickup(items, featured.week, hero?.id), [items, featured, hero]);
  const busyView = revealing || !!result || !!multi;
  const collectionLine = (
    <span
      className="gacha-collect-count"
      data-gacha-collection
      aria-label={`コレクション ${ownedCount} / ${items.length}`}
    >
      <span className="gacha-collect-word">コレクション </span>
      <b>{ownedCount}</b> / {items.length}
    </span>
  );

  /*
   * ★画面の流れ（C9）★ ① 今回の注目アイテム → ② 所持マナコイン → ③ ガチャを引く → ④ 結果 → ⑤ コレクションに追加
   *   注目アイテムは gachaFeatured()（ガチャデータから自動生成）。アイテム名は書かない（C23）。
   *   「注目」は見せ方で、割合は本物の抽選表（gachaItemRate）の値をそのまま出す（C8）。
   */
  return (
    <section
      className={`gacha-room ${result ? 'has-result' : ''} ${busyView ? 'is-busy' : ''}`}
      data-best-rarity={!revealing && bestRarity ? bestRarity : undefined}
    >
      {!embedded && (
        <button type="button" className="arena-back" onClick={onBack}>
          <ArrowLeft size={18} />
          マイページ
        </button>
      )}
      {/* ★2026-10-28 A10：モンストのガチャのように「バナー＋絵を押すと詳細」★
          目玉（週がわり）を大きく、その下に今週のピックアップ（LR・URを週ごとに入れ替え）の絵。押すと「アイテムの詳細」。
          ピックアップ一覧・提供割合・ミッションは小さいボタンにまとめた。セット・かけらはショップの「種類」へ移した。 */}
      {!busyView && hero && (
        <section className="gacha-banner" aria-labelledby="gacha-banner-title" data-gacha-featured>
          <header className="gacha-banner-head">
            <h1 id="gacha-banner-title"><Sparkles size={16} aria-hidden="true" />装飾ガチャ</h1>
            <small>{weekEndLabel(featured.week)}</small>
          </header>
          <button
            type="button"
            className="gacha-banner-hero"
            data-rarity={gachaRarityOf(hero)}
            data-gacha-hero
            onClick={() => openDetail(hero)}
            aria-label={`今週の目玉 ${hero.label} の詳細を見る`}
          >
            {/* B5（2026-10-29）：光が走る・キラキラが舞う（目玉を派手に）。動きを減らす設定では止める */}
            <span className="gacha-banner-shine" aria-hidden="true" />
            <span className="gacha-banner-sparks" aria-hidden="true"><i /><i /><i /><i /><i /></span>
            <span className="gacha-banner-art"><ItemArt item={hero} progress={progress} size={76} /></span>
            <span className="gacha-banner-body">
              <span className="gacha-banner-top"><RarityTag rarity={gachaRarityOf(hero)} /><em>今週の目玉</em></span>
              <strong>{hero.label}</strong>
              <small>1種あたり {pct(gachaItemRate(hero))}%{progress?.owned.includes(hero.id) ? ' · 所持済み' : ''}</small>
              <span className="gacha-banner-tap"><Info size={13} aria-hidden="true" />タップで詳細</span>
            </span>
          </button>
          <ul className="gacha-banner-picks" aria-label="今週のピックアップ（押すと詳細）">
            {pickup.map((item) => (
              <li key={item.id}>
                <button type="button" onClick={() => openDetail(item)} data-gacha-pickup-item={item.id} data-rarity={gachaRarityOf(item)} aria-label={`${gachaRarityOf(item)} ${item.label} の詳細を見る`}>
                  <ItemArt item={item} progress={progress} size={40} />
                  <RarityTag rarity={gachaRarityOf(item)} />
                </button>
              </li>
            ))}
          </ul>
          {/* B5：あいていた下の余白に、とびら君がひとこと（目玉をすすめる） */}
          <div className="gacha-banner-buddy">
            <TobiraBuddy size="sm" input={{ screen: 'gacha', seed: featured.week }} line={`今週の目玉は「${hero.label}」！${gachaRarityOf(hero)}はめったに出ないよ`} />
          </div>
          <nav className="gacha-banner-links" aria-label="ガチャの案内">
            <button type="button" className="gacha-chip" aria-haspopup="dialog" onClick={() => pickupDialog.current?.showModal()} data-gacha-pickup-open>ピックアップ一覧</button>
            <button type="button" className="gacha-chip gacha-odds-toggle" aria-haspopup="dialog" onClick={() => oddsDialog.current?.showModal()}>提供割合</button>
            {progress && progress.coins < GACHA_COST && <button type="button" className="gacha-chip" onClick={onMissions}><Target size={13} aria-hidden="true" />コインをためる</button>}
          </nav>
        </section>
      )}

      <div className="gacha-wallet" data-gacha-wallet>
        <p className="gacha-balance" aria-label={`所持 ${progress?.coins ?? 0} マナコイン`}>
          <Coins size={20} aria-hidden="true" />
          <span className="gacha-balance-word">所持</span>
          <b>{progress?.coins ?? '—'}</b>マナコイン
        </p>
        {collectionLine}
      </div>

      {/* 2026-09-30 確定演出：青→金→虹→大当たり と上がり、引いたレア度で止まる（それより上の色は出さない） */}
      {revealing && bestRarity ? (
        <GachaReveal key={revealKey} rarity={bestRarity} onDone={() => setRevealing(false)} />
      ) : result ? (
        <GachaSingleResult
          result={result}
          progress={progress}
          freeResult={freeResult}
          collectionLine={collectionLine}
          setResult={setResult}
          setError={setError}
        />
      ) : multi ? (
        <GachaMultiResult multi={multi} progress={progress} collectionLine={collectionLine} setMulti={setMulti} setError={setError} />
      ) : confirmMulti ? (
        <div className="gacha-confirm" role="group" aria-label="10＋1連ガチャ購入確認">
          <p>
            {multiCost}マナコインを使って{GACHA_MULTI_COUNT}回まとめて引きますか？
            <br />
            <small>10＋1連は R 以上が1つ以上確定</small>
          </p>
          <button type="button" disabled={busy} onClick={() => void drawMulti()}>
            {multiCost}枚で確定する
          </button>
          <button type="button" onClick={() => setConfirmMulti(false)}>
            キャンセル
          </button>
        </div>
      ) : confirm ? (
        <div className="gacha-confirm" role="group" aria-label="ガチャ購入確認">
          <p>{GACHA_COST}マナコインを使って1回引きますか？</p>
          <button type="button" disabled={busy} onClick={() => void draw()}>
            {GACHA_COST}枚で確定する
          </button>
          <button type="button" onClick={() => setConfirm(false)}>
            キャンセル
          </button>
        </div>
      ) : (
        <div className="gacha-pulls" data-gacha-pulls>
          <button
            type="button"
            className="gacha-pull"
            disabled={busy || !progress || progress.coins < GACHA_COST}
            onClick={() => setConfirm(true)}
          >
            <Gift size={20} aria-hidden="true" />
            <span>
              1回引く<small>{GACHA_COST}枚</small>
            </span>
          </button>
          <button
            type="button"
            className="gacha-pull gacha-pull-multi"
            disabled={busy || !progress || progress.coins < multiCost}
            onClick={() => setConfirmMulti(true)}
            data-gacha-multi-pull
          >
            <Gift size={20} aria-hidden="true" />
            <span>
              10＋1連<small>{multiCost}枚・R以上1つ確定</small>
            </span>
          </button>
          <button
            type="button"
            className="gacha-pull gacha-pull-video"
            disabled={busy || !progress || videoLeft === 0}
            onClick={() => void startFree()}
            data-video-gacha
            data-ad-mode={adMode ? 'rewarded' : 'clip'}
          >
            <PlayCircle size={20} aria-hidden="true" />
            <span>
              動画で1回<small>無料・今日あと{videoLeft} / {VIDEO_GACHA_DAILY_LIMIT}回</small>
            </span>
          </button>
        </div>
      )}

      {videoOpen && (
        <RewardVideo
          onCancel={() => setVideoOpen(false)}
          onComplete={async (token) => {
            setVideoOpen(false);
            await drawFree(token);
          }}
        />
      )}
      {error && (
        <p role="status" className="gacha-message">
          {error}
        </p>
      )}
      <div className="gacha-collection-meter" aria-label={`コレクション ${ownedCount}/${items.length}種類`} hidden>
        <progress value={ownedCount} max={items.length} aria-label="装飾の収集状況" />
      </div>
      <GachaCollectionModal oddsDialog={oddsDialog} items={items} tiers={tiers} progress={progress} />
      <GachaItemDetail dialog={detailDialog} item={detailItem} progress={progress} />
      <GachaPickupModal dialog={pickupDialog} items={items} progress={progress} />
    </section>
  );
}
