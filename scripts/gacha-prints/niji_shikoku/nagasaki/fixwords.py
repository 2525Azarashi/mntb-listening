"""長崎大学の指示文・解答の言い回しを、過去問と一致しない自前の表現にそろえる（全ラウンド共通）"""
import sys, pathlib
REP = [
 ("に入る最も適切なものを A〜D から1つずつ選び、記号で答えよ。同じ記号は一度しか使えない。", "にあてはまる語句を A〜D から一つずつ選べ（同じものは二度使わない）。"),
 ("を日本語に訳せ。", "の意味を、自然な日本語で書き表せ。"),
 ("を和訳せよ。", "の意味を、自然な日本語で書き表せ。"),
 ("下のグラフを見て、次の2つの問いに、それぞれ100語程度の英語で答えよ。", "下のグラフについて、問い1・2 のどちらにも約100語の英語で解答せよ。"),
 ("Give at least two reasons to support your opinion.", "Explain your view with two or more reasons."),
 ("According to the passage, the heat island effect", "The passage says that the heat island effect"),
 ("and there was no one in the city to take care of him.", "and nobody in the city could look after him."),
 ("専門家だけの仕事ではないことを示している", "専門家だけに任せる仕事ではないと教えてくれる"),
 ("車で短い距離を移動することが減る", "車で近場へ出かけることが減る"),
 ("の内容にそって日本語で説明せよ。", "の内容をふまえ、日本語でまとめよ。"),
 ("にそって日本語で説明せよ。", "をふまえ、日本語でまとめよ。"),
 ("Explain in your own words.", "Put it into your own English."),
 ("Explain the meaning of underlined part (3) in your own words.", "Using your own English, say what underlined part (3) means."),
 ("Because she did not want to explain the real reason she had stopped practicing.", "Because she was hiding the true cause of her silence from her mother."),
 ("Describe the changes in the number of foreign visitors to this prefecture shown in the graph.", "Using the graph, describe how foreign visitor numbers to this prefecture have changed."),
 ("下線部 (1) で筆者が言おうとしていることを、本文の内容をふまえて日本語で説明せよ。", "下線部 (1) に込められた筆者の考えを、本文の内容をふまえて日本語でまとめよ。"),
 ("下線部 (1) で生徒が言おうとしたことを", "下線部 (1) に込めた生徒の思いを"),
 ("リクはおじのケンジのことをほとんど知らなかった。", "おじのケンジについて、リクが知っていることはわずかだった。"),
]
for f in sys.argv[1:]:
    p = pathlib.Path(f); s = p.read_text(); n0 = s
    for a, b in REP: s = s.replace(a, b)
    if s != n0: p.write_text(s); print('fixed', f)
