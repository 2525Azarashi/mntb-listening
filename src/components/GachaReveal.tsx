import { useMountEffect } from '../hooks/useMountEffect';
import { useRef, useState } from 'react';
import { CinematicSequence, GACHA_REVEAL_CLIPS } from './CinematicClip';
import { FULLFRAME_CINEMATIC_MOVIES } from './AlphaCinematicClip';
import type { GachaRarity } from '../battle/core/growth';
import { play } from '../battle/ui/feedback';
import { REVEAL_BURST_MS, REVEAL_ORDER, REVEAL_TEASE_CAPTION, REVEAL_TEASE_MS, burstSfx, hasTease, revealSteps, revealTotalMs } from './gachaRevealSteps';

/**
 * ガチャの確定演出。光が 青→金→虹→大当たり と上がっていき、引いたレア度で止まって弾ける。
 * 既存のレア度別丸窓（GACHA_REVEAL_CLIPS）や光エフェクトを残したまま、
 * 切り抜きノイズのない美しいフル画角の光粒子バックドロップとして動画④（gacha_duo_intro.mp4）を背後に重ねて一緒に盛り上げる。
 */
export function GachaReveal({ rarity, onDone }: { rarity: GachaRarity; onDone: () => void; key?: number }) {
  const steps = revealSteps(rarity);
  const [index, setIndex] = useState(0);
  const [burst, setBurst] = useState(false);
  /** E1：最後の段のあとの溜め（次のゲージがチカチカ） */
  const [tease, setTease] = useState(false);
  const doneRef = useRef(onDone); doneRef.current = onDone;
  const finished = useRef(false);
  const bgVideoRef = useRef<HTMLVideoElement>(null);
  const finish = () => { if (finished.current) return; finished.current = true; doneRef.current(); };

  const totalSec = Math.max(2.6, revealTotalMs(rarity) / 1000);
  const duoRate = Math.min(2.2, Math.max(1.0, FULLFRAME_CINEMATIC_MOVIES.gachaDuoIntro.durationSec / totalSec));

  useMountEffect(() => {
    const reduce = typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
    const timers: ReturnType<typeof setTimeout>[] = [];
    if (reduce) {
      setIndex(steps.length - 1);
      play(burstSfx(rarity), false);
      timers.push(setTimeout(finish, 600));
      return () => timers.forEach(clearTimeout);
    }
    const v = bgVideoRef.current;
    if (v) {
      v.playbackRate = duoRate;
      void v.play().catch(() => undefined);
    }
    let at = 0;
    steps.forEach((s, i) => {
      timers.push(setTimeout(() => { setIndex(i); if (i > 0) play(s.sfx, s.vibrate); }, at));
      at += s.ms;
    });
    if (hasTease(rarity)) {
      timers.push(setTimeout(() => setTease(true), at));
      at += REVEAL_TEASE_MS;
    }
    timers.push(setTimeout(() => { setTease(false); setBurst(true); play(burstSfx(rarity), true); }, at));
    timers.push(setTimeout(finish, at + REVEAL_BURST_MS));
    return () => { timers.forEach(clearTimeout); v?.pause(); };
    // 1回の抽選につき1度だけ流す
  });

  const step = steps[index];
  const skip = () => { setTease(false); setBurst(true); play(burstSfx(rarity), false); setTimeout(finish, 180); };

  return <div className="gacha-cinema gacha-reveal" data-stage={step.stage} data-burst={burst || undefined} data-tease={tease || undefined} data-gacha-reveal>
    <div className="gacha-reveal-duo-backdrop" aria-hidden="true">
      <video
        ref={bgVideoRef}
        src={FULLFRAME_CINEMATIC_MOVIES.gachaDuoIntro.mp4}
        poster={FULLFRAME_CINEMATIC_MOVIES.gachaDuoIntro.poster}
        muted
        playsInline
        preload="auto"
        disablePictureInPicture
      />
    </div>
    <div className="gacha-reveal-rays" aria-hidden="true" />
    <div className="gacha-reveal-orb" aria-hidden="true"><CinematicSequence names={GACHA_REVEAL_CLIPS[rarity]} label="ガチャの開封動画" /></div>
    <div className="gacha-reveal-sparks" aria-hidden="true">{Array.from({ length: 12 }, (_, i) => <i key={i} style={{ ['--i' as string]: i }} />)}</div>
    <p className="gacha-reveal-caption" role="status" aria-live="assertive" key={tease ? 'tease' : step.stage} data-tease={tease || undefined}>{tease ? REVEAL_TEASE_CAPTION : step.caption}</p>
    {/* E1：ゲージは毎回5本。光った段だけ色が付き、溜めのときは次の1本が点滅する（色は付けない） */}
    <ol className="gacha-reveal-meter" aria-hidden="true">{REVEAL_ORDER.map((stage, i) => <li key={stage} data-stage={stage} data-on={i <= index || undefined} data-tease={tease && i === index + 1 || undefined} />)}</ol>
    <div className="gacha-reveal-flash" aria-hidden="true" />
    <button type="button" onClick={skip}>結果を見る</button>
  </div>;
}

/** 結果画面の星（レア度ぶん順番に光る） */
export function RarityStars({ count }: { count: number }) {
  return <span className="gacha-stars" aria-label={`星${count}`}>{Array.from({ length: count }, (_, i) => <i key={i} style={{ animationDelay: `${0.15 + i * 0.12}s` }}>★</i>)}</span>;
}
