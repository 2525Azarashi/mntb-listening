# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第3回 大問1・大問2（書き下ろし。人物・団体・地名・調査・数値は架空）
from j1a import CH, CO, TR

P1 = {
    'points': 150,
    'intro': '次の英文は，人が情報を信じてしまう仕組みと，誤った情報への向き合い方を論じている。',
    'title': 'Why We Believe What We Read',
    'passage': [
        "Every minute, millions of short messages, pictures, and videos are shared online. Some are accurate, some are mistaken, and "
        "some are deliberately false. Telling them apart is often harder than it looks. Most people believe that they can tell the difference easily. {b:a}, studies repeatedly show that "
        "even well-educated adults are fooled more often than they think. {u:b|The reason is not simply a lack of intelligence, but the "
        "way our minds handle the huge amount of information that reaches us every day.}",
        "Our brains save energy by taking shortcuts. When a statement feels familiar, we tend to accept it as true, even if we cannot "
        "remember where we first heard it. Psychologists call this the illusion of truth. In one experiment carried out at Tarnley "
        "University, students read a list of statements, some true and some false. A week later, they were shown the list again together "
        "with new statements. {u:c|They rated the statements they had seen before as more believable, regardless of whether those "
        "statements were actually correct.} Simply hearing something twice made it seem more likely to be true.",
        "Emotion plays a part as well. Messages that make us angry, afraid, or amused spread far faster than calm, careful explanations. "
        "When we feel strongly, we become {b:d} likely to stop and check the facts, and more likely to press the share button at once. "
        "People who create false stories know this well, and they often design their messages to provoke a strong reaction rather than "
        "to inform. A headline that says a common food \"destroys your brain\" will attract far more attention than one that says the "
        "food \"may slightly affect sleep in some people.\"",
        "Another factor is the company we keep. {u:e|We are more inclined to trust a message when it comes from a friend or family member, "
        "because we trust the person who sent it, not because we have examined the message itself.} In addition, online services "
        "usually show us content similar to what we have liked before. Over time, this can surround us with views that match our own, so "
        "that opposing opinions rarely {b:f} our screens. Within such a bubble, a false claim may be repeated so often that it begins to "
        "look like common knowledge.",
        "What can be done? Some researchers have tested an approach known as \"prebunking.\" Instead of correcting false stories after they "
        "spread, people are shown in advance the tricks that are commonly used to mislead, such as fake experts, emotional language, and "
        "pictures taken out of context. In a study involving 1,200 volunteers from the town of Ellisford, those who played a short "
        "online game that explained these tricks were about 20 percent better at spotting misleading posts a week later than those who "
        "did not play. {u:g|The effect was small but lasting, and it did not depend on the players' political opinions or level of "
        "education.}",
        "Individuals can also develop simple habits. Before sharing a surprising message, ask who wrote it and what evidence it offers. "
        "Search for the same information on a few reliable sites. Be especially careful with posts that make you feel strong emotions, "
        "because that feeling may be exactly what the writer intended. {u:h|None of these steps takes more than a minute, yet together "
        "they can greatly reduce the chance that we pass on something false to the people who trust us.}",
        "It would be unrealistic to expect everyone to check every message they see. Still, {b:i} a small share of readers paused before "
        "sharing, false stories would travel much more slowly. Small actions by many people can add up to a large change. {u:j|In the end, the quality of the information around us depends not only "
        "on the people who create it, but also on each of us who decides what to pass on.}",
    ],
    'notes': [(1, 'deliberately', 'わざと'), (2, 'shortcut', '近道'), (2, 'illusion', '錯覚'), (3, 'provoke', '引き起こす'),
              (4, 'inclined', '〜しがちな'), (4, 'bubble', '泡（外から閉ざされた空間）'), (5, 'mislead', '誤解させる'),
              (5, 'context', '文脈，前後関係')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（つなぎの語）', 'points': 8, 'stem': CH.format(x='a'),
         'options': ['In fact', 'For this reason', 'In addition', 'As a result'], 'answer': 0,
         'expl': '直前は「たいていの人は簡単に見分けられると思っている」，直後は「よく教育を受けた大人でさえ思っている以上にだまされている」。'
                 '思いこみを打ち消して実際を述べるので In fact（実際には）が入る。For this reason・As a result は因果，In addition は追加を表す。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': 'その理由は，単に知性が足りないことではなく，毎日私たちのもとに届く膨大な量の情報を，私たちの頭が処理するやり方にある。',
         'expl': 'not simply ～, but …「単に～ではなく…」。the way our minds handle ～「私たちの頭が～を扱うやり方」は，the way の後ろに主語＋動詞が続く形。'
                 'the huge amount of information that reaches us every day の that は主格の関係代名詞で，reaches の主語は information（単数）。',
         'criteria': [('The reason is not simply ～, but …', 5), ('a lack of intelligence', 3),
                      ('the way our minds handle ～（the way＋主語＋動詞）', 6), ('the huge amount of information that reaches us every day', 4)]},
        {'kind': 'ja', 'marks': ['c'], 'tag': '内容説明', 'points': 20, 'lines': 4,
         'stem': '下線部（c）の実験の結果から，どのようなことがわかるか。第②段落の内容に沿って，日本語で説明せよ。',
         'answer': '学生たちは，以前に見たことのある文を，それが実際に正しいかどうかに関係なく，より信じられると評価した。'
                   'このことから，人は同じことを二度聞いただけで，それが本当である可能性が高いように感じてしまう（聞き覚えがあるものを真実だと受け入れやすい）ことがわかる。',
         'expl': 'regardless of whether ～「～かどうかに関係なく」。実験の結果（前に見た文ほど信じられると評価した）と，そこからわかること'
                 '（直後の Simply hearing something twice made it seem more likely to be true，および段落前半の the illusion of truth の説明）の両方を書く。',
         'criteria': [('以前に見た文をより信じられると評価した', 6), ('実際に正しいかどうかに関係なく', 6),
                      ('二度聞くだけで本当らしく感じる（聞き覚えがあると真実だと思いやすい）', 8)]},
        {'kind': 'combo', 'marks': ['d'], 'tag': '空所補充（語の選択）', 'points': 6,
         'stem': '空所（ d ）に入れるのにふさわしい語を，（ア）〜（エ）から1つ選んで記号で書け。',
         'rows': [('more',), ('less',), ('most',), ('much',)], 'answer': 1,
         'expl': '後半の and more likely to press the share button at once と対になるので，「立ち止まって事実を確かめる可能性は低くなる」の less が入る。'
                 'more では後半と同じ向きになり，対比にならない。most・much は likely の前の比較の形として合わない。'},
        {'kind': 'ja', 'marks': ['e'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='e'), 'lines': 3,
         'answer': '私たちは，友人や家族から送られてきたメッセージをより信じがちである。それは，メッセージそのものを調べたからではなく，それを送ってきた人を信頼しているからである。',
         'expl': 'be inclined to ～「～する傾向がある，～しがちだ」。because ～, not because …「…だからではなく～だから」の対比。'
                 'the person who sent it の it は a message。examined the message itself「メッセージそのものを調べた」。itself は強調。',
         'criteria': [('We are more inclined to trust a message', 4), ('when it comes from a friend or family member', 4),
                      ('because ～, not because … の対比', 6), ('the message itself（強調）', 4)]},
        {'kind': 'choice', 'marks': ['f'], 'tag': '空所補充（語の選択）', 'points': 6, 'stem': CH.format(x='f'),
         'options': ['leave', 'reach', 'repeat', 'build'], 'answer': 1,
         'expl': '自分と同じ意見に囲まれると，反対の意見が画面に「届く」ことがめったになくなる，という意味なので reach が入る。'
                 'leave（離れる）では「めったに画面から離れない」となり意味が逆になる。'},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第⑤段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['In prebunking, people learn about common tricks before they meet false stories.',
                        'The study in Ellisford included fewer than one thousand volunteers.',
                        'Players of the game were better at recognizing misleading posts a week afterward.',
                        'The game worked well only for players with a high level of education.'],
         'answers': ['〇', '×', '〇', '×'],
         'expl': '（ア）people are shown in advance the tricks に合うので〇。（イ）1,200 volunteers なので×。'
                 '（ウ）about 20 percent better at spotting misleading posts a week later に合うので〇。（エ）did not depend on ... level of education とあるので×。各4点。'},
        {'kind': 'ja', 'marks': ['g'], 'tag': '下線部和訳', 'points': 16, 'stem': TR.format(x='g'), 'lines': 3,
         'answer': 'その効果は小さかったが長続きし，また，参加者の政治的な意見や教育の程度に左右されなかった。',
         'expl': 'small but lasting「小さいが持続する」。lasting は「長く続く」という形容詞。depend on ～「～に左右される，～しだいである」。'
                 'the players\' political opinions or level of education の players\' は複数形の所有格で，political opinions と level of education の両方にかかる。',
         'criteria': [('The effect was small but lasting', 6), ('it did not depend on ～', 5), ('the players\' political opinions or level of education', 5)]},
        {'kind': 'ja', 'marks': ['h'], 'tag': '内容説明', 'points': 22, 'lines': 4,
         'stem': '下線部（h）の “these steps” とは具体的にどのようなことか。第⑥段落の内容に沿って，3つ日本語で説明せよ。',
         'answer': '①おどろくようなメッセージを共有する前に，誰が書いたのか，どんな証拠を示しているのかを確かめること。'
                   '②同じ情報を，信頼できるいくつかのサイトで探してみること。'
                   '③強い感情をかき立てる投稿には特に注意すること（その感情こそが書き手のねらいかもしれないから）。',
         'expl': 'these steps は直前の3つの命令文（ask who wrote it and what evidence it offers / Search for the same information on a few reliable sites / Be especially careful with posts that make you feel strong emotions）を指す。'
                 '3つ目は because 以下の理由もそえると，より正確な説明になる。',
         'criteria': [('誰が書いたか・どんな証拠があるかを確かめる', 8), ('信頼できる複数のサイトで同じ情報を探す', 7),
                      ('強い感情をかき立てる投稿に特に注意する', 7)]},
        {'kind': 'choice', 'marks': ['i'], 'tag': '空所補充（接続詞）', 'points': 8, 'stem': CH.format(x='i'),
         'options': ['although', 'unless', 'if only', 'even if'], 'answer': 3,
         'expl': '「たとえ読者のほんの一部だけでも共有の前に立ち止まれば，誤った話の広がりはずっと遅くなるだろう」という意味にする。'
                 '後ろの would travel から仮定の文で，「たとえ～でも」の even if が入る。unless（～しない限り）では逆の意味になり，if only は「～でありさえすれば（いいのに）」という願望を表す。'},
        {'kind': 'ja', 'marks': ['j'], 'tag': '下線部和訳', 'points': 12, 'stem': TR.format(x='j'), 'lines': 3,
         'answer': '結局，私たちのまわりにある情報の質は，それを作る人々だけでなく，何を人に伝えるかを決める私たち一人ひとりにもかかっているのである。',
         'expl': 'depend not only on ～ but also on …「～だけでなく…にも左右される（かかっている）」。each of us who decides what to pass on「何を伝えるかを決める私たち一人ひとり」。'
                 'pass on「（ほかの人へ）回す，伝える」。',
         'criteria': [('the quality of the information around us', 3), ('depends not only on ～ but also on …', 4),
                      ('the people who create it', 2), ('each of us who decides what to pass on', 3)]},
    ],
    'translation': [
        '毎分，何百万もの短いメッセージや写真や動画がインターネット上で共有されている。正確なものもあれば，まちがっているものも，わざとうそをついているものもある。それらを見分けるのは，見た目より難しいことが多い。たいていの人は，自分ならその違いを簡単に見分けられると思っている。'
        '実際には，十分な教育を受けた大人でさえ，自分が思っている以上にだまされていることを，研究はくり返し示している。'
        '(b)その理由は，単に知性が足りないことではなく，毎日私たちのもとに届く膨大な量の情報を，私たちの頭が処理するやり方にある。',
        '私たちの脳は，近道をすることでエネルギーを節約している。ある文に聞き覚えがあると感じると，最初にどこで聞いたのか思い出せなくても，それを本当だと受け入れがちである。心理学者はこれを「真実の錯覚」と呼ぶ。'
        'ターンリー大学で行われたある実験では，学生たちが，正しいものとまちがったものがまざった文の一覧を読んだ。1週間後，学生たちはその一覧を新しい文といっしょにもう一度見せられた。'
        '(c)学生たちは，以前に見たことのある文を，それが実際に正しいかどうかに関係なく，より信じられると評価した。ただ二度聞くだけで，そのことが本当である可能性が高いように思えたのである。',
        '感情も一役買っている。私たちを怒らせたり，こわがらせたり，おもしろがらせたりするメッセージは，冷静でていねいな説明よりもはるかに速く広がる。強い感情をいだいているとき，私たちは立ち止まって事実を確かめることが少なくなり，すぐに共有ボタンを押すことが多くなる。'
        'うその話を作る人々はこのことをよく知っていて，情報を伝えるためというより，強い反応を引き起こすようにメッセージを作ることが多い。ある身近な食べ物が「脳を破壊する」という見出しは，その食べ物が「一部の人の睡眠に少し影響するかもしれない」という見出しよりも，はるかに多くの注目を集めるだろう。',
        'もう一つの要因は，私たちがつき合う相手である。(e)私たちは，友人や家族から送られてきたメッセージをより信じがちである。それは，メッセージそのものを調べたからではなく，それを送ってきた人を信頼しているからである。'
        'さらに，インターネットのサービスは，ふつう，私たちが以前に「いいね」をしたものに似た内容を見せてくる。時がたつにつれて，これによって私たちは自分と同じ考えに囲まれ，反対の意見が画面に届くことはめったになくなるかもしれない。'
        'そのような閉ざされた空間の中では，誤った主張があまりに何度もくり返されて，常識のように見え始めることもある。',
        'どうすればよいのだろうか。研究者の中には，「プレバンキング」と呼ばれる方法を試した人々がいる。うその話が広がったあとで訂正するのではなく，にせの専門家，感情的な言葉，文脈から切り離された写真など，人をあざむくためによく使われる手口を，前もって人々に見せるのである。'
        'エリスフォードの町の1,200人のボランティアが参加した研究では，こうした手口を説明する短いオンラインゲームをした人々は，ゲームをしなかった人々に比べて，1週間後に誤解をまねく投稿を見抜く力が約20％高かった。'
        '(g)その効果は小さかったが長続きし，また，参加者の政治的な意見や教育の程度に左右されなかった。',
        '個人も簡単な習慣を身につけることができる。おどろくようなメッセージを共有する前に，誰が書いたのか，どんな証拠を示しているのかを問うこと。同じ情報を信頼できるいくつかのサイトで探すこと。'
        '強い感情をいだかせる投稿には特に注意すること。その感情こそが，書き手がねらったものかもしれないからである。'
        '(h)これらの手順はどれも1分とかからないが，あわせて行えば，私たちを信頼してくれている人々に，誤ったものを伝えてしまう可能性を大きく減らすことができる。',
        '誰もが目にするすべてのメッセージを確かめることを期待するのは現実的ではないだろう。それでも，たとえ読者のほんの一部だけでも共有の前に立ち止まれば，誤った話の広がりはずっと遅くなるだろう。多くの人の小さな行動が積み重なれば，大きな変化になりうる。'
        '(j)結局，私たちのまわりにある情報の質は，それを作る人々だけでなく，何を人に伝えるかを決める私たち一人ひとりにもかかっているのである。',
    ],
}

P2 = {
    'points': 150,
    'intro': '次の英文は，ある町で始まった「修理カフェ」を紹介している。',
    'title': 'The Repair Café',
    'passage': [
        "On the first Sunday of every month, a community hall in the town of Brackwood fills with broken things. People arrive carrying "
        "toasters that no longer heat, lamps that flicker, jackets with torn pockets, and bicycles with flat tires. They are not there to "
        "throw these items away. They have come to the Repair Café, where volunteers with practical skills help visitors fix their "
        "belongings for free. {b:a} the visitors wait, they can drink tea, chat with their neighbors, and watch the repairs as they "
        "happen.",
        "The café was started six years ago by Maren Holt, a retired electrician. She noticed that her neighbors were throwing away "
        "appliances that needed only a simple repair, such as a new fuse or a loose wire. {u:b|\"Many people assume that if something "
        "stops working, it must be replaced, because they have never been shown how easy some repairs can be,\" she explained.} She put "
        "up a few posters, borrowed tools from friends, and waited to see whether anyone would come. Thirty people turned up on the first "
        "day.",
        "Today the café has about twenty regular volunteers, including a former sewing teacher, two high school students who are good "
        "with computers, and a carpenter who fixes chairs and tables. According to the café's own records, it has repaired about 4,300 "
        "items since it opened, and roughly two out of three objects brought in leave the hall in working order. {u:c|The items that "
        "cannot be fixed are usually those whose spare parts are no longer sold, or those that were designed so that they are "
        "almost impossible to open.}",
        "This second problem has become a topic of public debate. Some products are sealed with special screws or strong glue, so that "
        "replacing a battery or a small part requires sending the whole device back to the maker, which can cost almost as much as "
        "buying a new one. Supporters of the \"right to repair\" argue that people who buy a product should be {b:d} to fix it themselves "
        "or take it to an independent repair shop. {u:e|Manufacturers, however, claim that opening devices can be dangerous for "
        "untrained users and may damage the product's safety features.}",
        "For Holt, however, the café is about more than saving money or reducing waste. {u:f|She believes that fixing something "
        "together changes the way people think about the objects they own.} When visitors see how their toaster works inside, they begin "
        "to treat it with more care. Several regular visitors have learned enough to repair simple items at home and now help others at "
        "the café. The repairs, she says, also repair something else: the {b:g} between neighbors who might otherwise never have met.",
        "The idea has begun to spread. Two nearby towns have opened their own repair cafés, and Holt receives letters from people who want "
        "to start one in their community. Her advice is always the same. \"You don't need experts in everything,\" she tells them. "
        "{u:h|\"What you need is a room, a few patient people, and the willingness to admit that you do not know how to fix something "
        "yet.\"} Some of the most successful repairs, she adds, were made by two volunteers who had never done that kind of repair "
        "before and simply worked it out together.",
        "Of course, a monthly café cannot solve the problem of waste by itself. Every year, millions of tons of electronic goods are "
        "thrown away around the world. {u:i|Still, by showing that a broken object is not necessarily the end of its story, places like "
        "the Repair Café may help to change habits that many people have never thought to question.} As one young visitor said while "
        "holding her newly repaired headphones, \"I didn't know you were {b:j} to fix things like this.\"",
    ],
    'notes': [(1, 'flicker', '（明かりが）ちらつく'), (2, 'appliance', '家庭用の電気製品'), (2, 'fuse', 'ヒューズ（電気の安全部品）'),
              (3, 'carpenter', '大工'), (4, 'manufacturer', '製造会社'), (6, 'willingness', '進んで〜する気持ち')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（接続詞）', 'points': 8, 'stem': CH.format(x='a'),
         'options': ['While', 'Unless', 'Until', 'Because'], 'answer': 0,
         'expl': '「来場者は待っている間に，お茶を飲んだり近所の人と話したりできる」という意味になるので，「～する間に」の While が入る。'
                 'Until（～するまで）は「待つのが終わるまでお茶を飲む」となり不自然。Unless・Because は意味が通らない。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': '「多くの人は，何かが動かなくなったら，それは取りかえなければならないと思いこんでいます。というのも，修理によってはどれほど簡単にできるものがあるのかを，一度も見せてもらったことがないからです」と彼女は説明した。',
         'expl': 'assume that ～「（よく考えずに）～と思いこむ」。must be replaced「取りかえられなければならない」。'
                 'have never been shown how easy some repairs can be は show ～ …（～に…を見せる）の受け身で，「いくつかの修理がどれほど簡単になりうるかを見せられたことがない」。'
                 'some repairs は「修理によっては（簡単なものもある）」と訳すと自然。',
         'criteria': [('Many people assume that ～', 3), ('if something stops working, it must be replaced', 5),
                      ('have never been shown（受け身・経験）', 5), ('how easy some repairs can be', 5)]},
        {'kind': 'ja', 'marks': ['c'], 'tag': '内容説明', 'points': 20, 'lines': 4,
         'stem': '下線部（c）によると，修理カフェで直せない品物は，主にどのようなものか。2種類，日本語で説明せよ。',
         'answer': '一つは，交換部品がもう売られていない品物。もう一つは，開けることがほとんどできないように設計されている品物（特殊なねじや強い接着剤で閉じられているものなど）。',
         'expl': 'those whose spare parts are no longer sold と those that were designed so that they are almost impossible to open の2つ。'
                 'those は items の代わり。whose は所有格の関係代名詞。2つ目は第④段落の special screws or strong glue が具体例になる。',
         'criteria': [('交換部品がもう売られていない', 10), ('開けることがほとんどできない作りになっている', 10)]},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第③段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['Among the regular volunteers there are two high school students who know a lot about computers.',
                        'The café has repaired fewer than 3,000 items since it opened.',
                        'About two thirds of the objects brought to the café are successfully fixed.',
                        'All of the volunteers used to work as professional repairers.'],
         'answers': ['〇', '×', '〇', '×'],
         'expl': '（ア）two high school students who are good with computers に合うので〇。（イ）about 4,300 items なので×。'
                 '（ウ）roughly two out of three objects ... leave the hall in working order に合うので〇。（エ）元裁縫の先生や高校生もいるので×。各4点。'},
        {'kind': 'choice', 'marks': ['d'], 'tag': '空所補充（語の選択）', 'points': 8, 'stem': CH.format(x='d'),
         'options': ['forbidden', 'free', 'afraid', 'unable'], 'answer': 1,
         'expl': '「修理する権利」を支持する人々の主張なので，製品を買った人は自分で修理したり独立した修理店に持ちこんだりする「自由がある」べきだ，となる。be free to ～「自由に～できる」。'
                 'forbidden（禁じられた）・unable（できない）は主張と逆の意味になる。'},
        {'kind': 'ja', 'marks': ['e'], 'tag': '下線部和訳', 'points': 16, 'stem': TR.format(x='e'), 'lines': 3,
         'answer': '一方，製造会社は，訓練を受けていない利用者が機器を開けるのは危険なことがあり，製品の安全のための機能をそこなうおそれもあると主張している。',
         'expl': 'however は「しかし，一方」で，前の文の「修理する権利」の支持者との対比。claim that ～「～と主張する」。'
                 'opening devices「機器を開けること」が動名詞の主語で，can be dangerous と may damage の2つの述語につながっている。untrained users「訓練を受けていない利用者」。',
         'criteria': [('Manufacturers, however, claim that ～', 4), ('opening devices can be dangerous for untrained users（動名詞の主語）', 6),
                      ('may damage the product\'s safety features', 6)]},
        {'kind': 'ja', 'marks': ['f'], 'tag': '内容説明', 'points': 24, 'lines': 4,
         'stem': '下線部（f）について，人々の考え方がどのように変わると筆者は述べているか。第⑤段落に挙げられている例を含めて，日本語で説明せよ。',
         'answer': 'いっしょに修理をして，トースターなどの中がどのように動いているのかを見ると，人々は自分の持ち物をより大切に扱うようになる。'
                   'さらに，常連の来場者の中には，家で簡単なものを直せるほど学び，今ではカフェでほかの人を手伝う人も出てきた。'
                   'また，修理を通じて，ふだんなら出会わなかったかもしれない近所の人どうしのつながりも生まれる。',
         'expl': '第⑤段落の具体例は3つ。①中の仕組みを見て持ち物を大切に扱うようになる，②常連が家で直せるようになり，ほかの人を手伝う，③近所の人どうしの結びつきが生まれる（The repairs ... also repair something else）。'
                 '①を中心に，②③も加えてまとめるとよい。',
         'criteria': [('中の仕組みを見る', 4), ('持ち物をより大切に扱うようになる', 8), ('家で直せるようになり，ほかの人を手伝う常連もいる', 6),
                      ('近所の人どうしのつながりが生まれる', 6)]},
        {'kind': 'combo', 'marks': ['g'], 'tag': '空所補充（語の選択）', 'points': 6,
         'stem': '空所（ g ）に入れるのにふさわしい語を，（ア）〜（エ）から1つ選んで記号で書け。',
         'rows': [('distance',), ('arguments',), ('walls',), ('connections',)], 'answer': 3,
         'expl': '修理が「直す」もう一つのものは，ふだんなら出会わなかったかもしれない近所の人どうしの「つながり」なので connections。'
                 'distance（距離）・arguments（口論）・walls（壁）を「直す（よくする）」とは言わない。'},
        {'kind': 'ja', 'marks': ['h'], 'tag': '下線部和訳', 'points': 14, 'stem': TR.format(x='h'), 'lines': 3,
         'answer': '「必要なのは，部屋と，何人かの忍耐強い人と，まだ何かの直し方を知らないと認める気持ちです。」',
         'expl': 'What you need is ～「あなたに必要なものは～だ」。the willingness to admit that ～「～と認めようとする気持ち」。'
                 'not ... yet「まだ～ない」。how to fix something「何かの直し方」。',
         'criteria': [('What you need is ～', 3), ('a room, a few patient people', 3), ('the willingness to admit that ～', 5), ('you do not know how to fix something yet', 3)]},
        {'kind': 'ja', 'marks': ['i'], 'tag': '下線部和訳', 'points': 16, 'stem': TR.format(x='i'), 'lines': 3,
         'answer': 'それでも，壊れた物が必ずしもその物語の終わりではないことを示すことによって，修理カフェのような場所は，多くの人々が疑ってみようと考えたことさえない習慣を変える助けになるかもしれない。',
         'expl': 'by showing that ～「～ということを示すことによって」。not necessarily「必ずしも～ではない」（部分否定）。'
                 'habits that many people have never thought to question「多くの人々が疑ってみようと一度も考えたことのない習慣」。help to ～「～するのに役立つ」。',
         'criteria': [('by showing that ～', 3), ('a broken object is not necessarily the end of its story（部分否定）', 5),
                      ('places like the Repair Café may help to change habits', 4), ('that many people have never thought to question', 4)]},
        {'kind': 'choice', 'marks': ['j'], 'tag': '空所補充（語の選択）', 'points': 4, 'stem': CH.format(x='j'),
         'options': ['forced', 'sorry', 'allowed', 'likely'], 'answer': 2,
         'expl': '直ったばかりのヘッドホンを手にした若い来場者の言葉で，「こういうものを自分で直してもいいなんて知らなかった」となる allowed が入る。be allowed to ～「～してもよい」。'
                 'forced（強いられる）では意味が通らない。'},
    ],
    'translation': [
        '毎月第1日曜日，ブラックウッドの町の公民館は壊れた物でいっぱいになる。人々は，もう温まらないトースター，ちらつく電気スタンド，ポケットの破れた上着，パンクした自転車などを持ってやって来る。'
        '彼らはそれを捨てに来たのではない。修理カフェに来たのである。そこでは，実用的な技術を持つボランティアが，来場者の持ち物を無料で直す手伝いをしている。来場者は待っている間に，お茶を飲んだり，近所の人とおしゃべりしたり，目の前で行われる修理を見たりすることができる。',
        'このカフェは，6年前に，引退した電気技師のマレン・ホルトが始めた。彼女は，近所の人たちが，新しいヒューズやゆるんだ電線のように，簡単な修理しか必要のない電気製品を捨てていることに気づいた。'
        '(b)「多くの人は，何かが動かなくなったら，それは取りかえなければならないと思いこんでいます。というのも，修理によってはどれほど簡単にできるものがあるのかを，一度も見せてもらったことがないからです」と彼女は説明した。'
        '彼女はポスターを何枚か貼り，友人から道具を借りて，誰か来るかどうか様子を見た。初日には30人がやって来た。',
        '今日，このカフェには約20人の常連のボランティアがいる。元裁縫の先生，コンピュータにくわしい高校生2人，いすやテーブルを直す大工などである。カフェ自身の記録によると，開店以来約4,300点の品物を修理し，持ちこまれた物のおよそ3つに2つは，使える状態になって公民館をあとにする。'
        '(c)直せない品物は，たいてい，交換部品がもう売られていないものか，開けることがほとんど不可能なように設計されているものである。',
        'この2つ目の問題は，社会で議論の的になっている。製品の中には，特殊なねじや強い接着剤で閉じられているものがあり，電池や小さな部品を交換するには機器全体を製造会社に送り返さなければならず，その費用は新品を買うのとほとんど変わらないこともある。'
        '「修理する権利」の支持者は，製品を買った人は，自分でそれを直したり，独立した修理店に持ちこんだりする自由があるべきだと主張する。'
        '(e)一方，製造会社は，訓練を受けていない利用者が機器を開けるのは危険なことがあり，製品の安全のための機能をそこなうおそれもあると主張している。',
        'しかし，ホルトにとって，このカフェはお金の節約やごみを減らすことだけが目的ではない。(f)何かをいっしょに直すことは，人々が自分の持ち物について考える考え方を変える，と彼女は信じている。'
        '来場者は，自分のトースターが中でどのように動いているのかを見ると，それをより大切に扱うようになる。常連の来場者の中には，家で簡単な物を直せるほど学び，今ではカフェでほかの人を手伝っている人もいる。'
        '修理は別のものも直すのだと彼女は言う。そうでなければ出会うことがなかったかもしれない近所の人どうしのつながりである。',
        'この考えは広がり始めている。近くの2つの町がそれぞれの修理カフェを開き，ホルトのもとには自分の地域でも始めたいという人々から手紙が届く。彼女の助言はいつも同じだ。「何でも知っている専門家はいりません」と彼女は伝える。'
        '(h)「必要なのは，部屋と，何人かの忍耐強い人と，まだ何かの直し方を知らないと認める気持ちです。」最もうまくいった修理のいくつかは，その種の修理をしたことのなかったボランティア2人が，ただいっしょに考えて解決したものだったと彼女はつけ加える。',
        'もちろん，月に一度のカフェだけでごみの問題を解決することはできない。世界中で毎年，何百万トンもの電子機器が捨てられている。'
        '(i)それでも，壊れた物が必ずしもその物語の終わりではないことを示すことによって，修理カフェのような場所は，多くの人々が疑ってみようと考えたことさえない習慣を変える助けになるかもしれない。'
        'ある若い来場者は，直ったばかりのヘッドホンを手にしながら，「こういうものを自分で直してもいいなんて知らなかった」と言った。',
    ],
}
