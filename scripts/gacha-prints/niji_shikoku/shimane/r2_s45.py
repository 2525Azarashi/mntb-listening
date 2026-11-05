# 島根大学 前期 英語 予想問題 第2回 4（医学科以外の学部用）／5（医学科用）— すべて書き下ろし
S4 = {
    'no': '4', 'title': 'グラフを読んで英作文（医学科以外の学部用）', 'pts': 50,
    'lead': '下の英文の指示を読み、英語で書け。書いた語の数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'Average Daily Sleep of High School Students (hours)', 'x': ['Weekdays', 'Weekends'],
              'series': [('2015', [7.0, 8.3]), ('2025', [6.2, 8.6])], 'ymax': 10, 'ystep': 2, 'ylabel': 'hours',
              'source': '（架空の調査。本書のために作成）'},
    'prompt': 'The graph above shows the results of an imaginary survey about how long Japanese high school students sleep. Write about 70 words in English: explain the main trend you see, and suggest one or two causes for it.',
    'qs': [{'n': '', 'q': '', 'sheet': 'words9'}],
    'ans': [
        {'n': '解答例', 'pts': 50, 'min_words': 62, 'max_words': 82, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（変化の説明＋原因）',
         'model': "The graph shows that students now sleep less on weekdays than ten years ago, while they sleep slightly more on weekends. The gap between weekdays and weekends grew from about one hour to more than two. One possible cause is that many students use their phones in bed late at night. Because they do not get enough sleep during the week, they try to catch up by sleeping longer on Saturdays and Sundays.",
         'exp': '【構成】①変化（平日は減り、週末はやや増えた → 差が広がった）を数字で → ②原因を一つか二つ（夜のスマートフォン・部活や塾で帰りが遅い・平日の寝不足を週末に取り戻す など）。約70語なので、細かい数字を全部並べない。\n【採点の観点】グラフの読み取りの正確さ 20点、原因の説得力 15点、文法・語彙 15点。'},
    ],
    'tr': ['【解答例の訳】グラフは、生徒が平日は10年前より睡眠が短くなった一方、週末はわずかに長く寝ていることを示している。平日と週末の差は約1時間から2時間以上に広がった。考えられる原因の一つは、多くの生徒が夜遅くにベッドでスマートフォンを使うことだ。平日に十分な睡眠がとれないので、土曜と日曜に長く寝て取り戻そうとしているのである。'],
}

S5 = {
    'no': '5', 'title': '和文英訳・自由英作文（医学科用）', 'pts': 60,
    'lead': '各問いに答えよ。〔医学科用〕\nA．下の文章の下線部 (1)・(2) を英文にせよ。',
    'ja_paras': [
        '災害が起きると、けがの手当てだけでなく、避難所での生活そのものが人々の健康をおびやかす。{u:(1):慣れない場所で長く過ごすうちに体を動かさなくなり、持病が悪化したり、新たな病気にかかったりする人も少なくない。}',
        'そのため近年は、医師や看護師だけでなく、保健師や栄養士、薬剤師などがチームを組んで避難所を回る取り組みが進んでいる。{u:(2):目に見えるけがを治すことと同じくらい、一人一人の暮らしの変化に気づき、早めに手を打つことが必要とされているのである。}',
    ],
    'qlead': 'B．下の英文の指示に従い、80語前後の英語で書け。書いた語数を解答用紙の（　）に記すこと（符号は数えない）。\nSome people say that hospitals should let patients read all of their own medical records online at any time. Would you support such a plan? Support your view with concrete reasons.',
    'qs': [{'n': 'A (1)', 'q': '', 'sheet': 4}, {'n': 'A (2)', 'q': '', 'sheet': 4}, {'n': 'B', 'q': '', 'sheet': 'words10'}],
    'ans': [
        {'n': 'A (1)', 'pts': 15, 'ans': 'While they spend a long time in an unfamiliar place, many people stop moving their bodies, and as a result their chronic illnesses get worse or they develop new diseases.',
         'exp': '「慣れない場所」an unfamiliar place。「長く過ごすうちに」while they spend a long time / as they stay for a long time。「体を動かさなくなる」stop moving (their bodies) / become physically inactive。「持病」chronic illness / existing condition。「〜する人も少なくない」many people … / it is not unusual for people to …。論理のつながり 5点、語の選択 5点、文法 5点。'},
        {'n': 'A (2)', 'pts': 15, 'ans': 'Noticing changes in each person’s daily life and taking action early is now needed as much as treating visible injuries.',
         'exp': '「〜と同じくらい」as much as / just as important as。「暮らしの変化に気づく」notice changes in each person’s life。「早めに手を打つ」take action early / act before problems become serious。「必要とされている」is needed / is required / people are expected to。主語（動名詞）の作り方 5点、比較 5点、文法 5点。'},
        {'n': 'B', 'pts': 30, 'min_words': 72, 'max_words': 92, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋具体的な理由2つ＋結論）',
         'model': "I would support a plan that lets patients read their own medical records online. First, patients can check the names of their medicines and the results of their tests at home, so they can understand their condition better and ask clearer questions at the next visit. Second, if they move or see a new doctor, they can share accurate information quickly. However, hospitals must protect the data carefully and explain difficult results in plain language.",
         'exp': '【構成】①立場 → ②理由を二つ（First / Second）→ ③条件や結論。賛成なら「自分の状態の理解・医師との対話・転院時の情報共有」、反対なら「専門用語や検査結果を誤解して不安になる・個人情報の流出・説明なしに重い診断を知ってしまう」など、医療の場面に結びつけて具体的に書く。\n【採点の観点】立場と理由の明確さ 10点、具体性 10点、文法・語彙 10点。'},
    ],
    'tr': ['【B 解答例の訳】患者が自分の診療記録をオンラインで読めるのはよい考えだと思う。第一に、患者は家で薬の名前や検査の結果を確かめられるので、自分の状態をよりよく理解し、次の診察でより的確な質問ができる。第二に、引っ越したり新しい医師にかかったりするとき、正確な情報をすばやく伝えられる。ただし、病院はデータを慎重に守り、難しい結果はわかりやすい言葉で説明しなければならない。'],
}
