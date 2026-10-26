# 英語リスニング版の告知動画（2026-10-26）

実際のアプリ（ビルド版・ゲスト・広告なし）を操作した画面録画だけで作っています（動画生成AIは使っていません）。
問題の英語は、録画中にアプリが実際に再生した音源（`public/listening_audio/`）を、録画 json に残した再生・停止の時刻どおりに重ねています。

## できあがり

| ファイル | 用途 | 大きさ | 長さ |
|---|---|---|---|
| `listening_reel_9x16.mp4` | Instagram リール | 1080×1920 | 約86秒 |
| `listening_story_9x16.mp4` | Instagram ストーリーズ（上下の UI 部分をあけてある） | 1080×1920 | 約28秒 |
| `listening_youtube_16x9.mp4` | YouTube（パソコン版中心・最後にスマホ版も並べて QR） | 1920×1080 | 約1分53秒 |

- H.264 / 30fps、AAC 48kHz・-14 LUFS（ピーク -1.5dBFS 前後）。英語が鳴る間は BGM が自動で下がる。
- 投稿文・概要欄・チャプターは `CAPTIONS.md`（**BGM のクレジットが必須**）。

## 構成（英単語版と同じ「1本の道」の形）

| 場面 | 中身 | BGM |
|---|---|---|
| 悩み | 「英語リスニング、聞き取れない。」流れていく英語・ねむるとびら君 | 夕凪 |
| 迷い | 「スクリプトを読んで理解」VS「とにかく何度も聞く」→ どう練習するのが正解？ | 夕凪 |
| 答え | 「共通テストと同じ形式で、全6大問。」135回分のカウンター（YouTube は9単元の内訳） | 誕生（曲が広がる所から） |
| 道のり | 「1問ずつ、こなすだけ。」解く → 聞き直す → 音読 → 対戦 | 風の列車 |
| STEP1 解く | 大問タブ（第1問A〜第6問B）→ 第3問 第1回 問1 を再生。英語の字幕は読まれた単語から光り、和訳つき → ③ One week → 正解 | 風の列車（英語の間は下がる） |
| STEP2 聞き直す | 解説で再生 → 読まれている単語が光る（YouTube は和訳と「聞き取りの決め手」まで） | 同上 |
| STEP3 音読 | 音読練習：強弱・アクセント・区切り・つながりの記号つきで聞く → 「音読する」→ いっしょに読む | 同上 |
| STEP4 対戦 | AI と対戦（英語リスニング・第3問・5問）：カウントダウン → START! → 聞き終えてから早押し → ラスト1問 → FINISH! → 勝利・レベルアップ | カナリアスキップ（START! にサビ） |
| しめ | 「『聞き取れた！』を、毎日ひとつずつ。」→ ロゴ | 誕生（後半） |

## 文言の根拠

- 全6大問・9単元・135回分（各単元14〜16回）・全554問：`src/data/englishListeningData.ts`（`getListeningStats()` と、各単元の `practiceProblems`＋`miniTest` を数えた値）。
- 読み上げ「前半2回・後半1回」：同ファイルの parts（前半（2回読み）／後半（1回読み））。
- 英語の字幕の単語の時刻：`public/read_along/listening_audio/el3_set1_q1.json`、和訳：`public/data/listeningTranslations.json`（アプリが解説で出す和訳と同じ）。
- 対戦：AI（マナボ（受験生））・英語リスニング第3問・5問。スマホは 357 vs 357（同点・解答時間の合計で勝ち）、録画どおり。AI 対戦はレートが動かない練習用。
- 「必ず聞き取れる」「点数が上がる」「No.1」などの断定はしていません。

## 音の権利

| 音 | 出どころ | 条件 |
|---|---|---|
| 誕生 | `public/tanjou.mp3`（Suno 有料プランで作成） | 商用可 |
| 夕凪・風の列車 | 創作堂さくら紅葉 https://yukizakura.net/ | 商用・加工可。**配布元名と URL の記載が必須** |
| カナリアスキップ | まんぼう二等兵／OpenTracks | 商用・加工可・クレジット任意（書いている）。Content ID 登録禁止 |
| 効果音 | `public/sfx/battle/*.mp3`（数式で作った音） | 表記不要 |
| 問題の英語音声 | `public/listening_audio/`（アプリ自身の音源） | アプリの素材 |

## 作り直し方

```sh
NODE_OPTIONS=--max-old-space-size=2500 npx vite build --outDir .tmpwork/dist_l
npx vite preview --outDir .tmpwork/dist_l --port 4175 --host 0.0.0.0 &
# 録画（スマホ・パソコン）。対戦は1回 約3分（音声を聞き終えてから答えるため）
APP_URL=http://localhost:4175 python3 store-assets/_tools/record_listening.py store-assets/_footage/lrec_ph units q3 studio battle
REC_DEVICE=pc APP_URL=http://localhost:4175 python3 store-assets/_tools/record_listening.py store-assets/_footage/lrec_pc
# 編集（--sheet で静止画の一覧、FRAMES=秒,秒 で指定時刻、--draft で速い下書き、--audio-only で音だけ）
python3 store-assets/_tools/promo_listening.py .tmpwork/lout reel story youtube
```

- 録り直したら、`promo_listening.py` 先頭の時刻（`Q_OK`・対戦の `B`／`Bp` の start・ok・finish）を `measure.py` で測り直してください。音声の時刻は json の `audio` から自動で入ります。
- 対戦の問題はランダムなので、録り直すと出る問題・点数が変わります（README の点数も直す）。
