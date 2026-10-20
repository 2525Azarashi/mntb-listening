# UI刷新（2026-10-19）変更記録 — 元に戻すとき用

このPRは大きな見た目の変更です。「イメージと違った」ときに**全部まとめて**、または**画面ごとに**元へ戻せるよう、どこを変えたかをここに残します。

## 1. 全部まとめて元に戻す

マージ後、GitHub の PR 画面の「Revert」ボタンを押すのがいちばん簡単です（戻すPRが自動でできます）。

コマンドでやる場合（マージコミットの ID を `<M>` とする）：

```bash
git checkout genspark_ai_developer && git pull
git revert -m 1 <M>      # このPRの変更だけを打ち消すコミットを作る
git push
```

注意：このPRには **#46/#48（低スペック60fps・構造リファクタ C-01〜C-22）の載せ直し** も入っています。
「UIだけ戻して #46/#48 は残したい」ときは、下の「2. UIだけ戻す」を使ってください。

## 2. UIだけ戻す（#46/#48 は残す）

UI刷新は、このPRの中の **「merge: UI刷新…」というマージコミット** にまとまっています。

```bash
git log --oneline --merges -5          # 「merge: UI刷新（ホーム・マイページ…）」の ID を探す → <U>
git revert -m 1 <U>
```

## 3. 画面ごとに戻す

UI刷新前の状態は `a00fe1d`（UI刷新の元になったコミット）にあります。
ただし #46/#48 のリファクタで中身が移ったファイルがあるため、**ファイルを丸ごと a00fe1d に戻すとリファクタも消えます**。
画面ごとに戻すときは、下の「変えたところ」を見て該当箇所だけ戻すか、このファイルの一覧を添えて「○○画面だけ戻して」と依頼してください。

| 画面 | 主なファイル | 戻すとどうなるか |
|---|---|---|
| ホーム | `src/components/Home.tsx`、`src/components/home/*`（新規5ファイル）、`src/data/tobiraMood.ts`、`src/components/TobiraBuddy.tsx`、`src/battle/ui/GrowthHomeStrip.tsx` | 入口が約15個の旧ホームに戻る |
| PCサイドバーのとびら君 | `src/components/ui/SidebarBuddy.tsx`（新規）、`src/components/ui/BottomNavigation.tsx`、`src/styles/nav.css`、`src/App.tsx`（footer） | サイドバー下が空に戻る |
| マイページ・ショップ | `src/components/GrowthHub.tsx`、`src/components/growth-hub.css`、`src/components/MyCollection.tsx` | 「部位ごとに着がえる」一覧と保管の注意書きが戻る |
| 設定 | `src/components/ProfileModal.tsx`、`src/components/profile-settings.css`、`src/features/account/AccountSafetySection.tsx`、`src/ads/adConfig.ts` | 説明文・MY ACCOUNT・設定画面の広告が戻る |
| 対戦 | `src/battle/ui/BattleHome.tsx`、`src/battle/ui/battle-lobby.css`、`src/battle/ui/BattleLiveParts.tsx`、`BattleLiveStage.tsx`、`BattleResultLive.tsx` | 「ホームへ」「だれが来る？」・配点チップ・絵文字が戻る |
| ランキング | `src/components/Leaderboard.tsx`、`src/components/ranking.css`、`src/App.tsx`（戻る先＝対戦） | BATTLE LEAGUES・下の「対戦へ」バーが戻る |
| ガチャ | `src/components/GachaRoom.tsx`、`src/components/gacha/GachaCollectionModal.tsx`、`src/components/gacha.css`、`src/styles/system.css`（UR王冠のSVG） | 説明文・長い提供割合の文章・👑が戻る |
| 学習（復習・記録） | `src/components/StudyHub.tsx`、`src/App.tsx`（onStudyRecord / onRetry） | 「記録」タブがなくなる |
| 演出 | `src/components/ui/DoorTransition.tsx`・`door-transition.css`（扉の切り替え）、`src/components/ScreenStatus.tsx`・`screen-loading.css`（読み込みの扉）、`src/components/MissionToast.tsx`・`src/battle/ui/BattleMissions.tsx`（コインが飛ぶ） | それぞれの演出が消える |
| 絵文字の削除 | `src/utils/explanationFormat.ts`、`src/components/DoorMascot.tsx` | 💡⚠️などが戻る |

**演出だけ止めたい**ときのいちばん小さな変更：
- 扉のページ切り替え：`src/App.tsx` の `<DoorTransition screen={appState} />` を1行消す
- 復習カードの吸い込み・XPの火花：`src/components/home/home-v2.css` の該当ブロックを消す
- 見た目の「やわらかい影」：`src/components/home/home-v2.css` の冒頭（`--hv-*` 変数と `box-shadow: 0 4px 0 var(--lift)`）

## 4. 変えたところ（画面ごと）

### ホーム
- 入口を整理：左右の4ボタン・下のチップ・「学びの扉」を削除。**演習／対戦の2本柱**＋**「復習・記録」「ミッション」「ラッシュ」**の1段に。
  - きせかえ・称号・ショップ → マイページへ
  - ランキング → 対戦画面とPCの右列へ
  - 使い方・学びの扉 → 設定のヘルプ欄へ
- 「MY TOBIRA」→「マイとびら Lv.N」。コインは数字を先に・折り返さない表示。
- 共通テストまでの日数：スマホは右上の札、PCは右列の大きな表示（回転する数字＋90個の点＋2次まで）。残り30日・7日で色が強まり、とびら君のセリフも変わる。
- 時間帯で空の色が変わる（朝・昼・夕・夜）。ステージに小さな丸いステッカー。
- PCは3列（左＝今日の積み重ね、中＝ステージと主ボタン、右＝日数・ミッション・ランク）。ロゴはサイドバーの1つだけ。
- 見た目：紺の太枠とずらした影をやめ、**ボタン色ごとのやわらかい下影＋紙色の枠**に統一。
- 演出：吹き出しのポップ、扉が順に開く、XPバーの弾み＋火花、復習カードの吸い込み（すべて動きを減らす設定では止まる）。

### マイページ・ショップ
- 「部位ごとに着がえる」一覧を削除し、きせかえ／称号／ショップの3つの入口に。
- タブ：マイページ／きせかえ／称号／ショップ／マイPDF。
- ショップ：保管の注意書きを削除、上部の日よけ風の飾り＋方眼の背景、ガチャとの違いは1行に。

### 設定
- 削除：MY ACCOUNT、名前の説明、志望校〜非公開の注意、BGM「学習中〜OFF」の説明。
- 「対戦で相手に見えるカード」を押すとマイページへ。
- ヘルプ欄に「アプリの使い方」「学びの扉（開発者の想い）」。利用規約などのリンクは同じ欄に並べた（左上に固めない）。
- 設定画面には広告を出さない。PCは列ごとにスクロール。スマホは保存バーと下の間のすき間をなくした。

### 対戦
- 削除：「ホームへ」「だれが来る？」、配点チップ（正解で60点など）→ カウントダウン画面へ移動。
- 表示名を設定のニックネームにそろえた。
- スマホ：AIを横長1枚＋フレンド・全国を同じ大きさで2枚、サブタイトルは非表示。低い画面ではフレンドの2ボタンを横並びにして1画面に収めた。
- 「その他」にランキングの入口。
- 対戦中・結果の絵文字を記号や点に置き換え。

### ランキング
- 削除：BATTLE LEAGUES、下の「この範囲で1位・対戦へ」バー。
- 次のリーグまでのバーを、リーグ色の札＋グラデーション＋「あと○」の大きな数字に。
- シーズン報酬（もらえるもの）は中身だけスクロール。「もらえるもの」が2回出ていたのを1回に。
- 戻るボタンの行き先は対戦画面。

### ガチャ
- 削除：「コインでランダム〜ショップへ」。
- UR の王冠・SR の星を絵文字から SVG に（Apple の絵文字を使わない）。
- 提供割合：長い文章 → レア度4つの表＋要点4行＋「ショップとの違い・プリントについて」（たたみ）。数字は抽選表の値のまま。
- コレクションの小さい文字を12pxに。PCの所持コインの位置ずれ、低い画面の空白を修正。
- **景品（public/prints/*、gachaPrints.generated.ts、GACHA_PRINTS、LEVEL_PRINTS、scripts/gacha-prints/*）は一切変更していない。**

### 学習
- 「復習・記録」から開く学習ハブに「記録」タブ（学習記録をそのまま表示）。

### 共通の演出
- 主要画面どうしの移動で扉が左右に開く（0.36秒・演習と解説の間では出さない）。
- 読み込み中に小さな扉の絵。
- コインが飛ぶ演出を宝箱・まとめて受け取るにも。

## 5. マージ時に手を入れたところ（#46/#48 との合わせ込み）
- ガチャの提供割合ダイアログは #46 で `src/components/gacha/GachaCollectionModal.tsx` に移っていたため、UI刷新の変更をそちらへ移した。
- `tests/vocabRangeQuiz.test.ts` は両方に同じ修正があったので #48 側を採用。
- ランキングのバーのつや：#46 の低スペック規則（無限アニメは transform/opacity だけ）に合わせ、background-position → transform に変更。
