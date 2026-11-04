# -*- coding: utf-8 -*-
"""第2回 Ⅳ 自由英作文（2つの問いから1つ・100語程度）。書き下ろし。"""
W = {
    'prompts': ['Should schools ban smartphones during the school day? Give reasons for your answer.',
                'Describe someone who has influenced you, and explain how that person changed you.'],
    'prompts_ja': ['学校は授業のある時間帯にスマートフォンを禁止するべきか。理由を挙げて答えよ。',
                   'あなたに影響を与えた人を一人描写し，その人があなたをどのように変えたかを説明せよ。'],
    'criteria': [('内容：問いに正面から答え，立場・人物がはっきりしている', 15),
                 ('理由・具体例：理由や出来事が具体的に書かれている', 15),
                 ('構成：導入・理由（出来事）・まとめの流れがあり，つなぎの語が適切', 8),
                 ('語法・文法：時制・数・語順などの誤りが少ない', 8),
                 ('分量：100語程度（おおむね90〜120語）', 4)],
    'models': [
        (0, "In my opinion, schools should not ban smartphones completely, but they should limit their use during lessons. "
            "To begin with, phones can be useful study tools. Students can check the meaning of a word or look at a map in a geography class within seconds. "
            "Moreover, many parents feel safer when their children can contact them on the way home. "
            "On the other side, phones can easily distract students from what the teacher is saying. "
            "Therefore, a sensible rule would be to keep phones in bags during class and allow them only at lunch or when a teacher asks students to use them. "
            "This balance protects both learning and safety."),
        (1, "The person who has influenced me most is my former basketball coach, Ms. Hara. "
            "When I joined the team at junior high, I was shy and gave up easily whenever I made a mistake. "
            "Ms. Hara never shouted at us. Instead, after each game she asked every player to name one thing they had done well and one thing to improve. "
            "At first this felt strange, but slowly I began to see my mistakes as chances to grow. "
            "Thanks to her, I now try new things without worrying so much about failing. "
            "I hope to encourage younger players as she encouraged me."),
    ],
    'models_ja': [
        '私の意見では，学校はスマートフォンを完全に禁止するべきではないが，授業中の使用は制限するべきだ。まず，スマートフォンは役に立つ学習の道具になりうる。生徒は単語の意味を調べたり，地理の授業で地図を見たりすることが数秒でできる。さらに，多くの親は子どもが帰り道に連絡を取れるほうが安心する。一方で，スマートフォンは生徒の注意を先生の話からそらしやすい。したがって，授業中はかばんにしまい，昼休みか先生が使うよう指示したときだけ使ってよいというのが分別のあるきまりだろう。この釣り合いが，学習と安全の両方を守る。',
        '私に最も影響を与えた人は，以前のバスケットボールのコーチのハラ先生だ。中学校でチームに入ったとき，私は内気で，失敗するたびにすぐあきらめていた。ハラ先生は決して私たちをどなりつけなかった。その代わりに，試合のたびに，選手一人一人にうまくできたことを一つと改善すべきことを一つ挙げさせた。最初は奇妙に感じたが，少しずつ私は自分の失敗を成長の機会と見るようになった。先生のおかげで，私は今では失敗をあまり気にせずに新しいことに挑戦している。私も先生が励ましてくれたように，年下の選手たちを励ましたい。',
    ],
    'tips': ['(1) は「全面禁止」「全面許可」以外に「条件つき」の立場もとれる。その場合も最初の文で立場をはっきり書く。',
             '(2) は人物の説明だけで終わらせず，「どう変わったか」（以前→今）を必ず書く。問いの後半に答えていないと内容点が大きく下がる。',
             '過去の出来事は過去形，今の自分は現在形と，時制を書き分ける。',
             'influence は動詞（〜に影響を与える）としても名詞（影響）としても使える。influence on ~ と前置詞を付けるのは名詞のとき。',
             '書き終えたら語数を数え，100語程度（90〜120語）に収める。'],
}
