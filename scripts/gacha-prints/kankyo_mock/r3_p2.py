# -*- coding: utf-8 -*-
# 第3回 Part 2（英作文）
P2 = {
    'points': 24,
    'lead': '次の問いについて，あなたの考えを英語で書きなさい。150 語以上で書き，最後に使った語数を書くこと。',
    'prompt': 'In your opinion, what is the better way to learn about a foreign country: traveling there for a short time, or reading books '
              'and watching films about it at home? Explain your opinion with reasons and examples.',
    'prompt_ja': '外国について学ぶには，短い期間そこを旅行するのと，家でその国についての本を読んだり映画を見たりするのと，どちらがよい方法だと思いますか。理由と例を挙げて自分の意見を説明しなさい。',
    'model': "I think traveling to a country, even for a short time, is a better way to learn about it than reading books or watching "
             "films at home. The main reason is that travel lets us use all of our senses. When I visited Taiwan with my family last "
             "year, I could smell the food at the night market and hear people talking in the streets. No book could give me that "
             "experience.\n"
             "Another reason is that travel gives us chances to talk with local people. On the same trip, a shop owner taught me a few "
             "words of Chinese and told me about her favorite festival. Through this short conversation, I learned how people there "
             "actually live, which is often different from what films show.\n"
             "It is true that books and films are cheaper and can teach us about history in more detail. However, I believe they are "
             "most useful before and after a trip, not instead of one. For these reasons, I would choose to travel.",
    'model_ja': [
        '私は，短い期間であっても，その国へ旅行するほうが，家で本を読んだり映画を見たりするよりもその国について学ぶよい方法だと思う。いちばんの理由は，旅行ではすべての感覚を使えることだ。去年家族と台湾を訪れたとき，私は夜市の食べ物のにおいをかぎ，通りで人々が話す声を聞くことができた。どんな本もその経験を与えてはくれない。',
        'もう一つの理由は，旅行では地元の人と話す機会があることだ。同じ旅行で，ある店の主人が中国語の言葉をいくつか教えてくれ，お気に入りの祭りについて話してくれた。この短い会話を通して，私はそこの人々が実際にどう暮らしているかを知った。それは映画が見せるものとは違うことが多い。',
        '本や映画のほうが安く，歴史についてより詳しく教えてくれるのは確かだ。しかし，それらは旅行のかわりではなく，旅行の前後にこそいちばん役に立つと私は思う。これらの理由から，私は旅行を選ぶ。',
    ],
    'tips': [
        '最初の文で，二つのうちどちらを選ぶかをはっきり書く（I think traveling … is a better way …）。比べる問題なので better / than を使う。',
        '理由は2つにしぼり，自分の体験（いつ・どこで・何をしたか）を具体例にすると，150語に無理なく届く。',
        '選ばなかった方法のよい点（安い・詳しい）を It is true that … で認め，However で自分の考えに戻すと説得力が増す。',
        '体験は過去形，一般的な考えは現在形と，時制を分けて書く。',
        '最後に For these reasons, … で結論をくり返し，語数（150 words 以上）を確かめる。',
    ],
    'criteria': [
        ('問いに答えている：どちらの方法を選ぶかがはっきり書かれている', 6),
        ('内容：理由が二つ程度あり，それぞれに具体例がある', 6),
        ('構成：導入・理由・もう一方の方法への言及・結論の流れがあり，つなぎの語句が使われている', 4),
        ('英語の正確さ：文法・語法・つづりの誤りが少なく，意味が通じる', 6),
        ('語数：150語以上（不足する場合は大きく減点）', 2),
    ],
}
