import { describe, expect, it } from 'vitest';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { resolve } from 'node:path';
import { TOBIRA_MOTIONS, motionSrc, type TobiraMotionName } from '../src/components/TobiraMotion';

describe('とびら君の背景なしモーション', () => {
  it('ready のものは webm / webp / png がそろい、動画は 1MB 未満', () => {
    for (const [name, def] of Object.entries(TOBIRA_MOTIONS)) {
      if (!def.ready) continue;
      for (const ext of ['webm', 'webp', 'png'] as const) {
        const f = resolve('public', '.' + motionSrc(name as TobiraMotionName, ext));
        expect(existsSync(f), `${name}.${ext}`).toBe(true);
        if (ext !== 'png') expect(statSync(f).size, `${name}.${ext}`).toBeLessThan(1_000_000);
      }
    }
  });
  it('長さは 1〜4 秒（静止画の位置で短く動くだけ）', () => {
    for (const [name, def] of Object.entries(TOBIRA_MOTIONS)) {
      expect(def.ms, name).toBeGreaterThanOrEqual(1000);
      expect(def.ms, name).toBeLessThanOrEqual(4000);
    }
  });
  it('台帳とプロンプト集に全部載っている', () => {
    const ledger = readFileSync('docs/TOBIRA_MOTION.md', 'utf8');
    const prompts = readFileSync('docs/TOBIRA_MOTION_PROMPTS.md', 'utf8');
    for (const name of Object.keys(TOBIRA_MOTIONS)) {
      expect(ledger, name).toContain(`| ${name} |`);
      expect(prompts, name).toContain(`import.sh ${name}.mp4 ${name}`);
    }
  });
});
