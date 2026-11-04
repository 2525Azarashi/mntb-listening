# -*- coding: utf-8 -*-
# 第1回 問題Ⅰ：「正常値」という考え方の成り立ち（書き下ろし。都市・人物・数値・書名はすべて架空）
P1 = {
    'points': 50,
    'lead': '次の英文を読んで，問1〜問4に答えなさい。＊の付いた語句には文末に注がある。',
    'title': 'The Invention of the Normal Patient',
    'passage': [
        "When a doctor tells you that your blood pressure or your temperature is \u201cnormal,\u201d the word sounds like a simple "
        "description of nature. Yet the idea that the human body has a normal state, against which every individual can be measured, "
        "is surprisingly recent. For most of history, healers did not compare a patient with an average person. They compared the "
        "patient with himself: {u1|what mattered was not whether a man\u2019s pulse resembled that of his neighbours, but whether it had "
        "changed from what it had been before he fell ill}.",

        "The change began when hospitals started to keep records. In the city of Brennholt, a physician named Tomas Verhalt collected "
        "the temperatures of more than eight thousand patients over twelve years. By adding the figures together and dividing the "
        "total by their number, he arrived at a single value that he called the \u201chealthy temperature.\u201d His book was translated "
        "into many languages, and within a generation, doctors everywhere were treating his figure as a fact about the human body "
        "rather than as a fact about his patients.",

        "There was a problem, however, that few readers noticed. Verhalt\u2019s patients were not a random sample* of humanity. Most were "
        "working men from one northern city, many of them already ill, and his thermometers were slow and unreliable by modern "
        "standards. {u2|It is not that his figure was wrong, exactly; it is that it described a particular group of people measured in "
        "a particular way, and was then taken to describe everyone}. When researchers repeated the measurements a century and a half "
        "later with better instruments, they found that the average temperature of healthy adults was noticeably lower, and that it "
        "varied with age, the time of day and even the season.",

        "The story matters because the idea of the normal does more than describe. It also tells us what to do. Once a number is "
        "called normal, any body that does not match it begins to look like a body in need of correction. {u3|A value that was first "
        "chosen simply because it was easy to calculate can thus come to decide who is regarded as sick, who receives treatment and "
        "who does not}. This is especially serious when the original measurements left out whole groups, such as women, children or "
        "the elderly, whose bodies may differ in ways that matter.",

        "None of this means that averages are useless. Without them, modern medicine could hardly exist. But it does suggest that we "
        "should remember where our numbers come from. A careful doctor treats the average as a starting point for thinking about a "
        "particular patient, not as a {u4|standard} that every patient must meet.",
    ],
    'source': '（Hilde Marrow, //Counting the Body//, 2019 より。編集部による架空の文章）',
    'notes': [('random sample', '無作為に選んだ標本'), ('Brennholt', 'ブレンホルト（架空の都市名）')],
    'translation': [
        '医師があなたの血圧や体温は「正常」だと告げるとき，その言葉は自然をありのままに述べたもののように聞こえる。しかし，人間の体には正常な状態があり，あらゆる個人をそれに照らして測ることができるという考えは，驚くほど新しいものである。歴史の大部分において，治療者は患者を平均的な人と比べはしなかった。彼らは患者をその人自身と比べたのである。（1）大切なのは，ある男性の脈が隣人たちの脈に似ているかどうかではなく，その脈が病気になる前の状態から変わったかどうかだった。',
        '変化が始まったのは，病院が記録をつけるようになってからである。ブレンホルトという都市で，トマス・フェアハルトという医師が，12年にわたって8000人を超える患者の体温を集めた。数値を合計し，その合計を数値の個数で割ることで，彼は「健康な体温」と呼ぶ一つの値にたどりついた。彼の本は多くの言語に翻訳され，一世代のうちに，あらゆる場所の医師が彼の数値を，彼の患者についての事実としてではなく，人間の体についての事実として扱うようになっていた。',
        'しかし，ほとんどの読者が気づかなかった問題があった。フェアハルトの患者は人類から無作為に選ばれた標本ではなかった。大部分は北部の一つの都市の労働者の男性で，その多くはすでに病気にかかっており，また彼の体温計は現代の基準からすれば反応が遅く，当てにならないものだった。（2）彼の数値が厳密な意味で間違っていたというわけではない。それは特定のやり方で測定された特定の集団の人々を表していたのに，そのあとすべての人を表すものだと受け取られてしまった，ということなのである。150年後に研究者たちがよりよい器具で測定をやり直したところ，健康な大人の平均体温ははっきりと低く，しかも年齢や時刻，さらには季節によっても変わることがわかった。',
        'この話が重要なのは，「正常」という考えが，ものごとを記述する以上のことをするからである。それは私たちに何をすべきかも告げる。ある数値がいったん正常と呼ばれると，それに合わない体はどれも，正す必要のある体のように見え始める。（3）こうして，最初はただ計算しやすいという理由だけで選ばれた値が，誰が病気とみなされ，誰が治療を受け，誰が受けないかを決めるようになりうるのである。もとの測定が，女性や子どもや高齢者のように，大切な点で体が違っているかもしれない集団をまるごと除いていた場合には，このことはとりわけ深刻である。',
        'こうしたことはどれも，平均が役に立たないという意味ではない。平均がなければ，現代の医学はほとんど成り立たないだろう。しかし，こうしたことは，私たちが自分たちの数値の出どころを覚えておくべきだということを示している。注意深い医師は，平均を一人ひとりの患者について考えるための出発点として扱うのであって，すべての患者が満たさなければならない（4）基準として扱うのではない。',
    ],
    'vocab': [('resemble', '〜に似ている'), ('arrive at', '〜にたどりつく'), ('within a generation', '一世代のうちに'),
              ('unreliable', '当てにならない'), ('vary with', '〜によって変わる'), ('in need of', '〜を必要として'),
              ('be regarded as', '〜とみなされる'), ('leave out', '〜を除く'), ('hardly', 'ほとんど〜ない')],
    'about': '出典は架空の医学史の本。「正常値」が，ある時代・ある集団の測定から生まれた数値であることを論じる。下線部はどれも，指示語（it / that / this）や not A but B，it is not that … it is that … などの構文を正しくとらえることがポイント。',
}
