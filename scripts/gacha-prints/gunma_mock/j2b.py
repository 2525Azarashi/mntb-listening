# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第2回 大問3（書き下ろし）
P3 = {
    'points': 100,
    'scene': '大学の休み時間に，ＡさんとＢさんが来月の交流会について話している。',
    'lines': [
        ('Ａ', '来月の留学生との交流会で，地元の名物を紹介する係になったんだけど，何を話せばいいか迷っているんだ。'),
        ('Ｂ', '焼きまんじゅうはどう？　実際に食べてもらえば，説明を聞くだけよりずっと印象に残るはずだよ。'),
        ('Ａ', 'いい考えだね。ただ，甘いみそだれが苦手な人もいるかもしれないから，ほかの候補も用意しておこう。'),
    ],
    'criteria': [('Ａの1つ目：「〜する係になった」と「何を話せばいいか迷っている」（疑問詞＋to 不定詞など）', 30),
                 ('Ｂ：提案の表現と，「説明を聞くだけより印象に残る」の比較', 35),
                 ('Ａの2つ目：「〜が苦手な人もいるかもしれない」「ほかの候補も用意しておこう」', 25),
                 ('全体の語彙・文法・つづりの正確さ', 10)],
    'models': [
        ["I've been asked to introduce some local specialties at next month's party with the international students, but I can't decide what to talk about.",
         "How about yaki-manju, grilled buns with a sweet miso sauce? If they actually taste them, they will remember them much better than if they just listen to an explanation.",
         "That's a good idea. But some people may not like the sweet miso sauce, so I'll prepare a few other choices as well."],
        ["At the event with the exchange students next month, I'm in charge of presenting a famous local food, and I have no idea what to say.",
         "Why don't you choose yaki-manju? Eating something leaves a much stronger impression than only hearing about it.",
         "I like that. Still, there might be people who don't enjoy sweet miso, so let's get some other options ready too."],
    ],
    'expl': [
        'Ａの1つ目：「〜する係になった」は I\'ve been asked to ~（〜するよう頼まれた）/ I\'m in charge of ~ing / My job is to ~ などで表せる。'
        '「何を話せばいいか迷っている」は I can\'t decide what to talk about / I have no idea what to say。what to ~「何を〜すべきか」を使うと短く書ける。'
        '「交流会」は a party / an event / a gathering with the international（exchange）students でよい。',
        'Ｂ：「〜はどう？」は How about ~? / Why don\'t you choose ~?。焼きまんじゅうはローマ字のあとに grilled buns with a sweet miso sauce と短く説明を加えると，読み手に伝わりやすい。'
        '「説明を聞くだけより〜」は比較級＋than if they just listen to ... / than only hearing about it。「印象に残る」は remember ~ better / leave a strong impression と中身をかみくだく。',
        'Ａの2つ目：「〜が苦手な人もいるかもしれない」は some people may not like ~ / there might be people who don\'t enjoy ~。'
        '「用意しておこう」は I\'ll prepare ~ / let\'s get ~ ready。「ほかの候補」は other choices / other options / some alternatives。「も」は as well / too。',
    ],
    'tips': ['「係になった」を became a staff のようにしない（staff は集合名詞）。be asked to ~ / be in charge of ~ が自然。',
             '「迷う」を lose my way としない。これは「道に迷う」の意味。「決められない」can\'t decide / not sure と表す。',
             '名物の名前をローマ字だけで書くと伝わらないことがある。短い説明（grilled buns など）を同格で添えるとよい。',
             '「苦手」を weak point としない。食べ物の好みなら not like / not enjoy / not be fond of を使う。'],
}
