# -*- coding: utf-8 -*-
# 第1回 〔2〕 医学部 設問（36点）
M2Q = {'questions': [
    {'label': '問1', 'kind': '英文の完成（3語以上）', 'type': 'en', 'points': 6, 'min': 3,
     'stem': '第2段落の内容に合うように，次の英文の下線部に入る語句を英単語3語以上で書きなさい。{br}'
             'Nurses become less sensitive to alarms because most of the alarms they hear ＿＿＿＿＿＿＿＿.',
     'answers': ['turn out to be unimportant', 'are not important at all', 'do not mean anything'],
     'expl': '第2段落第2文 most of them turn out to be unimportant と，最終文 the brain learns to ignore signals that rarely mean anything が根拠。'
             'most of the alarms が主語なので動詞は複数形で受ける。',
     'criteria': [('「（警報の大部分が）重要でない・意味がない」という内容になっている', 4),
                  ('主語に合った動詞の形で，文法的に正しい（3語以上）', 2)]},
    {'label': '問2', 'kind': '理由説明（日本語）', 'type': 'ja', 'points': 6, 'lines': 2,
     'stem': '第4段落で，重要な警報に何分も誰も来なかったのはなぜか。その理由を本文に即して日本語で説明しなさい。',
     'answer': '担当の看護師がそのとき別の警報への対応に追われていて，しかもその警報の大部分は誤りだったから。',
     'expl': 'In each case, the nurse had been dealing with other alarms at the time, most of which proved to be false. が根拠。'
             '「看護師が怠けていた」のではなく，誤った警報に時間を取られていたことを書く（第2段落の This is not because nurses are careless. とも一致する）。',
     'criteria': [('看護師がそのとき別の警報に対応していたことを書いている', 4),
                  ('その警報の大部分が誤りだったことを書いている', 2)]},
    {'label': '問3', 'kind': '内容説明（25字以内×3）', 'type': 'ja', 'points': 12, 'lines': 3,
     'stem': '第5・6段落で，病院が誤った警報を減らすために行った工夫を3つ，それぞれ25字以内の日本語で書きなさい（句読点も1字に数える）。'
             '解答欄には(1)〜(3)の番号をつけて書くこと。',
     'answer': '(1)警報の基準値を見直し，少し広げた。(2)数秒で正常に戻れば鳴らないよう遅れを設けた。(3)勤務ごとに患者に合わせて基準値を調整した。',
     'expl': '第5段落：基準値を広げる／短い遅れ（delay）を設ける／センサーを毎日交換する。第6段落：患者ごとに設定を話し合って調整する。'
             'この4つのうち3つが書けていればよい（「センサーを毎日交換した」も正解）。「新しい機器を買った」は本文と逆なので誤り。',
     'criteria': [('基準値の拡大・遅れの設定・センサーの毎日交換・患者ごとの調整のうち1つ目（25字以内）', 4),
                  ('同じく2つ目（25字以内）', 4), ('同じく3つ目（25字以内）', 4)]},
    {'label': '問4', 'kind': '下線部和訳', 'type': 'ja', 'points': 12, 'ref': 'A', 'lines': 3,
     'stem': '下線部(A)を和訳しなさい。',
     'answer': '警報を切ることが答えなのではない。目標は，警報が鳴ったときには，それが耳を傾ける価値のあるものになるようにすることである。',
     'expl': 'Turning alarms off は動名詞の主語「警報を切ること」。the goal is to make sure that ～ は「目標は～であることを確実にすることだ」。'
             'it is worth listening to は be worth ～ing「～する価値がある」で，listen to の to を落とさないのがポイント（it が listen to の目的語にあたる）。',
     'criteria': [('Turning alarms off is not the answer を正しく訳している', 3),
                  ('the goal is to make sure that ～ を「目標は～ようにすることだ」と訳している', 4),
                  ('when an alarm sounds, it is worth listening to を「鳴ったときには耳を傾ける価値がある」と訳している', 5)]},
]}
