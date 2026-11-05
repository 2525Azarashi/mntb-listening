# -*- coding: utf-8 -*-
# 第1回 Part 2（英作文）・Part 3（会話の空所に4つの文から選ぶ）
P2 = {
    'points': 24,
    'lead': '次の問いについて，あなたの考えを英語で書きなさい。150 語以上で書き，最後に使った語数を書くこと。',
    'prompt': 'Imagine that your town has enough money to build one new public facility, such as a library, a sports center or a park. '
              'Which facility would you choose, and why? Explain how it would change the lives of the people in your town.',
    'prompt_ja': 'あなたの町に，図書館・スポーツセンター・公園など，新しい公共施設を一つ建てるだけのお金があると想像しなさい。あなたならどの施設を選びますか。それはなぜですか。その施設が町の人々の暮らしをどう変えるかを説明しなさい。',
    'model': "If my town could build one new public facility, I would choose a large library with a café and study rooms. "
             "At the moment, our town has only a small library that closes at five o’clock, so students like me have nowhere quiet "
             "to study in the evening.\n"
             "A new library would help people of all ages. Students could prepare for exams together in the study rooms, and parents "
             "could bring their small children to reading events on weekends. Older residents, who often feel lonely, could meet friends "
             "in the café and join computer classes. In this way, the library would become a place where different generations meet.\n"
             "Some people may say that a sports center is more useful because it keeps people healthy. However, a library is cheaper to run, "
             "and it is open to everyone, even people who cannot do sports. For these reasons, I believe a library would make our town "
             "a better place to live.",
    'model_ja': [
        'もし私の町が新しい公共施設を一つ建てられるなら，私はカフェと自習室のある大きな図書館を選ぶ。今，町には5時に閉まる小さな図書館しかないので，私のような学生は夜に静かに勉強できる場所がない。',
        '新しい図書館はあらゆる年代の人の役に立つだろう。学生は自習室でいっしょに試験勉強ができ，親は週末に小さな子どもを読み聞かせの催しに連れて来られる。寂しさを感じることの多い年配の住民も，カフェで友人と会ったりパソコン教室に参加したりできる。このように，図書館はさまざまな世代が出会う場所になるだろう。',
        'スポーツセンターのほうが人々を健康にするので役に立つと言う人もいるかもしれない。しかし，図書館は運営費が安く，スポーツができない人も含めて誰にでも開かれている。これらの理由から，図書館があれば私たちの町はもっと住みよい場所になると私は思う。',
    ],
    'tips': [
        '最初の文で「何を選ぶか」をはっきり書き，次に今の町の問題点（なぜ必要か）を書くと，理由に説得力が出る。',
        '「誰の暮らしがどう変わるか」を，学生・親子・高齢者のように具体的な人に分けて書くと，150語に無理なく届く。',
        '反対の意見（Some people may say …）を一つ取り上げて However で答えると，考えの深さを示せる。',
        '仮定の話なので，would / could を使う（I would choose …, Students could …）。will ばかりにならないよう注意。',
        '最後に For these reasons, … で結論をくり返し，語数（150 words 以上）を必ず確認する。',
    ],
    'criteria': [
        ('問いに答えている：選んだ施設とその理由がはっきり書かれている', 6),
        ('内容：町の人々の暮らしがどう変わるかが具体的に説明されている', 6),
        ('構成：導入・理由と具体例・結論の流れがあり，つなぎの語句が使われている', 4),
        ('英語の正確さ：文法・語法・つづりの誤りが少なく，意味が通じる', 6),
        ('語数：150語以上（不足する場合は大きく減点）', 2),
    ],
}

P3 = {
    'points': 12,
    'type': 'choose',
    'lead': '次の 1〜4 の会話の空所に入れるのにもっとも適切なものを，下の ①〜④ からそれぞれ一つ選び，番号を書きなさい。ただし，同じものを2回以上使ってはいけない。',
    'options': [
        'Better late than never.',
        'Two heads are better than one.',
        'Actions speak louder than words.',
        'Don’t put all your eggs in one basket.',
    ],
    'convs': [
        [('A', 'This math problem is impossible. I’ve been working on it for an hour.'),
         ('B', 'Why don’t we try to solve it together?'),
         ('A', 'Good idea. {blank}')],
        [('A', 'I’m only going to apply to one university. I’m sure I’ll pass.'),
         ('B', 'Are you? You should apply to a few more, just in case.'),
         ('A', 'Why?'),
         ('B', '{blank}')],
        [('A', 'Ken keeps saying he’ll help us clean the classroom.'),
         ('B', 'But he never actually comes, does he?'),
         ('A', 'No. {blank}')],
        [('A', 'Sorry, I’ve only just finished the report you asked for last week.'),
         ('B', 'Don’t worry. {blank} Thank you for finishing it.')],
    ],
    'answers': [1, 3, 2, 0],
    'expl': [
        '「いっしょに解こう」と言われて「いい考えだ」と答える場面。「二人寄れば文殊の知恵（一人より二人で考えるほうがよい）」の ② が合う。',
        '一つの大学しか受けないという相手に「念のためもっと受けたほうがいい」と助言している。「一つのかごに卵を全部入れるな（一つのことにすべてを賭けるな）」の ④。',
        '手伝うと言うだけで実際には来ない Ken について話している。「行動は言葉より雄弁だ（口で言うより何をするかが大事）」の ③。',
        '遅れて報告書を出した相手に「気にしないで」と言っている。「遅れてもしないよりはまし」の ①。',
    ],
    'ja': [
        '①遅れてもしないよりはまし。②二人寄れば文殊の知恵。③行動は言葉より雄弁だ。④一つのかごに卵を全部入れるな。',
        '1　A：この数学の問題は無理だよ。もう1時間も取り組んでいるんだ。　B：いっしょに解いてみない？　A：いい考えだね。二人寄れば文殊の知恵だ。',
        '2　A：大学は一つだけ受けるつもりなんだ。きっと受かるよ。　B：そう？念のためもう少し受けたほうがいいよ。　A：どうして？　B：一つのかごに卵を全部入れちゃだめだよ。',
        '3　A：ケンは教室の掃除を手伝うってずっと言っているよね。　B：でも実際には一度も来ないよね。　A：うん。口で言うより行動が大事なのに。',
        '4　A：ごめんなさい，先週頼まれた報告書，今やっと終わりました。　B：気にしないで。遅れてもしないよりはましだよ。仕上げてくれてありがとう。',
    ],
}
