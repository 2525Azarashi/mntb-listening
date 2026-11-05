# -*- coding: utf-8 -*-
# 第2回 Part 4：短い記事（書き下ろし。町・店・数値は架空）を読んで 80〜100 語で意見
P4 = {
    'points': 24,
    'lead': '次の記事を読んで，後の問いに英語で答えなさい（80〜100 語）。最後に使った語数を書くこと。',
    'title': 'No More Free Plastic Bags',
    'article': [
        "Since April, supermarkets in the city of Danbridge have charged ten cents for every plastic bag. The city says the number of bags "
        "used each month has dropped by about 70 percent, and volunteers find far fewer bags in the river. Many shoppers now carry their "
        "own cloth bags. However, some people complain that they often forget their bags and have to pay, and a few say that the cloth "
        "bags sold in shops are expensive and need to be used many times before they are better for the environment. Now the city is "
        "thinking about charging for paper bags and plastic cups, too.",
    ],
    'article_ja': [
        '4月から，ダンブリッジ市のスーパーマーケットはレジ袋1枚につき10セントを請求している。市によれば，毎月使われる袋の数は約70％減り，ボランティアが川で見つける袋もずっと少なくなった。今では多くの買い物客が自分の布製の袋を持ち歩いている。しかし，袋を忘れてお金を払うはめになることがよくあると不満を言う人もいるし，店で売られている布製の袋は高く，環境によくなるまでに何度も使わなければならないと言う人も少しいる。今，市は紙袋とプラスチックのカップにも料金をかけることを考えている。',
    ],
    'question': 'Do you think the city should also charge for paper bags and plastic cups? Why or why not?',
    'question_ja': 'あなたは，市が紙袋とプラスチックのカップにも料金をかけるべきだと思いますか。そう思う，または思わない理由は何ですか。',
    'model': "Yes, I think the city should also charge for paper bags and plastic cups. The article shows that a small charge can change "
             "people’s habits quickly, because plastic bag use fell by about 70 percent. If cups and paper bags also cost money, more "
             "people will bring their own bottles and bags, and there will be less rubbish in the river. To help people who forget their "
             "bags, shops could lend bags for free and ask customers to return them next time. In this way, the city can protect nature "
             "without causing much trouble.",
    'model_ja': [
        'はい，私は市が紙袋とプラスチックのカップにも料金をかけるべきだと思う。レジ袋の使用が約70％減ったことから，記事は少額の料金で人々の習慣がすぐに変わりうることを示している。カップや紙袋にもお金がかかれば，自分の水筒や袋を持ってくる人が増え，川のごみも減るだろう。袋を忘れた人のために，店は袋を無料で貸し出し，次に来るときに返してもらうこともできる。そうすれば，市は大きな不便を生まずに自然を守ることができる。',
    ],
    'tips': [
        '最初の文で Yes / No をはっきり示し，問いの表現（charge for paper bags and plastic cups）を使って立場を書く。',
        '記事の数値（約70％減った）を理由の根拠に使うと，記事を読んだうえでの意見になる。数字は自分の言葉で言いかえて使う。',
        '記事にある不満（袋を忘れる・布の袋が高い）への対策を一つ書くと，反対の立場の人も納得しやすい。反対の立場なら，その不満を理由にするとよい。',
        '80〜100語は短いので，理由は1〜2つにしぼり，記事の文をそのまま写さない。',
    ],
    'criteria': [
        ('問いに答えている：賛成か反対かがはっきり書かれている', 5),
        ('記事の内容をふまえた理由・具体例がある', 7),
        ('構成：立場→理由→まとめの流れがある', 4),
        ('英語の正確さ：文法・語法・つづりの誤りが少ない', 6),
        ('語数：80〜100語の範囲', 2),
    ],
}
