# -*- coding: utf-8 -*-
# 第1回 〔1〕 設問（基準配点 100：教育学部版。経済 ×1.2・医 ×0.4）
P1Q = {'questions': [
    {'label': '問1', 'kind': '空所補充（英語1語）', 'type': 'fill', 'points': 15, 'nums': [1, 2, 3],
     'answers': ['life', 'themselves', 'less'],
     'stem': '本文中の空所（　①　）〜（　③　）に入る最も適切な英語を，それぞれ1語で書きなさい。',
     'expl': '① bring ～ back to life「～を生き返らせる・再び使えるようにする」。壊れた物を直す場面なので life。'
             '② by oneself「自分で・ひとりで」。主語が some (people) なので themselves。'
             '③ 人々が新製品を買う量を減らせば，店や工場は「より少なく売る」ことになる。sell less。more では論旨が逆になる。'
             '（各5点）'},
    {'label': '問2', 'kind': '下線部和訳', 'type': 'ja', 'points': 20, 'ref': 'A',
     'stem': '下線部(A)を日本語に訳しなさい。',
     'answer': 'しかし，新しい品物の値段が下がるにつれて，古い物を誰かにお金を払って直してもらうより，物を捨てて別の物を買うほうが安くつくことが多くなった。',
     'expl': 'As は「～につれて」（比例・推移）。it は形式主語で，真主語は to throw an item away and buy another。'
             'cheaper ～ than to pay someone to fix the old one の比較の対象（「捨てて買う」と「お金を払って直してもらう」）を取り違えないこと。'
             'pay 人 to do は「人にお金を払って～してもらう」。another は another item の意味。',
     'criteria': [('As ～ fell を「～が下がるにつれて」と訳している', 5),
                  ('it ～ to throw … and buy another の形式主語構文を正しく訳している', 5),
                  ('than to pay someone to fix the old one を「お金を払って直してもらうより」と比較として訳している', 5),
                  ('often became cheaper（安くつくことが多くなった）・however を訳出している', 5)]},
    {'label': '問3', 'kind': '語義', 'type': 'mc', 'points': 5, 'ref': 'B', 'answer': 'ア',
     'stem': '下線部(B)の語に最も意味の近いものを，(ア)〜(エ)から1つ選び，記号で答えなさい。',
     'choices': [('ア', 'repair'), ('イ', 'replace'), ('ウ', 'design'), ('エ', 'sell')],
     'expl': 'mend は「（壊れた物・破れた物を）直す」。直後の「ボタンが取れるとシャツを捨てる」という例からも「直す」と分かる。'
             'replace「取り替える」は直さずに新しい物にすることで，文意と逆になる。'},
    {'label': '問4', 'kind': '下線部和訳', 'type': 'ja', 'points': 20, 'ref': 'C',
     'stem': '下線部(C)を日本語に訳しなさい。',
     'answer': '彼がいちばん楽しいと思うのは修理そのものではなく，その物が見かけほど絶望的ではまったくなかったと持ち主が気づく瞬間である。',
     'expl': 'What he enjoys most が主語（「彼が最も楽しむこと」）。not A but B「A ではなく B」。'
             'the moment when ～ は関係副詞 when で「～する瞬間」。never as hopeless as it seemed は「見かけほど絶望的では決してなかった」。'
             'itself は repair を強調する「～そのもの」。',
     'criteria': [('What he enjoys most を主語として「彼が最も楽しむこと（のは）」と訳している', 5),
                  ('not A but B の構造を正しく訳している', 5),
                  ('the moment when ～ を「～する瞬間」と訳している', 5),
                  ('never as hopeless as it seemed を「見かけほど絶望的ではなかった」と訳している', 5)]},
    {'label': '問5', 'kind': '空所補充（つなぎの語句）', 'type': 'mc', 'points': 5, 'answer': 'ウ',
     'stem': '本文中の空所（　E　）に入る最も適切なものを，(ア)〜(エ)から1つ選び，記号で答えなさい。',
     'choices': [('ア', 'Instead'), ('イ', 'Otherwise'), ('ウ', 'In addition'), ('エ', 'For example')],
     'expl': '前の文は「人と人を結びつける」という社会的な効果，後ろの文は「環境への実際の効果」。別の利点を付け加えているので In addition「それに加えて」。'
             'For example は前の内容の具体例を出すときに使うので合わない。'},
    {'label': '問6', 'kind': '内容説明（30字以内）', 'type': 'ja', 'points': 15, 'ref': 'D', 'limit': 30,
     'stem': '下線部(D)はどういうことか。本文に即して30字以内の日本語で説明しなさい。句読点も1字に数える。',
     'answer': '安い製品にも製造の資源や廃棄のごみという隠れた負担がある。',
     'expl': 'コロン（:）のあとに具体的な中身が書かれている。「作るのに使われたエネルギーと材料」と「捨てられたときに残るごみ」の2点を入れ，'
             'それが値段には表れない（hidden）ことを示す。',
     'criteria': [('製造に使われるエネルギー・材料（資源）に触れている', 5),
                  ('捨てたあとのごみ（廃棄物）に触れている', 5),
                  ('それらが値段に表れず見えにくいという趣旨がある', 5)]},
    {'label': '問7', 'kind': '内容理解（感想文の空所）', 'type': 'tfill', 'points': 20, 'nums': [4, 5, 6, 7],
     'answers': ['エ', 'オ', 'ア', 'ウ'],
     'stem': '次の英文は，本文を読んだ高校生が書いた感想である。空所（　④　）〜（　⑦　）に入る最も適切な語を，(ア)〜(ク)からそれぞれ1つ選び，記号で答えなさい。'
             'ただし，同じ記号を2度以上使ってはならない。',
     'text': ['After reading this passage, I learned that the Repair Café is not just a place where things are fixed for {c4}. '
              'Its main aim is to help people {c5} how objects work, so that they can solve problems by themselves next time. '
              'I was also interested in the point that the café connects different {c6}. '
              'Finally, Martin’s story about the music box shows that some objects have a value that money cannot {c7}.'],
     'choices': [('ア', 'generations'), ('イ', 'forget'), ('ウ', 'buy'), ('エ', 'free'),
                 ('オ', 'understand'), ('カ', 'expensive'), ('キ', 'machines'), ('ク', 'sell')],
     'expl': '④ 第5段落「私たちは無料のサービスではない」→ for free「無料で」。'
             '⑤ 持ち主がそばで見て仕組みを知るのが目的（第5段落）→ understand。'
             '⑥ 10代の若者とおばあさんが互いに学ぶ（第6段落）→ generations「世代」。'
             '⑦ 「これは代わりがきかない」（第8段落）→ money cannot buy「お金では買えない」。（各5点）'},
]}
