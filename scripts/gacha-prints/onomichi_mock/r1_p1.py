# -*- coding: utf-8 -*-
# 第1回 Ⅰ：退屈は想像力の目覚まし時計（解説文。書き下ろし。人物・大学・実験は架空）
P1 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'In Praise of Empty Minutes',
    'passage': [
        "Most of us treat boredom as a small enemy. The moment a queue slows down or a train is delayed, our hands reach for our phones, "
        "and the empty minutes disappear before we have even noticed them. Yet a growing group of researchers believes that, {r1}, "
        "we may be throwing away something valuable.",

        "Dr. Helen Marsh, a psychologist who studies attention at Westmoor University, describes boredom as “a signal rather than a problem.” "
        "“When we feel bored,” she explains, “the mind is telling us that what we are doing no longer {u2|holds our interest}. That message is "
        "uncomfortable, but it pushes us to look for something new.” In other words, boredom works {bA} a kind of alarm clock for our curiosity. "
        "It is not the end of thinking but the beginning, much {bB} hunger is the beginning of a good meal.",

        "In one study at Westmoor, Marsh’s team asked two groups of volunteers to think of as many uses as possible for an ordinary paper cup. "
        "Before the task, the first group spent fifteen minutes copying numbers from an old telephone directory, a job that almost everyone "
        "finds {p3}. The second group started the task straight away. The results surprised even the researchers. The volunteers who had been "
        "bored first produced more ideas, and a panel of judges rated their ideas as more original.",

        "Why should this happen? Marsh’s explanation is that boredom {p4} the mind to wander. When there is nothing interesting in front of us, "
        "attention turns inward, and the brain begins to link memories and ideas that are usually kept apart. A cup becomes a seed pot, a tiny "
        "drum, or a mold for sand castles. Daydreaming, which teachers once scolded, may be one of the ways in which new connections are made.",

        "This {r5}, however. Long periods of boredom at school or at work can lead to stress, low motivation and poor results. The key, Marsh "
        "says, is the difference between boredom we cannot escape and short moments of boredom that we choose to {u6|tolerate}. “Ten minutes of "
        "staring out of a window is not wasted time,” she says. “It may be the most productive part of your afternoon.”",

        "Marsh now encourages her own students to try what she calls “empty walks”: short walks with no music, no podcasts and no messages. "
        "At first, many students say they feel nervous {p7} their phones, and some admit that they check their pockets every few minutes. "
        "After a week or two, however, a large number report that their best ideas for essays and projects came to them during these walks, "
        "not while they were sitting at their desks.",

        "Of course, a walk will not solve every problem, and nobody is suggesting that we throw our phones into the sea. But the next time you "
        "find yourself waiting for a late bus, it may be worth leaving your phone where it is. The few quiet minutes that follow might be exactly "
        "what your imagination has been waiting for.",
    ],
    'notes': [('telephone directory', '電話帳'), ('mold', '型'), ('scold', '叱る'), ('podcast', 'ネット配信の音声番組')],
    'questions': [
        {'label': '問1', 'type': 'order', 'ref': 1, 'points': 4, 'kind': '語の並べかえ', 'seed': 1101,
         'words': ['by', 'filling', 'every', 'gap', 'in', 'the', 'day'],
         'ja': '一日のすき間をすべて埋めることによって',
         'stem': '下線部(1)が「一日のすき間をすべて埋めることによって」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': '前置詞 by ＋動名詞 filling で「〜することによって」。filling の目的語は every gap（every の後ろは単数名詞），「一日の」は in the day で後ろから gap を修飾する。'},
        {'label': '問2', 'type': 'mc', 'ref': 2, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(2)の意味にもっとも近いものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['keeps our attention', 'earns us money', 'makes us tired', 'protects our health'], 'answer': 'イ',
         'expl': 'hold one’s interest は「〜の興味を引きつけておく」。退屈とは「今していることがもう興味を引かない」と心が知らせている状態だ，という文脈。'},
        {'label': '問3', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '空所補充',
         'stem': '空所(3)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['exciting', 'dull', 'dangerous', 'expensive'], 'answer': 'ロ',
         'expl': '電話帳の数字を15分写すのは「退屈な」作業。この作業で第1グループをわざと退屈させたのが実験のポイント。find O C「OをCだと思う」の形。'},
        {'label': '問4', 'type': 'word', 'points': 3, 'kind': '共通する語', 'answer': 'as',
         'stem': '第2段落の空所（ A ）と（ B ）には同じ1語が入る。その語を書きなさい。',
         'expl': '（A）work as 〜「〜として働く・機能する」。（B）much as …「ちょうど…と同じように」。どちらも as。'},
        {'label': '問5', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '空所補充（語法）',
         'stem': '空所(4)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['allows', 'lets', 'makes', 'has'], 'answer': 'イ',
         'expl': '後ろが the mind to wander（O ＋ to 不定詞）なので allow O to do「Oが〜するのを可能にする」。let / make / have は O の後ろに原形をとるので to が合わない。'},
        {'label': '問6', 'type': 'order', 'ref': 5, 'points': 4, 'kind': '語の並べかえ', 'seed': 1105,
         'words': ['does', 'not', 'mean', 'that', 'all', 'boredom', 'is', 'good'],
         'ja': 'これは，退屈がすべてよいという意味ではない',
         'stem': '下線部(5)が「これは，退屈がすべてよいという意味ではない」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'This does not mean that S V「これは S が V するという意味ではない」。that 節の中は all boredom is good（部分否定の内容）。直後の however と，次の文の「長く続く退屈は害になる」に自然につながる。'},
        {'label': '問7', 'type': 'mc', 'ref': 6, 'points': 3, 'kind': '語句の言いかえ',
         'stem': '下線部(6)と言いかえられる語句としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['avoid', 'put up with', 'look forward to', 'complain about'], 'answer': 'ロ',
         'expl': 'tolerate は「我慢する・耐える」で put up with と同じ意味。「逃れられない退屈」と「自分で選んで我慢する短い退屈」の対比になっている。'},
        {'label': '問8', 'type': 'mc', 'ref': 7, 'points': 3, 'kind': '空所補充（前置詞）',
         'stem': '空所(7)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['with', 'without', 'by', 'for'], 'answer': 'ロ',
         'expl': '音楽もメッセージもない散歩なので，学生は「スマートフォンがないと」落ち着かない。直後の「数分ごとにポケットを確かめる」もヒント。'},
        {'label': '問9', 'type': 'tf', 'points': 7, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('Marsh は，退屈を，心が新しいものを探すよう背中を押す合図だと考えている。', True),
             ('紙コップの実験では，すぐに課題に取りかかったグループのほうが多くのアイデアを出した。', False),
             ('Marsh によれば，学校や職場で長く続く退屈は，ストレスややる気の低下につながることがある。', True),
             ('「empty walks」では，好きな音楽を聞きながら歩くことがすすめられている。', False),
             ('筆者は，スマートフォンを海に捨ててしまうべきだと主張している。', False),
         ],
         'expl': '(ア) 第2段落 a signal…pushes us to look for something new。(イ) 第3段落：先に退屈した人のほうが多く出した。(ウ) 第5段落 Long periods of boredom … can lead to stress, low motivation。(エ) 第6段落 no music。(オ) 第7段落 nobody is suggesting that we throw our phones into the sea。'},
    ],
    'translation': [
        'たいていの人は退屈を小さな敵のように扱う。列の進みが遅くなったり電車が遅れたりしたとたん，手はスマートフォンに伸び，空いた数分は気づく前に消えてしまう。しかし，一日のすき間をすべて埋めることによって，私たちは価値のあるものを捨てているのかもしれないと考える研究者が増えている。',
        'ウェストムーア大学で注意力を研究している心理学者ヘレン・マーシュ博士は，退屈を「問題というより合図」だと言う。「退屈を感じるとき，心は，今していることがもう自分の興味を引きつけていないと伝えているのです。その知らせは心地よくはありませんが，何か新しいものを探すよう私たちの背中を押します」。言いかえれば，退屈は好奇心の目覚まし時計のような働きをする。空腹がおいしい食事の始まりであるのとちょうど同じように，退屈は考えることの終わりではなく始まりなのだ。',
        'ウェストムーア大学のある研究で，マーシュのチームは2つのボランティアのグループに，ありふれた紙コップの使い道をできるだけ多く考えるよう頼んだ。課題の前に，第1グループは古い電話帳の数字を15分間書き写した。ほとんど誰もが退屈だと感じる作業である。第2グループはすぐに課題を始めた。結果には研究者たちでさえ驚いた。先に退屈したボランティアのほうが多くのアイデアを出し，審査員団も彼らのアイデアのほうが独創的だと評価したのだ。',
        'なぜこうなるのだろうか。マーシュの説明では，退屈は心がさまようのを可能にする。目の前に面白いものが何もないと注意は内側に向かい，脳はふだんは離れている記憶や考えを結びつけ始める。コップは種をまく鉢になり，小さな太鼓になり，砂の城の型になる。かつて先生に叱られた空想は，新しいつながりが生まれる方法の一つなのかもしれない。',
        'ただし，これは退屈がすべてよいという意味ではない。学校や職場で長く続く退屈は，ストレスややる気の低下，悪い成績につながることがある。大切なのは，逃れられない退屈と，自分で選んで我慢する短い退屈との違いだとマーシュは言う。「窓の外を10分ながめるのは無駄な時間ではありません。午後のうちでいちばん実りのある時間かもしれないのです」。',
        'マーシュは今，自分の学生たちに，彼女が「空っぽの散歩」と呼ぶものを試すようすすめている。音楽も音声番組もメッセージもない短い散歩である。最初は，多くの学生がスマートフォンがないと落ち着かないと言い，数分ごとにポケットを確かめてしまうと認める学生もいる。しかし1，2週間たつと，レポートや課題のいちばんよいアイデアは机に向かっているときではなく，この散歩の間に浮かんだと報告する学生がたくさん出てくる。',
        'もちろん，散歩であらゆる問題が解決するわけではないし，スマートフォンを海に投げ捨てようと言う人もいない。けれども，今度遅れているバスを待つことになったら，スマートフォンはそのままにしておく価値があるかもしれない。そのあとに続く静かな数分こそ，あなたの想像力が待っていたものなのかもしれない。',
    ],
    'vocab': [('treat A as B', 'AをBとして扱う'), ('delay', '遅らせる'), ('describe A as B', 'AをBだと言い表す'), ('curiosity', '好奇心'),
              ('volunteer', '（実験の）参加者'), ('rate A as B', 'AをBと評価する'), ('original', '独創的な'), ('wander', 'さまよう'),
              ('inward', '内側へ'), ('motivation', 'やる気'), ('productive', '実りの多い'), ('admit', '認める')],
}
