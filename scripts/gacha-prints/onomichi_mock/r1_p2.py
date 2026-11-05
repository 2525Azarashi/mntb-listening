# -*- coding: utf-8 -*-
# 第1回 Ⅱ：港町の「修理カフェ」（ニュース記事風。書き下ろし。人物・町・団体・数値は架空）
P2 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'Fixing Things, Fixing Towns',
    'passage': [
        "Every second Saturday, a former fish market in the small port town of Kelby fills with the sound of tiny screwdrivers and friendly "
        "arguments. People arrive carrying broken toasters, torn jackets and bicycles with flat tires. They are not customers in the usual sense. "
        "They have come to a repair café, where volunteers help visitors {p1} their own belongings instead of throwing them away.",

        "The café was started three years ago by Tom Achebe, a retired electrician who was tired of seeing good machines in the town’s rubbish "
        "bins. “Most of the things people throw away {r2},” he says. “A loose wire, a missing screw, a worn-out belt. People simply do not know "
        "how to do it, and new products are often cheaper than paying a professional.”",

        "The idea is simple. Visitors do not pay, but they are expected to stay and take part. A volunteer sits beside them, explains what is "
        "wrong and shows them how to fix it. “We are not a free repair shop,” says Achebe. “We want people to leave with a working kettle and a "
        "little more confidence than {u3|they} had when they arrived.”",

        "Last year, the volunteers looked at more than 1,400 items. About two-thirds of them were repaired successfully, and the café estimates "
        "that this kept almost four tons of waste out of the local landfill. Some items could not be saved. Many modern devices are glued "
        "together, or their makers do not sell spare parts. Achebe hopes that this will change. “If a phone can only be opened with a special "
        "tool that nobody can buy,” he says, “it has been designed to be {p4}.”",

        "For many visitors, however, the environmental benefits are not the main attraction. Sara Lindqvist, a nurse who first came with a "
        "broken lamp, now returns every month, even when she has nothing to fix. “I moved here two years ago and didn’t know anyone,” she "
        "explains. “Here I talk with retired engineers, students and young parents. We would never meet otherwise.” The café has become one of "
        "the few places in town where people of {p5} ages spend an afternoon together.",

        "Researchers have begun to take an interest in projects like this. A survey of repair cafés in four countries found that most volunteers "
        "were over sixty, while visitors were often in their twenties and thirties. The skills are passing from one generation to the next, "
        "not in a classroom but over a broken radio. Several local schools now send students to Kelby to help on Saturdays.",

        "Achebe admits that the café cannot solve the problem of waste {u6|on its own}. Factories still make products that are hard to repair, "
        "and shops still encourage people to buy new things. But he believes that small changes in habit matter. “Once you have fixed "
        "something with your own hands,” he says, “you look at it differently. You are less likely to throw the next thing away.”",
    ],
    'notes': [('screwdriver', 'ねじ回し'), ('electrician', '電気技師'), ('landfill', 'ごみの埋め立て地'), ('spare part', '交換部品')],
    'questions': [
        {'label': '問1', 'type': 'mc', 'ref': 1, 'points': 3, 'kind': '空所補充（句動詞）',
         'stem': '空所(1)に入れて「〜を修理する」という意味にしたい。もっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['fix up', 'give up', 'put off', 'turn down'], 'answer': 'イ',
         'expl': 'fix up「修理する・直す」。give up「あきらめる」，put off「延期する」，turn down「断る」。直後の instead of throwing them away とも対になる。'},
        {'label': '問2', 'type': 'order', 'ref': 2, 'points': 4, 'kind': '語の並べかえ', 'seed': 1202,
         'words': ['could', 'be', 'repaired', 'in', 'less', 'than', 'ten', 'minutes'],
         'ja': '10分もかからずに修理できるだろう',
         'stem': '下線部(2)が前後の内容と自然につながる英語になるよう，（　）内の語を正しい順に置きかえ，記号を左から順に書きなさい。',
         'expl': '主語 Most of the things people throw away に続く述語。助動詞 could ＋受動態 be repaired。「10分もかからずに」は in less than ten minutes。後ろに続く「ゆるんだ配線，なくなったねじ」が簡単な修理の例になっている。'},
        {'label': '問3', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '指示語',
         'stem': '下線部(3)の they が指すものとしてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['the volunteers', 'the people who come to the café', 'professional repair shops', 'working kettles'], 'answer': 'ロ',
         'expl': '「来たときよりも少し多くの自信を持って帰ってほしい」の主語は people（カフェに来た人）。want people to leave … than they had when they arrived の they も同じ people。'},
        {'label': '問4', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '空所補充',
         'stem': '空所(4)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['repaired', 'shared', 'replaced', 'recycled'], 'answer': 'ハ',
         'expl': '誰も買えない特別な道具がないと開けられない電話は，直すのではなく「買い替えられる」ように作られている，という皮肉。'},
        {'label': '問5', 'type': 'mc', 'ref': 5, 'points': 3, 'kind': '空所補充',
         'stem': '空所(5)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['similar', 'different', 'early', 'equal'], 'answer': 'ロ',
         'expl': '直前で「退職した技術者・学生・若い親」と幅広い人の名前が挙がっているので「さまざまな年齢の」。'},
        {'label': '問6', 'type': 'word', 'ref': 6, 'points': 4, 'kind': '抜き出し', 'answer': 'by itself', 'from_para': None,
         'stem': '下線部(6)とほぼ同じ意味を表す2語の語句を書きなさい。（itself を使うこと）',
         'expl': 'on its own「それだけで・単独で」＝ by itself。カフェだけでごみの問題は解決できない，という意味。'},
        {'label': '問7', 'type': 'mc', 'points': 5, 'kind': '内容の理解',
         'stem': '修理カフェのしくみとしてもっとも適切でないものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['来た人は料金を払わない。', 'ボランティアが故障の原因を説明し，直し方を見せる。',
                     '来た人は品物を預けて，修理が終わったころに取りに来る。', '昨年は持ちこまれた品物の約3分の2が直った。'], 'answer': 'ハ',
         'expl': '第3段落「その場に残って参加することが求められる」「無料の修理店ではない」に反する。(イ)(ロ)は第3段落，(ニ)は第4段落。'},
        {'label': '問8', 'type': 'tf', 'points': 8, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('アチェベは，まだ使える機械がごみ箱に捨てられるのを見るのにうんざりしてカフェを始めた。', True),
             ('アチェベは，現代の機器の多くが簡単に開けられるように作られていると述べている。', False),
             ('リンドクヴィストは，直すものがないときでもカフェに通っている。', True),
             ('ある調査では，ボランティアも訪問者もほとんどが60歳を超えていた。', False),
             ('地元のいくつかの学校は，土曜日に生徒をカフェへ手伝いに行かせている。', True),
         ],
         'expl': '(ア) 第2段落。(イ) 第4段落：多くは接着されていて部品も売られていない。(ウ) 第5段落 even when she has nothing to fix。(エ) 第6段落：訪問者は20〜30代が多い。(オ) 第6段落の最後の文。'},
    ],
    'translation': [
        '毎月第2土曜日になると，小さな港町ケルビーの元魚市場は，小さなねじ回しの音と和やかな言い合いの声でいっぱいになる。人々は壊れたトースターや破れた上着，パンクした自転車を抱えてやって来る。ふつうの意味でのお客ではない。彼らが来たのは修理カフェで，ここではボランティアが，訪れた人が自分の持ち物を捨てずに修理するのを手伝うのだ。',
        'このカフェは3年前，町のごみ箱にまだ使える機械が捨てられているのを見るのにうんざりしていた退職した電気技師，トム・アチェベが始めた。「人が捨てるものの大半は，10分もかからずに直せるでしょう」と彼は言う。「ゆるんだ配線，なくなったねじ，すり切れたベルト。みんなは直し方を知らないだけですし，専門家にお金を払うより新品のほうが安いことも多いのです」。',
        '考え方は単純だ。来た人はお金を払わないが，その場に残って参加することが求められる。ボランティアが隣に座り，どこが悪いのかを説明し，直し方を見せる。「ここは無料の修理店ではありません」とアチェベは言う。「動くやかんと，来たときより少し多くの自信を持って帰ってほしいのです」。',
        '昨年，ボランティアは1,400を超える品物を見た。そのうち約3分の2はうまく直り，カフェの見積もりでは，これによって4トン近いごみが地元の埋め立て地に行かずにすんだ。救えなかった品物もある。現代の機器の多くは接着されていたり，メーカーが交換部品を売っていなかったりするのだ。アチェベはこれが変わることを願っている。「誰も買えない特別な道具でしか開けられない電話があるとしたら，それは買い替えられるように設計されているのです」。',
        'しかし，多くの訪問者にとって，環境へのよい影響はいちばんの魅力ではない。壊れた電気スタンドを持って初めて来た看護師のサラ・リンドクヴィストは，今では直すものがないときでも毎月やって来る。「2年前にここに越してきて，知り合いが一人もいなかったんです。ここでは退職した技術者や学生，若い親と話をします。ほかの場所では決して会うことのない人たちです」。このカフェは，町の中で，さまざまな年齢の人が午後をいっしょに過ごす数少ない場所の一つになった。',
        '研究者もこうした取り組みに関心を持ち始めている。4か国の修理カフェを調べたある調査では，ボランティアのほとんどが60歳を超えていた一方，訪問者は20代や30代が多かった。技術は教室ではなく壊れたラジオを囲んで，ある世代から次の世代へと受けつがれているのだ。今では地元のいくつかの学校が，土曜日に生徒をケルビーへ手伝いに行かせている。',
        'カフェだけでごみの問題を解決することはできない，とアチェベは認める。工場は今も修理しにくい製品を作り，店は今も新しいものを買うよう人々をうながしている。しかし彼は，習慣の小さな変化が大切だと信じている。「一度自分の手で何かを直すと，それを見る目が変わります。次のものを捨てることが少なくなるのです」。',
    ],
    'vocab': [('former', '元の'), ('belongings', '持ち物'), ('retired', '退職した'), ('worn-out', 'すり切れた'), ('confidence', '自信'),
              ('estimate', '見積もる'), ('glue', '接着する'), ('attraction', '魅力'), ('otherwise', 'そうでなければ'),
              ('generation', '世代'), ('admit', '認める'), ('encourage O to do', 'Oに〜するようすすめる')],
}
