# scripts/ の案内

アプリ本体（`src/`）ではなく、**データを作る・確かめる・取り込む**ための道具の置き場。
アプリの実行中には使われない。どれもリポジトリの一番上（`/home/user/mntb` など）で実行する。

## よく使う（package.json から呼ぶ）

| 道具 | 呼び方 | 何をする |
|---|---|---|
| `pr/` | `npm run pr:create` / `pr:check` / `pr:sync` | PR を作る（main と他の PR を取り込み → 競合チェック → 型チェック → push）。**素の `gh pr create` は使わない** |
| `check-release.mjs` | `npm run build` の最初 | 本番ビルドがゲスト専用版になっていないか確かめる |
| `release-guard.sh` | `npm run release:guard` | ストアに出すビルドの元コミットを確かめる |
| `check-firebase-setup.mjs` | `npm run firebase:check` | Firebase の設定を読み取りだけで確かめる |
| `gen-chapter-index.mts` | `npm run gen:index` | 章の軽い索引を作る |
| `gen-battle-pool.mts` | `npm run gen:battle-pool` | 対戦の出題プールを作る |
| `gen-listening-vocabulary.mts` | `npm run gen:vocabulary` | リスニングの単語一覧を作る |
| `listening-audio.mts` | `npm run audio:status` など | リスニング音源の一覧・検査・取り込み（`docs/LISTENING_AUDIO_REPLACE.md`） |
| `purge-legacy-listening-audio.mjs` | `npm run audio:purge-legacy` | 旧音源が残っていないか確かめる |

## フォルダ

| フォルダ | 中身 |
|---|---|
| `listening-data/` | 共通テスト・リスニングの問題データづくり（PDF → JSON → 選択肢の並べ替え → `src/data/englishListening*.ts` の生成）、第2問の図・音声の検査、録音用台本の PDF |
| `icons/` | アプリアイコン・Android の起動画面の画像を作る／差し替える |
| `assets/` | 上の道具が使う元画像（アイコンの原画、ロゴ消しの型、第1問Bの元画像） |
| `data/` | 道具が読み書きする中間データ（`q2_parsed.json` など。アプリは読まない） |
| `gacha-prints/` | ガチャの UR 学習プリント（PDF）づくり。手順は中の `README.md` |
| `readalong/` | 音読・ディクテーション用の単語ごとの時刻づくり |
| `vocab-audio/` | 英単語の読み上げ原稿づくりと、まとめ録り音声の切り分け |
| `listening-translation/` | リスニングの和訳づくり |
| `firefly-kit/` | Adobe Firefly 用の動画キットづくり |
| `tobira-motion/` | とびら君のモーション動画の取り込み |
| `android-range-check/` | Android SDK なしで `RangeAwareWebViewClient.java` を検査する |

## その他（一番上に置いたまま）

| 道具 | 何をする |
|---|---|
| `build.sh` | ビルドの起動ラッパー（メモリ不足のときに対処法を出す。`docs/BUILD.md`） |
| `kasa-diff.sh` | カサニマロに送る差分 ZIP を作る |
| `listening-split.py` | まとめ録りの音声を問題ごとに切る（`docs/LISTENING_AUDIO_REPLACE.md`） |
| `export-listening-audio-prompts.mts` | 録音の指示書を書き出す（有料 API は呼ばない） |

## 新しい道具を足すとき

- 用途が上のフォルダに合うならそこへ。一番上には「package.json から呼ぶもの」だけを増やす。
- プロジェクトの場所は `Path(__file__).resolve().parents[N]`（Python）や `git rev-parse --show-toplevel`（shell）で決め、置き場所を変えたら N も直す。
- `.mts` は `npm run lint:scripts` で型チェックされる。
