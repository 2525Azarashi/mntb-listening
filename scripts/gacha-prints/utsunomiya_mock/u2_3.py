# -*- coding: utf-8 -*-
"""第2回 第3問 意見を述べる英作文（約150語）・第4問 会話文の完成。書き下ろし。調査・団体・数値は架空。"""
ESSAY = {
    'passage': "Last year, the education board of Corvell asked 900 high school students and their parents whether classes should begin at 9:30 a.m. instead of 8:30 a.m. "
               "Many students welcomed the idea, explaining that they often feel sleepy during their first lessons and could concentrate better after more rest. "
               "However, a number of parents worried that a later start would also mean a later finish, leaving less time for club activities, part-time jobs, and homework in the evening. "
               "The board has not yet reached a decision.",
    'passage_ja': 'コーヴェルの教育委員会は昨年，900人の高校生とその保護者に，授業を午前8時30分ではなく午前9時30分に始めるべきかどうかを尋ねた。多くの生徒はこの考えを歓迎し，最初の授業中に眠くなることが多く，もっと休めば集中しやすくなるだろうと説明した。しかし，始業が遅くなれば終業も遅くなり，夕方の部活動やアルバイト，宿題の時間が減ると心配する保護者も少なくなかった。委員会はまだ結論を出していない。',
    'question': 'Do you think high schools should start classes one hour later in the morning? Support your view with reasons.',
    'question_ja': '高校は朝の授業開始を1時間遅らせるべきだと思うか。理由を挙げて意見を説明せよ。',
    'criteria': [('内容：問いに対する立場が明確で，英文の論点を踏まえている', 12),
                 ('理由：理由が2つ程度あり，具体例や説明で支えられている', 12),
                 ('構成：導入・理由・結論の流れがあり，つなぎの語が適切', 6),
                 ('語法・文法：時制・数・冠詞・語順などの誤りが少ない', 7),
                 ('分量：約150語（おおむね130〜170語）で，語数を正しく記入している', 3)],
    'models': [
        ('遅らせるべきだという立場',
         "I think high schools should begin classes an hour later. "
         "The main reason is that teenagers need plenty of sleep. Many of my friends stay up late studying, and they come to school tired. "
         "In the first lesson, some of them can hardly keep their eyes open, so they learn very little. "
         "If classes started at 9:30, students could sleep longer and arrive ready to think. "
         "Another reason is safety and comfort on the way to school. Trains and buses are extremely crowded before 8:30, and in winter it is still dark when some students leave home. "
         "A later start would let them travel at a quieter and brighter time. "
         "Admittedly, the school day would finish later. However, schools could solve this problem by shortening breaks or moving some club activities to weekends. "
         "Overall, I believe students would study more effectively with a later start."),
        ('遅らせるべきではないという立場',
         "In my opinion, high schools should keep their present starting time. "
         "First of all, a later start would push everything else in the day back by an hour. "
         "Students who belong to sports clubs would have to practice until late in the evening, and those with part-time jobs might have to quit their jobs. "
         "They would also have less time for homework and family meals. "
         "Second, I am not sure that starting later would really give students more sleep. "
         "Many teenagers might simply go to bed an hour later and feel just as sleepy as before. "
         "Learning to rise early is a useful habit for adult life, since most companies expect workers to start early. "
         "Instead of changing the timetable, schools could teach students how to manage their time and sleep. "
         "Therefore, I am against a later start."),
    ],
    'models_ja': [
        '私は，高校は授業開始を1時間遅らせるべきだと思う。主な理由は，十代の若者には十分な睡眠が必要だということだ。私の友人の多くは夜遅くまで勉強し，疲れて登校してくる。1時間目には目を開けているのもやっとという人もいて，ほとんど何も学べていない。授業が9時30分に始まれば，生徒はもっと長く眠り，考える準備ができた状態で登校できるだろう。もう一つの理由は，通学の安全と快適さである。8時30分前の電車やバスはひどく混んでおり，冬には家を出るときにまだ暗い生徒もいる。始業が遅くなれば，より空いていて明るい時間に移動できる。たしかに学校の一日の終わりは遅くなる。しかし，学校は休み時間を短くしたり，部活動の一部を週末に移したりしてこの問題を解決できる。全体として，始業が遅いほうが生徒はより効果的に学べると思う。',
        '私の意見では，高校は今の始業時刻を維持すべきである。まず第一に，始業が遅くなれば，一日のほかのすべての予定が1時間後ろにずれる。運動部に入っている生徒は夜遅くまで練習しなければならなくなり，アルバイトをしている生徒は仕事をやめなければならなくなるかもしれない。宿題や家族との食事の時間も減るだろう。第二に，始業を遅らせて本当に生徒の睡眠が増えるのかは疑問である。多くの十代の若者は単に寝る時刻が1時間遅くなるだけで，以前と同じように眠いかもしれない。早起きを身につけることは，ほとんどの会社が早い始業を求める以上，大人の生活に役立つ習慣である。時間割を変えるのではなく，学校は生徒に時間と睡眠の管理のしかたを教えればよい。したがって私は，始業を遅らせることに反対である。',
    ],
    'tips': ['書き出しで立場をはっきり示す。英文の「生徒の意見」と「保護者の心配」を紹介するだけで終わらず，自分はどちらかを明確に書く。',
             '理由は2つにしぼり，The main reason is ~ / Another reason is ~，First of all / Second などで整理する。',
             '反対側の意見に一度触れ（Admittedly, ~. However, ~），解決策や反論を示すと説得力が増す。',
             '時刻は at 9:30 / before 8:30 のように前置詞に注意。「1時間遅く」は an hour later，「1時間ずれる」は push back by an hour のように by を使う。',
             '仮定の話（もし始業が遅くなったら）は If classes started ~, students could ~ と仮定法過去で書くと自然。最後に語数を記入する。'],
}
CONVS = [
    {'label': 'A', 'setting': 'Two friends, Yuna and Leo, are talking during lunch.',
     'lines': [('Yuna', 'Leo, it is Ms. Garvey\'s last week at our school. Have you heard?'),
               ('Leo', None),
               ('Yuna', 'She is moving to a school in another city. I want to give her something from our class.'),
               ('Leo', None),
               ('Yuna', 'That is a nice idea, but we only have four days.'),
               ('Leo', None),
               ('Yuna', 'OK. I will ask everyone in our class this afternoon.'),
               ('Leo', None)],
     'answers': ['Really? That is news to me. Why is she leaving',
                 'How about making a card with a message from each student',
                 'Then let us ask everyone to write their messages by Wednesday',
                 'Thanks. I will buy a large card after school today'],
     'ja': ['ユナ：レオ，今週でガーヴィー先生がこの学校を離れるの。聞いた？', 'レオ：（1）', 'ユナ：別の市の学校に移るんだって。クラスから何か贈りたいな。', 'レオ：（2）', 'ユナ：いい考えだね。でも4日しかないよ。', 'レオ：（3）', 'ユナ：わかった。午後にクラスのみんなに頼んでみる。', 'レオ：（4）'],
     'explain': ['(1)：直後にユナが別の市の学校に移ると理由を説明しているので，知らなかったことを伝え，理由を尋ねる文を入れる。',
                 '(2)：ユナが That is a nice idea と応じているので，具体的な贈り物の案を提案する。How about ~ing? / Why don\'t we ~? などが使える。',
                 '(3)：「4日しかない」という心配に対して，期限を決めるなど時間内に間に合わせる方法を答える。',
                 '(4)：ユナがクラスに頼む役を引き受けたので，自分の担当を伝えたり感謝したりして会話を締めくくる。',
                 '採点：前後と意味がつながり，文法的に正しい英文なら別の表現でもよい。各4点（内容2・語法2）。']},
    {'label': 'B', 'setting': 'A traveler is speaking to a staff member at Dunmore Station.',
     'lines': [('Traveler', 'Excuse me. My train to Ashbury was supposed to leave at ten, but it is not on the board.'),
               ('Staff', None),
               ('Traveler', 'Oh, no. Is there another way to get there this morning?'),
               ('Staff', None),
               ('Traveler', 'Where can I catch it?'),
               ('Staff', None),
               ('Traveler', 'Thank you. Can I use the same ticket on the bus?'),
               ('Staff', None)],
     'answers': ['I am sorry, but that train has been cancelled because of a problem with the line',
                 'Yes. There is a special bus to Ashbury that leaves in twenty minutes',
                 'It stops right outside the main entrance, on your left',
                 'Yes, you can. Just show it to the driver when you get on'],
     'ja': ['旅行者：すみません。アシュベリー行きの電車は10時に出るはずだったのですが，掲示板に出ていません。', '駅員：（1）', '旅行者：えっ，困ったな。午前中にそこへ行くほかの方法はありますか。', '駅員：（2）', '旅行者：どこで乗れますか。', '駅員：（3）', '旅行者：ありがとうございます。同じ切符でバスに乗れますか。', '駅員：（4）'],
     'explain': ['(1)：旅行者が Oh, no. と困っているので，電車が運休になった（遅れている）ことを理由とともに伝える。',
                 '(2)：ほかの行き方を尋ねられているので，代わりの手段（臨時バスなど）を案内する。直後の Where can I catch it? の it が指すものを入れる必要がある。',
                 '(3)：乗り場の場所を具体的に答える。',
                 '(4)：Can I ~? の質問に Yes / No で答え，必要な手続きを補う。',
                 '採点：前後と意味がつながり，文法的に正しい英文なら別の表現でもよい。各4点（内容2・語法2）。']},
]
