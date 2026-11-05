# -*- coding: utf-8 -*-
"""第1回 Ⅳ 自由英作文（2つの問いから1つ・100語程度）。書き下ろし。"""
W = {
    'prompts': ['Should high school students have part-time jobs? Give reasons for your view.',
                'What is one skill you hope to master before you turn twenty, and why?'],
    'prompts_ja': ['高校生はアルバイトをするべきか。理由を挙げて意見を説明せよ。',
                   '20歳になる前に身につけたい技能を一つ挙げ，その理由を述べよ。'],
    'criteria': [('内容：問いに正面から答え，立場・技能がはっきりしている', 15),
                 ('理由・具体例：理由が2つ程度あり，具体例や説明で支えられている', 15),
                 ('構成：導入・理由・まとめの流れがあり，つなぎの語が適切', 8),
                 ('語法・文法：時制・数・語順などの誤りが少ない', 8),
                 ('分量：100語程度（おおむね90〜120語）', 4)],
    'models': [
        (0, "I believe high school students should be allowed to have part-time jobs, as long as their studies do not suffer. "
            "First, working teaches responsibility. When students arrive on time and serve customers politely, they learn that other people depend on them. "
            "Second, a job helps young people understand the value of money. If they earn a thousand yen after an hour of hard work, they will think more carefully before spending it. "
            "Of course, some students may become too tired to study. For this reason, schools and parents should set a limit, such as ten hours a week. "
            "With sensible rules, part-time work can be a valuable experience."),
        (1, "Before I turn twenty, I hope to master cooking simple, healthy meals. "
            "At the moment, my mother prepares almost all of my food, so I have little idea how to plan a menu or buy ingredients. "
            "However, I hope to study at a university far from my hometown, and I will soon have to look after myself. "
            "If I can cook, I will manage to eat well without spending too much money at convenience stores. "
            "In addition, cooking for friends seems like a good way to get to know people in an unfamiliar city. "
            "So I plan to start by helping my mother in the kitchen every weekend."),
    ],
    'models_ja': [
        '私は，勉強がおろそかにならない限り，高校生はアルバイトをすることを認められるべきだと考える。第一に，働くことは責任感を教えてくれる。時間どおりに来て丁寧に客に接すると，ほかの人が自分を頼りにしていることを学ぶ。第二に，仕事は若者がお金の価値を理解する助けになる。1時間懸命に働いて千円を稼げば，それを使う前にもっとよく考えるだろう。もちろん，疲れすぎて勉強できなくなる生徒もいるかもしれない。そのため，学校や親が週10時間までのように上限を決めるべきだ。分別のあるきまりがあれば，アルバイトは貴重な経験になりうる。',
        '20歳になる前に，私は簡単で健康的な食事の作り方を身につけたい。今は母がほとんどすべての食事を用意してくれるので，献立の立て方や材料の買い方がほとんどわからない。しかし，私は地元から遠い大学で学びたいと思っており，もうすぐ自分の面倒は自分で見なければならなくなる。料理ができれば，コンビニにお金を使いすぎずにきちんと食べられるだろう。さらに，友人のために料理をすることは，知らない街で人と知り合うよい方法に思える。だから私は，毎週末に台所で母を手伝うことから始めるつもりだ。',
    ],
    'tips': ['最初の1文で立場（賛成・反対／選んだ技能）をはっきり書く。両論を並べるだけで結論がないと内容点が下がる。',
             '理由は2つ程度にしぼり，First, / Second, / In addition, などでつなぐ。1つの理由に具体例を1文添えると説得力が増す。',
             '「100語程度」なので，80語未満や140語を超える答案は分量で減点されやすい。書き終えたら語数を数える。',
             'part-time job は数えられる名詞（a part-time job / part-time jobs）。冠詞や複数形の落としに注意。',
             '日本語の「〜するべきだ」をすべて must にすると強すぎる。should を基本にする。'],
}
