import React, { useEffect, useState } from 'react';
import type { ListeningMaterial } from '../data/englishListeningQ1AProblems';

/**
 * 表のセルで ○／× のメモを付けられる列か。
 * 第4問B の条件表（Speaker × A/B/C）のように、見出しが 1〜2 文字の空欄の列だけ。
 * 第6問B の「Memo」列のような文章を書く列は対象外。
 */
const isMarkColumn = (header: string) => header.trim().length > 0 && header.trim().length <= 2;
const NEXT_MARK: Record<string, string> = { '': '○', '○': '×', '×': '' };

/** Render only printed question data. The shared document never follows answer-page keys. */
export function ListeningMaterials({ material, activeSubId }: {
  material: ListeningMaterial;
  activeSubId?: string;
}) {
  const activeNumber = activeSubId?.match(/_(\d+)$/)?.[1];
  /*
    ★表の ○× メモ（ご要望「タップで〇×がつけれるようになるとなおよし」）★
    本番の冊子に鉛筆で書き込む代わり。端末内の一時的なメモなので保存はしない
    （別の回・別の大問に移ったら消える）。
  */
  const [marks, setMarks] = useState<Record<string, string>>({});
  /* ★図はタップで全画面に拡大（ご要望「図が一部しか映ってない」）★ */
  const [zoomed, setZoomed] = useState<{ src: string; caption: string; minWidth?: number } | null>(null);
  useEffect(() => { setMarks({}); setZoomed(null); }, [material]);
  useEffect(() => {
    if (!zoomed) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setZoomed(null); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [zoomed]);

  const text = (value: string) => value.split(/(\(\s*\d+\s*\))/).map((part, i) => {
    const number = part.match(/^\(\s*(\d+)\s*\)$/)?.[1];
    if (!number) return part;
    return <mark key={i} data-material-blank={number}
      aria-current={number === activeNumber ? 'true' : undefined}
      className={`inline-block whitespace-nowrap rounded border px-2 font-bold ${
        number === activeNumber ? 'border-amber-500 bg-amber-100 text-gray-900' : 'border-gray-300 bg-white text-gray-700'
      }`}>({number})</mark>;
  });
  const table = material.table;
  const markable = !!table && table.headers.slice(1).some(isMarkColumn);
  /*
    ★条件表があるとき（第4問B）は条件と表を詰めて1画面に収める★
    ご指摘：「第4問B … 図一画面に収まってない」
    390x844 で Conditions 117px ＋ 表 4行×65px ＝ 約380px を使い、④の行が
    選択肢の下に隠れていた。条件の行間・表のセルの余白を詰め、
    話者の列は1行で収まるように幅を取り、A/B/C の列は ○× が入る幅だけにする。
  */
  const sections = material.sections?.map((section, i) => (
        <section key={i} className={`rounded-lg border border-gray-200 ${markable ? 'mb-2 px-2.5 py-1.5' : 'mb-3 px-3 py-2'}`}>
          {section.heading && <h3 className="mb-2 font-bold">{section.heading}</h3>}
          <ul className={markable ? 'space-y-0.5 text-[15px] leading-snug' : 'space-y-2'}>
            {section.rows.map((row, j) => <li key={j}>{text(row)}</li>)}
          </ul>
        </section>
      ));
  return (
    <article data-listening-material className="min-w-0 font-modern text-[16px] leading-relaxed text-gray-900">
      <h2 className={`${markable ? 'mb-1' : 'mb-1.5'} text-base font-bold leading-snug`}>{material.title}</h2>
      {!material.images?.length && material.instruction && <p className="mb-3 text-sm text-gray-600">{material.instruction}</p>}
      {!material.images?.length && sections}
      {table && <div className="mb-2 overflow-x-auto" tabIndex={0} aria-label="資料の表">
        <table className={`w-full border-collapse text-left ${markable ? 'table-fixed text-[15px] leading-snug' : 'text-[16px]'}`}>
          {markable && <colgroup>
            {table.headers.map((h, i) => <col key={i} style={i > 0 && isMarkColumn(h) ? { width: '3.25rem' } : undefined} />)}
          </colgroup>}
          <thead><tr>{table.headers.map((cell, i) =>
            <th key={i} scope="col" className={`border border-gray-300 bg-blue-50 ${markable ? 'px-2 py-1 text-center first:text-left' : 'px-3 py-2'}`}>{cell}</th>)}</tr></thead>
          <tbody>{table.rows.map((row, i) => <tr key={i}>
            {row.map((cell, j) => {
              const header = table.headers[j] ?? '';
              if (markable && j > 0 && !cell && isMarkColumn(header)) {
                const key = `${i}:${j}`;
                const mark = marks[key] || '';
                return <td key={j} className="border border-gray-300 p-0">
                  <button type="button" data-material-mark={mark || 'none'}
                    onClick={() => setMarks(m => ({ ...m, [key]: NEXT_MARK[mark] ?? '' }))}
                    aria-label={`${row[0]} の ${header}：${mark === '○' ? '○' : mark === '×' ? '×' : '未記入'}（タップで切り替え）`}
                    className={`flex h-11 w-full items-center justify-center text-xl font-bold ${
                      mark === '○' ? 'bg-emerald-50 text-emerald-700' : mark === '×' ? 'bg-rose-50 text-rose-700' : 'text-gray-300'
                    }`}>
                    {mark || <span aria-hidden="true" className="text-base">・</span>}
                  </button>
                </td>;
              }
              return <td key={j} className={`border border-gray-300 ${markable ? 'px-2 py-1' : 'min-w-20 px-3 py-2'}`}>{text(cell) || '\u00a0'}</td>;
            })}
          </tr>)}</tbody>
        </table>
        {markable && <p className="mt-1 text-xs leading-tight text-gray-600">空欄をタップすると ○ → × → 空欄 の順にメモできます</p>}
      </div>}
      {/*
        ★図は画面の幅に合わせて全体を見せる（横スクロールをやめた）★
        ご指摘：「図がこれ全然一部しか映ってないやん？ … 少し小さくなってもいいから、
        全画面映るようにしたい」
        以前は minWidth 640px で描いて横スクロールさせていたため、390px の画面では
        左の 55% ほどしか見えず、③〜⑤のコマとタイトルが切れていた。
        いまは幅いっぱい（縦横比そのまま）で全体を描き、細部はタップで全画面に拡大
        （ピンチで更に拡大できる）して確かめる。
      */}
      {material.images?.map(image => <figure data-material-graph key={image.src} className="mb-3">
        {image.caption !== material.title && <figcaption className="mb-1 text-sm font-bold">{image.caption}</figcaption>}
        <button type="button" onClick={() => setZoomed(image)}
          aria-label={`${image.caption}を全画面で拡大する`}
          className="relative block w-full cursor-zoom-in overflow-hidden rounded border border-gray-200 bg-white">
          <img src={image.src} alt={image.caption} className="block h-auto w-full" />
          <span aria-hidden="true" className="absolute bottom-1 right-1 rounded-full bg-[#2C3E50]/85 px-2 py-0.5 text-xs font-bold text-white">
            タップで拡大
          </span>
        </button>
      </figure>)}
      {!!material.images?.length && material.instruction && <p className="mb-3 text-sm text-gray-600">{material.instruction}</p>}
      {!!material.images?.length && sections}
      {zoomed && <div role="dialog" aria-modal="true" aria-label={`${zoomed.caption}（拡大）`} data-material-zoom
        className="fixed inset-0 z-[200] flex flex-col bg-black/90"
        style={{ paddingTop: 'env(safe-area-inset-top, 0px)', paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
        <div className="flex shrink-0 items-center justify-between gap-2 px-3 py-1 text-white">
          <span className="min-w-0 truncate text-sm font-bold">{zoomed.caption}</span>
          <button type="button" onClick={() => setZoomed(null)} autoFocus
            className="min-h-11 min-w-11 shrink-0 rounded-lg bg-white px-3 text-sm font-bold text-[#2C3E50]">閉じる</button>
        </div>
        <div className="min-h-0 flex-1 overflow-auto overscroll-contain" style={{ touchAction: 'pan-x pan-y pinch-zoom' }}
          onClick={(e) => { if (e.target === e.currentTarget) setZoomed(null); }}>
          {/* 横向きの図は縦の高さいっぱいまで大きくする（はみ出すぶんは横スクロール） */}
          <img src={zoomed.src} alt={zoomed.caption} className="mx-auto block h-auto max-w-none bg-white"
            style={{ width: `max(100%, min(${Math.round((zoomed.minWidth || 360) * 1.4)}px, 180vh))` }} />
        </div>
        <p className="shrink-0 px-3 py-1 text-center text-xs text-gray-200">ピンチで拡大・ドラッグで移動できます</p>
      </div>}
    </article>
  );
}
