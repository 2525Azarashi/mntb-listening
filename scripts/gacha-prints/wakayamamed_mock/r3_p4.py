# -*- coding: utf-8 -*-
# 第3回 問題Ⅳ：日本語の随筆の下線部を英訳（書き下ろし。筆者・書名は架空）
P4 = {
    'points': 50,
    'lead': '以下の日本文を読み，下線部(1)・(2)の内容を英語で書き表せ。',
    'passage_ja': [
        '学生のころ，ある老医師の外来を見学させてもらったことがある。その先生は，患者が診察室に入ってくると，カルテを見る前に必ず顔を上げて「今日はどうしましたか」と尋ねた。検査の数値はあとでいくらでも確かめられるが，患者の表情はその場でしか見られない，というのが口ぐせだった。',
        '当時の私は，それを少し古いやり方だと思っていた。{u1|機械がこれほど進歩した時代に，医師の目に頼る必要はないと考えていたのである}。ところが，自分が医師として働くようになって，あの先生の言葉の意味が少しずつわかってきた。',
        '数値は嘘をつかないが，すべてを語るわけでもない。痛みをこらえて平気な顔をする人もいれば，不安のあまり言葉が出てこない人もいる。{u2|患者が何を言わずにいるのかに気づけるかどうかは，結局のところ，目の前の人をどれだけよく見ているかにかかっている}。今では私も，カルテより先に患者の顔を見るようにしている。',
    ],
    'source': '（三浦 遥『診察室の窓から』より。編集部による架空の文章）',
    'questions': [
        {'label': '(1)', 'ref': '1', 'points': 25,
         'models': [
             'I thought that, in an age when machines had made such great progress, doctors no longer needed to rely on their own eyes.',
             'Since medical machines had become so advanced, I believed there was no need for doctors to depend on what they could see for themselves.',
         ],
         'tips': [
             '文の骨組みは「私は〜と考えていた（I thought / believed that …）」。主節が過去なので，that 節の中も時制をそろえる（needed / had made）。',
             '「〜な時代に」は in an age when … / in an era when …。「これほど進歩した」は had made such great progress や had become so advanced。',
             '「〜する必要はない」は did not need to do / there was no need for A to do。「もはや」の気持ちを no longer で加えるとよい。',
             '「医師の目に頼る」は rely on their own eyes / depend on what they could see。eyes だけで意味が伝わりにくいと思えば，解答例2のように言いかえる。',
         ],
         'criteria': [('「〜と考えていた」の骨組みと時制の一致が正しい', 6),
                      ('「機械がこれほど進歩した時代に」を in an age when … などで表している', 7),
                      ('「〜する必要はない」を did not need to / there was no need などで表している', 5),
                      ('「医師の目に頼る」を自然な英語で表し，文法・つづりの誤りがない', 7)]},
        {'label': '(2)', 'ref': '2', 'points': 25,
         'models': [
             'Whether we can notice what a patient is not saying depends, in the end, on how carefully we look at the person in front of us.',
             'In the end, our ability to realize what patients are leaving unsaid depends on how closely we observe the person before us.',
         ],
         'tips': [
             '文の骨組みは「〜かどうかは…にかかっている」＝ Whether … depends on …。whether 節が主語なので動詞は単数の depends。',
             '「何を言わずにいるのか」は間接疑問 what a patient is not saying。leave A unsaid（A を口にしないでおく）も使える。',
             '「どれだけよく見ているか」は how carefully / how closely we look at …。how の直後に副詞を置く語順に注意。',
             '「結局のところ」は in the end / after all。主語が明示されていないので，医師全体を表す we で書くと自然。',
         ],
         'criteria': [('「〜かどうかは…にかかっている」を Whether … depends on … などで正しく表している', 7),
                      ('「何を言わずにいるのか」を間接疑問の正しい語順で表している', 7),
                      ('「どれだけよく見ているか」を how carefully … などで表している', 6),
                      ('文法・語法・つづりの誤りがない', 5)]},
    ],
    'about': '架空の医師の随筆。「カルテより先に患者の顔を見る」ことの意味を，自分の経験から考える。「〜な時代に」「〜する必要はない」「〜かどうかは…にかかっている」など，英語の型に当てはめて書ける表現を見つけることがポイント。',
}
