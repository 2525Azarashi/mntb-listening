/**
 * 演習画面の左ペイン：リスニング後半（資料つき）の「資料・音源」ペイン（C-04）。
 * ProblemPane.tsx の早期 return の JSX をそのまま移した（DOM・クラス名・data-* / aria-* 属性・文言は1文字も変えていない）。
 *
 * ★部品ではなく描画関数にしている理由★
 *   ProblemPane の中で呼ぶだけにして、React の木（要素の種類と並び）を1段も変えないため。
 *   部品にすると、ここに入るたびに共有の音源プレーヤーが作り直され、再生が止まりうる
 *   （ProblemPane の「Never remount or seek the shared audio player」の約束を守る）。
 */
import React from 'react';
import type { AudioTrack, Problem, SubQuestion } from '../../types/curriculum';
import { ListeningAudioPlayer } from '../ListeningAudioPlayer';
import { ListeningMaterials } from '../ListeningMaterials';

export interface ListeningMaterialPaneContext {
  currentQuestion: Problem;
  isDesktop: boolean;
  isProblemExpanded: boolean;
  setIsProblemExpanded: (v: boolean) => void;
  setIsProblemCollapsed: (v: boolean) => void;
  listeningMaterialsMobile: boolean;
  selectedAnswerSub?: SubQuestion | null;
  /** 資料を持つ音源（呼び出し側で material があることを確かめてから渡す） */
  materialTrack: AudioTrack & { material: NonNullable<AudioTrack['material']> };
  activeStepSub: SubQuestion;
  listeningTracks: AudioTrack[];
  problemScrollRef: React.RefObject<HTMLDivElement | null>;
}

export function renderListeningMaterialPane({
  currentQuestion, isDesktop, isProblemExpanded, setIsProblemExpanded, setIsProblemCollapsed,
  listeningMaterialsMobile, selectedAnswerSub, materialTrack, activeStepSub, listeningTracks, problemScrollRef,
}: ListeningMaterialPaneContext) {
  return (
    <section data-listening-material-pane aria-label="問題の資料"
      className={`lg:w-[58%] flex min-h-0 flex-col border-b lg:border-r border-gray-200 bg-white ${
        isDesktop ? 'h-full' : isProblemExpanded ? 'absolute inset-0 z-30' :
        listeningMaterialsMobile ? 'flex-[1_1_0%]' : 'max-h-[50%] flex-none'
      }`}>
      {isDesktop ? (
        <>
          <div className="flex shrink-0 items-center justify-between gap-2 border-b px-3">
            <span className="text-sm font-bold text-[#2C3E50]">{materialTrack.label} · 資料</span>
          </div>
          <div data-listening-audio className="shrink-0 border-b bg-white px-3 py-1">
            <ListeningAudioPlayer tracks={listeningTracks} focusSubId={activeStepSub.id}
              variant="inline" orientation="horizontal" mode="practice" tone="light"
              readCount={currentQuestion.readCount || 2} playOnce={!!currentQuestion.playOnce} />
          </div>
        </>
      ) : (
        /*
          ★スマホ：見出し行と音源行を1行に統合する★
          ご指摘：「リスニングがまだ一画面に映ってない（後半パート）。見にくい」
          実測（375x740・第4問A）では
            見出し「問18〜21 · 資料 / 全画面で読む」 45px
            音源「▶再生（1回のみ）/ 0.75倍 / 標準」   53px
          の2段で 98px を使い、資料の読める高さが 188px しか残っていなかった。
          ［問18〜21］［▶再生］［0.75倍］［標準］［全画面］を1段（約46px）に
          まとめて、浮いた約50px をそのまま資料と選択肢に回す。
          ・「· 資料」は省く（この段の中身が資料であることは見れば分かる）
          ・「講義（問27〜31）」は「問27〜31」に縮める（幅を再生ボタンに譲る）
          ・全画面ボタンは aria-label で従来の名前（全画面で読む／選択肢に戻る）を保つ
          PC（isDesktop）は従来の2段のまま。
        */
        <div className="flex shrink-0 items-center gap-1.5 border-b bg-white px-2 py-1">
          <span className="max-w-[4.5rem] shrink-0 truncate text-xs font-bold leading-tight text-[#2C3E50]">
            {String(materialTrack.label).replace(/^講義（([^）]+)）$/u, '$1')}
          </span>
          <div data-listening-audio className="min-w-0 flex-1">
            <ListeningAudioPlayer tracks={listeningTracks} focusSubId={activeStepSub.id}
              variant="inline" orientation="horizontal" mode="practice" tone="light"
              readCount={currentQuestion.readCount || 2} playOnce={!!currentQuestion.playOnce} />
          </div>
          <button type="button"
            onClick={() => { setIsProblemExpanded(!isProblemExpanded); setIsProblemCollapsed(false); }}
            aria-label={isProblemExpanded ? '選択肢に戻る' : '全画面で読む'}
            className="min-h-11 min-w-11 shrink-0 rounded-lg border border-gray-200 bg-white px-1.5 text-xs font-bold text-gray-600">
            {isProblemExpanded ? '選択肢へ' : '全画面'}
          </button>
        </div>
      )}
      <div ref={problemScrollRef} tabIndex={0} aria-label="資料をスクロール"
        className={`min-h-0 flex-1 overflow-auto overscroll-contain px-3 md:px-6 ${isDesktop ? 'py-3' : 'py-2'}`}>
        <ListeningMaterials material={materialTrack.material}
          activeSubId={!isDesktop ? selectedAnswerSub?.id : undefined} />
        {materialTrack.hint && <details className="mt-3 text-sm leading-relaxed text-gray-600">
          <summary className="cursor-pointer py-2 font-bold">状況・場面を確認</summary>
          <p>{materialTrack.hint}</p>
        </details>}
      </div>
    </section>
  );
}
