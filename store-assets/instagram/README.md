# Instagram 用動画（実際のアプリ操作の画面録画）

動画生成AIは使っていません。本物のアプリ（ビルド版）をスマホ実寸で操作し、その画面をそのまま録画して編集しています。

## できあがり

| ファイル | 用途 | 大きさ | 長さ |
|---|---|---|---|
| `instagram_story_9x16.mp4` | ストーリーズ（予告） | 1080×1920（9:16） | 約22秒 |
| `instagram_post_reel_9x16.mp4` | 投稿（リール）：使い方・操作の流れ | 1080×1920（9:16） | 約50秒 |
| `instagram_post_feed_4x5.mp4` | 投稿（フィード）：上と同じ内容を 4:5 で | 1080×1350（4:5） | 約50秒 |

- 映像は H.264 / 30fps、音声は AAC 48kHz・約 -17 LUFS（ピーク -1.4dBFS）です。
- ストーリーズは上下 250px ほどが Instagram のボタンで隠れるため、文字と画面は真ん中に寄せています。
- リールのサムネイル（カバー）は、最初の「共通テストの英語リスニング」の画面か、アプリ内で選んでください。

## 構成

**ストーリー（予告・約22秒）**
1. ロゴ＋「共通テストの英語リスニング」
2. 問題の音声を再生（本物の音源）→「本番形式の音声で、聞き取りを鍛える」
3. 答える → 正解！ → 解説（強弱・和訳）「解いた直後に、採点と解説」
4. AI と対戦（カウントダウン → 早押し4択 → FINISH!）「AIと対戦して、早押しで競う」
5. 締め：「聞き取れた！」を、毎日ひとつずつ。／App Store・Google Play で「マナトビ」と検索／無料（広告表示あり）

**投稿（使い方・約50秒）**
STEP 1 大問を選ぶ → STEP 2 音声を聞いて4択 → STEP 3 その場で採点・コイン → STEP 4 解説 → STEP 5 復習ノートに自動で
→ BATTLE（AI・友だちと対戦、早押し4択）→ MISSION（毎日のミッション）→ MY PAGE（とびら君・きせかえ）→ 締め

## 画面・文言の根拠（実装で確認済み）
- 「全6大問」… `getListeningStats().sections = 6`（第1〜6問。9単元・135回・554小問）
- 「音声を聞いて」… 実際に「再生」を押した時刻に、その問題の音源 `public/listening_audio/el1A_set1_q1.mp3` を重ねています
- 「その場で採点。正解でコインも」… 解答直後の「正解！」と得点・ミッション達成の表示（録画どおり）
- 「強弱・和訳・語句」… 解説画面の強弱表示・和訳・語句（録画どおり）
- 「復習ノートに自動で」… わざと1問まちがえた結果、復習ノートに1問入ったところを録画（作り物のデータは入れていません）
- 「AIとも、友だちとも」… 対戦のモード（AIと対戦・フレンド・全国対戦）。録画は AI 対戦（英文法・5問・マナボ（受験生））
- 「毎日のミッション」… 対戦ミッション 3つ＋ボーナス 5つ（毎日入れかわり）
- 「無料（広告表示あり）」… 課金なし・広告あり（`docs/APP_STORE.md`, `src/utils/adConfig.ts`）
- 「No.1」「必ず点が上がる」などの断定表現は使っていません。

## 映っているもの
- ゲスト（未ログイン）の状態。名前は「ゲスト」で、実在の人の名前・メール・ランキングは映っていません。
- 広告は録画のために止めています（`?no_ads=1`）。実際のアプリでは広告が出ます（締めの画面に「広告表示あり」と書いています）。
- タップした場所の丸い印は、録画用に重ねた表示です（アプリの見た目は変えていません）。

## 音の権利
| 音 | 出どころ | 動画での利用 |
|---|---|---|
| BGM「カナリアスキップ」 | まんぼう二等兵／OpenTracks（旧DOVA-SYNDROME）https://opentracks.com/bgm/detail/7312 | 音源利用ライセンス（2026-10-16 確認）：Instagram などのオンライン動画の**背景音楽**として商用利用可・加工可・クレジット不要。音源だけの再配布・AI学習は禁止 |
| タップ音・正解音・カウントダウン・START・FINISH など | `public/sfx/battle/*.mp3`（運営が数式で一から作った音） | 商用・動画OK・表記不要（`public/sfx/battle/LICENSE_SFX.md`） |
| 問題の英語音声 | アプリの音源 `public/listening_audio/` | アプリ自身の素材 |

※ Instagram でアプリ内の曲を付けたい場合は、Instagram の編集画面で元の音量を下げてから曲を足してください。

## 作り直し方
```sh
# 1) ビルドして、ビルド版を 4173 番で開く（メモリが少ない環境では swap が必要。docs/BUILD.md）
npx vite build --outDir .tmpwork/dist && npx vite preview --outDir .tmpwork/dist --port 4173 &
# 2) 実際に操作して場面ごとに録画（2倍密度 860×1864・30fps。.tmpwork/scenes2 に mp4 と時刻の json ができる）
python3 store-assets/_tools/record_scenes.py .tmpwork/scenes2
# 3) 編集して書き出し（見出し・スマホ枠・効果音・BGM・音量そろえ）
MNTB_ROOT=$PWD python3 store-assets/_tools/edit_instagram.py .tmpwork/scenes2 store-assets/instagram
#    1本だけ：…edit_instagram.py .tmpwork/scenes2 store-assets/instagram story   （story / post / post45）
```
- 操作の手順は `record_scenes.py` の `scene_*`、見出し・切り出す時刻は `edit_instagram.py` の `POST` / `STORY` です。
- 対戦の正解は `grammar_answers.json`（対戦の出題プールから作った「問題文→正解」の表）で選んでいます。

## ElevenLabs で作る場合（任意）
ナレーションや別の BGM を ElevenLabs で作りたいときのプロンプトです（この動画は作らなくても完成しています）。
→ `ELEVENLABS_PROMPTS.md`
