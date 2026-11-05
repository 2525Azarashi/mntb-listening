# -*- coding: utf-8 -*-
# 第2回 〔1〕 設問（基準配点 100：教育学部版。経済 ×1.2・医 ×0.4）
P1Q = {'questions': [
    {'label': '問1', 'kind': '語形変化を伴う空所補充', 'type': 'formfill', 'points': 20, 'nums': [1, 2, 3, 4],
     'box': ['allow', 'depend', 'discover', 'fill', 'organize', 'reduce'],
     'bases': ['fill', 'organize', 'allow', 'discover'],
     'answers': ['filling', 'organized', 'allows', 'discovering'],
     'stem': '本文中の空所（　①　）〜（　④　）に入れる語を下の語群から選び，必要があれば適切な形に変えて書きなさい。同じ語は1度しか使えない。',
     'expl': '① 前置詞 by のあとなので動名詞 filling。fill A with B「A を B で埋める」。'
             '② Their days are ～ by adults の受け身なので過去分詞 organized「大人によって組み立てられる」。'
             '③ 主語 a screen は3人称単数・現在。allow 人 to do「人が～するのを可能にする」→ allows。'
             '④ 前置詞 without のあとなので動名詞 discovering。（各5点）'},
    {'label': '問2', 'kind': '指示語の内容説明', 'type': 'ja', 'points': 15, 'ref': 'A', 'lines': 3,
     'stem': '下線部(A)の This が指す内容を，本文に即して具体的に日本語で説明しなさい。',
     'answer': '豆を色ごとに分けるという退屈な作業を先にしたボランティアのほうが，ゼムクリップの使い道をより多く，しかもより風変わりなものまで思いついたこと。',
     'expl': 'This は直前の文（実験の結果）を指す。「退屈な作業をした人」と「しなかった人」の比較であることを示し，'
             '「アイデアの数が多い」「より風変わり」の2点を入れる。実験の手順だけを書いても結果がなければ得点にならない。',
     'criteria': [('退屈な作業（豆を色ごとに分ける作業）を先にした人たちについての結果であることを書いている', 5),
                  ('使い道（アイデア）をより多く思いついたことを書いている', 5),
                  ('そのアイデアがより風変わりだったことを書いている', 5)]},
    {'label': '問3', 'kind': '空所補充（つなぎの語句）', 'type': 'mc', 'points': 5, 'answer': 'ウ',
     'stem': '本文中の空所（　B　）に入る最も適切なものを，(ア)〜(エ)の中から1つ選び，その記号を書きなさい。',
     'choices': [('ア', 'For instance'), ('イ', 'In short'), ('ウ', 'Over time'), ('エ', 'Therefore')],
     'expl': '「最初の数週間は不満でいっぱいだった」→「（　）何かが変わり始めた」。時間がたつにつれての変化なので Over time「時がたつにつれて」。'
             'Therefore「したがって」では不満が変化の原因になってしまい，意味が通らない。'},
    {'label': '問4', 'kind': 'ことわざ', 'type': 'mc', 'points': 5, 'answer': 'イ',
     'stem': '第6段落のモレノ先生の話の内容に最も合うことわざを，(ア)〜(エ)の中から1つ選び，その記号を書きなさい。',
     'choices': [('ア', 'Strike while the iron is hot.'), ('イ', 'Good things come to those who wait.'),
                 ('ウ', 'Too many cooks spoil the broth.'), ('エ', 'Actions speak louder than words.')],
     'expl': '「少し待っていろいろ試せばアイデアが浮かぶ」「いちばん長い沈黙のあとによいアイデアが出た」は忍耐の大切さを述べている。'
             'イ「待つ者には良いことが訪れる（待てば海路の日和あり）」。ア「鉄は熱いうちに打て」は逆にすぐ行動せよという意味。'},
    {'label': '問5', 'kind': '下線部の内容', 'type': 'mc', 'points': 15, 'ref': 'C', 'answer': 'ア',
     'stem': '下線部(C)が表す内容に最も近いものを，(ア)〜(エ)の中から1つ選び，その記号を書きなさい。',
     'choices': [('ア', '短い時間で，何をするかを本人が自分で決めてよい退屈'),
                 ('イ', '授業が合わないために学校で毎日続く退屈'),
                 ('ウ', '大人が前もって計画を立ててくれる短い自由時間'),
                 ('エ', 'お金をかけずに遊ぶことのできる時間')],
     'expl': 'コロンのあとの a gap in the day that a person is allowed to fill in his or her own way が言いかえになっている。'
             'free は「無料の」ではなく「（何をするかが）自由な」の意味なのでエは誤り。イは前の文で「役に立たない退屈」として挙げられた例。'},
    {'label': '問6', 'kind': '下線部和訳', 'type': 'ja', 'points': 20, 'ref': 'D',
     'stem': '下線部(D)を和訳しなさい。',
     'answer': 'だとすれば，子どもに必要なのは退屈のない生活ではなく，何か手を打てば退屈はいつまでも続くわけではないと知る機会である。',
     'expl': 'What children need が主語（関係代名詞 what「～もの・こと」）。then は「それならば・だとすれば」で，前の段落までの内容を受ける。'
             'not A but B「A ではなく B」。the chance to find out that ～「～と知る機会」。'
             'does not last forever は部分否定的に「いつまでも続くわけではない」。if they do something about it の it は boredom。',
     'criteria': [('What children need を「子どもに必要なもの（こと）」と訳している', 5),
                  ('not A but B の構造を正しく訳している', 5),
                  ('the chance to find out that ～ を「～と知る（分かる）機会」と訳している', 5),
                  ('boredom does not last forever if they do something about it を正しく訳している', 5)]},
    {'label': '問7', 'kind': '内容理解（感想文の空所）', 'type': 'tfill', 'points': 20, 'nums': [5, 6, 7, 8],
     'answers': ['エ', 'オ', 'ア', 'ウ'],
     'stem': '次の英文は，本文を読んだ高校生が書いた感想である。空所（　⑤　）〜（　⑧　）に入る最も適切な語を，(ア)〜(ク)の中からそれぞれ1つ選び，その記号を書きなさい。'
             '同じ記号は1度しか使えない。',
     'text': ['This passage taught me that boredom works like a {c5} which tells us that our mind needs something to do. '
              'In Ms. Moreno’s class, the children {c6} about having no plan at first, but later they created many things. '
              'I also learned that boredom is not always good: if it continues for a {c7} time, it can be harmful. '
              'From now on, I would like to {c8} my free time in my own way instead of always looking at a screen.'],
     'choices': [('ア', 'long'), ('イ', 'reward'), ('ウ', 'fill'), ('エ', 'signal'),
                 ('オ', 'complained'), ('カ', 'short'), ('キ', 'avoid'), ('ク', 'laughed')],
     'expl': '⑤ 第2段落「退屈は空腹とよく似た合図」→ signal。⑥ 第5段落「最初の数週間は不満でいっぱい」→ complained。'
             '⑦ 第7段落「長期間の退屈はストレスなどと結びつく」→ long。⑧ 第7段落「自分のやり方で埋めてよいすき間」→ fill。（各5点）'},
]}
