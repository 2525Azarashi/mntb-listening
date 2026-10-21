import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { __resetPdfViewer, closePdf, openPdf, pdfViewerStore } from '../src/utils/pdfViewer';
import { AD_CONFIG } from '../src/ads/adConfig';

/** history / popstate をまねる（戻るボタン＝history.back で popstate が来る） */
function fakeBrowser() {
  const stack: unknown[] = [null]; let i = 0; const pop: (() => void)[] = [];
  const history = {
    get state() { return stack[i]; },
    pushState(st: unknown) { stack.splice(i + 1); stack.push(st); i++; },
    back() { if (i > 0) { i--; queueMicrotask(() => pop.forEach(f => f())); } },
  };
  const win = { location: { href: 'https://app.example/', origin: 'https://app.example' }, addEventListener: (t: string, f: () => void) => { if (t === 'popstate') pop.push(f); } };
  vi.stubGlobal('history', history); vi.stubGlobal('window', win);
  return { history, depth: () => i };
}

describe('アプリ内の PDF ビュー', () => {
  beforeEach(() => __resetPdfViewer());
  afterEach(() => { vi.unstubAllGlobals(); });

  it('開くと履歴を1つ積み、「もどる」で元の画面に戻る（履歴も元どおり）', async () => {
    const b = fakeBrowser();
    openPdf('/prints/a.pdf', '化学 プリント');
    expect(pdfViewerStore.get()).toMatchObject({ url: '/prints/a.pdf', title: '化学 プリント', fileName: '化学_プリント.pdf' });
    expect(b.depth()).toBe(1);
    closePdf();
    await Promise.resolve();
    expect(pdfViewerStore.get()).toBeNull();
    expect(b.depth()).toBe(0);
  });

  it('Android の戻るボタン（＝履歴を戻る）でも閉じる', async () => {
    const b = fakeBrowser();
    const seen: unknown[] = []; pdfViewerStore.subscribe(d => seen.push(d));
    openPdf('/prints/a.pdf', 'A');
    b.history.back();
    await Promise.resolve();
    expect(pdfViewerStore.get()).toBeNull();
    expect(seen.at(-1)).toBeNull();
  });

  it('外のサイトや PDF 以外は開かない', () => {
    fakeBrowser();
    openPdf('https://evil.example/x.pdf', 'x');
    openPdf('/prints/a.html', 'x');
    expect(pdfViewerStore.get()).toBeNull();
  });

  it('PDF を開いている間はバナー広告を出さない画面として扱う', () => {
    expect(AD_CONFIG.banner.hiddenOn).toContain('pdf');
  });
});

describe('PDF ビューの「もどる」と印刷（2026-10-21）', () => {
  beforeEach(() => __resetPdfViewer());
  afterEach(() => { vi.unstubAllGlobals(); });
  it('popstate が来ない WebView でも「もどる」で即座に閉じる', () => {
    const stack: unknown[] = [null]; let i = 0;
    vi.stubGlobal('history', { get state() { return stack[i]; }, pushState(st: unknown) { stack.push(st); i++; }, back() { if (i > 0) i--; /* popstate を出さない */ } });
    vi.stubGlobal('window', { location: { href: 'https://app.example/', origin: 'https://app.example' }, addEventListener: () => undefined });
    vi.stubGlobal('setTimeout', (() => 0) as unknown as typeof setTimeout);
    openPdf('/prints/a.pdf', 'A');
    closePdf();
    expect(pdfViewerStore.get()).toBeNull();
    expect(i).toBe(0);
  });
  it('ビューに印刷ボタン・もう一度・止まったときの作り直しがある', async () => {
    const { readFileSync } = await import('node:fs');
    const src = readFileSync('src/components/PdfViewer.tsx', 'utf8');
    expect(src).toContain('data-pdf-print');
    expect(src).toContain('もう一度');
    expect(src).toContain('watchdog');
    expect(src).toContain('if (!isNativeApp())');
    expect(src).toContain('setFallback(true)');
    expect(src).toContain('<iframe className="pdfv-native"');
    const share = readFileSync('src/utils/pdfShare.ts', 'utf8');
    expect(share).toContain('Share.share');
    expect(share).toContain('window.print()');
    expect(share).not.toContain("window.open(url, '_blank')");
    expect(share).toContain('closePdf();');
    expect(share).toContain('URL.createObjectURL(await fetchPdf(url))');
    expect(share).toContain('a.href = blobUrl');
    const collection = readFileSync('src/components/MyCollection.tsx', 'utf8');
    expect(collection).not.toContain('catch(() => openPdf(print.file, print.label))');
  });
});
