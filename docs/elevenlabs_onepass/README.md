# ElevenLabs 一括読み上げ原稿（英文法 1163文／英単語・英熟語 5713語）

| ファイル | 使い方 |
|---|---|
| `Studio_英文法_全1163文.epub` | ElevenLabs **Studio** に Upload（1回で全部）。章＝アプリの第1〜20章 |
| `Studio_英単語熟語_全5713語.epub` | 同上。Part 1〜24（1章400段落の上限内で約300語ずつ） |
| `Studio_*_章とID.json` | Studio の章 → 問題ID／語ID の対応 |
| `一括_*_間なし.pdf/.txt` | 全文1本（英文のみ）。Ctrl+A → Ctrl+C で原稿だけコピーできる |
| `一括_*_間あり.pdf/.txt` | 全文1本＋`<break>`。Text to Speech（Multilingual v2）用。5,000字/回の上限があるので一発では不可 |
| `ElevenLabs_英文法_原稿.pdf` / `grammar_batches/` | 分割版（約20文/回・1.5秒の間）。1問ずつ切る用 |
| `ElevenLabs_英単語熟語_原稿.pdf` | 分割版（30語/回・1.2秒の間）。`docs/elevenlabs_vocab` と同じ原稿 |

## 公式仕様（2026-11 確認）
- Text to Speech 画面：1回 最大5,000文字（有料）／2,500（無料）
- Studio：500章/プロジェクト、400段落/章、5,000文字/段落。EPUB の Heading 1 で章が自動分割
- `<break>`：Multilingual v2・Flash v2/v2.5 のみ（最大3秒）。v3・v4 は非対応。Studio は「Insert break」ボタンでの挿入のみ記載
- モデル：**Eleven Multilingual v2**（Studio の既定・安定した読み上げ）を使う

## 作り直し
```
cd scripts/elevenlabs-onepass
python3 make.py && python3 make_onepass.py && python3 make_epub.py   # 出力はカレントに出るので docs/elevenlabs_onepass へ移す
```
※ make.py は `../../docs/elevenlabs_vocab/{manifest.json,batches/}` を `vocab_manifest.json` / `vocab_batches/` として参照（実行前にコピー）。
