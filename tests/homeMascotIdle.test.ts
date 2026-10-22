import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const home = readFileSync('src/components/Home.tsx', 'utf8');
const css = readFileSync('src/components/home-mascot-idle.css', 'utf8');

describe('ホームのとびら君：継続的な待機アニメーション', () => {
  it('Home で読み込む', () => {
    expect(home).toContain("import './home-mascot-idle.css';");
  });
  it('回していないときに3.2秒周期の連続Idle Animationを再生する', () => {
    expect(css).toContain('.game-home .spin-mascot:not([data-spinning]):not([data-settling]) .spin-mascot-front {');
    expect(css).toContain('animation: home-mascot-idle 3.2s ease-in-out 0s infinite;');
    expect(css).toContain('animation: home-mascot-idle-shadow 3.2s ease-in-out 0s infinite;');
    expect(css).toContain('@keyframes home-mascot-idle {');
    expect(css).toContain('84% { translate: 0 -.7%;');
  });
  it('回転用の transform と重ならないよう、個別の translate/scale/rotate だけを使う', () => {
    const keyframes = css.slice(css.indexOf('@keyframes home-mascot-idle {'), css.indexOf('@keyframes home-mascot-idle-shadow'));
    expect(keyframes).not.toMatch(/transform\s*:/);
  });
  it('動きを減らす設定では止める', () => {
    expect(css).toContain('prefers-reduced-motion: reduce');
  });
});
