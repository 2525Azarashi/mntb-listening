# -*- coding: utf-8 -*-
# 第2回 Part 3：お知らせを読み，会話の空所に入る英語を書く（書き下ろし。施設・人物・数値はすべて架空）
P3 = {
    'points': 12,
    'type': 'write',
    'lead': '次のお知らせを読み，それについての会話の空所（ 1 ）〜（ 4 ）に入る適切な英語を，それぞれ1〜3語で書きなさい。',
    'info': {
        'title': 'Hollin Bay Beach Clean-Up Day',
        'lines': [
            'Date: Saturday, June 14 (If it rains, the event will be held on Sunday, June 15.)',
            'Time: 9:00 a.m. – 11:30 a.m.  Meeting place: the car park next to Hollin Bay Station',
            'Please bring: a hat, a towel and something to drink. Gloves and bags will be provided.',
            'Volunteers under 16 must come with an adult. All volunteers will receive a free lunch ticket for the Seaside Café.',
        ],
    },
    'conv': [
        ('Mia', 'Do you want to join the beach clean-up with me? It’s on Saturday morning.'),
        ('Tom', 'Sure. But what if it rains on Saturday?'),
        ('Mia', 'Then it will be held on {c1} instead.'),
        ('Tom', 'OK. Where do we meet?'),
        ('Mia', 'In the car park next to the {c2}. It starts at nine.'),
        ('Tom', 'Do I need to buy gloves?'),
        ('Mia', 'No, you don’t. They’ll {c3} them. Just bring a hat, a towel and a drink.'),
        ('Tom', 'Great. My little brother is twelve. Can he come too?'),
        ('Mia', 'Yes, but he has to come with an {c4}. Could your father join us?'),
        ('Tom', 'I’ll ask him. And I hear we get a free lunch at the Seaside Café afterwards!'),
    ],
    'answers': [
        ['Sunday', 'Sunday, June 15', 'June 15'],
        ['station', 'Hollin Bay Station'],
        ['provide', 'supply'],
        ['adult'],
    ],
    'expl': [
        'お知らせの1行目（If it rains, the event will be held on Sunday, June 15.）から，雨なら日曜日に行われる。on のあとなので Sunday（June 15 をつけてもよい）。',
        '集合場所は the car park next to Hollin Bay Station。空所の前に the があるので station（Hollin Bay Station も可）。',
        'Gloves and bags will be provided.（手袋と袋は用意される）を，They’ll（主催者が）を主語にして言いかえる。will のあとなので原形 provide（supply も可）。',
        'Volunteers under 16 must come with an adult. から，16歳未満の弟は大人といっしょに来なければならない。an のあとなので母音で始まる adult。',
    ],
    'ja': [
        'ホリン湾 海岸清掃の日　日時：6月14日（土）（雨の場合は6月15日（日）に行います）　時間：午前9時〜11時30分　集合場所：ホリン湾駅の隣の駐車場　持ち物：帽子・タオル・飲み物。手袋と袋は用意します。16歳未満のボランティアは大人といっしょに来てください。ボランティア全員にシーサイド・カフェの無料昼食券をお渡しします。',
        'ミア：いっしょに海岸の清掃に参加しない？土曜日の朝なんだ。　トム：いいよ。でも土曜日に雨が降ったらどうなるの？　ミア：そのときはかわりに（1 日曜日）に行われるよ。　トム：わかった。どこに集まるの？　ミア：（2 駅）の隣の駐車場だよ。9時に始まるんだ。',
        'トム：手袋は買わないといけない？　ミア：ううん，いらないよ。向こうが（3 用意して）くれるんだ。帽子とタオルと飲み物だけ持ってきて。　トム：よかった。弟が12歳なんだけど，いっしょに行ってもいい？　ミア：うん，でも（4 大人）といっしょに来ないといけないんだ。お父さんも来られるかな？　トム：聞いてみるよ。それに，終わったらシーサイド・カフェで無料の昼食が食べられるんだってね！',
    ],
}
