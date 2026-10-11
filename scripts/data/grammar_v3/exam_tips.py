"""【入試ではここ】のひと言（2026-10-11 大改訂③）。
入試で点を取るための「よく出る形・ひっかけ・言いかえ」を、文法事項ごとに手で書いた。
上から順に見て、最初に当てはまった1つを使う（キーは「文法事項名＋ポイント」に対する正規表現）。
元データに【プラス】がある問はそちらを優先する（ここは使わない）。"""
import re
RULES = [
 # 時制
 ((1), r'名詞節は will', '時・条件の副詞節は現在形でも、名詞節（「〜かどうか」「いつ〜か」）は未来なら will。if／when の働きで決める。'),
 ((1), r'時の副詞節|条件の副詞節|if 節（副詞節）|when 節（副詞節）|by the time|as soon as', '時・条件を表す副詞節の中は、未来のことでも現在形（完了なら現在完了）。will を選ぶひっかけが定番。'),
 ((1), r'ago|just now|when の疑問文', 'ago／just now／yesterday／When …? は「過去の一点」なので現在完了と一緒に使えない。過去形を選ぶ。'),
 ((1), r'have been to|have gone to', 'have been to「行ったことがある・行ってきた」／have gone to「行ってしまった（今いない）」。主語が I・you なら gone は不可。'),
 ((1), r'進行形にしない', '状態動詞（know／like／resemble／belong／see など）は進行形にしない。継続は現在完了で表す。'),
 ((1), r'since|It is 時間|It has been', '「〜して…になる」は It has been［It is］期間 since S 過去形＝ S have done … for 期間。3つの書きかえが頻出。'),
 ((1), r'完了', '完了形は「基準の時点まで」。基準が今→現在完了、過去→過去完了、未来→未来完了。by／before／until の語で基準を探す。'),
 ((1), r'進行形', '進行形は「その時点で途中」。at that time／when S did などで過去進行、this time tomorrow で未来進行。'),
 ((1), r'going to|be about to', 'be going to do は「すでに決めた予定・兆しのある予測」、be about to do は「まさに〜するところ」（時の副詞と一緒に使わない）。'),
 ((1), r'現在形|過去形', '習慣・真理は現在形、過去の一点は過去形。時を表す語（every day／yesterday／last 〜）が決め手。'),
 # 態
 ((2), r'群動詞の受動態', '群動詞の受け身は前置詞まで残す（be laughed at by／be taken care of by）。by の重なりに注意。'),
 ((2), r'by 以外|interested|caught|surprised|known|made from|made of|covered', 'be known to／for／as、be made of（材料が見える）／from（原料が変わる）など、by 以外の前置詞の区別が頻出。'),
 ((2), r'受動態|受け身', '主語が「される」側なら be＋過去分詞。完了形 have been done・進行形 be being done・助動詞 can be done の形を確認。'),
 # 助動詞
 ((3), r'have done|have been', '助動詞＋have done は過去への推量・後悔。must（違いない）／can\'t（はずがない）／may（かもしれない）／should（すべきだったのに）。'),
 ((3), r'had better', 'had better do「〜したほうがよい」は強い言い方。否定は had better not do（not の位置）。目上には使わない。'),
 ((3), r'would rather', 'would rather A than B「BよりむしろA」。A・B とも原形。would rather＋S 過去形 は仮定法になる。'),
 ((3), r'used to|would \(often\)', 'used to do「以前は〜だった（今は違う）」は状態にも使える。would (often) は動作だけ。be used to doing「慣れている」と区別。'),
 ((3), r'need|dare', 'need・dare は助動詞（need not do）と一般動詞（need to do）の両方がある。疑問・否定の形で見分ける。'),
 ((3), r'can\'t help|cannot but|cannot … too|may well|might as well', 'cannot help doing＝cannot but do／cannot … too〜／may well／might as well は熟語として丸ごと覚える。'),
 ((3), r'助動詞|must|may|should|can|will|Shall|ought', '助動詞の後ろは必ず原形。否定・過去の形（must→had to、can→could／was able to）を確認する。'),
 # 仮定法
 ((4), r'if の省略|Had S|Were S|Should S|Had it|Were I', 'if を省くと倒置（Had S done／Were S／Should S do）。文頭の Had・Were・Should が if の合図。'),
 ((4), r'wish|If only|as if|as though|would rather＋仮定法|It is time|high time', 'wish／as if／If only／It is time の後ろは仮定法。今のことなら過去形、過去のことなら過去完了。'),
 ((4), r'Without|But for|were not for|had not been for|otherwise', 'Without A／But for A は if 節の代わり。主節が would do なら現在、would have done なら過去の仮定。'),
 ((4), r'仮定法過去と過去完了の併用', 'if 節は過去（had done）、主節は今（would do）という「時のずれ」の形。now／today が主節にある。'),
 ((4), r'仮定法', '仮定法は「時を1つ過去へずらす」。今の反対→過去形、過去の反対→過去完了。主節の would／could と組で選ぶ。'),
 # 不定詞
 ((5), r'too … to|enough', 'too … to do＝so … that S can\'t do、… enough to do＝so … that S can do。enough は形容詞の後ろに置く。'),
 ((5), r'in order to|so as to|so as not|in order not', '「〜しないように」は so as not to do／in order not to do。not は to の直前。'),
 ((5), r'形式主語|形式目的語|It is＋|S V it C', 'It is ＋形容詞＋for A to do。人の性質（kind／careless）なら of A。形式目的語は think［find］it C to do。'),
 ((5), r'原形不定詞|使役|知覚|let|make|have O do|help O|get O to', 'make／let／have＋O＋原形、get＋O＋to do。受け身にすると to が復活（be made to do）。'),
 ((5), r'疑問詞＋to', '疑問詞＋to do「何を〜すべきか」。what／how／where／when／which＋to do が名詞のかたまりになる。why to do はない。'),
 ((5), r'独立不定詞|needless to say|to say the least|not to mention|to be frank', 'to tell the truth／needless to say／so to speak などの独立不定詞は意味ごと暗記。整序で頻出。'),
 ((5), r'be＋to|seem to|完了不定詞|代不定詞', 'seem to have done は「（以前に）〜したようだ」。be to do は予定・義務・可能・意図・運命を文脈で読む。'),
 ((5), r'不定詞', '不定詞は名詞（〜すること）・形容詞（〜するための）・副詞（〜するために）の働き。空所の前の語が何かで用法を決める。'),
 # 動名詞
 ((6,17), r'stop|remember|forget|regret|try|need doing|want doing|go on', 'remember／forget／regret＋doing は「（過去に）〜したこと」、＋to do は「（これから）〜すること」。意味の違いが頻出。'),
 ((6,17), r'look forward to|be used to|accustomed|object to|when it comes to|What do you say to|with a view to|devoted to', 'この to は前置詞なので後ろは動名詞。look forward to／be used to／object to／when it comes to が定番のひっかけ。'),
 ((6,17), r'no use|no point|no sense|worth|There is no doing|goes without|feel like|cannot help|on doing|in doing|busy|difficulty|trouble|spend', '動名詞の慣用表現（It is no use doing／be worth doing／feel like doing／have difficulty doing）は形ごと覚える。'),
 ((6,17), r'意味上の主語|完了動名詞|否定', '動名詞の意味上の主語は所有格・目的格を前に置く。否定は not doing、前のことは having done。'),
 ((6,17), r'動名詞|enjoy|mind|avoid|finish|give up|put off|consider|deny|practice|miss', 'mind／enjoy／give up／avoid／finish／escape／put off／stop（MEGAFEPS）は動名詞だけを目的語にとる。to do を選ばない。'),
 ((6,17), r'agree to|decide|expect|manage|refuse|hope|offer|pretend|promise|afford|plan|want', 'want／hope／decide／expect／manage／refuse／promise／pretend などは to do だけ。「これからのこと」を表す動詞が多い。'),
 # 分詞
 ((7), r'感情|exciting|boring|surprising|disappointed|pleased|confused|excited', '感情の分詞は、人が「させられる」なら -ed（excited）、物が「させる」なら -ing（exciting）。主語で決める。'),
 ((7), r'have O done|get O done|keep O|知覚動詞＋O|make oneself', 'O と分詞の関係が「する」なら -ing、「される」なら -ed。have my hair cut／make oneself understood が定番。'),
 ((7), r'分詞構文|独立分詞|judging|weather permitting|considering|generally speaking', '分詞構文は主語が同じなら省略、違えば残す（独立分詞構文）。受け身・完了は Having been done → (Being) done。'),
 ((7), r'with＋名詞', 'with＋名詞＋分詞「〜を…したままで」。名詞と分詞の関係（する／される）で -ing と -ed を選ぶ。with one\'s eyes closed が頻出。'),
 ((7), r'分詞|There be', '名詞を修飾する分詞は、名詞が「する」側なら -ing、「される」側なら -ed。1語なら名詞の前、2語以上なら後ろ。'),
 # 比較
 ((8), r'no more than|not more than|no less than|not less than|at most|at least', 'no more than＝only（たった）、not more than＝at most（せいぜい）、no less than＝as many［much］as（も）、not less than＝at least（少なくとも）。'),
 ((8), r'no more|no less|any more than', 'A is no more B than C「Cと同様AもBでない」（クジラの構文）。no less なら「同様にBだ」。意味が逆になる点に注意。'),
 ((8), r'倍|half|times|twice', '倍数表現は X times as … as A。2倍は twice、半分は half。twice the size of A の形も頻出。'),
 ((8), r'最上級|No other|one of the|by far|序数', '最上級の書きかえ：No other 単数名詞 … 比較級 than A／比較級 than any other 単数名詞。one of the 最上級＋複数名詞。'),
 ((8), r'比較級の強調|much|even|still|far', '比較級を強めるのは much／far／even／still／a lot。very は使えない（very は原級を強める）。'),
 ((8), r'the＋比較級|ますます', 'The＋比較級 S V, the＋比較級 S V「〜すればするほど…」。比較級 and 比較級「ますます」。the を落とすひっかけ。'),
 ((8), r'senior|junior|superior|inferior|prefer|ラテン', 'senior／junior／superior／inferior／prefer は than ではなく to をとる。prefer A to B。'),
 ((8), r'rather than|not so much|know better', 'not so much A as B「AというよりむしろB」＝ B rather than A。know better than to do「〜するほど愚かではない」。'),
 ((8), r'比較|原級|as＋', 'as … as の間は原級、than の前は比較級。前に much・many・little など量の語があるかで形を決める。'),
 # 代名詞
 ((9), r'one|ones|it ＝|that of|those', 'it は「前に出たその物」、one は「同じ種類の別の1つ」。the＋名詞のくり返しは that（単数）／those（複数）。'),
 ((9), r'other|another|the others|some … others', 'another は「もう1つ（不特定）」、the other は「残りの1つ」、others は「ほかの人々」、the others は「残り全部」。'),
 ((9), r'either|neither|both|none|each|every|all', 'both／either／neither は2者、all／any／none は3者以上。each・every は単数扱い。every は代名詞として単独で使えない。'),
 ((9), r'代名詞|mine|oneself|it', '所有代名詞（mine）・再帰代名詞（myself）・it の働きを確認。a friend of mine の形（a my friend は不可）。'),
 # 関係詞
 ((10), r'what', 'what は先行詞を含む（＝the thing which）。前に名詞があれば what は使えない。what little／what is more などの慣用も頻出。'),
 ((10), r'whoever|whatever|whichever|wherever|whenever|however|no matter', '-ever は「〜する人［物・所］なら何でも」と「たとえ〜しても（譲歩）」の2つ。no matter＋疑問詞で言いかえられるのは譲歩だけ。'),
 ((10), r'関係副詞|where|when|why|how', '後ろが完全な文なら関係副詞（where／when／why）、名詞が1つ欠けていれば関係代名詞（which）。先行詞だけで決めない。'),
 ((10), r'非制限|コンマ|all of whom|some of which|neither of which', 'コンマの後ろに that は使えない。前置詞の後ろも that 不可。all of whom／some of which の形。'),
 ((10), r'前置詞＋|前置詞を節', '前置詞＋関係代名詞（in which／with whom）。前置詞の直後に that・who は置けない。'),
 ((10), r'whose', 'whose＋名詞「その〜が」。先行詞が人でも物でも使える。後ろに名詞が来たら whose を疑う。'),
 ((10), r'関係|who|whom|which|that', '関係代名詞は、後ろの文で欠けている要素（主語→主格／目的語→目的格）と先行詞（人／物）の2点で選ぶ。'),
 # 接続詞
 ((11), r'no sooner|hardly|scarcely|the moment|the instant|directly|as soon as', '「〜するとすぐに」は as soon as＝the moment＝No sooner had S done … than ～＝Hardly had S done … when ～。倒置の形が頻出。'),
 ((11), r'not until|until|by the time|till|before', 'until は「〜までずっと（継続）」、by は「〜までに（期限）」。It was not until … that ～「…して初めて～」。'),
 ((11), r'unless|in case|provided|providing|supposing|on condition|as long as|as far as', 'unless「〜しない限り」（＝if … not）。as long as は条件「〜する限り」、as far as は範囲「〜する限りでは」。'),
 ((11), r'though|although|even if|even though|as he was|while|whereas', '譲歩の though／although は but と一緒に使わない。形容詞＋as S V「〜だけれども」は倒置の形。'),
 ((11), r'so that|in order that|so … that|such … that|Such is', 'so＋形容詞＋that、such＋(a)＋形容詞＋名詞＋that。so that S can「〜できるように」は目的。'),
 ((11), r'whether|if「', '「〜かどうか」の if は動詞の目的語だけ。主語・前置詞の後ろ・or not の直前は whether。'),
 ((11), r'not only|as well as|both|either|neither|not A but B', '相関接続詞：not only A but also B／both A and B／either A or B／neither A nor B。主語なら動詞は B（both は複数）。'),
 ((11), r'同格|that', '名詞＋that S V（同格）「〜という名詞」。fact／news／idea／belief などが前に来る。関係代名詞の that と区別。'),
 ((11), r'接続詞|and|but|or|so|for|yet|nor', '命令文, and「そうすれば」／命令文, or「さもないと」。nor の後ろは倒置（nor do I）。'),
 # 前置詞
 ((12), r'時を表す|時刻|朝|夕|曜|日付|季節|期間|期限|継続', 'at は時刻・一点、on は日・曜日・特定の日の朝、in は月・年・季節。特定の日の朝夕は on。by（期限）／until（継続）も頻出。'),
 ((12), r'前置詞', '前置詞は「後ろの名詞との関係」で選ぶ。for（期間）／during（特定の期間）／by（手段・差・期限）の区別が頻出。'),
 # 一致
 ((13), r'一致|number|There|most of|主語', '主語の中心語で単数・複数を決める。the number of＋複数名詞は単数扱い、a number of＋複数名詞は複数扱い。'),
 # 疑問文・語順
 ((14), r'付加疑問', '付加疑問は「肯定文→否定の疑問」。Let\'s …, shall we?／命令文, will you?／I am …, aren\'t I? が定番。'),
 ((14), r'Why don\'t|Why not', 'Why don\'t you do?「〜したらどう？」（提案）＝ Why not do?。Why don\'t we do? は「〜しましょう」＝ Let\'s do。'),
 ((14), r'間接疑問|if＋S|whether|疑問詞＋S', '間接疑問は「疑問詞＋S＋V」の平叙文の語順。Do you know＋疑問詞…／疑問詞＋do you think＋S V の形。'),
 ((14), r'倒置|Little|Never|Neither|So＋|So |Nor|So was|So do', '否定の語（Never／Little／Hardly／Only＋副詞）が文頭に出ると疑問文の語順に倒置。So do I／Neither do I も頻出。'),
 ((14), r'疑問|What|How|Why|Who', 'What is S like?「Sはどんな様子か」、How come S V?（語順は平叙文）、What do you think of A?（How は不可）。'),
 # 否定・省略・強調
 ((15), r'強調構文|It is … that|It is I', 'It is … that ～ の強調構文は、It is と that を消して文が成り立つかで見分ける。It is not until … that も頻出。'),
 ((15), r'部分否定|not … all|not always|not every|not necessarily', 'not＋all／always／every／necessarily は部分否定「すべてが〜というわけではない」。全体否定は no／none／never。'),
 ((15), r'anything but|nothing but|far from|the last|free from|yet to|remain to', 'anything but「決して〜ではない」、nothing but「〜だけ」、the last A to do「最も〜しそうにない」。否定語なしの否定表現。'),
 ((15), r'省略|if any|if ever|if not|When|While', '時・譲歩の副詞節では「S＋be」が省略できる（When young, …）。if any／if ever「たとえあるとしても」。'),
 ((15), r'否定|never|without|no A without B', 'never … without doing「〜すれば必ず…する」（二重否定）。not … in the least／not … at all「少しも〜ない」。'),
 # 話法
 ((16), r'話法|suggest|tell A|ask A|said', '話法の書きかえは、時制を1つ過去へ（時制の一致）＋代名詞・時の語（yesterday→the day before）の言いかえ。命令文は tell A to do。'),
 # 語法（動詞）
 ((17), r'remind|inform|deprive|rob|cure|warn|convince|suspect|accuse', 'remind／inform／convince／warn A of B（伝達）、rob／deprive／cure A of B（分離）。rob 人 of 物（steal 物 from 人）。'),
 ((17), r'prevent|keep A from|prohibit|stop A from|discourage', 'prevent／keep／stop／prohibit／discourage A from doing「Aが〜するのを妨げる」。from の後ろは動名詞。'),
 ((17), r'supply|provide|share|fill|present', 'provide［supply］A with B＝provide B for［to］A。前置詞の組み合わせで正解が決まる。'),
 ((17), r'blame|punish|thank|praise|criticize|excuse|apologize', 'blame／thank／praise／punish／excuse A for B「BのことでAを〜」。apologize to A for B（apologize A は不可）。'),
 ((17), r'raise|rise|lie|lay|seat|sit|find|found', 'rise（自）／raise（他）、lie（自・lay・lain）／lay（他・laid・laid）。目的語の有無と活用が頻出。'),
 ((17), r'自動詞|他動詞|marry|reach|discuss|enter|attend|approach|resemble|mention|graduate|argue', 'discuss／marry／reach／enter／approach／resemble／mention は他動詞なので前置詞を付けない（discuss about は×）。逆に graduate from／apologize to は前置詞が必要。'),
 ((17), r'tell|say|talk|speak|explain', 'tell は「人＋話の内容」、say は「話の内容（to 人）」、talk・speak は「話す行為（to／with 人、about 内容）」。explain to 人 that（explain 人 は×）。'),
 ((17), r'cost|take|charge|save|spare|owe|allow|cause|do A good|do harm|do A a favor|give A B|二重目的語', 'It costs［takes］A B to do「AがBかかる」、save A B「AのBを省く」、do A good／harm。二重目的語の型を丸ごと。'),
 ((17), r'suit|fit|match|go with|become|似合う|合う', 'suit（服・色が人に似合う）／fit（サイズが合う）／match・go with（物と物が合う）。'),
 ((17), r'lend|borrow|rent|use|貸す|借り', 'lend「貸す」／borrow「借りる（移動できる物を無料で）」／use「（その場で）借りて使う」／rent「お金を払って借りる・貸す」。'),
 ((17), r'S\+V\+O\+to do|to do\] の形|ask A to|persuade|encourage|allow A to|enable|force|compel|cause A to|want A to|would like A to|expect A to|advise|tell A to', 'want／ask／tell／allow／enable／force／persuade／encourage＋A＋to do。make／let／have は to なしの原形。'),
 ((17), r'help', 'help A (to) do／help A with B／cannot help doing（〜せずにいられない）。help A to do の to は省略可。'),
 ((17), r'suggest|demand|insist|propose|recommend|require|that S \(should\)', 'suggest／demand／insist／propose／recommend that S (should) 原形。主語が三人称でも原形のまま（仮定法現在）。'),
 ((17), r'動詞の語法|動詞', '動詞の語法は「後ろに何を置けるか（to do／doing／that節／前置詞）」で決まる。型ごとに覚える。'),
 # 形容詞・副詞
 ((18), r'few|little|a few|a little|quite a few|not a few|much|many', 'few・a few は数えられる名詞、little・a little は数えられない名詞。a が付くと「少しはある」、付かないと「ほとんどない」。'),
 ((18), r'alike|alive|asleep|afraid|aware|補語', 'alike／alive／asleep／afraid／aware は名詞の前に置けない（補語だけ）。名詞の前なら living／sleeping を使う。'),
 ((18), r'convenient|possible|impossible|necessary|likely|人を主語', 'convenient／possible／necessary は人を主語にしない（It is … for A to do）。likely は人を主語にできる（S is likely to do）。'),
 ((18), r'respectful|respectable|considerate|considerable|industrial|industrious|literary|literate|sensitive|sensible|imaginative|imaginary|economic|economical|priceless|invaluable', '形のよく似た形容詞（considerable／considerate、sensible／sensitive、respectable／respectful）は意味の取り違えが定番。'),
 ((18), r'price|salary|income|cost|fee|audience|population|traffic|large|small|high|low', 'price／salary／income は high・low、audience／population は large・small、traffic は heavy・light。expensive・cheap を使わない。'),
 ((18), r'形容詞|副詞|hard|hardly|late|lately|near|nearly|most|almost', 'hard（熱心に）／hardly（ほとんど〜ない）、late（遅く）／lately（最近）、near（近く）／nearly（ほとんど）。-ly で意味が変わる語に注意。'),
 # 名詞
 ((19), r'不可算|advice|furniture|information|news|homework|luggage|baggage|weather|equipment|money', 'advice／information／furniture／news／homework／baggage は数えられない。a や -s を付けず、a piece of で数える。'),
 ((19), r'friends|trains|turns|terms|hands|seats|複数形', 'make friends with／change trains／take turns／shake hands／be on good terms with は必ず複数形。'),
 ((19), r'fare|fee|toll|charge|cost|price|client|customer|guest|passenger|audience|spectator|habit|custom|shade|shadow|appointment|reservation', 'fare（運賃）・fee（料金・謝礼）・toll（通行料）、customer（店の客）・client（依頼人）・guest（招待客）など、意味の近い名詞の使い分けが頻出。'),
 ((19), r'名詞', '名詞は「数えられるか」と「決まった言い回し（make room for など）」が問われる。熟語の中の名詞の単複・冠詞にも注意。'),
 # 会話
 ((20), r'電話', '電話表現：This is A speaking.（こちらはAです）／Hold on.（切らずに待って）／You have the wrong number.（番号違い）。'),
 ((20), r'あいさつ', '初対面 How do you do?／Nice to meet you.、久しぶり How have you been?／It\'s been a long time.。答え方とセットで覚える。'),
 ((20), r'買い物|店|price|How much|waited on', '店の表現：May I help you?／I\'m just looking.／Have you been waited on?。値段は How much is A?／What\'s the price of A?。'),
 ((20), r'依頼|favor|kind enough|Would you mind|Could you|Can you', '依頼への答え方：Would you mind doing? には No, not at all.（いいですよ）／Sure. と答える。Yes は「嫌です」になる。'),
 ((), r'.', '空所の前後の語と、文全体の意味（和訳）の両方から決める。正解の形をそのまま声に出して覚えると、入試の4択で迷わない。'),
]
def _wb(p: str) -> str:
    """英語の語には語の境目を付ける（remind が mind に当たらないように）"""
    return '|'.join(f'(?<![A-Za-z]){a}(?![A-Za-z])' if re.match(r'[A-Za-z]', a) else a for a in p.split('|'))
_C = [((c if isinstance(c, tuple) else (c,)) if c != () else (), re.compile(_wb(p)), t) for c, p, t in RULES]
# どのルールにも当たらないときの、章の基本のひと言
CHAPTER_BASE = {
 1: '時制は「時を表す語（every day／yesterday／since／by the time）」で決まる。まず文中の時の語に印をつける。',
 2: '主語が「する」側か「される」側かを先に決める。される側なら be＋過去分詞、時制は be の形で表す。',
 3: '助動詞の後ろは原形。過去のことへの推量・後悔は 助動詞＋have done。意味（推量か義務か）を和訳で確かめる。',
 4: '仮定法は「時を1つ過去へずらす」。今の反対→過去形、過去の反対→過去完了。主節の would／could と組で選ぶ。',
 5: '不定詞は名詞・形容詞・副詞の3用法。空所の前の語（動詞・名詞・形容詞）で、どの用法かを決める。',
 6: '前置詞の後ろ・動名詞だけをとる動詞の後ろは doing。to が前置詞かどうかを見抜くのが得点のカギ。',
 7: '分詞は「名詞が する→-ing／される→-ed」。分詞構文は主語が同じなら省略、違えば残す。',
 8: 'as … as は原級、than は比較級、the＋最上級は of／in で範囲。比較の書きかえ（最上級⇔比較級）は必ず出る。',
 9: 'it（その物）／one（同じ種類の1つ）／that・those（the＋名詞のくり返し）の区別が頻出。',
 10: '関係詞は「先行詞（人・物・場所）」と「後ろで欠けている要素（主語・目的語・なし）」の2点で選ぶ。',
 11: '接続詞の後ろは S V、前置詞の後ろは名詞。during と while、because と because of の区別が定番。',
 12: '前置詞は後ろの名詞との関係で選ぶ。時（at／on／in）、期間（for／during）、期限（by）と継続（until）が頻出。',
 13: '主語の中心の名詞で単数・複数を決める。修飾語（of ～／関係詞節）に惑わされない。',
 14: '疑問文の語順と、否定語が文頭に来たときの倒置が頻出。間接疑問は平叙文の語順に戻す。',
 15: 'not＋all／always は部分否定、no／never は全体否定。強調構文は It is と that を消して確かめる。',
 16: '話法の書きかえは、時制の一致・代名詞・時の語（now→then、yesterday→the day before）の3点を変える。',
 17: '動詞の語法は「後ろに何を置けるか（to do／doing／that節／前置詞）」で決まる。型ごとに覚える。',
 18: '形容詞・副詞は「数えられる名詞か」「補語だけの形容詞か」「-ly で意味が変わるか」が問われる。',
 19: '名詞は「数えられるか」と「決まった言い回しの単複・冠詞」が問われる。',
 20: '会話表現は場面（あいさつ・電話・買い物・依頼）ごとに、答え方とセットで覚える。',
}
def tip_for(chapter: int, key: str):
    """その章のルールだけを上から見る。(ひと言, その問に合ったルールか)。当たらなければ章の基本のひと言"""
    rules = [(rx, t) for cs, rx, t in _C if chapter in cs]
    for rx, t in rules:
        if rx.search(key): return t, True
    return CHAPTER_BASE.get(chapter, ''), False
