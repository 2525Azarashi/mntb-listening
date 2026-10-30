/**
 * ===================================================================
 * 公開プロフィール（ほかの人から見えるページ）2026-10-26
 * ===================================================================
 *   ・ランキング／フレンド一覧の名前を押すと開く（UserProfileDialog）
 *   ・マイページの「ほかの人からの見え方」でも同じものを出す（プレビュー）
 *
 * ■ 見せるもの（本人が「プロフィールを公開」にしているときだけ）
 *   D6（2026-10-30）：その人のマイページ全体＝マイページ・カレンダー・きせかえ・称号・マイPDF の5タブ
 *   とびら君（見た目・レベル）・名前・称号・学年・志望校・志・自己紹介
 *   学習時間（累計・この7日）・7日間の棒グラフ・連続学習・解いた大問・達成ステージ・称号の数
 *   直近28日のカレンダーと教科ごとの合計（教材名・ひとことは出さない）・持っているアイテム・取った称号・持っているPDFの表紙
 * ■ 見せないもの
 *   実名・メール・在籍校・連絡先・答案の中身・成績
 *
 * 見た目は既存の部品だけで組む（mt-card・ps-stats の数字の札・GrowthAvatar・mt-dialog）。
 */
import { useState } from 'react';
import { Clock, Flame, BookOpen, Flag, Award, GraduationCap, School, CalendarDays, Swords, UserRound, Shirt, FileText, Share2 } from 'lucide-react';
import { PublicBadges, PublicCalendar, PublicOutfit, PublicPrints } from './PublicProfileTabs';
import { GrowthAvatar } from '../../battle/ui/GrowthParts';
import { emptyProgress, xpRequiredForLevel, DEFAULT_FRAME, DEFAULT_POSE, itemById, type GrowthProgress } from '../../battle/core/growth';
import { badgeById } from '../../battle/core/growthBadges';
import { displaySafeNickname, displaySafePublicText } from '../../features/safety/nicknameFilter';
import { formatStudyTime } from '../../utils/studyTime';
import { barPercents, weekLabels, weekSummary, dayKey, BIO_MAX } from '../../utils/publicProfileCore';
import type { PublicStudyProfile } from '../../utils/publicStudyProfile';
import type { StudyPost } from '../studylog/studyFeed';
import { subjectLabel } from '../studylog/manualLogCore';

/** 対戦の成績（battle_ranking の公開の値。ランキングに出ている数字と同じ） */
export interface PublicBattleStats { wins: number; losses: number; draws: number; rating: number }
import '../../components/profile-settings.css';
import './public-profile.css';

/** 公開された見た目（アイテムID）から、表示用の GrowthProgress を作る（持っていない物は付けない） */
export function lookToProgress(profile: PublicStudyProfile, xpForLevel = 0): GrowthProgress {
  const p = emptyProgress('public');
  const look = profile.look;
  const ok = (id: string, kind: string) => !!id && itemById(id)?.kind === kind;
  const pose = ok(look.pose, 'pose') ? look.pose : DEFAULT_POSE;
  const frame = ok(look.frame, 'frame') ? look.frame : DEFAULT_FRAME;
  const hat = ok(look.hat, 'hat') ? look.hat : '';
  const glasses = ok(look.glasses, 'glasses') ? look.glasses : '';
  p.owned = [pose, frame, hat, glasses].filter(Boolean);
  p.equipped = { ...p.equipped, pose, frame, hat, glasses };
  p.xp = xpForLevel;
  return p;
}

/** レベル表示のための xp（そのレベルになる最小の経験値） */
function xpForLevel(level: number | null): number {
  return level && level > 1 ? xpRequiredForLevel(level) : 0;
}

export function PublicProfileView({
  profile,
  fallbackName,
  isPreview = false,
  now = Date.now(),
  battle = null,
  posts = [],
}: {
  /** 対戦の成績（無ければ出さない） */
  battle?: PublicBattleStats | null;
  /** フレンドに共有された学習記録（フレンドのときだけ読める。無ければタブを出さない） */
  posts?: StudyPost[];
  profile: PublicStudyProfile;
  /** 公開文書に名前が無いとき（古い文書）に使う名前 */
  fallbackName?: string;
  isPreview?: boolean;
  now?: number;
}) {
  const name = displaySafeNickname(profile.nickname || fallbackName || 'なまえ未設定');
  const school = displaySafePublicText(profile.targetSchool);
  const motto = displaySafePublicText(profile.motto);
  // 改行は「使えない文字」扱いになるので、1行ずつ確かめてからつなぐ（使えない語・連絡先がある行は伏せる）
  const bio = profile.bio ? profile.bio.split('\n').map(line => (line.trim() ? displaySafePublicText(line, BIO_MAX) : '')).join('\n').trim() : '';
  const titleLabel = profile.title ? badgeById(profile.title)?.label || '' : '';
  // 週の記録が古い（7日以上前に書かれた）なら、グラフは「最近の記録なし」にする
  const weekFresh = !!profile.week && !!profile.weekEnd && profile.weekEnd >= dayKey(now - 6 * 86_400_000);
  const week = weekFresh && profile.week ? profile.week : null;
  const sum = week ? weekSummary(week) : null;
  const bars = week ? barPercents(week) : [];
  const labels = weekLabels(profile.weekEnd ? new Date(`${profile.weekEnd}T12:00:00`).getTime() : now);
  const progress = lookToProgress(profile, xpForLevel(profile.level));
  // ★D6（2026-10-30）公開したら「その人のマイページ全体」★ マイページと同じ5つのタブ（＋フレンドに共有した記録）
  type Tab = 'about' | 'calendar' | 'outfit' | 'badges' | 'prints' | 'posts';
  const [page, setPage] = useState<Tab>('about');
  const hasPosts = posts.length > 0;
  const tabs: [Tab, string, typeof UserRound][] = [['about', 'マイページ', UserRound], ['calendar', 'カレンダー', CalendarDays], ['outfit', 'きせかえ', Shirt], ['badges', '称号', Award], ['prints', 'マイPDF', FileText]];
  if (hasPosts) tabs.push(['posts', '共有', Share2]);

  return (
    <div className="pp-view" data-public-profile-view data-page={page} data-has-posts={hasPosts || undefined}>
      <nav className="pp-tabs" role="tablist" aria-label="プロフィールのタブ" data-pp-tabs={tabs.length}>
        {tabs.map(([id, label, Icon]) => (
          <button key={id} type="button" role="tab" aria-selected={page === id} onClick={() => setPage(id)} data-pp-tab={id}>
            <Icon size={16} aria-hidden="true" /><span>{label}</span>
          </button>
        ))}
      </nav>
      {page === 'about' && <div className="pp-page pp-page-about" data-pp-page="about">
      <section className="pp-head mt-card" aria-label="プロフィール">
        <GrowthAvatar progress={progress} size={72} showLevel={profile.level != null} />
        <div className="pp-id">
          {titleLabel && <span className="pp-title">{titleLabel}</span>}
          <h3 className="pp-name">{name}</h3>
          <p className="pp-tags">
            {profile.grade && <span><GraduationCap size={14} aria-hidden="true" />{profile.grade}</span>}
            {school && <span><School size={14} aria-hidden="true" />{school}</span>}
            {battle && battle.wins + battle.losses + battle.draws > 0 && <span data-public-battle><Swords size={14} aria-hidden="true" />対戦 {battle.wins}勝{battle.losses}敗（勝率{Math.round((battle.wins / (battle.wins + battle.losses + battle.draws)) * 100)}%）</span>}
          </p>
        </div>
      </section>

      {motto && <p className="pp-motto">「{motto}」</p>}
      {bio && <p className="pp-bio" data-public-bio>{bio}</p>}

      <dl className="ps-stats pp-stats">
        <div><dt><Clock size={15} aria-hidden="true" />学習時間</dt><dd>{formatStudyTime(profile.studySeconds)}</dd></div>
        <div><dt><Flame size={15} aria-hidden="true" />連続</dt><dd>{profile.streak ?? '—'}{profile.streak != null && <small>日</small>}</dd></div>
        <div><dt><BookOpen size={15} aria-hidden="true" />解いた大問</dt><dd>{profile.solved ?? '—'}</dd></div>
        <div><dt><Flag size={15} aria-hidden="true" />達成ステージ</dt><dd>{profile.stagesCleared ?? '—'}</dd></div>
        <div><dt><Award size={15} aria-hidden="true" />称号</dt><dd>{profile.badges ?? '—'}{profile.badges != null && <small>個</small>}</dd></div>
        <div><dt><CalendarDays size={15} aria-hidden="true" />この7日</dt><dd>{sum ? formatStudyTime(sum.total) : '—'}</dd></div>
      </dl>

      <section className="pp-week mt-card" aria-label="この7日間の学習時間">
        <header>
          <h4>この7日間</h4>
          {sum && <span>{sum.activeDays}日 学習</span>}
        </header>
        {week ? (
          <ol className="pp-bars">
            {week.map((sec, i) => (
              <li key={i} data-today={i === week.length - 1 || undefined}>
                <span className="pp-bar-track"><span className="pp-bar" style={{ height: `${bars[i]}%` }} title={formatStudyTime(sec)} /></span>
                <small>{labels[i]}</small>
              </li>
            ))}
          </ol>
        ) : (
          <p className="pp-empty">最近の記録はまだありません。</p>
        )}
      </section>

      <p className="ps-help pp-note">
        {isPreview
          ? 'ほかの人には、この内容が見えます。名前・志望校・志・自己紹介はマイページで直せます。'
          : '学習時間は本人の端末で記録した、演習・解説の時間です。成績や順位を表すものではありません。'}
      </p>
      </div>}
      {page === 'calendar' && <div className="pp-page" data-pp-page="calendar"><PublicCalendar profile={profile} /></div>}
      {page === 'outfit' && <div className="pp-page" data-pp-page="outfit"><PublicOutfit profile={profile} base={progress} /></div>}
      {page === 'badges' && <div className="pp-page" data-pp-page="badges"><PublicBadges profile={profile} /></div>}
      {page === 'prints' && <div className="pp-page" data-pp-page="prints"><PublicPrints profile={profile} /></div>}
      {hasPosts && page === 'posts' && <div className="pp-page" data-pp-page="posts">
        <ul className="pp-posts" aria-label="フレンドに共有した学習記録">
          {posts.map(p => <li key={p.id}>
            <span><strong>{subjectLabel(p.subject)}{p.materialName ? `・${displaySafePublicText(p.materialName)}` : ''}</strong>
              {p.comment && <small>{displaySafePublicText(p.comment, 140)}</small>}</span>
            <b>{formatStudyTime(p.minutes * 60)}</b>
          </li>)}
        </ul>
        <p className="ps-help pp-note">フレンドだけに共有された記録です（本人の自己申告）。</p>
      </div>}
    </div>
  );
}
