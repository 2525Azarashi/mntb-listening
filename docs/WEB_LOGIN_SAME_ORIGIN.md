# Web 版ログインを「同じドメイン」で行う設定（2026-10-22）

## 何が起きていたか
Web 版（Vercel）で Google ログインを押すと、ポップアップで Google の画面までは進むのに、
アプリ側が **「連携中…」のまま止まり、アカウントに入れない**。

- ログインの結果を受け取る画面（`/__/auth/handler`）が **別ドメイン**（`mntb-listening.firebaseapp.com`）にある
- Safari（ITP）や最近の Chrome は「別サイトの保存領域を分ける」ため、その結果がアプリのページに戻らない
- 本番を自動ブラウザで確かめると、`Cross-Origin-Opener-Policy ... window.closed` の警告が出て、画面は「連携中…」のまま

Firebase 公式の推奨（signInWithRedirect best practices の「方法3」）は、
**`/__/auth/*` を自分のドメインから firebaseapp.com へ中継し、authDomain を自分のドメインにする**こと。
これでログインの往復が同じドメインで完結し、どのブラウザでも結果が戻る。

## このPRで入れたもの（コード側。すでに入っている）
| 何を | どう | ファイル |
|---|---|---|
| `/__/auth/*` と `/__/firebase/*` を中継 | Vercel の rewrite で `https://mntb-listening.firebaseapp.com/__/...` へ。SPA の書き換えより先に置き、SPA 側は `__/` を除外 | `vercel.json` |
| 中継先の画面には自分のCSPを付けない | Firebase のログイン画面は自前の CSP を持つため、`/__/` には CSP 以外の安全ヘッダーとキャッシュ禁止だけ | `vercel.json`（headers） |
| authDomain を今のドメインに切り替え | **`VITE_AUTH_SAME_ORIGIN=true` のときだけ**。アプリ版（Capacitor）・localhost・http は今までどおり | `src/firebase.ts`（`resolveAuthDomain`） |
| 「連携中…」で永久に止まらない | ポップアップの結果が届かなくても、裏でログインが済んだら成功扱い。90秒で待つのをやめて案内を出す | `src/utils/googleAuth.ts`（`popupWithWatchdog`） |

**スイッチ（環境変数）を入れるまでは、authDomain は今までどおり**です。中継の追加と「止まらない」対策だけが先に効きます。

## あなたが管理画面でやること（順番どおりに）

本番のドメインを `<ドメイン>` と書きます（例：`mntb-listening.vercel.app`。独自ドメインがあればそれも同じように追加）。

### 1. Google Cloud Console（Google ログイン用）
1. https://console.cloud.google.com/apis/credentials を開き、プロジェクト **mntb-listening** を選ぶ
2. 「OAuth 2.0 クライアント ID」の **Web client (auto created by Google Service)** を開く
3. **承認済みの JavaScript 生成元** に `https://<ドメイン>` を追加
4. **承認済みのリダイレクト URI** に `https://<ドメイン>/__/auth/handler` を追加
5. 保存（反映まで数分〜最大数時間かかることがある）

### 2. Apple Developer（Apple ログイン用）
1. https://developer.apple.com/account/resources/identifiers/list/serviceId を開く
2. Firebase で使っている **Services ID** を開き、Sign In with Apple の「Configure」
3. **Domains and Subdomains** に `<ドメイン>` を追加
4. **Return URLs** に `https://<ドメイン>/__/auth/handler` を追加（今の `https://mntb-listening.firebaseapp.com/__/auth/handler` は消さない）
5. Save → Continue → Save

### 3. Firebase Console
1. Authentication → 設定 → **承認済みドメイン** に `<ドメイン>` があるか確認（無ければ追加）

### 4. Vercel（最後にスイッチを入れる）
1. Vercel のプロジェクト → Settings → Environment Variables
2. `VITE_AUTH_SAME_ORIGIN` = `true`（Environment は **Production**。プレビューでも試すなら Preview も）
3. Deployments から最新の本番を **Redeploy**（Vite は作るときに環境変数を読み込むため、作り直しが必要）

> Vercel のプロジェクトが2つ（`mntb-listening` と `mntb-listening-22aj`）ある場合は、実際に使う方に入れる。
> 両方使うなら、1・2 で両方のドメインを登録してから両方に入れる。

## 確かめ方
- `https://<ドメイン>/__/auth/handler` を開いて、白い画面（Firebase のログイン用ページ）が出れば中継は動いている（404 やアプリのホームが出たら中継が効いていない）
- 設定画面 → Google でログイン → ポップアップが閉じて、アカウントが表示されれば成功
- 失敗したとき：`redirect_uri_mismatch` が出たら手順1の4の登録漏れ。Apple で `invalid_request` なら手順2の4

## 元に戻すには
- **まずは Vercel の `VITE_AUTH_SAME_ORIGIN` を消して（または false にして）Redeploy** するだけで、authDomain は前の設定に戻る
- コードごと戻すなら、このPRのコミットを `git revert`
