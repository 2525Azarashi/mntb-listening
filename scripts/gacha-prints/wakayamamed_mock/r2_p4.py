# -*- coding: utf-8 -*-
# 第2回 問題Ⅳ：日本語の随筆の下線部を英訳（書き下ろし。筆者・書名は架空）
P4 = {
    'points': 50,
    'lead': '以下の日本文を読み，下線部(1)・(2)の内容を英語で書き表せ。',
    'passage_ja': [
        '子どものころ，祖母の家の庭には大きな柿の木があった。秋になると実がたくさんなったが，祖母はいつも高い枝の実をいくつか取らずに残しておいた。理由を尋ねると，「あれは鳥の分だよ」と笑うだけだった。',
        '当時の私には，せっかくの実をわざわざ残すのはもったいないことに思えた。{u1|しかし大人になってから，あの数個の柿のことをよく思い出すようになった}。自分の手に入るものは全部取ってしまう，というのは，じつは豊かさではなく，余裕のなさのあらわれなのかもしれない。',
        '何かを残しておくことは，自分以外の誰かがいることを忘れないということでもある。{u2|便利さを追い求めるあまり，私たちは他の生き物と分け合うという考え方を失いつつあるのではないだろうか}。冬の空の下で鳥が柿をついばむ姿を思い浮かべながら，私はときどきそう考える。',
    ],
    'source': '（篠原 真澄『庭の時間』より。編集部による架空の文章）',
    'questions': [
        {'label': '(1)', 'ref': '1', 'points': 25,
         'models': [
             'However, after I grew up, I often came to think of those few persimmons.',
             'Since becoming an adult, however, I have often found myself remembering the few persimmons my grandmother left on the tree.',
         ],
         'tips': [
             '「〜するようになった」は come to do や began to do で表す。「大人になってから今まで」と考えれば現在完了（have often remembered / found myself remembering）も使える。',
             '「思い出す」は remember / think of / recall。「よく」は often で，位置は一般動詞の前・助動詞の後ろ。',
             '「あの数個の柿」は those few persimmons。柿を知らない読み手を考え，解答例2のように「祖母が木に残した」と補ってもよい。',
             '「大人になる」は grow up / become an adult。after I grew up と過去形にするか，since 〜 と現在完了にするかで時制をそろえる。',
         ],
         'criteria': [('「大人になってから」を after I grew up / since becoming an adult などで表している', 6),
                      ('「〜するようになった」を come to do / began to do / 現在完了などで正しく表している', 7),
                      ('「あの数個の柿のことを思い出す」を正しく表している', 7),
                      ('時制・文法・つづりの誤りがない', 5)]},
        {'label': '(2)', 'ref': '2', 'points': 25,
         'models': [
             'I wonder if, in our pursuit of convenience, we are losing the idea of sharing with other living things.',
             'Because we are so eager to make our lives more convenient, we may be forgetting that we should share the world with other creatures.',
         ],
         'tips': [
             '「〜ではないだろうか」は I wonder if … や，we may be doing（〜しているのかもしれない）で表すとよい。疑問文の形（Aren\'t we …?）にすると強い言い方になる。',
             '「〜を追い求めるあまり」は in our pursuit of 〜 や because we are so eager to do 〜 と言いかえる。直訳の too much を使うと意味がずれやすい。',
             '「失いつつある」は進行形 are losing。「つつある」の変化の途中を表す。',
             '「他の生き物と分け合う」は share with other living things / creatures。何を分け合うかがはっきりしなければ，share the world with … と補う。',
         ],
         'criteria': [('「〜ではないだろうか」を I wonder if … / may be などで表している', 5),
                      ('「便利さを追い求めるあまり」を自然な英語に言いかえている', 7),
                      ('「失いつつある」を進行形などで表している', 5),
                      ('「他の生き物と分け合うという考え方」を正しく表している', 5),
                      ('文法・語法・つづりの誤りがない', 3)]},
    ],
    'about': '架空の随筆。祖母が柿の実を鳥のために残していた思い出から，「分け合うこと」の意味を考える。「〜するようになった」「〜あまり」「〜ではないだろうか」など，日本語らしい表現を英語の型に言いかえられるかがポイント。',
}
