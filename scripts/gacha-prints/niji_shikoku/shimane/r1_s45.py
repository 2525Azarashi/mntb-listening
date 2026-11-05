# 島根大学 前期 英語 予想問題 第1回 4（法文・人間科学・総合理工・生物資源科学部用）／5（医学部医学科用）— すべて書き下ろし
S4 = {
    'no': '4', 'title': 'グラフを読んで英作文（医学科以外の学部用）', 'pts': 50,
    'lead': '下の英文の指示を読み、英語で書け。書いた語の数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'How High School Students Mainly Study at Home', 'x': ['Paper textbooks', 'Videos online', 'Study apps', 'AI chat tools'],
              'series': [('2020', [58, 22, 15, 1]), ('2025', [35, 30, 21, 12])], 'ymax': 60, 'ystep': 10, 'ylabel': '% of students',
              'source': '（架空の調査。本書のために作成）'},
    'prompt': 'The graph above shows the results of an imaginary survey that asked Japanese high school students how they mainly study at home. Write about 70 words in English: explain the main trend you see, and suggest one or two causes for it.',
    'qs': [{'n': '', 'q': '', 'sheet': 'words9'}],
    'ans': [
        {'n': '解答例', 'pts': 50, 'min_words': 62, 'max_words': 82, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（気づいたこと＋理由）',
         'model': "The graph shows that fewer students mainly study with paper textbooks now, while more of them use online videos, study apps and AI chat tools. The use of AI tools grew from almost zero to twelve percent. I think the main reason is that most students now have their own smartphones. They can watch a short lesson or ask a question at any time, so digital tools feel quicker and more convenient than books.",
         'exp': '【構成】①気づいたこと（紙の教科書の減少と、デジタルの学び方の増加。数字を一つ二つ入れる）→ ②理由（スマートフォンの普及・いつでも使える便利さ など）。約70語なので、変化を全部並べず「最も大きい変化」に絞る。\n【採点の観点】グラフの読み取りの正確さ 20点、理由の説得力 15点、文法・語彙 15点。語数が大きく外れる（50語未満・90語超）ものは減点。'},
    ],
    'tr': ['【解答例の訳】グラフは、いまは主に紙の教科書で勉強する生徒が減り、一方でオンラインの動画や学習アプリ、AIのチャットツールを使う生徒が増えていることを示している。AIツールの利用はほぼゼロから12パーセントに増えた。主な理由は、いまではほとんどの生徒が自分のスマートフォンを持っていることだと思う。いつでも短い授業を見たり質問したりできるので、デジタルの道具のほうが本より速く便利に感じられるのだ。'],
}

S5 = {
    'no': '5', 'title': '和文英訳・自由英作文（医学科用）', 'pts': 60,
    'lead': '各問いに答えよ。〔医学科用〕\nA．下の文章の下線部 (1)・(2) を英文にせよ。',
    'ja_paras': [
        '高齢化が進むにつれて、一人の患者が複数の病気を抱え、いくつもの医療機関に通うことは珍しくなくなった。{u:(1):それぞれの医師が正しく薬を出していても、全部を合わせると薬の数が多くなりすぎ、かえって体に害を与えることがある。}',
        'こうした問題を防ぐために、薬剤師が患者の飲んでいる薬をまとめて確認し、医師に減らす提案をする取り組みが各地で広がっている。{u:(2):大切なのは、患者自身が自分の飲んでいる薬について知り、気になることを遠慮せずに相談できる関係を作ることである。}',
    ],
    'qlead': 'B．下の英文の指示に従い、80語前後の英語で書け。書いた語数を解答用紙の（　）に記すこと（符号は数えない）。\nSome people say that all medical students should spend several weeks working in a rural clinic before they graduate. Do you agree or disagree? Support your view with concrete reasons.',
    'qs': [{'n': 'A (1)', 'q': '', 'sheet': 4}, {'n': 'A (2)', 'q': '', 'sheet': 4}, {'n': 'B', 'q': '', 'sheet': 'words10'}],
    'ans': [
        {'n': 'A (1)', 'pts': 15, 'ans': 'Even if each doctor prescribes medicine correctly, the total number of drugs may become too large, and this can actually harm the patient’s body.',
         'exp': '「〜していても」は Even if / Even though。「薬を出す」prescribe medicine / prescribe drugs。「全部を合わせると」は when (they are) put together / in total / the total number of drugs。「かえって」actually / instead / rather。「体に害を与える」harm the body / do harm to the patient。主節と従属節の論理 5点、語の選択 5点、文法 5点。'},
        {'n': 'A (2)', 'pts': 15, 'ans': 'What is important is to build a relationship in which patients themselves know about the medicines they take and can consult someone without hesitation about anything that worries them.',
         'exp': '「大切なのは〜である」What is important is to do / The important thing is to do。「〜できる関係」a relationship in which (where) S can do。「遠慮せずに」without hesitation / freely / without feeling shy。「気になること」anything that worries them / their concerns。関係詞の使い方 6点、語の選択 5点、文法 4点。'},
        {'n': 'B', 'pts': 30, 'min_words': 72, 'max_words': 92, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋具体的な理由2つ＋結論）',
         'model': "I agree that all medical students should work in a rural clinic for several weeks. First, many rural areas in Japan do not have enough doctors, and students can see how serious this problem is with their own eyes. This experience may encourage some of them to work there in the future. Second, doctors in small clinics must treat many kinds of illness and know each patient’s life. Students can learn that good medicine depends on understanding people, not only diseases.",
         'exp': '【構成】①立場をはっきり書く → ②理由を二つ（First / Second）、それぞれ具体的に → ③（余裕があれば）まとめ。「具体的な理由」が求められているので、地方の医師不足・幅広い病気を診る経験 など、医療の場面に結びつけて書く。反対の立場（学ぶべきことが多い時期に時間を取られる、指導できる医師が地方に少ない など）でも同じく評価する。\n【採点の観点】立場と理由の明確さ 10点、具体性 10点、文法・語彙 10点。'},
    ],
    'tr': ['【B 解答例の訳】私は、すべての医学生が数週間、地方の診療所で働くべきだという考えに賛成だ。第一に、日本の多くの地方では医師が足りず、学生はこの問題がどれほど深刻かを自分の目で見ることができる。この経験が、彼らの何人かに将来そこで働こうという気持ちを起こさせるかもしれない。第二に、小さな診療所の医師は多くの種類の病気を診なければならず、患者一人一人の生活を知っている。学生は、よい医療は病気だけでなく人を理解することにかかっていると学べるのだ。'],
}
