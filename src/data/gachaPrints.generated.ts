// ★自動生成ファイル★ 手で直さない。
// 再生成: npx tsx scripts/gacha-prints/dump-data.mts .tmpwork/prints-data.json
//         node scripts/gacha-prints/build-prints.mjs .tmpwork/prints-data.json
//         python3 scripts/gacha-prints/finalize.py

export type GachaPrintCategory = '出題傾向' | '演習プリント' | '単語テスト' | '完全版';

export interface GachaPrintDef {
  /** ガチャのアイテム id（ITEMS にもこの id で入る） */
  id: string;
  label: string;
  subject: string;
  category: GachaPrintCategory;
  /** public/ からの PDF パス */
  file: string;
  /** 1ページ目のサムネイル（webp） */
  thumb: string;
  pages: number;
  kb: number;
}

export const GACHA_PRINTS: readonly GachaPrintDef[] = [
  {
    "id": "print_trend_cb_all",
    "label": "化学基礎 共通テスト出題傾向 総合レポート",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_all.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_all.webp",
    "pages": 5,
    "kb": 604
  },
  {
    "id": "print_trend_cb_ch1",
    "label": "化学基礎 1章 物質の構成 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch1.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch1.webp",
    "pages": 9,
    "kb": 621
  },
  {
    "id": "print_trend_cb_ch2",
    "label": "化学基礎 2章 物質の構成粒子 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch2.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch2.webp",
    "pages": 7,
    "kb": 460
  },
  {
    "id": "print_trend_cb_ch3",
    "label": "化学基礎 3章 化学結合 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch3.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch3.webp",
    "pages": 8,
    "kb": 525
  },
  {
    "id": "print_trend_cb_ch4",
    "label": "化学基礎 4章 物質量と化学反応式 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch4.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch4.webp",
    "pages": 9,
    "kb": 531
  },
  {
    "id": "print_trend_cb_ch5",
    "label": "化学基礎 5章 酸と塩基 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch5.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch5.webp",
    "pages": 12,
    "kb": 597
  },
  {
    "id": "print_trend_cb_ch6",
    "label": "化学基礎 6章 酸化還元反応 出題傾向＋即演習",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_trend_cb_ch6.pdf",
    "thumb": "/prints/thumbs/print_trend_cb_ch6.webp",
    "pages": 9,
    "kb": 565
  },
  {
    "id": "print_trend_c_all",
    "label": "化学 共通テスト出題傾向 総合レポート",
    "subject": "chemistry",
    "category": "出題傾向",
    "file": "/prints/print_trend_c_all.pdf",
    "thumb": "/prints/thumbs/print_trend_c_all.webp",
    "pages": 9,
    "kb": 724
  },
  {
    "id": "print_trend_c_theoretical",
    "label": "化学 理論化学 出題傾向＋即演習",
    "subject": "chemistry",
    "category": "出題傾向",
    "file": "/prints/print_trend_c_theoretical.pdf",
    "thumb": "/prints/thumbs/print_trend_c_theoretical.webp",
    "pages": 34,
    "kb": 1001
  },
  {
    "id": "print_trend_c_inorganic",
    "label": "化学 無機化学 出題傾向＋即演習",
    "subject": "chemistry",
    "category": "出題傾向",
    "file": "/prints/print_trend_c_inorganic.pdf",
    "thumb": "/prints/thumbs/print_trend_c_inorganic.webp",
    "pages": 22,
    "kb": 854
  },
  {
    "id": "print_trend_c_organic",
    "label": "化学 有機化学 出題傾向",
    "subject": "chemistry",
    "category": "出題傾向",
    "file": "/prints/print_trend_c_organic.pdf",
    "thumb": "/prints/thumbs/print_trend_c_organic.webp",
    "pages": 21,
    "kb": 793
  },
  {
    "id": "print_cb_ch1",
    "label": "化学基礎 1章 物質の構成 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch1.pdf",
    "thumb": "/prints/thumbs/print_cb_ch1.webp",
    "pages": 11,
    "kb": 635
  },
  {
    "id": "print_cb_ch2",
    "label": "化学基礎 2章 物質の構成粒子 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch2.pdf",
    "thumb": "/prints/thumbs/print_cb_ch2.webp",
    "pages": 11,
    "kb": 536
  },
  {
    "id": "print_cb_ch3",
    "label": "化学基礎 3章 化学結合 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch3.pdf",
    "thumb": "/prints/thumbs/print_cb_ch3.webp",
    "pages": 11,
    "kb": 583
  },
  {
    "id": "print_cb_ch4",
    "label": "化学基礎 4章 物質量と化学反応式 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch4.pdf",
    "thumb": "/prints/thumbs/print_cb_ch4.webp",
    "pages": 11,
    "kb": 559
  },
  {
    "id": "print_cb_ch5",
    "label": "化学基礎 5章 酸と塩基 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch5.pdf",
    "thumb": "/prints/thumbs/print_cb_ch5.webp",
    "pages": 12,
    "kb": 627
  },
  {
    "id": "print_cb_ch6",
    "label": "化学基礎 6章 酸化還元反応 演習50題",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_cb_ch6.pdf",
    "thumb": "/prints/thumbs/print_cb_ch6.webp",
    "pages": 13,
    "kb": 638
  },
  {
    "id": "print_c_theoretical",
    "label": "化学 理論化学（熱化学） 演習50題",
    "subject": "chemistry",
    "category": "演習プリント",
    "file": "/prints/print_c_theoretical.pdf",
    "thumb": "/prints/thumbs/print_c_theoretical.webp",
    "pages": 12,
    "kb": 635
  },
  {
    "id": "print_c_inorganic",
    "label": "化学 無機化学 演習50題",
    "subject": "chemistry",
    "category": "演習プリント",
    "file": "/prints/print_c_inorganic.pdf",
    "thumb": "/prints/thumbs/print_c_inorganic.webp",
    "pages": 23,
    "kb": 300
  },
  {
    "id": "print_math_prob",
    "label": "数学 数学A「場合の数と確率」演習40題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_prob.pdf",
    "thumb": "/prints/thumbs/print_math_prob.webp",
    "pages": 11,
    "kb": 585
  },
  {
    "id": "print_math_int",
    "label": "数学 数学A「整数の性質」演習39題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_int.pdf",
    "thumb": "/prints/thumbs/print_math_int.webp",
    "pages": 12,
    "kb": 553
  },
  {
    "id": "print_math_data",
    "label": "数学 数学Ⅰ「データの分析」演習40題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_data.pdf",
    "thumb": "/prints/thumbs/print_math_data.webp",
    "pages": 10,
    "kb": 521
  },
  {
    "id": "print_math_integral",
    "label": "数学 数学Ⅲ「積分法」演習40題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_integral.pdf",
    "thumb": "/prints/thumbs/print_math_integral.webp",
    "pages": 11,
    "kb": 588
  },
  {
    "id": "print_math_vector",
    "label": "数学 数学C「ベクトル」演習40題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_vector.pdf",
    "thumb": "/prints/thumbs/print_math_vector.webp",
    "pages": 11,
    "kb": 521
  },
  {
    "id": "print_math_basic_all",
    "label": "数学Ⅰ・A・Ⅱ・B・Ⅲ・C 基礎〜標準 総まとめ114題",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_basic_all.pdf",
    "thumb": "/prints/thumbs/print_math_basic_all.webp",
    "pages": 33,
    "kb": 299
  },
  {
    "id": "print_math_quadratic_weekly",
    "label": "数学Ⅰ 2次関数 週課題 全6週（62ページ）",
    "subject": "math",
    "category": "演習プリント",
    "file": "/prints/print_math_quadratic_weekly.pdf",
    "thumb": "/prints/thumbs/print_math_quadratic_weekly.webp",
    "pages": 62,
    "kb": 261
  },
  {
    "id": "print_bio_1",
    "label": "生物基礎 前半（生物の特徴・遺伝子）演習50題",
    "subject": "biology_basic",
    "category": "演習プリント",
    "file": "/prints/print_bio_1.pdf",
    "thumb": "/prints/thumbs/print_bio_1.webp",
    "pages": 10,
    "kb": 672
  },
  {
    "id": "print_bio_2",
    "label": "生物基礎 後半（体内環境・植生・生態系）演習50題",
    "subject": "biology_basic",
    "category": "演習プリント",
    "file": "/prints/print_bio_2.pdf",
    "thumb": "/prints/thumbs/print_bio_2.webp",
    "pages": 10,
    "kb": 722
  },
  {
    "id": "print_joho_jh1",
    "label": "情報Ⅰ「情報社会」演習40題",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_joho_jh1.pdf",
    "thumb": "/prints/thumbs/print_joho_jh1.webp",
    "pages": 12,
    "kb": 708
  },
  {
    "id": "print_joho_jh2",
    "label": "情報Ⅰ「デジタル化」演習40題",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_joho_jh2.pdf",
    "thumb": "/prints/thumbs/print_joho_jh2.webp",
    "pages": 11,
    "kb": 599
  },
  {
    "id": "print_joho_jh3",
    "label": "情報Ⅰ「プログラミング」演習40題",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_joho_jh3.pdf",
    "thumb": "/prints/thumbs/print_joho_jh3.webp",
    "pages": 11,
    "kb": 541
  },
  {
    "id": "print_joho_jh4",
    "label": "情報Ⅰ「ネットワーク」演習40題",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_joho_jh4.pdf",
    "thumb": "/prints/thumbs/print_joho_jh4.webp",
    "pages": 11,
    "kb": 620
  },
  {
    "id": "print_joho_jh5",
    "label": "情報Ⅰ「データ活用」演習40題",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_joho_jh5.pdf",
    "thumb": "/prints/thumbs/print_joho_jh5.webp",
    "pages": 11,
    "kb": 626
  },
  {
    "id": "print_grammar_100",
    "label": "英文法 全20単元 総合100題",
    "subject": "english_grammar",
    "category": "演習プリント",
    "file": "/prints/print_grammar_100.pdf",
    "thumb": "/prints/thumbs/print_grammar_100.webp",
    "pages": 63,
    "kb": 543
  },
  {
    "id": "print_vocab_lv1",
    "label": "英単語 Lv1 共通テスト基礎 100語テスト",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv1.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv1.webp",
    "pages": 14,
    "kb": 202
  },
  {
    "id": "print_vocab_lv2",
    "label": "英単語 Lv2 共通テスト標準 100語テスト",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv2.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv2.webp",
    "pages": 14,
    "kb": 216
  },
  {
    "id": "print_vocab_lv3",
    "label": "英単語 Lv3 二次・私大標準 100語テスト",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv3.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv3.webp",
    "pages": 14,
    "kb": 199
  },
  {
    "id": "print_vocab_lv4",
    "label": "英単語 Lv4 難関・最難関 100語テスト",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv4.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv4.webp",
    "pages": 14,
    "kb": 195
  },
  {
    "id": "print_vocab_ilv1",
    "label": "英熟語 Lv1 基礎 100熟語テスト",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_ilv1.pdf",
    "thumb": "/prints/thumbs/print_vocab_ilv1.webp",
    "pages": 13,
    "kb": 150
  },
  {
    "id": "print_rika_1",
    "label": "高校入試 理科 生物編 最終チェック60題",
    "subject": "rika",
    "category": "演習プリント",
    "file": "/prints/print_rika_1.pdf",
    "thumb": "/prints/thumbs/print_rika_1.webp",
    "pages": 28,
    "kb": 363
  },
  {
    "id": "print_rika_2",
    "label": "高校入試 理科 物理編 最終チェック60題",
    "subject": "rika",
    "category": "演習プリント",
    "file": "/prints/print_rika_2.pdf",
    "thumb": "/prints/thumbs/print_rika_2.webp",
    "pages": 28,
    "kb": 307
  },
  {
    "id": "print_rika_3",
    "label": "高校入試 理科 化学・地学編 最終チェック60題",
    "subject": "rika",
    "category": "演習プリント",
    "file": "/prints/print_rika_3.pdf",
    "thumb": "/prints/thumbs/print_rika_3.webp",
    "pages": 25,
    "kb": 279
  },
  {
    "id": "print_rank_cb",
    "label": "化学基礎 共テ頻出ランキング＆直前暗記チェックシート",
    "subject": "chemistry_basic",
    "category": "出題傾向",
    "file": "/prints/print_rank_cb.pdf",
    "thumb": "/prints/thumbs/print_rank_cb.webp",
    "pages": 9,
    "kb": 673
  },
  {
    "id": "print_rank_c",
    "label": "化学 共テ頻出ランキング＆直前暗記チェックシート",
    "subject": "chemistry",
    "category": "出題傾向",
    "file": "/prints/print_rank_c.pdf",
    "thumb": "/prints/thumbs/print_rank_c.webp",
    "pages": 12,
    "kb": 754
  },
  {
    "id": "print_mock_cb_1",
    "label": "化学基礎 共テ形式ミニ模試 第1回（30問・30分）",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_mock_cb_1.pdf",
    "thumb": "/prints/thumbs/print_mock_cb_1.webp",
    "pages": 12,
    "kb": 698
  },
  {
    "id": "print_mock_cb_2",
    "label": "化学基礎 共テ形式ミニ模試 第2回（30問・30分）",
    "subject": "chemistry_basic",
    "category": "演習プリント",
    "file": "/prints/print_mock_cb_2.pdf",
    "thumb": "/prints/thumbs/print_mock_cb_2.webp",
    "pages": 12,
    "kb": 696
  },
  {
    "id": "print_mock_joho_1",
    "label": "情報Ⅰ 共テ形式ミニ模試 第1回（40問・40分）",
    "subject": "joho",
    "category": "演習プリント",
    "file": "/prints/print_mock_joho_1.pdf",
    "thumb": "/prints/thumbs/print_mock_joho_1.webp",
    "pages": 11,
    "kb": 684
  },
  {
    "id": "print_mock_bio_1",
    "label": "生物基礎 共テ形式ミニ模試 第1回（40問・30分）",
    "subject": "biology_basic",
    "category": "演習プリント",
    "file": "/prints/print_mock_bio_1.pdf",
    "thumb": "/prints/thumbs/print_mock_bio_1.webp",
    "pages": 9,
    "kb": 755
  },
  {
    "id": "print_vocab_lv2_2",
    "label": "英単語 Lv2 共通テスト標準 100語テスト 第2集",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv2_2.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv2_2.webp",
    "pages": 14,
    "kb": 206
  },
  {
    "id": "print_vocab_lv3_2",
    "label": "英単語 Lv3 二次・私大標準 100語テスト 第2集",
    "subject": "english_vocab",
    "category": "単語テスト",
    "file": "/prints/print_vocab_lv3_2.pdf",
    "thumb": "/prints/thumbs/print_vocab_lv3_2.webp",
    "pages": 14,
    "kb": 202
  },
  // ★2026-10-24 UR（大当たり）＝完全版の本（scripts/gacha-prints/build-vocab-book.py / build-reading-mock.py / build-analysis-book.py）★
  {
    "id": "print_book_vocab_lv1",
    "label": "英単語 完全版 Lv1 共通テスト基礎の全語（1185語・30日で3周）",
    "subject": "english_vocab",
    "category": "完全版",
    "file": "/prints/print_book_vocab_lv1.pdf",
    "thumb": "/prints/thumbs/print_book_vocab_lv1.webp",
    "pages": 77,
    "kb": 759
  },
  {
    "id": "print_book_vocab_lv2",
    "label": "英単語 完全版 Lv2 共通テスト標準の全語（962語）",
    "subject": "english_vocab",
    "category": "完全版",
    "file": "/prints/print_book_vocab_lv2.pdf",
    "thumb": "/prints/thumbs/print_book_vocab_lv2.webp",
    "pages": 61,
    "kb": 686
  },
  {
    "id": "print_book_vocab_adv",
    "label": "英単語 完全版 Lv3・Lv4 二次・私大・難関の全語（1681語）",
    "subject": "english_vocab",
    "category": "完全版",
    "file": "/prints/print_book_vocab_adv.pdf",
    "thumb": "/prints/thumbs/print_book_vocab_adv.webp",
    "pages": 89,
    "kb": 879
  },
  {
    "id": "print_book_idiom_all",
    "label": "英熟語 完全版 基礎から難関まで全熟語（1885熟語）",
    "subject": "english_vocab",
    "category": "完全版",
    "file": "/prints/print_book_idiom_all.pdf",
    "thumb": "/prints/thumbs/print_book_idiom_all.webp",
    "pages": 95,
    "kb": 745
  },
  {
    "id": "print_book_reading_mock1",
    "label": "共通テスト 英語リーディング 大問別演習 完全版 第1回（全8大問・100点）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_reading_mock1.pdf",
    "thumb": "/prints/thumbs/print_book_reading_mock1.webp",
    "pages": 25,
    "kb": 247
  },
  {
    "id": "print_book_analysis_all",
    "label": "共通テスト 全科目 出題分析 完全版（2026年度平均点・約50年の流れ・時期別対策）",
    "subject": "all",
    "category": "完全版",
    "file": "/prints/print_book_analysis_all.pdf",
    "thumb": "/prints/thumbs/print_book_analysis_all.webp",
    "pages": 18,
    "kb": 235
  },
  {
    "id": "print_book_reading_mock2",
    "label": "共通テスト 英語リーディング 大問別演習 完全版 第2回（全8大問・100点）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_reading_mock2.pdf",
    "thumb": "/prints/thumbs/print_book_reading_mock2.webp",
    "pages": 24,
    "kb": 232
  },
  {
    "id": "print_book_reading_mock3",
    "label": "共通テスト 英語リーディング 大問別演習 完全版 第3回（全8大問・100点）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_reading_mock3.pdf",
    "thumb": "/prints/thumbs/print_book_reading_mock3.webp",
    "pages": 24,
    "kb": 242
  },
  {
    "id": "print_book_listening_all",
    "label": "共通テスト 英語リスニング 大問別演習 完全版（全6大問・3回分・アプリの音声と連動）",
    "subject": "english_listening",
    "category": "完全版",
    "file": "/prints/print_book_listening_all.pdf",
    "thumb": "/prints/thumbs/print_book_listening_all.webp",
    "pages": 79,
    "kb": 2327
  },
  // ★2026-10-27 UR に追加：B4 白黒の小テスト・英文法4択（scripts/gacha-prints/idiom_reading/ ・ grammar_b4/ → idiom_reading/publish.py）★
  {
    "id": "print_book_idiom_reading_basic",
    "label": "英熟語＋英文解釈 小テスト 基礎コース 全12回（熟語 No.1〜479・B4白黒・解答つき）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_idiom_reading_basic.pdf",
    "thumb": "/prints/thumbs/print_book_idiom_reading_basic.webp",
    "pages": 24,
    "kb": 456
  },
  {
    "id": "print_book_idiom_reading_standard",
    "label": "英熟語＋英文解釈 小テスト 標準コース 全12回（熟語 No.480〜939・B4白黒・解答つき）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_idiom_reading_standard.pdf",
    "thumb": "/prints/thumbs/print_book_idiom_reading_standard.webp",
    "pages": 24,
    "kb": 487
  },
  {
    "id": "print_book_idiom_reading_advanced",
    "label": "英熟語＋英文解釈 小テスト 発展コース 全12回（熟語 No.940〜1388・B4白黒・解答つき）",
    "subject": "english_reading",
    "category": "完全版",
    "file": "/prints/print_book_idiom_reading_advanced.pdf",
    "thumb": "/prints/thumbs/print_book_idiom_reading_advanced.webp",
    "pages": 24,
    "kb": 511
  },
  {
    "id": "print_book_grammar_b4_bunpo",
    "label": "英文法 4択プリント 文法編 第1〜16章（729問・80回分・アプリと同じ問題）",
    "subject": "english_grammar",
    "category": "完全版",
    "file": "/prints/print_book_grammar_b4_bunpo.pdf",
    "thumb": "/prints/thumbs/print_book_grammar_b4_bunpo.webp",
    "pages": 80,
    "kb": 737
  },
  {
    "id": "print_book_grammar_b4_gohou",
    "label": "英文法 4択プリント 語法編 第17〜19章（290問・30回分・アプリと同じ問題）",
    "subject": "english_grammar",
    "category": "完全版",
    "file": "/prints/print_book_grammar_b4_gohou.pdf",
    "thumb": "/prints/thumbs/print_book_grammar_b4_gohou.webp",
    "pages": 30,
    "kb": 434
  },
  {
    "id": "print_book_grammar_b4_kaiwa",
    "label": "英文法 4択プリント 会話表現編 第20章（144問・15回分・アプリと同じ問題）",
    "subject": "english_grammar",
    "category": "完全版",
    "file": "/prints/print_book_grammar_b4_kaiwa.pdf",
    "thumb": "/prints/thumbs/print_book_grammar_b4_kaiwa.webp",
    "pages": 16,
    "kb": 258
  }
];
