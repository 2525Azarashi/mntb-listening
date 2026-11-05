# -*- coding: utf-8 -*-
# 茨城大学 第3回 Ⅰ・Ⅱ（書き下ろし。人物・団体・地名・調査・数値は架空）
P1 = {
    'points': 50,
    'title': 'The Quiet Power of Trees in Cities',
    'passage': [
        "When people imagine the benefits of trees, they usually think of forests far from towns: places that store carbon, shelter "
        "wildlife, and supply clean water. Trees planted along city streets receive less attention, as if they were only decoration. When budgets are tight, they are often "
        "among the first things to be cut, and new roads are rarely designed with space for them. "
        "{u1|Recent research, however, suggests that a single row of trees can change the daily life of a neighborhood in ways that are "
        "easy to overlook.}",
        "The most obvious effect is on temperature. On a hot summer afternoon, roads and rooftops absorb sunlight and release heat long "
        "after sunset, so that city centers often stay several degrees warmer than the surrounding countryside. Trees reduce this effect in "
        "two ways. Their leaves block sunlight before it reaches the ground, and they release water vapor that cools the air around them. "
        "In a survey carried out in the city of Brennick, streets lined with mature trees were on average about four degrees cooler at "
        "midday than similar streets without them. Residents of those streets also reported sleeping better on hot nights.",
        "Trees may also affect how people behave. Researchers in Brennick counted how many residents walked, sat outside, or stopped to "
        "talk with neighbors on streets with and without trees. On the shaded streets, all three activities were more common, especially "
        "among elderly people. {u2|Since loneliness is known to harm health, a street that encourages people to spend time outdoors and "
        "meet one another may be doing more for public health than its planners ever intended.}",
        "There are costs, of course. Trees must be watered while they are young, their roots can crack pavements, and falling leaves block "
        "drains in autumn. Some shop owners complain that branches hide their signs. For these reasons, city governments have sometimes "
        "cut down healthy trees to save money on maintenance. Yet such decisions often ignore benefits that do not appear in any budget, "
        "such as lower electricity bills for air conditioning or fewer people becoming ill during heat waves.",
        "{u3|Another difficulty is that trees take decades to reach their full size, while political decisions are usually made with only "
        "the next few years in mind.} A tree planted today may not shade a street until the children who watched it being planted have "
        "grown up. This is why some cities now publish maps showing every street tree, its age, and the benefits it is estimated to provide. "
        "{u4|By making the value of trees visible, they hope to persuade both officials and residents that it is worth protecting something "
        "whose rewards arrive slowly.}",
    ],
    'questions': [
        {'ref': 1, 'kind': '下線部和訳', 'points': 12,
         'stem': '下線部(1)を和訳せよ。',
         'answer': 'しかし最近の研究は，一列の木々が，見落としやすいさまざまな形で，ある地域の日々の暮らしを変えうることを示している。',
         'expl': 'suggests that ~「〜ということを示している」。a single row of trees「一列の木」。in ways that are easy to overlook は関係代名詞 that が ways を修飾し，'
                 '「見落としやすい形で」。easy to overlook は「見落とすのが簡単な」と不定詞が形容詞を限定する形。',
         'criteria': [('Recent research suggests that ~「最近の研究は〜を示している」', 3), ('a single row of trees「一列の木々」', 2),
                      ('can change the daily life of a neighborhood「地域の日々の暮らしを変えうる」', 3), ('in ways that are easy to overlook「見落としやすい形で」', 4)]},
        {'kind': '内容説明（気温への効果）', 'points': 12, 'lines': 4,
         'stem': '第2段落で，都市の中心部が周りの田園地帯より暑くなるのはなぜか。また，木はどのような二つの方法でそれをやわらげるか。説明せよ。',
         'answer': '道路や屋根が日光を吸収し，日が沈んだあとも長い間熱を放出するから。木は，葉で日光が地面に届く前にさえぎることと，水蒸気を出して周りの空気を冷やすことの二つの方法でこれをやわらげる。',
         'expl': '原因は roads and rooftops absorb sunlight and release heat long after sunset。方法は Their leaves block sunlight ... と they release water vapor that cools the air ... の二つ。'
                 'Brennick の調査（木のある通りは約4度涼しい）を加えてもよい。',
         'criteria': [('道路や屋根が日光を吸収し，日没後も熱を放出する', 4), ('葉が日光を地面に届く前にさえぎる', 4), ('水蒸気を出して空気を冷やす', 4)]},
        {'ref': 2, 'kind': '下線部和訳', 'points': 13,
         'stem': '下線部(2)を和訳せよ。',
         'answer': '孤独は健康を害することが知られているので，人々に外で時間を過ごし，互いに出会うよう促す通りは，その計画者が意図していたよりも多くのことを人々の健康のためにしているのかもしれない。',
         'expl': 'Since は理由。be known to do「〜することが知られている」。a street that encourages people to spend ... and meet ... が主語で，encourage 人 to do「人に〜するよう促す」。'
                 'more for public health than its planners ever intended「計画者が意図していたよりも多くのことを公衆衛生のために」。ever は比較を強める。',
         'criteria': [('Since loneliness is known to harm health「孤独は健康を害すると知られているので」', 3),
                      ('a street that encourages people to spend time outdoors and meet one another（主語のまとまり）', 4),
                      ('may be doing more for public health「健康のためにより多くのことをしているかもしれない」', 3), ('than its planners ever intended「計画者が意図したより」', 3)]},
        {'refs': [3, 4], 'kind': '下線部の内容説明と筆者が紹介する対策', 'points': 13, 'lines': 5,
         'stem': '下線部(3)はどのような難しさか。具体例を示して説明せよ。また，下線部(4)で，一部の都市はその難しさに対してどのようなことをしているか，その目的とともに説明せよ。',
         'answer': '木は十分な大きさになるまで何十年もかかるのに，政治の決定はたいてい数年先のことしか考えずに行われるという難しさ。たとえば今日植えた木は，植えるのを見ていた子どもが大人になるまで通りに日陰を作らないかもしれない。'
                   'そこで一部の都市は，すべての街路樹とその樹齢，もたらすと見積もられる利益を示した地図を公表している。木の価値を目に見えるようにして，役人と住民の両方に，効果がゆっくり現れるものでも守る価値があると納得してもらうためである。',
         'expl': '下線部(3)は trees take decades ... と political decisions are usually made with only the next few years in mind の while による対比。具体例は直後の A tree planted today ... の文。'
                 '対策は publish maps showing every street tree ...，目的は下線部(4)の By making the value of trees visible, they hope to persuade ...。',
         'criteria': [('木が育つには何十年もかかる', 3), ('政治の決定は数年先しか考えない', 3), ('具体例：植えた木が日陰を作るのは子どもが大人になってから', 2),
                      ('対策：街路樹・樹齢・利益を示した地図を公表', 2), ('目的：価値を見えるようにし，ゆっくり効果が出るものも守る価値があると説得する', 3)]},
    ],
    'translation': [
        '人々が木の恩恵を思い描くとき，ふつうは町から遠く離れた森を考える。炭素をたくわえ，野生生物のすみかとなり，きれいな水をもたらす場所だ。'
        '都市の通りに植えられた木は，まるで飾りにすぎないかのように，あまり注目されない。予算が厳しくなると真っ先に削られるものの一つになることが多く，新しい道路が木のための場所を考えて設計されることもめったにない。しかし最近の研究は，一列の木々が，見落としやすいさまざまな形で，ある地域の日々の暮らしを変えうることを示している。',
        '最もはっきりした効果は気温に対するものである。暑い夏の午後，道路や屋根は日光を吸収し，日が沈んだあとも長い間熱を放出するので，都市の中心部は周りの田園地帯より数度暑いままであることが多い。'
        '木はこの効果を二つの方法でやわらげる。葉が日光を地面に届く前にさえぎり，さらに周りの空気を冷やす水蒸気を出すのである。'
        'ブレニック市で行われた調査では，大きく育った木が並ぶ通りは，木のない同じような通りより，正午に平均で約4度涼しかった。そうした通りの住民は，暑い夜によく眠れるとも答えた。',
        '木は人々のふるまい方にも影響するかもしれない。ブレニックの研究者たちは，木のある通りとない通りで，歩いたり，外に座ったり，立ち止まって隣人と話したりする住民の数を数えた。'
        '日陰のある通りでは，三つの行動のどれもがより多く見られ，特にお年寄りの間でそうだった。'
        '孤独は健康を害することが知られているので，人々に外で時間を過ごし，互いに出会うよう促す通りは，その計画者が意図していたよりも多くのことを人々の健康のためにしているのかもしれない。',
        'もちろん費用もかかる。木は若いうちは水をやらなければならないし，根は歩道にひびを入れることがあり，秋には落ち葉が排水口をふさぐ。枝が看板を隠すと不満を言う店主もいる。'
        'こうした理由から，市当局は維持費を節約するために健康な木を切ってしまうことがあった。しかしそのような決定は，冷房の電気代が下がることや，猛暑の間に体をこわす人が減ることなど，どの予算にも表れない恩恵を見落としていることが多い。',
        'もう一つの難しさは，木は十分な大きさになるまで何十年もかかるのに，政治の決定はたいてい数年先のことだけを考えて行われることである。'
        '今日植えた木は，それが植えられるのを見ていた子どもたちが大人になるまで，通りに日陰を作らないかもしれない。このため，今ではすべての街路樹とその樹齢，もたらすと見積もられる恩恵を示した地図を公表している都市もある。'
        '木の価値を目に見えるようにすることで，効果がゆっくりとしか現れないものでも守る価値があると，役人と住民の両方を説得したいと考えているのである。',
    ],
    'vocab': [('benefit', '恩恵'), ('store', 'たくわえる'), ('shelter', 'すみかを与える'), ('decoration', '飾り'), ('overlook', '見落とす'),
              ('absorb', '吸収する'), ('release', '放出する'), ('surrounding', '周りの'), ('water vapor', '水蒸気'), ('mature', '大きく育った'),
              ('shaded', '日陰の'), ('loneliness', '孤独'), ('intend', '意図する'), ('crack', 'ひびを入れる'), ('pavement', '歩道'),
              ('drain', '排水口'), ('maintenance', '維持（費）'), ('budget', '予算'), ('heat wave', '猛暑'), ('estimate', '見積もる'),
              ('persuade', '説得する'), ('reward', '報い・恩恵')],
}

P2 = {
    'points': 50,
    'title': 'Learning from Mistakes in the Kitchen',
    'passage': [
        "Chefs in busy restaurants make mistakes every day. A sauce is too salty, a cake sinks in the middle, a piece of fish is overcooked "
        "by thirty seconds. In most kitchens, such errors are quietly thrown away and forgotten. Head chefs may shout at the cook responsible, and the "
        "lesson that everyone learns is to hide the next mistake more carefully. {u1|A small restaurant in the harbor town of "
        "Penhallow, however, has become known for treating its failures not as something to hide but as a source of new ideas.}",
        "The restaurant’s owner, a cook named Tobias Wren, keeps a notebook on the wall beside the stove. Whenever a dish goes wrong, the "
        "person responsible writes down what happened and what they think caused it. Nobody is blamed. At the end of each week, the whole "
        "team reads the notebook together and discusses whether any of the mistakes could be turned into something useful. Wren says that "
        "the rule took several months to work. At first, young cooks were afraid that writing down their errors would cost them their jobs. "
        "To show that he meant it, Wren began by writing down several of his own failures, including a dessert he had ruined in front "
        "of a large group of guests.",
        "Some of the restaurant’s most popular dishes began in this way. A batch of bread that had been left to rise too long turned out to "
        "have a sour flavor that customers loved. A soup that had been accidentally burned at the bottom gave the cooks the idea of adding a "
        "smoky taste on purpose. {u2|Had these accidents been thrown away without a second thought, the restaurant’s menu would be much "
        "less interesting today.}",
        "The notebook has had another effect that Wren did not expect. Because mistakes are discussed openly, the same error is rarely "
        "repeated. New staff learn quickly from the experience of others, and experienced cooks are reminded that even they can get things "
        "wrong. {u3|Wren believes that a kitchen where people are afraid to admit their mistakes is not only less creative but also less "
        "safe, since problems that are hidden cannot be fixed.}",
        "Similar ideas have been adopted in fields far from cooking. Hospitals and airlines, for example, have developed systems that "
        "encourage workers to report errors and near misses without fear of punishment. The details differ, but the principle is the same. In each case, the goal is to learn about a problem before it causes serious harm. "
        "{u4|An organization that wants to improve must first make it possible for people to talk honestly about what went wrong.}",
    ],
    'questions': [
        {'ref': 1, 'kind': '下線部和訳', 'points': 12,
         'stem': '下線部(1)を和訳せよ。',
         'answer': 'しかし，港町ペンハロウのある小さなレストランは，自分たちの失敗を隠すべきものとしてではなく，新しい考えの源として扱っていることで知られるようになった。',
         'expl': 'has become known for ~ing「〜していることで知られるようになった」。treat ～ not as … but as ―「～を…としてではなく―として扱う」。'
                 'something to hide は不定詞の形容詞用法で「隠すべきもの」。a source of new ideas「新しい考えの源」。',
         'criteria': [('A small restaurant in the harbor town of Penhallow「港町ペンハロウの小さなレストラン」', 2), ('has become known for ~ing「〜で知られるようになった」', 3),
                      ('not as something to hide「隠すべきものとしてではなく」', 4), ('but as a source of new ideas「新しい考えの源として」', 3)]},
        {'kind': '内容説明（ノートの決まり）', 'points': 12, 'lines': 4,
         'stem': '第2段落で説明されているノートの決まりとはどのようなものか。また，その決まりがうまく機能するまでに時間がかかったのはなぜか。説明せよ。',
         'answer': '料理を失敗したら，その担当者が何が起きたか，原因は何だと思うかをこんろの横のノートに書く。誰も責められず，毎週末にチーム全員でノートを読み，失敗を役立つものに変えられないか話し合う。'
                   '時間がかかったのは，はじめ若い料理人たちが，失敗を書くと仕事を失うのではないかと恐れていたから。',
         'expl': '決まりは Whenever a dish goes wrong, the person responsible writes down ... / Nobody is blamed. / At the end of each week, the whole team reads ... の三点。'
                 '時間がかかった理由は were afraid that writing down their errors would cost them their jobs。cost 人 ~「人に〜を失わせる」。',
         'criteria': [('失敗したら担当者が起きたことと原因を書く', 3), ('誰も責められない', 2), ('毎週チーム全員で読み，役立てられないか話し合う', 3),
                      ('若い料理人が書くと仕事を失うと恐れた', 4)]},
        {'ref': 2, 'kind': '下線部和訳', 'points': 13,
         'stem': '下線部(2)を和訳せよ。',
         'answer': 'もしこれらの偶然の失敗が深く考えられることもなく捨てられていたら，そのレストランの献立は今日ずっとつまらないものになっているだろう。',
         'expl': '文頭の Had these accidents been ... は，if を使った仮定の if 節（If ＋主語＋had been ...）から if を省略し，had を前に出した倒置。主節は would be ... today で，'
                 '過去の仮定（仮定法過去完了）と現在の結果（仮定法過去）を組み合わせた形。without a second thought「深く考えずに」。',
         'criteria': [('Had ~ = If ~ had ...（倒置の仮定）を正しく訳す', 4), ('without a second thought「よく考えずに」', 3),
                      ('would be much less interesting「ずっとつまらないだろう」', 3), ('today「今日（では）」：過去の仮定と現在の結果', 3)]},
        {'refs': [3, 4], 'kind': '下線部の内容説明（筆者の主張と関連づけて）', 'points': 13, 'lines': 5,
         'stem': '下線部(3)で Wren はなぜそのように考えるのか。第4段落の内容をふまえて説明せよ。また，下線部(4)で述べられている考えが，料理以外のどのような分野でどのように生かされているか説明せよ。',
         'answer': '失敗を認めるのを恐れる台所では，失敗から新しい料理が生まれることがないので創造的でなくなるうえ，隠された問題は直すことができないので安全でもなくなるから。'
                   '失敗が公に話し合われれば同じ失敗はめったにくり返されず，新人も他人の経験から早く学べる。この考えは病院や航空会社で，働く人が罰を恐れずにミスやミスになりかけたことを報告できる仕組みとして生かされている。',
         'expl': 'not only less creative but also less safe の二点を，since problems that are hidden cannot be fixed と第4段落の the same error is rarely repeated から説明する。'
                 '後半は第5段落 Hospitals and airlines ... encourage workers to report errors and near misses without fear of punishment。',
         'criteria': [('失敗を恐れると新しい考えが生まれず創造的でない', 3), ('隠された問題は直せないので安全でない', 3),
                      ('話し合えば同じ失敗をくり返さず，新人も学べる', 3), ('病院・航空会社で罰を恐れずミスを報告できる仕組み', 4)]},
    ],
    'translation': [
        '忙しいレストランの料理人たちは毎日失敗をする。ソースが塩辛すぎたり，ケーキの真ん中がへこんだり，魚の切り身を30秒焼きすぎたりする。'
        'たいていの台所では，そうした失敗はひっそりと捨てられて忘れられる。料理長が担当の料理人をどなりつけることもあり，皆が学ぶ教訓は，次の失敗をもっとうまく隠すことになってしまう。しかし，港町ペンハロウのある小さなレストランは，自分たちの失敗を隠すべきものとしてではなく，新しい考えの源として扱っていることで知られるようになった。',
        'その店の主人であるトバイアス・レンという料理人は，こんろの横の壁にノートを掛けている。料理がうまくいかなかったときはいつでも，その担当者が何が起きたか，何が原因だと思うかを書き留める。'
        '誰も責められることはない。毎週の終わりには，チーム全員でいっしょにノートを読み，失敗のどれかを役に立つものに変えられないかを話し合う。'
        'レンによれば，この決まりがうまく機能するまでには数か月かかった。はじめのうち，若い料理人たちは，失敗を書き留めたら仕事を失うのではないかと恐れていたのである。本気であることを示すため，レンはまず自分の失敗をいくつか書いた。大勢の客の前で台なしにしたデザートのこともそこに含まれていた。',
        'この店で最も人気のある料理のいくつかは，こうして生まれた。発酵させる時間が長すぎたパンの一回分は，客に大好評の酸味をもっていることがわかった。'
        'うっかり底をこがしてしまったスープからは，わざと燻製のような風味を加えるという考えが生まれた。'
        'もしこれらの偶然の失敗が深く考えられることもなく捨てられていたら，そのレストランの献立は今日ずっとつまらないものになっているだろう。',
        'そのノートは，レンが予想していなかったもう一つの効果ももたらした。失敗が隠されずに話し合われるので，同じ失敗がくり返されることはめったにないのだ。'
        '新しい従業員はほかの人の経験から早く学び，経験を積んだ料理人は自分たちでさえ失敗しうることを思い出す。'
        'レンは，人々が自分の失敗を認めるのを恐れる台所は，創造性に欠けるだけでなく安全性にも欠けると考えている。隠された問題は直すことができないからである。',
        '同じような考えは，料理から遠く離れた分野でも取り入れられている。たとえば病院や航空会社は，働く人が罰を恐れずにミスやミスになりかけたことを報告するよう促す仕組みを作ってきた。'
        '細かい点は違っても，原則は同じである。どの場合も，問題が深刻な害をもたらす前にそれについて知ることが目的である。よくなりたいと願う組織は，まず人々が何がうまくいかなかったかについて正直に話せるようにしなければならないのだ。',
    ],
    'vocab': [('chef', '料理人'), ('overcook', '焼き（煮）すぎる'), ('harbor', '港'), ('treat A as B', 'A を B として扱う'), ('source', '源'),
              ('stove', 'こんろ'), ('responsible', '担当の・責任のある'), ('blame', '責める'), ('cost 人 ~', '人に〜を失わせる'), ('batch', '一回分'),
              ('rise', '（パンが）ふくらむ'), ('sour', '酸っぱい'), ('accidentally', 'うっかり'), ('on purpose', 'わざと'), ('without a second thought', 'よく考えずに'),
              ('openly', '隠さずに'), ('admit', '認める'), ('adopt', '取り入れる'), ('near miss', 'ミスになりかけたこと'), ('punishment', '罰'),
              ('principle', '原則')],
}
