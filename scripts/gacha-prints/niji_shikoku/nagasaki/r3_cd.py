# 長崎大学 前期 英語 予想問題 第3回 C（理系選抜の学部用）／D（それ以外の学部用）— すべてマナトビ編集部の書き下ろし
M = ['A.', 'B.', 'C.', 'D.']

SC = {
    'no': 'C', 'title': '語彙・同意表現（教育〈文系以外〉・情報データ科学〈理系〉用）', 'pts': 60, 'marks': M,
    'lead': '1〜10 の英文の下線を引いた語句に意味が最も近いものを、A〜D の中から1つずつ選び、記号で答えよ。',
    'qs': [
        {'n': '1.', 'q': 'The museum will {_:set up} a special exhibition on local history next month.', 'opts': ['close', 'organize', 'visit', 'review'], 'sheet': 'box'},
        {'n': '2.', 'q': 'The scientist gave a {_:brief} explanation of her research before the questions began.', 'opts': ['short', 'detailed', 'boring', 'clear'], 'sheet': 'box'},
        {'n': '3.', 'q': 'You should not {_:give in} to pressure from your friends if you think they are wrong.', 'opts': ['respond', 'yield', 'listen', 'object'], 'sheet': 'box'},
        {'n': '4.', 'q': 'It is {_:essential} to wear a helmet when you ride a motorcycle.', 'opts': ['popular', 'optional', 'necessary', 'difficult'], 'sheet': 'box'},
        {'n': '5.', 'q': 'The teacher asked us to {_:go over} our answers once more before handing in the test.', 'opts': ['check', 'erase', 'share', 'guess'], 'sheet': 'box'},
        {'n': '6.', 'q': 'The old bridge was {_:demolished} to make way for a wider one.', 'opts': ['painted', 'protected', 'torn down', 'rebuilt'], 'sheet': 'box'},
        {'n': '7.', 'q': 'Many young people {_:look up to} the famous soccer player.', 'opts': ['respect', 'envy', 'imitate', 'criticize'], 'sheet': 'box'},
        {'n': '8.', 'q': 'The company tried to {_:minimize} the risk of accidents in the factory.', 'opts': ['ignore', 'measure', 'increase', 'reduce'], 'sheet': 'box'},
        {'n': '9.', 'q': 'His story about seeing a ghost sounded {_:plausible} at first, but nobody believed it later.', 'opts': ['frightening', 'believable', 'ridiculous', 'familiar'], 'sheet': 'box'},
        {'n': '10.', 'q': 'The festival was {_:called off} because of the approaching typhoon.', 'opts': ['cancelled', 'delayed', 'shortened', 'advertised'], 'sheet': 'box'},
    ],
    'ans': [
        {'n': '1.', 'pts': 6, 'ans': 'B', 'exp': 'set up ＝「設ける・準備する（開催する）」＝ organize / arrange。'},
        {'n': '2.', 'pts': 6, 'ans': 'A', 'exp': 'brief ＝「短い・簡潔な」＝ short。detailed「詳しい」は反対の意味。'},
        {'n': '3.', 'pts': 6, 'ans': 'B', 'exp': 'give in (to) ＝「（〜に）屈する・従う」＝ yield (to) / surrender (to)。object「反対する」は逆。'},
        {'n': '4.', 'pts': 6, 'ans': 'C', 'exp': 'essential ＝「絶対に必要な」＝ necessary / vital。optional「任意の」は反対。'},
        {'n': '5.', 'pts': 6, 'ans': 'A', 'exp': 'go over ＝「見直す・よく調べる」＝ check / review。'},
        {'n': '6.', 'pts': 6, 'ans': 'C', 'exp': 'demolish ＝「（建物などを）取り壊す」＝ tear down / pull down。to make way for a wider one（もっと広い橋を造るために）がヒント。'},
        {'n': '7.', 'pts': 6, 'ans': 'A', 'exp': 'look up to ＝「尊敬する」＝ respect / admire。反対は look down on「見下す」。'},
        {'n': '8.', 'pts': 6, 'ans': 'D', 'exp': 'minimize ＝「最小限にする」＝ reduce。increase は反対の意味。'},
        {'n': '9.', 'pts': 6, 'ans': 'B', 'exp': 'plausible ＝「もっともらしい・信じられそうな」＝ believable。but nobody believed it later との対比がヒント。'},
        {'n': '10.', 'pts': 6, 'ans': 'A', 'exp': 'call off ＝「中止する」＝ cancel。delay「遅らせる」は put off に近い。'},
    ],
    'vocab': [('set up', '設ける・準備する'), ('brief', '短い・簡潔な'), ('give in', '屈する'), ('essential', '絶対に必要な'), ('go over', '見直す'),
              ('demolish', '取り壊す'), ('look up to', '尊敬する'), ('minimize', '最小限にする'), ('plausible', 'もっともらしい'), ('call off', '中止する')],
}

SD = {
    'no': 'D', 'title': 'グラフを読んで英作文（C を解かない学部用）', 'pts': 60,
    'lead': '下のグラフについて、問い1・2 のどちらにも約100語の英語で解答せよ。書いた語数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。',
    'chart': {'title': 'What Junior High and High School Students Mainly Use to Get News', 'x': ['TV', 'Newspapers', 'News websites/apps', 'Social media', 'Video sites'],
              'series': [('2016', [64, 12, 14, 7, 3]), ('2026', [28, 3, 21, 31, 17])],
              'ymax': 70, 'ystep': 10, 'ylabel': '% of students', 'source': '（架空の調査。本書のために作成）'},
    'qs': [
        {'n': '1.', 'q': 'Using the graph, explain how the main sources of news for students changed between 2016 and 2026.', 'sheet': 'words12'},
        {'n': '2.', 'q': 'Some people say that getting news mainly from social media is risky for young people. Do you agree? Explain your view with two or more reasons.', 'sheet': 'words12'},
    ],
    'ans': [
        {'n': '1.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（テレビ・新聞の減少とSNS・動画の増加・数字）',
         'model': "The graph shows a big shift in how students mainly get news. In 2016, television was by far the most common source, used by 64 percent of students, but by 2026 this figure had fallen to 28 percent. Newspapers also dropped, from 12 to only 3 percent. In contrast, social media rose sharply from 7 to 31 percent and became the top source. Video sites grew from 3 to 17 percent, and news websites and apps also increased, though only from 14 to 21 percent. Overall, students have clearly moved away from traditional media such as TV and newspapers toward online sources, especially social media.",
         'exp': '【構成】①全体の変化（伝統的なメディア→オンライン）→ ②テレビ・新聞の減少（数字）→ ③SNS・動画サイトの増加（SNS が首位に）→ ④まとめ。\n【採点の観点】読み取りの正確さ 12点、数字を使った具体性 8点、文法・語彙 10点。'},
        {'n': '2.', 'pts': 30, 'min_words': 88, 'max_words': 118, 'ans': '（下の解答例を参照）', 'short': '下の解答例を参照（立場＋理由2つ＋結論）',
         'model': "I agree that relying mainly on social media for news can be risky for young people. First, anyone can post on social media, so false information spreads quickly, and it is often hard to tell who wrote a story or whether it was checked. Second, social media shows us posts based on what we have liked before. As a result, young people may see only opinions they already agree with and miss other points of view. Social media can still be useful for finding news quickly, but students should compare it with reliable sources such as newspapers or official websites.",
         'exp': '【構成】①立場 → ②理由1（誤情報・発信者や確認の不明さ）→ ③理由2（好みに合わせた表示で視野が狭くなる）→ ④条件つきの結論。\n反対の立場（速報性がある／多様な人の声が聞ける／自分で確かめる力を育てればよい など）でも同じ基準で評価する。\n【採点の観点】立場と理由の明確さ 10点、具体性・論理のつながり 10点、文法・語彙 10点。'},
    ],
    'tr': [
        '【1 の解答例の訳】グラフは、生徒が主にニュースを得る方法が大きく変わったことを示している。2016年にはテレビが群を抜いて多い情報源で、64パーセントの生徒が使っていたが、2026年までにこの数字は28パーセントに下がった。新聞も12パーセントからわずか3パーセントに減った。対照的に、SNS は7パーセントから31パーセントへと急増し、最も多い情報源になった。動画サイトは3パーセントから17パーセントに伸び、ニュースサイトやアプリも、14パーセントから21パーセントと小幅ながら増えた。全体として、生徒はテレビや新聞といった伝統的なメディアから、オンラインの情報源、特に SNS へとはっきり移っている。',
        '【2 の解答例の訳】ニュースを主に SNS に頼ることは若い人にとって危険になりうるという考えに賛成だ。第一に、SNS には誰でも投稿できるので、誤った情報がすぐに広まり、誰が記事を書いたのか、内容が確かめられたのかを見分けるのが難しいことが多い。第二に、SNS は私たちが以前に「いいね」を押したものをもとに投稿を表示する。その結果、若い人はすでに賛成している意見ばかりを目にし、ほかの見方を見逃すかもしれない。SNS はニュースを素早く見つけるにはやはり役に立つが、生徒は新聞や公式のウェブサイトなど信頼できる情報源と比べるべきだ。',
    ],
}
