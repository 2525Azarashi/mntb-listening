# -*- coding: utf-8 -*-
# 第3回 Ⅰ：「ちょうどいい」選択肢の数（解説文。書き下ろし。人物・大学・店・実験は架空）
P1 = {
    'points': 33,
    'lead': '次の英文を読んで，後の問いに答えなさい。',
    'title': 'When More Choice Means Less',
    'passage': [
        "Walk into a large supermarket and you may find more than forty kinds of breakfast cereal on a single shelf. Most of us assume that "
        "this is a good thing. If there are more options, surely we are more likely to find exactly what we want. Yet researchers who study "
        "decision-making have found that {r1}, too much choice can leave people feeling worse rather than better.",

        "In a well-known experiment at a food market in the town of Corwen, a team led by the economist Laura Pike set up a table where "
        "shoppers could taste different kinds of jam. On some days the table offered twenty-four flavors, and on other days only six. The "
        "larger display {p2} more people to stop and try the jam. However, when it came to actually buying a jar, the result was reversed. "
        "Shoppers who had seen only six flavors were about five times more likely to make a purchase.",

        "Pike calls this “choice overload.” When there are too many possibilities, comparing them all becomes tiring, and people worry that "
        "they will pick the wrong one. Many of them {u3|put off} the decision, and some give up completely. “The shopper who walks away "
        "without buying anything,” Pike says, “is often not someone who found nothing good. It is someone who found too many good things.”",

        "Even when people do decide, a large number of options can reduce their satisfaction. With only a few choices, we can feel confident "
        "that we chose well. With dozens, it is easy to imagine that one of the others {p4} have been better. This feeling of regret "
        "can spoil the pleasure of something that is, in fact, perfectly good.",

        "Some businesses have learned from this research. A clothing shop in Corwen reduced the number of shirts it sold from more than 200 "
        "designs to about 60, and its sales rose by nearly a fifth. Several restaurants have also shortened their menus, {u5|claiming} that "
        "customers order more quickly and leave happier when they have fewer dishes to think about. One owner added that her cooks were "
        "happier too, because they could now spend more time on each dish.",

        "This does not mean that choice is always bad. When people know exactly what they want, or when they are experts in a field, a wide "
        "range of options can be useful. A professional photographer, for example, may be glad to find fifty types of lens in a shop, while a "
        "beginner may feel completely lost. {r6} depends on who is choosing and how much they already know.",

        "So what can ordinary shoppers do? Pike’s advice is to decide in advance what really matters and to stop searching once something "
        "meets those needs. “You do not have to find the best jam in the world,” she says. “You only have to find one that you will enjoy on "
        "your toast tomorrow morning.”",
    ],
    'notes': [('cereal', 'シリアル（穀物の朝食食品）'), ('flavor', '味・風味'), ('overload', '過多・過重'), ('lens', 'レンズ')],
    'questions': [
        {'label': '問1', 'type': 'order', 'ref': 1, 'points': 3, 'kind': '語の並べかえ', 'seed': 3101,
         'words': ['in', 'a', 'surprising', 'number', 'of', 'situations'],
         'ja': '意外なほど多くの場面で',
         'stem': '下線部(1)が「意外なほど多くの場面で」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'a number of …「多くの…」の number を形容詞 surprising が修飾して a surprising number of situations。前置詞 in を先頭に置いて「〜の場面で」。'},
        {'label': '問2', 'type': 'mc', 'ref': 2, 'points': 3, 'kind': '空所補充（語法）',
         'stem': '空所(2)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['encouraged', 'prevented', 'kept', 'stopped'], 'answer': 'イ',
         'expl': '後ろが more people to stop（O ＋ to 不定詞）なので encourage O to do「Oに〜するよう促す」。prevent / keep / stop は O from doing の形をとる。直後の However とも合う（立ち寄る人は多いが買う人は少ない）。'},
        {'label': '問3', 'type': 'mc', 'ref': 3, 'points': 3, 'kind': '語句の意味',
         'stem': '下線部(3)の意味にもっとも近いものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['complete', 'share', 'postpone', 'celebrate'], 'answer': 'ハ',
         'expl': 'put off「延期する・先のばしにする」＝ postpone。続く「完全にあきらめる人もいる」へと程度が強まっていく流れ。'},
        {'label': '問4', 'type': 'mc', 'ref': 4, 'points': 3, 'kind': '空所補充（助動詞）',
         'stem': '空所(4)にあてはまる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['can', 'might', 'will', 'shall'], 'answer': 'ロ',
         'expl': 'might have done「〜だったかもしれない」（過去についての推量）。選ばなかったほうがよかったかもしれないと想像してしまう，という意味。'},
        {'label': '問5', 'type': 'mc', 'ref': 5, 'points': 3, 'kind': '語句の言いかえ',
         'stem': '下線部(5)と言いかえられる語としてもっともふさわしいものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['denying', 'doubting', 'forgetting', 'saying'], 'answer': 'ニ',
         'expl': 'claim は「（事実だと）主張する・言う」。レストランは「品数が少ないと客は早く注文し満足して帰る」と言っている。denying「否定して」は逆。'},
        {'label': '問6', 'type': 'order', 'ref': 6, 'points': 3, 'kind': '語の並べかえ', 'seed': 3106,
         'words': ['Whether', 'choice', 'helps', 'or', 'hurts'],
         'ja': '選択肢が助けになるか害になるか',
         'stem': '下線部(6)が「選択肢が助けになるか害になるか（は）」という意味の英語になるよう，（　）内の語を並べかえ，記号を左から順に書きなさい。',
         'expl': 'Whether A or B「AかBか（ということ）」の名詞節が文の主語になり，depends on …「…しだいである」が続く。'},
        {'label': '問7', 'type': 'word', 'points': 3, 'kind': '抜き出し', 'answer': 'choice overload', 'from_para': 2, 'n_words': 2,
         'stem': '選択肢が多すぎると比べるのに疲れ，決められなくなる現象を Pike は何と呼んでいるか。第3段落から連続する2語で抜き出して書きなさい。',
         'expl': '第3段落の最初の文 Pike calls this “choice overload.”。call O C「OをCと呼ぶ」。'},
        {'label': '問8', 'type': 'mc', 'points': 5, 'kind': '内容の理解',
         'stem': 'ジャムの実験についての説明としてもっとも適切なものを，次の(イ)〜(ニ)から一つ選び，記号を書きなさい。',
         'choices': ['24種類並べた日のほうが，ジャムを買った人の数が多かった。',
                     '6種類だけ並べた日のほうが，立ち止まって味見をした人が多かった。',
                     '6種類だけ見た買い物客は，約5倍ジャムを買いやすかった。',
                     '実験は大学の研究室で，学生を対象に行われた。'], 'answer': 'ハ',
         'expl': '第2段落の最後の文 about five times more likely to make a purchase。(イ) 買った人は6種類の日のほうが多い。(ロ) 立ち止まったのは24種類の日のほうが多い。(ニ) 実験はコーウェンの町の食品市場で行われた。'},
        {'label': '問9', 'type': 'tf', 'points': 7, 'kind': '内容一致',
         'stem': '次の(ア)〜(オ)が本文の内容と合っていれば〇，合っていなければ×を書きなさい。',
         'items': [
             ('Pike によると，何も買わずに立ち去る客の多くは，よいものを一つも見つけられなかった人である。', False),
             ('選択肢がたくさんあると，実際にはよいものを選んでいても後悔を感じやすくなる。', True),
             ('コーウェンのある衣料品店は，シャツのデザインの数を減らしたあと売り上げが落ちた。', False),
             ('専門家にとっては，幅広い選択肢が役に立つこともある。', True),
             ('Pike は，何を大切にするかを前もって決め，それを満たすものが見つかったら探すのをやめるよう助言している。', True),
         ],
         'expl': '(ア) 第3段落：よいものを見つけすぎた人である。(イ) 第4段落。(ウ) 第5段落：売り上げは約5分の1増えた。(エ) 第6段落。(オ) 第7段落。'},
    ],
    'translation': [
        '大きなスーパーマーケットに入ると，一つの棚に40種類を超える朝食用シリアルが並んでいることがある。たいていの人はこれをよいことだと思っている。選択肢が多ければ，ほしいものをぴったり見つけられる可能性はきっと高くなるはずだ，と。ところが意思決定を研究する人たちは，意外なほど多くの場面で，選択肢が多すぎると人の気分はよくなるどころか悪くなりうることを発見している。',
        'コーウェンの町の食品市場で行われたよく知られた実験で，経済学者ローラ・パイクが率いるチームは，買い物客がさまざまなジャムを味見できるテーブルを設けた。ある日にはテーブルに24種類の味を並べ，別の日には6種類だけにした。大きな陳列のほうが，より多くの人に立ち止まって味見をするよう促した。しかし実際にびんを買うことになると，結果は逆になった。6種類しか見なかった買い物客のほうが，約5倍買いやすかったのである。',
        'パイクはこれを「選択過多」と呼ぶ。可能性が多すぎると，すべてを比べるのは疲れるし，人はまちがったものを選ぶのではないかと心配する。多くの人は決めるのを先のばしにし，完全にあきらめてしまう人もいる。「何も買わずに立ち去る客は，よいものを何も見つけられなかった人とはかぎりません。よいものを見つけすぎた人であることが多いのです」とパイクは言う。',
        '実際に決めた場合でも，選択肢が多いと満足感が下がることがある。選択肢が少しなら，自分はうまく選んだと自信をもてる。何十もあると，ほかのどれかのほうがよかったかもしれないと想像しやすくなる。この後悔の気持ちは，実はまったく申し分のないものから得られる喜びを台なしにしかねない。',
        'この研究から学んだ企業もある。コーウェンのある衣料品店は，扱うシャツを200を超えるデザインから約60に減らしたところ，売り上げがほぼ5分の1増えた。メニューを短くしたレストランもいくつかあり，考える料理が少ないほうが客は早く注文し，満足して帰っていくと言っている。ある店主は，一つひとつの料理にかけられる時間が増えたので，料理人たちも前より満足しているとつけ加えた。',
        'だからといって，選択肢がいつも悪いわけではない。自分がほしいものがはっきりわかっているときや，その分野の専門家であるときには，幅広い選択肢が役に立つこともある。たとえばプロの写真家は店に50種類のレンズがあれば喜ぶかもしれないが，初心者はすっかり途方に暮れてしまうかもしれない。選択肢が助けになるか害になるかは，誰が選ぶのか，そしてその人がすでにどれだけ知っているかしだいなのだ。',
        'では，ふつうの買い物客はどうすればよいのだろうか。パイクの助言は，何が本当に大切かを前もって決め，それを満たすものが見つかったら探すのをやめることだ。「世界一のジャムを見つける必要はありません。明日の朝トーストにぬって楽しめるものを一つ見つければよいのです」と彼女は言う。',
    ],
    'vocab': [('option', '選択肢'), ('assume', '思いこむ'), ('decision-making', '意思決定'), ('display', '陳列'),
              ('when it comes to …', '…のこととなると'), ('reverse', '逆にする'), ('purchase', '購入'), ('satisfaction', '満足'),
              ('regret', '後悔'), ('add that …', '…とつけ加える'), ('spoil', '台なしにする'), ('in advance', '前もって'), ('meet one’s needs', '必要を満たす')],
}
