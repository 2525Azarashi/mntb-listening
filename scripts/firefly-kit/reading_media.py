"""英文解釈（リーディング）に入れる動画・図のプロンプト（2026-10-24）。

1. READING_VIDEOS … 画面の演出動画（Firefly Video・とびら君）。全画面ではなく、読む画面の上部・結果画面に小さく出す
2. PASSAGE_ART    … 英文60本それぞれの「扉絵」（Firefly Image）。読む前に1枚だけ見せて、内容を想像させる
3. BOOK_FIGURES   … UR 本「リーディング大問別演習」の図・イラスト（本番は図表が第4問以外の全大問に出る）

扉絵と図は「Firefly Image」（Text to image）で作る。文字・数字はプロンプトで禁止し、数字の入るグラフは
アプリ側（PDF を作るスクリプト）で描くので、ここでは「イラスト」だけを作る。
"""

IMG_STYLE = ("Soft flat illustration for a Japanese study app, warm pastel colors, clean shapes, gentle light, "
             "no text, no letters, no numbers, no logos, no watermark. Square composition with empty space around the subject.")

# ── 1. 読む画面の演出動画（とびら君） ─────────────────────────────
READING_VIDEOS = [
  dict(id='R01', name='read_start', kind='motion', first='green:studying', last='green:studying', loop=True, sec='3.0', prio='A',
       where='英文解釈：読み始めの画面（ReadingQuiz.tsx の上部）。読んでいる間くり返し',
       ja='本を広げて読み、指で行をなぞる → ページを1枚めくる（くり返し）',
       action='The character sits reading a blue book, follows a line with one finger, turns one page and keeps reading with interest. Seamless loop.'),
  dict(id='R02', name='read_think', kind='motion', first='green:thinking', last='green:thinking', loop=True, sec='2.4', prio='A',
       where='英文解釈：設問を考えているとき',
       ja='あごに手を当てて考え、うなずく（くり返し）',
       action='The character holds its chin and thinks carefully, eyes moving as if reading, then gives a small nod. Seamless loop.'),
  dict(id='R03', name='read_evidence', kind='motion', first='green:good', last='green:good', loop=False, sec='2.0', prio='A',
       where='英文解釈：根拠の一文がハイライトされたとき（正解）',
       ja='「ここだ！」と鉛筆で前を指し、ウインク',
       action='The character points the pencil forward as if pointing at a sentence, its face lights up, and it winks at the viewer.'),
  dict(id='R04', name='read_retry', kind='motion', first='green:thinking', last='green:basic', loop=False, sec='2.0', prio='A',
       where='英文解釈：不正解のとき（もう一度本文へ）',
       ja='首をかしげる → 本をのぞき込む → 「もう一回読もう」とうなずく',
       action='The character tilts its head, leans forward to look at an open book again, then nods encouragingly to the viewer.'),
  dict(id='R05', name='read_clear', kind='cinema', first='cream:studying', last='cream:cheering', loop=False, sec='3.0', prio='A',
       where='英文解釈：1本読み終えた結果画面',
       ja='本をぱたんと閉じる → 立ち上がってバンザイ → 本のページが数枚ふわっと舞う',
       action='The character closes the blue book with a satisfied smile, stands up and raises both arms in a banzai, a few blank white pages flutter softly around it.'),
  dict(id='R06', name='read_levelup', kind='cinema', first='cream:basic', last='cream:trophy', loop=False, sec='3.0', prio='B',
       where='英文解釈：レベル（Lv1〜5）を全部読み終えたとき',
       ja='本が5冊積み上がり、いちばん上に金色の本 → とびら君が金の本をかかげる',
       action='Five books stack up one by one next to the character, the top one glows gold, the character lifts the golden book above its head proudly. The book covers are plain with no text.'),
  dict(id='R07', name='mock_start', kind='cinema', first='cream:good', last='cream:good', loop=False, sec='2.5', prio='B',
       where='UR リーディング大問別演習を開いたとき（本の表紙の前）',
       ja='とびら君が鉛筆を構えて「よし、80分！」とうなずく → 背景に時計の針がひと回りする影',
       action='The character grips the pencil in a ready stance and nods firmly, the soft shadow of a clock hand sweeps once around on the wall behind it.'),
]

# ── 2. 英文60本の扉絵（Firefly Image） ─────────────────────────────
# (id, 題名, 絵の中身)
PASSAGE_ART = [
 ('r1-01', 'The Library Cat', 'a sleepy orange cat curled up on a wooden library shelf between books, afternoon sunlight from a window'),
 ('r1-02', 'The Bus Stop Bookshelf', 'a small wooden bookshelf at a rural bus stop with a bench, a few books, green hills behind'),
 ('r1-03', 'A Tree for Every Baby', 'a young sapling planted in a park with a tiny ribbon tied to it, a family silhouette in the distance'),
 ('r1-04', 'The Lost Umbrella', 'a single bright yellow umbrella left on a train platform bench on a rainy day'),
 ('r1-05', 'Learning to Ride at Sixty', 'an older woman happily riding a bicycle on a quiet riverside path, a helper waving'),
 ('r1-06', 'Message in a Bottle', 'a glass bottle with a rolled paper inside washed up on a sandy beach at sunset'),
 ('r1-07', 'The Night Market', 'a lively Asian night market street with glowing lanterns and food stalls, warm colors'),
 ('r1-08', 'A Robot in the Classroom', 'a friendly small robot standing at the front of a classroom with students raising hands'),
 ('r1-09', "Grandma's Recipe Book", 'an old handwritten-looking recipe notebook open on a kitchen table with flour and a wooden spoon'),
 ('r1-10', 'A Week Without Phones', 'a smartphone locked inside a small box while teenagers play a board game together'),
 ('r1-11', 'The Quiet Hour', 'a calm school library with students reading silently, a wall clock, soft light'),
 ('r1-12', 'A Garden on the School Roof', 'a vegetable garden on a school rooftop with tomatoes and students watering plants, city behind'),
 ('r2-01', 'Why We Forget Names', 'two people shaking hands, one looking puzzled with a faint question-mark-shaped cloud above, no letters'),
 ('r2-02', 'The Four-Day Week', 'a weekly calendar shape with three relaxed days highlighted in green, a person enjoying a park'),
 ('r2-03', 'Bees in the City', 'beehives on a city rooftop surrounded by flowers and skyscrapers'),
 ('r2-04', 'The Power of Handwriting', 'a hand writing in a notebook with a pencil next to a closed laptop'),
 ('r2-05', 'Sleeping on It', 'a student asleep on a pillow with a gentle glowing light bulb shape floating above'),
 ('r2-06', 'Small Shops, Big Changes', 'a small local shopping street with a bakery and a bookshop, people chatting'),
 ('r2-07', 'Learning a Language Later in Life', 'an elderly man with headphones practicing with flash cards at a desk, smiling'),
 ('r2-08', 'Why Ice Floats', 'ice cubes floating in a clear glass of water, simple scientific feel'),
 ('r2-09', 'Reviews You Can Trust?', 'a phone screen showing star-shaped icons with a magnifying glass over it, no text'),
 ('r2-10', 'The Walking Meeting', 'three coworkers talking while walking in a green park'),
 ('r2-11', 'A Second Life for Old Phones', 'old smartphones being collected in a recycling box, green arrows forming a circle'),
 ('r2-12', 'The Myth of the Ten Percent Brain', 'a stylized brain glowing all over in soft colors'),
 ('r3-01', 'The Paradox of Choice', 'a supermarket shelf with dozens of jam jars and a confused shopper'),
 ('r3-02', 'Plastic That Disappears?', 'a plastic bag slowly breaking into leaves and soil'),
 ('r3-03', 'The Myth of Learning Styles', 'three students learning in different ways: listening, drawing, reading, under one teacher'),
 ('r3-04', 'Food Miles', 'a world map with dotted routes of a truck, ship and airplane carrying fruit'),
 ('r3-05', 'Praise and Effort', 'a teacher giving a thumbs-up to a student climbing steps of books'),
 ('r3-06', 'When Silent Reading Was Strange', 'a medieval monk reading a book aloud by candlelight'),
 ('r3-07', 'The Wisdom of Crowds', 'many people guessing the weight of a large ox at a country fair'),
 ('r3-08', 'Robots and Jobs', 'a factory robot arm working next to a human worker, both friendly'),
 ('r3-09', 'Why We Procrastinate', 'a student at a desk looking at a phone while a pile of homework waits'),
 ('r3-10', 'Endangered Languages', 'an elder telling stories to children around a fire, speech bubbles without words'),
 ('r3-11', 'The Value of Doing Nothing', 'a person lying on grass looking at clouds, peaceful'),
 ('r3-12', 'Urban Trees', 'a city street lined with big shady trees, people walking in the shade'),
 ('r4-01', 'The Myth of the Multitasker', 'a person juggling a phone, laptop, coffee and book, looking stressed'),
 ('r4-02', 'Who Owns English?', 'people from many countries chatting around a globe'),
 ('r4-03', 'The Price of "Free"', 'a gift box with a hidden price-tag-shaped shadow behind it, no numbers'),
 ('r4-04', 'Learning from Failure', 'a team looking at a broken model airplane on a table and planning together'),
 ('r4-05', 'The Urban Heat Island', 'a hot city with orange glow above dark rooftops, green countryside cooler nearby'),
 ('r4-06', 'In Praise of Boredom', 'a child staring out of a rainy window, then imagining a colorful dream'),
 ('r4-07', 'Beyond GDP', 'a balance scale with coins on one side and a happy family and a tree on the other'),
 ('r4-08', 'Is a Tomato a Fruit?', 'a red tomato between a basket of fruit and a basket of vegetables'),
 ('r4-09', 'Do Grades Motivate?', 'a student holding a report card shape with a thoughtful face, no letters'),
 ('r4-10', 'The Return of the Wolves', 'wolves in a snowy forest valley with a river and trees growing back'),
 ('r4-11', 'Reading on Screens', 'a paper book and a tablet side by side on a desk'),
 ('r4-12', 'The Placebo Puzzle', 'two identical white pills on a doctor\'s desk, one glowing softly'),
 ('r5-01', 'The Map and the Territory', 'a folded paper map lying on top of a real mountain landscape'),
 ('r5-02', 'The Tyranny of Metrics', 'people running on a giant measuring ruler toward a finish line'),
 ('r5-03', 'Memory as Reconstruction', 'puzzle pieces of a family photo being put back together, some pieces different colors'),
 ('r5-04', 'The Problem of Other Minds', 'two people facing each other with glass-like transparent heads showing different colors inside'),
 ('r5-05', 'Risk and Perception', 'a person nervous on an airplane but relaxed in a car, split scene'),
 ('r5-06', 'The Division of Cognitive Labor', 'a doctor, a pilot and an engineer each holding their tools, people trusting them'),
 ('r5-07', 'Translation and Loss', 'a bridge between two islands with words turning into colorful birds, no letters'),
 ('r5-08', 'Antibiotics and Evolution', 'bacteria under a microscope with a few stronger ones glowing'),
 ('r5-09', 'The Paradox of Tolerance', 'an open door with a gentle barrier line in front of it, calm colors'),
 ('r5-10', 'Why Do We Sleep?', 'a sleeping person with gentle waves and stars flowing around the head'),
 ('r5-11', 'History and Hindsight', 'a person looking back at a winding road behind them that looks clear, foggy road ahead'),
 ('r5-12', 'The Limits of Prediction', 'a weather forecaster looking at swirling clouds that become harder to see far away'),
]

# ── 3. UR 本の図・イラスト（大問別演習） ─────────────────────────────
BOOK_FIGURES = [
 ('F01', '第1回 第1問', 'お祭りの出店テーブルと絵本', 'a community festival table with picture books and a rug for children, near a gate with flags'),
 ('F02', '第1回 第2問', '図書館の自習ラウンジ', 'a bright library study lounge with desks, power sockets and soundproof booths'),
 ('F03', '第1回 第3問', '台湾の夜市', 'a Taiwanese night market street with lanterns, bubble tea and grilled corn stalls'),
 ('F04', '第1回 第5問', '川の科学キャンプ（ドローン）', 'teenagers by a river with a drone flying above and nets for river animals'),
 ('F05', '第1回 第6問', '坂の上の時計店', 'an old clock shop window with many clocks showing different times, rainy street'),
 ('F06', '第1回 第7問 問2', '忘却曲線（グラフの形の参考）', 'a simple smooth curve falling sharply then leveling off, drawn as a clean line on a plain background, no axes labels'),
 ('F07', '第1回 第8問', 'AIと宿題', 'a student at a desk with a laptop showing a friendly AI helper icon, homework papers'),
 ('F08', '第2回 第1問', '農場の収穫祭', 'an apple orchard and pumpkin patch with a hay wagon and a red barn in autumn'),
 ('F09', '第2回 第3問', '博物館の恐竜の部屋', 'children holding a fossil replica in a museum dinosaur hall with a skeleton'),
 ('F10', '第2回 第6問', '第2ヴァイオリン', 'a youth orchestra on stage, violin section in warm light'),
 ('F11', '第2回 第7問', '屋上緑化と白い屋根', 'city rooftops: one covered with plants and grass, one painted white, one dark, sunny sky'),
 ('F12', '第2回 第8問', '朝の通学と眠気', 'a sleepy teenager yawning at a bus stop in early morning light'),
]


def image_prompt(subject: str) -> str:
    return f'{subject}. {IMG_STYLE}'
