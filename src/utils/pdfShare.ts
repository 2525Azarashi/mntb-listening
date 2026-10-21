import { Capacitor } from '@capacitor/core';

/**
 * PDF の印刷・保存（2026-10-21 ご指摘「PDF が印刷できない」）
 *
 * ■ アプリ（iOS / Android）
 *   WebView では window.print() も <a download> も効かない（何も起きない）。
 *   そこで PDF を端末のキャッシュに書き出し、OS の共有シートを開く。
 *   共有シートには「プリント」「"ファイル"に保存」「AirDrop」などが並ぶので、そこから印刷・保存できる。
 * ■ ブラウザ
 *   印刷：見えない iframe に PDF を読み込んでブラウザの印刷を呼ぶ。だめなら新しいタブで開く（そこから印刷）。
 *   保存：ダウンロード。
 * 戻り値：画面に出す一言（なければ空）
 */
export const isNativeApp = () => Capacitor.isNativePlatform();

async function fetchPdf(url: string): Promise<Blob> {
  const r = await fetch(url, { cache: 'force-cache' });
  if (!r.ok) throw new Error(`pdf ${r.status}`);
  return r.blob();
}

function toBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => resolve(String(fr.result).replace(/^data:[^,]*,/, ''));
    fr.onerror = () => reject(fr.error);
    fr.readAsDataURL(blob);
  });
}

/** アプリ：キャッシュに書き出して共有シートを開く */
async function shareNative(url: string, fileName: string, title: string): Promise<string> {
  const [{ Filesystem, Directory }, { Share }] = await Promise.all([import('@capacitor/filesystem'), import('@capacitor/share')]);
  const data = await toBase64(await fetchPdf(url));
  const path = `pdf/${fileName.replace(/[\\/:*?"<>|]+/g, '_')}`;
  const res = await Filesystem.writeFile({ path, data, directory: Directory.Cache, recursive: true });
  try {
    await Share.share({ title, files: [res.uri], dialogTitle: '印刷・保存' });
  } catch (e) {
    // 共有シートを閉じただけ（キャンセル）はエラー扱いにしない
    if (/cancel/i.test(String((e as Error)?.message ?? e))) return '';
    throw e;
  }
  return '';
}

export async function printPdf(url: string, fileName: string, title: string): Promise<string> {
  if (isNativeApp()) return shareNative(url, fileName, title);
  const blobUrl = URL.createObjectURL(await fetchPdf(url));
  const frame = document.createElement('iframe');
  frame.setAttribute('aria-hidden', 'true');
  frame.style.cssText = 'position:fixed;right:0;bottom:0;width:1px;height:1px;border:0;opacity:0;';
  const cleanup = () => setTimeout(() => { frame.remove(); URL.revokeObjectURL(blobUrl); }, 60_000);
  return new Promise<string>(resolve => {
    frame.onload = () => {
      try { frame.contentWindow?.focus(); frame.contentWindow?.print(); resolve(''); }
      catch { window.open(url, '_blank', 'noopener'); resolve('新しいタブで開きました。そこから印刷してください。'); }
      cleanup();
    };
    frame.src = blobUrl;
    document.body.appendChild(frame);
  });
}

export async function savePdf(url: string, fileName: string, title: string): Promise<string> {
  if (isNativeApp()) return shareNative(url, fileName, title);
  const a = document.createElement('a');
  a.href = url; a.download = fileName; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); a.remove();
  return '';
}
