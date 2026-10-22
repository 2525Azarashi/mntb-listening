import { initializeApp } from 'firebase/app';
import {
  getAuth,
  initializeAuth,
  indexedDBLocalPersistence,
  browserLocalPersistence,
  GoogleAuthProvider,
  connectAuthEmulator
} from 'firebase/auth';
import { getFirestore, initializeFirestore, connectFirestoreEmulator, disableNetwork, type Firestore } from 'firebase/firestore';
const env = import.meta.env;
export const FIREBASE_CONFIGURED = Boolean(env.VITE_FIREBASE_API_KEY && env.VITE_FIREBASE_PROJECT_ID && env.VITE_FIREBASE_AUTH_DOMAIN && env.VITE_FIREBASE_APP_ID);
export const USE_EMULATORS = env.VITE_USE_EMULATORS === 'true';
if (env.VITE_FIREBASE_PROJECT_ID === 'mntb-4ef06') throw new Error('統合版のFirebaseには接続できません。リスニング専用プロジェクトを設定してください。');
const projectId = FIREBASE_CONFIGURED ? env.VITE_FIREBASE_PROJECT_ID : 'demo-manatobi-listening';
/**
 * ★Web 版のログインを「同じドメイン」で行う（2026-10-22）★
 *   ログイン画面（/__/auth/handler）が別ドメイン（<project>.firebaseapp.com）だと、
 *   Safari・Chrome の「別サイトの保存領域を分ける」仕組みで結果が画面に戻らず「連携中…」で止まる。
 *   vercel.json で /__/auth/* を firebaseapp.com へ中継しているので、authDomain を今のドメインにすれば同じドメインで完結する。
 *   ・VITE_AUTH_SAME_ORIGIN=true のときだけ（Google / Apple の管理画面にこのドメインの戻り先を登録してから入れる。docs/WEB_LOGIN_SAME_ORIGIN.md）
 *   ・アプリ版（Capacitor：localhost / capacitor://）と開発環境では使わない＝今までどおり
 */
function resolveAuthDomain(configured: string): string {
  try {
    if (env.VITE_AUTH_SAME_ORIGIN !== 'true' || typeof window === 'undefined') return configured;
    // アプリ版（Capacitor）は端末のログインを使うので、ここは常に今までどおり
    const cap = (window as unknown as { Capacitor?: { isNativePlatform?: () => boolean } }).Capacitor;
    if (cap?.isNativePlatform?.()) return configured;
    const { protocol, host, hostname } = window.location;
    if (protocol !== 'https:' || hostname === 'localhost' || hostname.startsWith('127.') || hostname.endsWith('.local')) return configured;
    return host;
  } catch { return configured; }
}
const app = initializeApp({
  apiKey: FIREBASE_CONFIGURED ? env.VITE_FIREBASE_API_KEY : 'demo-listening-key',
  projectId, authDomain: FIREBASE_CONFIGURED ? resolveAuthDomain(env.VITE_FIREBASE_AUTH_DOMAIN) : 'demo-manatobi-listening.firebaseapp.com',
  appId: FIREBASE_CONFIGURED ? env.VITE_FIREBASE_APP_ID : '1:123:web:listening',
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET, messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
}, 'manatobi-listening');

function initAuth() {
  try {
    return initializeAuth(app, {
      persistence: [indexedDBLocalPersistence, browserLocalPersistence],
    });
  } catch {
    return getAuth(app);
  }
}
export const auth = initAuth();
export const provider = new GoogleAuthProvider();
// 統合版と同じ：学校・塾の Wi-Fi などでストリーム通信が詰まる環境だけ、自動でロングポーリングに切り替える
function createDb(): Firestore {
  try { return initializeFirestore(app, { experimentalAutoDetectLongPolling: true }); } catch { return getFirestore(app); }
}
export const db = createDb();
if (USE_EMULATORS) {
  if (!projectId.startsWith('demo-')) throw new Error('Emulator testing requires a demo- project ID.');
  connectAuthEmulator(auth, 'http://127.0.0.1:9099', { disableWarnings: true });
  connectFirestoreEmulator(db, '127.0.0.1', 8080);
} else if (!FIREBASE_CONFIGURED) {
  // Guest preview only. Never connect to the integrated app or an unknown backend.
  void disableNetwork(db);
}
