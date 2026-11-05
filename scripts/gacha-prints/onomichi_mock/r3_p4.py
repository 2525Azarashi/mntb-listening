# -*- coding: utf-8 -*-
# 第3回 Ⅳ：日本文に合わせた並べ替え（書き下ろし）
P4 = {
    'points': 18,
    'lead': '次の1〜6について，日本語の内容を表す英文になるよう（　）内の8語を並べかえたとき，前から数えて4番目と7番目にくる語の記号をそれぞれ書きなさい。',
    'items': [
        {'ja': '私たちが乗るはずだった電車は，今日，大雪のため運休になった。', 'pre': 'The train', 'post': 'because of heavy snow.', 'seed': 3401,
         'words': ['we', 'were', 'supposed', 'to', 'take', 'was', 'canceled', 'today'],
         'expl': 'The train (that) we were supposed to take が主語（目的格の関係代名詞の省略）。be supposed to do「〜することになっている」。述語は受動態 was canceled。'},
        {'ja': '彼がなぜそんなに怒っているのか，私にはさっぱりわからない。', 'pre': 'I', 'post': 'angry.', 'seed': 3402,
         'words': ['have', 'no', 'idea', 'why', 'he', 'is', 'getting', 'so'],
         'expl': 'have no idea ＋間接疑問「…がまったくわからない」。間接疑問は why S V の語順（why is he とはしない）。get angry「怒る」の進行形 is getting so angry。'},
        {'ja': 'この本は難しすぎて，小さな子どもには十分に理解できない。', 'pre': 'This book', 'post': 'understand.', 'seed': 3403,
         'words': ['is', 'too', 'difficult', 'for', 'young', 'children', 'to', 'fully'],
         'expl': 'too … for 人 to do「…すぎて人には〜できない」。to understand の目的語は主語の This book なので，文末に it を置かない。fully は to と understand の間に入る。'},
        {'ja': '窓を少し開けたままにしておいてもかまいませんか。', 'pre': 'Would you', 'post': 'open?', 'seed': 3404,
         'words': ['mind', 'if', 'I', 'left', 'the', 'window', 'a', 'little'],
         'expl': 'Would you mind if I ＋過去形 …?「…してもかまいませんか」。leave O C「OをCのままにしておく」で left the window open。a little は open を修飾する。'},
        {'ja': 'その店は，開店してからずっと地元の人々に愛されてきた。', 'pre': 'The shop', 'post': 'it opened.', 'seed': 3405,
         'words': ['has', 'been', 'loved', 'by', 'local', 'people', 'ever', 'since'],
         'expl': '現在完了の受動態 has been loved「ずっと愛されてきた」。ever since S V「Sが〜して以来ずっと」。'},
        {'ja': '大切なのは，何を言うかではなく，どのように伝えるかだ。', 'pre': 'What matters is', 'post': 'which you express it.', 'seed': 3406,
         'words': ['not', 'what', 'you', 'say', 'but', 'the', 'way', 'in'],
         'expl': 'not A but B「AではなくB」。A は what you say「あなたが言うこと」，B は the way in which you express it「それを伝えるやり方」。the way in which S V は the way S V / how S V と同じ意味。'},
    ],
}
