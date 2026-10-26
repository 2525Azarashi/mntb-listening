# TOEIC 拡張 設計書（2026-10-25 たたき台）

マナトビで共通テストを扱っているのと同じ流れ（**パート別演習 → 模試 → 復習 → 対戦・ガチャ**）で、TOEIC® L&R を扱う。
今回作ったのは**型と骨組みだけ**（`src/features/toeic/`）。画面と問題データはまだない。

## 1. 共通テストとの対応

| 共通テスト（既存） | TOEIC（追加） | 共通化できる部品 |
|---|---|---|
| 大問別演習（第1問〜第6問） | Part 1〜7 別演習 | Quiz / 解説画面 / 下のバー |
| 本番形式の模試 | 通し200問の模試（L45分・R75分） | タイマー・解答用紙 |
| リスニング素材（図・カルーセル） | Part 1 の写真・Part 3/4 の図表 | ListeningMaterials / FigureCarousel |
| 英文解釈（4択内容一致・全訳） | Part 7（シングル/ダブル/トリプル） | ReadingQuiz の全訳 `<details>` |
| 英単語・英熟語 | TOEIC 単語（スコア帯別） | VocabQuiz（データだけ差し替え） |
| 復習（missed） | 復習（missed + 分野別の弱点） | 復習画面 |
| ガチャ景品（UR/LR の PDF） | TOEIC 模試 PDF を景品に | gachaPrints（category を追加） |

## 2. データの単位：「セット」

- 写真・音声・本文を共有する設問のまとまり＝**セット**（`ToeicSet`）。Part 1/2/5 は設問1つのセットとして持つ。
- `part` で型が分かれる判別共用体なので、`switch (set.part)` で表示を切り替えれば、型で書き漏れが分かる。
- 模試（`ToeicMockExam`）はセットIDを並べるだけ → 同じセットをパート別演習と模試の両方で使い回せる。
- ID 規約：`toeic-p{part}-{3桁}`、設問は `{setId}-q{n}`（テンプレートリテラル型で強制）。

## 3. ファイル

| ファイル | 中身 |
|---|---|
| `src/features/toeic/types.ts` | 型すべて（素材・設問・セット・模試・記録・単語） |
| `src/features/toeic/format.ts` | 公式形式（パートごとの問題番号・選択肢数・本番のセット構成） |
| `src/features/toeic/validate.ts` | 構造チェック（設問数・選択肢・空所数・全訳の段落数・模試の構成） |
| `src/features/toeic/catalog.ts` | 学習カタログ用カード（`StudyContent` と同じ形）・`openStudyContent` に足す action |
| `src/features/toeic/samples.ts` | 書き方見本（Part 2・Part 5 を1つずつ） |

## 4. 本体（マナトビ）へ組み込む手順

1. ✅ `src/features/toeic/` に型・形式・構造チェックを置いた（React/Firebase に依存しない。このPR）。
2. `StudyAction` に `ToeicStudyAction` を足し、`STUDY_CATALOG` の英語に `TOEIC_STUDY_CONTENTS` を並べる（「NEW」付き）。
3. `openStudyContent` に `kind: 'toeic' | 'toeicVocab'` を追加し、`appState = 'toeic'` へ。
4. `ToeicHome`（タブ：パート別 / 模試 / 単語 / 復習 / スコア）を遅延読み込み（lazy）で追加。
5. 演習は既存の `Quiz` に `ToeicSet` → `practiceProblems` の変換を挟んで再利用する（変換関数は次の段階で作る）。
6. 記録は Firestore の `users/{uid}/toeic`（`ToeicProgress`）。`userDataSyncCore` の merge に missed / mastered の和集合を足す。
7. ✅ `tests/toeicTypes.test.ts`（このPR）。問題データが入ったら `tests/toeicData.test.ts` で全セットに `validateSet`、全模試に `validateMock` をかける。

## 5. 決めたこと

- **スコア予想は「目安」**：公式の換算表は公開されていないので、`approximate: true` を型で必須にして、画面にも必ず「目安」と出す。
- **Part 1/2 の選択肢**：本番では印刷されないため、演習中は音声だけで出し、解説で英文と訳を見せる（`audioOnlyChoices`）。
- **音声**：ファイルを収録するまでは台本（`ScriptLine[]`）を TTS で読む。4つの発音（US/UK/CA/AU）を台本の行ごとに持たせて、ElevenLabs で声を割り当てる。
- **問題はすべて自作**：`source.author` と確認者を記録。公式問題の転載はしない。
- **商標表記**：「TOEIC is a registered trademark of ETS. This product is not endorsed or approved by ETS.」を画面と PDF に入れる。

## 6. まだ決めていないこと（要相談）

- 対象ユーザー：高校生・大学生（就活の600〜730）を主にするか、社会人まで広げるか → 単語のスコア帯と初期の難易度が変わる。
- 対戦モードに入れるパート：Part 2・Part 5 は1問が短いので対戦に向く。Part 3/4/7 は長すぎるので対戦には入れない案。
- ガチャ：TOEIC 模試 PDF を UR/LR のどちらにするか、`GachaPrintDef.category` に `'TOEIC模試'` を足すか。
- 通学中に解く「ミニ模試」（10分／30分）の配分。

## 7. 次の段階

1. 各パート 5 セットずつ問題を作る → `validate` を通す
2. `ToeicSet` → `Quiz` の変換関数と、Part 1（写真）・Part 6（空所の表示）の部品
3. ToeicHome の画面（320×568 で縦スクロールなし、文字12px以上、タップ領域44px以上）
4. 模試1回分（200問）＋ PDF 化してガチャ景品へ
