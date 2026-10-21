/** レベル1：基礎（高校1年・共通テストの前半）。80〜110語・設問2問 */
import { p, q } from './types';

export const LEVEL1 = [
  p('r1-01', 1, 'The Library Cat', '図書館のネコ', `
A small town library in England has a famous member of staff: a gray cat named Pepper. Pepper first walked into the library on a rainy day six years ago and never left. The librarians gave her food and a soft bed near the window.

Today, many children visit the library just to see Pepper. Some of them did not like reading before, but now they sit next to her and read picture books aloud. One librarian says, "Pepper does not read, but she helps children start reading."`, [
    q('r1-01-1', 'ペッパーが図書館に住むようになったきっかけは何か。', [
      '雨の日に自分から図書館に入ってきた', '図書館の職員が店で買ってきた', '子どもたちが近所から連れてきた', '前の飼い主が図書館にあずけた'],
      '第1段落に「6年前の雨の日に図書館に歩いて入ってきて、それきり出ていかなかった」とある。',
      'Pepper first walked into the library on a rainy day six years ago and never left.'),
    q('r1-01-2', '図書館員の言葉が伝えていることとして最も適切なものはどれか。', [
      'ペッパーは子どもが本を読み始めるきっかけになっている', 'ペッパーは字を読むことができる', 'ペッパーがいるので図書館が静かになった', '子どもたちはペッパーの世話をするために来ている'],
      '「ペッパーは本を読まないが、子どもたちが読み始める手助けをしている」。本が苦手だった子どもがペッパーの横で読むようになった。',
      'Pepper does not read, but she helps children start reading.'),
  ]),

  p('r1-02', 1, 'A New Kind of Lunch', '学校の給食', `
At a junior high school in Japan, students now plan one school lunch each month. In April, a group of second-year students chose a menu from Okinawa. They studied the food of the island and talked with the school cook about the cost.

The cook was worried that the students would choose only sweets and fried food. However, their menu had fish, vegetables, and a small dessert. "They thought about health and money, just like I do every day," she said. The students also made posters to explain each dish to younger students.`, [
    q('r1-02-1', '調理員が最初に心配していたことは何か。', [
      '生徒が甘い物や揚げ物ばかり選ぶこと', '沖縄の食材が手に入らないこと', '生徒が献立を決められないこと', '下級生が給食を残すこと'],
      '「生徒が甘い物と揚げ物しか選ばないのではないかと心配していた」とある。',
      'The cook was worried that the students would choose only sweets and fried food.'),
    q('r1-02-2', '本文の内容と合うものはどれか。', [
      '生徒は料理を説明するポスターも作った', '献立には魚が入っていなかった', '生徒は費用のことは考えなかった', 'この取り組みは年に1回だけである'],
      '最後の文に「下級生に料理を説明するポスターも作った」とある。毎月1回なので年1回ではない。',
      'The students also made posters to explain each dish to younger students.'),
  ]),

  p('r1-03', 1, 'The Bus Stop Bookshelf', 'バス停の本棚', `
In a quiet village, the bus comes only once an hour. People often wait for a long time with nothing to do. Last year, an old man named Mr. Hara put a small wooden bookshelf at the bus stop. He filled it with his own books and wrote a note: "Take one, bring one back."

At first, only a few books moved. But soon people began to add their own books. Now the shelf has over a hundred books, and Mr. Hara buys a new shelf every spring because the old one gets too full.`, [
    q('r1-03-1', '原さんが本棚を置いた理由として最も適切なものはどれか。', [
      'バスを長い時間待つ人が多かったから', '自分の家に本を置く場所がなかったから', '村に図書館を作るように頼まれたから', '古い本を売りたかったから'],
      'バスは1時間に1本しか来ず、人々は何もすることがなく長く待つことが多かった、という状況の後で本棚を置いている。',
      'People often wait for a long time with nothing to do.'),
    q('r1-03-2', '現在の本棚の様子として正しいものはどれか。', [
      '本が100冊を超え、毎年春に新しい棚を買っている', 'ほとんど本が動かず、原さんの本だけである', '本を持ち帰ることが禁止された', '村の人がお金を出して本を買っている'],
      '「今は100冊を超え、古い棚がいっぱいになるので原さんは毎年春に新しい棚を買う」。',
      'Now the shelf has over a hundred books, and Mr. Hara buys a new shelf every spring because the old one gets too full.'),
  ]),

  p('r1-04', 1, 'Learning to Ride', '自転車の練習', `
Emma was nine years old, and she still could not ride a bicycle. All her friends rode to the park after school, but Emma walked. She felt embarrassed.

One Saturday, her older brother took her to an empty parking lot. He did not hold the bicycle. Instead, he took off the pedals. "Just push with your feet and try to balance," he said. After an hour, Emma could roll a long way without touching the ground. Then he put the pedals back on. By evening, she rode all the way home.`, [
    q('r1-04-1', '兄の教え方の特徴として正しいものはどれか。', [
      'ペダルを外して、まずバランスをとる練習をさせた', '自転車の後ろをずっと支えていた', '公園で友だちに教えてもらうようにした', '補助輪をつけて練習させた'],
      '兄は自転車を支えず、ペダルを外して「足で押してバランスをとって」と言った。',
      'He did not hold the bicycle. Instead, he took off the pedals.'),
    q('r1-04-2', 'その日の終わりにエマはどうなったか。', [
      '自転車に乗って家まで帰った', 'まだ自転車に乗れなかった', '兄に家まで送ってもらった', '友だちと公園に行った'],
      '「夕方までに、彼女は家までずっと自転車に乗って帰った」。',
      'By evening, she rode all the way home.'),
  ]),

  p('r1-05', 1, 'A Tree for Every Baby', '誕生の木', `
In one city in Finland, the local government plants a tree for every baby born there. Parents receive a card with a map, so they can find their child's tree in a park. Some families visit the tree on the child's birthday and take a photo next to it.

The city started the program twenty years ago. At that time, the park was an empty field. Now it is a small forest. "The children and the trees grew up together," says one mother. The trees also give the city cleaner air and a place to relax.`, [
    q('r1-05-1', '親が受け取るカードには何があるか。', [
      '子どもの木の場所がわかる地図', '木を育てるための説明書', '公園の入場券', '誕生日の写真'],
      '「親は地図つきのカードを受け取るので、子どもの木を公園で見つけられる」。',
      "Parents receive a card with a map, so they can find their child's tree in a park."),
    q('r1-05-2', '本文の内容と一致するものはどれか。', [
      '20年前は何もない野原だった場所が、今は小さな森になっている', 'この取り組みは最近始まったばかりである', '木は家族の家の庭に植えられる', '木を植えることで市の財政が豊かになった'],
      '「20年前、その公園は何もない野原だった。今では小さな森だ」。',
      'At that time, the park was an empty field. Now it is a small forest.'),
  ]),

  p('r1-06', 1, 'The Lost Umbrella', '忘れられた傘', `
Every year, people leave about 300,000 umbrellas on trains in Tokyo. Most of them are cheap plastic umbrellas, and the owners never come back for them. After a few months, the station must throw them away.

A small company decided to do something about this. It collects the forgotten umbrellas, washes them, and lends them for free at shops near stations. When it suddenly rains, people can borrow one and return it at any shop in the program. The company says it has saved more than 10,000 umbrellas from the trash.`, [
    q('r1-06-1', '忘れられた傘について本文で述べられていることはどれか。', [
      'ほとんどは安いビニール傘で、持ち主が取りに来ない', 'ほとんどが高価な傘で、すぐに持ち主に返される', '駅は傘を何年も保管する', '忘れ物の傘は毎年少なくなっている'],
      '「その多くは安いビニール傘で、持ち主は取りに戻らない」。',
      'Most of them are cheap plastic umbrellas, and the owners never come back for them.'),
    q('r1-06-2', 'この会社の取り組みとして正しいものはどれか。', [
      '傘を洗って、駅の近くの店で無料で貸し出す', '傘を集めて安く売る', '傘を溶かして新しい製品を作る', '駅員に忘れ物を減らすよう呼びかける'],
      '「忘れられた傘を集めて洗い、駅の近くの店で無料で貸し出す」。',
      'It collects the forgotten umbrellas, washes them, and lends them for free at shops near stations.'),
  ]),

  p('r1-07', 1, 'The Quiet Hour', '静かな時間', `
A supermarket in New Zealand has a "quiet hour" every Tuesday evening. During this hour, the music is turned off, the lights are made softer, and staff do not use loud machines. The idea came from a worker whose son has autism. Bright lights and noise made shopping very hard for him.

Many customers like the quiet hour, not only families with special needs. Older people say they can hear the staff more easily, and some office workers say it is the most relaxing hour of their week.`, [
    q('r1-07-1', '「静かな時間」を始めるきっかけは何だったか。', [
      '自閉症の息子をもつ従業員の考え', '店の電気代を減らしたいという考え', '近所の住民からの苦情', '音楽の著作権料の問題'],
      '「その考えは、息子が自閉症である従業員から生まれた」。',
      'The idea came from a worker whose son has autism.'),
    q('r1-07-2', '本文の内容と合うものはどれか。', [
      '特別な支援が必要な家族以外の客にも好評である', '高齢者は店員の声が聞きにくくなったと言っている', 'この時間は毎日ある', '会社員はこの時間を利用しない'],
      '「多くの客が気に入っている。特別な支援が必要な家族だけではない」。',
      'Many customers like the quiet hour, not only families with special needs.'),
  ]),

  p('r1-08', 1, 'Message in a Bottle', 'びんの手紙', `
When Lucas was ten, he wrote a letter, put it in a glass bottle, and threw it into the sea from a beach in France. In the letter, he wrote his address and asked the finder to write back.

He waited for months, but nothing came. He soon forgot about it. Eleven years later, a letter arrived from a fisherman in Portugal. The fisherman had found the bottle in his net. Lucas, now a university student, was so surprised that he traveled to Portugal to meet him. They are still friends today.`, [
    q('r1-08-1', 'ルーカスが手紙に書いたことは何か。', [
      '自分の住所と、見つけた人に返事をくれるようにというお願い', '自分の電話番号と写真', '海をきれいにしようという呼びかけ', '漁師への感謝の言葉'],
      '「手紙には自分の住所を書き、見つけた人に返事をくれるよう頼んだ」。',
      'In the letter, he wrote his address and asked the finder to write back.'),
    q('r1-08-2', '返事が届いたのはいつか。', [
      'びんを海に投げてから11年後', '数か月後', '大学に入る前の年', 'びんを投げた次の日'],
      '「11年後、ポルトガルの漁師から手紙が届いた」。',
      'Eleven years later, a letter arrived from a fisherman in Portugal.'),
  ]),

  p('r1-09', 1, 'Too Much Screen Time?', 'スマホの使いすぎ', `
A high school in Canada tried an experiment. For two weeks, students put their phones in a box when they arrived at school and took them back after the last class.

At first, many students were angry. But by the second week, teachers noticed changes. Students talked more during lunch, and fewer students were late for class. In a survey after the experiment, sixty percent of students said they felt less tired. However, some students said they missed listening to music between classes.`, [
    q('r1-09-1', '2週目に先生たちが気づいた変化はどれか。', [
      '昼食の時間に生徒がよく話すようになった', '生徒の成績が大きく上がった', '遅刻する生徒が増えた', '生徒が授業中に寝るようになった'],
      '「生徒は昼食の間によく話し、授業に遅れる生徒が減った」。',
      'Students talked more during lunch, and fewer students were late for class.'),
    q('r1-09-2', '実験後の調査について正しいものはどれか。', [
      '6割の生徒が疲れにくくなったと答えた', '全員がこの決まりを続けたいと答えた', '音楽を聞けないことに不満をもつ生徒はいなかった', '生徒の6割が怒っていると答えた'],
      '「60％の生徒が疲れが減ったと答えた」。一方で音楽を聞けないのがさみしいという生徒もいた。',
      'In a survey after the experiment, sixty percent of students said they felt less tired.'),
  ]),

  p('r1-10', 1, 'The Night Market', '夜市', `
In Taiwan, night markets are an important part of daily life. They usually open around five in the evening and close after midnight. Visitors can enjoy cheap street food, play simple games, and buy clothes or phone cases.

For tourists, the night market is a good place to try local food. But for many local people, it is simply the place where they eat dinner. Some families visit the same food stand every week, and the owners know their names. One stand owner says, "My customers are like my neighbors."`, [
    q('r1-10-1', '夜市について本文で述べられていることはどれか。', [
      'ふつう夕方5時ごろに開き、真夜中すぎに閉まる', '昼の間だけ開いている', '観光客しか利用しない', '食べ物の値段が高い'],
      '「たいてい夕方5時ごろに開き、真夜中すぎに閉まる」。',
      'They usually open around five in the evening and close after midnight.'),
    q('r1-10-2', '屋台の店主の言葉が表していることとして最も適切なものはどれか。', [
      '常連客との間に近所づきあいのような関係がある', '客の多くは外国から来た観光客である', '近所の人は屋台に来ない', '客が多すぎて名前を覚えられない'],
      '毎週同じ屋台に来る家族がいて、店主は名前を知っている。「お客さんは近所の人のようだ」。',
      'My customers are like my neighbors.'),
  ]),

  p('r1-11', 1, 'The Robot Teacher', 'ロボットの先生', `
An elementary school in South Korea started using a small robot in English classes. The robot can say simple sentences, ask questions, and dance when students give correct answers. The children love it.

However, the robot does not replace the human teacher. "It is good at repeating words many times without getting tired," the teacher explains. "But it cannot see when a child is sad or confused. That is my job." The school plans to use the robot only for speaking practice.`, [
    q('r1-11-1', '先生が考えるロボットの得意なことは何か。', [
      '疲れずに何度でも言葉をくり返すこと', '子どもの気持ちに気づくこと', 'テストを作って採点すること', '英語の文法をくわしく説明すること'],
      '「疲れることなく何度も言葉をくり返すのが得意だ」。',
      'It is good at repeating words many times without getting tired'),
    q('r1-11-2', '本文の内容と一致するものはどれか。', [
      'ロボットは話す練習にだけ使われる予定である', 'ロボットが人間の先生の代わりになった', 'ロボットは子どもが悲しんでいるのに気づける', '子どもたちはロボットを怖がっている'],
      '「学校はロボットを話す練習にだけ使う予定だ」。ロボットは人間の先生の代わりにはならない。',
      'The school plans to use the robot only for speaking practice.'),
  ]),

  p('r1-12', 1, 'Grandma’s Recipe Book', '祖母のレシピ帳', `
After her grandmother died, Mai found an old notebook in the kitchen. It was full of handwritten recipes, and some pages had small stains from sauce and oil. There were no exact amounts. Instead, her grandmother wrote things like "a little sugar" and "cook until it smells good."

At first, Mai's dishes did not taste right. She called her aunts and asked them to cook with her. Little by little, the family remembered the flavors together. Now they meet once a month to cook from the book.`, [
    q('r1-12-1', 'レシピ帳の特徴として正しいものはどれか。', [
      '分量がはっきり書かれていない', 'パソコンで印刷されていた', '料理の写真がたくさんある', '使われた形跡がほとんどない'],
      '「正確な分量はなかった。かわりに『砂糖少し』などと書いてあった」。',
      'There were no exact amounts.'),
    q('r1-12-2', 'マイが料理の味を再現できた方法はどれか。', [
      'おばたちと一緒に料理して、家族で味を思い出した', '料理学校に通った', 'インターネットで同じ料理を調べた', '祖母の友人に作り方を習った'],
      '「おばたちに一緒に料理してもらうよう頼み、家族で少しずつ味を思い出した」。',
      'Little by little, the family remembered the flavors together.'),
  ]),
];
