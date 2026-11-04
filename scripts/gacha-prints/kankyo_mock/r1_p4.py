# -*- coding: utf-8 -*-
# 第1回 Part 4：短い記事（書き下ろし。町・数値は架空）を読んで 80〜100 語で意見
P4 = {
    'points': 24,
    'lead': '次の記事を読んで，後の問いに英語で答えなさい（80〜100 語）。最後に使った語数を書くこと。',
    'title': 'A Week Without Cars',
    'article': [
        "Every September, the town of Larkfield closes its main streets to cars for one whole week. During this week, people walk, cycle "
        "or take free buses to work and school. Shops put tables on the empty roads, and children draw pictures on the ground with chalk. "
        "The town says that air pollution falls by about 30 percent during the week, and many residents enjoy the quiet streets. However, "
        "some delivery companies and older people who find walking difficult say the week causes them real problems. A few shop owners "
        "also report fewer customers from nearby villages. The town is now "
        "discussing whether the car-free week should become a car-free month.",
    ],
    'article_ja': [
        '毎年9月，ラークフィールドの町は中心部の道路を丸1週間車の通行止めにする。この週の間，人々は歩くか，自転車に乗るか，無料のバスを使って職場や学校へ行く。店は空いた道路にテーブルを出し，子どもたちはチョークで地面に絵を描く。町によれば，この週の間は大気汚染が約30％減り，多くの住民が静かな通りを楽しんでいる。しかし，配送業者や歩くのが難しい高齢者の中には，この週が実際に困りごとを生んでいると言う人もいる。近くの村から来る客が減ったと言う店主も何人かいる。町は今，車のない週を車のない月にするかどうかを話し合っている。',
    ],
    'question': 'Do you think the town should make the car-free week a car-free month? Why or why not?',
    'question_ja': 'あなたは，町が車のない週を車のない月にすべきだと思いますか。そう思う，または思わない理由は何ですか。',
    'model': "No, I do not think the town should make the car-free week a car-free month. It is true that cleaner air and quiet streets "
             "are good for everyone. However, one month is too long for people who depend on cars. Older people who cannot walk far may "
             "be unable to go shopping or visit a hospital, and delivery companies may lose a lot of money. Instead, the town could keep "
             "the car-free week and close one street every Sunday. In this way, it can reduce pollution without causing serious problems.",
    'model_ja': [
        'いいえ，私は町が車のない週を車のない月にすべきだとは思わない。きれいな空気と静かな通りが誰にとってもよいのは確かだ。しかし，車に頼っている人にとって1か月は長すぎる。遠くまで歩けない高齢者は買い物や病院に行けなくなるかもしれないし，配送業者は大きな損失を出すかもしれない。そのかわりに，町は車のない週を続けながら，毎週日曜日に1本の通りを閉鎖することもできる。そうすれば，深刻な問題を起こさずに汚染を減らすことができる。',
    ],
    'tips': [
        '最初の文で Yes / No をはっきり示し，問いの表現（make the car-free week a car-free month）を使って立場を書く。',
        '記事に書かれた良い点（汚染が30％減る）と困りごと（配送業者・高齢者）の両方にふれると，記事を読んだうえでの意見になる。',
        '反対の立場なら「かわりにどうするか（Instead, …）」を一つ示すと，説得力が増す。賛成の立場なら，困る人への対策（バスを増やす など）を書くとよい。',
        '80〜100語は短いので，理由は1〜2つにしぼる。記事の文をそのまま写さず，自分の言葉で言いかえる。',
    ],
    'criteria': [
        ('問いに答えている：賛成か反対かがはっきり書かれている', 5),
        ('記事の内容をふまえた理由・具体例がある', 7),
        ('構成：立場→理由→まとめの流れがある', 4),
        ('英語の正確さ：文法・語法・つづりの誤りが少ない', 6),
        ('語数：80〜100語の範囲', 2),
    ],
}
