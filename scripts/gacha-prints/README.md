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
- `kyotsu_mock/figs.py`＋`kyotsu_mock/assets/img/*.jpg`：受け取った画像（リスニングの絵34・地図4・リーディングの図24）を PDF に組み込む設定。4枚組の絵は枠を検出して切り出し、本番と同じく各絵の下中央に①〜④。地図は元の点線の丸を消し、同じ位置・大きさで丸数字を描く。リーディングの図は `R_PLACE`（回・大問・枠の番号・位置・幅）。
- **ElevenLabs（Eleven v4）で音声を作る**：`kyotsu_mock/build_orders_el.py` → `.tmpwork/kyotsu_mock_elevenlabs_v4.pdf`（声のキャスト12役・読み方のルール・全120トラックの台本）。一括作成は `kyotsu_mock/make_audio_el.py`（Text to Dialogue API・`eleven_v4`。`ELEVENLABS_API_KEY` と `el_voices.json`（役名→voice_id、`el_voices.example.json` をコピー・git 管理外）が必要。`--dry-run` は課金なし）。生成済みの部品は `.tmpwork/el_cache/` に残り、作り直しでは再生成しない。
- リーディングの英文量は本番（約5,600語）に合わせて増量済み（各回 約5,000〜5,400語）。図に描かれた内容・正解は変えていない。図は全29枚そろった（受け取り24枚＋生成5枚：r4_6_indigo_dye / r4_7_heat_island / r5_2_sunfold / r5_3_calligraphy / r5_6_feel_music）。

### ピックアップの「中身を少し見る」画像（2026-10-27）

`python3 scripts/gacha-prints/build-previews.py` で、LR 10種＋厳選UR（`GachaParts.tsx` の `FEATURED_UR_IDS`）10種の
2ページ目と真ん中のページを、**上半分だけ・幅360px・下はぼかし**の webp にする → `public/prints/previews/`。
一覧は `src/data/gachaPreviews.generated.ts` に自動で書き出す。厳選URを入れ替えたら、このスクリプトを流し直す
（`tests/gachaPickup.test.ts` が「厳選URと一致・実物あり・1枚30KB以下・余分なファイルなし」を確かめる）。

### LR リスニングの音声（第1回のみ・2026-10-27）

利用者が ElevenLabs v4 で作った6本（`audio_sources/commercial/elevenlabs_2026-10-26_kyotsu_l1/`）を、無音の中ほどで
問題ごとの24トラックに切って `public/prints/kyotsu_assets/audio/kyotsu_l1_q*.mp3` に置いた（区切りは同フォルダの `split_manifest.json`）。
第1問・第2問は4秒あけて2回つなぐ。対応表は `src/data/kyotsuMockAudio.ts`。第2回〜第5回は音声が届いたら同じ形で足す。
**`listening_audio_ledger.json`（374本）には入れない**（別教材）。
