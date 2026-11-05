# -*- coding: utf-8 -*-
# 茨城大学 第1回 Ⅲ・Ⅳ（書き下ろし。人物・団体・地名・数値は架空）
P3 = {
    'points': 50,
    'title': 'The Long Journey of the Potato',
    'passage': [
        "Few foods are as ordinary as the potato. It is boiled, baked, fried, and mashed in kitchens on every continent, and many people "
        "would be surprised to learn that it was once regarded with deep suspicion. The potato was first grown in the high mountains of "
        "South America, where farmers developed hundreds of varieties suited to cold nights and thin air. For them it was not a side dish "
        "but the center of daily life.",
        "When European sailors brought the plant across the ocean in the sixteenth century, it was not welcomed. Because it grew under the "
        "ground and belonged to the same family as some poisonous plants, many people believed it caused illness. In some regions it was "
        "fed only to animals, and in others it was grown in gardens simply for its flowers. Farmers who had grown wheat and other grains "
        "for generations saw no reason to try a strange new crop. Some writers even warned that a diet of potatoes would make "
        "people weak and lazy, and that only the poorest families should be forced to eat them.",
        "Attitudes changed slowly, and often for practical reasons. The potato produced far more food from a small field than grain did, "
        "and it could be left in the ground until it was needed, which made it harder for passing armies to steal. During years when the "
        "grain harvest failed, families who had planted potatoes were far less likely to go hungry. Some rulers began to encourage their "
        "use. One story, probably more legend than fact, tells of a king who had a field of potatoes guarded by soldiers during the day "
        "but not at night. Curious villagers, assuming that anything so carefully protected must be valuable, crept in after dark and "
        "took plants home to grow for themselves.",
        "By the nineteenth century the potato had become a basic food for millions of poor families in northern Europe. Its success, "
        "however, also created a danger. In some areas people depended on a single variety, so when a plant disease arrived, it spread "
        "through the fields with nothing to stop it. Crops rotted in the ground, and the result was a terrible famine that caused great "
        "suffering and forced many people to leave their homeland.",
        "Scientists today draw a lesson from this history. Growing many different varieties of a crop makes it less likely that one "
        "disease will destroy everything. For this reason, seed banks around the world, including one in the mountain town of Valdoro, "
        "keep samples of thousands of traditional potatoes. Some of these old varieties may one day provide the resistance to disease or "
        "drought that farmers will need in a changing climate.",
    ],
    'questions': [
        {'q': 'Where was the potato first grown, and why was it important to the farmers there?', 'points': 10,
         'answer': 'In the mountains of South America. The farmers there depended on it as their main food every day, and they bred many kinds that could survive the cold.',
         'expl': '第1段落。first grown in the high mountains of South America と，For them it was not a side dish but the center of daily life の二点を答える。'
                 'not A but B の B（the center of daily life）を答えの中心にする。',
         'criteria': [('南米の高い山地で最初に栽培された', 4), ('人々の日々の生活の中心だった（主食だった）', 4), ('寒さに合う多くの品種を作った', 2)]},
        {'q': 'Why did many Europeans refuse to eat potatoes at first?', 'points': 10,
         'answer': 'Because it grew underground and was related to some poisonous plants, so many people believed it made them ill.',
         'alt': 'They thought potatoes caused illness, because the plant grew under the ground and was in the same family as poisonous plants.',
         'expl': '第2段落 Because it grew under the ground and belonged to the same family as some poisonous plants, many people believed it caused illness. '
                 'Why の問いには Because ... で答えてよい。本文をそのまま写さず，be related to ~ などで言いかえると表現力の点でもよい。',
         'criteria': [('地中で育つ', 3), ('毒のある植物と同じ仲間', 3), ('病気の原因になると信じられた', 4)]},
        {'q': 'What practical advantages did the potato have over grain?', 'points': 10,
         'answer': 'It produced much more food from a small field, and it could be kept in the ground until needed, so armies could not easily steal it.',
         'expl': '第3段落の前半。produced far more food from a small field than grain did と，could be left in the ground until it was needed, which made it harder for passing armies to steal の二点。'
                 'which は前の内容全体を受ける。凶作の年に飢えにくかったことを加えてもよい。',
         'criteria': [('小さな畑からずっと多くの食料がとれる', 4), ('必要になるまで地中に置いておける', 3), ('通りかかった軍隊に盗まれにくい', 3)]},
        {'q': 'According to the story, why did the villagers take potatoes from the king’s field?', 'points': 10,
         'answer': 'They thought the potatoes must be valuable because soldiers guarded the field so carefully, so they took some at night when there were no guards.',
         'expl': '第3段落後半の言い伝え。assuming that anything so carefully protected must be valuable が理由。guarded by soldiers during the day but not at night だったので夜に忍びこんだ。'
                 'must be は「〜にちがいない」。',
         'criteria': [('兵士が厳重に見張っていた', 3), ('だから価値があるにちがいないと考えた', 5), ('見張りのいない夜に持ち帰った', 2)]},
        {'q': 'Why do seed banks keep thousands of traditional potato varieties?', 'points': 10,
         'answer': 'Because if there are many kinds of potatoes, a single disease cannot easily wipe out every crop, and old kinds may help farmers deal with disease or dry weather later.',
         'expl': '第4段落（一つの品種に頼ったために病気で大飢饉が起きた）からの教訓が第5段落。Growing many different varieties ... less likely that one disease will destroy everything と，'
                 'may one day provide the resistance to disease or drought の二点を答える。',
         'criteria': [('多くの品種があれば一つの病気ですべてが失われにくい', 5), ('古い品種が将来，病気や干ばつへの強さをもたらすかもしれない', 5)]},
    ],
    'translation': [
        'ジャガイモほどありふれた食べ物はほとんどない。世界中の台所でゆでられ，焼かれ，揚げられ，つぶされている。かつてそれが深い疑いの目で見られていたと知れば，多くの人は驚くだろう。'
        'ジャガイモは最初，南アメリカの高い山地で栽培された。そこで農民たちは，寒い夜と薄い空気に合った何百もの品種を作り出した。彼らにとってそれは付け合わせではなく，日々の生活の中心だった。',
        '16世紀にヨーロッパの船乗りたちがこの植物を海の向こうから持ち帰ったとき，それは歓迎されなかった。地中で育ち，いくつかの毒のある植物と同じ仲間だったため，多くの人が病気の原因になると信じたのである。'
        '動物のえさにしかされない地域もあれば，花を見るためだけに庭で育てられる地域もあった。何世代にもわたって小麦などの穀物を育ててきた農民たちには，見慣れない新しい作物を試す理由が見当たらなかった。ジャガイモばかり食べていると人は弱く怠け者になるから，最も貧しい家族だけに食べさせればよいと警告する書き手さえいた。',
        '人々の態度はゆっくりと，しかもたいていは実用的な理由から変わっていった。ジャガイモは小さな畑から穀物よりはるかに多くの食料を生み出し，必要になるまで地中に置いておけたので，通りかかる軍隊に盗まれにくかった。'
        '穀物が不作だった年には，ジャガイモを植えていた家族は飢えることがずっと少なかった。ジャガイモの利用を勧め始める支配者も現れた。'
        'おそらく事実というより伝説だが，こんな話がある。ある王が，昼間はジャガイモの畑を兵士に守らせ，夜は守らせなかった。'
        '好奇心をもった村人たちは，これほど厳重に守られているものは価値があるにちがいないと考え，暗くなってから忍びこみ，自分で育てるために株を持ち帰ったという。',
        '19世紀までに，ジャガイモは北ヨーロッパの何百万もの貧しい家族にとっての基本的な食べ物になっていた。しかしその成功は危険も生んだ。'
        'ある地域では人々がたった一つの品種に頼っていたので，植物の病気がやってくると，止めるものもなく畑じゅうに広がった。作物は地中で腐り，その結果，大きな苦しみをもたらし，多くの人を故郷から去らせる恐ろしい飢饉が起きた。',
        '今日の科学者たちは，この歴史から教訓を引き出している。一つの作物の多くの異なる品種を育てれば，一つの病気がすべてを滅ぼす可能性は低くなる。'
        'このため，山あいの町ヴァルドーロのものをはじめ，世界中の種子銀行が何千もの在来のジャガイモの標本を保存している。こうした古い品種のいくつかは，気候が変わる中で農民が必要とする，病気や干ばつへの強さをいつかもたらしてくれるかもしれない。',
    ],
    'vocab': [('ordinary', 'ありふれた'), ('mash', 'つぶす'), ('regard A with suspicion', 'A を疑いの目で見る'), ('variety', '品種'),
              ('side dish', '付け合わせ'), ('poisonous', '毒のある'), ('grain', '穀物'), ('generation', '世代'), ('crop', '作物'),
              ('attitude', '態度'), ('practical', '実用的な'), ('harvest', '収穫'), ('ruler', '支配者'), ('legend', '伝説'),
              ('assume', '思いこむ'), ('creep in', '忍びこむ'), ('depend on ~', '〜に頼る'), ('rot', '腐る'), ('famine', '飢饉'),
              ('seed bank', '種子銀行'), ('resistance', '抵抗力'), ('drought', '干ばつ')],
}

P4 = {
    'points': 50,
    'title': '「わからない」と言える教室',
    'passage': [
        '中学校で理科を教えていたころ，授業の最後に「何か質問はありますか」とたずねても，手が挙がることはほとんどなかった。'
        'ところが，授業が終わって廊下に出ると，何人かの生徒が追いかけてきて，小さな声で質問をする。'
        '{u1|みんなの前で質問すると，自分だけが理解できていないと思われるのではないかと心配していたのだ。}',
        'そこで私は，授業の最初に，前の時間に自分がうまく説明できなかったところを正直に話すことにした。'
        '教師がまちがいを認めると，教室の空気が少しやわらかくなる。しばらくすると，生徒たちも「ここがわかりません」と口にするようになった。'
        '{u2|わからないことを恥ずかしがらずに言えるようになって初めて，本当の学びが始まるのだと，私は生徒たちから教わった。}',
    ],
    'items': [
        {'points': 25,
         'rephrase': '生徒たちは「もしみんなの前で質問したら，ほかの人たちは自分だけがわかっていないと思うだろう」と心配していた。',
         'models': ['They were worried that if they asked a question in front of everyone, the others would think they were the only ones who did not understand.',
                    'They were afraid that asking questions in front of the class would make the others think that only they had not understood the lesson.'],
         'tips': ['主語は「生徒たち」（they）。「〜するのではないかと心配していた」は be worried (that) ~ / be afraid (that) ~。過去の話なので時制の一致で would think にする。',
                  '「自分だけが理解できていない」は they were the only ones who did not understand / only they had not understood。「思われる」は受け身にせず，the others would think ~ と能動にすると書きやすい。'],
         'criteria': [('「〜ではないかと心配していた」（be worried / afraid that）', 5), ('「みんなの前で質問すると」（if 節・動名詞主語など）', 6),
                      ('「自分だけが理解できていない」（the only ones who / only they）', 8), ('時制の一致（would・過去完了など）', 6)]},
        {'points': 25,
         'rephrase': '私は生徒たちから「生徒がわからないことを恥ずかしがらずに言えるようになって，そのとき初めて，本当の学びが始まる」ということを学んだ。',
         'models': ['My students taught me that real learning begins only when students can say what they do not understand without feeling embarrassed.',
                    'I learned from my students that it is not until people feel free to admit that they do not understand something that true learning starts.'],
         'tips': ['「〜して初めて…」は only when ~ / not until ~ を使う。It is not until ~ that … の強調構文も使えるが，語順をまちがえやすいので only when が安全。',
                  '「わからないこと」は what they do not understand（関係詞 what）。「恥ずかしがらずに」は without feeling embarrassed / without being ashamed。「私は生徒たちから教わった」は My students taught me that ~ と主語を入れかえると自然。一般的な真理なので that 節の中は現在形のままでよい。'],
         'criteria': [('「生徒たちから教わった」（My students taught me / I learned from）', 4), ('「〜して初めて」（only when / not until）', 8),
                      ('「わからないことを言う」（what they do not understand）', 7), ('「恥ずかしがらずに」（without ~ing）', 6)]},
    ],
}
