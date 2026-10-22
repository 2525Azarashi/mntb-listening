import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const home = readFileSync('src/components/Home.tsx', 'utf8');
const css = readFileSync('src/components/home-mascot-idle.css', 'utf8');

describe('ホームのとびら君：待機モーション（2026-10-21）', () => {
  it('Home で読み込む', () => {
    expect(home).toContain("import './home-mascot-idle.css';");
  });
  it('回していないときだけ、6秒ごとに約0.6秒（10%）跳ねる', () => {
    expect(css).toContain('.game-home .spin-mascot:not([data-spinning]):not([data-settling]) .spin-mascot-front {');
    expect(css).toContain('animation: home-mascot-hop 6s');
    expect(css).toContain('10%, 100% { translate: 0 0; scale: 1 1;');
  });
  it('回転用の transform と重ならないよう、個別の translate/scale/rotate だけを使う', () => {
    const keyframes = css.slice(css.indexOf('@keyframes home-mascot-hop {'), css.indexOf('@keyframes home-mascot-hop-shadow'));
    expect(keyframes).not.toMatch(/transform\s*:/);
  });
  it('動きを減らす設定では止める', () => {
    expect(css).toContain('prefers-reduced-motion: reduce');
  });
});
