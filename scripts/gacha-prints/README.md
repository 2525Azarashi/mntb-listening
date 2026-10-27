# UR 学習プリントの作り直し（英語・理科・化学 無機・数学）

アプリの英文法・単語帳のデータから、ガチャの UR 学習プリント（PDF＋サムネイル）を作ります。

```bash
# 1) 英文法の素データ（手書きの問題・解説）を書き出す
mkdir -p .tmpwork/eg && cp src/data/egProblems*.ts .tmpwork/eg/
sed 's#^export function buildEgSet(meta: EgSetMeta, items: EgItem\[\]): GrammarProblem {#&\n  (globalThis as any).__egCapture?.(meta, items);#' src/data/englishGrammarKit.ts > .tmpwork/eg/englishGrammarKit.ts
cp scripts/gacha-prints/dump-grammar.mts .tmpwork/eg/dump.mts && npx tsx .tmpwork/eg/dump.mts
# 2) PDF を作る（reportlab・pdftoppm・Pillow・IPAゴシックが必要）
python3 scripts/gacha-prints/build-grammar-ur.py
python3 scripts/gacha-prints/build-vocab-ur.py
# 理科3冊・化学 無機・数学 総まとめ（★教科データはアプリから外したので、元のリポジトリから src/data と src/features/rika を一時的に戻してから実行★）
npx tsx scripts/gacha-prints/dump-science.mts
python3 scripts/gacha-prints/build-science-ur.py            # 一部だけなら: ... inorganic math rika1 rika2 rika3
# 3) src/data/gachaPrints.generated.ts の pages / kb を実物に合わせる（tests/gachaPrintsQuality.test.ts が検査）
```

- 問題文・選択肢・解説は **アプリのデータのまま**。並べ替えるのは選択肢の順番だけ（正解位置を①〜④に均等にするため）で、解説中の「② の〜は」の番号も同じ対応表で付け替えます。
- 品質の下限は `tests/gachaPrintsQuality.test.ts`（100問すべてに解説・正解位置25問ずつ・4択の答えあり）。
- 理科・化学・数学は `ur_common.py`（表紙・問題・解答用紙・答えの一覧・解説・要点・自己採点表）を共通で使う。IPAゴシックに無い下付き・上付き数字や ≤ ≥ は DejaVu Sans で描く。

## UR「完全版」の本（2026-10-24）

ガチャの UR（大当たり）は「その一冊で完成する本」だけ。単元プリント・100語テストは SR。

```bash
python3 scripts/gacha-prints/build-vocab-book.py        # 英単語 Lv1・Lv2・Lv3+4、英熟語（アプリの単語帳の全語）
python3 scripts/gacha-prints/build-reading-mock.py      # 共通テスト英語リーディング 大問別演習 第1〜3回（問題データ reading_mock_a/b1/b2/c1/c2/c3.py・解き方 reading_guide.py）
npx tsx scripts/gacha-prints/dump-listening.ts /tmp/listening.json && python3 scripts/gacha-prints/build-listening-book.py  # 共通テスト英語リスニング 大問別演習（アプリの問題・音声をそのまま使う。QR＝https://mntb-listening.vercel.app の mp3）
python3 scripts/gacha-prints/build-analysis-book.py     # 共通テスト全科目 出題分析（データ analysis_*.py・出典つき）
```
- 共通レイアウトは `book_common.py`（紺と金の表紙・帯・囲み）。
- 作り直したら `src/data/gachaPrints.generated.ts` の pages / kb を合わせる（`tests/gachaDeluxe.test.ts` が検査）。
- リーディングは第1回（reading_mock_a.py）・第2回（reading_mock_b1.py＋b2.py）。第3回は同じ形のデータを足して BOOKS に1行追加。

## LR：共通テスト 英語 予想問題（2026-10-24）

```bash
# reportlab・pdftoppm・Pillow・IPAゴシック/IPA明朝（fonts-ipafont-gothic / fonts-ipafont-mincho）が必要
python3 scripts/gacha-prints/kyotsu_mock/build.py        # 5回分すべて（一部だけなら: build.py 2 4）
# → public/prints/print_lr_kyotsu_{r,l}_{n}.pdf と thumbs、.tmpwork/kyotsu-mock.json（ページ数・KB）
# src/data/kyotsuMockPrints.ts の pages / kb を .tmpwork/kyotsu-mock.json に合わせる（tests/kyotsuMockPrints.test.ts が検査）
```

- 問題データは `setN_r1.py`・`setN_r2.py`（リーディング第1〜4問・第5〜8問）、`setN_l.py`（リスニング）。描画は `render.py`、組み立ては `build.py`。
- `build.py` が毎回検査：大問数（R8・L6）・解答数（R44・L37）・各大問の配点・合計100点。
- 見た目は本番の問題冊子と同じ白黒（明朝・四角囲みの解答番号・大問ごとに改ページ）。色は使わない。

### 共通テスト予想問題の素材（音声・イラスト・図）の制作指示書

- `kyotsu_mock/assets_plan.py`：まだ無い素材の一覧（リスニング120トラックの台本と声の割り当て／4択の絵34／地図4／リーディングの図29）。問題データから自動で作る。
- `kyotsu_mock/build_orders.py`：ChatGPT に貼るプロンプト集＋全台本を1冊の PDF に（`.tmpwork/kyotsu_mock_seisaku_shijisho.pdf`）。
- `kyotsu_mock/make_audio.py`：OpenAI TTS（gpt-4o-mini-tts）でリスニング音声を作る。`--dry-run` は課金なしで台本だけ表示。実行者の `OPENAI_API_KEY` に課金。
- 素材を受け取ったら `public/prints/kyotsu_assets/{img,audio}/` に置き、問題 PDF の `［絵］` 枠を差し替える（未対応・次の作業）。

## 熟語＋英文解釈 小テスト（B4横・B5縦2面・問題と解答を同じ PDF・白黒）2026-10-27

```bash
npx tsx scripts/gacha-prints/idiom_reading/dump.ts && python3 scripts/gacha-prints/idiom_reading/build.py
# → .tmpwork/idiom_reading/熟語英文解釈_{基礎,標準,発展}_第01-12回.pdf（各12回・B4 24ページ）
```
- 左：英熟語（ilv1）をアプリの単語帳と同じ順に（英→日・書く）。右：**上に熟語のつづき → 下に英文解釈1題**（熟語は 左上→左下→右上 と続く）。
- コース：基礎＝英文解釈レベル1、標準＝レベル2、発展＝レベル3。熟語は通し番号（基礎 1〜479 → 標準 480〜939 → 発展 940〜1388）。
- 白黒印刷用：熟語の答え＝太字、設問の正解＝太字＋下線、本文の根拠＝波下線（`<u color="#010101">`）、ポイント＝太字。赤は使わない。
- 本文が長い回は右上の熟語を減らし（最低4語）、それでも入らなければ文字を少し小さくする（最小0.85倍）。
- 共通部品は `scripts/gacha-prints/b4common.py`（フォント・波下線・英日混在・見出し帯）。

## 英文法 4択 B4プリント（アプリと同じ問題・同じ順）2026-10-27

```bash
npx tsx scripts/gacha-prints/idiom_reading/dump.ts && python3 scripts/gacha-prints/grammar_b4/build.py
# → .tmpwork/idiom_reading/英文法_4択_第1-16章.pdf（80回分・B4 80ページ）
```
- アプリの英文法 第1〜16章（729問）を、章→問題番号の順・同じ選択肢の並びで。1面（B5）＝1回分（7〜10問、章をまたがない）。見出しは「時制（1）」「時制（2）」…
- 1枚目＝左右2回分の問題、2枚目＝同じ配置で解答。解説はアプリより短く：正解の英文（答えの部分を太字＋下線）・和訳・ポイント1行。
