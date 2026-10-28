import { describe, expect, it } from 'vitest';
import {
  addDays, byMaterial, bySubject, currentStreak, deleteMaterial, deleteRecord, emptyStore, mergeStores, monthGrid, parseStore,
  setGoals, setRecordPost, summarize, upsertMaterial, upsertRecord, validateMaterial, validateRecord, weekStart, dayOf, noonOf,
  type ManualLogStore, type RecordInput,
} from '../src/features/studylog/manualLogCore';

// 2026-10-28（水）12:00（端末の時刻）
const NOW = new Date(2026, 9, 28, 12).getTime();
const rec = (over: Partial<RecordInput> = {}): RecordInput => ({ day: '2026-10-28', subject: 'math', materialName: '青チャート', minutes: 30, ...over });
const add = (s: ManualLogStore, over: Partial<RecordInput> = {}, now = NOW) => upsertRecord(s, rec(over), now).store;

describe('日付', () => {
  it('週は月曜はじまり・月末をまたいでも正しい', () => {
    expect(weekStart('2026-10-28')).toBe('2026-10-26');
    expect(weekStart('2026-11-01')).toBe('2026-10-26'); // 日曜
    expect(weekStart('2026-11-02')).toBe('2026-11-02'); // 月曜
    expect(addDays('2026-12-31', 1)).toBe('2027-01-01');
    expect(dayOf(noonOf('2026-03-29'))).toBe('2026-03-29');
  });
  it('深夜0時直前・直後は端末の日付で分かれる（UTC に直さない）', () => {
    expect(dayOf(new Date(2026, 9, 27, 23, 59).getTime())).toBe('2026-10-27');
    expect(dayOf(new Date(2026, 9, 28, 0, 1).getTime())).toBe('2026-10-28');
  });
  it('カレンダーは月曜はじまりで7の倍数', () => {
    const g = monthGrid('2026-10');
    expect(g.length % 7).toBe(0);
    expect(g.indexOf('2026-10-01')).toBe(3); // 10/1 は木曜
    expect(g.filter(Boolean)).toHaveLength(31);
  });
});

describe('記録の入力チェック', () => {
  const s = emptyStore();
  it('ふつうの記録は通る・過去の日付も記録できる', () => {
    expect(validateRecord(rec(), s, NOW)).toBeNull();
    expect(validateRecord(rec({ day: '2025-04-01' }), s, NOW)).toBeNull();
  });
  it('0分・12時間超・未来・2年より前・教科なしは止める', () => {
    expect(validateRecord(rec({ minutes: 0 }), s, NOW)).toBe('minutes_low');
    expect(validateRecord(rec({ minutes: -5 }), s, NOW)).toBe('minutes_low');
    expect(validateRecord(rec({ minutes: 721 }), s, NOW)).toBe('minutes_high');
    expect(validateRecord(rec({ day: '2026-10-29' }), s, NOW)).toBe('future');
    expect(validateRecord(rec({ day: '2024-10-01' }), s, NOW)).toBe('too_old');
    expect(validateRecord(rec({ subject: 'xx' }), s, NOW)).toBe('subject');
    expect(validateRecord(rec({ day: '2026-02-30' }), s, NOW)).toBe('day');
  });
  it('同じ日の合計が24時間をこえると止める（編集中の記録は数えない）', () => {
    let t = add(s, { minutes: 720 });
    t = add(t, { minutes: 700 });
    expect(validateRecord(rec({ minutes: 30 }), t, NOW)).toBe('day_total');
    const id = t.records[0].id;
    expect(validateRecord(rec({ minutes: 710 }), t, NOW, id)).toBeNull();
  });
});

describe('記録の追加・編集・削除', () => {
  it('編集すると同じIDのまま中身が変わり、作成日時は残る', () => {
    const a = upsertRecord(emptyStore(), rec(), NOW);
    const b = upsertRecord(a.store, rec({ minutes: 45, comment: '  模試の復習  ' }), NOW + 1000, a.record.id);
    expect(b.store.records).toHaveLength(1);
    expect(b.record.id).toBe(a.record.id);
    expect(b.record.createdAt).toBe(NOW);
    expect(b.record.minutes).toBe(45);
    expect(b.record.comment).toBe('模試の復習');
    expect(b.record.kind).toBe('manual');
    expect(b.record.visibility).toBe('private'); // 初期は自分だけ
  });
  it('削除は印を残して集計から外れる・90日で印も消える', () => {
    const a = upsertRecord(emptyStore(), rec(), NOW);
    const d = deleteRecord(a.store, a.record.id, NOW + 1);
    expect(d.records[0].deleted).toBe(true);
    expect(summarize(d, { total: 0, days: {} }, NOW).all.self).toBe(0);
    const later = deleteRecord(d, 'none', NOW + 91 * 86400000);
    expect(later.records).toHaveLength(0);
  });
  it('共有の印を付け外しできる', () => {
    const a = upsertRecord(emptyStore(), rec(), NOW);
    const p = setRecordPost(a.store, a.record.id, 'post1', NOW + 1);
    expect(p.records[0]).toMatchObject({ postId: 'post1', visibility: 'friends' });
    const q = setRecordPost(p, a.record.id, undefined, NOW + 2);
    expect(q.records[0].postId).toBeUndefined();
    expect(q.records[0].visibility).toBe('private');
  });
});

describe('教材', () => {
  it('登録して記録で選べる・名前を変えると過去の記録の名前もそろう', () => {
    const m = upsertMaterial(emptyStore(), { name: '青チャート', subject: 'math', type: '参考書', goalMinutes: 600 }, NOW);
    let s = upsertRecord(m.store, rec({ materialId: m.material.id, materialName: '' }), NOW).store;
    expect(s.records[0].materialName).toBe('青チャート');
    s = upsertMaterial(s, { name: '青チャートII', subject: 'math', type: '参考書' }, NOW + 1, m.material.id).store;
    expect(s.records[0].materialName).toBe('青チャートII');
    const stat = byMaterial(s).find(x => x.materialId === m.material.id)!;
    expect(stat.seconds).toBe(1800);
  });
  it('教材を消しても過去の記録と教材名は残る', () => {
    const m = upsertMaterial(emptyStore(), { name: '化学の新演習', subject: 'chem' }, NOW);
    let s = upsertRecord(m.store, rec({ subject: 'chem', materialId: m.material.id, materialName: '' }), NOW).store;
    s = deleteMaterial(s, m.material.id, NOW + 1);
    expect(s.records[0].materialName).toBe('化学の新演習');
    expect(byMaterial(s)[0]).toMatchObject({ label: '化学の新演習', seconds: 1800 });
  });
  it('同じ教科の同じ名前・空の名前は止める', () => {
    const m = upsertMaterial(emptyStore(), { name: '英単語ターゲット', subject: 'eng' }, NOW);
    expect(validateMaterial({ name: '英単語ターゲット', subject: 'eng' }, m.store)).toBe('duplicate');
    expect(validateMaterial({ name: '英単語ターゲット', subject: 'eng' }, m.store, m.material.id)).toBeNull();
    expect(validateMaterial({ name: '  ', subject: 'eng' }, m.store)).toBe('name');
  });
});

describe('集計', () => {
  it('今日・今週・今月・累計をアプリ計測と自分の記録に分けて出す（二重に数えない）', () => {
    let s = add(emptyStore(), { minutes: 30 });                 // 今日
    s = add(s, { day: '2026-10-26', minutes: 60 });            // 今週（月曜）
    s = add(s, { day: '2026-10-25', minutes: 10 });            // 先週の日曜・今月
    s = add(s, { day: '2026-09-30', minutes: 20 });            // 先月
    const app = { total: 9000, days: { '2026-10-28': 600, '2026-10-26': 1200, '2026-09-01': 7200 } };
    const sum = summarize(s, app, NOW);
    expect(sum.today).toEqual({ app: 600, self: 1800, total: 2400 });
    expect(sum.week).toEqual({ app: 1800, self: 5400, total: 7200 });
    expect(sum.month.self).toBe(6000);
    expect(sum.month.app).toBe(1800);
    expect(sum.all).toEqual({ app: 9000, self: 7200, total: 16200 });
    expect(sum.last7.map(d => d.day)).toEqual(['2026-10-22', '2026-10-23', '2026-10-24', '2026-10-25', '2026-10-26', '2026-10-27', '2026-10-28']);
  });
  it('連続日数：今日まだでも昨日まで続いていれば数える', () => {
    const days = new Set(['2026-10-25', '2026-10-26', '2026-10-27']);
    expect(currentStreak(days, NOW)).toBe(3);
    expect(currentStreak(new Set(['2026-10-25']), NOW)).toBe(0);
  });
  it('教科別は記録の多い順、アプリ内の時間は「マナトビ」としてまとめる', () => {
    let s = add(emptyStore(), { subject: 'eng', minutes: 10 });
    s = add(s, { subject: 'math', minutes: 50 });
    const b = bySubject(s, 600);
    expect(b.map(x => x.key)).toEqual(['math', 'eng', 'app']);
  });
  it('目標を保存できる（範囲外は捨てる）', () => {
    const s = setGoals(emptyStore(), { dailyMinutes: 90, weeklyMinutes: 0 }, NOW);
    expect(s.goals.dailyMinutes).toBe(90);
    expect(s.goals.weeklyMinutes).toBeUndefined();
  });
});

describe('読み込みと端末どうしの合わせ方', () => {
  it('壊れた値・知らない値は捨てる', () => {
    expect(parseStore(null).records).toEqual([]);
    const s = parseStore({ version: 1, records: [{ id: 'x', day: 'bad' }, { id: 'y', day: '2026-10-01', createdAt: 1, updatedAt: 1, subject: 'math', minutes: 99999, materialName: '' }], materials: [{}], goals: { dailyMinutes: -1 } });
    expect(s.records).toEqual([]);
    expect(s.materials).toEqual([]);
    expect(s.goals).toEqual({});
  });
  it('両方の端末で足した記録は両方残り、片方で消した記録は消える', () => {
    const base = upsertRecord(emptyStore(), rec(), NOW);
    const a = add(base.store, { subject: 'eng' }, NOW + 10);           // 端末A で追加
    const b = deleteRecord(add(base.store, { subject: 'bio' }, NOW + 20), base.record.id, NOW + 30); // 端末B で追加・削除
    const m = mergeStores(a, b, NOW + 40);
    const live = m.records.filter(r => !r.deleted).map(r => r.subject).sort();
    expect(live).toEqual(['bio', 'eng']);
    expect(mergeStores(b, a, NOW + 40).records.filter(r => !r.deleted)).toHaveLength(2);
  });
  it('同じ記録を両方で直したら新しい方', () => {
    const base = upsertRecord(emptyStore(), rec(), NOW);
    const a = upsertRecord(base.store, rec({ minutes: 40 }), NOW + 10, base.record.id).store;
    const b = upsertRecord(base.store, rec({ minutes: 50 }), NOW + 20, base.record.id).store;
    expect(mergeStores(a, b).records[0].minutes).toBe(50);
    expect(mergeStores(b, a).records[0].minutes).toBe(50);
  });
});

describe('あとから教材を登録', () => {
  it('同じ教科・同じ名前の記録だけがひもづく', async () => {
    const { linkRecordsToMaterial } = await import('../src/features/studylog/manualLogCore');
    let s = add(emptyStore(), { subject: 'math', materialName: 'フォーカスゴールド' });
    s = add(s, { subject: 'eng', materialName: 'フォーカスゴールド' });
    const m = upsertMaterial(s, { name: 'フォーカスゴールド', subject: 'math' }, NOW);
    const linked = linkRecordsToMaterial(m.store, m.material.id, NOW + 1);
    expect(linked.records.filter(r => r.materialId === m.material.id)).toHaveLength(1);
    expect(byMaterial(linked).find(x => x.materialId === m.material.id)?.seconds).toBe(1800);
  });
});
