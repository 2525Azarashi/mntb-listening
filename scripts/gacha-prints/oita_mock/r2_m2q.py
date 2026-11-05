# -*- coding: utf-8 -*-
# 第2回 〔2〕 医学部 設問（36点）
M2Q = {'questions': [
    {'label': '問1', 'kind': '英文の完成（3語以上）', 'type': 'en', 'points': 6, 'min': 3,
     'stem': '第2段落の内容に合うように，次の英文の下線部に入る語句を英単語3語以上で書きなさい。{br}'
             'When patients do not take their medicine, their illnesses may get worse and they may ＿＿＿＿＿＿＿＿.',
     'answers': ['have to go into hospital', 'end up in hospital', 'need to stay in hospital'],
     'expl': '第2段落最終文 illnesses which could have been controlled become worse, and patients end up in hospital が根拠。'
             'may のあとなので動詞の原形で始める（end up in hospital / have to go into hospital）。',
     'criteria': [('「入院することになる」という内容になっている', 4),
                  ('助動詞 may に続く形（動詞の原形）で，文法的に正しい（3語以上）', 2)]},
    {'label': '問2', 'kind': '理由説明（日本語）', 'type': 'ja', 'points': 6, 'lines': 2,
     'stem': '第4段落で，高血圧の患者が毎日薬を飲む理由に疑問をもつことがあるのはなぜか。その理由を本文に即して日本語で説明しなさい。',
     'answer': '高血圧にはふつう症状がないので，患者はどこも悪くないように感じてしまうから。',
     'expl': 'High blood pressure, for example, usually has no symptoms, so a patient may wonder why … when nothing seems to be wrong. が根拠。'
             '「症状がない」と「悪いところがないように思える」の2点を書く。',
     'criteria': [('高血圧にはふつう症状がないことを書いている', 4),
                  ('そのため，どこも悪くないように感じることを書いている', 2)]},
    {'label': '問3', 'kind': '内容説明（25字以内×3）', 'type': 'ja', 'points': 12, 'lines': 3,
     'stem': '第4段落と第5段落から，患者が薬を飲むのをやめてしまう理由を3つ，それぞれ25字以内の日本語で書きなさい（句読点も1字に数える）。'
             '解答欄には(1)〜(3)の番号をつけて書くこと。',
     'answer': '(1)体調がよく，飲む必要を感じないから。(2)ネットの情報などで副作用を恐れるから。(3)費用の負担が大きく，量を減らすから。',
     'expl': '第4段落：元気だと感じる／副作用への恐れ／費用。第5段落：薬が必要な理由を理解していない（質問できなかった）。'
             'この4つのうち3つが書けていればよい。「単に忘れた」は第3段落でごく少数とされているので，主な理由としては誤り。',
     'criteria': [('元気だと感じる・副作用への恐れ・費用・必要性を理解していない のうち1つ目（25字以内）', 4),
                  ('同じく2つ目（25字以内）', 4), ('同じく3つ目（25字以内）', 4)]},
    {'label': '問4', 'kind': '下線部和訳', 'type': 'ja', 'points': 12, 'ref': 'A', 'lines': 3,
     'stem': '下線部(A)を和訳しなさい。',
     'answer': '患者は処方せんを手にしてはいても，その薬が何をするのか，飲むのをやめたら何が起こりうるのかをはっきり分からないまま診察室を出ることが多い。',
     'expl': 'with a prescription in their hand「処方せんを手にして」と but without a clear idea of ～「～がはっきり分からないまま」が対比になっている。'
             'idea of のあとに what the drug does と what might happen if ～ の2つの間接疑問が or で並ぶ。might は「起こるかもしれない」。',
     'criteria': [('leave the room with a prescription in their hand を正しく訳している', 3),
                  ('but without a clear idea of ～ を「～がはっきり分からないまま」と訳している', 4),
                  ('what the drug does と what might happen if they stop taking it を正しく訳している', 5)]},
]}
