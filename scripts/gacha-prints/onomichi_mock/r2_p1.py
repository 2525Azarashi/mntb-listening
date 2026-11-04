# -*- coding: utf-8 -*-
# 第2回 Ⅰ：手書きのメモと記憶（解説文。書き下ろし。人物・大学・実験は架空）
P1 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'Why the Pen Still Matters',
    'passage': [
        "In many university lecture halls today, the sound of pens moving across paper has been replaced by the quiet tapping of keyboards. "
        "Typing is fast, neat and easy to search later. It seems obvious that students who type their notes {r1}. A number of studies, "
        "however, suggest that the slower method may help us remember more.",

        "At Linfield College, a psychologist named Daniel Okoro asked a group of first-year students to watch three short talks on topics "
        "they knew little about, such as the history of glass and the life of deep-sea fish. Half of the students took notes on laptops, and "
        "the other half used pens and notebooks. A week later, both groups were given a test on the talks. The students who had written by "
        "hand {p2} the typists, especially on questions that asked them to explain ideas rather than repeat facts.",

        "At first this result seems strange. The typists had written down almost twice as many words, so they should have had more information "
        "to study. Okoro believes that this was the real reason {bA} the difference. Because typing is fast, many students simply copied what the speaker "
        "said, word {bB} word, without thinking about it. Writing by hand is too slow for that. “When you cannot write everything down,” Okoro "
        "explains, “you are {u3|forced} to decide what is important and to put it in your own words.”",

        "That act of choosing and summarizing is a form of thinking. In order to shorten an idea, a student has to understand it first, and "
        "understanding is what makes information {p4} in the memory. In other words, the extra effort that handwriting requires is not a "
        "weakness but the very reason it works.",

        "Some researchers have also pointed out that laptops bring {u5|distractions} with them. A message from a friend, a news headline or a "
        "video can pull attention away from the lecture in a second. In Okoro’s study, students using laptops were not allowed to go online, but "
        "in real classrooms there is no such rule, and the gap between the two groups {r6}.",

        "This does not mean that keyboards should be banned. For students with certain disabilities, typing may be the only practical way to "
        "take notes, and some people simply write too slowly to keep up with a fast speaker. Okoro himself types most of his emails and papers. "
        "His advice is not to give up technology but to use it {p7}. Students who type, he suggests, can still benefit if they try to "
        "summarize instead of copying.",

        "Perhaps the most useful lesson is that learning is not the same as collecting information. A notebook full of every word a teacher said "
        "may look impressive, but a single page of short, messy notes in your own words may be worth much more on the day of the exam.",
    ],
    'notes': [('lecture hall', '講義室'), ('deep-sea', '深海の'), ('summarize', '要約する'), ('disability', '障害')],
    'questions': [
        {'label': '問1', 'type': 'order', 'ref': 1, 'points': 4, 'kind': '語の並べかえ', 'seed': 2101,
         'words': ['would', 'have', 'an', 'advantage', 'over', 'those', 'who', "don't"],
         'ja': 'そうしない人たちより有利になるだろう',
         'stem': '下線部(1)が「そうしない人たちより有利になるだろう」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'have an advantage over …「…より有利である」。those who …「…する人たち」，don’t の後ろには type their notes が省略されている。'},
        {'label': '問2', 'type': 'mc', 'ref': 2, 'points': 3, 'kind': '空所補充',
         'stem': '空所(2)にあてはまる語句としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['did better than', 'were slower than', 'looked after', 'took over'], 'answer': 'イ',
         'expl': '手書きの学生のほうが，とくに説明を求める問題で「よくできた」。次の段落の「最初は奇妙に思える」もこの結果を受けている。'},
        {'label': '問3', 'type': 'word', 'points': 3, 'kind': '共通する語', 'answer': 'for',
         'stem': '第3段落の空所（ A ）と（ B ）には同じ1語が入る。その語を書きなさい。',
         'expl': '（A）the reason for …「…の理由」。（B）word for word「一語一語・逐語的に」。どちらも for。'},
        {'label': '問4', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(3)の意味にもっとも近いものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['allowed', 'made', 'invited', 'paid'], 'answer': 'ロ',
         'expl': 'be forced to do「〜せざるをえない」＝ be made to do。全部は書けないので，何が大事かを決めるしかない，という文脈。'},
        {'label': '問5', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '空所補充',
         'stem': '空所(4)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['stay', 'stays', 'to stay', 'staying'], 'answer': 'イ',
         'expl': '使役動詞 make O do「Oに〜させる」なので原形 stay。「理解することが情報を記憶にとどまらせる」。'},
        {'label': '問6', 'type': 'mc', 'ref': 5, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(5)の具体例として本文に挙げられていないものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['a message from a friend', 'a news headline', 'a video', 'a noisy classmate'], 'answer': 'ニ',
         'expl': '直後の文で挙がっているのは友人からのメッセージ，ニュースの見出し，動画の3つ。うるさい同級生は書かれていない。'},
        {'label': '問7', 'type': 'order', 'ref': 6, 'points': 4, 'kind': '語の並べかえ', 'seed': 2106,
         'words': ['might', 'be', 'even', 'larger', 'than', 'it', 'was', 'in'],
         'ja': '彼の研究のときよりさらに大きいかもしれない',
         'stem': '下線部(6)が「彼の研究のときよりさらに大きいかもしれない」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。なお，下線部の直後に his study が続くものとする。',
         'expl': 'might be ＋比較級「〜かもしれない」。比較級を強める even，than it was in his study で「彼の研究のとき（の差）より」。'},
        {'label': '問8', 'type': 'mc', 'ref': 7, 'points': 3, 'kind': '空所補充',
         'stem': '空所(7)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['wisely', 'rarely', 'quickly', 'secretly'], 'answer': 'イ',
         'expl': 'テクノロジーを捨てるのではなく「賢く」使う。次の文の「写すのではなく要約する」が賢い使い方の具体例。'},
        {'label': '問9', 'type': 'tf', 'points': 7, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('オコロの実験では，学生は1週間後に講義の内容についてのテストを受けた。', True),
             ('パソコンでメモをとった学生は，手書きの学生よりも書いた語数が少なかった。', False),
             ('オコロは，手書きに余分な手間がかかることこそが，記憶に役立つ理由だと考えている。', True),
             ('オコロの実験では，パソコンを使う学生もインターネットを自由に使うことができた。', False),
             ('オコロは，大学の講義ではキーボードの使用を禁止すべきだと主張している。', False),
         ],
         'expl': '(ア) 第2段落 A week later…。(イ) 第3段落：ほぼ2倍の語数を書いた。(ウ) 第4段落の最後の文。(エ) 第5段落 were not allowed to go online。(オ) 第6段落 This does not mean that keyboards should be banned。'},
    ],
    'translation': [
        '今日，多くの大学の講義室では，紙の上を走るペンの音が，キーボードを打つ静かな音に取って代わられた。タイピングは速く，きれいで，あとから検索するのも簡単だ。メモをタイプする学生は，そうしない学生より有利になるだろうというのは当然に思える。ところが多くの研究は，遅いほうの方法のほうが多くのことを覚えるのに役立つかもしれないと示している。',
        'リンフィールド大学で，ダニエル・オコロという心理学者は1年生のグループに，ガラスの歴史や深海魚の生態など，あまりよく知らない話題についての短い講演を3つ見てもらった。学生の半分はノートパソコンで，残りの半分はペンとノートでメモをとった。1週間後，両方のグループは講演についてのテストを受けた。手書きでメモをとった学生のほうがタイプした学生よりよくでき，とくに事実をくり返すのではなく考えを説明するよう求める問題でその差が大きかった。',
        'この結果は最初は奇妙に思える。タイプした学生はほぼ2倍の語数を書いていたのだから，勉強に使える情報は多かったはずだ。オコロは，それこそが差の本当の理由だったと考えている。タイピングは速いので，多くの学生は話し手が言ったことを考えもせず一語一語そのまま写していた。手書きではそれをするには遅すぎる。「すべてを書きとれないとき，人は何が大事かを決め，それを自分の言葉で表さざるをえないのです」とオコロは説明する。',
        '選んで要約するというその行為は，考えることの一つの形である。考えを短くするためには，まずそれを理解しなければならない。そして理解することこそが，情報を記憶にとどまらせるのだ。言いかえれば，手書きに必要な余分な努力は欠点ではなく，手書きが効果をもつ理由そのものなのである。',
        'ノートパソコンは気を散らすものもいっしょに持ちこむと指摘する研究者もいる。友人からのメッセージやニュースの見出し，動画は，一瞬で講義から注意をそらしてしまう。オコロの研究では，パソコンを使う学生はインターネットにつなぐことを許されていなかったが，実際の教室にはそのような決まりはなく，2つのグループの差は彼の研究のときよりさらに大きいかもしれない。',
        'だからといって，キーボードを禁止すべきだというわけではない。ある種の障害をもつ学生にとっては，タイピングが唯一の現実的なメモのとり方かもしれないし，話すのが速い人についていけないほど書くのが遅い人もいる。オコロ自身もメールや論文のほとんどをタイプしている。彼の助言はテクノロジーをやめることではなく，それを賢く使うことだ。タイプする学生も，写すのではなく要約しようとすれば，やはり効果が得られると彼は言う。',
        'おそらくいちばん役に立つ教訓は，学ぶことは情報を集めることと同じではないということだろう。先生の言ったことが一語残らず書かれたノートは立派に見えるかもしれないが，自分の言葉で書いた短くて雑なメモ1ページのほうが，試験の日にはずっと価値があるかもしれない。',
    ],
    'vocab': [('replace', '取って代わる'), ('obvious', '明らかな'), ('advantage', '有利な点'), ('copy', '写す'),
              ('weakness', '弱点'), ('distraction', '気を散らすもの'), ('ban', '禁止する'), ('practical', '現実的な'),
              ('keep up with', '〜についていく'), ('benefit', '利益を得る'), ('impressive', '立派な'), ('messy', '散らかった・雑な')],
}
