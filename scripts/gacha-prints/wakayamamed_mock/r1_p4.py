# -*- coding: utf-8 -*-
# 第1回 問題Ⅳ：日本語の随筆の下線部を英訳（書き下ろし。筆者・書名は架空）
P4 = {
    'points': 50,
    'lead': '以下の日本文を読み，下線部(1)・(2)の内容を英語で書き表せ。',
    'passage_ja': [
        '若いころ，私は「わからない」と言うのが怖かった。研究室で先輩に質問されると，よくわからないことでも，わかったような顔をしてうなずいていた。わからないと認めれば，自分の力が足りないことを知られてしまう気がしたのである。',
        'ところが，長く研究を続けるうちに，考えが変わってきた。{u1|本当に優れた研究者ほど，自分が何を知らないのかをはっきりと口にするものだ}。彼らは「ここから先はまだ誰にもわかっていない」と平気で言う。その一言があるからこそ，周りの人たちは次に何を調べればよいのかがわかるのである。',
        '知らないことを恥じる気持ちは，誰にでもある。しかし，その気持ちに負けてわかったふりを続けていると，いつまでたっても本当の疑問にたどりつけない。{u2|わからないことをわからないと言える人だけが，新しいことを学び続けることができるのだと，今の私は思っている}。',
    ],
    'source': '（宮坂 透『問いを手放さない』より。編集部による架空の文章）',
    'questions': [
        {'label': '(1)', 'ref': '1', 'points': 25,
         'models': [
             'The more truly excellent a researcher is, the more clearly he or she tends to say what he or she does not know.',
             'Really good researchers are usually the ones who state clearly what they do not know.',
         ],
         'tips': [
             '「〜ほど…」は the 比較級 …, the 比較級 … で表せる。The better a researcher is, the more clearly … の語順に注意（形容詞・副詞を前に出す）。',
             '比較の構文が難しければ，解答例2のように「本当に優れた研究者とは〜する人たちだ」と言いかえてもよい。',
             '「〜するものだ」は一般的な傾向なので，現在形や tend to do で表す。',
             '「自分が何を知らないのか」は間接疑問 what they do not know。what do they not know としない。',
         ],
         'criteria': [('「優れた研究者ほど」の比較（または同じ意味の言いかえ）が正しく表されている', 8),
                      ('「何を知らないのか」を間接疑問の正しい語順で表している', 7),
                      ('「はっきりと口にする」を say / state clearly などで表している', 5),
                      ('文法・語法・つづりの誤りがない', 5)]},
        {'label': '(2)', 'ref': '2', 'points': 25,
         'models': [
             'I now believe that only people who can admit that they do not understand something can keep learning new things.',
             'Now I think that it is only those who are able to say "I don\'t know" when they do not know something that can continue to learn.',
         ],
         'tips': [
             '文の骨組みは「今の私は思っている（I now believe / think）＋ that 節」。',
             '「〜できる人だけが」は only people who can … を主語にする。only を主語の前に置くと「〜だけ」の意味がはっきりする。',
             '「わからないことをわからないと言う」は，そのまま訳すと不自然になりやすい。admit that they do not understand something（わからないと認める）や say "I don\'t know"（「わからない」と言う）と言いかえる。',
             '「学び続ける」は keep learning / continue to learn。',
         ],
         'criteria': [('「今の私は思っている」を I now believe / think that … で表している', 4),
                      ('「〜できる人だけが」を only people who can … などで正しく表している', 8),
                      ('「わからないことをわからないと言える」を自然な英語に言いかえている', 8),
                      ('「新しいことを学び続ける」を表し，文法・語法の誤りがない', 5)]},
    ],
    'about': '架空の研究者の随筆。日本語の「〜ほど…」「〜だけが」「わからないことをわからないと言う」など，そのまま英語にしにくい表現を，意味を変えずに英語にしやすい形に言いかえられるかがポイント。',
}
