# Web版とアプリ版をそろえる決まり（2026-10-11〜）

## いまの形
- GitHub（このリポジトリ）が **Web版とアプリ版（iOS / Android）の共通の元**。`ios/` `android/` `capacitor.config.ts` もここに入っている。
- 2026-10-11 にカサニマロから受け取った「ストアに出した版」（App Store / Google Play 提出版, iOS 1.0.1 (10) / Android 1.0.1 (8)）をそのまま取り込み、
  そこに Web 版だけで先に入っていた変更（音読・読み方、絵の問題の復習、装備をはずす、BGM の修正）を重ねた。
- アプリ専用のコードは、すべて `Capacitor.isNativePlatform()` で分けてあるので、Web では動かない（広告・ネイティブログインなど）。

## カサニマロに送るときの基準
- タグ **`kasa-baseline`** = カサニマロの手元にある版。
- 差分は `bash scripts/kasa-diff.sh` で作る。基準からの「変更したファイル」をそのままの場所で ZIP にする。
- **カサニマロに「送った」と確認できたら**、基準を進める：
  ```bash
  git tag -f kasa-baseline HEAD && git push -f origin kasa-baseline
  ```
  送ったと確認できるまでは、基準は動かさない（差分はどんどん足していく）。

## GitHub に入れないもの（カサニマロの手元だけ）
`.env`、`AuthKey_*.p8`（Apple の鍵）、`android/app/upload-keystore.jks` と `android/key.properties`（Android の署名）、
`ios/App/App/GoogleService-Info.plist`、`android/app/google-services.json`。`.gitignore` で止めてある。
差分 ZIP にも入らないので、上書きコピーしても消えない。

## カサニマロ側の更新手順
1. 差分 ZIP の `app/` の中身を、手元のフォルダにそのまま上書きコピー（`_消すファイル.txt` に書いてあるものがあれば消す）
2. `npm install`（package.json が変わったときだけ）
3. `npm test` → `npm run app:ios` / `npm run app:android`
4. バージョン番号を 1 つ上げてストアへ
