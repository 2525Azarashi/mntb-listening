# -*- coding: utf-8 -*-
# 第3回 〔2〕 医学部 設問（36点）
M2Q = {'questions': [
    {'label': '問1', 'kind': '英文の完成（3語以上）', 'type': 'en', 'points': 6, 'min': 3,
     'stem': '第4段落の内容に合うように，次の英文の下線部に入る語句を英単語3語以上で書きなさい。{br}'
             'Antibiotics do not help patients with a cold or the flu, because these illnesses ＿＿＿＿＿＿＿＿.',
     'answers': ['are caused by viruses', 'are caused by a virus', 'come from viruses'],
     'expl': '第4段落第2文 these illnesses are caused by viruses, on which antibiotics have no effect at all が根拠。'
             '主語 these illnesses は複数なので are caused by viruses。',
     'criteria': [('「ウイルスによって引き起こされる」という内容になっている', 4),
                  ('主語に合った動詞の形（受け身など）で，文法的に正しい（3語以上）', 2)]},
    {'label': '問2', 'kind': '理由説明（日本語）', 'type': 'ja', 'points': 6, 'lines': 2,
     'stem': '第6段落で，製薬会社が新しい抗生物質の開発に積極的でないのはなぜか。その理由を本文に即して日本語で説明しなさい。',
     'answer': '開発に長い年月と多額の費用がかかるのに，患者は短期間しか飲まず，新薬は重症例のために取っておかれるので，利益がほとんど出ないから。',
     'expl': 'Developing a drug takes many years and costs a great deal of money, and companies earn little from antibiotics, because … が根拠。'
             '「開発にお金と時間がかかる」と「利益が少ない（その理由：短期間の服用・新薬は温存される）」の2点を書く。',
     'criteria': [('開発に長い年月と多額の費用がかかることを書いている', 2),
                  ('利益がほとんど出ないこと（短期間しか飲まない・新薬は重症例のために取っておかれる）を書いている', 4)]},
    {'label': '問3', 'kind': '内容説明（25字以内×3）', 'type': 'ja', 'points': 12, 'lines': 3,
     'stem': '第4段落から，抗生物質が不必要に使われてしまう例を3つ，それぞれ25字以内の日本語で書きなさい（句読点も1字に数える）。'
             '解答欄には(1)〜(3)の番号をつけて書くこと。',
     'answer': '(1)風邪などウイルスの病気で抗生物質を求める。(2)患者を満足させるため医師が処方してしまう。(3)家畜の成長を速めるために大量に与える。',
     'expl': '第4段落：風邪やインフルエンザで患者が求める／医師が時間不足や患者を満足させたい気持ちから処方する／具合がよくなるとすぐ飲むのをやめる／家畜に成長促進のため与える。'
             'このうち3つが書けていればよい（「よくなるとすぐ飲むのをやめる」も正解）。',
     'criteria': [('患者が求める・医師が処方してしまう・途中でやめる・家畜に与える のうち1つ目（25字以内）', 4),
                  ('同じく2つ目（25字以内）', 4), ('同じく3つ目（25字以内）', 4)]},
    {'label': '問4', 'kind': '下線部和訳', 'type': 'ja', 'points': 12, 'ref': 'A', 'lines': 3,
     'stem': '下線部(A)を和訳しなさい。',
     'answer': '抗生物質が使われる回数が多ければ多いほど，耐性菌が広がる機会は多くなる。',
     'expl': 'The 比較級 ～, the 比較級 …「～すればするほど…」。後半は there are more chances for resistant bacteria to spread が元の形で，'
             'for resistant bacteria は to spread の意味上の主語「耐性菌が広がる」。chances は「機会・可能性」。',
     'criteria': [('The more often antibiotics are used を「抗生物質が使われる回数が多いほど」と訳している', 4),
                  ('The 比較級, the 比較級 の構文を「～すればするほど…」と正しく訳している', 4),
                  ('chances for resistant bacteria to spread を「耐性菌が広がる機会（可能性）」と訳している', 4)]},
]}
