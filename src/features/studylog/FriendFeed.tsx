/**
 * 学習記録ページの「フレンド」：フレンドが共有した記録（新しい順・20件ずつ）とリアクション。
 *   読めるのはルールでフレンドだけ。ブロックした人は出さない。名前を押すとその人のプロフィール。
 *   個別チャット・自由コメントは作らない（リアクションだけ）。
 */
import { useCallback, useEffect, useState } from 'react';
import { auth } from '../../firebase';
import { fetchFriendUids } from '../../utils/friends';
import { displaySafeNickname, displaySafePublicText } from '../safety/nicknameFilter';
import { useWithoutBlocked } from '../safety/useBlockedFilter';
import { UserSafetyMenu } from '../safety/UserSafetyMenu';
import { UserProfileDialog, type ProfileTarget } from '../profile/UserProfileDialog';
import '../profile/public-profile.css';
import { subjectLabel } from './manualLogCore';
import { REACTIONS, fetchFeed, fetchReactions, setReaction, type ReactionSummary, type ReactionType, type StudyPost } from './studyFeed';
import { fmtDay, fmtMin } from './ui';

export function FriendFeed({ onOpenFriends, onToast }: { onOpenFriends?: () => void; onToast?: (m: string) => void }) {
  const me = auth.currentUser?.uid || '';
  const [posts, setPosts] = useState<StudyPost[]>([]);
  const [reactions, setReactions] = useState<Record<string, ReactionSummary>>({});
  const [friendCount, setFriendCount] = useState<number | null>(null);
  const [state, setState] = useState<'idle' | 'loading' | 'more' | 'error'>('idle');
  const [hasMore, setHasMore] = useState(false);
  const [error, setError] = useState('');
  const [openProfile, setOpenProfile] = useState<ProfileTarget | null>(null);
  const [uids, setUids] = useState<string[]>([]);

  const load = useCallback(async (before?: number) => {
    if (!me) return;
    setState(before ? 'more' : 'loading'); setError('');
    try {
      const ids = before ? uids : await fetchFriendUids(true);
      if (!before) { setUids(ids); setFriendCount(ids.filter(u => u !== me).length); }
      const page = await fetchFeed(ids, before);
      setPosts(prev => {
        const by = new Map<string, StudyPost>((before ? prev : []).map(p => [p.id, p] as const));
        page.posts.forEach(p => by.set(p.id, p));
        return [...by.values()].sort((a, b) => b.createdAt - a.createdAt);
      });
      setHasMore(page.hasMore);
      const r = await fetchReactions(page.posts.map(p => p.id));
      setReactions(prev => ({ ...(before ? prev : {}), ...r }));
      setState('idle');
    } catch (e) {
      setError(e instanceof Error ? e.message : '読み込めませんでした。'); setState('error');
    }
  }, [me, uids]);
  useEffect(() => { void load(); }, [me]); // eslint-disable-line react-hooks/exhaustive-deps

  const visible = useWithoutBlocked<StudyPost>(posts);
  const react = async (post: StudyPost, type: ReactionType) => {
    const cur = reactions[post.id] ?? { counts: { cheer: 0, nice: 0 }, mine: null };
    const next: ReactionType | null = cur.mine === type ? null : type;
    const counts = { ...cur.counts };
    if (cur.mine) counts[cur.mine] = Math.max(0, counts[cur.mine] - 1);
    if (next) counts[next] += 1;
    setReactions(r => ({ ...r, [post.id]: { counts, mine: next } }));
    try { await setReaction(post.id, next); }
    catch (e) { setReactions(r => ({ ...r, [post.id]: cur })); onToast?.(e instanceof Error ? e.message : '送れませんでした。'); }
  };

  if (!me) return <div className="slog-empty"><p>フレンドの記録を見るにはGoogleログインが必要です。</p></div>;
  if (state === 'loading' && !posts.length) return <div className="mt-loading" role="status"><i aria-hidden="true" />読み込んでいます…</div>;
  return <>
    {error && <p className="slog-error" role="alert">{error} <button type="button" className="slog-more" onClick={() => void load()}>もう一度</button></p>}
    <div className="slog-scroll" tabIndex={0} aria-label="フレンドの学習記録" data-friend-feed>
      {!visible.length && state !== 'error'
        ? <div className="slog-empty" data-feed-empty>
            <p>{friendCount === 0 ? 'まだフレンドがいません。フレンドを追加すると、共有した学習記録がここに並びます。' : 'まだ共有された記録はありません。記録するときに「フレンドに共有」をオンにすると、ここに出ます。'}</p>
            {friendCount === 0 && onOpenFriends && <button type="button" className="mt-btn mt-btn-primary" onClick={onOpenFriends}>フレンドを追加する</button>}
          </div>
        : <ul className="slog-rows">{visible.map(p => {
            const mine = p.uid === me;
            const name = displaySafeNickname(p.nickname);
            const r = reactions[p.id] ?? { counts: { cheer: 0, nice: 0 }, mine: null };
            return <li key={p.id}><article className="slog-post" data-post={p.id}>
              <header>
                {mine ? <strong>あなた</strong> : <button type="button" className="pp-open" onClick={() => setOpenProfile({ uid: p.uid, nickname: name, where: 'friend' })} aria-label={`${name} さんのプロフィールを見る`}><strong>{name}</strong></button>}
                <span className="slog-tag" data-tone="self">自分で記録</span>
                <time dateTime={p.day}>{fmtDay(p.day, true)}</time>
                {!mine && <UserSafetyMenu target={{ uid: p.uid, nickname: name, where: 'friend' }} />}
              </header>
              <p>{subjectLabel(p.subject)}{p.materialName ? `・${displaySafePublicText(p.materialName)}` : ''}　<b>{fmtMin(p.minutes)}</b>{p.amount != null ? `（${p.amount}${p.amountUnit ?? ''}）` : ''}</p>
              {p.comment && <p className="comment">{displaySafePublicText(p.comment, 140)}</p>}
              <footer>
                {REACTIONS.map(x => mine
                  ? <span key={x.type} className="slog-tag">{x.label} {r.counts[x.type]}</span>
                  : <button key={x.type} type="button" className="slog-react" aria-pressed={r.mine === x.type} onClick={() => void react(p, x.type)} data-react={x.type}>{x.label}<b>{r.counts[x.type]}</b></button>)}
              </footer>
            </article></li>;
          })}</ul>}
      {hasMore && <button type="button" className="mt-btn mt-btn-secondary mt-btn-block" disabled={state === 'more'} onClick={() => void load(posts.at(-1)?.createdAt)} data-feed-more>{state === 'more' ? '読み込み中…' : 'もっと見る'}</button>}
      <p className="slog-note">共有された時間は本人の自己申告です。見られるのはフレンドどうしだけです。</p>
    </div>
    <UserProfileDialog target={openProfile} onClose={() => setOpenProfile(null)} />
  </>;
}
