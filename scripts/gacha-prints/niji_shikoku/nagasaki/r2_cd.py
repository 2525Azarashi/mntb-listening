# 長崎大学 前期 英語 予想問題 第2回 C（理系選抜の学部用）／D（それ以外の学部用）— すべてマナトビ編集部の書き下ろし
M = ['A.', 'B.', 'C.', 'D.']

SC = {
    'no': 'C', 'title': '語彙・同意表現（教育〈文系以外〉・情報データ科学〈理系〉用）', 'pts': 60, 'marks': M,
    'lead': '1〜10 の英文の下線を引いた語句に意味が最も近いものを、A〜D の中から1つずつ選び、記号で答えよ。',
    'qs': [
        {'n': '1.', 'q': 'The meeting was {_:put off} until next week because the manager was sick.', 'opts': ['cancelled', 'postponed', 'shortened', 'moved forward'], 'sheet': 'box'},
        {'n': '2.', 'q': 'Scientists are trying to find a {_:reliable} way to predict earthquakes.', 'opts': ['cheap', 'quick', 'dependable', 'new'], 'sheet': 'box'},
        {'n': '3.', 'q': 'I {_:ran into} my old classmate at the station yesterday.', 'opts': ['met by chance', 'waited for', 'argued with', 'said goodbye to'], 'sheet': 'box'},
        {'n': '4.', 'q': 'The museum has a {_:vast} collection of ancient coins.', 'opts': ['small', 'valuable', 'strange', 'huge'], 'sheet': 'box'},
        {'n': '5.', 'q': 'She was {_:reluctant} to speak in front of so many people.', 'opts': ['eager', 'unwilling', 'proud', 'able'], 'sheet': 'box'},
        {'n': '6.', 'q': 'We had to {_:get rid of} a lot of old furniture when we moved.', 'opts': ['repair', 'buy', 'throw away', 'carry'], 'sheet': 'box'},
        {'n': '7.', 'q': 'The results of the two experiments were {_:identical}.', 'opts': ['exactly the same', 'quite different', 'disappointing', 'surprising'], 'sheet': 'box'},
        {'n': '8.', 'q': 'Heavy rain {_:caused} the river to flood the nearby fields.', 'opts': ['prevented', 'led', 'warned', 'allowed'], 'sheet': 'box'},
        {'n': '9.', 'q': 'The town is {_:renowned} for its hot springs and fresh seafood.', 'opts': ['criticized', 'known only', 'famous', 'responsible'], 'sheet': 'box'},
        {'n': '10.', 'q': 'Please {_:look over} this contract before you sign it.', 'opts': ['copy', 'examine', 'translate', 'ignore'], 'sheet': 'box'},
    ],
    'ans': [
        {'n': '1.', 'pts': 6, 'ans': 'B', 'exp': 'put off ＝「延期する」＝ postpone。until next week があるので cancel「中止する」ではない。'},
        {'n': '2.', 'pts': 6, 'ans': 'C', 'exp': 'reliable ＝「信頼できる」＝ dependable。'},
        {'n': '3.', 'pts': 6, 'ans': 'A', 'exp': 'run into ＝「偶然出会う」＝ meet by chance / come across / bump into。'},
        {'n': '4.', 'pts': 6, 'ans': 'D', 'exp': 'vast ＝「ばく大な・広大な」＝ huge。'},
        {'n': '5.', 'pts': 6, 'ans': 'B', 'exp': 'reluctant to do ＝「〜したがらない」＝ unwilling to do。eager「熱心な」は反対の意味。'},
        {'n': '6.', 'pts': 6, 'ans': 'C', 'exp': 'get rid of ＝「処分する・取り除く」＝ throw away / dispose of。'},
        {'n': '7.', 'pts': 6, 'ans': 'A', 'exp': 'identical ＝「まったく同じ」＝ exactly the same。'},
        {'n': '8.', 'pts': 6, 'ans': 'B', 'exp': 'cause O to do ＝「O に〜させる（〜を引き起こす）」。lead O to do も「O を〜させる（導く）」で同じ形・意味。prevent は prevent O from doing の形で反対の意味。'},
        {'n': '9.', 'pts': 6, 'ans': 'C', 'exp': 'renowned for ＝「〜で有名な」＝ famous for / well known for。'},
        {'n': '10.', 'pts': 6, 'ans': 'B', 'exp': 'look over ＝「ざっと目を通す・調べる」＝ examine / go through。'},
    ],
    'vocab': [('put off', '延期する'), ('reliable', '信頼できる'), ('run into', '偶然出会う'), ('vast', 'ばく大な'), ('reluctant', '気が進まない'),
              ('get rid of', '処分する'), ('identical', 'まったく同じ'), ('cause O to do', 'O に〜させる'), ('renowned', '有名な'), ('look over', '目を通す')],
}

SD = {
    'no': 'D', 'title': 'グラフを読んで英作文（C を解かない学部用）', 'pts': 60,
    'lead': '下のグラフについて、問い1・2 のどちらにも約100語の英語で解答せよ。書いた語数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'Foreign Visitors to an Imaginary Prefecture in Japan (thousands)', 'x': ['2015', '2017', '2019', '2021', '2023', '2025'],
              'series': [('Visitors from Asia', [420, 560, 690, 40, 510, 760]), ('Visitors from other regions', [110, 140, 170, 10, 160, 250])],
              'ymax': 800, 'ystep': 200, 'ylabel': 'thousands of visitors', 'source': '（架空の統計。本書のために作成）'},
    'qs': [
        {'n': '1.', 'q': 'Using the graph, describe how foreign visitor numbers to this prefecture have changed.', 'sheet': 'words12'},
        {'n': '2.', 'q': 'Do you think an increase in foreign tourists is good for local communities in Japan? Explain your view with two or more reasons.', 'sheet': 'words12'},
    ],
    'ans': [
        {'n': '1.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（増加→急減→回復・数字）',
         'model': "The number of foreign visitors to the prefecture rose steadily from 2015 to 2019. Visitors from Asia increased from 420,000 to 690,000, and those from other regions went up from 110,000 to 170,000. In 2021, however, both numbers fell sharply to almost nothing, probably because of travel restrictions during the pandemic. After that, the numbers recovered quickly. By 2025, visitors from Asia reached 760,000 and visitors from other regions reached 250,000. Both figures were higher than before the drop, and the number from other regions grew especially fast, rising by about fifty percent between 2023 and 2025. Throughout the period, Asian visitors made up the large majority of all foreign visitors.",
         'exp': '【構成】①2015〜2019年の増加 → ②2021年の急減 → ③その後の回復（2025年は以前より多い）→ ④アジアからの訪問者が大部分という全体の特徴。\n【採点の観点】読み取りの正確さ 12点、数字を使った具体性 8点、文法・語彙 10点。急減の理由は「おそらく」と推測の形で短く添える程度でよい。'},
        {'n': '2.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋理由2つ＋結論）',
         'model': "I think an increase in foreign tourists is mostly good for local communities, as long as it is managed well. First, tourists spend money at hotels, restaurants and small shops, which creates jobs in areas where young people are leaving. Second, visitors can help local people see the value of their own culture. When tourists show interest in a local festival or a traditional craft, residents may feel proud and work harder to protect it. Of course, too many visitors can cause crowding and noise. However, if towns plan carefully, the benefits are greater than the problems.",
         'exp': '【構成】①立場 → ②理由1（経済効果・雇用）→ ③理由2（地域文化の再評価）→ ④反対意見への一言＋結論。\n反対の立場（混雑・ごみ・家賃の上昇・住民の生活への影響 など）でも同じ基準で評価する。\n【採点の観点】立場と理由の明確さ 10点、具体性・論理のつながり 10点、文法・語彙 10点。'},
    ],
    'tr': [
        '【1 の解答例の訳】この県を訪れる外国人の数は、2015年から2019年まで着実に増えた。アジアからの訪問者は42万人から69万人に増え、ほかの地域からの訪問者は11万人から17万人に増えた。しかし2021年には、おそらく感染症の流行中の渡航制限のために、どちらの数もほとんどゼロにまで急激に落ち込んだ。その後、数は急速に回復した。2025年までに、アジアからの訪問者は76万人、ほかの地域からの訪問者は25万人に達した。どちらも落ち込む前より多く、とくにほかの地域からの訪問者は2023年から2025年のあいだに約5割増えるという速い伸びを見せた。期間を通じて、アジアからの訪問者が外国人訪問者全体の大部分を占めていた。',
        '【2 の解答例の訳】外国人観光客の増加は、うまく管理されているかぎり、地域社会にとっておおむねよいことだと思う。第一に、観光客はホテルやレストラン、小さな店でお金を使い、若い人が出て行ってしまう地域に仕事を生み出す。第二に、訪問者は地元の人々が自分たちの文化の価値に気づく手助けになりうる。観光客が地元の祭りや伝統工芸に関心を示すと、住民は誇りを感じ、それを守るためにいっそう努力するかもしれない。もちろん、訪問者が多すぎると混雑や騒音を引き起こしうる。しかし町が慎重に計画すれば、利点のほうが問題よりも大きい。',
    ],
}
