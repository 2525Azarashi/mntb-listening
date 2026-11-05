# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第3回 大問3（書き下ろし）
P3 = {
    'points': 100,
    'scene': '放課後，ＡさんとＢさんが文化祭の準備について話している。',
    'lines': [
        ('Ａ', '文化祭のポスター，締め切りが明日なのに，まだ半分しかできていないんだ。今夜は寝られそうにないよ。'),
        ('Ｂ', '一人で抱えこまないで，手伝おうか。色をぬるくらいなら私にもできるし，二人でやれば二時間もかからないと思う。'),
        ('Ａ', '本当に助かるよ。代わりに，来週の数学の小テストの前に，わからないところを教えるね。'),
    ],
    'criteria': [('Ａの1つ目：「締め切りが明日なのに」「まだ半分しかできていない」「寝られそうにない」', 30),
                 ('Ｂ：「一人で抱えこまないで」の中身の表現・申し出の表現・「二時間もかからない」', 35),
                 ('Ａの2つ目：感謝の表現と「代わりに～を教える」（来週の小テストの前に）', 25),
                 ('全体の語彙・文法・つづりの正確さ', 10)],
    'models': [
        ["The poster for the school festival is due tomorrow, but I've only finished half of it. I don't think I'll be able to sleep tonight.",
         "You don't have to do it all by yourself. Shall I help you? I can at least color it in, and if we work together, I think it'll take less than two hours.",
         "That would really help. In return, I'll explain the parts you don't understand before next week's math quiz."],
        ["Even though the deadline for the festival poster is tomorrow, only half of it is done. It looks like I'll be up all night.",
         "Don't try to handle everything alone. Let me help. Even I can do the coloring, and with two of us, it shouldn't take more than two hours.",
         "Thanks a lot. To pay you back, I'll help you with anything you find difficult before our math quiz next week."],
    ],
    'expl': [
        'Ａの1つ目：「締め切りが明日」は ～ is due tomorrow / the deadline is tomorrow。「～なのに」は but / even though でつなぐ。'
        '「半分しかできていない」は I\'ve only finished half of it / only half of it is done。'
        '「寝られそうにない」は I don\'t think I\'ll be able to sleep / I\'ll be up all night。',
        'Ｂ：「一人で抱えこまないで」は中身をかみくだき，You don\'t have to do it all by yourself / Don\'t try to handle everything alone と表す。'
        '申し出は Shall I help you? / Let me help. / Would you like some help?。「～くらいなら私にもできる」は I can at least ～ / Even I can ～。'
        '「二時間もかからない」は take less than two hours / shouldn\'t take more than two hours。',
        'Ａの2つ目：「本当に助かる」は That would really help. / Thanks a lot.。「代わりに」は in return / to pay you back。'
        '「わからないところを教える」は explain the parts you don\'t understand / help you with anything you find difficult。ここでは teach より explain や help with が自然。',
    ],
    'tips': ['「締め切り」を limit としない。deadline / be due を使う。',
             '「寝られない」を can\'t sleep だけにすると「眠れない（不眠）」の意味にとられやすい。徹夜になる，という中身を be up all night などで表す。',
             '「抱えこむ」を hold や carry で直訳しない。「全部を一人でやる」という中身を英語にする。',
             '「小テスト」は quiz。small test でも通じるが，quiz のほうが自然。'],
}
