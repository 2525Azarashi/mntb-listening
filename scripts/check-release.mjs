import {loadEnv} from 'vite';
import {readFileSync} from 'node:fs';
const audio=JSON.parse(readFileSync(new URL('../COMMERCIAL_AUDIO_STATUS.json',import.meta.url),'utf8'));
if(audio.status!=='approved'){console.error('公開ビルドを中止: 商用音声の差し替え・品質確認が未完了です。COMMERCIAL_AUDIO_MIGRATION.mdを確認してください。');process.exit(1);}
const env={...loadEnv('production',process.cwd(),''),...process.env};
const required=['VITE_FIREBASE_API_KEY','VITE_FIREBASE_PROJECT_ID','VITE_FIREBASE_AUTH_DOMAIN','VITE_FIREBASE_APP_ID'];
const missing=required.filter(k=>!env[k]?.trim());
if(missing.length || env.VITE_USE_EMULATORS==='true' || env.VITE_FIREBASE_PROJECT_ID==='mntb-4ef06' || env.VITE_FIREBASE_PROJECT_ID?.startsWith('demo-')) {
 console.error('公開ビルドを中止: 専用Firebase設定が必要です。READMEを参照してください。設定前の画面確認は npm run build:demo。',missing.join(', '));process.exit(1);
}
console.log('Release target: '+env.VITE_FIREBASE_PROJECT_ID);
