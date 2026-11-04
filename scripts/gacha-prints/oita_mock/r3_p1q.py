# -*- coding: utf-8 -*-
# 第3回 〔1〕 設問（基準配点 100：教育学部版。経済 ×1.2・医 ×0.4）
P1Q = {'questions': [
    {'label': '問1', 'kind': '空所補充（英語1語）', 'type': 'fill', 'points': 20, 'nums': [1, 2, 3, 4],
     'answers': ['from', 'in', 'off', 'spent'],
     'stem': '本文中の空所（　①　）〜（　④　）に入る最も適切な英語を，それぞれ1語で書きなさい。',
     'expl': '① the light from the ground「地上からの光」。空は変わらず，地上の明かりが変わったという対比。'
             '② in the wrong direction「間違った方向に」。方向は in で表す（×to the direction）。'
             '③ switch off「（明かりを）消す」。the moment ～「～したとたんに」。'
             '④ the money it spent on electricity「電気代に使っていたお金」。spend A on B。目的格の関係代名詞が省略されている。（各5点）'},
    {'label': '問2', 'kind': '下線部和訳', 'type': 'ja', 'points': 20, 'ref': 'A',
     'stem': '下線部(A)を日本語に訳しなさい。',
     'answer': 'その大部分の人は，自分が何を失ったのかに気づいたことがない。星でいっぱいの空は，彼らが一度も体験したことのないものだからである。',
     'expl': 'Most of them の them は直前の「天の川が見えない人々」。have never noticed は経験の現在完了「一度も気づいたことがない」。'
             'what they have lost は間接疑問（または関係代名詞）で「自分が何を失ったのか（失ったもの）」。'
             'because 以下の something they have never experienced は，something のあとに目的格の関係代名詞が省略されている。',
     'criteria': [('Most of them have never noticed を「その大部分は一度も気づいたことがない」と訳している', 5),
                  ('what they have lost を「何を失ったのか（失ったもの）」と訳している', 5),
                  ('a sky full of stars を「星でいっぱいの空」と訳している', 5),
                  ('something they have never experienced を「一度も体験したことのないもの」と訳し，because の理由関係を示している', 5)]},
    {'label': '問3', 'kind': '語義', 'type': 'mc', 'points': 5, 'ref': 'B', 'answer': 'エ',
     'stem': '下線部(B)の語に最も意味の近いものを，(ア)〜(エ)から1つ選び，記号で答えなさい。',
     'choices': [('ア', 'refused'), ('イ', 'risen'), ('ウ', 'changed direction'), ('エ', 'gone down')],
     'expl': 'decline は「（数・量が）減る」。直前で昆虫が街灯で死ぬ話をしているので「減った」理由と分かる。'
             'ア refuse「断る」は decline の別の意味（申し出を断る）だが，ここでは数について述べているので合わない。'},
    {'label': '問4', 'kind': '下線部和訳', 'type': 'ja', 'points': 20, 'ref': 'C',
     'stem': '下線部(C)を日本語に訳しなさい。',
     'answer': 'その結果，寝つきにくくなることがあり，何年にもわたって睡眠が不足すると，さまざまな健康上の問題の危険が高まるかもしれない。',
     'expl': 'it can become harder to fall asleep の it は形式主語で，to fall asleep「寝つくこと」が真主語。can は「～することがある」（可能性）。'
             'over many years「何年にもわたって」。poor sleep は無生物主語なので「睡眠不足は～」または「睡眠が不足すると～」と訳す。'
             'a number of ～「いくつもの・さまざまな～」。',
     'criteria': [('As a result と it can become harder to fall asleep（形式主語）を正しく訳している', 5),
                  ('over many years を「何年にもわたって」と訳している', 5),
                  ('poor sleep may increase the risk of ～ を「睡眠不足は～の危険を高めるかもしれない」と訳している', 5),
                  ('a number of health problems を「さまざまな（いくつもの）健康上の問題」と訳している', 5)]},
    {'label': '問5', 'kind': '空所補充（つなぎの語句）', 'type': 'mc', 'points': 5, 'answer': 'イ',
     'stem': '本文中の空所（　E　）に入る最も適切なものを，(ア)〜(エ)から1つ選び，記号で答えなさい。',
     'choices': [('ア', 'However'), ('イ', 'For example'), ('ウ', 'In contrast'), ('エ', 'Nevertheless')],
     'expl': '前の文「多くの街灯は光を横や上に送っている（光の使い方が問題）」の具体的な解決策として，「街灯の上部を覆う」例を挙げている。For example「たとえば」。'
             'However・Nevertheless・In contrast はいずれも前の内容と対立する内容を導く。'},
    {'label': '問6', 'kind': '内容説明（30字以内）', 'type': 'ja', 'points': 15, 'ref': 'D', 'limit': 30,
     'stem': '下線部(D)のように言えるのはなぜか。ローザの言葉をもとに，30字以内の日本語で説明しなさい。句読点も1字に数える。',
     'answer': '星空は誰のものでもなく，次の世代に残すべきものだから。',
     'expl': '直後のローザの言葉「星は誰のものでもない」「不注意だと次の世代から星を奪ってしまう」が根拠。'
             '「誰のものでもない（皆で共有する）」と「次の世代に受け継ぐ（奪ってはならない）」の2点を入れる。',
     'criteria': [('星空が誰のものでもない（皆のものである）ことに触れている', 5),
                  ('次の世代に残す（奪ってはならない）ものであることに触れている', 5),
                  ('理由を答える形で30字以内にまとめている', 5)]},
    {'label': '問7', 'kind': '内容理解（空所選択）', 'type': 'tfill', 'points': 15, 'nums': [5, 6, 7],
     'answers': ['ウ', 'カ', 'ア'],
     'stem': '次の英文は本文の要約である。空所（　⑤　）〜（　⑦　）に入る最も適切な語句を，(ア)〜(カ)からそれぞれ1つ選び，記号で答えなさい。'
             'ただし，同じ記号を2度以上使ってはならない。',
     'text': ['Artificial light at night hides the stars and also harms animals and human {c5}. '
              'However, light pollution can be reduced easily, because the main problem is {c6} light is used. '
              'In Kerrow, new street lamps helped the town {c7} money without increasing crime, and the night sky became visible again.'],
     'choices': [('ア', 'save'), ('イ', 'spend'), ('ウ', 'health'), ('エ', 'crime'), ('オ', 'how much'), ('カ', 'how')],
     'expl': '⑤ 第4段落：体内時計が乱れ，睡眠不足が健康の危険を高める → health。'
             '⑥ 第5段落「問題は光の量ではなく使い方」→ how（how much は「量」なので逆）。'
             '⑦ 第6段落「電気代の約3分の1を節約した」→ help 人 do の形で save。（各5点）'},
]}
