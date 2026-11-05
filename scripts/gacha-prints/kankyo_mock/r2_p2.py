# -*- coding: utf-8 -*-
# 第2回 Part 2（英作文）
P2 = {
    'points': 24,
    'lead': '次の問いについて，あなたの考えを英語で書きなさい。150 語以上で書き，最後に使った語数を書くこと。',
    'prompt': 'Some people say that high schools should start classes one hour later in the morning so that students can sleep longer. '
              'Do you agree with this idea? Give reasons and examples to support your opinion.',
    'prompt_ja': '高校は，生徒がもっと長く眠れるように，朝の授業を1時間遅く始めるべきだと言う人がいる。あなたはこの考えに賛成ですか。理由と例を挙げて自分の意見を述べなさい。',
    'model': "I agree that high schools should start classes one hour later. Many teenagers go to bed late because of homework and club "
             "activities, and they often feel sleepy during the first lesson. If school started at nine instead of eight, students would "
             "have more energy and pay more attention in class.\n"
             "In addition, a later start would make mornings safer and calmer. At present, some of my friends skip breakfast and ride "
             "their bikes very fast to arrive on time. With one more hour, they could eat a proper meal and travel to school without "
             "rushing. This would be good for both their health and their safety.\n"
             "Of course, some people worry that a later start means a later finish, which leaves less time for clubs and part-time work. "
             "However, schools could solve this problem by making lunch breaks shorter or by moving some club practice to weekends. "
             "Overall, I believe that a well-rested student learns better, so starting classes later is a change worth trying.",
    'model_ja': [
        '私は，高校は授業を1時間遅く始めるべきだという考えに賛成だ。多くの十代の若者は宿題や部活動のせいで寝るのが遅く，1時間目の授業中に眠く感じることがよくある。もし学校が8時ではなく9時に始まれば，生徒はもっと元気になり，授業にもっと集中できるだろう。',
        'さらに，始まりが遅くなれば朝はより安全で落ち着いたものになるだろう。今は，友人の中に朝食を抜き，間に合うように自転車をとても速く走らせる人もいる。あと1時間あれば，きちんと食事をとり，急がずに登校できる。これは健康にも安全にもよいだろう。',
        'もちろん，始まりが遅くなると終わりも遅くなり，部活動やアルバイトの時間が減ると心配する人もいる。しかし，学校は昼休みを短くしたり，部活動の練習の一部を週末に移したりすることでこの問題を解決できる。全体として，よく休んだ生徒のほうがよく学ぶと私は思うので，授業を遅く始めるのは試してみる価値のある変化だ。',
    ],
    'tips': [
        '最初の文で I agree / I disagree をはっきり書き，問いの表現（start classes one hour later）を使って立場を示す。',
        '理由は2つにしぼり，In addition でつなぐ。「集中できる」「朝食・通学が安全になる」のように，それぞれに身近な具体例をつける。',
        '反対意見（Of course, some people worry that …）を一つ取り上げ，However で解決策を示すと，考えの深さが伝わる。',
        '「もし～なら」の話なので，would / could を使う（students would have …）。',
        '最後に Overall, … で結論をくり返し，語数（150 words 以上）を必ず確かめる。',
    ],
    'criteria': [
        ('問いに答えている：賛成か反対かがはっきり書かれている', 6),
        ('内容：理由が二つ程度あり，それぞれに具体例がある', 6),
        ('構成：導入・理由・反対意見への答え・結論の流れがあり，つなぎの語句が使われている', 4),
        ('英語の正確さ：文法・語法・つづりの誤りが少なく，意味が通じる', 6),
        ('語数：150語以上（不足する場合は大きく減点）', 2),
    ],
}
