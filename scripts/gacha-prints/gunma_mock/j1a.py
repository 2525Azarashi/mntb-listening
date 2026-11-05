# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第1回 大問1・大問2（書き下ろし。人物・団体・地名・調査・数値は架空）
CH = '空所（ {x} ）に入れるのにふさわしい語句を，（ア）〜（エ）から1つ選んで記号で書け。'
CO = '空所（ {x} ）に入れる語の組み合わせとしてふさわしいものを，（ア）〜（エ）から1つ選んで記号で書け。'
TR = '下線部（{x}）を日本語に訳せ。'

P1 = {
    'points': 150,
    'intro': '次の英文は，デジタルの記録を長く残すことの難しさを論じている。',
    'title': 'Will Our Files Outlive Us?',
    'passage': [
        "Every day, people around the world take billions of photographs, send countless messages, and save documents that they "
        "expect to keep for the rest of their lives. Most of us assume that anything stored on a computer will last forever, or at "
        "least much longer than a letter written on paper. {b:a}, the opposite is often true. A clay tablet made in an ancient city "
        "can still be read thousands of years later, and a book printed in the fifteenth century can be opened by anyone today. "
        "{u:b|In contrast, a file created only twenty years ago may already be impossible to open, not because it has been destroyed, "
        "but because no machine that can understand it is still in use.} Some historians have begun to warn that our era could become "
        "a \"digital dark age,\" a period that future generations will know surprisingly little about.",
        "The problem has two main causes. The first is physical. Hard disks, memory cards, and even the optical discs that were once "
        "advertised as permanent slowly lose their data. Magnetic signals weaken, tiny parts wear out, and a single scratch can make an "
        "entire disc unreadable. The second cause, which experts consider more serious, is technical change. Software companies "
        "constantly release new versions of their programs and stop supporting old ones. {u:c|When a format is abandoned, the files "
        "saved in it become locked boxes whose keys have been thrown away.} A researcher at the Marrowfield Institute of Information "
        "once tried to open a set of reports written in the 1990s and found that none of the five computers in her office could "
        "display them correctly.",
        "One possible solution is to make copies again and again. Libraries that store digital collections often move their files to "
        "new storage devices every few years, before the old ones fail. This process, called migration, keeps the data alive, but it is "
        "far {b:d} expensive and time-consuming than many people imagine, and it is not {b:e} risk. Each time a file is converted to "
        "a newer format, small details such as fonts, colors, or the position of images may change, and after several conversions the "
        "copy may look quite different from the original. Another approach is to keep old machines working so that old files can be "
        "opened in their original form. However, spare parts for a thirty-year-old computer are hard to find, and the people who know "
        "how to repair such machines are getting older. Some institutions therefore use programs that imitate old computers on modern "
        "ones, much as an actor plays the role of a person from another century. Such a program serves as a kind of {b:f} between "
        "the present and the past.",
        "Technology alone, however, cannot solve the problem. Deciding what to keep is just as important as deciding how to keep it. "
        "In earlier times, archivists could not save every piece of paper, so they had to choose carefully, and their choices shaped "
        "what we know about history today. Now the amount of information produced each day is so enormous that keeping all of it is "
        "impossible. {u:g|Ironically, the ease with which we can create digital records has made it harder, not easier, to decide "
        "which of them are worth saving.} A family that once kept a single album of a few dozen prints may now have tens of thousands "
        "of photographs scattered across phones, laptops, and online services, and most of them will never be looked at again.",
        "Ordinary people can also play a part. According to a survey of 2,000 adults carried out by the Marrowfield Institute, only "
        "14 percent had made a backup of their personal photos within the previous year, and nearly half did not know which format "
        "their important documents were saved in. Many respondents believed that online storage services would keep their files safe "
        "for as long as they liked. {u:h|Yet such services are businesses, and businesses can change their rules, raise their prices, "
        "or close down altogether.} When one popular photo service shut down several years ago, users were given just two months to "
        "download their pictures, and many of them never received the warning.",
        "What, then, should we do? Experts suggest a few simple habits. First, keep at least two copies of anything important, and "
        "store them in different places. Second, choose formats that are widely {b:i} and openly described, so that programmers in "
        "the future can still understand them. Third, and perhaps most importantly, be {b:j} about what you save: delete blurry photos "
        "and duplicate files, and give the remaining ones clear names and dates. Finally, do not {b:k} the value of printing, because "
        "a paper copy of a few treasured pictures may outlast every device you will ever own. {u:l|The records we leave behind will "
        "tell future generations who we were, and it is up to us to make sure that the story does not end with a file that nobody "
        "can open.}",
    ],
    'notes': [(1, 'clay tablet', '粘土板'), (2, 'optical disc', '光ディスク'), (2, 'magnetic', '磁気の'),
              (3, 'migration', '移行'), (3, 'imitate', 'まねる'), (4, 'archivist', '記録保管の専門家'),
              (5, 'respondent', '回答者'), (6, 'duplicate', '重複した'), (6, 'outlast', '〜より長くもつ')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（つなぎの語）', 'points': 6, 'stem': CH.format(x='a'),
         'options': ['Moreover', 'Therefore', 'However', 'Similarly'], 'answer': 2,
         'expl': '直前は「コンピュータに保存したものは紙よりずっと長く残ると思いこんでいる」，直後は「the opposite is often true（実際はその逆であることが多い）」。'
                 '前後が反対の内容なので，逆接の However（しかし）が入る。Moreover は追加，Therefore は結果，Similarly は類似を表す。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': 'それに対して，わずか20年前に作られたファイルが，もう開けなくなっていることがある。それは壊されたからではなく，それを理解できる機械がもうどこでも使われていないからである。',
         'expl': 'In contrast「それに対して」は，前文の粘土板や古い本との対比。may already be impossible to open「すでに開けないかもしれない」。'
                 'not because ~, but because …「〜だからではなく…だから」の構文をきちんと訳し分ける。no machine that can understand it is still in use は'
                 '「それを理解できる機械はもはや1台も使われていない」。no を「〜がない」と文全体の否定として訳す。',
         'criteria': [('In contrast を対比として訳している', 3), ('a file created only twenty years ago / may already be impossible to open', 5),
                      ('not because ~, but because … の構文', 5), ('no machine that can understand it is still in use（否定・関係代名詞・in use）', 5)]},
        {'kind': 'ja', 'marks': ['c'], 'tag': '内容説明', 'points': 18, 'lines': 3,
         'stem': '下線部（c）は，ファイルがどのような状態になることをたとえているか。本文の内容に沿って日本語で説明せよ。',
         'answer': 'ソフトウェアの会社がある保存形式の対応をやめると，その形式で保存されたファイルは中身が残っていても，それを読み取れるプログラムや機械がなくなるため，開いて内容を見ることができなくなる状態。',
         'expl': 'locked boxes（鍵のかかった箱）＝ファイル，keys（鍵）＝そのファイルを開くためのソフトウェア・機械，have been thrown away（捨てられた）＝対応がやめられた・使われなくなった，という対応を読み取る。'
                 '前の文の stop supporting old ones と，第①段落の not because it has been destroyed（壊れたわけではない）がヒント。「中身は残っているのに開けない」ことを書く。',
         'criteria': [('保存形式（ソフト）の対応が打ち切られることが原因', 6), ('ファイルの中身（データ）自体は残っている', 4),
                      ('読み取れるプログラム・機械がないので開けない・内容を見られない', 8)]},
        {'kind': 'combo', 'marks': ['d', 'e'], 'tag': '空所補充（語の組み合わせ）', 'points': 10, 'stem': CO.format(x='d ）・（ e'),
         'rows': [('less', 'with'), ('more', 'without'), ('more', 'with'), ('less', 'without')], 'answer': 1,
         'expl': '（d）は直後の than many people imagine から比較級。移行は「何年かごとにファイルを新しい装置に移す」作業なので，思われているよりずっとお金と時間がかかる（far more expensive）。'
                 '（e）は次の文で「変換のたびに細かい部分が変わることがある」と危険を説明しているので，not without risk（危険がないわけではない＝危険もある）となる without が入る。'},
        {'kind': 'choice', 'marks': ['f'], 'tag': '空所補充（語の選択）', 'points': 6, 'stem': CH.format(x='f'),
         'options': ['bridge', 'wall', 'mirror', 'gap'], 'answer': 0,
         'expl': '古いコンピュータをまねるプログラムは，今のコンピュータで昔のファイルを開けるようにするもの。現在と過去を「つなぐ」ものなので bridge（橋）が入る。'
                 'between the present and the past とのつながりから，wall（壁）や gap（すき間）は反対の意味になる。'},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第⑤段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['In the survey, fewer than one in five adults had backed up their personal photos during the previous year.',
                        'About half of the people in the survey knew exactly which format their important documents used.',
                        'A large number of respondents expected online storage to protect their files for as long as they wanted.',
                        'When a photo service closed, its users were given two years to save their pictures.'],
         'answers': ['〇', '×', '〇', '×'],
         'expl': '（ア）only 14 percent（14％）は5人に1人（20％）より少ないので〇。（イ）nearly half did not know（半数近くが知らなかった）とあるので×。'
                 '（ウ）would keep their files safe for as long as they liked に合うので〇。（エ）just two months（わずか2か月）なので×。各4点。'},
        {'kind': 'ja', 'marks': ['g'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='g'), 'lines': 3,
         'answer': '皮肉なことに，私たちがデジタルの記録を簡単に作れるようになったことで，そのうちのどれを保存する価値があるかを決めるのは，簡単になるどころか，かえって難しくなった。',
         'expl': '主語は the ease with which we can create digital records「私たちがデジタルの記録を作ることができる容易さ」。with which は create ~ with ease（簡単に〜を作る）の with が前に出た形。'
                 '「容易さが〜を難しくした」と直訳せず，「簡単に作れるようになったことで〜が難しくなった」と因果で訳すと自然。'
                 'made it harder, not easier, to decide ~ の it は形式目的語で，to decide 以下を指す。which of them are worth saving「それらのうちどれが保存する価値があるか」。',
         'criteria': [('Ironically「皮肉なことに」', 2), ('the ease with which we can create digital records の把握', 6),
                      ('make it harder, not easier, to ~（形式目的語・「かえって」の対比）', 6), ('which of them are worth saving', 4)]},
        {'kind': 'ja', 'marks': ['h'], 'tag': '内容説明', 'points': 20, 'lines': 4,
         'stem': '下線部（h）のように筆者が述べるのは，オンラインの保存サービスにどのような危険があるからか。本文の内容に沿って日本語で説明せよ。',
         'answer': 'オンラインの保存サービスは企業が営んでいるので，規則を変えたり料金を上げたり，サービスそのものをやめたりすることがある。実際に，ある写真サービスが終了したときには，利用者は2か月で写真を取り出さなければならず，その知らせを受け取れなかった人も多かったように，預けたファイルを失うおそれがある。',
         'expl': '下線部は，前の文の「多くの人がオンラインの保存サービスがファイルをいつまでも安全に保ってくれると信じていた」への反論。'
                 '企業なので「規則の変更・値上げ・サービスの終了」がありうること，その具体例として直後の文の写真サービスの終了（2か月の猶予・知らせが届かない）を挙げ，'
                 '「ファイルを失うかもしれない」という危険にまとめる。',
         'criteria': [('サービスは企業が運営している', 4), ('規則の変更・値上げ・終了がありうる（2つ以上）', 6),
                      ('写真サービス終了の例（2か月・知らせが届かない）', 6), ('預けたファイルを失うおそれがある，とまとめている', 4)]},
        {'kind': 'combo', 'marks': ['i', 'j', 'k'], 'tag': '空所補充（語の組み合わせ）', 'points': 12, 'stem': CO.format(x='i ）〜（ k'),
         'rows': [('used', 'careless', 'underestimate'), ('hidden', 'selective', 'underestimate'),
                  ('hidden', 'careless', 'overuse'), ('used', 'selective', 'underestimate')], 'answer': 3,
         'expl': '（i）未来のプログラマーにも理解できるのは，広く使われていて（widely used），中身が公開されている形式。hidden（隠された）は openly described と矛盾する。'
                 '（j）直後の「ぼやけた写真や重複したファイルを消す」から，保存するものを選ぶ selective（よく選ぶ）が入る。careless（不注意な）は逆。'
                 '（k）「紙に印刷した写真はどの装置よりも長くもつかもしれない」ので，印刷の価値を underestimate（軽く見る）してはいけない。'},
        {'kind': 'ja', 'marks': ['l'], 'tag': '下線部和訳', 'points': 16, 'stem': TR.format(x='l'), 'lines': 3,
         'answer': '私たちが後に残す記録は，私たちがどのような人間だったのかを未来の世代に伝えるだろう。だから，その物語が誰にも開けないファイルで終わってしまわないようにするのは，私たち次第である。',
         'expl': 'The records we leave behind は records の後ろに関係代名詞が省略された形「私たちが後に残す記録」。tell ～ who we were「～に私たちが誰（どんな人間）だったかを伝える」。'
                 'it is up to us to ~「〜するのは私たち次第だ」。make sure that ~「必ず〜するようにする」。a file that nobody can open「誰も開けないファイル」。',
         'criteria': [('The records we leave behind（関係代名詞の省略）', 4), ('tell future generations who we were', 4),
                      ('it is up to us to make sure that ~', 5), ('the story does not end with a file that nobody can open', 3)]},
        {'kind': 'choice', 'tag': '主旨', 'points': 10,
         'stem': '本文全体の主旨としてふさわしいものを，（ア）〜（エ）から1つ選んで記号で書け。',
         'options': ['Digital records are always safer than paper ones because they can be copied easily.',
                     'Keeping digital information for the future requires good technology, careful choices, and simple daily habits.',
                     'Only libraries and governments need to worry about losing digital data.',
                     'Old computers should be kept in museums so that people can see how technology has changed.'],
         'answer': 1,
         'expl': '第②・③段落で技術的な問題と対策，第④段落で「何を残すかを選ぶこと」，第⑤・⑥段落で一人ひとりができる習慣を述べているので（イ）。'
                 '（ア）は第①段落の内容と逆。（ウ）は第⑤段落の Ordinary people can also play a part に反する。（エ）は本文にない。'},
    ],
    'translation': [
        '毎日，世界中の人々が何十億枚もの写真を撮り，数えきれないほどのメッセージを送り，一生とっておくつもりの文書を保存している。私たちの多くは，コンピュータに保存したものは永遠に，少なくとも紙に書いた手紙よりはずっと長く残ると思いこんでいる。'
        'しかし，実際はその逆であることが多い。古代の都市で作られた粘土板は何千年もたった今でも読むことができ，15世紀に印刷された本は今日でも誰でも開くことができる。'
        '(b)それに対して，わずか20年前に作られたファイルが，もう開けなくなっていることがある。それは壊されたからではなく，それを理解できる機械がもうどこでも使われていないからである。'
        '歴史家の中には，私たちの時代は「デジタルの暗黒時代」，つまり未来の世代がおどろくほど少ししか知ることのない時代になるかもしれないと警告し始めた人もいる。',
        'この問題には主な原因が二つある。一つ目は物理的なものだ。ハードディスクやメモリーカード，そしてかつては永久にもつと宣伝された光ディスクでさえ，少しずつデータを失っていく。磁気の信号は弱まり，小さな部品はすり減り，たった一つの傷でディスク全体が読めなくなることもある。'
        '二つ目の原因は，専門家がより深刻だと考えているもので，技術の変化である。ソフトウェアの会社は，プログラムの新しい版を次々に出し，古い版への対応をやめてしまう。(c)ある形式が見捨てられると，その形式で保存されたファイルは，鍵を捨てられた鍵つきの箱になってしまう。'
        'マローフィールド情報研究所のある研究者は，1990年代に書かれた報告書を開こうとしたが，事務所にある5台のコンピュータのどれでも正しく表示できなかった。',
        '考えられる解決策の一つは，何度も何度もコピーを作ることである。デジタルの資料を保管する図書館は，古い装置が壊れる前に，数年ごとにファイルを新しい保存装置へ移すことが多い。'
        'この作業は移行と呼ばれ，データを生き続けさせるが，多くの人が思っているよりはるかにお金と時間がかかり，危険がないわけでもない。ファイルが新しい形式に変換されるたびに，文字の書体や色，画像の位置といった細かい部分が変わることがあり，何度も変換するうちに，コピーは元のものとかなり違って見えるようになるかもしれない。'
        'もう一つの方法は，古いファイルを元の形のまま開けるように，古い機械を動く状態にしておくことだ。しかし，30年前のコンピュータの交換部品は見つけにくく，そうした機械を修理する方法を知っている人々も年をとってきている。'
        'そこで，俳優が別の世紀の人物を演じるのと同じように，古いコンピュータを今のコンピュータの上でまねるプログラムを使う機関もある。そのようなプログラムは，現在と過去をつなぐ一種の橋の役目を果たしている。',
        'しかし，技術だけでこの問題を解決することはできない。何を残すかを決めることは，どうやって残すかを決めることと同じくらい大切である。昔は，記録保管の専門家はすべての紙を保存することはできなかったので，注意深く選ばなければならず，その選択が，今日私たちが歴史について知っていることを形づくった。'
        '今では毎日生み出される情報の量があまりに膨大なので，そのすべてを残すことは不可能である。(g)皮肉なことに，私たちがデジタルの記録を簡単に作れるようになったことで，そのうちのどれを保存する価値があるかを決めるのは，簡単になるどころか，かえって難しくなった。'
        'かつては数十枚の写真を収めたアルバムを1冊だけ持っていた家族が，今では何万枚もの写真を電話やノートパソコンやオンラインのサービスにばらばらに持っていて，そのほとんどは二度と見られることがないだろう。',
        '一般の人々にもできることがある。マローフィールド研究所が成人2,000人に行った調査によると，前の1年間に自分の写真のバックアップを取っていたのはわずか14％で，半数近くは自分の大切な文書がどの形式で保存されているかを知らなかった。'
        '多くの回答者は，オンラインの保存サービスが，好きなだけ長くファイルを安全に保ってくれると信じていた。(h)しかし，そうしたサービスは事業であり，事業というものは規則を変えたり，料金を上げたり，すっかりやめてしまったりすることがある。'
        '数年前に人気のある写真サービスが終了したとき，利用者には写真をダウンロードするためにわずか2か月しか与えられず，その多くは知らせを受け取ることさえなかった。',
        'では，私たちはどうすればよいのだろうか。専門家はいくつかの簡単な習慣を勧めている。第一に，大切なものは少なくとも二つのコピーを作り，別々の場所に保管すること。第二に，未来のプログラマーにも理解できるように，広く使われていて中身が公開されている形式を選ぶこと。'
        '第三に，そしておそらく最も大切なことに，何を残すかをよく選ぶこと。ぼやけた写真や重複したファイルは消し，残すものにははっきりした名前と日付をつけること。最後に，印刷の価値を軽く見ないこと。大切な数枚の写真を紙に印刷したものは，あなたがこれから持つどの装置よりも長くもつかもしれないからだ。'
        '(l)私たちが後に残す記録は，私たちがどのような人間だったのかを未来の世代に伝えるだろう。だから，その物語が誰にも開けないファイルで終わってしまわないようにするのは，私たち次第である。',
    ],
}

P2 = {
    'points': 150,
    'intro': '次の英文は，一般の人々が科学の研究に参加する「市民科学」を紹介している。',
    'title': 'Counting Birds by the Lake',
    'passage': [
        "On a cold Saturday morning in January, about forty volunteers gathered at the edge of a lake near the town of Wexley. Some "
        "were retired teachers, some were high school students, and one was a seven-year-old girl who had come with her grandfather. "
        "None of them were professional scientists, but for the next three hours they did something that scientists badly needed: "
        "they counted birds. Each volunteer was given a notebook, a map of one section of the shore, and a simple guide with pictures "
        "of the most common species. {b:a} the morning ended, they had recorded more than 3,000 birds of 41 different kinds.",
        "This kind of activity is often called citizen science. {u:b|The idea is that ordinary people, working in large numbers, can "
        "collect information over an area far wider and a period far longer than any small team of researchers could manage on its "
        "own.} A single scientist can visit only a handful of places in a year, but thousands of volunteers spread across a country can "
        "observe what is happening almost everywhere at once. In this way, citizen science has helped researchers follow the movement "
        "of butterflies, map the spread of invasive plants, and measure changes in the timing of spring flowers.",
        "Citizen science is not new. Long before the word \"scientist\" existed, farmers kept careful records of the weather, and "
        "amateur astronomers {u:c|charted} the night sky with homemade telescopes. What has changed is the scale. Smartphones now allow "
        "almost anyone to take a photograph, record the exact location, and send both to a database in seconds. Some projects receive "
        "millions of reports every year. {u:d|In a sense, the phone in a volunteer's pocket has become a small laboratory that never "
        "closes.}",
        "Researchers in the Northvale Bird Survey analyzed reports sent by volunteers over twenty-five years. They found that eleven "
        "species had moved their winter homes an average of 80 kilometers to the north, a change that matched the rise in local "
        "temperatures. The survey's director, Dr. Imogen Pell, admits that her team could never have gathered such evidence alone. "
        "\"We had six staff members,\" she said. \"Our volunteers numbered more than 12,000. They were our eyes and ears.\"",
        "Not everyone was enthusiastic at first. Some scientists worried that data collected by amateurs would be {b:e} inaccurate "
        "to be trusted. A beginner might confuse two similar birds or count the same flock twice. These concerns are reasonable, but "
        "studies comparing volunteer data with measurements made by professionals have found that the two {b:f} closely in many "
        "cases. Projects have also found ways to reduce errors. Volunteers receive training, unusual reports are checked by experts, "
        "and computer programs flag numbers that seem too high or too low. {u:g|Moreover, when thousands of observations are combined, "
        "the random mistakes of individuals tend to cancel each other out, leaving a picture that is often surprisingly reliable.}",
        "Citizen science also benefits the volunteers themselves. Participants often say that they began to notice things they had "
        "never paid attention to before: the song of a bird outside the kitchen window, or the first leaves on a tree in their street. "
        "{u:h|Teachers have found that students who take part in such projects come to see science not as a list of facts in a "
        "textbook, but as an activity that they themselves can join.} For people who live far from universities and research centers, "
        "it offers a rare chance to contribute to real discoveries.",
        "Of course, volunteers cannot replace professional scientists. Someone still has to design the projects, analyze the data, and "
        "explain what the results mean. {u:i|But the relationship between experts and the public is gradually changing from one in "
        "which scientists speak and others listen to one in which both sides work together.} The girl who counted birds by the lake "
        "that January morning may never become a researcher. Still, she now knows that her careful observations can {b:j} something "
        "to what humanity understands about the world.",
    ],
    'notes': [(1, 'species', '（生物の）種'), (2, 'invasive', '外から入りこんで広がる'), (3, 'astronomer', '天文学者'),
              (3, 'telescope', '望遠鏡'), (5, 'flock', '（鳥の）群れ'), (5, 'flag', '目印をつけて知らせる'), (7, 'humanity', '人類')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（接続詞）', 'points': 8, 'stem': CH.format(x='a'),
         'options': ['Since', 'Unless', 'By the time', 'Although'], 'answer': 2,
         'expl': '主節が had recorded（過去完了）で，「朝の時間が終わるまでに3,000羽以上を記録していた」という意味になる。'
                 'by the time ~「〜するまでには」は，過去完了と組み合わせて「その時点までに完了していたこと」を表す。Unless（〜しない限り）・Although（〜だけれども）では意味が通らない。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': 'その考え方とは，一般の人々が大勢で取り組めば，研究者の小さなチームが自分たちだけで扱えるよりもはるかに広い地域とはるかに長い期間にわたって，情報を集めることができるというものである。',
         'expl': 'The idea is that ~「その考えとは〜ということだ」。working in large numbers は分詞構文で「大勢で取り組んで（取り組めば）」。'
                 'over an area far wider and a period far longer than ~ は，area と period の両方に比較級がかかっている。far は比較級を強める「はるかに」。'
                 'any small team of researchers could manage on its own「研究者のどんな小さなチームでも自分たちだけで扱える（範囲）」。',
         'criteria': [('The idea is that ~ の構文', 3), ('working in large numbers（分詞構文）', 4),
                      ('an area far wider and a period far longer than ~（比較の対象・far の強調）', 7), ('any small team ... could manage on its own', 4)]},
        {'kind': 'choice', 'marks': ['c'], 'tag': '語の意味', 'points': 8,
         'stem': '下線部（c）の語に意味が最も近いものを，（ア）〜（エ）から1つ選んで記号で書け。',
         'options': ['mapped', 'ignored', 'admired', 'painted'], 'answer': 0,
         'expl': 'chart は名詞では「図・海図」，動詞では「図に表す・記録する」。手作りの望遠鏡で夜空を観察して星の位置を図に記録した，という文脈なので mapped（地図・図にした）が近い。'
                 'admired（感心して眺めた）は記録の意味を含まない。'},
        {'kind': 'ja', 'marks': ['d'], 'tag': '内容説明', 'points': 22, 'lines': 4,
         'stem': '下線部（d）は，どのようなことを表しているか。本文の内容に沿って日本語で説明せよ。',
         'answer': 'スマートフォンを使えば，ほとんど誰でも写真を撮り，正確な場所を記録し，それを数秒でデータベースに送ることができる。そのため，ボランティアはいつでもどこでも研究室のように観察の記録を集めて研究に役立てることができる，ということ。',
         'expl': 'laboratory（研究室）＝データを集める場所，never closes（決して閉まらない）＝いつでも使える，というたとえ。'
                 '直前の Smartphones now allow almost anyone to take a photograph, record the exact location, and send both to a database in seconds が具体的な中身。'
                 '「スマホでできること（撮影・位置の記録・送信）」と「いつでも・誰でも研究のデータを集められる」の両方を書く。',
         'criteria': [('スマートフォンで写真を撮り，場所を記録できる', 6), ('数秒でデータベースに送れる', 6),
                      ('ほとんど誰でもできる', 4), ('いつでも（休みなく）研究のためのデータを集められる，というたとえの説明', 6)]},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第④段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['The Northvale Bird Survey studied reports from volunteers collected over a quarter of a century.',
                        'According to the survey, eleven species had moved their winter homes about 80 kilometers to the south.',
                        'The director believes that her staff could have collected the same evidence without any volunteers.',
                        'The survey had far more volunteers than staff members.'],
         'answers': ['〇', '×', '×', '〇'],
         'expl': '（ア）twenty-five years（25年）＝a quarter of a century なので〇。（イ）to the north（北へ）なので×。'
                 '（ウ）could never have gathered such evidence alone（自分たちだけでは決して集められなかった）とあるので×。（エ）職員6人に対しボランティアは12,000人以上なので〇。各4点。'},
        {'kind': 'combo', 'marks': ['e', 'f'], 'tag': '空所補充（語の組み合わせ）', 'points': 10, 'stem': CO.format(x='e ）・（ f'),
         'rows': [('so', 'differ'), ('too', 'differ'), ('so', 'agree'), ('too', 'agree')], 'answer': 3,
         'expl': '（e）直後の inaccurate to be trusted から，too ~ to …「…するには〜すぎる」の too が入る（「信頼するには不正確すぎる」）。so だと so ~ that … の形になる。'
                 '（f）直前の These concerns are reasonable, but（そうした心配はもっともだが）から，心配を打ち消す内容が続く。ボランティアのデータと専門家の測定が「よく一致する」ので agree。'},
        {'kind': 'ja', 'marks': ['g'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='g'), 'lines': 3,
         'answer': 'さらに，何千もの観察が組み合わされると，一人ひとりの偶然のまちがいはたがいに打ち消し合う傾向があり，その結果，おどろくほど信頼できることが多い全体像が残る。',
         'expl': 'tend to ~「〜する傾向がある」。cancel each other out「たがいに打ち消し合う」。leaving a picture that ~ は結果を表す分詞構文で「（その結果）〜な全体像を残す」。'
                 'picture は「絵」ではなく「全体像・状況」。random mistakes は「でたらめな（偶然の）まちがい」。',
         'criteria': [('when thousands of observations are combined', 4), ('the random mistakes of individuals tend to cancel each other out', 6),
                      ('leaving a picture ...（結果の分詞構文）', 5), ('that is often surprisingly reliable', 3)]},
        {'kind': 'ja', 'marks': ['h'], 'tag': '内容説明', 'points': 24, 'lines': 4,
         'stem': '下線部（h）によると，市民科学に参加した生徒たちは，科学に対する見方がどのように変わるか。変わる前と後がわかるように，日本語で説明せよ。',
         'answer': '参加する前は，科学を教科書に書かれた事実を並べたものと考えていたが，参加すると，科学を自分たちも加わることのできる活動として見るようになる。',
         'expl': 'see ～ not as … but as －「～を…としてではなく－として見る」の構文。come to ~ は「〜するようになる」で，変化を表す。'
                 '変わる前＝a list of facts in a textbook（教科書の中の事実の一覧），変わった後＝an activity that they themselves can join（自分たち自身が加われる活動）。'
                 '「前」と「後」の両方を書くこと。',
         'criteria': [('変わる前：教科書の中の事実の一覧（覚えるもの）', 8), ('変わった後：自分たちも加われる（参加できる）活動', 10),
                      ('come to ~ の変化を表している', 6)]},
        {'kind': 'ja', 'marks': ['i'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='i'), 'lines': 3,
         'answer': 'しかし，専門家と一般の人々の関係は，科学者が話して他の人々が聞くという関係から，両者がいっしょに取り組むという関係へと，少しずつ変わりつつある。',
         'expl': 'change from ～ to …「～から…へ変わる」。～・…にあたるのは one in which ~ で，one は relationship の代わり，in which は関係代名詞（「その中で〜する関係」）。'
                 '「科学者が話し他の人が聞く関係」から「両者が協力する関係」へ，と対比をはっきり訳す。',
         'criteria': [('the relationship between experts and the public', 3), ('is gradually changing from ～ to …', 5),
                      ('one in which scientists speak and others listen（one＝relationship，関係代名詞）', 5), ('one in which both sides work together', 5)]},
        {'kind': 'choice', 'marks': ['j'], 'tag': '空所補充（語の選択）', 'points': 8, 'stem': CH.format(x='j'),
         'options': ['owe', 'lose', 'add', 'lend'], 'answer': 2,
         'expl': 'add A to B「A を B に加える」。「自分の注意深い観察が，人類が世界について理解していることに何かを加えられる（＝貢献できる）」という意味になる。'
                 'lose（失う）は逆の意味で，owe A to B は「A は B のおかげだ」となり文脈に合わない。'},
    ],
    'translation': [
        '1月のある寒い土曜日の朝，40人ほどのボランティアが，ウェクスリーという町の近くの湖のほとりに集まった。退職した教師もいれば高校生もいて，祖父といっしょに来た7歳の女の子も一人いた。'
        '彼らの中にプロの科学者は一人もいなかったが，それから3時間，科学者たちがどうしても必要としていることをした。鳥を数えたのである。ボランティアはそれぞれ，ノートと，岸辺の一区画の地図と，よく見られる種の絵がのった簡単な案内を渡された。'
        '朝の時間が終わるまでに，彼らは41種類，3,000羽以上の鳥を記録していた。',
        'この種の活動は，よく市民科学と呼ばれる。(b)その考え方とは，一般の人々が大勢で取り組めば，研究者の小さなチームが自分たちだけで扱えるよりもはるかに広い地域とはるかに長い期間にわたって，情報を集めることができるというものである。'
        '一人の科学者が1年に訪れることができる場所はほんのわずかだが，国中に散らばった何千人ものボランティアは，ほとんどあらゆる場所で起きていることを同時に観察できる。'
        'こうして市民科学は，研究者がチョウの移動を追ったり，外から入りこんだ植物の広がりを地図にしたり，春の花が咲く時期の変化を測ったりするのに役立ってきた。',
        '市民科学は新しいものではない。「科学者」という言葉が生まれるずっと前から，農民は天気を注意深く記録し，アマチュアの天文学者は手作りの望遠鏡で夜空を図に記していた。'
        '変わったのはその規模である。今ではスマートフォンのおかげで，ほとんど誰でも写真を撮り，正確な場所を記録し，その両方を数秒でデータベースに送ることができる。毎年何百万件もの報告を受け取る計画もある。'
        '(d)ある意味で，ボランティアのポケットの中の電話は，決して閉まることのない小さな研究室になったのだ。',
        'ノースベール鳥類調査の研究者たちは，ボランティアが25年にわたって送った報告を分析した。その結果，11種の鳥が冬を過ごす場所を平均80キロメートル北へ移していたことがわかった。それはその地域の気温の上昇と一致する変化だった。'
        '調査の責任者であるイモジェン・ペル博士は，自分のチームだけでは決してそのような証拠を集められなかったと認めている。「職員は6人でした」と彼女は言った。「ボランティアは12,000人を超えていました。彼らが私たちの目となり耳となってくれたのです。」',
        '初めから誰もが乗り気だったわけではない。アマチュアが集めたデータは不正確すぎて信頼できないのではないかと心配する科学者もいた。初心者は似た2種類の鳥をとりちがえたり，同じ群れを2回数えたりするかもしれない。'
        'そうした心配はもっともだが，ボランティアのデータと専門家による測定を比べた研究では，多くの場合，両者がよく一致することがわかっている。計画の側も，まちがいを減らす方法を見つけてきた。ボランティアは研修を受け，めずらしい報告は専門家が確認し，コンピュータのプログラムが多すぎたり少なすぎたりする数に目印をつける。'
        '(g)さらに，何千もの観察が組み合わされると，一人ひとりの偶然のまちがいはたがいに打ち消し合う傾向があり，その結果，おどろくほど信頼できることが多い全体像が残る。',
        '市民科学はボランティア自身のためにもなる。参加者たちは，それまで気にとめたことのなかったものに気づくようになったとよく言う。台所の窓の外の鳥の歌声や，近所の通りの木に出た最初の葉などである。'
        '(h)教師たちは，こうした計画に参加する生徒が，科学を教科書の中の事実の一覧としてではなく，自分たち自身も加わることのできる活動として見るようになることに気づいている。'
        '大学や研究所から遠く離れて暮らす人々にとって，市民科学は本物の発見に貢献するめったにない機会を与えてくれる。',
        'もちろん，ボランティアがプロの科学者に取って代わることはできない。計画を立て，データを分析し，結果が何を意味するのかを説明する人は，やはり必要である。'
        '(i)しかし，専門家と一般の人々の関係は，科学者が話して他の人々が聞くという関係から，両者がいっしょに取り組むという関係へと，少しずつ変わりつつある。'
        'あの1月の朝に湖のほとりで鳥を数えた女の子は，研究者にはならないかもしれない。それでも彼女は今，自分の注意深い観察が，人類が世界について理解していることに何かを加えられるのだと知っている。',
    ],
}
