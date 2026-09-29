import {loadEnv} from 'vite';
import {readFileSync} from 'node:fs';
const audio=JSON.parse(readFileSync(new URL('../COMMERCIAL_AUDIO_STATUS.json',import.meta.url),'utf8'));
if(audio.status!=='approved'){console.error('公開ビルドを中止: 商用音声の差し替え・品質確認が未完了です。COMMERCIAL_AUDIO_MIGRATION.mdを確認してください。');process.exit(1);}
const env={...loadEnv('production',process.cwd(),''),...process.env};
const required=['VITE_FIREBASE_API_KEY','VITE_FIREBASE_PROJECT_ID','VITE_FIREBASE_AUTH_DOMAIN','VITE_FIREBASE_APP_ID'];
const missing=required.filter(k=>!env[k]?.trim());
const firebaseValues=Object.keys(env).filter(k=>k.startsWith('VITE_FIREBASE_') && typeof env[k]==='string' && env[k].trim());
const invalidTarget=env.VITE_USE_EMULATORS==='true' || env.VITE_FIREBASE_PROJECT_ID==='mntb-4ef06' || env.VITE_FIREBASE_PROJECT_ID?.startsWith('demo-');
// Only Vercel's dedicated build may publish the offline guest experience. Never silently
// treat a partially configured production backend as an offline deployment.
const guestOnVercel=process.argv.includes('--vercel') && env.VERCEL==='1' && firebaseValues.length===0 && missing.length===required.length;
if(invalidTarget || (missing.length>0 && !guestOnVercel)) {
 console.error('公開ビルドを中止: リスニング専用Firebaseの設定が不足・不正です。',missing.join(', '));process.exit(1);
}
if(guestOnVercel) console.warn('Vercel guest deployment: 専用Firebase未設定。ゲスト演習・音声・AI対戦のみ利用できます。Googleログイン・オンライン機能は無効です。');
else console.log('Release target: '+env.VITE_FIREBASE_PROJECT_ID);
