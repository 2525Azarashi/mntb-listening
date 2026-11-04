# -*- coding: utf-8 -*-
# 第3回 Ⅱ：商店街の空き店舗を「日替わり店」に（ニュース記事風。書き下ろし。町・人物・団体・数値は架空）
P2 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'One Shop, Seven Owners',
    'passage': [
        "For years, the old shopping street in the hill town of Ashwick seemed to be slowly dying. One by one, the bakery, the shoe shop "
        "and the bookshop closed, and their windows were covered with paper. By 2022, nearly a third of the shops on the street {p1} empty, "
        "and many residents had started driving to a large shopping center on the edge of town.",

        "Then a group of young residents came up with an unusual idea. Instead of waiting for one business to rent an empty shop for many "
        "years, why not let several small businesses share it, each using it for one day a week? The town council agreed to try the plan in "
        "a former hardware store, and {r2} for each day of the week.",

        "The response was far greater than anyone expected. More than eighty people applied for the seven places. In the end, the shop was "
        "shared by a coffee roaster, a retired teacher selling secondhand books, two students who repair bicycles, a woman who makes "
        "children’s clothes, a vegetable farmer, a potter and a man who bakes bread only on Sundays. Each owner pays {u3|a fraction} of the "
        "usual rent, and they share the cost of electricity and cleaning.",

        "For the owners, the biggest advantage is that they can test a business without taking a huge risk. “I always wanted to sell my "
        "pottery in a real shop,” says Mia Hartley, who uses the shop on Wednesdays. “But I could never {p4} to rent one for a whole year. "
        "With one day a week, I can find out whether people actually want to buy my work.” Two of the original seven have already moved into "
        "shops of their own on the same street.",

        "The street itself has changed, too. Because the shop sells something different every day, people visit more often to see what is "
        "on offer. Other shops nearby report that they have more customers on weekdays than before. “People come for the bread on Sunday "
        "and notice that the café next door has reopened,” says Hartley. “{u5|It works like a chain.}”",

        "Not every problem has been solved. Some older residents complain that it is confusing to have a different shop every day, and the "
        "owners sometimes argue about how to arrange the shelves. A few of the businesses have also struggled to earn enough money from a "
        "single day of sales. The council is now considering a website that shows which business is open on {p6} day.",

        "Still, the experiment has attracted attention from other towns facing the same problem. Visitors from as far away as the coast have "
        "come to Ashwick to see how it works. For the residents who started it, the lesson is simple. “An empty shop is not a sign that "
        "nobody wants to do business,” says one of them. “Sometimes it only means that the door was too big for one person to open alone.”",
    ],
    'notes': [('hardware store', '金物店'), ('roaster', '（コーヒー豆の）焙煎業者'), ('potter', '陶芸家'), ('pottery', '陶器')],
    'questions': [
        {'label': '問1', 'type': 'mc', 'ref': 1, 'points': 3, 'kind': '空所補充（主語と動詞の一致）',
         'stem': '空所(1)にあてはまる語句としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['was', 'were', 'has been', 'being'], 'answer': 'ロ',
         'expl': '主語は nearly a third of the shops。「分数 ＋ of ＋名詞」は of の後ろの名詞に動詞の数を合わせるので，複数の shops に合わせて were。being では文の動詞にならない。'},
        {'label': '問2', 'type': 'order', 'ref': 2, 'points': 4, 'kind': '語の並べかえ', 'seed': 3202,
         'words': ['invited', 'local', 'people', 'to', 'apply'],
         'ja': '地元の人々に応募するよう呼びかけた',
         'stem': '下線部(2)が「地元の人々に応募するよう呼びかけた」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'invite O to do「Oに〜するよう呼びかける・勧める」。agreed と並ぶ過去形の動詞 invited で始め，apply for …「…に応募する」へつなぐ。'},
        {'label': '問3', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(3)の意味にもっとも近いものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['twice the amount', 'a small part', 'the whole amount', 'a little more'], 'answer': 'ロ',
         'expl': 'a fraction of …「…のほんの一部」。週に1日しか使わないので，ふつうの家賃のほんの一部だけを払う。'},
        {'label': '問4', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '空所補充',
         'stem': '空所(4)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['hesitate', 'pretend', 'afford', 'deserve'], 'answer': 'ハ',
         'expl': 'can afford to do「〜する（金銭的な）余裕がある」。1年間ずっと店を借りるお金の余裕はなかったが，週1日なら試せる，という流れ。'},
        {'label': '問5', 'type': 'mc', 'ref': 5, 'points': 4, 'kind': '下線部の内容',
         'stem': '下線部(5)の内容としてもっとも適切なものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['同じ店主が，通りのいくつもの店を次々に経営するようになるということ。',
                     'ある店に来た客が近くの別の店にも気づき，通り全体に客が広がっていくということ。',
                     '日替わりの店主たちが，鎖のように一列に並んで商品を売るということ。',
                     '大きなショッピングセンターの系列店が，通りに次々と出店するということ。'], 'answer': 'ロ',
         'expl': '直前の「日曜日にパンを買いに来た人が，隣のカフェが再開したことに気づく」が具体例。一つの店への来店が次の店へとつながる様子を chain（連鎖）にたとえている。'},
        {'label': '問6', 'type': 'mc', 'ref': 6, 'points': 3, 'kind': '空所補充',
         'stem': '空所(6)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['both', 'either', 'each', 'few'], 'answer': 'ハ',
         'expl': 'on each day「それぞれの日に」。曜日ごとにどの店が開いているかを示すサイト。both / either は2つのものについて使い，few day は文法的に誤り。'},
        {'label': '問7', 'type': 'word', 'points': 4, 'kind': '抜き出し', 'answer': 'risk', 'from_para': 3, 'n_words': 1,
         'stem': '店主たちにとっての最大の利点は，大きな「危険」を冒さずに商売を試せることである。この「危険」にあたる1語を第4段落から抜き出して書きなさい。',
         'expl': '第4段落の最初の文 they can test a business without taking a huge risk。take a risk「危険を冒す」。'},
        {'label': '問8', 'type': 'tf', 'points': 9, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('2022年までに，通りの店のほぼ3分の1が空き店舗になっていた。', True),
             ('7つの枠に応募したのは80人に満たなかった。', False),
             ('最初の7人のうち2人は，すでに同じ通りで自分の店を持っている。', True),
             ('近くのほかの店は，平日の客が以前より減ったと言っている。', False),
             ('町議会は，どの店がどの日に開いているかがわかるウェブサイトを検討している。', True),
         ],
         'expl': '(ア) 第1段落。(イ) 第3段落：80人を超える人が応募した。(ウ) 第4段落の最後の文。(エ) 第5段落：平日の客が以前より増えた。(オ) 第6段落の最後の文。'},
    ],
}
