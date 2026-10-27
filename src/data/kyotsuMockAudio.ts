/**
 * LR 共通テスト 英語リスニング 予想問題の音声（問題ごとに分けた mp3）。
 *   いま入っているのは第1回だけ（2026-10-26 ElevenLabs v4 で利用者が生成 → 問題ごとに切り分け）。
 *   元の6ファイルは audio_sources/commercial/elevenlabs_2026-10-26_kyotsu_l1/ に保管。
 *   第1問・第2問（q01〜q11）は本番どおり2回読み（間に4秒）、第3問〜第6問は1回読み。
 *   ※ 問題番号の日本語アナウンスは入っていない（英語のみ）。
 *
 * 持っている人だけ「マイPDF」で再生できる（tests/kyotsuMockAudio.test.ts がファイルの実在を確認）。
 * scripts/data/listening_audio_ledger.json（374件の共通リスニング台帳）には入れない。
 */
export interface KyotsuAudioTrack {
  /** 画面に出す名前（例：第1問A 問1） */
  label: string;
  /** public/ からのパス */
  file: string;
  /** 秒（目安） */
  sec: number;
  /** 2回読みか */
  twice: boolean;
}

const A = (q: string) => `/prints/kyotsu_assets/audio/kyotsu_l1_q${q}.mp3`;
const t = (label: string, q: string, sec: number, twice = false): KyotsuAudioTrack => ({ label, file: A(q), sec, twice });

export const KYOTSU_MOCK_AUDIO: Readonly<Record<string, readonly KyotsuAudioTrack[]>> = {
  print_lr_kyotsu_l_1: [
    t('第1問A 問1', '01', 14, true),
    t('第1問A 問2', '02', 13, true),
    t('第1問A 問3', '03', 11, true),
    t('第1問A 問4', '04', 13, true),
    t('第1問B 問5', '05', 12, true),
    t('第1問B 問6', '06', 11, true),
    t('第1問B 問7', '07', 9, true),
    t('第2問 問8', '08', 47, true),
    t('第2問 問9', '09', 34, true),
    t('第2問 問10', '10', 29, true),
    t('第2問 問11', '11', 36, true),
    t('第3問 問12', '12', 11),
    t('第3問 問13', '13', 14),
    t('第3問 問14', '14', 15),
    t('第3問 問15', '15', 16),
    t('第3問 問16', '16', 13),
    t('第3問 問17', '17', 9),
    t('第4問A 問18〜21', '18-21', 27),
    t('第4問A 問22〜25', '22-25', 18),
    t('第4問B 問26', '26', 29),
    t('第5問 問27〜32', '27-32', 68),
    t('第5問 問33', '33', 17),
    t('第6問A 問34・35', '34-35', 32),
    t('第6問B 問36・37', '36-37', 48),
  ],
};

export function kyotsuAudioOf(printId: string): readonly KyotsuAudioTrack[] {
  return KYOTSU_MOCK_AUDIO[printId] ?? [];
}
