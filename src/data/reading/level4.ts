/** レベル4：難関（早慶・旧帝・難関国立）。180〜230語・設問3問（問いと選択肢は英語） */
import { p, q } from './types';

export const LEVEL4 = [
  p('r4-01', 4, 'The Myth of the Multitasker', 'マルチタスクの思い込み', `
Many people take pride in their ability to do several things at once: answering messages during a meeting, listening to a lecture while checking social media, or studying with the television on. They believe that multitasking makes them more productive. A growing body of research suggests otherwise.

What we call multitasking is, in most cases, rapid switching between tasks. Each time the brain shifts its attention, it needs a moment to reorient itself, and these small delays add up. In laboratory studies, participants who switched frequently between two tasks took considerably longer to complete them, and made more errors, than those who finished one task before starting the other.

More surprisingly, people who multitask heavily in daily life appear to be worse at ignoring irrelevant information, not better. One explanation is that habitual multitaskers have trained themselves to respond to every new stimulus, so they find it harder to filter out distractions when focus is required.

None of this means that we can never do two things at once. Walking while talking is easy, because one of the activities has become almost automatic. The problem arises when both tasks demand conscious thought.`, [
    q('r4-01-1', 'According to the passage, what is "multitasking" in most cases?', [
      'Moving quickly back and forth between tasks', 'Performing two demanding tasks at exactly the same moment', 'Doing tasks in a carefully planned order', 'Using technology to finish work automatically'],
      '「私たちが multitasking と呼ぶものは、たいていの場合、作業間のすばやい切り替えである」。',
      'What we call multitasking is, in most cases, rapid switching between tasks.'),
    q('r4-01-2', 'What did research find about people who multitask heavily in daily life?', [
      'They are less able to ignore information that is not relevant', 'They are better at filtering out distractions', 'They finish tasks faster than other people', 'They rarely respond to new stimuli'],
      '「日常的によくマルチタスクをする人は、無関係な情報を無視するのがむしろ下手である」。better ではなく worse。',
      'people who multitask heavily in daily life appear to be worse at ignoring irrelevant information, not better.'),
    q('r4-01-3', 'Why is walking while talking described as easy?', [
      'Because one of the activities requires little conscious thought', 'Because both activities use the same part of the body', 'Because people practice it in laboratory studies', 'Because talking is less important than walking'],
      '「片方の活動がほとんど自動的になっているから」。問題は両方が意識的な思考を必要とするときに起こる。',
      'because one of the activities has become almost automatic.'),
  ]),

  p('r4-02', 4, 'Who Owns a Language?', '言語はだれのものか', `
English is now spoken by far more people as a second or foreign language than as a first language. This simple fact raises a difficult question: who decides what counts as "correct" English?

For a long time, the answer seemed obvious. Correct English was the English of educated speakers in Britain or the United States, and learners elsewhere were expected to imitate it as closely as possible. Accents and expressions that differed from these models were treated as mistakes to be corrected.

Today, many linguists challenge this view. They point out that in countries such as India, Nigeria, and Singapore, English has developed its own stable patterns of pronunciation, vocabulary, and grammar, which are used confidently by millions of people. To call these patterns errors, they argue, is to confuse difference with deficiency.

This does not mean that anything goes. Communication still depends on shared conventions, and a speaker who wants to be understood internationally must be aware of how others will hear him or her. But the goal of learning English, according to this perspective, is not to sound like a native speaker. It is to be clear, flexible, and intelligible to a wide range of listeners.`, [
    q('r4-02-1', 'What does the first paragraph imply?', [
      'Non-native speakers of English now outnumber native speakers', 'Most people learn English as their first language', 'The number of English learners is decreasing', 'English is no longer used for international communication'],
      '「英語は今や、第一言語としてよりも、第二言語・外国語として話す人のほうがはるかに多い」。',
      'English is now spoken by far more people as a second or foreign language than as a first language.'),
    q('r4-02-2', 'What do the linguists mean by "to confuse difference with deficiency"?', [
      'To treat ways of speaking that are merely different as if they were faulty', 'To believe that all varieties of English are identical', 'To think that native speakers make more mistakes than learners', 'To mix up the vocabulary of different countries'],
      'インドなどの英語には安定した独自の型がある。それを「誤り」と呼ぶのは「違い」を「欠陥」と取り違えることだ、という主張。',
      'To call these patterns errors, they argue, is to confuse difference with deficiency.'),
    q('r4-02-3', 'According to the perspective described in the last paragraph, what is the goal of learning English?', [
      'To be clearly understood by many different kinds of listeners', 'To sound exactly like a native speaker', 'To create a completely new form of English', 'To ignore the conventions that other speakers follow'],
      '「目標はネイティブのように聞こえることではない。明瞭で柔軟で、幅広い聞き手に通じることだ」。「何でもよい」わけではない点にも注意。',
      'It is to be clear, flexible, and intelligible to a wide range of listeners.'),
  ]),

  p('r4-03', 4, 'The Cost of Free', '「無料」の値段', `
Search engines, email services, maps, and social networks are offered to us without charge. It is easy to conclude that these services are simply gifts. Yet the companies that provide them are among the most profitable in the world, and their profits have to come from somewhere.

In most cases, the money comes from advertising. Advertisers will pay a great deal to reach people who are likely to buy their products, and the more a company knows about its users, the more precisely it can target those advertisements. As the saying goes, if you are not paying for the product, you are the product.

Defenders of this model argue that it is a fair exchange. Users receive valuable tools, and in return they allow their data to be used to show them advertisements that may actually be useful. Without advertising, they note, many services would be available only to those who could afford a subscription.

Critics reply that the exchange is hardly fair if one side does not understand its terms. Few people read the long privacy policies they agree to, and fewer still could say what information is collected about them or how long it is kept. A genuine bargain, they insist, requires informed consent.`, [
    q('r4-03-1', 'What point does the author make in the first paragraph?', [
      'Free services must generate profit in some way', 'Free services are gifts from generous companies', 'Companies that offer free services rarely make money', 'People should pay for search engines and maps'],
      '「提供企業は世界有数の高収益企業であり、その利益はどこかから来ているはずだ」。',
      'their profits have to come from somewhere.'),
    q('r4-03-2', 'What argument do defenders of the advertising model make?', [
      'It allows people who cannot afford subscriptions to use the services', 'It protects users from receiving any advertisements', 'It ensures that companies collect no personal data', 'It makes privacy policies shorter and easier to read'],
      '擁護派は「広告がなければ、多くのサービスは購読料を払える人だけのものになる」と指摘する。',
      'Without advertising, they note, many services would be available only to those who could afford a subscription.'),
    q('r4-03-3', 'Why do critics say the exchange is not fair?', [
      'Users do not really know what they have agreed to', 'Advertisements are never useful to users', 'Companies charge hidden fees for their services', 'Privacy policies forbid the use of personal data'],
      '「一方が条件を理解していないなら公正とは言えない」。本当の取引には informed consent（十分な説明にもとづく同意）が必要。',
      'Critics reply that the exchange is hardly fair if one side does not understand its terms.'),
  ]),

  p('r4-04', 4, 'Learning from Failure', '失敗から学ぶ組織', `
In many organizations, admitting a mistake is risky. Employees who report errors may be blamed, passed over for promotion, or even dismissed. As a result, problems are often hidden until they become too large to ignore.

The aviation industry offers a striking contrast. When an accident or a near miss occurs, it is investigated in detail, and the findings are shared across the industry so that the same mistake is not repeated. Pilots are encouraged to report their own errors, and in many systems such reports cannot be used to punish them. This culture of open reporting is widely credited with making commercial flight one of the safest forms of travel.

Researchers studying hospitals have found a similar pattern. In one study, the teams that reported the most errors turned out to be the best-performing teams, not the worst. The likely explanation is not that they made more mistakes, but that their members felt safe enough to speak up, which allowed errors to be caught and corrected early.

The lesson is not that mistakes should be welcomed. It is that an organization which punishes people for revealing failure will, in the end, learn very little from it.`, [
    q('r4-04-1', 'What is described as a result of blaming employees for errors?', [
      'Problems tend to be concealed until they grow serious', 'Employees make fewer mistakes than before', 'Mistakes are reported more quickly', 'Organizations become safer over time'],
      '責められるので「問題は無視できないほど大きくなるまで隠されることが多い」。',
      'problems are often hidden until they become too large to ignore.'),
    q('r4-04-2', 'How does the author explain the hospital study\'s finding?', [
      'Members of the best teams felt secure enough to report errors', 'The best teams actually made the largest number of mistakes', 'The worst teams were punished more often', 'The researchers counted the errors incorrectly'],
      '「より多くミスをしたのではなく、メンバーが安心して声を上げられたから」と説明している。',
      'The likely explanation is not that they made more mistakes, but that their members felt safe enough to speak up'),
    q('r4-04-3', 'Which statement best expresses the main idea of the passage?', [
      'Organizations improve when people can reveal mistakes without fear', 'Mistakes should be encouraged in every workplace', 'The aviation industry has never had an accident', 'Hospitals are more dangerous than airplanes'],
      '「失敗を明かした人を罰する組織は、結局失敗からほとんど学べない」。「ミスを歓迎すべき」ではない点に注意。',
      'an organization which punishes people for revealing failure will, in the end, learn very little from it.'),
  ]),

  p('r4-05', 4, 'Why Cities Are Hotter', '都市はなぜ暑いのか', `
On a summer afternoon, the center of a large city can be several degrees warmer than the surrounding countryside. This phenomenon, known as the urban heat island effect, has several causes.

The most important is the materials that cities are made of. Asphalt roads, concrete buildings, and dark rooftops absorb a large share of the sunlight that falls on them and release the heat slowly, often well into the night. Fields and forests, by contrast, reflect more sunlight, and the water that evaporates from plants and soil cools the air around them. In addition, tall buildings can block the wind, and the heat produced by cars, factories, and air conditioners adds further warmth.

The effect is more than a matter of comfort. During heat waves, the high temperatures in cities increase the risk of heatstroke, particularly among elderly people, and push up the demand for electricity.

Fortunately, some remedies are relatively simple. Painting roofs white or light gray allows them to reflect more sunlight, and planting trees provides both shade and cooling through evaporation. Some cities have also begun to grow plants on rooftops. Ironically, the widespread use of air conditioning, which helps individuals cope with the heat, makes the problem worse for the city as a whole.`, [
    q('r4-05-1', 'According to the passage, what is the most important cause of the urban heat island effect?', [
      'The materials used to build cities', 'The heat produced by air conditioners', 'The lack of wind between tall buildings', 'The number of people living in cities'],
      '「最も重要なのは、都市をつくっている材料である」。風や排熱は In addition で付け加えられた要因。',
      'The most important is the materials that cities are made of.'),
    q('r4-05-2', 'How do fields and forests help keep the air cool?', [
      'They reflect more sunlight, and evaporation from them cools the air', 'They absorb sunlight and release it slowly at night', 'They block the wind that carries heat', 'They produce electricity for air conditioning'],
      '「畑や森はより多くの日光を反射し、植物や土から蒸発する水が周りの空気を冷やす」。',
      'Fields and forests, by contrast, reflect more sunlight, and the water that evaporates from plants and soil cools the air around them.'),
    q('r4-05-3', 'Why does the author use the word "Ironically" in the last paragraph?', [
      'A device that helps people with the heat also adds to the problem', 'White roofs are more expensive than dark roofs', 'Planting trees makes cities hotter in winter', 'Elderly people prefer hot weather'],
      'エアコンは個人が暑さをしのぐ助けになるのに、都市全体では問題を悪化させる、という皮肉。',
      'the widespread use of air conditioning, which helps individuals cope with the heat, makes the problem worse for the city as a whole.'),
  ]),

  p('r4-06', 4, 'The Value of Boredom', '退屈の効用', `
Boredom has a bad reputation. We think of it as an unpleasant state to be escaped as quickly as possible, and modern technology makes escape easy: whenever we have a spare moment, we can reach for a phone and fill it with news, games, or videos.

Some psychologists, however, argue that boredom serves a useful purpose. It is a signal, they say, that what we are currently doing is not satisfying, and that we should look for something more meaningful. Like pain, which warns us of physical harm, boredom pushes us to change our situation.

There is also evidence that boredom can encourage creativity. In one experiment, participants were first asked to complete a dull task, such as copying numbers from a telephone directory. They were then asked to think of as many uses as possible for a pair of plastic cups. Those who had done the boring task came up with more ideas than those who had not. When the mind has nothing interesting to focus on, it seems, it begins to wander and make unexpected connections.

If this is true, the constant stimulation provided by our devices may come at a cost. By never allowing ourselves to be bored, we may be giving up opportunities for reflection and invention.`, [
    q('r4-06-1', 'Why do some psychologists compare boredom to pain?', [
      'Both are signals that push us to change our situation', 'Both are caused by spending too much time on phones', 'Both are physical conditions that need medical care', 'Both disappear if we ignore them long enough'],
      '「痛みが身体の害を知らせるように、退屈は状況を変えるよう私たちを促す」。',
      'Like pain, which warns us of physical harm, boredom pushes us to change our situation.'),
    q('r4-06-2', 'What happened in the experiment described in the passage?', [
      'Participants who did a dull task first produced more ideas', 'Participants who copied numbers became too tired to think', 'Participants who were not bored produced the most ideas', 'Participants refused to finish the boring task'],
      '「退屈な作業をした人のほうが、しなかった人より多くのアイデアを出した」。',
      'Those who had done the boring task came up with more ideas than those who had not.'),
    q('r4-06-3', 'What does the author suggest in the last paragraph?', [
      'Always avoiding boredom may cost us chances to think and create', 'Smartphones should be banned from schools', 'Boredom is more harmful than pain', 'People should do dull tasks every day'],
      '「退屈を決して許さないことで、内省や発明の機会を手放しているのかもしれない」。',
      'By never allowing ourselves to be bored, we may be giving up opportunities for reflection and invention.'),
  ]),

  p('r4-07', 4, 'Measuring a Nation\'s Progress', 'GDPで豊かさは測れるか', `
For most of the twentieth century, the success of a national economy was judged largely by a single number: gross domestic product, or GDP, the total value of the goods and services a country produces in a year. When GDP rose, governments claimed success; when it fell, they faced criticism.

GDP is a useful measure, but it was never designed to capture everything that matters. It counts the money spent on cleaning up after a disaster as a contribution to the economy, yet it ignores the damage the disaster caused. It includes the value of trees cut down and sold, but not the loss of the forest. It also leaves out unpaid work, such as caring for children or elderly relatives, even though such work is essential to any society.

For these reasons, economists and governments have begun to experiment with broader measures of progress. Some combine income with indicators of health and education; others ask people directly how satisfied they are with their lives. Bhutan famously adopted the goal of "gross national happiness."

Such measures have their own problems. Happiness is difficult to define, and surveys can be influenced by the weather or by how a question is worded. Still, many argue that an imperfect measure of what we value is better than a precise measure of something else.`, [
    q('r4-07-1', 'Which of the following is NOT counted in GDP according to the passage?', [
      'Unpaid work such as caring for family members', 'Money spent on cleaning up after a disaster', 'The value of trees that are cut down and sold', 'Goods and services produced in a year'],
      'GDPは「子どもや高齢の家族の世話のような無償労働を除外している」。他の3つは数えられる。NOT問題に注意。',
      'It also leaves out unpaid work, such as caring for children or elderly relatives'),
    q('r4-07-2', 'What problem with happiness surveys does the author mention?', [
      'The results can be affected by the weather or the wording of questions', 'People always say that they are happy', 'They are too expensive for most governments', 'They measure only income and education'],
      '「調査は天気や質問の言葉づかいに左右されうる」。',
      'surveys can be influenced by the weather or by how a question is worded.'),
    q('r4-07-3', 'What does the final sentence mean?', [
      'It is better to measure roughly what matters than to measure exactly what matters less', 'Precise measures are always better than imperfect ones', 'GDP should be replaced by gross national happiness everywhere', 'No measure of progress can ever be useful'],
      '「大切なものの不完全な尺度は、別のものの正確な尺度にまさる」という意味。',
      'an imperfect measure of what we value is better than a precise measure of something else.'),
  ]),

  p('r4-08', 4, 'The Tomato Problem', 'トマトは野菜か果物か', `
Is a tomato a fruit or a vegetable? To a botanist, the answer is clear. A fruit is the part of a flowering plant that develops from the flower and contains the seeds. By this definition, tomatoes, cucumbers, and even peppers are fruits.

Yet few cooks would put tomatoes in a fruit salad. In the kitchen, the distinction between fruits and vegetables is based not on biology but on taste and use: fruits are generally sweet and eaten as desserts or snacks, while vegetables are savory and served as part of a main meal. In 1893, the United States Supreme Court was even asked to decide the question, because imported vegetables were taxed while fruits were not. The court ruled that tomatoes should be treated as vegetables, since that was how ordinary people understood them.

The case illustrates a broader point about categories. We often assume that words reflect natural divisions in the world, waiting to be discovered. In fact, many categories are created to serve particular purposes, and the same object may be classified differently depending on who is doing the classifying and why. Neither the botanist nor the cook is wrong; they are simply answering different questions.`, [
    q('r4-08-1', 'Why was the tomato question brought before the Supreme Court in 1893?', [
      'Because the classification affected whether a tax had to be paid', 'Because botanists and cooks wanted to end their argument', 'Because tomatoes were not allowed in fruit salads', 'Because scientists had discovered a new kind of tomato'],
      '「輸入野菜には課税され、果物には課税されなかった」ので、分類が税に関わった。',
      'because imported vegetables were taxed while fruits were not.'),
    q('r4-08-2', 'On what basis did the court make its decision?', [
      'How ordinary people understood tomatoes', 'The botanical definition of a fruit', 'The sweetness of tomatoes', 'The amount of tax collected'],
      '「それが普通の人々の理解の仕方だったから」野菜として扱うべきだとした。',
      'since that was how ordinary people understood them.'),
    q('r4-08-3', 'What broader point does the author draw from the case?', [
      'Categories often depend on the purpose of the person classifying', 'Words always reflect natural divisions in the world', 'Cooks understand plants better than botanists', 'Courts should decide scientific questions'],
      '「多くの分類は特定の目的のために作られ、だれが何のために分類するかで変わる」。',
      'many categories are created to serve particular purposes'),
  ]),

  p('r4-09', 4, 'Do Grades Motivate?', '成績は学ぶ意欲を高めるか', `
Grades are so familiar a part of schooling that it is hard to imagine education without them. Teachers use them to judge progress, parents use them to check on their children, and universities use them to select students. Many people also assume that grades motivate students to work harder.

Research on motivation complicates this assumption. Psychologists distinguish between intrinsic motivation, which comes from interest in an activity itself, and extrinsic motivation, which comes from rewards or punishments. Studies have found that when people are offered rewards for doing something they already enjoy, their interest in the activity can actually decline. The reward changes how they understand their own behavior: they come to see themselves as working for the prize rather than for the pleasure of the task.

In one study, students who received only written comments on their work showed greater interest and better performance on later tasks than students who received grades, or grades together with comments. It appeared that when a grade was present, students paid attention to the number and ignored the advice.

This does not prove that grades should be abolished. But it suggests that feedback is most useful when it tells learners how to improve, not merely where they stand.`, [
    q('r4-09-1', 'What can happen when people are rewarded for an activity they already enjoy?', [
      'Their interest in the activity may decrease', 'They always become more interested in it', 'They stop caring about rewards', 'They start to enjoy other activities as well'],
      '「すでに楽しんでいることに報酬を出すと、その活動への興味がかえって下がることがある」。',
      'their interest in the activity can actually decline.'),
    q('r4-09-2', 'Why did comments seem less effective when they were given with grades?', [
      'Students focused on the grade and overlooked the advice', 'The comments were too short to be useful', 'Teachers wrote fewer comments when giving grades', 'Students did not understand the comments'],
      '「成績があると、生徒は数字に注目し助言を無視した」。',
      'when a grade was present, students paid attention to the number and ignored the advice.'),
    q('r4-09-3', 'What is the author\'s conclusion?', [
      'Feedback should mainly show learners how they can improve', 'Grades should be abolished immediately', 'Students work harder when they receive grades', 'Universities should stop selecting students'],
      '「成績を廃止すべきとは言えないが、フィードバックは現在地ではなく改善の仕方を示すときに最も役立つ」。',
      'feedback is most useful when it tells learners how to improve, not merely where they stand.'),
  ]),

  p('r4-10', 4, 'The Return of the Wolves', 'オオカミが戻った公園', `
In 1995, after an absence of about seventy years, gray wolves were reintroduced to Yellowstone National Park in the United States. The decision was controversial. Ranchers living near the park feared for their cattle, and many people regarded wolves as dangerous pests.

The effects of the wolves' return went far beyond what most people had expected. Before 1995, the park's elk population had grown large, and the elk ate young trees along the riverbanks, preventing them from growing. Once wolves were present, the elk not only declined in number but also changed their behavior, avoiding open valleys where they could easily be attacked. Trees such as willows began to recover, providing food and building material for beavers, whose dams in turn created ponds for fish and birds.

Some scientists have described this chain of events as a "trophic cascade," in which a change at the top of the food chain spreads downward through the whole ecosystem. Others caution that the story has been simplified. Changes in climate and in human activity also affected the park, and the recovery of plants has been uneven. Nevertheless, the Yellowstone case has encouraged scientists to pay closer attention to the role that predators play in maintaining healthy ecosystems.`, [
    q('r4-10-1', 'Why was the reintroduction of wolves controversial?', [
      'Some people were worried about their livestock and saw wolves as harmful', 'Scientists believed wolves would destroy the trees', 'The park did not have enough space for wolves', 'Wolves had never lived in the area before'],
      '「牧場主は牛を心配し、多くの人がオオカミを危険な害獣とみなした」。',
      'Ranchers living near the park feared for their cattle, and many people regarded wolves as dangerous pests.'),
    q('r4-10-2', 'How did the elk change after wolves returned?', [
      'They became fewer and avoided open valleys', 'They grew in number and ate more trees', 'They moved to the riverbanks to find food', 'They began to hunt beavers'],
      '「エルクは数が減っただけでなく、襲われやすい開けた谷を避けるようになった」。',
      'the elk not only declined in number but also changed their behavior, avoiding open valleys'),
    q('r4-10-3', 'What do some scientists caution about the Yellowstone story?', [
      'It may be too simple, since other factors also influenced the park', 'Wolves had no effect on the ecosystem at all', 'Beavers were the real cause of the changes', 'The reintroduction should be reversed'],
      '「話は単純化されている。気候や人間の活動の変化も影響し、植物の回復はむらがある」。',
      'Others caution that the story has been simplified.'),
  ]),

  p('r4-11', 4, 'Reading on Screens', '画面で読むと理解は浅くなるか', `
More and more reading now takes place on screens rather than on paper. Students read textbooks on tablets, and adults read news on their phones. Does the medium make a difference to how well we understand what we read?

A number of studies suggest that it can. When people read long or complex texts, those who read on paper tend to understand and remember them slightly better than those who read the same texts on a screen. Interestingly, the gap is largest when readers are under time pressure, and it has not disappeared as people have become more familiar with digital devices.

Researchers offer several possible explanations. Screens encourage a habit of quick skimming, which we develop while scrolling through short messages and web pages, and we may carry this habit over to texts that require careful reading. Paper also gives readers a physical sense of where they are in a text, which may help them build a mental map of its structure.

The findings do not mean that digital reading is useless. For short and simple texts, the difference is small or absent, and screens offer advantages such as search functions and adjustable text size. The point is rather that readers should be aware of their habits and slow down when a text demands it.`, [
    q('r4-11-1', 'According to the studies, when is the difference between paper and screens largest?', [
      'When readers have limited time', 'When readers are very familiar with devices', 'When the texts are short and simple', 'When readers can adjust the text size'],
      '「その差は、読み手が時間に追われているときに最も大きい」。',
      'the gap is largest when readers are under time pressure'),
    q('r4-11-2', 'Which explanation for the difference is mentioned in the passage?', [
      'People may apply a habit of quick skimming to texts that need careful reading', 'Screens damage readers\' eyesight', 'Digital texts contain more difficult words', 'Paper books are usually shorter than digital ones'],
      '「短いメッセージをスクロールするうちについた流し読みの癖を、丁寧に読むべき文章にも持ち込むのかもしれない」。',
      'we may carry this habit over to texts that require careful reading.'),
    q('r4-11-3', 'Which statement is consistent with the passage?', [
      'For short and simple texts, screens and paper make little difference', 'The gap has disappeared as people have got used to digital devices', 'Digital reading is useless for students', 'Paper offers search functions that screens lack'],
      '「短く簡単な文章なら差は小さいかない」。差は慣れても消えていない、検索機能は画面の利点。',
      'For short and simple texts, the difference is small or absent'),
  ]),

  p('r4-12', 4, 'The Placebo Puzzle', 'プラセボの不思議', `
A placebo is a treatment with no active ingredient, such as a sugar pill. In medical trials, some patients receive the real drug and others receive a placebo, so that researchers can tell whether the drug works better than the mere expectation of being treated. Remarkably, patients who receive placebos often report real improvements, particularly in conditions such as pain, nausea, and anxiety.

For a long time, it was assumed that placebos work only if patients are deceived, that is, if they believe they are taking a real drug. Recent studies have challenged this assumption. In several experiments, patients with long-term pain were given pills and told honestly that they contained no medicine. Many of them still reported feeling better than patients who received no pills at all.

How can this be explained? One theory is that the ritual of treatment itself, including the attention of a doctor and the act of taking a pill, triggers the body's own mechanisms for reducing pain. Another is that patients learn, through past experience, to associate taking pills with relief.

Placebos are not a cure for everything. They do not shrink tumors or heal broken bones. But the research reminds us that the way treatment is delivered can matter as much as what is delivered.`, [
    q('r4-12-1', 'Why do medical trials give some patients a placebo?', [
      'To find out whether a drug is more effective than the expectation of treatment', 'To save money on expensive drugs', 'To deceive patients into feeling better', 'To test whether sugar is harmful'],
      '「薬が、治療を受けているという期待以上に効くかどうかを見分けるため」。',
      'so that researchers can tell whether the drug works better than the mere expectation of being treated.'),
    q('r4-12-2', 'What was surprising about the recent experiments?', [
      'Patients improved even though they knew the pills contained no medicine', 'Patients refused to take pills without medicine', 'Placebos worked only when patients were deceived', 'Patients felt worse after taking placebos'],
      '「薬が入っていないと正直に伝えられても、多くが良くなったと報告した」。',
      'Many of them still reported feeling better than patients who received no pills at all.'),
    q('r4-12-3', 'What is the main lesson of the passage?', [
      'How a treatment is given can be as important as the treatment itself', 'Placebos can cure any illness', 'Doctors should never tell patients the truth', 'Pills are always better than other treatments'],
      '「治療の届け方は、何を届けるかと同じくらい重要になりうる」。腫瘍や骨折は治さないので「何でも治る」は誤り。',
      'the way treatment is delivered can matter as much as what is delivered.'),
  ]),
];
