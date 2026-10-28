import { Capacitor } from '@capacitor/core';
import { AD_TOGGLES, getEffectiveBannerId, getEffectiveRewardedId } from '../utils/adConfig';

const env = (import.meta as unknown as { env?: Record<string, string | undefined> }).env ?? {};
const on = (v: string | undefined, defaultVal: boolean) => (v != null ? v === '1' || v === 'true' : defaultVal);

export type BannerPosition = 'top' | 'bottom' | 'both';

const isIos = Capacitor.getPlatform() === 'ios';

export const AD_CONFIG = {
  rewarded: {
    /** true にすると「動画で1回」が広告になる（アプリ版または環境変数で有効） */
    enabled: on(env.VITE_ADS_REWARDED, Capacitor.isNativePlatform() && AD_TOGGLES.enableRewarded),
    unitId: getEffectiveRewardedId(isIos ? 'ios' : 'android'),
    dailyLimit: 5,
  },
  banner: {
    /**
     * ネイティブアプリでバナー枠を予約する。Web版ではAdMobを表示しないため空白枠も作らない。
     * ?no_ads=1 または VITE_ADS_BANNER=0 でネイティブ広告も無効化できる。
     */
    enabled: Capacitor.isNativePlatform() && on(env.VITE_ADS_BANNER, AD_TOGGLES.enableBottomBanner),
    position: ((env.VITE_ADS_BANNER_POSITION as BannerPosition) || 'bottom') as BannerPosition,
    unitId: getEffectiveBannerId(isIos ? 'ios' : 'android'),
    height: 50,
    /** バナーを出さない画面（問題を解いている最中・対戦中・解説など）。学習の邪魔をしない */
    // 'pdf' … アプリ内の PDF ビューを開いている間（PDF の上に広告を重ねない・2026-10-17）
    hiddenOn: ['quiz', 'explanation', 'battle_live', 'onboarding', 'launch', 'pdf'] as string[],
  },
} as const;

export const adsActive = () => AD_CONFIG.rewarded.enabled || AD_CONFIG.banner.enabled;
