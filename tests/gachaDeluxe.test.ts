import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import { GACHA_RARITY_RATES, gachaItemsByRarity } from '../src/battle/core/arenaEconomy';
import { GACHA_PRINTS } from '../src/data/gachaPrints.generated';
import { printRarity } from '../src/battle/core/growth';

/** ★2026-10-24 ご要望「はずれを多く・大当たりはとびきり豪華に（その一冊で完成する本）」★ */
const hasPdf = (() => { try { execFileSync('pdftotext', ['-v'], { stdio: 'ignore' }); return true; } catch { return false; } })();
const text = (file: string) => execFileSync('pdftotext', ['-layout', `public${file}`, '-'], { encoding: 'utf8', maxBuffer: 64 << 20 });
const books = GACHA_PRINTS.filter(p => p.category === '完全版');

describe('ガチャの配分（はずれ多め・URは完全版の本だけ）', () => {
  it('N が 74%・UR は 3%・LR 1%（合計 1）', () => {
    expect(GACHA_RARITY_RATES).toEqual({ LR: 0.01, UR: 0.03, SR: 0.06, R: 0.16, N: 0.74 });
    expect(Object.values(GACHA_RARITY_RATES).reduce((a, b) => a + b, 0)).toBeCloseTo(1, 10);
  });
  it('ガチャの UR は全部「完全版」の本。単元プリント・100語テストは SR', () => {
    const tiers = gachaItemsByRarity();
    expect(tiers.UR.length).toBe(books.length);
    for (const item of tiers.UR) expect(books.some(b => b.id === item.id), item.id).toBe(true);
    for (const p of GACHA_PRINTS) expect(printRarity(p), p.id).toBe(p.category === '完全版' ? 'UR' : 'SR');
  });
  it('完全版は15冊（英単語3・英熟語1・リーディング大問別3・リスニング大問別1・全科目分析1・熟語＋英文解釈3・英文法4択3）がそろい、ファイルとページ数が台帳と合う', () => {
    expect(books.map(b => b.id).sort()).toEqual(['print_book_analysis_all', 'print_book_grammar_b4_bunpo', 'print_book_grammar_b4_gohou', 'print_book_grammar_b4_kaiwa',
      'print_book_idiom_all', 'print_book_idiom_reading_advanced', 'print_book_idiom_reading_basic', 'print_book_idiom_reading_standard', 'print_book_listening_all',
      'print_book_reading_mock1', 'print_book_reading_mock2', 'print_book_reading_mock3', 'print_book_vocab_adv', 'print_book_vocab_lv1', 'print_book_vocab_lv2']);
    for (const b of books) {
      expect(existsSync(`public${b.file}`), b.id).toBe(true);
      expect(existsSync(`public${b.thumb}`), b.id).toBe(true);
      expect(Math.abs(statSync(`public${b.file}`).size / 1024 - b.kb), b.id).toBeLessThan(2);
      expect(b.pages, b.id).toBeGreaterThanOrEqual(15);
    }
  });
});

describe.skipIf(!hasPdf)('完全版の中身（その一冊で完成するか）', () => {
  it('単語帳・熟語帳はデータの全語を収録し、確認テスト・総仕上げ100問・解答・さくいんがある', () => {
    for (const id of ['print_book_vocab_lv1', 'print_book_vocab_lv2', 'print_book_vocab_adv', 'print_book_idiom_all']) {
      const t = text(books.find(b => b.id === id)!.file);
      for (const k of ['この本の使い方', '学習計画表', '確認テスト', '総仕上げテスト（100問）', '解答', 'さくいん']) expect(t, `${id} ${k}`).toContain(k);
    }
    expect(text('/prints/print_book_vocab_lv2.pdf')).toContain('962語');
    expect(text('/prints/print_book_idiom_all.pdf')).toContain('1,885熟語');
  });
  it.each(['print_book_reading_mock1', 'print_book_reading_mock2', 'print_book_reading_mock3'])('リーディング大問別 %s：第1問〜第8問すべてに解き方・問題・解説・重要語句、44マーク', (id) => {
    const t = text(`/prints/${id}.pdf`);
    for (let q = 1; q <= 8; q++) {
      expect(t, `第${q}問`).toMatch(new RegExp(`第${q}問\\s*解答・解説`));
    }
    expect((t.match(/特徴と解き方/g) || []).length).toBeGreaterThanOrEqual(8);
    expect((t.match(/重要語句/g) || []).length).toBeGreaterThanOrEqual(8);
    expect(t).toContain('44マーク');
    expect(t).toContain('得点記録表');
  });
  it('リスニング大問別：全単元に聞き方・3回分・解答とスクリプト。QR はアプリの公開サイトの mp3 を指し、そのファイルがリポジトリにある', () => {
    const t = text('/prints/print_book_listening_all.pdf');
    for (const u of ['第1問 A', '第1問 B', '第2問', '第3問', '第4問 A', '第4問 B', '第5問', '第6問 A', '第6問 B']) {
      expect(t, u).toMatch(new RegExp(`${u.replace(' ', '\\s*')}\\s*解答・スクリプト・解説`));
    }
    expect((t.match(/特徴と聞き方/g) || []).length).toBeGreaterThanOrEqual(9);
    for (const k of ['第1回（100点）', '第2回（100点）', '第3回（100点）', '得点記録表', '英語リスニング ＞']) expect(t, k).toContain(k);
    // 音声ファイル名（QR の行き先）はすべて public にある＝アプリと同じ音声
    const files = [...new Set(t.match(/(el1A|el1B|el2|el3)_set\d+_q\d+\.mp3|set\d+_4[AB](_front|_back)?\.mp3|q5set\d+_(lecture|q32|q33)\.mp3|q6set\d+_[AB]\.mp3/g) || [])];
    expect(files.length).toBeGreaterThanOrEqual(70);
    const dir = (f: string) => f.startsWith('q5') ? 'listening_q5' : f.startsWith('q6') ? 'listening_q6' : f.startsWith('set') ? 'listening_q4' : 'listening_audio';
    for (const f of files) expect(existsSync(`public/${dir(f)}/${f}`), f).toBe(true);
  });
  it.each([
    ['print_book_idiom_reading_basic', '英文解釈（基礎）', 'r1-12'],
    ['print_book_idiom_reading_standard', '英文解釈（標準）', 'r2-12'],
    ['print_book_idiom_reading_advanced', '英文解釈（発展）', 'r3-12'],
  ])('熟語＋英文解釈 %s：全12回の問題と解答、熟語のつづき（右上）と英文解釈', (id, head, last) => {
    const t = text(`/prints/${id}.pdf`);
    for (let r = 1; r <= 12; r++) expect(t, `第${r}回`).toContain(`第${r}回`);
    expect(t).toContain(head);
    expect(t).toContain('英熟語（つづき）');
    expect(t).toContain(last);
    expect(t).toContain('全訳と解答');
  });
  it.each([
    ['print_book_grammar_b4_bunpo', ['時制（1）', '時制の一致と話法（2）'], 729],
    ['print_book_grammar_b4_gohou', ['動詞の語法（1）', '名詞の語法（5）'], 290],
    ['print_book_grammar_b4_kaiwa', ['会話表現（1）', '会話表現（15）'], 144],
  ])('英文法4択 %s：見出し「〇〇（1）」、アプリの問題数ぶんの正解と解説', (id, heads, n) => {
    const t = text(`/prints/${id}.pdf`);
    for (const h of heads) expect(t, h).toContain(h);
    expect((t.match(/正解\s*[①②③④]/g) || []).length).toBe(n);
    expect((t.match(/ポイント/g) || []).length).toBeGreaterThanOrEqual(n);
  });
  it('全科目分析：主要科目すべてと出典・最新平均点がある', () => {
    const t = text('/prints/print_book_analysis_all.pdf');
    for (const k of ['英語（リーディング）', '英語（リスニング）', '国語', '数学Ⅰ、数学A', '数学Ⅱ、数学B、数学C', '情報Ⅰ', '物理', '化学', '生物',
      '歴史総合、日本史探究', '歴史総合、世界史探究', '地理総合、地理探究', '出典', '116.37', '56.59']) expect(t, k).toContain(k);
  });
});
