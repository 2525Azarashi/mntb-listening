// リスニング本（UR）用：アプリの問題データを JSON に書き出す
//   npx tsx scripts/gacha-prints/dump-listening.ts /tmp/listening.json
import { englishListeningData } from '../../src/data/englishListeningData';
import { writeFileSync } from 'node:fs';
const out: Record<string, unknown> = {};
for (const ch of englishListeningData.parts.flatMap(p => p.chapters)) {
  out[ch.id] = { title: ch.realTitle, group: ch.questionGroup, topics: ch.topics, points: ch.points, marks: ch.marks,
    readCount: ch.readCount, speakers: ch.speakers, problems: ch.practiceProblems };
}
writeFileSync(process.argv[2] ?? '/tmp/listening.json', JSON.stringify(out));
