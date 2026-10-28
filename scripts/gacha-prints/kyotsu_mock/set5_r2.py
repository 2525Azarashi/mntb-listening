"""第5回 リーディング 第5〜8問"""

P5 = {
 'label': '第5問', 'title': 'コンテスト要項・応募用紙・メール（複数資料の照合）', 'pts': 16,
 'gist': ['イギリスの「若者向け環境アイデアコンテスト」の要項（部門・年齢・提出物・賞）、応募用紙、主催者からのメール。',
          '年齢による部門分け、チームの人数、締め切りの延長、最終審査の形式（オンライン可）を照合する。'],
 'vocab': ['category 部門', 'shortlist 最終候補', 'deadline 締め切り', 'prototype 試作品', 'mentor 助言者'],
 'sections': [{
  'instr': 'あなたは留学先の高校の友人と、次のコンテストに応募しようとしています。次の資料を読みなさい。',
  'blocks': [
   ('box', [
    ('title', 'Green Futures Challenge 2026'),
    ('p', 'Have an idea that could make your school or town greener? Every year, hundreds of young people across the country take part in our competition. Enter the Green Futures Challenge! Teams of **2 to 4 people** may enter. Each team must have a teacher or another adult who supports the project, but all the work must be done by the students themselves.'),
    ('table', [['Category', 'Age of all members', 'What to submit'],
               ['Junior', '11–14', 'A poster (A2 size) explaining your idea'],
               ['Senior', '15–18', 'A 3-minute video and a one-page written plan'],
               ['Open', 'Mixed ages (11–18)', 'A 3-minute video only']], [35, 50, 89]),
    ('pl', '**Deadline:** 31 March, 5 p.m.\n'
           '**Prizes (each category):** 1st — £500 for your school and a meeting with an environmental scientist; 2nd — £200; 3rd — £100.\n'
           'Five shortlisted teams in each category will present their ideas to the judges on 25 April. The results will be announced on our website on 2 May.'),
   ]),
   ('box', [
    ('h', 'Entry Form (summary)'),
    ('table', [['Team name', 'The Rain Savers', 'Members', 'Ruby (16), Ken (17), Amir (13)'],
               ['Idea', 'Collecting rainwater from the school roof to water the garden', 'Contact', 'Ruby Hart']], [28, 60, 28, 58]),
   ]),
   ('box', [
    ('small', '**From:** Green Futures Team\n**To:** Ruby Hart\n**Subject:** Your entry'),
    ('p', 'Dear Ruby,'),
    ('p', 'Thank you for registering "The Rain Savers." Your idea sounds very interesting, and we look forward to seeing your submission. Because of the ages of your members, your team has been entered in the category that matches your group. Please make sure your submission meets the requirements for that category. Submissions that do not follow the rules for their category cannot be judged.'),
    ('p', 'Good news: because of the school holidays, the deadline has been extended to **7 April**. Also, shortlisted teams can now choose to present on 25 April either in person in Birmingham or online. Teams who come to Birmingham will receive help with travel costs of up to £50 per person, and lunch will be provided. Online presentations will take place by video call, and each team will have ten minutes to present followed by five minutes of questions from the judges.'),
    ('p', 'Good luck!\nGreen Futures Team'),
   ]),
   ('box', [
    ('h', 'Judging criteria (all categories)'),
    ('pl', '• **Impact (40%)**: How much would your idea help the environment?\n'
           '• **Practicality (30%)**: Could your idea really be carried out at your school or in your town? Have you thought about the cost?\n'
           '• **Creativity (20%)**: Is your idea new, or does it use an existing idea in a new way?\n'
           '• **Communication (10%)**: Is your submission clear and easy to understand?'),
    ('p', 'Last year\'s Senior winners, from a school in Leeds, designed a system for collecting food waste from the school canteen and turning it into compost for local farms. Their school used the £500 prize to buy the first compost bins, and the system is still running today. '
          '**FAQ:** Can one student join more than one team? — No, each student may be a member of only one team. Can we change members after registering? — Yes, until the deadline, as long as the new members are within the age range of your category.'),
   ]),
  ],
  'qs': [
   {'no': 1, 'prompt': 'Which category has The Rain Savers been entered in?', 'pts': 3, 'ans': 3,
    'choices': ['Junior', 'Senior', 'Open', 'They cannot enter because of Amir\'s age.'],
    'ex': ['13歳・16歳・17歳の混合 → 全員が同じ年齢帯でないので **Open**（11〜18歳の混合）。']},
   {'no': 2, 'prompt': 'Complete the sentence.\nThe team must submit {1}, and if they win first prize, their school will receive {2}.', 'pts': 3, 'ans': [1, 6], 'score': 'all', 'no_balance': True,
    'choices': ['a 3-minute video only', 'a poster only', 'a video and a written plan', '£100', '£200', '£500'],
    'ans_text': '①・⑥（完答）',
    'ex': ['{1}：Open 部門は「3分の動画のみ」→ ①（③ は Senior 部門）。', '{2}：1位は学校に **£500** → ⑥。']},
   {'no': 3, 'prompt': 'By when must the team submit their entry?', 'pts': 3, 'ans': 4,
    'choices': ['31 March', '25 April', '5 April', '7 April'],
    'ex': ['メールで締め切りが **4月7日** に延長。① は要項の元の締め切り。']},
   {'no': 4, 'prompt': 'Which of the following statements are true? Choose the best combination.\nA. A team of five people could enter.\nB. The first prize includes money for the team\'s school.\nC. Shortlisted teams must travel to Birmingham.\nD. Each category has five shortlisted teams.', 'pts': 3, 'ans': 4,
    'choices': ['A and B', 'A and C', 'B and C', 'B and D'],
    'ex': ['B：1位は学校に £500 → 正。D：各部門5チームが最終候補 → 正。',
           'A：2〜4人 → 誤。C：オンラインも選べる → 誤。']},
   {'no': 5, 'prompt': 'Which **two** can be inferred from the materials? (The order does not matter.)', 'pts': 4, 'ans': [2, 4], 'any_order': True,
    'choices': ['Amir is too young to enter any category.', 'If the team wins first prize, they may meet a scientist.', 'The team must make a poster.',
                'The team has more time to prepare than originally planned.', 'All presentations must be given in person.'],
    'ans_text': '②・④（順不同）',
    'ex': ['② 1位には環境科学者との面会がある。④ 締め切りが1週間延びた。',
           '① Open 部門なら参加できる。③ ポスターは Junior 部門。⑤ オンラインも可。']},
  ]}]}

P6 = {
 'label': '第6問', 'title': '物語文＋発表メモ（時系列・人物の変化）', 'pts': 12,
 'gist': ['架空の女性「Mariko Sato」の物語。若いころ聴力を失った元ピアノ教師が、振動で音を感じる方法を研究し、耳の聞こえない子どものための音楽教室を開いた。',
          '最初は周囲に反対されたが、床に響く太鼓や手で触れるスピーカーを使い、子どもたちがリズムを体で感じられるようにした。',
          '※設問の題材としての架空の人物です。'],
 'vocab': ['vibration 振動', 'deaf 耳の聞こえない', 'rhythm リズム', 'skeptical 懐疑的な', 'sign language 手話'],
 'sections': [{
  'instr': 'あなたは英語の授業で、音楽と教育についての文章を読み、発表メモを作っています。',
  'blocks': [
   ('box', [
    ('title', 'Music You Can Feel'),
    ('p', 'Mariko Sato began playing the piano when she was four. By the age of twenty-five, she was teaching piano at a music school in Osaka. Then, after a serious illness, she lost most of her hearing within a single year. '
          'She stopped teaching and, for a long time, could not bring herself to open the piano at home. Friends tried to cheer her up by taking her to concerts, but she found them painful. She could see the musicians moving and the audience smiling, but the music itself had disappeared.'),
    ('p', 'During those years, Mariko worked in an office, entering data into a computer. She was good at the job, but she felt as if a part of her had been switched off. She avoided music shops and changed the subject whenever friends talked about concerts. Her sister later said that Mariko had lost not only her hearing but also her way of understanding the world.'),
    ('p', 'One evening, her young nephew was banging on a drum in the living room. Mariko, sitting on the wooden floor, suddenly realised she could feel each beat through her body. She took off her slippers and put her hands flat on the floor. '
          'Low notes made the floor tremble slowly; high notes felt like light tapping. "I could not hear the music," she later wrote, "but I could feel its shape." That night, for the first time in two years, she lifted the lid of her piano.'),
    ('p', 'Mariko began experimenting. She played the piano with her bare feet on its wooden pedals and her hand resting on its side. Over several years, she developed a method for teaching rhythm and melody through vibration, using drums placed on the floor, balloons that people hold against their chests — because the thin rubber passes on even small changes in sound — and speakers that can be touched. She also learned to read the movement of other musicians\' bodies, watching the rise and fall of their shoulders to follow the beat. Progress was slow, and there were weeks when she felt she was getting nowhere, but she kept a diary of every experiment, recording what worked and what did not.'),
    ('p', 'When she proposed opening a music class for deaf children, many people were skeptical. Some parents worried that their children would feel frustrated. A local official told her that music was "not a priority" for deaf students. '
          'Mariko did not argue. Instead, she invited the parents to a free trial lesson. She asked them to close their eyes, cover their ears and hold a balloon while she played a drum. Several of them were in tears by the end. One father said afterwards that it was the first time he had understood how his son might experience the world. The next week, nine families signed up.'),
    ('p', 'The class started with six children in a borrowed community hall, every Saturday morning. Mariko communicated with them in sign language, which she had learned after losing her hearing. The children took off their shoes at the door, sat in a circle on the wooden floor and began each lesson by "listening" to the floor with their hands. Within a year, the children were playing simple songs together on drums and xylophones, keeping perfect time by watching each other and feeling the floor. '
          'Ten years later, her school has trained more than eighty teachers, and similar classes have opened in four other countries.'),
    ('p', 'One of her first students, a girl named Yui, later became a percussion teacher herself. In a television interview, Yui explained that before joining the class, she had thought music was something that belonged only to hearing people. "Mariko-sensei showed me that music was mine too," she said. Today, Yui runs workshops in schools, where hearing and deaf children play drums together on the same wooden stage.'),
    ('p', 'Mariko still plays the piano every morning before work. When people call her story a miracle, she shakes her head. "Deaf children were always able to enjoy music," she says. "We simply had not found the right door."'),
   ]),
   ('box', [
    ('ja', '**発表メモ**'),
    ('pl', '**Mariko Sato: Music You Can Feel**'),
    ('pl', '・Events in order → 問1 (four boxes)'),
    ('pl', '・Her discovery → 問2'),
    ('pl', '・How she won support → 問3'),
    ('pl', '・What her story shows → 問4 (two answers)'),
   ]),
  ],
  'qs': [
   {'no': 1, 'prompt': 'Put the following events into the order in which they happened.\n{1} → {2} → {3} → {4}', 'pts': 3, 'ans': [4, 2, 1, 3], 'score': 'all',
    'choices': ['Mariko developed a method of teaching through vibration.', 'Mariko felt a drum through the floor.', 'Mariko\'s class began with six children.', 'Mariko lost most of her hearing.'],
    'ans_text': '④→②→①→③',
    'ex': ['聴力を失う（第1段落）→ 床で太鼓を感じる（第2段落）→ 振動で教える方法を開発（第3段落）→ 6人で教室開始（第5段落）。']},
   {'no': 2, 'prompt': 'What did Mariko discover on the evening with her nephew?', 'pts': 3, 'ans': 3,
    'choices': ['Her hearing had returned.', 'Her nephew wanted to learn the piano.', 'She could sense music through vibrations in her body.', 'Drums are louder than pianos.'],
    'ex': ['床を通して一拍ごとに体で感じられた → ③。']},
   {'no': 3, 'prompt': 'How did Mariko respond to people who doubted her idea?', 'pts': 3, 'ans': 1,
    'choices': ['She let parents experience music through vibration themselves.', 'She argued with the local official.', 'She gave up and returned to teaching piano.', 'She moved the class to another country.'],
    'ex': ['反論せず、保護者を無料体験に招き、目と耳をふさいで振動を体験させた → ①。']},
   {'no': 4, 'prompt': 'Choose **two** statements that the story supports. (The order does not matter.)', 'pts': 3, 'ans': [2, 5], 'any_order': True,
    'choices': ['Deaf children cannot keep time in music.', 'A personal difficulty can lead to a new way of helping others.', 'Music classes are a low priority for all schools.',
                'Mariko\'s method requires expensive equipment.', 'The right approach can open music to people who were thought unable to enjoy it.'],
    'ans_text': '②・⑤（順不同）',
    'ex': ['② 自身の聴力喪失から新しい教え方を生んだ。⑤ 最後の言葉「正しい扉が見つかっていなかっただけ」。',
           '① 子どもたちは完璧にリズムを合わせた。④ 風船・床の太鼓など身近な道具。']},
  ]}]}

P7 = {
 'label': '第7問', 'title': '論理的な文章＋スライド（要点・応用）', 'pts': 16,
 'gist': ['「習慣はどう作られるか」の説明文。きっかけ・行動・報酬のループ、新しい習慣が定着するまでの日数は人や行動によって大きく違う（平均約66日、18〜254日）。',
          '習慣を作るコツ：既存の習慣に結びつける、小さく始める、環境を変える。一日休んでも大きな影響はない。'],
 'vocab': ['cue きっかけ', 'routine 決まった行動', 'reward 報酬', 'automatic 自動的な', 'willpower 意志の力'],
 'sections': [{
  'instr': 'あなたは健康や生活習慣についての発表のために、次の記事を読んでスライドを作っています。',
  'blocks': [
   ('box', [
    ('title', 'How Habits Are Made'),
    ('p', 'Have you ever arrived at school and realised that you cannot remember the journey? About 40% of what we do each day is not the result of a conscious decision, but of habit. Brushing our teeth, checking our phones when we wake up, taking the same route to school — these actions happen almost automatically. Understanding how habits form can help us build good ones and break bad ones. Habits save the brain a great deal of effort: once an action becomes automatic, we can do it while thinking about something else entirely.'),
    ('p', 'Researchers often describe a habit as a loop with three parts. First comes a **cue**: something that triggers the behaviour, such as a time, a place or a feeling. Next is the **routine**, the behaviour itself. Finally, there is a **reward**, which makes the brain want to repeat the loop. '
          'For example, feeling bored (cue) leads us to check social media (routine), and seeing new messages (reward) makes us more likely to do it again next time we are bored. Over time, the brain begins to expect the reward as soon as it notices the cue, which is why habits can feel so hard to resist.'),
    ('p', 'A popular idea says that it takes 21 days to form a new habit. However, a well-known study at a university in London found that the average was about 66 days — and the range was enormous, from 18 to 254 days. Simple actions, like drinking a glass of water after breakfast, became automatic much faster than complex ones, like doing fifty sit-ups before dinner. Participants in the study chose their own new behaviour and reported each day how automatic it felt, so the results show how habits form in real life rather than in a laboratory.'),
    ('p', 'The same study found something encouraging: missing a day now and then did not seriously affect the process. What mattered was repeating the behaviour in a consistent situation. In other words, people who did their new habit at the same time and in the same place each day made faster progress than those who did it whenever they had a free moment. This is good news for anyone who has ever given up on a goal after one bad day.'),
    ('p', 'Experts suggest several strategies. One is "habit stacking": linking a new behaviour to an existing habit. For example, "After I brush my teeth at night, I will read one page of a book." Another is to start very small — two minutes of exercise rather than thirty — so that the behaviour feels easy. '
          'A third is to change your environment, so that the cue for a good habit is easy to see and the cue for a bad one is hidden. People who keep fruit on the kitchen table eat more fruit; people who leave their phones in another room sleep better. Rewards matter too: ticking a box on a calendar or telling a friend about your progress can give the brain a small sense of satisfaction that makes the habit more likely to stick.'),
    ('p', 'Breaking a bad habit works in a similar way, but in reverse. Because the cue and the reward are what keep the loop going, it is often more effective to change the routine than to try to stop it completely. A student who checks social media whenever she feels bored, for example, might keep the same cue (boredom) and the same kind of reward (a short break) but replace the routine with a five-minute walk or a glass of water. Making a bad habit harder to do — by logging out of apps or leaving snacks in a high cupboard — also helps.'),
    ('p', 'Relying on willpower alone rarely works for long. By designing the cues, routines and rewards in our lives, we can make good behaviour the easy choice. The aim is not to become a different person overnight, but to make small changes that, repeated over weeks and months, quietly add up.'),
   ]),
   ('slide', 'Building Better Habits', ['The habit loop: cue → routine → reward', 'Time to form a habit: average ( 問2 )',
                                        'Good news: ( 問3 )', 'Strategies: habit stacking / start small / change your environment']),
  ],
  'qs': [
   {'no': 1, 'prompt': 'In the example in the second paragraph, which is the "reward"?', 'pts': 3, 'ans': 4,
    'choices': ['Feeling bored', 'Checking social media', 'Waking up', 'Seeing new messages'],
    'ex': ['退屈（きっかけ）→ SNS を見る（行動）→ 新着メッセージを見る（報酬）→ ④。']},
   {'no': 2, 'prompt': 'Which best completes "Time to form a habit" on the slide?', 'pts': 3, 'ans': 2,
    'choices': ['exactly 21 days for everyone', 'about 66 days, but it varies widely', 'at least 254 days', 'less than 18 days'],
    'ex': ['平均約66日、18〜254日と幅が大きい → ②。① は俗説として否定されている。']},
   {'no': 3, 'prompt': 'Which best completes "Good news" on the slide?', 'pts': 3, 'ans': 1,
    'choices': ['Missing a day occasionally does not ruin progress.', 'Complex habits form faster than simple ones.', 'Willpower is enough to form any habit.', 'Habits can be formed in one week.'],
    'ex': ['第4段落：ときどき一日休んでも大きな影響はない → ①。② 逆。']},
   {'no': 4, 'prompt': 'Which **two** are examples of the strategies described in the article? (The order does not matter.)', 'pts': 4, 'ans': [3, 4], 'any_order': True,
    'choices': ['Promising yourself to exercise for two hours every day', 'Waiting until you feel motivated', 'Doing ten squats every time you finish brushing your teeth in the morning',
                'Putting your guitar on a stand in the living room instead of in its case', 'Changing the time of your new habit every day'],
    'ans_text': '③・④（順不同）',
    'ex': ['③ 既存の習慣（歯みがき）に結びつける＝habit stacking。④ 目につく所にギターを置く＝環境を変える。',
           '① 小さく始めるの逆。② 意志に頼る。⑤ 一定の状況でくり返すことが大切。']},
   {'no': 5, 'prompt': 'Your friend Nao wants to study English vocabulary every day but keeps forgetting. Based on the article, which plan is the best?', 'pts': 3, 'ans': 3,
    'choices': ['Study 200 words every Sunday for three hours.', 'Decide to study only when she feels like it.', 'Learn five words every day right after she eats breakfast, keeping her word book on the table.',
                'Study at a different time each day so it doesn\'t get boring.'],
    'ex': ['小さく始める（5語）＋朝食後という既存の習慣に結びつける＋机に単語帳を置く（環境）→ ③。']},
  ]}]}

P8 = {
 'label': '第8問', 'title': '複数の資料＋論説文の構成（統合・要約）', 'pts': 17,
 'gist': ['テーマ「高校で投資・お金の教育を必修にすべきか」。記事（お金の知識と若者の借金の関係）、調査グラフ（お金について学んだ場所）、生徒・保護者・教員・銀行員の意見。',
          'エッセイの構成メモを完成させる。'],
 'vocab': ['financial literacy 金融リテラシー', 'debt 借金', 'budget 予算を立てる', 'compound interest 複利', 'curriculum 教育課程'],
 'sections': [{
  'instr': 'あなたは「高校でお金の教育をもっと行うべきか」についてエッセイを書くために、次の資料を集めました。',
  'blocks': [
   ('box', [
    ('h', 'Source A — Article'),
    ('p', 'Should schools teach students how to manage money? A survey of 2,000 young adults aged 18 to 25 found that those who had taken a personal finance course at school were less likely to have credit card debt they could not repay. They were also more likely to have savings. '
          'However, the researchers point out that a single short course had little effect; the benefits were clearest among students who had studied the topic over several years and practised with realistic examples, such as planning a monthly budget. '
          'Young people today face financial choices earlier than their parents did. Many sign phone contracts, shop online with "buy now, pay later" services and are targeted by advertisements for investment apps while they are still at school. Experts warn that without basic knowledge, it is easy to make mistakes that take years to fix. '
          'In some countries, money education is already part of the national curriculum. In England, for example, it has been taught in secondary schools since 2014, although teachers say the amount of time given to it varies a great deal from school to school.'),
   ]),
   ('bar', {'title': 'Where did you mainly learn about money? (Students, n = 600)', 'cats': ['Family', 'School', 'Internet', 'Friends', 'Nowhere'],
            'series': [[38, 12, 29, 6, 15]], 'unit': '%', 'maxv': 50, 'step': 10}),
   ('box', [
    ('h', 'Source B — Opinions'),
    ('pl', '**Hana (student):** I learned about money mainly from videos online, but I\'m never sure which ones to trust. Some of them are clearly trying to sell something.'),
    ('pl', '**Mr. Evans (parent):** Talking about money is the family\'s job. Schools already have too many subjects. I would rather teachers spent more time on maths and reading, which are the basis for everything else. At home, we give our children pocket money and let them make their own mistakes.'),
    ('pl', '**Ms. Mori (teacher):** Not every family can teach this. If schools don\'t, the gap between students will grow. Some of my students have parents who have never had a bank account themselves.'),
    ('pl', '**Kenta (university student):** When I moved out and started living alone, I had no idea how much to spend on food or electricity. By the end of my first month, I had almost no money left. I wish someone had taught me how to make a budget in high school.'),
    ('pl', '**Mr. Silva (bank employee):** I often meet young customers who don\'t understand interest. Practical lessons — budgeting, comparing loans — are what they need, not just theory. Many of them are surprised to learn how much a small loan can grow if they only pay the minimum each month.'),
   ]),
   ('box', [
    ('h', 'Source C — Example: A school programme'),
    ('p', 'At Riverside High School, money lessons are spread across three years. In the first year, students learn to keep a simple record of what they spend. Students say the lessons feel useful because the examples come from their own lives. In the second year, they plan a monthly budget for an imaginary young adult with a part-time job, including rent, food and transport. '
          'In the third year, they compare real phone contracts and loans and calculate how much interest they would pay.'),
    ('p', 'Teachers say the most popular activity is a role-play in which students must decide how to spend a fixed amount of money after an unexpected bill arrives. "It\'s the first time I\'ve realised how quickly money disappears," one student said. '
          'The school invites local bank staff to answer questions once a term, but they are not allowed to advertise their own products.'),
   ]),
   ('box', [
    ('ja', '**エッセイの構成メモ**'),
    ('pl', '**Title:** Money Lessons for Everyone'),
    ('pl', '**Step 1:** Position → {問1}'),
    ('pl', '**Step 2:** Reasons → {問2 (two answers)}　Data → {問3}　Opposing view and response → {問4}'),
    ('pl', '**Step 3:** Conclusion → {問5}'),
   ]),
  ],
  'qs': [
   {'no': 1, 'prompt': 'Which position best matches the title?', 'pts': 3, 'ans': 2,
    'choices': ['Money education should be left to families.', 'All students should receive practical money education at school.', 'Only students who want to work in banks should learn about money.', 'Money should not be discussed with teenagers.'],
    'ex': ['題名 "Money Lessons for Everyone" → ②。']},
   {'no': 2, 'prompt': 'Choose **two** reasons supported by the sources. (The order does not matter.)', 'pts': 4, 'ans': [1, 4], 'any_order': True,
    'choices': ['Not all families are able to teach about money.', 'Online videos are always reliable.', 'One short lesson is enough to change behaviour.',
                'Students who studied finance at school were less likely to have unpayable debt.', 'Students learn most about money from school now.'],
    'ans_text': '①・④（順不同）',
    'ex': ['① Ms. Mori。④ Source A の調査結果。② Hana は信頼できるか不安。③ 短い講座だけでは効果が小さい。⑤ グラフで学校は12％と少ない。']},
   {'no': 3, 'prompt': 'Which statement is supported by the graph?', 'pts': 3, 'ans': 3,
    'choices': ['Most students learned about money at school.', 'Friends were the most common source.', 'More students learned from the internet than from school.', 'Nobody said they had learned nowhere.'],
    'ex': ['インターネット 29％ ＞ 学校 12％ → ③。最多は家族38％。何も学んでいない人も15％。']},
   {'no': 4, 'prompt': 'Which pair best shows an opposing view and a response to it?', 'pts': 3, 'ans': 4,
    'choices': ['Banks need more customers. / So schools should advertise banks.', 'Videos are fun. / So students should watch more videos.',
                'Theory is important. / So lessons should avoid examples.', 'Money is the family\'s job. / But not every family can teach it, so the gap may grow.'],
    'ex': ['Mr. Evans の反対意見（家庭の役割）に Ms. Mori の論点で応答 → ④。']},
   {'no': 5, 'prompt': 'Which is the most suitable conclusion?', 'pts': 4, 'ans': 1,
    'choices': ['Schools should teach money skills over several years using practical tasks such as budgeting, while working with families.',
                'Schools should hold one lecture on money in the final year.', 'Students should learn about money only from the internet.', 'Families should stop talking about money at home.'],
    'ex': ['数年にわたる学習・実践的な例（Source A・Mr. Silva）、家庭との協力（Mr. Evans への配慮）→ ①。② 短い講座は効果が小さい。']},
  ]}]}

PARTS_B = [P5, P6, P7, P8]
