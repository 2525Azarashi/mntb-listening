/** レベル2：標準（共通テスト本番・中堅私大）。120〜150語・設問2〜3問 */
import { p, q } from './types';

export const LEVEL2 = [
  p('r2-01', 2, 'Why We Forget Names', '名前を忘れるわけ', `
Most of us have had this experience: you meet someone, hear their name, and forget it within a minute. Interestingly, we usually remember the person's face, and even their job, much better than their name.

Psychologists explain that a job gives us something to connect to. If someone is a baker, we can imagine bread, an early morning, or the smell of an oven. A name like "Baker," however, is just a sound with no picture attached. This is called the "Baker-baker paradox."

The lesson is simple. To remember a name, give it a picture. If you meet a woman named Rose, imagine her holding a red flower. The stranger the image, the longer it stays in your memory.`, [
    q('r2-01-1', '職業のほうが名前より覚えやすい理由として本文が挙げているものはどれか。', [
      '職業はイメージと結びつけやすいから', '職業は名前より短いから', '職業はくり返し聞くことが多いから', '名前は外国語であることが多いから'],
      '「職業は結びつけるものを与えてくれる」。パン屋ならパンやオーブンの匂いを思い浮かべられるが、名前はただの音である。',
      'Psychologists explain that a job gives us something to connect to.'),
    q('r2-01-2', '筆者が勧める名前の覚え方はどれか。', [
      '名前に絵（イメージ）をつける', '名前を声に出して10回くり返す', '名前をメモ帳に書いておく', '相手の顔をよく見る'],
      '「名前を覚えるには、それに絵をつけること」。ローズさんなら赤い花を持っている姿を想像する。',
      'To remember a name, give it a picture.'),
    q('r2-01-3', '最後の文の内容と合うものはどれか。', [
      'イメージが奇妙であるほど長く記憶に残る', '普通のイメージのほうが覚えやすい', 'イメージはすぐに忘れてしまう', '奇妙なイメージは記憶を混乱させる'],
      '「イメージが奇妙であるほど、記憶に長く残る」。',
      'The stranger the image, the longer it stays in your memory.'),
  ]),

  p('r2-02', 2, 'The Four-Day Week', '週休3日制', `
Several companies in Britain recently tested a four-day working week. Employees worked 32 hours instead of 40, but their pay stayed the same. Many managers expected the companies to produce less.

The results surprised them. In most companies, the amount of work done stayed about the same, and in some it even increased. Workers took fewer sick days and said they felt less stressed. Because they had only four days, people cut down on long meetings and unnecessary emails.

Not every business found it easy, though. A restaurant, for example, could not simply close for a day without losing customers. It had to hire extra staff and arrange the days carefully. The experiment suggests that the four-day week works best where work can be measured by results rather than by hours.`, [
    q('r2-02-1', '実験の結果として本文で述べられているものはどれか。', [
      '多くの会社で仕事の量はほぼ変わらなかった', 'ほとんどの会社で仕事の量が大きく減った', '従業員の給料が下がった', '病気で休む日が増えた'],
      '「多くの会社で、こなした仕事の量はほぼ同じで、増えた会社もあった」。',
      'In most companies, the amount of work done stayed about the same, and in some it even increased.'),
    q('r2-02-2', 'レストランの例が示しているのはどれか。', [
      '業種によっては週休3日制の導入が難しいこと', 'レストランでは週休3日制が最も成功したこと', '客は休みの日を気にしないこと', 'レストランは会議を減らせなかったこと'],
      '「すべての事業が簡単だったわけではない」の具体例。1日閉めると客を失うので人を増やす必要があった。',
      'Not every business found it easy, though.'),
    q('r2-02-3', '筆者の結論として最も適切なものはどれか。', [
      '働いた時間より成果で仕事を測れる職場に向いている', 'すべての会社がすぐに導入すべきだ', '週休3日制は従業員のストレスを増やす', '会議が多い会社ほど向いている'],
      '最後の文「仕事が時間ではなく成果で測れるところで最もうまくいく」。',
      'The experiment suggests that the four-day week works best where work can be measured by results rather than by hours.'),
  ]),

  p('r2-03', 2, 'Bees in the City', '都会のミツバチ', `
On the roofs of some office buildings in Tokyo, you can find boxes full of honeybees. A group of volunteers started keeping bees in the city center about twenty years ago. Many people thought it was a strange idea, because there seemed to be few flowers among the tall buildings.

In fact, the bees found plenty of food. They fly up to three kilometers to visit trees along the streets, flowers in parks, and even gardens on the Imperial Palace grounds. The honey they make has a unique taste that changes with the seasons.

The project has done more than produce honey. Office workers now plant flowers on their balconies to help the bees, and local schools use the hives to teach children about nature in the city.`, [
    q('r2-03-1', '多くの人がこの計画を奇妙だと思った理由は何か。', [
      '高いビルの間には花が少ないように見えたから', 'ミツバチが人を刺すおそれがあったから', 'ビルの屋上は風が強すぎるから', '都会のはちみつは売れないと思われたから'],
      '「高いビルの間には花がほとんどないように思えたので、多くの人が奇妙な考えだと思った」。',
      'Many people thought it was a strange idea, because there seemed to be few flowers among the tall buildings.'),
    q('r2-03-2', 'この計画がもたらした効果として本文に述べられているものはどれか。', [
      '会社員がベランダに花を植えるようになった', 'ビルの電気代が下がった', '皇居の庭が一般に開放された', '学校がミツバチの飼育をやめた'],
      '最後の段落「会社員はミツバチを助けるためにベランダに花を植えるようになった」。',
      'Office workers now plant flowers on their balconies to help the bees'),
  ]),

  p('r2-04', 2, 'A Second Life for Old Phones', '古いスマホの再利用', `
Many people keep their old phones in a drawer after buying a new one. Some people worry about their personal data. Others simply forget. In Japan alone, millions of unused phones are sitting in homes.

These phones contain small amounts of valuable metals such as gold, silver, and copper. For the Tokyo 2020 Olympic Games, the organizers collected about five million old phones and other small devices from the public. From them, they made all the gold, silver, and bronze medals.

Experts say that recycling is better than mining. Getting one gram of gold from the ground can require digging up a ton of rock, while the same amount can be taken from far less electronic waste. Still, recycling works only if people actually hand in their devices.`, [
    q('r2-04-1', '古いスマホが家に眠っている理由として本文が挙げているものはどれか。', [
      '個人情報を心配したり、単に忘れていたりするから', '新しいスマホが故障したときの予備にするから', '売っても値段がつかないから', '法律で捨てることが禁止されているから'],
      '「個人データを心配する人もいれば、単に忘れている人もいる」。',
      'Some people worry about their personal data. Others simply forget.'),
    q('r2-04-2', '東京2020大会について正しいものはどれか。', [
      '回収した小型機器からすべてのメダルを作った', '金メダルだけを古いスマホから作った', '500万台の新しいスマホを配った', 'メダルの材料を外国から買った'],
      '「約500万台の古いスマホなどを集め、金・銀・銅のすべてのメダルを作った」。',
      'From them, they made all the gold, silver, and bronze medals.'),
    q('r2-04-3', '最後の段落の主旨として最も適切なものはどれか。', [
      'リサイクルは採掘より効率的だが、人が機器を出さなければ成り立たない', '金は電子ごみからは取り出せない', '採掘のほうがリサイクルより環境によい', '専門家はリサイクルに反対している'],
      'リサイクルは採掘よりよいが、「人々が実際に機器を提出して初めて機能する」。',
      'Still, recycling works only if people actually hand in their devices.'),
  ]),

  p('r2-05', 2, 'The Power of Handwriting', '手で書くこと', `
Students today often take notes on laptops because typing is faster than writing by hand. You might think that more notes mean better learning. However, a well-known study suggests the opposite.

In the study, students watched a lecture and took notes either on a laptop or on paper. Those who typed wrote down many more words, often copying the speaker exactly. Those who wrote by hand could not keep up, so they had to choose the important points and put them in their own words. When tested later, the handwriting group understood the ideas better.

The researchers concluded that the slowness of handwriting is actually an advantage. It forces us to think about what we hear instead of simply recording it.`, [
    q('r2-05-1', 'パソコンでノートをとった学生の特徴はどれか。', [
      '話し手の言葉をそのまま写すことが多かった', '大事な点だけを選んで書いた', '書いた語数が少なかった', '講義中に別の作業をしていた'],
      '「タイプした学生ははるかに多くの語を書き、話し手の言葉をそのまま写すことが多かった」。',
      'Those who typed wrote down many more words, often copying the speaker exactly.'),
    q('r2-05-2', '研究者たちの結論はどれか。', [
      '手書きの遅さは、聞いたことを考えさせるので利点である', '手書きは遅いので学習に向かない', 'ノートの量が多いほど理解が深まる', 'パソコンと手書きに差はない'],
      '「手書きの遅さは実は利点だ。聞いたことをただ記録するのではなく考えさせる」。',
      'The researchers concluded that the slowness of handwriting is actually an advantage.'),
  ]),

  p('r2-06', 2, 'Sleeping on It', 'ひと晩寝て考える', `
When people face a difficult decision, they are often told to "sleep on it." This old advice may have a scientific basis. Researchers have found that sleep does not simply rest the brain. During certain stages of sleep, the brain replays and organizes information from the day.

In one experiment, people were given a puzzle with a hidden shortcut. Those who slept for eight hours before trying again were more than twice as likely to discover the shortcut as those who stayed awake for the same length of time.

This does not mean that we should stop thinking about problems during the day. The brain needs information to work with. But after collecting the facts, taking a break, and especially sleeping, may lead to a clearer answer.`, [
    q('r2-06-1', '睡眠中の脳について本文で述べられていることはどれか。', [
      'その日の情報を再生し、整理している', '完全に活動を止めて休んでいる', '新しい情報を受け入れなくなる', '翌日の予定を立てている'],
      '「睡眠のある段階で、脳はその日の情報を再生し整理する」。',
      'During certain stages of sleep, the brain replays and organizes information from the day.'),
    q('r2-06-2', '実験の結果として正しいものはどれか。', [
      '8時間眠った人は近道に気づく割合が2倍以上だった', '起きていた人のほうが早く答えを出した', '睡眠の長さは結果に関係なかった', '眠った人は問題の内容を忘れていた'],
      '「8時間眠った人は、同じ時間起きていた人の2倍以上、近道を見つけやすかった」。',
      'Those who slept for eight hours before trying again were more than twice as likely to discover the shortcut'),
    q('r2-06-3', '最後の段落で筆者が言いたいことはどれか。', [
      'まず事実を集め、そのあと休んだり眠ったりするのがよい', '問題については昼間は考えないほうがよい', '睡眠さえとれば情報は不要である', '難しい決定はすぐに下すべきだ'],
      '日中に考えるのをやめるのではなく、「事実を集めたあと、休憩し、とりわけ眠ること」がよい。',
      'But after collecting the facts, taking a break, and especially sleeping, may lead to a clearer answer.'),
  ]),

  p('r2-07', 2, 'Small Shops, Big Changes', '商店街の工夫', `
In many Japanese towns, the old shopping streets are becoming quiet as people drive to large shopping centers. But one street in Osaka has found a way to bring people back.

Instead of competing on price, the shop owners began offering free lessons. The fish seller teaches people how to clean a fish. The tea shop owner explains how to brew tea properly. The bookshop holds reading events for children on weekends. These lessons cost little, but they give customers a reason to visit and talk with the owners.

As a result, the number of visitors has slowly increased. More importantly, customers now feel a personal connection to the shops. "People don't come just to buy," says the head of the shopping association. "They come because they know us."`, [
    q('r2-07-1', 'この商店街の店主たちがとった方法はどれか。', [
      '値段で競うかわりに無料の教室を開いた', '大型店より安い値段で売った', '駐車場を新しく作った', '営業時間を夜遅くまで延ばした'],
      '「値段で競うかわりに、店主たちは無料の教室を開き始めた」。',
      'Instead of competing on price, the shop owners began offering free lessons.'),
    q('r2-07-2', '商店街の会長の言葉が表していることはどれか。', [
      '客は店主との人間関係があるから来ている', '客は安く買えるから来ている', '客は教室だけが目的で、買い物はしない', '客の数はまだ増えていない'],
      '「人は買うためだけに来るのではない。私たちを知っているから来るのだ」。',
      "They come because they know us."),
  ]),

  p('r2-08', 2, 'The Truth About Multitasking', 'ながら作業', `
Many people believe they are good at multitasking. They answer messages while studying, or listen to a podcast while writing a report. However, research shows that the human brain cannot really focus on two demanding tasks at the same time. Instead, it switches quickly between them.

Each switch has a cost. It takes the brain a moment to remember where it was and what it was doing. These small delays add up. In some studies, people who switched between tasks took up to forty percent longer to finish than people who did one task at a time, and they made more mistakes.

Simple activities such as walking while talking are an exception, because one of them requires almost no attention.`, [
    q('r2-08-1', '研究によると、2つの作業を同時にするとき脳は何をしているか。', [
      '2つの作業の間をすばやく切り替えている', '両方に同時に集中している', '片方の作業を完全に忘れている', '作業の量を自動的に減らしている'],
      '「脳は2つの難しい作業に同時に集中できず、かわりにすばやく切り替えている」。',
      'Instead, it switches quickly between them.'),
    q('r2-08-2', '歩きながら話すことが例外とされる理由はどれか。', [
      '片方の活動にほとんど注意が必要ないから', '歩くと脳の働きがよくなるから', '話す内容が簡単だから', '2つとも同じ脳の部分を使うから'],
      '「片方にはほとんど注意が要らないので例外だ」。',
      'because one of them requires almost no attention.'),
  ]),

  p('r2-09', 2, 'Learning a Language Late', '大人になってからの外国語', `
It is often said that children learn languages more easily than adults. In some ways this is true. Young children who move to a new country usually develop a native-like accent, while adults rarely do.

However, adults have their own strengths. They already understand how language works, so they can learn grammar rules quickly and use them consciously. They can also use dictionaries and study plans. In the first year of learning, adults often make faster progress than children.

What children have is time and freedom from embarrassment. They hear the language for many hours every day and are not afraid of making mistakes. Adults who want to succeed may need to copy this attitude, not the child's brain.`, [
    q('r2-09-1', '大人の学習者の強みとして本文が挙げているものはどれか。', [
      '文法の規則をすばやく理解して意識的に使える', '母語話者のような発音を身につけやすい', '間違えることを恐れない', '毎日長い時間その言語を聞いている'],
      '「言語の仕組みをすでに理解しているので、文法規則をすばやく学び意識的に使える」。',
      'They already understand how language works, so they can learn grammar rules quickly and use them consciously.'),
    q('r2-09-2', '筆者が大人に勧めていることとして最も適切なものはどれか。', [
      '子どもの脳ではなく、子どもの態度をまねること', '子どもと同じ学校に通うこと', '辞書を使わずに学ぶこと', '発音の練習をやめること'],
      '最後の文「子どもの脳ではなく、この態度をまねる必要があるかもしれない」。この態度＝多くの時間ふれ、間違いを恐れないこと。',
      "Adults who want to succeed may need to copy this attitude, not the child's brain."),
    q('r2-09-3', '本文の内容と一致するものはどれか。', [
      '学習の最初の1年は大人のほうが子どもより速く進むことが多い', '大人は子どもに比べてすべての点で劣っている', '子どもは文法の規則を意識して使う', '大人もたいてい母語話者のような発音になる'],
      '「学習の最初の1年では、大人のほうが子どもより速く進歩することが多い」。',
      'In the first year of learning, adults often make faster progress than children.'),
  ]),

  p('r2-10', 2, 'Why Ice Floats', '氷はなぜ浮くか', `
Most substances become heavier, or denser, when they change from liquid to solid. A piece of solid wax, for example, sinks in melted wax. Water is unusual. When it freezes, its molecules form an open structure with a lot of empty space, so ice is about nine percent less dense than liquid water. That is why ice floats.

This small fact is very important for life on Earth. In winter, ice forms on the surface of lakes and acts like a blanket. The water below stays liquid, and fish can survive until spring. If ice sank, lakes would freeze from the bottom up, and many of them might become solid ice. Life in cold regions would be very different.`, [
    q('r2-10-1', '水が「珍しい」とされる理由はどれか。', [
      '固体になると液体より密度が小さくなるから', '固体になると重くなるから', 'ろうと同じように沈むから', '凍るときに分子のすき間がなくなるから'],
      '多くの物質は固体になると密度が大きくなるが、水は凍るとすき間の多い構造になり、液体より約9％密度が小さい。',
      'so ice is about nine percent less dense than liquid water.'),
    q('r2-10-2', '本文の内容から、氷が沈むとしたらどうなると考えられるか。', [
      '湖が底から凍り、全体が氷になるものもあるだろう', '湖の表面だけが凍るだろう', '魚は冬の間も変わらず生きられるだろう', '寒い地域の生き物は今と同じだろう'],
      '「もし氷が沈めば、湖は底から凍り、その多くは固い氷になるかもしれない」。',
      'If ice sank, lakes would freeze from the bottom up, and many of them might become solid ice.'),
  ]),

  p('r2-11', 2, 'Reviews You Can Trust?', '口コミは信用できるか', `
Before buying something online, most of us check the reviews. A product with hundreds of five-star ratings seems like a safe choice. But not all reviews are honest. Some sellers pay people to write positive reviews, and some even write them themselves.

There are clues that can help. Fake reviews are often very short and use general words like "great" or "amazing" without details. Many of them appear within a few days. Real reviews, on the other hand, tend to mention specific experiences, including small problems. Interestingly, a product with a 4.5 rating may be more trustworthy than one with a perfect 5.0, because real customers rarely agree completely.`, [
    q('r2-11-1', 'にせの口コミの特徴として本文が挙げているものはどれか。', [
      '短く、具体的な内容のない一般的な言葉を使う', '小さな問題点についても書いている', '長い期間にわたって少しずつ投稿される', '具体的な体験がくわしく書かれている'],
      '「にせの口コミは短く、詳細なしに『すごい』などの一般的な言葉を使うことが多い」。',
      'Fake reviews are often very short and use general words like "great" or "amazing" without details.'),
    q('r2-11-2', '評価4.5の商品のほうが5.0より信用できる場合がある理由はどれか。', [
      '本物の客の意見が完全に一致することはめったにないから', '評価が高すぎる商品は値段が高いから', '4.5の商品のほうが口コミの数が多いから', '5.0の評価はシステムの誤りだから'],
      '「本物の客が完全に意見が一致することはめったにないので」。',
      'because real customers rarely agree completely.'),
  ]),

  p('r2-12', 2, 'The Walking Meeting', '歩きながら会議', `
Some companies have started holding "walking meetings." Instead of sitting around a table, two or three people discuss their work while walking outside or around the office building.

Supporters say this has several benefits. Walking is good for health, of course, but it also seems to help creativity. In a study at an American university, people came up with about sixty percent more creative ideas while walking than while sitting. Walking side by side may also make conversations feel more equal and relaxed than facing each other across a desk.

Walking meetings are not suitable for everything. They do not work well when people need to look at documents or when more than four people take part. They are best for brainstorming and one-to-one talks.`, [
    q('r2-12-1', '大学の研究で分かったことはどれか。', [
      '歩いているときのほうが座っているときより創造的な考えが多く出た', '座っているほうが集中できた', '歩くと会議の時間が短くなった', '歩きながらだと話し合いが難しくなった'],
      '「歩いているときは座っているときより約60％多く創造的な考えを出した」。',
      'people came up with about sixty percent more creative ideas while walking than while sitting.'),
    q('r2-12-2', '歩きながらの会議に向いていない場面はどれか。', [
      '書類を見る必要があるとき', 'アイデアを出し合うとき', '1対1で話すとき', '2〜3人で話すとき'],
      '「書類を見る必要があるときや、4人より多く参加するときはうまくいかない」。',
      'They do not work well when people need to look at documents or when more than four people take part.'),
  ]),
];
