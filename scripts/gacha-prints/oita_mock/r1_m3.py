# -*- coding: utf-8 -*-
# 第1回 〔3〕 医学部：語句整序（24点）。英文は書き下ろし（人物・数値は架空）
M3 = {
    'lead': '次の英文の【　①　】〜【　⑥　】には，下の a〜f の [　] 内の語句を並べ替えてできる英語が1つずつ入る。'
            '[　] 内の語句を正しく並べ替え，【　①　】〜【　⑥　】に入る英語をそれぞれ解答欄に書きなさい（a〜f の記号は書かなくてよい）。'
            'ただし，文頭に来る語も小文字で示してある。',
    'title': 'Why We Yawn',
    'passage': [
        'Almost everyone yawns several times a day. Babies yawn even before they are born, and many animals, from dogs to fish, yawn as well. And yet scientists still argue about why we do it. For a long time, the most popular explanation was '
        'that yawning brings more oxygen into the body. When we are tired or bored, the idea went, our breathing becomes shallow, and {o1}. '
        'It sounds reasonable, but experiments have not supported it. When volunteers breathed air containing extra oxygen, they yawned just as often as before. Yawning, it seems, has little to do with a shortage of oxygen.',

        'A newer idea is that yawning helps to cool the brain. Like a computer, the brain works best within a narrow range of temperatures. '
        'A deep yawn pulls a large amount of air into the mouth and nose and increases the flow of blood to the head, {o2}. '
        'Supporting this idea, one study found that people yawned less often when they held a cold pack against their foreheads. '
        'Another found that people yawn more in mild weather than in very hot weather. Breathing in air cannot do much to cool the brain {o3}.',

        'Yawning is also famous for being contagious. Seeing, hearing, or even reading about a yawn can make us yawn ourselves; '
        'some readers may already have yawned while reading this paragraph. Interestingly, {o4} than when a stranger does. '
        'Some researchers think this shows that contagious yawning is connected with empathy, the ability to share the feelings of others. Dogs, too, are known to catch yawns from their owners more readily than from people they have never met.',

        'Children seem to support this view. Very young children rarely catch yawns from others, and {o5} until they are about four or five years old, '
        'which is roughly the age at which they begin to understand what other people are thinking. '
        'However, not all scientists are convinced, and some studies have found only a weak link between yawning and empathy.',

        'Doctors also pay attention to yawning. In rare cases, yawning far more than usual can be a sign of a problem with the nervous system '
        'or a side effect of certain medicines, {o6}. For most of us, though, a yawn is simply a yawn, and there is no need to hide it, '
        'except perhaps during a long meeting.',
    ],
    'notes': [('yawn', 'あくび（をする）'), ('shallow', '浅い'), ('cold pack', '保冷剤'), ('forehead', '額'),
              ('contagious', 'うつりやすい'), ('empathy', '共感'), ('nervous system', '神経系'), ('side effect', '副作用')],
    'items': [
        {'key': 'a', 'shown': ['the', 'body', 'need', 'may', 'catch', 'up', 'to'], 'answer': ['the', 'body', 'may', 'need', 'to', 'catch', 'up'],
         'slot': 1, 'expl': '「呼吸が浅くなる → 体が追いつく必要がある」という古い説。may need to do「～する必要があるのかもしれない」。catch up は「遅れを取り戻す」。'},
        {'key': 'b', 'shown': ['a family member yawns', 'more likely', 'we are', 'when', 'to yawn'],
         'answer': ['we are', 'more likely', 'to yawn', 'when', 'a family member yawns'],
         'slot': 4, 'expl': '後ろの than when a stranger does と比較の形がそろう（does = yawns）。be likely to do「～しやすい」の比較級 be more likely to do。'
         '「知らない人があくびをするときより，家族があくびをするときのほうが」という対比をつかむ。'},
        {'key': 'c', 'shown': ['the', 'brain', 'may', 'which', 'help', 'cool'], 'answer': ['which', 'may', 'help', 'cool', 'the', 'brain'],
         'slot': 2, 'expl': 'コンマのあとの非制限用法の which が前の内容全体を受ける。help do「～するのに役立つ」は to を省略できる。'},
        {'key': 'd', 'shown': ['the', 'outside', 'air', 'when', 'too', 'warm', 'is'], 'answer': ['when', 'the', 'outside', 'air', 'is', 'too', 'warm'],
         'slot': 3, 'expl': 'cannot do much to cool the brain「脳を冷やすのにあまり役立たない」のは「外気が暑すぎるとき」。接続詞 when ＋ 主語 the outside air ＋ is too warm。'},
        {'key': 'e', 'shown': ['do', 'not', 'begin', 'most', 'to', 'do', 'so'], 'answer': ['most', 'do', 'not', 'begin', 'to', 'do', 'so'],
         'slot': 5, 'expl': 'most (children) do not begin to do so until ～「ほとんどの子どもは～になって初めてそうし始める」。do so は catch yawns を受ける。not ～ until … の形。'},
        {'key': 'f', 'shown': ['should', 'a', 'doctor', 'checked', 'by', 'be', 'and'], 'answer': ['and', 'should', 'be', 'checked', 'by', 'a', 'doctor'],
         'slot': 6, 'expl': '主語 yawning far more than usual を受けて and should be checked by a doctor「医師に診てもらうべきだ」。助動詞＋受け身 should be done。'},
    ],
    'translation': [
        'ほとんど誰もが1日に何回かあくびをする。赤ちゃんは生まれる前からあくびをするし，犬から魚まで多くの動物もあくびをする。それなのに，なぜそうするのかについて科学者たちはいまだに議論している。長い間，最も一般的な説明は，あくびは体内により多くの酸素を取り込むというものだった。'
        'その考えによれば，疲れたり退屈したりすると呼吸が浅くなり，体は遅れを取り戻す必要があるのかもしれない，というのである。もっともらしく聞こえるが，実験はそれを裏づけていない。'
        '余分な酸素を含む空気を吸ったボランティアも，以前とまったく同じくらいの頻度であくびをしたのだ。あくびは酸素不足とはほとんど関係がないようである。',
        'より新しい考えは，あくびが脳を冷やすのに役立つというものである。コンピューターと同じように，脳は狭い温度の範囲内で最もよく働く。深いあくびは大量の空気を口と鼻に引き込み，'
        '頭への血流を増やすので，それが脳を冷やすのに役立つのかもしれない。この考えを裏づけるように，ある研究では，額に保冷剤を当てた人はあくびの回数が減った。'
        '別の研究では，人はとても暑い天候のときより穏やかな天候のときによくあくびをすることが分かった。外気が暑すぎるときには，空気を吸い込んでも脳を冷やすことはあまりできないのである。',
        'あくびは，うつりやすいことでも有名である。あくびを見たり，聞いたり，あくびについて読んだりするだけでも，自分があくびをしてしまうことがある。この段落を読みながら，すでにあくびをした読者もいるかもしれない。'
        '興味深いことに，私たちは知らない人があくびをするときより，家族があくびをするときのほうがあくびをしやすい。これは，うつるあくびが共感，つまり他人の気持ちを分かち合う能力と関係があることを示していると考える研究者もいる。犬もまた，会ったことのない人より飼い主からのほうがあくびがうつりやすいことが知られている。',
        '子どもはこの見方を支持しているように見える。とても幼い子どもはめったに他人のあくびがうつらず，ほとんどの子どもは4，5歳ごろになって初めてそうし始める。'
        'それはおよそ，他人が考えていることを理解し始める年齢である。しかし，すべての科学者が納得しているわけではなく，あくびと共感の間には弱い関連しか見つからなかった研究もある。',
        '医師もあくびに注目している。まれに，ふだんよりはるかに多くあくびをすることが神経系の問題の兆候だったり，ある種の薬の副作用だったりすることがあり，医師に診てもらうべきである。'
        'とはいえ，私たちの大部分にとって，あくびはただのあくびであり，隠す必要はない。ただし，長い会議の最中は別かもしれないが。',
    ],
    'vocab': [('and yet', 'それなのに'), ('the idea went', 'その考えによれば'), ('reasonable', 'もっともらしい'), ('range', '範囲'),
              ('mild', '穏やかな'), ('catch a yawn', 'あくびがうつる'), ('roughly', 'およそ'), ('convinced', '納得している'), ('rare', 'まれな')],
}
