# -*- coding: utf-8 -*-
# 群馬大学 情報学部 第2回 大問1・大問2（書き下ろし。人物・団体・地名・調査・数値は架空）
from j1a import CH, CO, TR

P1 = {
    'points': 150,
    'intro': '次の英文は，都市の暑さと街路樹の役割を論じている。',
    'title': 'Cooling Cities with Trees',
    'passage': [
        "On a hot afternoon in August, the temperature in the center of a large city can be several degrees higher than in the "
        "countryside only a short drive away. Roads, rooftops, and parking lots absorb sunlight during the day and release the heat "
        "slowly at night, so that even after sunset the streets remain uncomfortably warm. Scientists call this effect the urban heat "
        "island. {b:a} summers grow hotter around the world, the problem is no longer a matter of comfort alone. {u:b|In several recent "
        "heat waves, the number of residents taken to hospital rose sharply in neighborhoods with few green spaces, while areas with parks "
        "and tree-lined streets suffered far less.}",
        "Trees cool a city in two ways. First, their leaves block sunlight, so the ground beneath them stays cooler. Second, trees "
        "release water vapor through their leaves, a process that works rather like sweating in humans: as the water evaporates, it "
        "takes heat away from the surrounding air. A study carried out in the city of Calbridge measured surface temperatures on a "
        "summer afternoon and found that a sidewalk in full sun reached 52 degrees Celsius, while a sidewalk under a large tree only a "
        "few meters away stayed at 31 degrees. {u:c|For a person waiting at a bus stop, that difference can decide whether the wait is "
        "merely unpleasant or actually dangerous.}",
        "Planting trees sounds simple, but it is {b:d} easy as it seems. A young tree needs regular watering for its first few years, "
        "and many die before they grow large enough to provide much shade. Roots can damage pipes and pavements, and falling leaves "
        "block drains in autumn. In crowded city centers, there is often little space above or below the ground: electric cables run "
        "overhead, and water and gas pipes fill the soil. For these reasons, some city officials have been {b:e} to plant trees, "
        "preferring cheaper solutions such as painting roofs white so that they reflect sunlight.",
        "Yet the benefits of trees go well beyond cooling. They clean the air by catching dust, reduce the risk of flooding by slowing "
        "rainwater, and provide homes for birds and insects. Researchers have also found that people who can see trees from their "
        "windows report lower levels of stress. In one hospital, patients whose rooms looked out on a garden {u:f|recovered} from "
        "surgery slightly faster and asked for less pain medicine than patients whose windows faced a brick wall. {u:g|When all of these "
        "advantages are taken into account, a tree that costs a few hundred dollars to plant may return several times that amount in "
        "value over its lifetime.}",
        "In 2019 the city of Ferncastle set a goal of increasing the share of its land shaded by branches and leaves from 18 percent to "
        "30 percent within fifteen years. Instead of planting trees mainly in parks, the city focused on its poorest districts, where "
        "tree cover was lowest and summer temperatures were highest. Volunteers helped by watering young trees near their homes, and "
        "local schools adopted trees on nearby streets and took care of them. By 2025, tree cover had reached 23 percent, and surveys "
        "showed that residents of the targeted districts felt more attached to their neighborhoods than before.",
        "{u:h|Of course, trees are not a magic solution.} They take decades to reach full size, so a city that begins planting today will "
        "not feel the full effect for many years. Cities must also choose species that will {b:i} the hotter and drier summers expected "
        "in the future, not only the conditions of today. Still, most experts agree that trees are among the most effective tools that "
        "cities have, and that the cost of doing nothing will keep rising. {u:j|Cities that start planting now may not see the full "
        "results for a generation, but those that wait will find themselves with even fewer choices when the heat arrives.}",
    ],
    'notes': [(1, 'urban heat island', 'ヒートアイランド（都市の高温化）'), (1, 'heat wave', '熱波'), (2, 'water vapor', '水蒸気'),
              (2, 'evaporate', '蒸発する'), (3, 'drain', '排水口'), (4, 'surgery', '手術'), (5, 'adopt', '（世話をするために）引き受ける'),
              (6, 'species', '（生物の）種')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（接続詞）', 'points': 8, 'stem': CH.format(x='a'),
         'options': ['As', 'Unless', 'Before', 'Whether'], 'answer': 0,
         'expl': '「世界中で夏が暑くなるにつれて，この問題はもはや快適さだけの問題ではなくなっている」という意味にする。比例・変化を表す as「〜するにつれて」が入る。'
                 'Unless（〜しない限り）や Before（〜する前に）では意味が通らない。Whether は名詞節や「〜であろうとなかろうと」を表し，ここには合わない。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': '最近のいくつかの熱波では，緑地の少ない地区で病院に運ばれた住民の数が急に増えたが，公園や並木道のある地域では被害がはるかに少なかった。',
         'expl': 'the number of residents taken to hospital「病院に運ばれた住民の数」は，taken 以下が residents を後ろから修飾する過去分詞。rose sharply「急増した」。'
                 'while は「〜する一方で」と対比を表す。suffered far less は「（被害を）はるかに少なくしか受けなかった」なので，「被害がずっと少なかった」と訳すと自然。',
         'criteria': [('In several recent heat waves', 2), ('the number of residents taken to hospital rose sharply（過去分詞の修飾・急増）', 6),
                      ('in neighborhoods with few green spaces', 4), ('while 以下の対比と suffered far less', 6)]},
        {'kind': 'ja', 'marks': ['c'], 'tag': '内容説明', 'points': 20, 'lines': 4,
         'stem': '下線部（c）の “that difference” の中身を数値を使って示し，筆者がなぜそれを大きな違いだと考えているのか，日本語で説明せよ。',
         'answer': '夏の午後，日なたの歩道は52度にまで達したのに，数メートルしか離れていない大きな木の下の歩道は31度にとどまったという，20度以上の温度の差。'
                   'バスを待つ人にとっては，この差によって，待つことが単に不快なだけで済むか，体に危険がおよぶほどになるかが分かれるから。',
         'expl': 'that difference は直前の文の「日なたの歩道 52度」と「木の下の歩道 31度」の差を指す。数字を入れて具体的に書くこと。'
                 'decide whether ~ or …「〜か…かを決める」。merely unpleasant（単に不快）と actually dangerous（実際に危険）の対比を説明に入れる。',
         'criteria': [('日なたの歩道が52度', 4), ('数メートル先の木の下の歩道は31度（約20度の差）', 6),
                      ('バスを待つ人などにとって', 2), ('不快で済むか危険になるかが分かれる', 8)]},
        {'kind': 'combo', 'marks': ['d', 'e'], 'tag': '空所補充（語の組み合わせ）', 'points': 10, 'stem': CO.format(x='d ）・（ e'),
         'rows': [('as', 'eager'), ('not as', 'eager'), ('as', 'reluctant'), ('not as', 'reluctant')], 'answer': 3,
         'expl': '（d）直前の but と，続く段落で「水やり・根が管を傷める・場所がない」と難しさを並べていることから，not as を入れて「見かけほど簡単ではない」とする。'
                 '（e）そうした理由で，屋根を白く塗るなどの安い方法を好むのだから，木を植えることには reluctant（気が進まない）。eager（熱心な）は逆の意味になる。'},
        {'kind': 'choice', 'marks': ['f'], 'tag': '語の意味', 'points': 8,
         'stem': '下線部（f）の語に意味が最も近いものを，（ア）〜（エ）から1つ選んで記号で書け。',
         'options': ['complained', 'moved out', 'got better', 'grew weaker'], 'answer': 2,
         'expl': 'recover from ~ は「（病気・けが）から回復する」。手術のあと庭の見える部屋の患者のほうが少し早く回復し，痛み止めも少なくてすんだ，という文脈なので got better（よくなった）が近い。'
                 'grew weaker（弱った）は反対の意味になる。'},
        {'kind': 'ja', 'marks': ['g'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='g'), 'lines': 3,
         'answer': 'これらの利点をすべて考えに入れると，植えるのに数百ドルかかる木は，その一生の間に，その何倍もの価値をもたらすかもしれない。',
         'expl': 'When all of these advantages are taken into account は take ~ into account「〜を考慮する」の受け身。'
                 'a tree that costs a few hundred dollars to plant「植えるのに数百ドルかかる木」。cost ~ to …「…するのに〜がかかる」。'
                 'return several times that amount in value「その額の何倍もの価値を返す」。that amount は「数百ドル」を指す。over its lifetime「その一生（寿命）の間に」。',
         'criteria': [('take ~ into account の受け身', 4), ('a tree that costs a few hundred dollars to plant', 5),
                      ('return several times that amount in value（that amount の内容）', 6), ('over its lifetime', 3)]},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第⑤段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['Ferncastle hoped to raise its tree cover to 30 percent within fifteen years.',
                        'The city planted most of its new trees in its wealthiest districts.',
                        'Some schools looked after trees growing on streets close to them.',
                        'By 2025 the city had already reached the goal it set in 2019.'],
         'answers': ['〇', '×', '〇', '×'],
         'expl': '（ア）from 18 percent to 30 percent within fifteen years に合うので〇。（イ）focused on its poorest districts（最も貧しい地区）なので×。'
                 '（ウ）local schools adopted trees on nearby streets and took care of them に合うので〇。（エ）2025年は23％で，目標の30％には届いていないので×。各4点。'},
        {'kind': 'ja', 'marks': ['h'], 'tag': '内容説明', 'points': 20, 'lines': 4,
         'stem': '下線部（h）のように筆者が述べる理由として，第⑥段落で挙げられていることを2つ，日本語で説明せよ。',
         'answer': '一つは，木が大きく育つまでに何十年もかかるので，今植え始めた都市でも，効果が十分に感じられるのは何年も先になること。'
                   'もう一つは，今の気候だけでなく，将来予想されるもっと暑く乾いた夏にも耐えられる種類の木を選ばなければならないこと。',
         'expl': 'magic solution は「（それさえあればすべて解決する）魔法の解決策」。直後の2文が理由にあたる。'
                 '①They take decades to reach full size ...（育つのに数十年かかり，効果が出るのは何年も先），②choose species that will ... the hotter and drier summers expected in the future（将来の暑さに耐える種を選ぶ必要）。',
         'criteria': [('木が大きくなるまでに数十年かかる', 5), ('そのため効果が十分に出るのは何年も先', 5),
                      ('将来のもっと暑く乾いた夏に耐える種類を選ぶ必要がある', 10)]},
        {'kind': 'choice', 'marks': ['i'], 'tag': '空所補充（語の選択）', 'points': 8, 'stem': CH.format(x='i'),
         'options': ['cause', 'survive', 'predict', 'avoid'], 'answer': 1,
         'expl': '都市が選ぶべきなのは，将来のもっと暑く乾いた夏を「生きのびる（耐えぬく）」ことのできる種類の木なので survive が入る。'
                 '木が夏を cause（引き起こす）や predict（予測する）ことはなく，avoid（避ける）こともできない。'},
        {'kind': 'ja', 'marks': ['j'], 'tag': '下線部和訳', 'points': 14, 'stem': TR.format(x='j'), 'lines': 3,
         'answer': '今，木を植え始める都市は，一世代の間，十分な成果を目にすることはないかもしれないが，待っている都市は，暑さがやって来たときに，さらに選べる道が少なくなっていることに気づくだろう。',
         'expl': 'Cities that start planting now と those that wait の対比。those は cities の代わり。for a generation「一世代の間（約30年）」。'
                 'find oneself with ~「（気がつくと）〜をかかえている」。even fewer choices「さらに少ない選択肢」。even は比較級を強める。',
         'criteria': [('Cities that start planting now may not see the full results for a generation', 5),
                      ('those（＝cities）that wait との対比', 3), ('find themselves with even fewer choices（even の強調）', 4), ('when the heat arrives', 2)]},
        {'kind': 'choice', 'tag': '主旨', 'points': 10,
         'stem': '本文全体の主旨としてふさわしいものを，（ア）〜（エ）から1つ選んで記号で書け。',
         'options': ['Painting roofs white is a cheaper and better way to cool cities than planting trees.',
                     'Although planting trees involves difficulties and takes time, trees are among the most valuable ways to protect cities from heat.',
                     'Trees in cities cause more problems than they solve because their roots damage pipes.',
                     'Only poor districts suffer from the urban heat island, so trees should be planted only there.'],
         'answer': 1,
         'expl': '第③段落で難しさ，第④段落で冷やす以外の利点，第⑥段落で「魔法の解決策ではないが最も効果的な道具の一つ」と述べているので（イ）。'
                 '（ア）屋根を白く塗るのは一部の役人が好む安い方法として紹介されているだけ。（ウ）第④段落の利点に反する。（エ）本文にない。'},
    ],
    'translation': [
        '8月の暑い午後，大都市の中心部の気温は，車で少し走っただけの郊外よりも数度高くなることがある。道路や屋根や駐車場は昼の間に日光を吸収し，夜になってゆっくりと熱を放出するので，日が沈んだあとでさえ通りは不快なほど暖かいままである。'
        '科学者はこの現象をヒートアイランドと呼ぶ。世界中で夏が暑くなるにつれて，この問題はもはや快適さだけの問題ではなくなっている。'
        '(b)最近のいくつかの熱波では，緑地の少ない地区で病院に運ばれた住民の数が急に増えたが，公園や並木道のある地域では被害がはるかに少なかった。',
        '木は二つの方法で都市を冷やす。第一に，葉が日光をさえぎるので，その下の地面は涼しいままである。第二に，木は葉から水蒸気を出す。これは人間が汗をかくのとよく似たはたらきで，水が蒸発するときにまわりの空気から熱をうばう。'
        'カルブリッジ市で行われたある研究では，夏の午後に地表の温度を測ったところ，日なたの歩道は摂氏52度に達したが，ほんの数メートル離れた大きな木の下の歩道は31度にとどまった。'
        '(c)バス停で待っている人にとって，その違いは，待つことが単に不快なだけで済むか，実際に危険なものになるかを分けることがある。',
        '木を植えるのは簡単そうに聞こえるが，見かけほど簡単ではない。若い木は最初の数年間は定期的に水をやる必要があり，十分な日陰を作れるほど大きくなる前に枯れてしまうものも多い。'
        '根は管や舗装を傷めることがあり，秋には落ち葉が排水口をふさぐ。混み合った都心では，地上にも地下にもほとんど場所がないことが多い。頭上には電線が通り，土の中は水道管やガス管でいっぱいなのだ。'
        'こうした理由から，木を植えることに気が進まず，日光を反射させるために屋根を白く塗るといった安い方法を好む市の役人もいる。',
        'しかし，木の利点は冷やすことだけにとどまらない。木はほこりをとらえて空気をきれいにし，雨水の流れをゆるやかにして洪水の危険を減らし，鳥や虫にすみかを与える。'
        '研究者たちはまた，窓から木が見える人々はストレスの度合いが低いと答えることも発見した。ある病院では，部屋から庭が見える患者は，窓がれんがの壁に面している患者よりも，手術から少し早く回復し，痛み止めの薬を求めることも少なかった。'
        '(g)これらの利点をすべて考えに入れると，植えるのに数百ドルかかる木は，その一生の間に，その何倍もの価値をもたらすかもしれない。',
        '2019年，ファーンキャッスル市は，枝や葉で日陰になる土地の割合を，15年以内に18％から30％に増やすという目標を立てた。市は主に公園に木を植えるのではなく，木の覆う割合が最も低く，夏の気温が最も高い，最も貧しい地区に力を入れた。'
        'ボランティアは自宅の近くの若い木に水をやって手伝い，地元の学校は近くの通りの木を引き受けて世話をした。2025年までに木の覆う割合は23％に達し，調査では，対象となった地区の住民が以前よりも自分の地域に愛着を感じるようになったことがわかった。',
        '(h)もちろん，木は魔法の解決策ではない。木が十分な大きさになるには何十年もかかるので，今日植え始める都市が十分な効果を感じるのは何年も先のことになる。'
        '都市はまた，今日の気候だけでなく，将来予想されるもっと暑く乾いた夏を生きのびることのできる種類を選ばなければならない。それでも，ほとんどの専門家は，木は都市が持っている最も効果的な道具の一つであり，何もしないことの代償は上がり続けるという点で一致している。'
        '(j)今，木を植え始める都市は，一世代の間，十分な成果を目にすることはないかもしれないが，待っている都市は，暑さがやって来たときに，さらに選べる道が少なくなっていることに気づくだろう。',
    ],
}

P2 = {
    'points': 150,
    'intro': '次の英文は，失敗した製品を集めた小さな博物館を紹介している。',
    'title': 'A Museum of Mistakes',
    'passage': [
        "In a quiet corner of the city of Halbrook stands a small museum with an unusual collection. Instead of famous inventions that "
        "changed the world, it displays products that failed: a toothbrush that played music but broke after a week, a folding bicycle "
        "that was too heavy to carry, and a type of frozen dinner that nobody wanted to eat. The museum was founded by Dr. Selwyn Orme, a "
        "retired engineer who spent forty years designing household goods. {b:a} he first proposed the idea, many of his former "
        "colleagues laughed. \"Why would anyone pay to look at mistakes?\" one of them asked.",
        "Dr. Orme's answer was simple. {u:b|In his experience, people learn far more from a product that did not work than from one that "
        "did, because a failure forces them to ask questions that a success allows them to ignore.} When something sells well, companies "
        "rarely stop to think about why. When something fails, they have no choice but to look closely at every decision that led to "
        "the disaster.",
        "Many of the objects in the museum failed not because they were badly made but because their designers misunderstood the people "
        "who would use them. The musical toothbrush, for example, was carefully engineered, and its sound quality was excellent. {b:c}, "
        "its makers never asked whether adults wanted music while they brushed their teeth. Most did not. Similarly, the frozen dinner "
        "was healthy and cheap, but it came in a gray box that made the food look {b:d} appetizing than it really was.",
        "Visitors are encouraged to handle some of the products and to write their own ideas on cards placed next to each display. "
        "{u:e|A board near the exit is covered with these cards, and Dr. Orme reads every one of them.} Some suggest small changes, such as "
        "a lighter frame for the bicycle; others propose entirely new uses for the failed products. A group of high school students once "
        "suggested that the musical toothbrush could help young children brush for the recommended two minutes, since a song of that "
        "length would tell them when to stop. Dr. Orme liked the idea so much that he mailed it to a toothbrush maker, although he "
        "has not received a reply yet.",
        "The museum now receives about 9,000 visitors a year, more than a third of them in school groups. Several companies send their "
        "new employees there as part of their training. One manager explained that her company wanted young designers to understand that "
        "failure is a normal part of creating something new, not a reason to feel ashamed. Since the visits began, she said, her team had "
        "become more willing to share early ideas, even ones that might not work. Some teachers also use the visit to start class discussions about how everyday products could be "
        "designed better.",
        "Not everyone agrees with Dr. Orme's approach. Some critics argue that celebrating failure may make people {u:f|careless}, as if "
        "mistakes did not matter. Dr. Orme rejects this view. {u:g|What he wants to celebrate, he says, is not failure itself but the "
        "courage to try something whose outcome is uncertain, together with the honesty to admit what went wrong.} A designer who never "
        "fails, in his opinion, is probably not attempting anything new.",
        "{u:h|The museum also has a lesson for students.} Many young people are afraid of giving a wrong answer in class, so they stay "
        "silent even when they have an interesting idea. Dr. Orme hopes that a visit to his museum will help them see mistakes "
        "differently. {u:i|After all, every product that people now use without thinking was once an idea that might have failed, and "
        "someone had to be brave enough to find out.} He keeps one more item in a glass case at the entrance: a notebook from his first "
        "year as an engineer, filled with designs that never {b:j} the factory.",
    ],
    'notes': [(1, 'household goods', '家庭用品'), (2, 'disaster', '大失敗'), (3, 'engineer', '設計・製作する'),
              (3, 'appetizing', 'おいしそうな'), (6, 'outcome', '結果')],
    'questions': [
        {'kind': 'choice', 'marks': ['a'], 'tag': '空所補充（接続詞）', 'points': 8, 'stem': CH.format(x='a'),
         'options': ['Unless', 'So that', 'When', 'Even if'], 'answer': 2,
         'expl': '「彼が最初にその考えを提案したとき，元同僚の多くは笑った」という時を表す文にする。When が入る。'
                 'Unless（〜しない限り）・So that（〜するように）・Even if（たとえ〜でも）は，過去の一度の出来事を述べるこの文には合わない。'},
        {'kind': 'ja', 'marks': ['b'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='b'), 'lines': 3,
         'answer': '彼の経験では，人はうまくいった製品よりもうまくいかなかった製品からはるかに多くのことを学ぶ。というのも，失敗は，成功なら無視させてくれるような問いを，人に考えさせずにはおかないからである。',
         'expl': 'learn far more from ~ than from …「…からよりも〜からはるかに多くを学ぶ」。one that did は a product that worked の言いかえ（did＝worked）。'
                 'force ~ to …「〜に…することを強いる」，allow ~ to …「〜に…させておく」。questions that a success allows them to ignore は「成功なら彼らに無視させておく問い」。'
                 'force と allow の対比をはっきり訳すこと。',
         'criteria': [('In his experience', 2), ('learn far more from ~ than from one that did（one・did の内容）', 6),
                      ('a failure forces them to ask questions', 5), ('that a success allows them to ignore（関係代名詞・対比）', 5)]},
        {'kind': 'combo', 'marks': ['c', 'd'], 'tag': '空所補充（語の組み合わせ）', 'points': 10, 'stem': CO.format(x='c ）・（ d'),
         'rows': [('Therefore', 'more'), ('However', 'more'), ('Therefore', 'less'), ('However', 'less')], 'answer': 3,
         'expl': '（c）前の文は「歯ブラシはていねいに作られ，音質もすばらしかった」，後ろは「大人が歯をみがきながら音楽を聞きたいかを作り手は一度もたずねなかった」。前後が逆の流れなので However。'
                 '（d）灰色の箱のせいで，料理が実際より「おいしくなさそうに」見えたので less appetizing。'},
        {'kind': 'ja', 'marks': ['e'], 'tag': '内容説明', 'points': 22, 'lines': 4,
         'stem': '下線部（e）の “these cards” には，どのようなことが書かれているか。本文に挙げられている例を含めて，日本語で説明せよ。',
         'answer': '来館者が，展示されている失敗した製品について自分の考えを書いたもので，自転車の骨組みを軽くするといった小さな改良の提案や，製品のまったく新しい使い道の提案が書かれている。'
                   'たとえば，高校生のグループは，音楽の鳴る歯ブラシを使えば，2分間の曲が終わるまでみがくことで，小さな子どもが勧められている時間だけ歯をみがけると提案した。',
         'expl': 'these cards は前の文の cards placed next to each display（各展示の横に置かれたカード）で，来館者が自分の考えを書いたもの。'
                 '直後の Some suggest ... ; others propose ... で中身が2種類（小さな改良・新しい使い道）に分けて説明され，最後の文が具体例になっている。',
         'criteria': [('来館者が失敗した製品について自分の考えを書いたもの', 4), ('小さな改良の提案（自転車の骨組みを軽くする）', 6),
                      ('製品のまったく新しい使い道の提案', 4), ('高校生の例（歌の長さで子どもが2分間みがける）', 8)]},
        {'kind': 'tf', 'tag': '内容一致', 'points': 16,
         'stem': '次の（ア）〜（エ）の英文について，第⑤段落の内容に合っていれば〇，合っていなければ×を書け。',
         'statements': ['School groups account for over a third of all visitors to the museum.',
                        'Fewer than 1,000 people visit the museum each year.',
                        'Some companies send newly hired workers to the museum as part of their training.',
                        'The manager said her team had become less willing to talk about ideas that might fail.'],
         'answers': ['〇', '×', '〇', '×'],
         'expl': '（ア）more than a third of them in school groups に合うので〇。（イ）about 9,000 visitors a year なので×。'
                 '（ウ）Several companies send their new employees there as part of their training に合うので〇。（エ）more willing to share early ideas（より進んで話すようになった）なので×。各4点。'},
        {'kind': 'choice', 'marks': ['f'], 'tag': '語の意味', 'points': 8,
         'stem': '下線部（f）の語に意味が最も近いものを，（ア）〜（エ）から1つ選んで記号で書け。',
         'options': ['not paying enough attention', 'thoughtful', 'confident', 'well prepared'], 'answer': 0,
         'expl': 'careless は「不注意な，いいかげんな」。直後の as if mistakes did not matter（まちがいなど大したことではないかのように）から，注意をはらわなくなる，という意味だとわかる。'
                 'thoughtful（よく考える）・well prepared（準備のよい）は反対の意味になる。'},
        {'kind': 'ja', 'marks': ['g'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='g'), 'lines': 3,
         'answer': '彼が言うには，自分がたたえたいのは失敗そのものではなく，結果がどうなるかわからないことに挑戦する勇気と，何がうまくいかなかったのかを認める正直さなのである。',
         'expl': 'What he wants to celebrate ... is not ～ but …「彼がたたえたいものは～ではなく…だ」。he says は挿入で「彼が言うには」。'
                 'something whose outcome is uncertain「結果が不確かなこと」の whose は所有格の関係代名詞。together with ~「〜とともに」。admit what went wrong「何がまずかったのかを認める」。',
         'criteria': [('What he wants to celebrate ... is not ～ but …（he says の挿入を含む）', 6), ('failure itself', 2),
                      ('the courage to try something whose outcome is uncertain', 6), ('the honesty to admit what went wrong', 4)]},
        {'kind': 'ja', 'marks': ['h'], 'tag': '内容説明', 'points': 24, 'lines': 4,
         'stem': '下線部（h）の “a lesson” とはどのような教えか。第⑦段落の内容に沿って，日本語で説明せよ。',
         'answer': '授業でまちがった答えを言うのを恐れて，おもしろい考えがあっても黙ってしまう生徒に対して，まちがいの見方を変え，失敗するかもしれなくても思いきって考えを口にしたり試したりすることの大切さを教えるということ。'
                   '今では当たり前に使われている製品も，かつては失敗するかもしれない考えで，誰かが勇気を出して試したからこそ生まれたのだという教え。',
         'expl': '生徒の問題点（まちがいを恐れて黙る）→博物館で期待すること（まちがいの見方を変える）→理由（今使われている製品も，かつては失敗したかもしれない考えで，誰かが勇気を出して確かめた），という流れをまとめる。',
         'criteria': [('生徒はまちがいを恐れて，考えがあっても黙ってしまう', 6), ('まちがいの見方を変える（失敗を恐れず考えを出す）', 8),
                      ('今の製品もかつては失敗したかもしれない考えだった', 6), ('誰かが勇気を出して試した', 4)]},
        {'kind': 'ja', 'marks': ['i'], 'tag': '下線部和訳', 'points': 18, 'stem': TR.format(x='i'), 'lines': 3,
         'answer': '結局のところ，今では人々が何も考えずに使っているどの製品も，かつては失敗していたかもしれない考えだったのであり，誰かが勇気を出してそれを確かめなければならなかったのだ。',
         'expl': 'After all「結局のところ，なにしろ」。every product that people now use without thinking「人々が今，何も考えずに使っているあらゆる製品」。'
                 'an idea that might have failed は might have ＋過去分詞で「（過去に）失敗したかもしれない考え」。brave enough to find out「確かめるのに十分なほど勇敢な」。',
         'criteria': [('After all', 2), ('every product that people now use without thinking', 5),
                      ('was once an idea that might have failed（might have＋過去分詞）', 6), ('someone had to be brave enough to find out', 5)]},
        {'kind': 'choice', 'marks': ['j'], 'tag': '空所補充（語の選択）', 'points': 8, 'stem': CH.format(x='j'),
         'options': ['reached', 'left', 'closed', 'visited'], 'answer': 0,
         'expl': '技術者1年目のノートには，工場に「届く（実際に製造される）」ことのなかった設計がたくさん書かれている，という意味になる。reach「〜に達する，届く」。'
                 'never left the factory だと「工場から出なかった＝製造はされた」となり，失敗した設計という流れに合わない。'},
    ],
    'translation': [
        'ハルブルック市の静かな一角に，変わった収蔵品を持つ小さな博物館がある。そこには世界を変えた有名な発明品ではなく，失敗した製品が展示されている。音楽が鳴るけれど1週間で壊れた歯ブラシ，重すぎて持ち運べない折りたたみ自転車，誰も食べたがらなかった冷凍食品などである。'
        'この博物館を作ったのはセルウィン・オーム博士で，40年間家庭用品の設計をしてきた引退した技術者である。彼が最初にその考えを提案したとき，元同僚の多くは笑った。「まちがいを見るのに誰がお金を払うんだい？」とある同僚はたずねた。',
        'オーム博士の答えは単純だった。(b)彼の経験では，人はうまくいった製品よりもうまくいかなかった製品からはるかに多くのことを学ぶ。というのも，失敗は，成功なら無視させてくれるような問いを，人に考えさせずにはおかないからである。'
        '何かがよく売れたとき，会社がわざわざ立ち止まってその理由を考えることはめったにない。何かが失敗したとき，会社はその大失敗につながったあらゆる決定を詳しく調べるしかなくなる。',
        '博物館にある品物の多くは，作りが悪かったからではなく，設計者がそれを使う人々のことを誤解していたために失敗した。たとえば，音楽の鳴る歯ブラシはていねいに作られていて，音質もすばらしかった。'
        'しかし，作り手は，大人が歯をみがきながら音楽を聞きたいかどうかを一度もたずねなかった。ほとんどの大人は聞きたくなかったのだ。同じように，あの冷凍食品は健康によくて安かったが，灰色の箱に入っていたため，料理が実際よりおいしくなさそうに見えた。',
        '来館者は，いくつかの製品を手に取ったり，各展示の横に置かれたカードに自分の考えを書いたりするよう勧められる。(e)出口の近くの掲示板はそうしたカードでおおわれていて，オーム博士はその一枚一枚をすべて読んでいる。'
        '自転車の骨組みを軽くするといった小さな変更を提案するものもあれば，失敗した製品のまったく新しい使い道を提案するものもある。ある高校生のグループは，音楽の鳴る歯ブラシを使えば，その長さの歌がいつやめればよいかを教えてくれるので，小さな子どもが勧められている2分間歯をみがけるようになるかもしれないと提案した。オーム博士はその考えをとても気に入り，歯ブラシの製造会社に郵送したが，まだ返事は届いていない。',
        'この博物館には今では年に約9,000人が訪れ，その3分の1以上は学校の団体である。新入社員を研修の一環としてここに送る会社もいくつかある。'
        'ある管理職の女性は，失敗は新しいものを作るうえでふつうのことであり，恥ずかしく思う理由ではないということを，若い設計者たちにわかってほしかったのだと説明した。訪問を始めてから，彼女のチームは，うまくいかないかもしれないものも含めて，初期の考えをより進んで出し合うようになったという。また，訪問をきっかけに，身近な製品をどうすればもっとよく設計できるかを授業で話し合う教師もいる。',
        '誰もがオーム博士のやり方に賛成しているわけではない。失敗をたたえると，まちがいなど大したことではないかのように，人が不注意になるかもしれないと主張する批評家もいる。オーム博士はこの考えを否定する。'
        '(g)彼が言うには，自分がたたえたいのは失敗そのものではなく，結果がどうなるかわからないことに挑戦する勇気と，何がうまくいかなかったのかを認める正直さなのである。彼の考えでは，一度も失敗しない設計者は，おそらく何も新しいことに挑んでいないのだ。',
        '(h)この博物館には，生徒たちへの教えもある。多くの若者は授業でまちがった答えを言うのを恐れているので，おもしろい考えがあるときでさえ黙っている。オーム博士は，博物館を訪れることで，彼らがまちがいを違った目で見られるようになることを願っている。'
        '(i)結局のところ，今では人々が何も考えずに使っているどの製品も，かつては失敗していたかもしれない考えだったのであり，誰かが勇気を出してそれを確かめなければならなかったのだ。'
        '彼は入口のガラスケースにもう一つの品物を置いている。技術者として1年目のときのノートで，工場まで届くことのなかった設計でいっぱいである。',
    ],
}
