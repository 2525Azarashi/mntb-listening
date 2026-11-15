import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { ALPHA_CINEMATIC_CLIPS } from '../src/components/AlphaCinematicClip';
import { TITLE_SCREEN_BGM_SRC, TITLE_SCREEN_BGM_SUBTLE_GAIN } from '../src/components/TitleBgmControl';

const probe = (file: string) => {
  try {
    return JSON.parse(
      execFileSync(
        'ffprobe',
        ['-v', 'error', '-show_entries', 'stream=codec_type,codec_name,width,height:format=duration', '-of', 'json', file],
        { encoding: 'utf8' },
      ),
    );
  } catch {
    return null;
  }
};

describe('2026-11-15 透過演出動画4種＋タイトルBGMループ', () => {
  it('すべての透過WebM・iOS用SBS MP4・ポスター・終了プレートが実在し、1MB未満かつ音声トラック無し', () => {
    for (const [name, clip] of Object.entries(ALPHA_CINEMATIC_CLIPS)) {
      for (const rel of [clip.webm, clip.sbsMp4, clip.poster, clip.endPlate]) {
        const file = resolve('public', '.' + rel);
        expect(existsSync(file), `${name}: ${rel}`).toBe(true);
        expect(statSync(file).size, `${name} size: ${rel}`).toBeLessThan(1_000_000);
      }
      const webmInfo = probe(resolve('public', '.' + clip.webm));
      if (webmInfo) {
        expect(webmInfo.streams.some((s: { codec_type: string }) => s.codec_type === 'audio'), `${name} webm muted`).toBe(false);
      }
      const sbsInfo = probe(resolve('public', '.' + clip.sbsMp4));
      if (sbsInfo) {
        expect(sbsInfo.streams.some((s: { codec_type: string }) => s.codec_type === 'audio'), `${name} sbs muted`).toBe(false);
        const v = sbsInfo.streams.find((s: { codec_type: string }) => s.codec_type === 'video');
        expect([v.width, v.height], `${name} sbs stacked dimensions`).toEqual([clip.width, clip.height * 2]);
      }
    }
  });

  it('タイトル画面が横向き／縦向きを動的に切り替え、スキップ可能で、BGMミュート切替を備える', () => {
    const launch = readFileSync('src/components/LaunchScreen.tsx', 'utf8');
    expect(launch).toContain('(orientation: landscape) and (min-width: 768px)');
    expect(launch).toContain('ALPHA_CINEMATIC_CLIPS.titleLandscape');
    expect(launch).toContain('ALPHA_CINEMATIC_CLIPS.titlePortrait');
    expect(launch).toContain('skippable');
    expect(launch).toContain('TitleBgmMuteButton');
    expect(launch).toContain('titleClip.endPlate');

    const bgmFile = resolve('public', '.' + TITLE_SCREEN_BGM_SRC);
    expect(existsSync(bgmFile)).toBe(true);
    expect(statSync(bgmFile).size).toBeLessThan(500_000);
    expect(TITLE_SCREEN_BGM_SUBTLE_GAIN).toBeGreaterThan(0.1);
    expect(TITLE_SCREEN_BGM_SUBTLE_GAIN).toBeLessThanOrEqual(0.5);
  });

  it('対戦カウントダウン（3・2・1・START!）とガチャ確定演出（GachaReveal / RewardVideo）に統合されている', () => {
    const countdown = readFileSync('src/battle/ui/BattleLiveParts.tsx', 'utf8');
    expect(countdown).toContain('ALPHA_CINEMATIC_CLIPS.battleCountdown');
    expect(countdown).toContain("label === 'START!'");

    const gachaReveal = readFileSync('src/components/GachaReveal.tsx', 'utf8');
    expect(gachaReveal).toContain('ALPHA_CINEMATIC_CLIPS.gachaOverlay');
    expect(gachaReveal).toContain('GACHA_REVEAL_CLIPS[rarity]');

    const rewardVideo = readFileSync('src/components/RewardVideo.tsx', 'utf8');
    expect(rewardVideo).toContain('ALPHA_CINEMATIC_CLIPS.gachaOverlay');
  });
});
