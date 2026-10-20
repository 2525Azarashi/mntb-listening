# UI 変更記録（元に戻すとき用）

見た目を変えたら、ここに **いつ・どの画面・どのファイル・どう戻すか** を追記します（新しいものを上に）。
「イメージと違った」ときは、この記録の項目名を添えて「○○を戻して」と伝えてください。

---

## 2026-10-20 ホーム・対戦・ランキングの手直し（PR: fix/home-battle-ranking-polish）

前提：#55 で UI 刷新はいったん戻され、その後 #56〜#58 でホームの導線が整理された。今回はその **今の main の上に、指定の項目だけ** を入れた（ほかの見た目は今のまま）。

### ① ホーム：とびら君の足元の札
| 何を | どう変えた | ファイル |
|---|---|---|
| 「MY TOBIRA」 | 「マイとびら」に | `src/components/Home.tsx`（札の `<span className="my-tobira-tag">`）、`src/battle/ui/GrowthHomeStrip.tsx`（マイページ側の小見出し） |
| 名前とレベルの色が同化 | 名前＝紺の文字・クリーム地、レベル＝金のメダル（濃い茶の文字）に分けた。札の左右に小さな金の星 | `src/components/my-tobira-tag.css`（新規）／`Home.tsx` の先頭で読み込み |

**戻し方**：`Home.tsx` の札を `<span>MY TOBIRA <b>Lv.{…}</b></span>` に戻し、`import './my-tobira-tag.css';` の1行と `my-tobira-tag.css` を消す。`GrowthHomeStrip.tsx` の「マイとびら」を「MY TOBIRA」に戻す。

### ② 対戦：自分の名前
| 何を | どう変えた | ファイル |
|---|---|---|
| 自分のとびら君の名前がアカウント名（Google の名前＝本名のことが多い） | 設定したニックネームを出す | `src/battle/ui/BattleHome.tsx`（`resolveNickname()` を使う） |
| ニックネーム未設定のとき、対戦・ランキング・フレンドでアカウント名が送られていた | アカウント名には落とさず「名無しの化学者」に | `src/utils/leaderboard.ts` の `resolveNickname()` |

**戻し方**：`BattleHome.tsx` の `resolveNickname()` を `user.displayName || 'あなた'` に戻す。`leaderboard.ts` の最後の `return '名無しの化学者';` を `return sanitizeNickname(user.displayName || '', '名無しの化学者');` に戻す。
※ プライバシーのため、② は戻さないことをおすすめします。

### ③ 対戦：「正解で60点」などのタグ
| 何を | どう変えた | ファイル |
|---|---|---|
| 対戦画面の「正解で60点・速いほどボーナス・勝てば+10枚」 | 対戦画面から削除 | `src/battle/ui/BattleHome.tsx`（`arena-rule-chips` を削除） |
| 同じ3つ | 試合前のカウントダウン画面（紙と筆記用具を用意…）に小さな札で表示 | `src/battle/ui/BattleLiveParts.tsx`（`battle-ready-rules`）、`src/styles/game-dashboard.css`（末尾の札の見た目） |

**戻し方**：`BattleHome.tsx` に `<ul className="arena-rule-chips">…</ul>` を戻し（`Target`・`Coins` の import も）、`BattleLiveParts.tsx` の `battle-ready-rules` の1行と `game-dashboard.css` 末尾のブロックを消す。

### ④ ランキング（スマホの一覧を広く）
| 何を | どう変えた | ファイル |
|---|---|---|
| 下の「この範囲で○位・対戦へ」バー | 削除（対戦へは上の切替から行ける） | `src/components/Leaderboard.tsx`（`league-footer` を削除） |
| 見出しの「BATTLE LEAGUES」 | 削除 | `Leaderboard.tsx` |
| スマホの上の部品 | 見出し行と「ランキング／とびらバトル」の切替を1行に。自分のカード・シーズンの帯を低く。一覧の行も低く | `src/components/ranking.css`（末尾の「2026-10-20」のブロック） |
| 「もらえるもの」が左右に2回 | 右端の1回だけに | `Leaderboard.tsx`（`season-mine` はログイン時だけ）、`ranking.css` |

実測（一覧の高さ）：390×844 で約430px（約7人分）、320×568 で約180px（約3人分）。

### ⑤ ランキング：「ゴールドまで○○」のバー
| 何を | どう変えた | ファイル |
|---|---|---|
| 細い灰色のバー＋文字だけ | いまのリーグ色→次のリーグ色のグラデーション、両端にリーグ名の札、「あと○」を大きな数字で。つやの帯がゆっくり流れる（動きを減らす設定では止まる） | `Leaderboard.tsx`（`league-progress-rich` と `BAR_COLORS`）、`ranking.css` |

**④⑤の戻し方**：`ranking.css` の「2026-10-20」以降のブロックを消す。`Leaderboard.tsx` の `league-progress-rich` の部分を元の `<div className="league-progress"><progress …/><span>…まであと…</span></div>` に戻し、`BAR_COLORS` を消す。下のバーが必要なら `league-footer` を戻す。

### テスト
- `tests/homeBattleRankingPolish.test.ts`（新規）で上の①〜⑤が崩れていないかを確認。戻すときはこのテストも消す。
- `tests/revision.test.ts`：main で1件落ちていた（#58 でホームの「ランキングを見る」を外したのに、テストがホームにあることを求めていた）。入口が対戦画面の切替（`onRanking`）にあることを確かめる形に直した。
