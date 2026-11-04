# -*- coding: utf-8 -*-
# 第2回 〔3〕 医学部：語句整序（24点）。英文は書き下ろし（歴史的事実は一般的な内容のみ。人物の発言・数値は架空の設定を含む）
M3 = {
    'lead': '次の英文の【　①　】〜【　⑥　】には，下の a〜f の [　] 内の語句を並べ替えてできる英語が1つずつ入る。'
            '[　] 内の語句を正しく並べ替え，【　①　】〜【　⑥　】に入る英語をそれぞれ解答欄に書きなさい（a〜f の記号は書かなくてよい）。'
            'ただし，文頭に来る語も小文字で示してある。',
    'title': 'Listening to the Body',
    'passage': [
        'Few objects are as closely connected with doctors as the stethoscope. Hanging around the neck of a doctor, it has become a symbol of the medical profession itself, '
        'and many children who play “doctor” at home ask for a toy one. Yet this simple tool is only about two hundred years old, and {o1}.',

        'Before the stethoscope, doctors who wanted to hear the sounds inside a patient’s chest had to press an ear directly against the body. '
        'This method had obvious problems. It was uncomfortable for both doctor and patient, and the sounds were often too faint to be useful. '
        'In the early nineteenth century, a French doctor faced exactly this difficulty with a young patient. He rolled a sheet of paper into a tube, '
        'placed one end on her chest and put his ear to the other. To his surprise, {o2} than he had ever heard it before.',

        'He soon replaced the paper with a wooden tube and spent several years studying the sounds made by healthy and diseased lungs and hearts. '
        'By carefully comparing what he heard with what was later found in his patients’ bodies, {o3} that doctors could use to identify particular illnesses. '
        'His work changed medicine, because for the first time doctors could learn about the inside of a living body without opening it.',

        'Over the following decades, the stethoscope was improved again and again. The single wooden tube gave way to rubber tubes and two earpieces, '
        '{o4} with both ears at once. Later models added a flat disc that made it easier to pick up high sounds, and a cup that was better for low ones.',

        'Today, some people wonder whether the stethoscope still has a future. Machines that use sound waves can now produce detailed pictures of the heart, '
        'and they show far more than any doctor can hear. Some medical schools have even reported that {o5} as well as students did in the past. '
        'Supporters of the old tool reply that it is cheap, needs no electricity and can be carried anywhere.',

        'There is another reason why many doctors want to keep it. Placing a stethoscope on a patient’s chest requires the doctor to come close, to touch the patient and to pay full attention for a moment. '
        'For many patients, this simple act is reassuring. As one experienced doctor put it, {o6} is often the first step towards helping them.',
    ],
    'notes': [('stethoscope', '聴診器'), ('profession', '（専門的な）職業'), ('faint', 'かすかな'), ('lung', '肺'),
              ('give way to ～', '～に取って代わられる'), ('earpiece', '（耳に入れる）イヤーピース'), ('disc', '円盤'), ('reassuring', '安心させる')],
    'items': [
        {'key': 'a', 'shown': ['to', 'listen', 'allowed', 'doctors', 'which'], 'answer': ['which', 'allowed', 'doctors', 'to', 'listen'],
         'slot': 4, 'expl': 'コンマのあとの非制限用法の which が「ゴム管と2つのイヤーピース」を受ける。allow 人 to do「人が～できるようにする」。続きの with both ears at once「両耳で同時に」とつながる。'},
        {'key': 'b', 'shown': ['the heart', 'he', 'more clearly', 'could hear', 'beating'], 'answer': ['he', 'could hear', 'the heart', 'beating', 'more clearly'],
         'slot': 2, 'expl': '後ろの than he had ever heard it before と比較の形がそろう（it = the heart）。hear O doing「O が～しているのを聞く」。'},
        {'key': 'c', 'shown': ['is', 'how', 'surprisingly simple', 'was invented', 'the story of', 'it'],
         'answer': ['the story of', 'how', 'it', 'was invented', 'is', 'surprisingly simple'],
         'slot': 1, 'expl': '主語は the story of how it was invented「それがどのように発明されたかという話」（前置詞 of のあとに間接疑問 how ＋ S ＋ V）。動詞 is ＋ 補語 surprisingly simple。'},
        {'key': 'd', 'shown': ['he', 'a', 'list', 'of', 'sounds', 'built up'], 'answer': ['he', 'built up', 'a', 'list', 'of', 'sounds'],
         'slot': 3, 'expl': '文頭の By carefully comparing … は分詞的な前置き（～することによって）で，主節の主語は he。build up「（少しずつ）作り上げる」。後ろの that doctors could use … は a list of sounds を修飾する関係代名詞。'},
        {'key': 'e', 'shown': ['the tool', 'many', 'use', 'cannot', 'young doctors'], 'answer': ['many', 'young doctors', 'cannot', 'use', 'the tool'],
         'slot': 5, 'expl': 'that 節の主語 many young doctors ＋ cannot use ＋ 目的語 the tool。後ろの as well as students did in the past「昔の学生ほど上手に」と比べている。did は used the tool の代わり。'},
        {'key': 'f', 'shown': ['that', 'listening', 'patients', 'you', 'showing', 'to', 'them', 'are'], 'answer': ['showing', 'patients', 'that', 'you', 'are', 'listening', 'to', 'them'],
         'slot': 6, 'expl': '動名詞 showing が主語で，後ろの is often the first step の主語になる。show 人 that ～「人に～ということを示す」。listen to them「彼らの話を聞く」の現在進行形。'},
    ],
    'translation': [
        '聴診器ほど医師と深く結びついている物はほとんどない。医師の首にかけられたそれは，医療という職業そのものの象徴になっており，家で「お医者さんごっこ」をする子どもの多くはおもちゃの聴診器を欲しがる。'
        'しかし，この単純な道具はほんの200年ほどの歴史しかなく，それがどのように発明されたかという話は驚くほど単純である。',
        '聴診器ができる前は，患者の胸の中の音を聞きたい医師は，耳を直接体に押し当てなければならなかった。この方法には明らかな問題があった。医師にとっても患者にとっても気まずく，'
        '音はかすかすぎて役に立たないことが多かった。19世紀の初め，あるフランス人医師が，若い患者を前にしてまさにこの困難に直面した。彼は1枚の紙を丸めて筒にし，'
        '一方の端を彼女の胸に当て，もう一方の端に耳をつけた。驚いたことに，心臓が鼓動しているのが，それまで聞いたどんなときよりもはっきりと聞こえたのである。',
        '彼はすぐに紙を木の筒に替え，健康な肺や心臓と病気の肺や心臓が立てる音を何年もかけて研究した。聞こえた音と，あとで患者の体の中に見つかったものを注意深く比べることによって，'
        '彼は，医師が特定の病気を見分けるのに使える音の一覧を作り上げた。彼の研究は医学を変えた。医師が初めて，生きている体を開かずにその内部について知ることができるようになったからである。',
        'その後の数十年間で，聴診器は何度も改良された。1本の木の筒はゴム管と2つのイヤーピースに取って代わられ，医師は両耳で同時に聞けるようになった。'
        'のちの型には，高い音を拾いやすくする平らな円盤と，低い音に向いたカップが加えられた。',
        '今日，聴診器にまだ未来があるのかと疑問に思う人もいる。音波を使う機械は今では心臓の詳しい画像を作り出すことができ，それはどんな医師が聞き取れるよりもはるかに多くのことを示す。'
        '多くの若い医師は昔の学生ほど上手にその道具を使えないと報告している医学部さえある。古い道具を支持する人々は，聴診器は安く，電気がいらず，どこへでも持ち運べると反論する。',
        '多くの医師がそれを残したいと思う理由はもう一つある。患者の胸に聴診器を当てるには，医師が近づき，患者に触れ，少しの間すべての注意を向けることが必要になる。'
        '多くの患者にとって，この単純な行為は安心できるものである。ある経験豊かな医師が言ったように，自分が話を聞いていることを患者に示すことが，しばしば患者を助ける第一歩なのである。',
    ],
    'vocab': [('be connected with ～', '～と結びついている'), ('symbol', '象徴'), ('press A against B', 'AをBに押し当てる'), ('obvious', '明らかな'),
              ('to one’s surprise', '驚いたことに'), ('identify', '見分ける'), ('decade', '10年間'), ('pick up ～', '（音など）を拾う'),
              ('as … put it', '…が言ったように')],
}
