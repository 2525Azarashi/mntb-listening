/**
 * LR 共通テスト 英語リスニング 予想問題の音声（問題ごとに分けた mp3）。
 *   いま入っているのは第1回だけ（2026-10-26 ElevenLabs v4 で利用者が生成 → 問題ごとに切り分け）。
 *   元の6ファイルは audio_sources/commercial/elevenlabs_2026-10-26_kyotsu_l1/ に保管（区切りは split_manifest.json）。
 *   第1問・第2問（問1〜11）は本番どおり2回読み（間に4秒）、第3問〜第6問は1回読み。
 *   ※ 問題番号の日本語アナウンスは入っていない（英語のみ）。
 *
 * 持っている人だけ「マイPDF」で再生できる（tests/kyotsuMockAudio.test.ts がファイルの実在・長さを確認）。
 * scripts/data/listening_audio_ledger.json（374件の共通リスニング台帳）には入れない。
 */
export interface KyotsuAudioTrack {
  /** 問番号（'01' や '18-21'）。ファイル名にも使う */
  q: string;
  /** 大問（例：第1問A）。プレーヤーの見出し */
  part: string;
  /** 画面に出す名前（例：第1問A 問1） */
  label: string;
  /** public/ からのパス */
  file: string;
  /** 秒（目安・実物と±1秒） */
  sec: number;
  /** 2回読みか */
  twice: boolean;
}

/** '01' → 問1、'18-21' → 問18〜21 */
export function kyotsuAudioLabel(q: string): string {
  const [a, b] = q.split('-').map(Number);
  return b ? `問${a}〜${b}` : `問${a}`;
}

const t = (part: string, q: string, sec: number): KyotsuAudioTrack => ({
  q,
  part,
  label: `${part} ${kyotsuAudioLabel(q)}`,
  file: `/prints/kyotsu_assets/audio/kyotsu_l1_q${q}.mp3`,
  sec,
  twice: Number(q.split('-')[0]) <= 11,
});

export const KYOTSU_MOCK_AUDIO: Readonly<Record<string, readonly KyotsuAudioTrack[]>> = {
  print_lr_kyotsu_l_1: [
    t('第1問A', '01', 14), t('第1問A', '02', 13), t('第1問A', '03', 11), t('第1問A', '04', 13),
    t('第1問B', '05', 12), t('第1問B', '06', 11), t('第1問B', '07', 9),
    t('第2問', '08', 47), t('第2問', '09', 34), t('第2問', '10', 29), t('第2問', '11', 36),
    t('第3問', '12', 11), t('第3問', '13', 14), t('第3問', '14', 15), t('第3問', '15', 16), t('第3問', '16', 13), t('第3問', '17', 9),
    t('第4問A', '18-21', 27), t('第4問A', '22-25', 18), t('第4問B', '26', 29),
    t('第5問', '27-32', 68), t('第5問', '33', 17),
    t('第6問A', '34-35', 32), t('第6問B', '36-37', 48),
  ],
};

export function kyotsuAudioOf(printId: string): readonly KyotsuAudioTrack[] {
  return KYOTSU_MOCK_AUDIO[printId] ?? [];
}
