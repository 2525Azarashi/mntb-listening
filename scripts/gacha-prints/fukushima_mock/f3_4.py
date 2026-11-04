# -*- coding: utf-8 -*-
"""第3回 Ⅳ 自由英作文（2つの問いから1つ・100語程度）。書き下ろし。"""
W = {
    'prompts': ['Do you prefer shopping in stores or shopping online? Give reasons for your choice.',
                'If you could spend one month in any country, where would you go and what would you do there?'],
    'prompts_ja': ['店で買い物をするのと，ネットで買い物をするのとでは，どちらが好きか。選んだ理由を述べよ。',
                   'どこの国でも1か月過ごせるとしたら，どこへ行き，そこで何をしたいか。'],
    'criteria': [('内容：問いに正面から答え，選んだもの・国がはっきりしている', 15),
                 ('理由・具体例：理由や計画が具体的に書かれている', 15),
                 ('構成：導入・理由（計画）・まとめの流れがあり，つなぎの語が適切', 8),
                 ('語法・文法：時制（仮定法を含む）・数・語順などの誤りが少ない', 8),
                 ('分量：100語程度（おおむね90〜120語）', 4)],
    'models': [
        (0, "Although online shopping is convenient, I prefer buying things in real stores. "
            "The main reason is that I can check products with my own eyes and hands. When I buy clothes, for example, I can try them on and see whether the size and color really suit me. "
            "Online, a jacket that looks perfect in a photo may turn out to be too small. "
            "Another reason is that shopping in stores is a pleasant way to spend time with friends or family. We can talk, compare items, and have lunch together. "
            "So, in most cases I go to stores, even if online prices are sometimes a little lower."),
        (1, "If I could spend one month anywhere, I would go to New Zealand. "
            "First, I would love to see its famous natural scenery, such as tall mountains, clear lakes, and wide green fields. I have only seen these places in films, and walking through them myself is a dream of mine. "
            "Second, I would stay with a local family on a farm. By helping with daily work, I could practice English and learn how people there live. "
            "Finally, I would keep a short diary every night to remember what I saw and felt. "
            "I believe such an experience would make me more independent and open-minded."),
    ],
    'models_ja': [
        'ネットショッピングは便利だが，私は実際の店で物を買うほうが好きだ。主な理由は，自分の目と手で商品を確かめられることだ。たとえば服を買うとき，試着して，サイズや色が本当に自分に合うかを確かめられる。ネットでは，写真では完璧に見えた上着が小さすぎたとわかることもある。もう一つの理由は，店での買い物は友人や家族と時間を過ごす楽しい方法だということだ。話をしたり，品物を比べたり，一緒に昼食をとったりできる。だから，ネットの値段のほうが少し安いことがあっても，私はたいてい店に行く。',
        'どこでも1か月過ごせるなら，私はニュージーランドに行きたい。まず，高い山々，澄んだ湖，広い緑の野原といった有名な自然の景色を見たい。これらの場所は映画でしか見たことがなく，自分で歩いてみるのが夢だ。次に，農場の地元の家族のところに滞在したい。日々の仕事を手伝うことで，英語を練習し，そこの人々の暮らし方を学べるだろう。最後に，見たことや感じたことを覚えておくために，毎晩短い日記をつけたい。そうした経験は，私をより自立した，心の広い人間にしてくれると思う。',
    ],
    'tips': ['(2) は If I could ~, I would ~（仮定法過去）で書く。I will go と書くと「実際に行く予定」の意味になり，時制の誤りとして減点されやすい。',
             '(1) は「どちらも良い」で終わらせず，必ず一方を選ぶ。もう一方の長所を認めたうえで（Although ~）自分の選択を示すと説得力が増す。',
             '理由は2つ程度にしぼり，The main reason is that ~ / Another reason is that ~ / First, ~ Second, ~ などで整理する。',
             '国名は固有名詞なので大文字で書き始める（New Zealand）。',
             '書き終えたら語数を数え，100語程度（90〜120語）に収める。'],
}
