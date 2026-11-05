# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第1回 大問3（書き下ろし）
P3 = {
    'points': 100,
    'scene': '高校の教室で，ＡさんとＢさんが通学について話している。',
    'lines': [
        ('Ａ', '先週から自転車で通学しているんだけど，思っていたより坂がきつくて，毎朝くたくたになるよ。'),
        ('Ｂ', 'それなら電動アシスト付きの自転車にしたら？　少し高いけど，雨の日以外は毎日使うなら，元は取れると思うよ。'),
        ('Ａ', '確かにね。でも，まずは一か月続けてみて，本当に毎日乗るかどうか確かめてから決めるつもり。'),
    ],
    'criteria': [('Ａの1つ目：「先週から〜している」（現在完了進行形または始まりを言う過去形）と「思っていたより」の比較', 30),
                 ('Ｂ：提案の表現（Why don\'t you ~? / How about ~?）と，「元は取れる」をかみくだいた表現', 35),
                 ('Ａの2つ目：「一か月続けてみる」「〜かどうか確かめてから決める」', 25),
                 ('全体の語彙・文法・つづりの正確さ', 10)],
    'models': [
        ["I've been riding my bike to school since last week, but the hills are steeper than I expected, so I'm exhausted every morning.",
         "Then why don't you get an electric bicycle? It's a little expensive, but if you use it every day except when it rains, I think it'll be worth the money.",
         "You may be right. But first I'm going to keep riding for a month and check whether I really use my bike every day before I decide."],
        ["I started cycling to school last week. The slopes are harder than I thought, and I'm worn out when I arrive every morning.",
         "How about buying a bike with an electric motor? It costs a bit more, but if you ride it on all the days that aren't rainy, it will pay for itself.",
         "That's true. Still, I'll try going on like this for a month to find out if I actually ride every day, and then I'll make up my mind."],
    ],
    'expl': [
        'Ａの1つ目：「先週から〜している」は，今も続いているので現在完了進行形 have been riding ... since last week が基本。I started cycling to school last week と「始めた」と言いかえてもよい。'
        '「思っていたより坂がきつい」は比較級＋than I expected / than I thought。「くたくたになる」は be exhausted / be worn out / be very tired。',
        'Ｂ：「〜にしたら？」は提案なので Why don\'t you ~? / How about ~ing? / You should ~ など。「電動アシスト付きの自転車」は an electric bicycle / a bike with an electric motor でよい。'
        '「元は取れる」はそのまま訳しにくいので，「お金を払う価値がある（be worth the money）」「（節約で）費用をまかなえる（pay for itself）」のように中身をかみくだく。「雨の日以外」は except on rainy days / except when it rains。',
        'Ａの2つ目：「まずは一か月続けてみる」は keep riding for a month / try it for a month。「〜かどうか」は whether / if。'
        '「確かめてから決める」は before I decide / and then I\'ll decide のように順番がわかる形にする。「〜するつもり」は be going to ~ / will ~。',
    ],
    'tips': ['since last week と現在形（I ride ... since）をいっしょに使うのは誤り。since は完了形と組み合わせる。',
             '「坂」は slope / hill。「きつい」を hard だけでなく steep（急な）で表すと正確になる。',
             '「元が取れる」を get my original back のように直訳しない。言いたいこと（払ったお金に見合う）を英語で言える形に置きかえる。',
             '「〜かどうか確かめる」の if は名詞節なので，if I will ride としない（未来のことでも if I really ride / whether I ride）。※ここでは「確かめる」時点での事実なので現在形でよい。'],
}
