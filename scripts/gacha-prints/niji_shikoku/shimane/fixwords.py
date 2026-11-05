"""島根大学の指示文を、過去問と一致しない自前の言い回しにそろえる（全ラウンド共通）"""
import sys, re, pathlib
REP = [
 ("Read the following passage and answer the questions.（共通問題）", "Study the passage below, then respond to each item.〔共通〕"),
 ("What is the best title of this passage?", "Choose the heading that fits the whole passage most closely."),
 ("Which was NOT mentioned as an example of (4) “Not everything went smoothly”?", "Which of these is NOT given in the passage as one of the problems referred to in (4)?"),
 ("In about 70 words, describe what you notice from the data, and give the reason(s) why it happens.", "Write about 70 words in English: explain the main trend you see, and suggest one or two causes for it."),
 ("次の英語の指示に従って英語で答えなさい。なお、解答用紙の指定した（　）欄に、使用した語数を記入すること。ただし、コンマやピリオドなどの記号は語数に入れない。",
  "下の英文の指示を読み、英語で書け。書いた語の数を解答用紙の（　）に記すこと（カンマ・ピリオド等の符号は数に含めない）。"),
 ("を次から選び、解答しなさい。ただし、同じ語を複数回使わないこと。", "に合う語を、［　］の4語から重ならないように選べ。"),
 ("に入れるのに最も適切な語", "にあてはまる語"),
 ("の（　）内の語句を、本文の文脈に合うように並べ替えなさい。", "の（　）の中の語句を、前後の内容が通じる順に並べて書け。"),
 ("この英文のタイトルとして最もふさわしいものを次の (a)〜(e) の中から1つ選びなさい。", "本文全体の題名として、いちばん合うものを (a)〜(e) から一つ選べ。"),
 ("の具体的内容として本文中で述べられていないものを、次の (a)〜(e) の中から1つ選びなさい。", "の例として、本文に挙がっていないものを (a)〜(e) から一つ選べ。"),
 ("本文の内容と一致するものを次の (a)〜(h) の中から2つ選びなさい。", "本文の内容に合うものを (a)〜(h) から二つ選べ。"),
 ("の具体的内容と、その結果起こることを、本文にそって日本語で説明しなさい。", "が指している事態と、それが招く結果を、日本語でまとめよ。"),
 ("を、It の具体的内容がわかるように、本文にそって日本語で説明しなさい。", "について、It が何を受けているかを示しつつ、筆者の主張を日本語でまとめよ。"),
 ("、本文にそって日本語で説明しなさい。", "、日本語でまとめよ。"),
 ("本文にそって日本語で説明しなさい", "日本語でまとめよ"),
 ("を日本語に訳しなさい。", "を和訳せよ。"),
 ("次の英文を読んで問いに答えなさい。（医学部医学科用問題）", "以下の英文について、各問いに答えよ。〔医学科用〕"),
 ("次の英文を読んで、問いに答えなさい。（共通問題）", "次の英文を読み、後の問いに答えよ。〔共通〕"),
 ("次の問いに答えなさい。（医学部医学科用問題）", "各問いに答えよ。〔医学科用〕"),
 ("A．次の本文の下線部 (1)・(2) を英語に直しなさい。", "A．下の文章の下線部 (1)・(2) を英文にせよ。"),
 ("B．次の英語の指示に従って80語程度の英語で答えなさい。なお、解答用紙の指定した（　）欄に、使用した語数を記入すること。ただし、コンマやピリオドなどの記号は語数に入れない。",
  "B．下の英文の指示に従い、80語前後の英語で書け。書いた語数を解答用紙の（　）に記すこと（符号は数えない）。"),
 ("のそれぞれについて、本文の内容と一致すれば T、一致しなければ F と答えなさい。", "が本文の内容に合っていれば T、合っていなければ F を書け。"),
 ("（医学部医学科用問題）", "（医学科用）"),
 ("（法文学部・人間科学部・総合理工学部・生物資源科学部用問題）", "（医学科以外の学部用）"),
 ("Give specific reasons for your opinion.", "Support your view with concrete reasons."),
]
for f in sys.argv[1:]:
    p = pathlib.Path(f); s = p.read_text(); n0 = s
    for a, b in REP: s = s.replace(a, b)
    if s != n0: p.write_text(s); print('fixed', f)
