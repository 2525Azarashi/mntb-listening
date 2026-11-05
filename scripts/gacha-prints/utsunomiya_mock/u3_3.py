# -*- coding: utf-8 -*-
"""第3回 第3問 意見を述べる英作文（約150語）・第4問 会話文の完成。書き下ろし。調査・団体・数値は架空。"""
ESSAY = {
    'passage': "The city library of Fenwick is thinking about replacing half of its printed books with e-books in order to save space and money. "
               "In a recent survey of 1,500 library users, many younger people supported the plan, pointing out that e-books can be borrowed at any hour and never have to be carried back to the building. "
               "However, many other users said that they find paper books easier on the eyes and enjoy discovering titles by walking along the shelves. "
               "The library will announce its decision in the autumn.",
    'passage_ja': 'フェンウィック市立図書館は，場所と費用を節約するために，紙の本の半分を電子書籍に置き換えることを検討している。最近の1,500人の利用者への調査では，多くの若い人がこの計画を支持し，電子書籍はいつでも借りられ，建物に返しに行く必要もないと指摘した。一方で，紙の本のほうが目にやさしく，書棚に沿って歩きながら本を見つけるのが楽しいと答えた利用者も多かった。図書館は秋に決定を発表する予定である。',
    'question': 'Do you think public libraries should replace many of their paper books with e-books? Include reasons for your view.',
    'question_ja': '公立図書館は紙の本の多くを電子書籍に置き換えるべきだと思うか。理由を挙げて自分の立場を説明せよ。',
    'criteria': [('内容：問いに対する立場が明確で，英文の論点を踏まえている', 12),
                 ('理由：理由が2つ程度あり，具体例や説明で支えられている', 12),
                 ('構成：導入・理由・結論の流れがあり，つなぎの語が適切', 6),
                 ('語法・文法：時制・数・冠詞・語順などの誤りが少ない', 7),
                 ('分量：約150語（おおむね130〜170語）で，語数を正しく記入している', 3)],
    'models': [
        ('置き換えるべきだという立場',
         "I believe public libraries should replace many of their paper books with e-books. "
         "First, e-books make libraries available to more people. Students who study late at night and workers who are busy during the day can borrow a book whenever they like, without traveling to the library. "
         "This is especially helpful for residents living far from the building or who have difficulty walking. "
         "Second, libraries can use their money more wisely. Printed books take up a great deal of space and wear out after being borrowed many times, while e-books never get damaged. "
         "The money saved could be spent on longer opening hours or study rooms. "
         "Some readers prefer paper, so libraries should keep popular printed books. "
         "Still, I am convinced that offering more e-books would allow libraries to serve the whole community better."),
        ('置き換えるべきではないという立場',
         "In my opinion, public libraries should keep most of their paper books. "
         "My first reason is that not everyone can use e-books easily. Some elderly people are not familiar with digital devices, and some families cannot afford a tablet. "
         "A library should be a place where anyone can read for free, so it must not depend too much on technology. "
         "My second reason is that browsing the shelves leads to unexpected discoveries. When I look for one book, I often notice another interesting title next to it. "
         "This kind of chance meeting rarely happens on a screen, where we usually search only for what we already know. "
         "Libraries could certainly add some e-books for convenience. "
         "However, replacing half of their printed collection would take away something valuable, so I am against the plan."),
    ],
    'models_ja': [
        '私は，公立図書館は紙の本の多くを電子書籍に置き換えるべきだと考える。第一に，電子書籍は図書館をより多くの人が利用できるものにする。夜遅くに勉強する学生や昼間忙しい労働者も，図書館まで出かけることなく，好きなときに本を借りられる。これは建物から遠くに住む人や歩くのが難しい人にとって特に役に立つ。第二に，図書館はお金をより賢く使えるようになる。紙の本は多くの場所を取り，何度も貸し出されるうちに傷んでしまうが，電子書籍は決して傷まない。節約したお金は，開館時間の延長や自習室に使えるだろう。紙を好む読者もいるので，図書館は人気のある紙の本は残すべきだ。それでも，電子書籍を増やすことで，図書館は地域全体により役立つことができると確信している。',
        '私の意見では，公立図書館は紙の本の大半を残すべきである。第一の理由は，誰もが電子書籍を簡単に使えるわけではないことだ。デジタル機器に慣れていない高齢者もいるし，タブレットを買う余裕のない家庭もある。図書館は誰でも無料で本が読める場所であるべきなので，技術に頼りすぎてはならない。第二の理由は，書棚を見て回ることが思いがけない発見につながることだ。私はある本を探しているとき，その隣にある別のおもしろい本に気づくことがよくある。こうした偶然の出会いは，すでに知っているものだけを検索することが多い画面上では，めったに起こらない。もちろん，図書館が便利さのために電子書籍をいくらか加えることはできる。しかし，紙の蔵書の半分を置き換えれば価値のあるものが失われてしまうので，私はこの計画に反対である。',
    ],
    'tips': ['最初の1文で立場を明確にする。英文の賛成意見・反対意見を要約するだけでは自分の意見にならない。',
             '理由は2つにしぼり，First / Second や My first reason is ~ / My second reason is ~ で整理する。具体的な利用者の姿（学生・高齢者など）を挙げると説得力が出る。',
             '反対側に一部譲歩して（Some readers prefer ~ / Libraries could certainly ~）から自分の結論に戻ると，バランスのよい文章になる。',
             'replace A with B（AをBに置き換える）の語順に注意。「BでAを置き換える」と考えると覚えやすい。',
             'e-books / paper books / printed books などの名詞は複数形で一般論を表す。最後に語数を記入する。'],
}
CONVS = [
    {'label': 'A', 'setting': 'Priya and her younger brother Kiran are talking at home on Saturday morning.',
     'lines': [('Priya', 'Kiran, Mom\'s birthday is tomorrow. Have you got a present yet?'),
               ('Kiran', None),
               ('Priya', 'Neither have I. Any ideas about what she would like?'),
               ('Kiran', None),
               ('Priya', 'Good idea, but we cannot cook very well.'),
               ('Kiran', None),
               ('Priya', 'All right. Let us go to the supermarket this afternoon.'),
               ('Kiran', None)],
     'answers': ['No, not yet. I completely forgot about it',
                 'She is always busy, so why don\'t we make dinner for her',
                 'Then let us choose a simple dish and practice it tonight',
                 'OK. I will write a list of what we need'],
     'ja': ['プリヤ：キラン，お母さんの誕生日は明日だよ。プレゼントはもう用意した？', 'キラン：（1）', 'プリヤ：私もまだなの。何を喜ぶと思う？', 'キラン：（2）', 'プリヤ：いい考えだね。でも私たち，料理はあまり得意じゃないよ。', 'キラン：（3）', 'プリヤ：わかった。今日の午後スーパーに行こう。', 'キラン：（4）'],
     'explain': ['(1)：直後にプリヤが Neither have I.（私もまだ）と言っているので，まだ用意していないと否定で答える。',
                 '(2)：プリヤが Good idea と応じ，さらに料理の話をしているので，料理に関わる案を出す。',
                 '(3)：「料理が得意でない」という心配に対し，それを解決する方法を答える。',
                 '(4)：買い物に行くことが決まったので，準備の役割を申し出るなどして会話を締めくくる。',
                 '採点：前後と意味がつながり，文法的に正しい英文なら別の表現でもよい。各4点（内容2・語法2）。']},
    {'label': 'B', 'setting': 'A customer is talking to a clerk at Marlow Electronics.',
     'lines': [('Clerk', 'Good afternoon. Can I help you find anything?'),
               ('Customer', None),
               ('Clerk', 'Certainly. Do you have the receipt with you?'),
               ('Customer', None),
               ('Clerk', 'Thank you. Would you like a new one or your money back?'),
               ('Customer', None),
               ('Clerk', 'I am afraid that model is sold out at the moment. We will have more next Tuesday.'),
               ('Customer', None)],
     'answers': ['Yes. I bought these headphones last week, but the left side does not work',
                 'Yes, here it is. I bought them on Monday',
                 'Could I exchange them for the same model, please',
                 'That is fine. Could you call me when they arrive'],
     'ja': ['店員：こんにちは。何かお探しですか。', '客：（1）', '店員：かしこまりました。レシートはお持ちですか。', '客：（2）', '店員：ありがとうございます。新しいものと交換しますか，それとも返金にしますか。', '客：（3）', '店員：あいにくその型は現在売り切れです。来週の火曜日に入荷します。', '客：（4）'],
     'explain': ['(1)：店員が Certainly. と応じ，レシートを求めているので，買った商品の不具合を伝える。',
                 '(2)：レシートを持っているかへの答え。直後の Thank you. から，渡す内容にする。',
                 '(3)：交換か返金かの選択に答える。直後に「その型は売り切れ」とあるので，同じ型への交換を希望する内容にする。',
                 '(4)：入荷を待つことを了承し，連絡を頼むなどして会話を締めくくる。',
                 '採点：前後と意味がつながり，文法的に正しい英文なら別の表現でもよい。各4点（内容2・語法2）。']},
]
