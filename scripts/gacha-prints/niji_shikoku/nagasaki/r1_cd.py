# 長崎大学 前期 英語 予想問題 第1回 C（理系選抜の学部用）／D（それ以外の学部用）— すべてマナトビ編集部の書き下ろし
M = ['A.', 'B.', 'C.', 'D.']

SC = {
    'no': 'C', 'title': '語彙・同意表現（教育〈文系以外〉・情報データ科学〈理系〉用）', 'pts': 60, 'marks': M,
    'lead': '1〜10 の英文の下線を引いた語句に意味が最も近いものを、A〜D の中から1つずつ選び、記号で答えよ。',
    'qs': [
        {'n': '1.', 'q': 'Please make sure you {_:turn in} your report by Friday afternoon.', 'opts': ['submit', 'return', 'copy', 'correct'], 'sheet': 'box'},
        {'n': '2.', 'q': 'The new traffic rule had a {_:significant} effect on the number of accidents.', 'opts': ['slight', 'considerable', 'temporary', 'strange'], 'sheet': 'box'},
        {'n': '3.', 'q': 'My sister {_:came up with} a clever way to reuse the water from the bath.', 'opts': ['rejected', 'remembered', 'thought of', 'heard about'], 'sheet': 'box'},
        {'n': '4.', 'q': 'The village is so {_:remote} that the bus comes only twice a day.', 'opts': ['distant', 'crowded', 'modern', 'famous'], 'sheet': 'box'},
        {'n': '5.', 'q': 'He smiled politely and tried to {_:conceal} his disappointment.', 'opts': ['hide', 'show', 'explain', 'forget'], 'sheet': 'box'},
        {'n': '6.', 'q': 'The engineers still need to {_:figure out} why the machine stopped suddenly.', 'opts': ['ignore', 'understand', 'repair', 'report'], 'sheet': 'box'},
        {'n': '7.', 'q': 'The weather was surprisingly {_:mild} for the middle of January.', 'opts': ['severe', 'dry', 'unusual', 'gentle'], 'sheet': 'box'},
        {'n': '8.', 'q': 'After ten years of success, the bakery decided to {_:expand} its business to the next town.', 'opts': ['reduce', 'move', 'enlarge', 'sell'], 'sheet': 'box'},
        {'n': '9.', 'q': 'Maps of the hiking trails are {_:available} at the front desk of the visitor center.', 'opts': ['sold out', 'obtainable', 'checked', 'displayed'], 'sheet': 'box'},
        {'n': '10.', 'q': 'My teacher {_:pointed out} several spelling mistakes in my essay.', 'opts': ['made', 'corrected', 'overlooked', 'indicated'], 'sheet': 'box'},
    ],
    'ans': [
        {'n': '1.', 'pts': 6, 'ans': 'A', 'exp': 'turn in ＝「提出する」＝ submit。hand in も同じ意味。'},
        {'n': '2.', 'pts': 6, 'ans': 'B', 'exp': 'significant ＝「（効果・量などが）かなりの・重要な」＝ considerable。slight「わずかな」は反対の意味。'},
        {'n': '3.', 'pts': 6, 'ans': 'C', 'exp': 'come up with ＝「（考え・案）を思いつく」＝ think of。'},
        {'n': '4.', 'pts': 6, 'ans': 'A', 'exp': 'remote ＝「（場所が）遠く離れた・へんぴな」＝ distant。バスが1日2便しかないことがヒント。'},
        {'n': '5.', 'pts': 6, 'ans': 'A', 'exp': 'conceal ＝「隠す」＝ hide。smiled politely（礼儀正しくほほえんだ）から、気持ちを表に出さなかったと分かる。'},
        {'n': '6.', 'pts': 6, 'ans': 'B', 'exp': 'figure out ＝「（原因・答え）を理解する・解明する」＝ understand / work out。repair「修理する」は原因を知ったあとの行為。'},
        {'n': '7.', 'pts': 6, 'ans': 'D', 'exp': 'mild ＝「（気候が）穏やかな」＝ gentle。surprisingly … for the middle of January から、1月にしては寒くなかったと分かる。severe「厳しい」は反対。'},
        {'n': '8.', 'pts': 6, 'ans': 'C', 'exp': 'expand ＝「拡大する・広げる」＝ enlarge。to the next town（隣の町まで）とあるので move「移す」ではない。'},
        {'n': '9.', 'pts': 6, 'ans': 'B', 'exp': 'available ＝「入手できる・利用できる」＝ obtainable。displayed は「展示されている」で、手に入るかどうかは表さない。'},
        {'n': '10.', 'pts': 6, 'ans': 'D', 'exp': 'point out ＝「指摘する」＝ indicate。overlooked「見落とした」は反対の意味。'},
    ],
    'vocab': [('turn in / hand in', '提出する'), ('significant', 'かなりの・重要な'), ('come up with', '思いつく'), ('remote', '遠く離れた'), ('conceal', '隠す'),
              ('figure out', '理解する・解明する'), ('mild', '穏やかな'), ('expand', '拡大する'), ('available', '入手できる'), ('point out', '指摘する')],
}

SD = {
    'no': 'D', 'title': 'グラフを読んで英作文（C を解かない学部用）', 'pts': 60,
    'lead': '下のグラフについて、問い1・2 のどちらにも約100語の英語で解答せよ。書いた語数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'Average Time Spent per Day: Reading Books and Using Smartphones', 'x': ['10-19', '20-29', '30-39', '40-49', '50-59', '60 or older'],
              'series': [('Reading books (paper or e-books)', [28, 18, 15, 17, 22, 35]), ('Using smartphones (not for work)', [190, 172, 128, 106, 84, 48])],
              'ymax': 200, 'ystep': 40, 'ylabel': 'minutes per day', 'source': '（架空の調査。本書のために作成。年齢は years old）'},
    'qs': [
        {'n': '1.', 'q': 'According to the graph, how does the time people spend reading books and using smartphones change with age?', 'sheet': 'words12'},
        {'n': '2.', 'q': 'Some people say that high schools should set aside fifteen minutes every day for students to read books of their own choice. Do you agree with this idea? Explain your view with two or more reasons.', 'sheet': 'words12'},
    ],
    'ans': [
        {'n': '1.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（2つの変化と数字・対比）',
         'model': "The graph shows that smartphone use falls steadily with age, while reading time follows a different pattern. People in their teens use smartphones for about 190 minutes a day, but this drops to 106 minutes in their forties and to only 48 minutes for those aged 60 or older. Reading time, on the other hand, is lowest in the thirties at 15 minutes. It rises again after that and reaches 35 minutes among the oldest group. As a result, the gap between the two activities is very large for young people but becomes much smaller as people grow older.",
         'exp': '【構成】①全体の傾向（スマートフォンは年齢とともに減る／読書は30代で最も少なく、その後増える）→ ②具体的な数字（最大・最小・変わり目）→ ③まとめ（両者の差の変化）。\n【採点の観点】読み取りの正確さ 12点、数字を使った具体性 8点、文法・語彙 10点。グラフにないこと（理由の推測など）を長く書く必要はない。語数が大きく外れる（70語未満・130語超）ものは減点。'},
        {'n': '2.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋理由2つ＋結論）',
         'model': "I agree that high schools should give students fifteen minutes a day to read books they choose themselves. First, as the graph suggests, young people spend a lot of time on their phones and very little time reading. A fixed reading time would give them a quiet break from screens and help them build a habit that may last for life. Second, reading books of their own choice can show students that reading is enjoyable, not just homework. Someone who starts with a comic novel may later move on to history or science. For these reasons, I support the idea.",
         'exp': '【構成】①立場（agree / disagree）→ ②理由1（First, …）→ ③理由2（Second, …）→ ④結論。グラフの内容を理由に使うと説得力が増す。\n反対の立場（すでに忙しい授業時間が減る／読書は強制されると楽しくなくなる など）でも同じ基準で評価する。\n【採点の観点】立場と理由の明確さ 10点、具体性・論理のつながり 10点、文法・語彙 10点。'},
    ],
    'tr': [
        '【1 の解答例の訳】グラフは、スマートフォンの利用は年齢とともに着実に減る一方で、読書時間は違う形をとることを示している。10代はスマートフォンを1日約190分使うが、これは40代で106分、60歳以上ではわずか48分に下がる。一方、読書時間は30代が15分で最も少ない。その後再び増え、最も年齢の高いグループでは35分に達する。その結果、2つの活動の差は若い人では非常に大きいが、年齢が上がるにつれてずっと小さくなる。',
        '【2 の解答例の訳】私は、高校が生徒に毎日15分、自分で選んだ本を読む時間を与えるべきだという考えに賛成だ。第一に、グラフが示すように、若い人は携帯電話に多くの時間を使い、読書にはほとんど時間を使っていない。決まった読書の時間があれば、画面から離れて静かに休むことができ、一生続くかもしれない習慣を身につける助けになる。第二に、自分で選んだ本を読むことで、読書は宿題ではなく楽しいものだと生徒に示すことができる。ユーモアのある小説から始めた人が、のちに歴史や科学の本へ進むかもしれない。以上の理由から、私はこの考えを支持する。',
    ],
}
