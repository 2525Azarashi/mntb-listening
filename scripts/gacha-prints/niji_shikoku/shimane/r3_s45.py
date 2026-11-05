# 島根大学 前期 英語 予想問題 第3回 4（医学科以外の学部用）／5（医学科用）— すべて書き下ろし
S4 = {
    'no': '4', 'title': 'グラフを読んで英作文（医学科以外の学部用）', 'pts': 50,
    'lead': '下の英文の指示を読み、英語で書け。書いた語の数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'Where Young People Want to Live in the Future', 'x': ['Big city', 'Medium town', 'Countryside', 'Abroad'],
              'series': [('2016', [52, 27, 9, 12]), ('2026', [38, 31, 19, 12])], 'ymax': 60, 'ystep': 10, 'ylabel': '% of answers',
              'source': '（架空の調査。本書のために作成）'},
    'prompt': 'The graph above shows the results of an imaginary survey that asked Japanese people aged 18 to 25 where they would like to live in the future. Write about 70 words in English: explain the main trend you see, and suggest one or two causes for it.',
    'qs': [{'n': '', 'q': '', 'sheet': 'words9'}],
    'ans': [
        {'n': '解答例', 'pts': 50, 'min_words': 62, 'max_words': 82, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（変化の説明＋原因）',
         'model': "The graph shows that fewer young people now want to live in a big city, while the share who prefer the countryside has doubled from nine to nineteen percent. One reason may be that many jobs can now be done online, so people do not have to live near their office. Also, housing in big cities is expensive, and some young people want a quieter life with more space and nature.",
         'exp': '【構成】①最も大きい変化（大都市の減少と、地方・田舎の増加。数字を一つ二つ）→ ②原因（在宅・オンラインで働ける仕事の増加、都市の住居費、自然の多い暮らしへの関心 など）。「海外」は変化がないので、ふれなくてもよい。\n【採点の観点】グラフの読み取りの正確さ 20点、原因の説得力 15点、文法・語彙 15点。'},
    ],
    'tr': ['【解答例の訳】グラフは、いまは大都市に住みたい若者が減り、田舎を好む人の割合が9パーセントから19パーセントに倍増したことを示している。一つの理由は、今では多くの仕事がオンラインでできるので、会社の近くに住む必要がないことかもしれない。また、大都市の住居は高く、もっと広さと自然のある静かな暮らしを望む若者もいる。'],
}

S5 = {
    'no': '5', 'title': '和文英訳・自由英作文（医学科用）', 'pts': 60,
    'lead': '各問いに答えよ。〔医学科用〕\nA．下の文章の下線部 (1)・(2) を英文にせよ。',
    'ja_paras': [
        '病院で働く人の多くは、一日の大半を立ったまま過ごし、夜勤もある。{u:(1):患者の健康を守る仕事をしている人が、自分の健康を後回しにしてしまうのは、皮肉なことである。}',
        '医療従事者が疲れ切ってしまえば、ミスが起こりやすくなり、結局は患者にも影響が及ぶ。{u:(2):働く人が休みを取りやすい職場をつくることは、ぜいたくではなく、安全な医療を続けるための条件だと考えるべきだろう。}',
    ],
    'qlead': 'B．下の英文の指示に従い、80語前後の英語で書け。書いた語数を解答用紙の（　）に記すこと（符号は数えない）。\nIn some countries, patients can talk with a doctor through a video call instead of visiting a clinic. Should Japan make this kind of online medical care more common? State your position and support it with concrete reasons.',
    'qs': [{'n': 'A (1)', 'q': '', 'sheet': 4}, {'n': 'A (2)', 'q': '', 'sheet': 4}, {'n': 'B', 'q': '', 'sheet': 'words10'}],
    'ans': [
        {'n': 'A (1)', 'pts': 15, 'ans': 'It is ironic that people whose job is to protect the health of patients tend to put their own health last.',
         'exp': '「皮肉なことである」It is ironic that ～。「患者の健康を守る仕事をしている人」people whose job is to protect patients’ health / those who work to protect patients’ health。「自分の健康を後回しにする」put their own health last / neglect their own health / think about their own health later。構文 5点、関係詞 5点、語の選択 5点。'},
        {'n': 'A (2)', 'pts': 15, 'ans': 'We should regard creating workplaces where staff can easily take time off not as a luxury but as a condition for continuing to provide safe medical care.',
         'exp': '「〜を…と考える」regard A as B / think of A as B。「ぜいたくではなく〜」not as a luxury but as ～（not A but B）。「休みを取りやすい職場」workplaces where staff can easily take time off / take a rest。「安全な医療を続ける」continue to provide safe medical care。別解：Making it easy for workers to take a break should be seen as a condition for safe medical care, not a luxury. 構文 6点、語の選択 5点、文法 4点。'},
        {'n': 'B', 'pts': 30, 'min_words': 72, 'max_words': 92, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋具体的な理由2つ＋結論）',
         'model': "I believe Japan should make online medical care more common. First, many elderly people in rural areas live far from hospitals and cannot drive. Video calls would let them see a doctor without a long and tiring trip. Second, patients with infectious diseases could stay at home, which would protect other people in waiting rooms. Of course, doctors cannot examine the body through a screen, so online care should be used together with regular visits, not instead of them.",
         'exp': '【構成】①立場 → ②理由を二つ（First / Second）→ ③限界・条件を一言。賛成なら「地方の高齢者の通院の負担・感染症の拡大防止・仕事を休まずに受診できる」、反対なら「体に触れる診察ができず見落としが起こる・高齢者が機器を使いこなせない・個人情報の管理」など、医療の場面に結びつけて書く。\n【採点の観点】立場と理由の明確さ 10点、具体性 10点、文法・語彙 10点。'},
    ],
    'tr': ['【B 解答例の訳】日本はオンライン診療をもっと一般的にすべきだと私は考える。第一に、地方の多くの高齢者は病院から遠くに住み、車を運転できない。ビデオ通話があれば、長く疲れる移動なしに医師に診てもらえる。第二に、感染症の患者が家にいられるので、待合室にいるほかの人を守ることになる。もちろん画面越しでは医師は体を診察できないので、オンライン診療は通常の受診の代わりではなく、それと組み合わせて使うべきだ。'],
}
