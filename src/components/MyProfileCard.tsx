import { useEffect, useState } from 'react';
import { BookOpen, Check, ChevronDown, Clock, Compass, Flame, GraduationCap, Pencil, Save, School } from 'lucide-react';
import { auth } from '../firebase';
import { MOTTO_MAX, normalizeMotto, readOwnPublicStudyProfile, savePublicStudyProfile } from '../utils/publicStudyProfile';
import { syncRankingNickname } from '../utils/leaderboard';
import { ensureFriendProfile } from '../utils/friends';
import { profileKey, streakKey, completedKey } from '../utils/userStorageKeys';
import { checkNickname, checkPublicText, NICKNAME_MAX } from '../features/safety/nicknameFilter';
import { BADGES } from '../battle/core/growth';
import { useGrowthProgress } from '../hooks/useGrowthProgress';
import { readStudyTime, formatStudyTime } from '../utils/studyTime';
import { GOAL_OPTIONS, TARGET_SCHOOL_MAX, normalizeTargetSchool, readGoal, writeGoal, type GoalId } from '../utils/vocabGoal';
import { readJsonArray, requireLocalStorage, setItemOrThrow } from '../utils/safeLocalStorage';
import { logRejection } from '../utils/reportError';
import './profile-settings.css';

/**
 * マイページの「プロフィール」（2026-10-21）
 *   以前は 設定 ＞ 基本設定 ＞「アカウント・プロフィール」にあった中身をマイページへ移した。
 *   とびら君のアイコンとレベルはマイページ上部に出ているので、ここには載せない（重複させない）。
 *   スマホでも1画面に収めるため、公開トグルの長い説明文は省いた（公開の仕組みはランキング画面の「について」に記載）。
 */
export function MyProfileCard() {
  const { progress: growth } = useGrowthProgress();
  const uid = auth.currentUser?.uid || 'guest';
  const [studySeconds] = useState(() => readStudyTime(uid).total);
  const earnedBadges = BADGES.filter(b => b.id in growth.badges);
  const [name, setName] = useState('');
  const [grade, setGrade] = useState('');
  const [stream, setStream] = useState('science');
  const [targetSchool, setTargetSchool] = useState('');
  const [motto, setMotto] = useState('');
  const [goal, setGoal] = useState<GoalId>(readGoal);
  const [profilePublic, setProfilePublic] = useState(false);
  const [wasPublic, setWasPublic] = useState(false);
  const [publicationReady, setPublicationReady] = useState(!auth.currentUser);
  const [message, setMessage] = useState<{ text: string; error?: boolean } | null>(null);
  const [streak, setStreak] = useState(0);
  const [completedCount, setCompletedCount] = useState(0);
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    let alive = true;
    if (auth.currentUser) void readOwnPublicStudyProfile().then(p => {
      if (alive) { setProfilePublic(!!p); setWasPublic(!!p); setPublicationReady(true); }
    }).catch(() => { if (alive) setMessage({ text: '公開設定を確認できません。公開機能には新版のFirestoreルールの反映が必要です。', error: true }); });
    return () => { alive = false; };
  }, []);

  useEffect(() => {
    try {
      const ls = requireLocalStorage();
      const raw = ls.getItem(profileKey(uid));
      if (raw) {
        const d = JSON.parse(raw);
        setName(d.name || ''); setGrade(d.grade || ''); setStream(d.stream || 'science');
        setTargetSchool(typeof d.targetSchool === 'string' ? d.targetSchool : '');
        setMotto(typeof d.motto === 'string' ? d.motto : '');
      } else {
        setName(auth.currentUser?.displayName || (auth.currentUser ? 'ユーザー' : 'ゲスト'));
        setGrade('高校生');
      }
      setStreak(parseInt(ls.getItem(streakKey(uid)) || '0', 10));
      setCompletedCount(readJsonArray(completedKey(uid)).length);
    } catch (error) { console.error('プロフィール取得エラー:', error); }
  }, [uid]);

  const nameCheck = checkNickname(name);
  const schoolCheck = checkPublicText(targetSchool, TARGET_SCHOOL_MAX);
  const mottoCheck = checkPublicText(motto, MOTTO_MAX);
  const edit = <T,>(set: (v: T) => void) => (v: T) => { set(v); setDirty(true); setMessage(null); };

  const save = async () => {
    if (!nameCheck.ok || !schoolCheck.ok || !mottoCheck.ok) return;
    setSaving(true); setMessage(null);
    try {
      // 公開設定の保存に失敗しても、名前・学年などは保存する
      let publishFailed: string | null = null;
      if (auth.currentUser && (profilePublic || wasPublic)) {
        try { await savePublicStudyProfile(profilePublic, targetSchool, motto); setWasPublic(profilePublic); }
        catch (e) {
          const code = (e as { code?: string })?.code || '';
          console.error('公開設定の保存エラー:', e);
          publishFailed = code === 'permission-denied'
            ? '公開だけ保存できませんでした（サーバー側の公開設定が未更新です）。ほかは保存しました。'
            : code === 'unavailable' || !navigator.onLine
              ? 'オフラインのため、公開だけ保存できませんでした。ほかは保存しました。'
              : '公開だけ保存できませんでした。ほかは保存しました。少し時間をおいてもう一度保存してください。';
        }
      }
      setItemOrThrow(profileKey(uid), JSON.stringify({
        name: name.trim(), grade: grade.trim(), stream, profilePublic: publishFailed ? wasPublic : profilePublic,
        targetSchool: normalizeTargetSchool(targetSchool), motto: normalizeMotto(motto), iconUrl: auth.currentUser?.photoURL || '',
      }));
      writeGoal(goal);
      // 名前を変えたら、ランキング・フレンド検索の表示名もその場で最新化する
      if (auth.currentUser) {
        void syncRankingNickname().catch(logRejection('ranking.syncNickname'));
        void ensureFriendProfile().catch(logRejection('friends.ensureProfile'));
      }
      if (publishFailed) { setProfilePublic(wasPublic); setMessage({ text: publishFailed, error: true }); return; }
      setDirty(false);
      setMessage({ text: '保存しました' });
    } catch (error) {
      console.error('保存エラー:', error);
      setMessage({ text: '保存できませんでした。もう一度お試しください。', error: true });
    } finally { setSaving(false); }
  };

  return <section className="ps-card mt-card mypage-profile" aria-label="プロフィール" data-mypage-profile>
    <div className="mypage-profile-top">
      <label className="ps-name">
        <span className="sr-only">ニックネーム</span>
        <input value={name} maxLength={NICKNAME_MAX} onChange={e => edit(setName)(e.target.value)} placeholder="ニックネーム" aria-invalid={!!name.trim() && !nameCheck.ok} aria-describedby={name.trim() && !nameCheck.ok ? 'nickname-help' : undefined} />
        <Pencil size={16} aria-hidden="true" />
      </label>
      <button type="button" className="mypage-profile-save" onClick={() => void save()} disabled={saving || !dirty || !nameCheck.ok || !schoolCheck.ok || !mottoCheck.ok} data-mypage-save>
        {message && !message.error && !dirty ? <Check size={16} aria-hidden="true" /> : <Save size={16} aria-hidden="true" />}{saving ? '保存中…' : message && !message.error && !dirty ? '保存済み' : '保存'}
      </button>
    </div>
    {name.trim() && !nameCheck.ok && <p id="nickname-help" role="alert" className="ps-help" data-error>{nameCheck.message}</p>}
    <dl className="ps-stats">
      <div><dt><Flame size={15} aria-hidden="true" />連続</dt><dd>{streak}<small>日</small></dd></div>
      <div><dt><Clock size={15} aria-hidden="true" />学習時間</dt><dd>{formatStudyTime(studySeconds)}</dd></div>
      <div><dt><BookOpen size={15} aria-hidden="true" />修了</dt><dd>{completedCount}<small>章</small></dd></div>
    </dl>
    <div className="ps-badges" aria-label={`獲得バッジ ${earnedBadges.length}個`}>
      <span>バッジ {earnedBadges.length}/{BADGES.length}</span>
      {earnedBadges.length === 0 ? <small>対戦や復習で集まります</small> : earnedBadges.slice(0, 3).map(b => <i key={b.id} title={b.desc}>{b.label}</i>)}
      {earnedBadges.length > 3 && <small>ほか{earnedBadges.length - 3}個</small>}
    </div>
    <div className="ps-fields">
      <label className="ps-select"><GraduationCap size={15} aria-hidden="true" /><span className="sr-only">学年</span>
        <input value={grade} onChange={e => edit(setGrade)(e.target.value)} placeholder="学年（例：高校1年）" /><Pencil size={15} aria-hidden="true" />
      </label>
      <label className="ps-select"><Compass size={15} aria-hidden="true" /><span className="sr-only">文理</span>
        <select value={stream} onChange={e => edit(setStream)(e.target.value)}>
          <option value="science">理系</option><option value="humanities">文系</option><option value="other">その他</option>
        </select><ChevronDown size={16} aria-hidden="true" />
      </label>
      <label className="ps-select" data-target-school><School size={15} aria-hidden="true" /><span className="sr-only">志望校</span>
        <input value={targetSchool} maxLength={TARGET_SCHOOL_MAX} onChange={e => edit(setTargetSchool)(e.target.value)} placeholder="志望校" aria-invalid={!schoolCheck.ok || undefined} /><Pencil size={15} aria-hidden="true" />
      </label>
      <label className="ps-select" data-target-goal><GraduationCap size={15} aria-hidden="true" /><span className="sr-only">目標レベル（単語帳の範囲）</span>
        <select value={goal} onChange={e => edit(setGoal)(e.target.value as GoalId)}>
          {GOAL_OPTIONS.map(o => <option key={o.id} value={o.id}>{o.label}</option>)}
        </select><ChevronDown size={16} aria-hidden="true" />
      </label>
      <label className="ps-select mypage-profile-motto" data-motto><Compass size={15} aria-hidden="true" /><span className="sr-only">志（ひとこと）</span>
        <input value={motto} maxLength={MOTTO_MAX} onChange={e => edit(setMotto)(e.target.value)} placeholder="志（例：医者になって地元を支える）" aria-invalid={!mottoCheck.ok || undefined} /><Pencil size={15} aria-hidden="true" />
      </label>
    </div>
    {!schoolCheck.ok && <p role="alert" className="ps-help" data-error>{schoolCheck.message?.replace('名前', '志望校')}</p>}
    {!mottoCheck.ok && <p role="alert" className="ps-help" data-error>{mottoCheck.message?.replace('名前', '志')}</p>}
    <div className="ps-toggle-row mypage-profile-public">
      <div className="ps-toggle-text"><p>プロフィールを公開</p></div>
      <button type="button" role="switch" aria-checked={profilePublic} aria-label="プロフィールを公開（志望校・志・学習時間・達成ステージを他の人に表示）" className="ps-switch"
        onClick={() => { if (auth.currentUser && publicationReady) { setProfilePublic(p => !p); setDirty(true); setMessage(null); } else setMessage({ text: 'Googleログインと公開設定の確認が必要です。', error: true }); }}><span /></button>
    </div>
    {message && <p className="ps-help" role={message.error ? 'alert' : 'status'} data-error={message.error || undefined}>{message.text}</p>}
  </section>;
}
