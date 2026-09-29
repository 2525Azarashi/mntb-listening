// src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { ThemeProvider } from './contexts/ThemeContext';
import { AppWallpaper } from './components/AppWallpaper';


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
      <AppWallpaper />
    </ThemeProvider>
    {/*
      Vercel Web Analytics（画面には何も描画されず、計測用スクリプトだけを注入する）
      - Vercel にデプロイされている場合のみデータが収集される
      - 本アプリは URL が変化しない SPA のため、既定ではページビューが常に "/" に集約される
    */}

  </StrictMode>
);
