# -*- coding: utf-8 -*-
# 第2回 Ⅱ：都市の屋上でミツバチを飼う（ニュース記事風。書き下ろし。人物・都市・団体・数値は架空）
P2 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'Bees on the Roof',
    'passage': [
        "On the roof of a ten-story office building in the city of Branford, thousands of bees are busy at work. Below them, buses and taxis "
        "crawl through traffic. The hives belong to a small company called Skyline Honey, which looks after more than forty colonies on roofs "
        "across the city. “People are always surprised,” says its founder, Grace Delmont. “They imagine that bees {p1} only in the countryside.”",

        "In fact, cities can be surprisingly good places for bees. Parks, gardens, street trees and even window boxes offer a wide variety of "
        "flowers, and many cities use fewer chemicals than farms do. {p2} some of the large farms outside Branford grow only one crop, which "
        "flowers for just a few weeks a year. In the city, something is blooming from early spring until late autumn.",

        "Delmont started keeping bees as a hobby twelve years ago, with a single hive in her back garden. When neighbors began asking to buy "
        "her honey, she realized that there was a market for it. Today Skyline Honey {p3} ten people and sells honey to shops and restaurants. "
        "Each jar is labeled with the name of the roof where the honey was made, and customers often say they can taste the difference between "
        "honey from the park district and honey from the old harbor.",

        "Companies are also eager to {u4|host} hives. For an annual fee, Skyline Honey places hives on a company’s roof and takes care of "
        "them, and the company receives the honey to give to its staff and visitors. Some workers now volunteer to help with the hives during "
        "their lunch breaks. “It gets people out of their chairs,” says one office manager. “And it gives them something to talk about {p5} "
        "the weather.”",

        "Not everyone is enthusiastic, however. Some scientists warn that too many honeybees in one area may compete with wild bees for food. "
        "Wild bees, which live alone or in small groups, are often more important than honeybees for pollinating certain plants, and many "
        "species are already in decline. “Adding hives is not the same as helping nature,” says Dr. Paul Seddon, an ecologist at Branford "
        "University. “If there are not enough flowers, the newcomers simply take food from {u6|the bees that were already there}.”",

        "Delmont takes these concerns seriously. Her company now limits the number of hives in each district and asks every customer to plant "
        "flowers on the roof or nearby. Last year, Skyline Honey and its customers planted more than 3,000 plants, chosen to feed wild bees "
        "as well as honeybees. “The honey is the part people notice,” she says, “but the flowers {r7}.”",

        "Seddon agrees that projects like this can do some good, especially when they make city residents more aware of insects. Still, he "
        "hopes that people will remember the less famous bees too. “A hive on the roof is a fine start,” he says. “A city full of flowers "
        "would be even better.”",
    ],
    'notes': [('hive', '巣箱'), ('colony', '（ミツバチの）群れ'), ('bloom', '花が咲く'), ('pollinate', '受粉させる'), ('ecologist', '生態学者')],
    'questions': [
        {'label': '問1', 'type': 'mc', 'ref': 1, 'points': 3, 'kind': '空所補充',
         'stem': '空所(1)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['belong', 'happen', 'appear', 'arrive'], 'answer': 'イ',
         'expl': 'belong in …「（本来）…にいるべきだ・…がふさわしい場所だ」。ミツバチは田舎にいるものだと人は思っている，という意味。'},
        {'label': '問2', 'type': 'mc', 'ref': 2, 'points': 4, 'kind': '空所補充（つなぎの語句）',
         'stem': '空所(2)にあてはまる語句としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['By contrast,', 'As a result,', 'For this reason,', 'In addition,'], 'answer': 'イ',
         'expl': '前の文は「都市には多様な花があり化学薬品も少ない」，後ろは「農場では1種類の作物が数週間しか咲かない」。都市と農場を比べているので By contrast「対照的に」。'},
        {'label': '問3', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '空所補充',
         'stem': '空所(3)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['employs', 'borrows', 'invites', 'returns'], 'answer': 'イ',
         'expl': '会社が10人を「雇っている」。employ「雇う」。趣味から始めた養蜂が会社に成長したという流れ。'},
        {'label': '問4', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(4)の意味にもっとも近いものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['have on their property', 'sell to customers', 'destroy completely', 'study carefully'], 'answer': 'イ',
         'expl': 'host は「（催しなどを）主催する・受け入れる」。ここでは巣箱を自社の屋上に置く＝自分の敷地に置くという意味。'},
        {'label': '問5', 'type': 'mc', 'ref': 5, 'points': 3, 'kind': '空所補充（前置詞）',
         'stem': '空所(5)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['besides', 'despite', 'until', 'among'], 'answer': 'イ',
         'expl': 'besides …「…のほかに」。天気以外の話題ができる，という意味。despite「…にもかかわらず」では意味が通らない。'},
        {'label': '問6', 'type': 'word', 'ref': 6, 'points': 4, 'kind': '抜き出し', 'answer': 'wild bees', 'from_para': 4, 'n_words': 2,
         'stem': '下線部(6)が指すものを，第5段落から連続する2語で抜き出して書きなさい。',
         'expl': '新しく来たミツバチ（the newcomers）が食べ物を奪う相手は，もとからいた野生のハチ。第5段落の wild bees。'},
        {'label': '問7', 'type': 'order', 'ref': 7, 'points': 4, 'kind': '語の並べかえ', 'seed': 2207,
         'words': ['are', 'what', 'really', 'make', 'a', 'difference'],
         'ja': '本当に違いを生むものだ',
         'stem': '下線部(7)が「本当に違いを生むものだ」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'the flowers are what …「花こそが…なものだ」。関係代名詞 what が先行詞を含み，what really make a difference「本当に違いを生むもの」。make a difference「違いを生む・効果がある」。'},
        {'label': '問8', 'type': 'tf', 'points': 9, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('ブランフォードの外の大規模農場の中には，1年に数週間しか花の咲かない作物だけを育てているところがある。', True),
             ('デルモントは，最初から会社としてハチミツを売るつもりで養蜂を始めた。', False),
             ('ハチミツのびんには，それがつくられた屋上の名前が書かれている。', True),
             ('セドン博士は，巣箱を増やせばそれだけ自然を守ることになると考えている。', False),
             ('スカイライン・ハニーは，客に屋上やその近くに花を植えるよう頼んでいる。', True),
         ],
         'expl': '(ア) 第2段落。(イ) 第3段落：趣味として始めた。(ウ) 第3段落 Each jar is labeled…。(エ) 第5段落 Adding hives is not the same as helping nature。(オ) 第6段落。'},
    ],
    'translation': [
        'ブランフォード市にある10階建てのオフィスビルの屋上で，何千匹ものミツバチが忙しく働いている。その下ではバスやタクシーが渋滞の中をのろのろと進んでいる。巣箱はスカイライン・ハニーという小さな会社のもので，この会社は市内の屋上で40を超える群れの世話をしている。「みんないつも驚きます」と創業者のグレース・デルモントは言う。「ミツバチがいるのは田舎だけだと思っているのです」。',
        '実は，都市はミツバチにとって意外なほどよい場所になりうる。公園や庭，街路樹，窓辺の植木箱にまでさまざまな花があり，多くの都市では農場ほど化学薬品を使わない。それとは対照的に，ブランフォードの外にある大規模農場の中には，1年に数週間しか花の咲かない作物を1種類だけ育てているところもある。都市では，早春から晩秋まで何かしらの花が咲いている。',
        'デルモントは12年前，裏庭に巣箱を1つ置いて，趣味として養蜂を始めた。近所の人がハチミツを買いたいと言い出したとき，彼女はそれに需要があることに気づいた。今ではスカイライン・ハニーは10人を雇い，店やレストランにハチミツを売っている。どのびんにもハチミツがつくられた屋上の名前が書かれており，公園地区のハチミツと古い港のハチミツの味の違いがわかると言う客も多い。',
        '企業も巣箱を置くことに熱心だ。年間料金を払うと，スカイライン・ハニーが会社の屋上に巣箱を置いて世話をし，会社はハチミツを受け取って社員や来客に配る。今では昼休みに巣箱の手伝いを買って出る社員もいる。「みんなをいすから立ち上がらせてくれます」とあるオフィスの管理者は言う。「それに，天気のほかに話す話題もできますしね」。',
        'しかし，誰もが乗り気なわけではない。一つの地域にミツバチが多すぎると，野生のハチと食べ物を奪い合うかもしれないと警告する科学者もいる。単独か小さな集団で暮らす野生のハチは，ある種の植物を受粉させるうえでミツバチより重要なことが多く，多くの種がすでに減少している。「巣箱を増やすことは自然を助けることと同じではありません」とブランフォード大学の生態学者ポール・セドン博士は言う。「花が十分になければ，新しく来たハチはもとからいたハチから食べ物を奪うだけです」。',
        'デルモントはこうした懸念を真剣に受けとめている。彼女の会社は今では地区ごとの巣箱の数を制限し，すべての客に屋上かその近くに花を植えるよう頼んでいる。昨年，スカイライン・ハニーとその客は，ミツバチだけでなく野生のハチの食べ物にもなるよう選んだ植物を3,000株以上植えた。「人が気づくのはハチミツのほうですが，本当に違いを生むのは花なのです」と彼女は言う。',
        'セドンも，こうした取り組みは，とくに都市の住民が昆虫を意識するきっかけになるなら，いくらかよい効果があると認めている。それでも彼は，人々があまり有名でないハチのことも覚えていてほしいと願っている。「屋上の巣箱はよい出発点です。でも，花でいっぱいの都市ならもっとよいでしょう」。',
    ],
    'vocab': [('crawl', 'のろのろ進む'), ('founder', '創業者'), ('variety', '多様さ'), ('crop', '作物'), ('realize', '気づく'),
              ('label', 'ラベルをはる'), ('eager to do', 'しきりに〜したがる'), ('annual fee', '年間料金'), ('enthusiastic', '熱心な'),
              ('compete with', '〜と競争する'), ('in decline', '減少して'), ('concern', '懸念')],
}
