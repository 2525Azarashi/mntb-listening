/**
 * ほかの人の公開プロフィールを開く窓（2026-10-26）。
 *   ランキング・フレンド一覧の名前を押すと開く。見た目は既存の窓（.game-details-dialog.mt-dialog）と同じ。
 *   ・公開していない人（文書なし）… 「この人はプロフィールを公開していません」
 *   ・ブロックしている人 … 開かない（呼び出し側の一覧からも消えている）
 *   ・窓の右上に「通報・ブロック」（既存の UserSafetyMenu）
 */
import { useEffect, useRef, useState } from 'react';
import { Lock } from 'lucide-react';
import { fetchPublicStudyProfile, type PublicStudyProfile } from '../../utils/publicStudyProfile';
import { UserSafetyMenu } from '../safety/UserSafetyMenu';
import { isBlocked, type ReportTarget } from '../safety/userSafety';
import { displaySafeNickname } from '../safety/nicknameFilter';
import { PublicProfileView } from './PublicProfileView';

export interface ProfileTarget {
  uid: string;
  /** 一覧に出ている名前（公開文書に名前が無いときに使う） */
  nickname: string;
  where: ReportTarget['where'];
}

export function UserProfileDialog({ target, onClose }: { target: ProfileTarget | null; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [state, setState] = useState<{ uid: string; profile: PublicStudyProfile | null; loading: boolean; error: boolean }>({ uid: '', profile: null, loading: false, error: false });

  useEffect(() => {
    const d = dialog.current;
    if (!d) return;
    if (target && !isBlocked(target.uid)) {
      if (!d.open) d.showModal();
    } else if (d.open) d.close();
  }, [target]);

  useEffect(() => {
    if (!target) return;
    let alive = true;
    setState({ uid: target.uid, profile: null, loading: true, error: false });
    fetchPublicStudyProfile(target.uid)
      .then((profile) => { if (alive) setState({ uid: target.uid, profile, loading: false, error: false }); })
      .catch(() => { if (alive) setState({ uid: target.uid, profile: null, loading: false, error: true }); });
    return () => { alive = false; };
  }, [target]);

  const name = target ? displaySafeNickname(state.profile?.nickname || target.nickname || 'なまえ未設定') : '';

  return (
    <dialog
      ref={dialog}
      className="game-details-dialog mt-dialog"
      aria-labelledby="user-profile-title"
      data-user-profile-dialog
      onClose={onClose}
      onCancel={(e) => { e.preventDefault(); onClose(); }}
      onClick={(e) => { if (e.target === dialog.current) onClose(); }}
    >
      <header>
        <h2 id="user-profile-title">{name || 'プロフィール'}{name && <span className="sr-only"> さんのプロフィール</span>}</h2>
        {target && <UserSafetyMenu target={{ uid: target.uid, nickname: name, where: target.where }} />}
        <button type="button" autoFocus onClick={onClose}>閉じる</button>
      </header>
      <div className="game-details-body">
        {!target ? null : state.loading || state.uid !== target.uid ? (
          <div className="mt-loading" role="status"><i aria-hidden="true" />読み込んでいます…</div>
        ) : state.error ? (
          <p role="alert" className="ps-help" data-error>読み込めませんでした。通信を確認して、もう一度開いてください。</p>
        ) : state.profile ? (
          <PublicProfileView profile={state.profile} fallbackName={target.nickname} />
        ) : (
          <div className="pp-private" data-profile-private>
            <Lock size={28} aria-hidden="true" />
            <p>この人はプロフィールを公開していません。</p>
          </div>
        )}
      </div>
    </dialog>
  );
}
