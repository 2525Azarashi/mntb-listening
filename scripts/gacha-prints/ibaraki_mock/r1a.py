# -*- coding: utf-8 -*-
# 茨城大学 第1回 Ⅰ・Ⅱ（書き下ろし。人物・団体・地名・調査・数値は架空）
P1 = {
    'points': 50,
    'title': 'The Hidden Work of Small Talk',
    'passage': [
        "Many people think of small talk as a waste of time. Conversations about the weather, the weekend, or the traffic on the way "
        "to work seem to contain little real information, and busy workers may feel that they should skip them and get straight to "
        "business. {u1|Yet researchers who study workplaces have begun to suspect that these brief exchanges do far more than fill silence.}",
        "In a study carried out at several offices in the city of Hartwell, employees were asked to keep a short diary for three weeks. "
        "When each working day was over, they recorded how many casual conversations they had had with colleagues and how they felt "
        "about their work. On days when people reported more small talk, they also tended to report more positive feelings, such as "
        "being cheerful and relaxed. Interestingly, they did not get less work done on those days. {u2|The few minutes spent chatting "
        "seemed to be repaid by a better mood that lasted for hours.}",
        "Small talk also helps people build trust. When we chat with someone about unimportant topics, we pick up small facts about "
        "their life: that they have a young daughter, that they enjoy fishing, that they are worried about a sick parent. Such knowledge "
        "makes it easier to understand their behavior later. A colleague who seems unusually short-tempered one morning may simply be "
        "exhausted after a sleepless night with a baby. {u3|Without the information gathered through casual conversation, we might "
        "interpret the same behavior as rudeness and respond with anger.}",
        "The value of small talk became especially clear when many companies moved to remote work. Meetings held online usually begin "
        "exactly on time and focus strictly on the agenda. There is no chance to bump into someone in the corridor or to chat while "
        "waiting for coffee. Many workers reported that, although they remained productive, they felt increasingly isolated and found it "
        "harder to ask colleagues for help. Some managers responded by scheduling short online coffee breaks with no fixed topic. Others "
        "asked teams to spend the first five minutes of each meeting talking about anything except work.",
        "Of course, not everyone enjoys small talk. Some people find it tiring or even stressful, especially with people they hardly "
        "know. {u4|It need not be long or clever, however; what matters is that it signals a willingness to treat the other person as a "
        "human being rather than simply as a colleague with a job to do.} A short question about someone’s weekend, asked with genuine "
        "interest, may be among the cheapest and most effective investments a workplace can make.",
    ],
    'questions': [
        {'ref': 1, 'kind': '下線部和訳', 'points': 12,
         'stem': '下線部(1)を和訳せよ。',
         'answer': 'しかし，職場を研究する研究者たちは，こうした短いやりとりが沈黙を埋めるよりもはるかに多くのことをしているのではないかと考え始めている。',
         'expl': 'suspect that ~ は「〜ではないかと思う」（doubt「〜ではないと思う」と区別する）。these brief exchanges は第1段落の天気や週末の会話（small talk）を指す。'
                 'do far more than fill silence は far が比較級を強めて「沈黙を埋めるよりはるかに多くのことをする」。',
         'criteria': [('researchers who study workplaces「職場を研究する研究者」', 2), ('have begun to suspect that ~「〜ではないかと考え始めている」', 4),
                      ('these brief exchanges「こうした短いやりとり」', 2), ('do far more than fill silence「沈黙を埋めるよりはるかに多くのことをする」', 4)]},
        {'ref': 2, 'kind': '下線部の内容説明（調査と関連づけて）', 'points': 12, 'lines': 4,
         'stem': '下線部(2)はどういうことか。Hartwell の調査の方法と結果をふまえて説明せよ。',
         'answer': '3週間，社員に毎日，同僚と何回雑談したかと仕事についての気分を日記に書いてもらったところ，雑談の多い日ほど明るくくつろいだ気分になっており，'
                   'しかもその日の仕事量は減っていなかった。つまり，雑談に使った数分間は，何時間も続くよい気分という形で十分に取り戻されているということ。',
         'expl': 'be repaid は「（使ったものが）返ってくる・報われる」。方法（keep a short diary / how many casual conversations / how they felt）と，'
                 '結果（more positive feelings）、さらに did not get less work done（仕事は減らなかった）を書くと「元が取れている」ことがはっきりする。',
         'criteria': [('方法：3週間，雑談の回数と気分を日記に記録', 3), ('雑談の多い日ほど明るくくつろいだ気分', 3),
                      ('仕事の量は減らなかった', 3), ('雑談の数分が何時間も続くよい気分で報われる', 3)]},
        {'ref': 3, 'kind': '下線部の内容説明（具体例を用いて）', 'points': 13, 'lines': 4,
         'stem': '下線部(3)はどういうことか。第3段落の具体例を用いて説明せよ。',
         'answer': '雑談を通して，同僚に幼い子どもがいるといった私生活の小さな事実を知っていれば，ある朝その人がいつになく怒りっぽくても，赤ちゃんのせいで眠れず疲れているだけだと理解できる。'
                   'そうした情報がなければ，同じふるまいを失礼な態度だと受け取り，怒って言い返してしまうかもしれないということ。',
         'expl': 'the same behavior は直前の unusually short-tempered one morning を指す。interpret A as B「A を B と解釈する」。'
                 '雑談で得た情報（幼い娘がいる・眠れない夜）があるかないかで，同じ行動の受け取り方が変わるという対比で書く。',
         'criteria': [('雑談で同僚の私生活の小さな事実を知る（例：幼い子どもがいる）', 3), ('例：ある朝いつになく怒りっぽい', 3),
                      ('情報があれば：寝不足で疲れているだけと理解できる', 3), ('情報がなければ：失礼だと解釈し怒って応じる', 4)]},
        {'ref': 4, 'kind': '下線部和訳（It の内容を明らかに）', 'points': 13,
         'stem': '下線部(4)を和訳せよ。その際，It が何を表しているかがわかるように訳すこと。',
         'answer': '雑談は長くも気のきいたものでもある必要はない。大切なのは，相手を単にするべき仕事をもった同僚としてではなく，一人の人間として扱おうとする気持ちを，雑談が示すということである。',
         'expl': 'It は前文の small talk。need not be ~「〜である必要はない」。what matters is that ~「大切なのは〜ということだ」。'
                 'signals a willingness to ~「〜しようとする気持ちを示す」。treat ～ as …「～を…として扱う」に rather than (simply) as ―「―としてではなく」が加わった形。',
         'criteria': [('It ＝ 雑談（small talk）を明示', 3), ('need not be long or clever「長くも気がきいている必要もない」', 3),
                      ('what matters is that ~ / signals a willingness to ~', 3),
                      ('treat ... as a human being rather than simply as a colleague with a job to do', 4)]},
    ],
    'translation': [
        '多くの人は雑談を時間のむだだと考えている。天気や週末，通勤途中の渋滞についての会話には本当の情報がほとんど含まれていないように見え，'
        '忙しい働き手は，そんな会話は飛ばしてすぐ本題に入るべきだと感じるかもしれない。しかし，職場を研究する研究者たちは，こうした短いやりとりが沈黙を埋めるよりもはるかに多くのことをしているのではないかと考え始めている。',
        'ハートウェル市のいくつかの職場で行われた調査で，社員たちは3週間，短い日記をつけるよう求められた。その日の勤務が終わると，同僚と何回くだけた会話をしたか，そして仕事についてどう感じたかを記録したのである。'
        '雑談が多かったと報告した日には，明るい，くつろいでいるといった前向きな気持ちも報告される傾向があった。興味深いことに，そうした日に仕事の量が減ることはなかった。'
        'おしゃべりに使った数分間は，何時間も続くよい気分によって報われているようだった。',
        '雑談は，人どうしが信頼を築くのにも役立つ。大事ではない話題について誰かとおしゃべりすると，その人の生活についての小さな事実を知ることになる。幼い娘がいるとか，釣りが好きだとか，病気の親のことを心配しているといったことだ。'
        'そうした知識があると，後でその人の行動を理解しやすくなる。ある朝いつになく怒りっぽく見える同僚は，赤ちゃんのせいで眠れない夜を過ごし，疲れきっているだけかもしれない。'
        'くだけた会話を通して集めた情報がなければ，私たちは同じふるまいを無礼だと解釈し，怒って応じてしまうかもしれない。',
        '雑談の価値は，多くの会社が在宅勤務に移ったとき，とりわけはっきりした。オンラインで行う会議はたいてい時間ちょうどに始まり，議題だけに集中する。廊下で誰かとばったり会ったり，コーヒーを待ちながらおしゃべりしたりする機会はない。'
        '多くの働き手が，仕事ははかどっているものの，しだいに孤立感が強まり，同僚に助けを求めにくくなったと報告した。これに対して，決まった話題のない短いオンラインのコーヒー休憩を予定に組み入れる管理職もいた。'
        'また，会議のたびに最初の5分間は仕事以外なら何について話してもよいことにしたチームもあった。',
        'もちろん，誰もが雑談を楽しめるわけではない。特にほとんど知らない相手との雑談は疲れる，あるいはストレスになると感じる人もいる。'
        'しかし，雑談は長くも気のきいたものでもある必要はない。大切なのは，相手を単にするべき仕事をもった同僚としてではなく，一人の人間として扱おうとする気持ちを，雑談が示すということである。'
        '心からの関心をもってたずねる，週末についてのちょっとした質問は，職場ができる最も安上がりで最も効果的な投資の一つかもしれない。',
    ],
    'vocab': [('small talk', '雑談'), ('get straight to business', 'すぐ本題に入る'), ('suspect that ~', '〜ではないかと思う'), ('exchange', 'やりとり'),
              ('colleague', '同僚'), ('casual', 'くだけた'), ('tend to do', '〜する傾向がある'), ('repay', '報いる・返す'), ('mood', '気分'),
              ('pick up', '（情報などを）得る'), ('short-tempered', '怒りっぽい'), ('exhausted', '疲れきった'), ('interpret A as B', 'A を B と解釈する'),
              ('rudeness', '無礼'), ('remote work', '在宅勤務・リモートワーク'), ('agenda', '議題'), ('bump into ~', '〜にばったり会う'),
              ('isolated', '孤立した'), ('willingness', '進んで〜する気持ち'), ('genuine', '心からの'), ('investment', '投資')],
}

P2 = {
    'points': 50,
    'title': 'Finding Our Way',
    'passage': [
        "Before satellite navigation became common, finding your way in an unfamiliar city took effort. You studied a paper map, "
        "remembered landmarks, and perhaps asked strangers for directions. Today, a voice from a phone tells us exactly when to turn left "
        "or right. {u1|This is undoubtedly convenient, but some scientists worry that by handing the task over to machines, we may be "
        "losing a skill that human brains have developed over thousands of years.}",
        "The part of the brain most closely linked to navigation is the hippocampus*. Researchers at a university in the city of Calloway "
        "compared delivery drivers who had memorized the complicated streets of a large city with people of a similar age who did office "
        "work. Brain scans showed that this region was larger in the drivers, and the longer they had worked, the larger it tended to be. "
        "{u2|This suggested that the brain, like a muscle, changes according to the demands we place on it.}",
        "If using the brain for navigation strengthens it, does relying on devices weaken it? The evidence so far is mixed, but several "
        "experiments point in the same direction. In one, volunteers walked through an unfamiliar neighborhood twice, once following a "
        "phone and once using a paper map. Afterwards, they were asked to draw the route and to point toward the place where they had "
        "started. When they had followed the phone, their drawings were less accurate and they were more often wrong about the direction "
        "of the starting point. {u3|They had reached the destination, but they had not really learned where they were.}",
        "One reason may be that satellite navigation encourages us to pay attention to the screen rather than to our surroundings. A "
        "person with a paper map must constantly compare the map with the real world: a church on the corner, a river on the left, a hill "
        "in the distance. This comparison builds a mental picture of the area that can be used again later. A person who simply follows "
        "instructions has no need for such a picture, so the brain does not bother to make one.",
        "None of this means that we should throw away our phones. Navigation apps save time and reduce stress, especially in emergencies. "
        "Researchers suggest, however, a few simple habits for keeping our sense of direction alive: looking at the whole route before "
        "setting off, noticing landmarks along the way, and occasionally walking a familiar journey without any help. {u4|The aim is not "
        "to reject technology but to make sure that it remains a tool that serves us, rather than a replacement for abilities we would be "
        "sorry to lose.}",
    ],
    'notes': [('hippocampus', '海馬（記憶や空間の把握に関わる脳の部位）')],
    'questions': [
        {'ref': 1, 'kind': '下線部の内容説明', 'points': 12, 'lines': 4,
         'stem': '下線部(1)で，一部の科学者たちが心配しているのはどのようなことか。the task と a skill がそれぞれ何を指すかを明らかにして説明せよ。',
         'answer': '知らない町で道を見つけるという仕事を，携帯電話などの機械に任せてしまうことで，人間の脳が何千年もかけて発達させてきた，'
                   '自分で道を見つけ出す能力（方向感覚）を失いつつあるのではないかということ。',
         'expl': 'the task は第1段落の finding your way in an unfamiliar city。handing ~ over to machines「〜を機械に引き渡す」。'
                 'a skill は「地図を見て目印を覚え，道を見つける力」。may be losing は進行形で「失いつつあるかもしれない」。',
         'criteria': [('the task：知らない町で道を見つけること', 3), ('それを機械（携帯電話のナビ）に任せる', 3),
                      ('a skill：自分で道を見つける能力・方向感覚', 3), ('脳が何千年もかけて発達させた力を失いつつある', 3)]},
        {'ref': 2, 'kind': '下線部和訳', 'points': 12,
         'stem': '下線部(2)を和訳せよ。',
         'answer': 'このことは，脳は筋肉と同じように，私たちが脳に課す負担に応じて変化するということを示していた。',
         'expl': 'This は直前の調査結果（運転手の海馬が大きく，勤務年数が長いほど大きい）。like a muscle は挿入で「筋肉のように」。'
                 'according to ~「〜に応じて」。the demands we place on it は demands のあとに関係代名詞が省略され，place demands on ~「〜に負担を課す」の形。it は the brain。',
         'criteria': [('This suggested that ~「このことは〜を示していた」', 2), ('like a muscle「筋肉のように」', 2),
                      ('changes according to ~「〜に応じて変化する」', 3), ('the demands we place on it「私たちが脳に課す負担・要求」（関係詞の省略）', 5)]},
        {'ref': 3, 'kind': '下線部の内容説明（実験と関連づけて）', 'points': 13, 'lines': 5,
         'stem': '下線部(3)はどういうことか。第3段落の実験の方法と結果にふれながら説明せよ。',
         'answer': '参加者に知らない地域を，一度は携帯電話の案内に従って，一度は紙の地図を使って歩いてもらい，その後で道順を描かせ，出発点の方向を指させた。'
                   '電話に従ったときは，描いた道順が不正確で，出発点の方向もまちがえることが多かった。つまり，案内に従って目的地には着けても，自分がどこにいるのかという土地の様子は頭に入っていなかったということ。',
         'expl': '方法（twice, once following a phone and once using a paper map / draw the route / point toward the place）と結果（less accurate / more often wrong）を書いたうえで，'
                 '下線部の対比 reached the destination ⇔ had not really learned where they were を説明する。',
         'criteria': [('方法：電話の案内と紙の地図で一度ずつ歩く', 3), ('その後，道順を描き出発点の方向を指す', 3),
                      ('電話のときは道順が不正確・方向をまちがえる', 3), ('目的地には着けても，自分の位置や土地の様子は覚えていない', 4)]},
        {'ref': 4, 'kind': '下線部和訳', 'points': 13,
         'stem': '下線部(4)を和訳せよ。',
         'answer': '目的は，科学技術を拒むことではなく，それが，失えば残念に思うような能力の代わりになるものではなく，私たちの役に立つ道具であり続けるようにすることである。',
         'expl': 'not A but B「A ではなく B」。make sure that ~「必ず〜であるようにする」。remains a tool that serves us「私たちに仕える（役立つ）道具であり続ける」。'
                 'rather than a replacement for ~「〜の代わりになるものではなく」。abilities we would be sorry to lose は関係詞の省略で，would は「（もし失ったら）〜だろう」。',
         'criteria': [('not to reject technology but to ~「技術を拒むことではなく〜すること」', 3), ('make sure that it remains a tool that serves us', 4),
                      ('rather than a replacement for ~「〜の代わりではなく」', 3), ('abilities we would be sorry to lose「失えば残念に思う能力」', 3)]},
    ],
    'translation': [
        '衛星ナビゲーションが普及する前は，知らない町で道を見つけるには苦労が必要だった。紙の地図をじっくり見て，目印を覚え，ときには見知らぬ人に道をたずねた。'
        '今日では，携帯電話から聞こえる声が，いつ左や右に曲がればよいかを正確に教えてくれる。'
        'これはまちがいなく便利だが，その仕事を機械に任せることで，私たちは人間の脳が何千年もかけて発達させてきた能力を失いつつあるのではないかと心配する科学者もいる。',
        '脳の中で道を見つけることと最も深く結びついている部位は海馬である。キャロウェイ市の大学の研究者たちは，大都市の複雑な通りを覚えた配達の運転手と，事務の仕事をしている同じくらいの年齢の人々を比べた。'
        '脳の画像からは，この部位が運転手のほうで大きく，しかも勤務年数が長いほど大きい傾向があることがわかった。'
        'このことは，脳は筋肉と同じように，私たちが脳に課す負担に応じて変化するということを示していた。',
        '道を見つけるために脳を使うことで脳が強くなるのなら，機器に頼ると脳は弱くなるのだろうか。今のところ証拠はまちまちだが，いくつかの実験は同じ方向を指している。'
        'ある実験では，参加者たちが知らない地域を2回歩いた。1回は携帯電話に従い，もう1回は紙の地図を使った。その後，彼らは道順を描き，出発した場所の方向を指すよう求められた。'
        '電話に従ったときには，描いた図はより不正確で，出発点の方向をまちがえることもより多かった。彼らは目的地に着きはしたが，自分がどこにいるのかを本当に覚えたわけではなかったのである。',
        '理由の一つは，衛星ナビゲーションが，周りの様子よりも画面に注意を向けるよう私たちを促すことかもしれない。紙の地図を持った人は，地図と現実の世界をたえず見比べなければならない。'
        '角にある教会，左手の川，遠くの丘といった具合だ。この見比べが，後でまた使える，その地域の頭の中の地図を作り上げる。指示に従うだけの人にはそのような地図は必要ないので，脳はわざわざ作ろうとしないのである。',
        'これは，携帯電話を捨てるべきだということではまったくない。ナビのアプリは時間を節約し，特に緊急のときにはストレスを減らしてくれる。'
        'しかし研究者たちは，方向感覚を保つためのいくつかの簡単な習慣を勧めている。出発する前に道順全体を見ておくこと，途中の目印に気づくこと，そしてときどき慣れた道を何の助けも借りずに歩くことである。'
        '目的は，科学技術を拒むことではなく，それが，失えば残念に思うような能力の代わりになるものではなく，私たちの役に立つ道具であり続けるようにすることである。',
    ],
    'vocab': [('satellite navigation', '衛星ナビゲーション'), ('unfamiliar', 'よく知らない'), ('landmark', '目印'), ('directions', '道順'),
              ('undoubtedly', 'まちがいなく'), ('hand A over to B', 'A を B に引き渡す'), ('memorize', '覚える'), ('complicated', '複雑な'),
              ('scan', '（脳などの）画像検査'), ('according to ~', '〜に応じて'), ('place demands on ~', '〜に負担を課す'),
              ('rely on ~', '〜に頼る'), ('mixed', 'まちまちの'), ('accurate', '正確な'), ('destination', '目的地'), ('surroundings', '周囲の様子'),
              ('constantly', 'たえず'), ('bother to do', 'わざわざ〜する'), ('emergency', '緊急事態'), ('set off', '出発する'), ('reject', '拒む'),
              ('replacement', '代わりのもの')],
}
