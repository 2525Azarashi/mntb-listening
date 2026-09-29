export function Intro({onBack,onBattle}:{onBack:()=>void;onBattle?:()=>void}) {
  return <main className="mtb-page overflow-y-auto pb-app-nav"><button className="mtb-back" onClick={onBack}>ホームに戻る</button>
    <h1>マナトビ リスニングの使い方</h1><h2>ひとりで演習</h2><p>第1問Aから第6問Bまで、大問を選び音源を聞いて解答します。解説ではスクリプト・和訳・聞き取りの決め手を確認できます。</p>
    <h2>対戦で力試し</h2><p>AI対戦はゲストでも遊べます。全国対戦とフレンド対戦にはGoogleログインが必要です。イヤホンを使い、音声が再生できることを確認してから始めてください。</p>
    <h2>復習と成長</h2><p>復習ノート・学習記録・ランキング・マナコイン・ガチャ・きせかえを引き継いだリスニング専用版です。オンライン保存には運営者によるFirebase設定が必要です。</p>
    {onBattle && <button className="mtb-back" onClick={onBattle}>対戦ロビーへ</button>}</main>;
}
