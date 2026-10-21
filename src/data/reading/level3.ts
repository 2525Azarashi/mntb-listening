/** レベル3：応用（GMARCH・関関同立・地方国立）。150〜180語・設問3問 */
import { p, q } from './types';

export const LEVEL3 = [
  p('r3-01', 3, 'The Paradox of Choice', '選択肢が多すぎると', `
We usually assume that having more options makes us happier. If a café offers fifty kinds of coffee, surely everyone can find the perfect cup. Yet research suggests that too much choice can have the opposite effect.

In a famous experiment, a supermarket set up a table offering samples of jam. On some days, there were twenty-four flavors; on others, only six. The larger display attracted more visitors, but people were far more likely to actually buy jam when there were only six options.

Psychologists argue that a large number of choices increases the effort needed to decide and raises our expectations. After choosing, we are also more likely to wonder whether another option would have been better, which reduces our satisfaction. This does not mean that choice is bad. Rather, there seems to be a point beyond which additional options stop helping and start causing stress.`, [
    q('r3-01-1', 'ジャムの実験の結果として正しいものはどれか。', [
      '種類が多いほうが人は集まったが、実際に買う人は少なかった', '種類が多いほうが多く売れた', '種類が少ないと誰も立ち寄らなかった', '種類の数と買う人の割合に関係はなかった'],
      '「多い展示のほうが客を集めたが、実際に買う可能性は6種類のときのほうがはるかに高かった」。',
      'The larger display attracted more visitors, but people were far more likely to actually buy jam when there were only six options.'),
    q('r3-01-2', '選択肢が多いと満足度が下がる理由として本文が挙げているものはどれか。', [
      '選んだあとで、別のほうがよかったのではと考えやすくなるから', '選択肢が多いと値段が高くなるから', '店員の説明が不十分になるから', '品質の悪い商品が混ざるから'],
      '「選んだあとで、別の選択肢のほうがよかったのではと考えやすく、それが満足を下げる」。',
      'After choosing, we are also more likely to wonder whether another option would have been better, which reduces our satisfaction.'),
    q('r3-01-3', '筆者の考えとして最も適切なものはどれか。', [
      '選択肢はある程度を超えると、役に立たずストレスの原因になる', '選択肢はできるだけ少ないほうがよい', '選ぶこと自体が悪いことである', '選択肢は多ければ多いほど人を幸せにする'],
      '「選択が悪いという意味ではない。ある点を超えると、それ以上の選択肢は役立たずストレスを生む」。',
      'there seems to be a point beyond which additional options stop helping and start causing stress.'),
  ]),

  p('r3-02', 3, 'Plastic That Disappears?', '分解するプラスチック', `
"Biodegradable" plastic bags are sold as an environmentally friendly alternative to ordinary plastic. The word suggests that they will simply break down and return to nature. The reality is more complicated.

Many biodegradable plastics only break down under specific conditions, such as the high temperatures found in industrial composting facilities. In the ocean or in a home garden, they may last for years. In one study, researchers buried several types of "biodegradable" bags in soil and placed others in seawater. After three years, some of the bags were still strong enough to carry a full load of shopping.

There is also a risk that the label encourages careless behavior. If people believe a bag will disappear, they may be less careful about throwing it away. Experts therefore recommend reducing the use of single-use bags altogether, rather than relying on new materials to solve the problem.`, [
    q('r3-02-1', '多くの生分解性プラスチックについて本文で述べられていることはどれか。', [
      '特定の条件のもとでしか分解しない', 'どんな場所でも数週間で分解する', '海の中でいちばん早く分解する', '家庭の庭で使うと土を豊かにする'],
      '「多くは、工業用の堆肥施設の高温など特定の条件のもとでしか分解しない」。',
      'Many biodegradable plastics only break down under specific conditions'),
    q('r3-02-2', '3年後の実験結果が示しているものはどれか。', [
      '袋の中には、まだ買い物の荷物を運べるほど丈夫なものがあった', 'すべての袋が完全になくなっていた', '海水の中の袋だけが残っていた', '土の中の袋は植物の栄養になっていた'],
      '「3年後、いくつかの袋はまだ買い物の荷物いっぱいを運べるほど丈夫だった」。',
      'After three years, some of the bags were still strong enough to carry a full load of shopping.'),
    q('r3-02-3', '専門家が勧めていることはどれか。', [
      '使い捨ての袋の使用そのものを減らすこと', '生分解性の袋だけを使うこと', '袋を土に埋めて処分すること', '新しい素材の開発に期待すること'],
      '「新しい素材に頼るのではなく、使い捨ての袋の使用そのものを減らすこと」を勧めている。',
      'Experts therefore recommend reducing the use of single-use bags altogether, rather than relying on new materials to solve the problem.'),
  ]),

  p('r3-03', 3, 'The Value of Boredom', '退屈の価値', `
Modern life offers endless ways to avoid boredom. A few seconds of waiting in line are enough for many of us to take out our phones. But some psychologists believe that we are losing something valuable when we never allow ourselves to be bored.

When the mind has nothing to focus on, it begins to wander. This "mind-wandering" is not wasted time. It allows us to connect memories, imagine the future, and form new ideas. In one study, participants who first did a boring task, such as copying numbers from a phone book, later performed better on a test of creative thinking than those who had not.

Of course, boredom can be unpleasant, and long periods of it may lead to frustration. The point is not to seek boredom for its own sake, but to stop filling every empty moment automatically. A short walk without headphones may be more productive than it seems.`, [
    q('r3-03-1', '「心がさまようこと（mind-wandering）」について本文で述べられていることはどれか。', [
      '記憶を結びつけたり新しい考えを生んだりする', '時間のむだであり、避けるべきである', '集中力を大きく下げる', '長く続くと必ずいらだちにつながる'],
      '「心のさまよいは時間のむだではない。記憶を結びつけ、未来を想像し、新しい考えを生む」。',
      'It allows us to connect memories, imagine the future, and form new ideas.'),
    q('r3-03-2', '実験の結果として正しいものはどれか。', [
      '先に退屈な作業をした人のほうが、創造力のテストの成績がよかった', '退屈な作業をした人は、テストに集中できなかった', '電話帳の番号を写した人は、記憶力が上がった', '退屈な作業の有無で成績に差はなかった'],
      '「先に退屈な作業をした参加者は、そうでない人より創造的思考のテストでよい成績だった」。',
      'later performed better on a test of creative thinking than those who had not.'),
    q('r3-03-3', '筆者の主張として最も適切なものはどれか。', [
      '空いた時間をいつも自動的に何かで埋めるのをやめるべきだ', '退屈な時間をできるだけ長くつくるべきだ', 'スマホは完全に使うのをやめるべきだ', '退屈は不快なので避けるべきだ'],
      '「退屈そのものを求めるのではなく、すべての空いた時間を自動的に埋めるのをやめることが大切だ」。',
      'The point is not to seek boredom for its own sake, but to stop filling every empty moment automatically.'),
  ]),

  p('r3-04', 3, 'Why Cities Are Hotter', 'ヒートアイランド', `
On a summer afternoon, the center of a large city can be several degrees hotter than the surrounding countryside. This is known as the "urban heat island" effect.

There are several causes. Concrete and asphalt absorb sunlight during the day and release the heat slowly at night, so cities stay warm even after sunset. Tall buildings block the wind, which would otherwise carry heat away. In addition, cars, air conditioners, and factories produce heat directly. Ironically, air conditioners make the outside air hotter while cooling the inside.

Cities are trying different solutions. Some paint roofs white to reflect sunlight. Others plant trees, which provide shade and release water vapor that cools the air. In Tokyo, certain roads have been covered with a special surface that holds water and lowers the temperature as it evaporates. No single method is enough, but together they can make a noticeable difference.`, [
    q('r3-04-1', '都市が夜になっても暖かい理由として本文が挙げているものはどれか。', [
      'コンクリートなどが昼に熱を吸収し、夜にゆっくり放出するから', '夜も工場が熱を出しているから', '夜は風が強くなるから', '夜は日光が反射するから'],
      '「コンクリートとアスファルトは昼に日光を吸収し、夜にゆっくり熱を放出するので、日没後も暖かい」。',
      'Concrete and asphalt absorb sunlight during the day and release the heat slowly at night, so cities stay warm even after sunset.'),
    q('r3-04-2', '本文中の「皮肉にも（Ironically）」が指しているのはどれか。', [
      'エアコンは室内を冷やす一方で外の空気を暑くする', '高いビルが風をさえぎる', '白い屋根が日光を反射する', '木が日陰をつくる'],
      '「皮肉にも、エアコンは中を冷やしながら外の空気を暑くする」。',
      'Ironically, air conditioners make the outside air hotter while cooling the inside.'),
    q('r3-04-3', '対策について筆者はどう考えているか。', [
      '1つの方法では足りないが、組み合わせれば目に見える効果がある', '白い屋根が最も効果的である', '木を植えても効果はない', '対策はどれも費用がかかりすぎる'],
      '「1つの方法では十分ではないが、合わせれば目立つ違いを生む」。',
      'No single method is enough, but together they can make a noticeable difference.'),
  ]),

  p('r3-05', 3, 'The Myth of the Learning Style', '学習スタイルの思い込み', `
Many teachers and students believe that each person has a particular "learning style." According to this idea, visual learners learn best from pictures, auditory learners from listening, and so on. Teaching should therefore match each student's style.

The idea is popular, but researchers have found little evidence to support it. In carefully designed studies, students who were taught in their preferred style did not learn more than those who were taught in another way. People certainly have preferences, but preferring something is not the same as learning better from it.

What does seem to matter is matching the method to the content. Maps are best learned visually, and pronunciation is best learned by listening, regardless of the learner. Moreover, combining several methods, such as reading a text while looking at a diagram, tends to help almost everyone.`, [
    q('r3-05-1', '注意深く設計された研究で分かったことはどれか。', [
      '好みのスタイルで教わった学生が、よりよく学んだわけではなかった', '好みのスタイルで教わった学生のほうがよく学んだ', '視覚型の学生は聞くことが苦手だった', '学習スタイルは年齢とともに変わった'],
      '「好みのスタイルで教えられた学生は、別の方法で教えられた学生より多くを学ばなかった」。',
      'students who were taught in their preferred style did not learn more than those who were taught in another way.'),
    q('r3-05-2', '筆者が重要だと考えていることはどれか。', [
      '教え方を、学ぶ人ではなく学ぶ内容に合わせること', '学ぶ人の好みに合わせて教えること', '1つの方法だけで集中して教えること', '学生に自分の学習スタイルを調べさせること'],
      '「重要に思われるのは、方法を内容に合わせることだ」。地図は目で、発音は耳で、学習者に関係なく。',
      'What does seem to matter is matching the method to the content.'),
    q('r3-05-3', '本文の内容と一致するものはどれか。', [
      '複数の方法を組み合わせると、ほとんどの人の役に立つ', '人には学び方の好みがない', '発音は図を見て学ぶのがよい', '学習スタイルの考えには多くの証拠がある'],
      '最後の文「いくつかの方法を組み合わせることは、ほとんど誰にとっても助けになる傾向がある」。',
      'Moreover, combining several methods, such as reading a text while looking at a diagram, tends to help almost everyone.'),
  ]),

  p('r3-06', 3, 'Food Miles', 'フードマイル', `
"Buy local" has become a popular slogan among environmentally conscious shoppers. The reasoning seems clear: food that travels a shorter distance should produce less carbon dioxide. This distance is sometimes called "food miles."

However, transportation is often a small part of the total environmental cost of food. How the food is produced usually matters much more. For example, tomatoes grown in heated greenhouses in a cold country may produce more emissions than tomatoes grown outdoors in a warm country and shipped long distances by sea. Ships carry huge amounts of goods very efficiently, while a short trip by an individual car to a farm shop can be surprisingly costly per kilogram.

None of this means local food is a bad choice. It can be fresher and supports nearby farmers. But if the goal is to reduce emissions, what we eat, such as how much meat, may matter more than where it comes from.`, [
    q('r3-06-1', '「地元のものを買う」考え方の根拠として本文が説明しているものはどれか。', [
      '運ぶ距離が短い食べ物ほど二酸化炭素が少ないはずだという考え', '地元の食べ物のほうが安いという考え', '地元の農家は農薬を使わないという考え', '輸入品は品質が悪いという考え'],
      '「短い距離を運ばれる食べ物は二酸化炭素が少ないはずだ」という理屈。',
      'food that travels a shorter distance should produce less carbon dioxide.'),
    q('r3-06-2', 'トマトの例が示していることはどれか。', [
      '作り方のほうが運ぶ距離より環境への影響が大きいことがある', '船で運ぶと排出量が非常に多くなる', '温室で育てたトマトは環境にやさしい', '暖かい国のトマトは味が悪い'],
      '寒い国の暖房温室のトマトは、暖かい国で露地栽培し船で運んだものより排出量が多いことがある。「作り方のほうがずっと重要」の例。',
      'How the food is produced usually matters much more.'),
    q('r3-06-3', '筆者の結論として最も適切なものはどれか。', [
      '排出量を減らすには、どこから来たかより何を食べるかが重要かもしれない', '地元の食べ物は買うべきではない', '食べ物はすべて船で運ぶべきだ', '肉を食べても排出量には関係ない'],
      '「排出を減らすことが目的なら、どこから来たかより、何を（肉をどれだけ）食べるかのほうが重要かもしれない」。',
      'what we eat, such as how much meat, may matter more than where it comes from.'),
  ]),

  p('r3-07', 3, 'Praise and Effort', 'ほめ方と努力', `
Parents often praise children by saying, "You're so smart!" It seems like a kind and encouraging thing to say. Yet a series of studies suggests that this kind of praise can sometimes do more harm than good.

In one experiment, children solved a set of easy puzzles. Some were praised for their intelligence, others for their effort. Next, they were offered a choice between a harder puzzle and an easy one. Most of the children praised for being smart chose the easy puzzle, apparently to avoid the risk of looking less intelligent. Most of those praised for effort chose the challenge.

The researchers suggest that praising ability teaches children that intelligence is fixed, so failure becomes a threat. Praising effort and strategy, in contrast, teaches them that skills can be developed, which makes mistakes part of learning rather than proof of weakness.`, [
    q('r3-07-1', '頭のよさをほめられた子どもの多くはどうしたか。', [
      '易しいパズルを選んだ', '難しいパズルを選んだ', 'パズルをやめた', '他の子に助けを求めた'],
      '「賢いとほめられた子どもの多くは、頭がよくないと見られる危険を避けるため、易しいパズルを選んだ」。',
      'Most of the children praised for being smart chose the easy puzzle'),
    q('r3-07-2', '努力をほめることの効果として本文が述べているものはどれか。', [
      '能力はのばせると学び、失敗を学習の一部と考えるようになる', '自分は頭がよいと考えるようになる', '失敗を恐れるようになる', '易しい問題ばかり選ぶようになる'],
      '「努力や工夫をほめると、技能はのばせると教えることになり、間違いは弱さの証拠ではなく学習の一部になる」。',
      'which makes mistakes part of learning rather than proof of weakness.'),
    q('r3-07-3', '本文のタイトルとして最も適切なものはどれか。', [
      'How the Way We Praise Shapes Children’s Attitude to Challenge', 'Why Children Should Solve Puzzles Every Day', 'The Best Puzzles for Smart Children', 'Why Parents Should Stop Praising Children'],
      '本文はほめ方（能力か努力か）によって子どもの挑戦への態度が変わることを述べている。ほめること自体をやめよとは言っていない。',
      'Praising effort and strategy, in contrast, teaches them that skills can be developed'),
  ]),

  p('r3-08', 3, 'Silent Reading Was Once Strange', '黙読の歴史', `
Today, we take silent reading for granted. In a library, reading aloud would seem rude. But for much of history, reading was usually done out loud, even when people were alone.

One reason was the way texts were written. In many ancient manuscripts, there were no spaces between words and little punctuation. Reading such texts silently was difficult; sounding them out helped readers find where one word ended and the next began. Books were also rare and expensive, so one person often read to a group.

Over the centuries, as spaces between words became standard and books became cheaper, silent reading spread. This change had important effects. Reading became a private activity, allowing people to explore ideas, including dangerous or forbidden ones, without anyone else knowing.`, [
    q('r3-08-1', '昔の写本が声に出して読まれた理由として本文が挙げているものはどれか。', [
      '語と語の間にすき間がなく、声に出すと区切りが分かりやすかったから', '黙って読むことが法律で禁じられていたから', '本の文字が大きすぎたから', '図書館で読むことが多かったから'],
      '「多くの古代の写本には語の間のすき間がなく、声に出すと語の区切りを見つけやすかった」。',
      'sounding them out helped readers find where one word ended and the next began.'),
    q('r3-08-2', '黙読が広まった結果として本文が述べていることはどれか。', [
      '読書が個人的な行為になり、人に知られずに考えを探れるようになった', '本の値段が上がった', '人々は集まって本を読むようになった', '危険な本は読まれなくなった'],
      '「読書は個人的な行為になり、危険な、あるいは禁じられた考えも誰にも知られずに探れるようになった」。',
      'Reading became a private activity, allowing people to explore ideas, including dangerous or forbidden ones, without anyone else knowing.'),
    q('r3-08-3', '本文の内容と一致するものはどれか。', [
      '本が高価で珍しかったので、1人が集団に読み聞かせることが多かった', '昔の人は1人のときは必ず黙読していた', '古代の写本には句読点が多かった', '黙読は古代からずっと一般的だった'],
      '「本は珍しく高価だったので、1人が集団に読み聞かせることが多かった」。',
      'Books were also rare and expensive, so one person often read to a group.'),
  ]),

  p('r3-09', 3, 'The Wisdom of Crowds', '集団の知恵', `
In 1906, at a country fair in England, nearly 800 people guessed the weight of an ox. Most guesses were far from correct. Yet when the scientist Francis Galton calculated the average of all the guesses, it was within one percent of the true weight.

This phenomenon is known as the "wisdom of crowds." When many people make independent judgments, their individual errors tend to cancel each other out. Some guess too high, others too low, and the average ends up close to the truth.

The key word, however, is "independent." If people can hear each other's opinions before guessing, they tend to follow the loudest or most confident voice. Their errors then point in the same direction instead of canceling out. This is why a group discussion does not always produce better decisions than individuals working alone.`, [
    q('r3-09-1', '1906年の出来事について正しいものはどれか。', [
      '推測の平均が実際の重さとほぼ一致した', 'ほとんどの人が正確な重さを当てた', 'ゴルトンが1人で重さを当てた', '平均は実際の重さと大きく違った'],
      '「すべての推測の平均は、本当の重さの1％以内だった」。',
      'it was within one percent of the true weight.'),
    q('r3-09-2', '「集団の知恵」がはたらくための条件として筆者が強調しているものはどれか。', [
      '一人ひとりが他人に影響されずに判断すること', '自信のある人の意見に従うこと', 'できるだけ専門家だけで判断すること', '全員で話し合ってから判断すること'],
      '「しかし、かぎとなる語は『独立した』だ」。他人の意見を聞くと誤りが同じ方向にそろってしまう。',
      'The key word, however, is "independent."'),
    q('r3-09-3', '最後の段落から言えることはどれか。', [
      '集団での話し合いが、個人で考えるよりよい決定を生むとは限らない', '話し合いをすれば誤りは必ず打ち消し合う', '声の大きい人の意見は正しいことが多い', '個人で考えるのは常に集団より劣る'],
      '最後の文「だから集団での話し合いが、個人で取り組むより常によい決定を生むとは限らない」。',
      'This is why a group discussion does not always produce better decisions than individuals working alone.'),
  ]),

  p('r3-10', 3, 'Robots and Jobs', 'ロボットと仕事', `
Every time a new technology appears, people worry that machines will take away jobs. When automatic teller machines (ATMs) spread in the United States in the 1970s and 1980s, many expected bank tellers to disappear. In fact, the number of tellers actually increased for several decades.

The reason was surprising. Because ATMs reduced the cost of running each branch, banks opened many more branches. Each branch needed fewer tellers, but there were more branches overall. At the same time, the tellers' job changed. Instead of counting cash, they spent more time advising customers and selling services.

This example does not prove that technology never destroys jobs. Some jobs do disappear completely. But it shows that the effects of automation are often less direct than we expect: tasks change, new work appears, and the overall picture can be quite different from the first prediction.`, [
    q('r3-10-1', 'ATMが広まったあと、銀行の窓口係の数はどうなったか。', [
      '数十年にわたって増えた', 'すぐにほとんどいなくなった', '半分に減った', '変わらなかった'],
      '「実際には、窓口係の数は数十年間増え続けた」。',
      'In fact, the number of tellers actually increased for several decades.'),
    q('r3-10-2', 'そのような結果になった理由として正しいものはどれか。', [
      '支店の運営費が下がり、銀行が支店を大幅に増やしたから', 'ATMがよく故障したから', '法律で窓口係の数が決められていたから', '客がATMを使いたがらなかったから'],
      '「ATMが各支店の運営費を下げたので、銀行ははるかに多くの支店を開いた」。',
      'Because ATMs reduced the cost of running each branch, banks opened many more branches.'),
    q('r3-10-3', '筆者の主張として最も適切なものはどれか。', [
      '自動化の影響は予想より間接的で、最初の予測と違うことが多い', '技術が仕事を奪うことは決してない', 'すべての仕事はいずれ機械に置きかわる', '新しい技術は導入すべきではない'],
      '「自動化の影響は予想より間接的なことが多い。仕事の中身が変わり、新しい仕事が生まれる」。',
      'it shows that the effects of automation are often less direct than we expect'),
  ]),

  p('r3-11', 3, 'Why We Procrastinate', '先のばしの心理', `
Most people have put off an important task, even when they knew it would cause problems later. We often explain this as laziness or poor time management. However, psychologists increasingly see procrastination as a problem of managing emotions.

When a task makes us feel anxious, bored, or unsure of ourselves, avoiding it brings immediate relief. Checking social media or cleaning the room feels better, at least for a while. The cost, of course, is paid later, often with more stress than before.

If this view is correct, simply making a better schedule may not help much. A more effective approach is to reduce the unpleasant feelings attached to the task. Breaking it into very small first steps, such as "open the file and write one sentence," can lower the emotional barrier. Being kind to oneself after procrastinating also helps; people who forgive themselves tend to delay less the next time.`, [
    q('r3-11-1', '心理学者は先のばしをどのようなものと考えるようになっているか。', [
      '感情をうまく扱えないことの問題', '単なるなまけ', '時間の管理が下手なこと', '能力が足りないこと'],
      '「心理学者は先のばしを、感情を管理する問題と見るようになっている」。',
      'psychologists increasingly see procrastination as a problem of managing emotions.'),
    q('r3-11-2', '筆者が効果的だとする方法はどれか。', [
      '最初の一歩をとても小さくして、気持ちの壁を下げる', 'よりくわしい予定表を作る', '締め切りをもっと早くする', 'スマホを使えなくする'],
      '「ごく小さな最初の一歩に分けることで、感情の壁を下げられる」。',
      'Breaking it into very small first steps, such as "open the file and write one sentence," can lower the emotional barrier.'),
    q('r3-11-3', '本文の内容と一致するものはどれか。', [
      '先のばししたあと自分を許す人は、次に先のばしが少なくなる', '自分を厳しく責めると先のばしが減る', '先のばしをすると長い間気分がよくなる', '予定表を作ることが最も効果的である'],
      '最後の文「自分を許す人は、次に遅らせることが少ない傾向がある」。',
      'people who forgive themselves tend to delay less the next time.'),
  ]),

  p('r3-12', 3, 'Endangered Languages', '消えゆく言語', `
There are about 7,000 languages in the world today, but nearly half of them may disappear by the end of this century. Many are spoken by only a few hundred people, most of them elderly. When children grow up speaking a more widely used language at school and on television, the old language is no longer passed on.

Some people ask why this matters, since a common language makes communication easier. Linguists answer that each language contains knowledge that cannot be fully translated. Some languages have detailed words for local plants and their medical uses, or ways of describing direction and time that reflect a unique view of the world.

Efforts to save languages are increasing. Communities record elderly speakers, create apps for learners, and open schools where children are taught in the local language. Success is not guaranteed, but the example of Welsh, which now has more young speakers than it did fifty years ago, shows that decline can be reversed.`, [
    q('r3-12-1', '言語が受け継がれなくなる原因として本文が挙げているものはどれか。', [
      '子どもが学校やテレビでより広く使われる言語で育つから', '高齢者が言語を教えたがらないから', '言語を記録する方法がないから', '国が使用を禁止しているから'],
      '「子どもが学校やテレビで、より広く使われる言語を話して育つと、古い言語は受け継がれなくなる」。',
      'When children grow up speaking a more widely used language at school and on television, the old language is no longer passed on.'),
    q('r3-12-2', '言語学者が言語を守るべきだとする理由はどれか。', [
      'それぞれの言語には、完全には翻訳できない知識が含まれているから', '共通の言語は意思疎通を難しくするから', '話す人が多いほど経済がよくなるから', '古い言語のほうが学びやすいから'],
      '「それぞれの言語には、完全には翻訳できない知識が含まれている」。',
      'Linguists answer that each language contains knowledge that cannot be fully translated.'),
    q('r3-12-3', 'ウェールズ語の例が示しているのはどれか。', [
      '言語の衰退は逆転させることができる', '若い人は古い言語に関心がない', '言語を守る取り組みは必ず成功する', 'ウェールズ語は50年前より話す人が減った'],
      '「若い話者が50年前より多いウェールズ語の例は、衰退が逆転できることを示している」。',
      'shows that decline can be reversed.'),
  ]),
];
