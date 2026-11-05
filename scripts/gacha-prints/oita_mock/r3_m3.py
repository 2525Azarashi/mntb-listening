# -*- coding: utf-8 -*-
# 第3回 〔3〕 医学部：語句整序（24点）。英文は書き下ろし（研究・人物・数値は架空）
M3 = {
    'lead': '次の英文の【　①　】〜【　⑥　】には，下の a〜f の [　] 内の語句を並べ替えてできる英語が1つずつ入る。'
            '[　] 内の語句を正しい順序にし，【　①　】〜【　⑥　】に入る英語をそれぞれ解答欄に書きなさい（a〜f の記号は書かなくてよい）。'
            'ただし，文頭に来る語も小文字で示してある。',
    'title': 'The Power of an Empty Pill',
    'passage': [
        'Imagine taking a pill for a headache and feeling better within half an hour, only to learn later that the pill contained nothing but sugar. '
        'This is the placebo effect, and it is one of the strangest findings in medicine. A placebo has no active ingredient, and yet {o1} when they believe they are receiving real treatment.',

        'Doctors have known about this effect for centuries, but for a long time it was seen mainly as a problem. When a new drug is tested, researchers must show that it works better than a placebo. '
        'For this reason, patients in a trial are usually divided into two groups, and {o2} which group they belong to. '
        'If both groups improve by the same amount, the drug is judged to have no real effect. In this way, the placebo became a standard against which every new medicine is measured.',

        'In recent years, however, scientists have become interested in the placebo effect itself. Brain scans have shown that when people expect pain relief, '
        'their brains release natural chemicals that reduce pain. The effect, in other words, is not simply imaginary. '
        'Expectations seem to matter a great deal: in one study, people who were told that a pill was expensive reported more relief than those {o3}.',

        'Even the appearance of a treatment can make a difference. Some studies suggest that two pills work better than one, that injections work better than pills, '
        'and that the color of a pill can influence {o4}. Surprisingly, a few experiments have found that placebos can help even when patients are told honestly '
        'that the pills contain no medicine, as long as the purpose of the treatment is carefully explained.',

        'The placebo effect also has a dark side, known as the nocebo effect. When patients are warned about possible side effects, some of them begin to experience those very symptoms, '
        'even if they have only been given a sugar pill. This creates a difficult problem for doctors, {o5} without making patients feel worse.',

        'Placebos cannot shrink a tumor or cure an infection, and no responsible doctor would use them in place of effective treatment. '
        'What the research does show is that the relationship between doctor and patient matters. A doctor who listens carefully and explains things clearly '
        'may be adding something real to every treatment, whatever the pills themselves contain. As one researcher put it, {o6} as part of the medicine.',
    ],
    'notes': [('placebo', 'プラセボ・偽薬'), ('active ingredient', '有効成分'), ('trial', '臨床試験'), ('brain scan', '脳の画像検査'),
              ('injection', '注射'), ('nocebo', 'ノセボ'), ('symptom', '症状'), ('tumor', '腫瘍')],
    'items': [
        {'key': 'a', 'shown': ['how', 'feel', 'it', 'people', 'makes'], 'answer': ['how', 'it', 'makes', 'people', 'feel'],
         'slot': 4, 'expl': 'influence の目的語になる間接疑問 how ＋ S ＋ V。it は the color of a pill を受ける。make 人 feel「人に～と感じさせる」（使役動詞 make ＋ 目的語 ＋ 原形）。'},
        {'key': 'b', 'shown': ['who', 'it', 'were', 'was', 'told', 'cheap'], 'answer': ['who', 'were', 'told', 'it', 'was', 'cheap'],
         'slot': 3, 'expl': 'those who ～「～する人々」。前の people who were told that a pill was expensive と対比になっている。be told (that) S V「～だと言われる」。'},
        {'key': 'c', 'shown': ['who', 'must', 'honest', 'be', 'about', 'risks'], 'answer': ['who', 'must', 'be', 'honest', 'about', 'risks'],
         'slot': 5, 'expl': 'コンマのあとの非制限用法の who が doctors を受ける。be honest about ～「～について正直である」。後ろの without making patients feel worse「患者の具合を悪くさせずに」とつながる。'},
        {'key': 'd', 'shown': ['many', 'can', 'improve', 'patients', 'genuinely'], 'answer': ['many', 'patients', 'can', 'genuinely', 'improve'],
         'slot': 1, 'expl': 'and yet のあとの主節。主語 many patients ＋ 助動詞 can ＋ 副詞 genuinely ＋ 動詞 improve「本当に良くなりうる」。後ろの when they believe … の they は many patients。'},
        {'key': 'e', 'shown': ['the doctors', 'nor', 'know', 'the patients', 'neither'], 'answer': ['neither', 'the patients', 'nor', 'the doctors', 'know'],
         'slot': 2, 'expl': 'neither A nor B「A も B も～ない」が主語。動詞は B（the doctors）に合わせるので複数の know。後ろの which group they belong to「どちらのグループに属しているか」が know の目的語（二重盲検）。'},
        {'key': 'f', 'shown': ['the', 'we', 'see', 'should', 'conversation'], 'answer': ['we', 'should', 'see', 'the', 'conversation'],
         'slot': 6, 'expl': 'see A as B「A を B とみなす」。主語 we ＋ should see ＋ 目的語 the conversation ＋ as part of the medicine「話し合いを薬の一部とみなすべきだ」。'},
    ],
    'translation': [
        '頭痛のために錠剤を飲み，30分以内に楽になったのに，あとになってその錠剤には砂糖しか入っていなかったと知ったと想像してみてほしい。'
        'これがプラセボ効果であり，医学における最も不思議な発見の一つである。プラセボには有効成分がないのに，本物の治療を受けていると信じると，多くの患者は本当に良くなりうるのだ。',
        '医師たちは何世紀も前からこの効果を知っていたが，長い間それは主に問題とみなされていた。新しい薬を試験するとき，研究者はそれがプラセボよりよく効くことを示さなければならない。'
        'このため，試験の患者はふつう2つのグループに分けられ，患者も医師たちも，患者がどちらのグループに属しているかを知らない。両方のグループが同じだけ良くなれば，その薬には本当の効果がないと判断される。こうしてプラセボは，あらゆる新薬を測る基準になったのである。',
        'しかし近年，科学者たちはプラセボ効果そのものに興味をもつようになった。脳の画像検査によって，痛みが和らぐと期待すると，脳が痛みを減らす天然の化学物質を放出することが分かった。'
        'つまり，その効果は単なる思い込みではないのである。期待は非常に重要なようだ。ある研究では，錠剤が高価だと言われた人は，安いと言われた人よりも痛みが和らいだと報告した。',
        '治療の見た目でさえ違いを生みうる。2錠は1錠よりよく効き，注射は錠剤よりよく効き，錠剤の色がそれによって人がどう感じるかに影響しうると示す研究もある。'
        '驚いたことに，治療の目的が注意深く説明されていれば，錠剤に薬が入っていないと正直に伝えられた場合でもプラセボが役に立ちうることを見つけた実験もいくつかある。',
        'プラセボ効果には，ノセボ効果として知られる暗い面もある。起こりうる副作用について警告されると，砂糖の錠剤しか与えられていなくても，まさにその症状を感じ始める患者がいるのだ。'
        'これは医師にとって難しい問題を生む。医師は患者の具合を悪くさせずに，危険について正直でなければならないからである。',
        'プラセボは腫瘍を小さくしたり感染症を治したりすることはできないし，責任ある医師なら効果のある治療の代わりにそれを使うことはないだろう。'
        '研究が実際に示しているのは，医師と患者の関係が重要だということである。注意深く耳を傾け，分かりやすく説明する医師は，錠剤そのものに何が入っていようと，あらゆる治療に何か本物のものを加えているのかもしれない。'
        'ある研究者が言ったように，私たちは話し合いを薬の一部とみなすべきなのである。',
    ],
    'vocab': [('only to do', '（結果）結局～するだけだ'), ('nothing but ～', '～だけ'), ('belong to ～', '～に属する'), ('relief', '（苦痛の）軽減'),
              ('imaginary', '想像上の'), ('as long as ～', '～しさえすれば'), ('side effect', '副作用'), ('shrink', '小さくする'),
              ('in place of ～', '～の代わりに'), ('see A as B', 'AをBとみなす')],
}
