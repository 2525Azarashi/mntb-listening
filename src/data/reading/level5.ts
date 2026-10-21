/** レベル5：最難関（東大・京大・医学部）。抽象度の高い論説・200〜250語・設問3問（英語） */
import { p, q } from './types';

export const LEVEL5 = [
  p('r5-01', 5, 'The Map and the Territory', '地図と現地', `
Every map is a lie, but a useful one. To be of any value, a map must leave out almost everything about the place it represents. A map that showed every tree, every stone, and every passing cloud would have to be as large as the land itself, and would therefore be useless. The cartographer's art lies not in reproducing reality but in deciding what to ignore.

The same is true of scientific models, economic forecasts, and, arguably, of language itself. When we describe a person as "generous" or a policy as "fair," we select certain features of a complex reality and pass over others. Such simplification is not a defect of thought; it is the condition that makes thought possible.

The danger arises when we forget that a simplification has taken place. A traveler who trusts a map so completely that he walks into a river not marked on it has confused the representation with the thing represented. Similarly, an economist who treats a model's assumptions as facts about human beings may be surprised when real people behave otherwise.

The appropriate response is not to abandon maps, which would leave us lost, but to hold them with a certain lightness: to use them while remembering what they were designed to show, and what, by necessity, they were designed to omit.`, [
    q('r5-01-1', 'Why does the author call every map "a lie, but a useful one"?', [
      'A map is valuable precisely because it omits most details of reality', 'Cartographers deliberately include false information', 'Maps are always out of date by the time they are printed', 'A map is useful only if it is as large as the land itself'],
      '地図は役立つためにほとんどすべてを省かねばならない。現実をそのまま写さない（=lie）が、だからこそ役立つ。',
      'To be of any value, a map must leave out almost everything about the place it represents.'),
    q('r5-01-2', 'According to the passage, what is the real danger of simplification?', [
      'Forgetting that the simplification has been made', 'Making a map that is too detailed to read', 'Using words such as "generous" or "fair"', 'Relying on more than one model at a time'],
      '「危険は、単純化が行われたことを忘れるときに生じる」。単純化自体は思考を可能にする条件。',
      'The danger arises when we forget that a simplification has taken place.'),
    q('r5-01-3', 'Which attitude toward maps and models does the author recommend?', [
      'Using them while keeping in mind what they leave out', 'Abandoning them in favor of direct experience', 'Trusting them completely to avoid confusion', 'Adding as many details to them as possible'],
      '「捨てるのではなく軽やかに持つ。何を示すために作られ、何を省かざるをえなかったかを覚えておきながら使う」。',
      'to use them while remembering what they were designed to show'),
  ]),

  p('r5-02', 5, 'The Tyranny of Metrics', '数値指標の暴走', `
When a measure becomes a target, it ceases to be a good measure. This principle, often attributed to the economist Charles Goodhart, describes a pattern that appears wherever institutions try to manage performance through numbers.

Consider a hospital that is judged by the proportion of patients seen within four hours of arriving at the emergency department. The figure was originally chosen because it seemed to reflect the quality of care. Once staff are rewarded or punished according to it, however, their behavior changes. Patients may be moved to a waiting area that technically counts as "seen," or treated hastily as the deadline approaches. The number improves; the care it was meant to reflect may not.

The problem is not that the people involved are dishonest. Most are responding rationally to the incentives they face. The difficulty is that any single indicator captures only part of what an organization is trying to achieve, and when attention is concentrated on that part, the unmeasured remainder tends to be neglected.

None of this implies that measurement should be abandoned; without data, organizations would be blind to their own failures. What it implies is that numbers should inform judgment rather than replace it. A figure is best treated as a question—why has this changed?—rather than as an answer.`, [
    q('r5-02-1', 'What does the hospital example illustrate?', [
      'Targeting a figure can improve the number without improving what it represents', 'Emergency departments are generally poorly managed', 'Four hours is too short a time to treat patients', 'Staff deliberately falsify hospital records'],
      '「数字は改善するが、それが反映するはずだったケアは改善しないかもしれない」。',
      'The number improves; the care it was meant to reflect may not.'),
    q('r5-02-2', 'How does the author explain the behavior of the people involved?', [
      'They are reacting sensibly to the incentives placed on them', 'They are dishonest and want to deceive their managers', 'They do not understand how the indicator is calculated', 'They are opposed to any form of measurement'],
      '「関係者が不誠実なのではない。多くは直面する誘因に合理的に反応している」。',
      'Most are responding rationally to the incentives they face.'),
    q('r5-02-3', 'What does the author mean by treating a figure "as a question rather than as an answer"?', [
      'Numbers should prompt investigation and support judgment rather than settle matters', 'Numbers should be ignored when they are inconvenient', 'Organizations should collect data only when asked to', 'Every figure should be checked by an independent auditor'],
      '数値は判断を置き換えるのではなく情報を与えるべき。「なぜ変わったのか」と問いを立てるきっかけとして使う。',
      'numbers should inform judgment rather than replace it.'),
  ]),

  p('r5-03', 5, 'Memory as Reconstruction', '記憶は再構成される', `
We tend to think of memory as a kind of recording. An event happens, the brain stores it, and when we remember, we simply play the recording back. On this view, forgetting is a matter of the recording fading, and a vivid memory is a reliable one.

Decades of research have shown this picture to be mistaken. Remembering is not retrieval but reconstruction. Each time we recall an event, we rebuild it from fragments, filling the gaps with general knowledge, expectations, and information acquired afterward. In well-known experiments, people who watched a film of a car accident and were later asked how fast the cars were going when they "smashed" into each other estimated higher speeds than those asked about cars that "hit" each other. Some even reported seeing broken glass that had not been in the film.

Particularly troubling is the finding that confidence is a poor guide to accuracy. Memories of dramatic public events, which people often describe as perfectly clear, have been shown to change substantially over the years, while their owners remain certain that nothing has changed.

From an evolutionary perspective, this flexibility may not be a flaw. A memory system designed to guide future action has little reason to preserve the past exactly; it needs instead to extract what is useful and to update it as circumstances change. The cost of this design becomes apparent only when we ask memory to do what it was never built for: to serve as a precise record, as in a court of law.`, [
    q('r5-03-1', 'What did the car accident experiment demonstrate?', [
      'The wording of a later question can alter what people remember', 'People remember fast cars better than slow ones', 'Films are a poor way of studying memory', 'Most people can estimate speed accurately'],
      'smashed と聞かれた人は速度を高く見積もり、なかったガラスまで見たと報告した。後から得た情報で記憶が作り直される例。',
      'Some even reported seeing broken glass that had not been in the film.'),
    q('r5-03-2', 'What is "particularly troubling" according to the passage?', [
      'Feeling sure about a memory does not mean the memory is accurate', 'Memories of public events fade completely within a year', 'People refuse to admit that their memories have changed', 'Dramatic events are impossible to remember'],
      '「自信は正確さのよい目安にならない」。',
      'confidence is a poor guide to accuracy.'),
    q('r5-03-3', 'Why might the reconstructive nature of memory not be a flaw from an evolutionary viewpoint?', [
      'Memory evolved to guide future behavior, not to keep an exact record of the past', 'Exact memories would take up too much space in the brain', 'Early humans did not need to remember anything', 'Courts of law existed before memory evolved'],
      '「将来の行動を導くための記憶システムには、過去を正確に保存する理由がほとんどない」。',
      'A memory system designed to guide future action has little reason to preserve the past exactly'),
  ]),

  p('r5-04', 5, 'The Problem of Other Minds', '他者の心', `
I know that I have thoughts and feelings because I experience them directly. But how do I know that anyone else does? I can observe other people's behavior: they cry, laugh, and complain of pain. Yet behavior is not experience. It is at least conceivable that another person might act exactly as I do while experiencing nothing at all.

Philosophers have offered various responses to this puzzle. The most common is an argument from analogy: since other people are physically similar to me and behave as I do in similar circumstances, it is reasonable to infer that they have similar inner lives. Critics point out, however, that this argument generalizes from a single case—my own—which would be considered weak reasoning in any other context.

Others have argued that the puzzle rests on a confusion. On this view, our concept of a mind is not derived from private inspection of our own experience and then projected onto others; rather, we learn words like "pain" and "joy" in a shared public world, by observing how they are used in connection with behavior. If so, the skeptic who doubts that others have minds is using a vocabulary whose very meaning presupposes that they do.

Whatever the merits of these arguments, the practical stakes are rising. As machines become increasingly capable of imitating human conversation, the question of what, if anything, lies behind behavior is no longer merely academic.`, [
    q('r5-04-1', 'What weakness do critics find in the argument from analogy?', [
      'It draws a general conclusion from only one example', 'It ignores the physical differences between people', 'It relies too heavily on scientific experiments', 'It assumes that behavior and experience are the same'],
      '「この議論はただ一つの事例（自分）から一般化しており、他の文脈なら弱い推論とされる」。',
      'this argument generalizes from a single case—my own—which would be considered weak reasoning in any other context.'),
    q('r5-04-2', 'According to the view described in the third paragraph, why is the skeptic\'s position problematic?', [
      'The words the skeptic uses already assume that others have minds', 'The skeptic has never observed other people\'s behavior', 'The skeptic cannot prove that he himself has a mind', 'The skeptic relies on an argument from analogy'],
      '心を表す語は公共の世界で行動と結びつけて学ばれる。だから懐疑論者は、他者に心があることを前提とする語彙を使っている。',
      'the skeptic who doubts that others have minds is using a vocabulary whose very meaning presupposes that they do.'),
    q('r5-04-3', 'Why does the author say the question is "no longer merely academic"?', [
      'Machines that imitate human conversation make the question practically important', 'Philosophers have finally solved the problem', 'Most people now doubt that others have minds', 'Scientists can now observe experience directly'],
      '「機械が人間の会話をまねる能力を高めるにつれて」、行動の背後に何があるのかは実際的な問題になっている。',
      'As machines become increasingly capable of imitating human conversation'),
  ]),

  p('r5-05', 5, 'Risk and Perception', 'リスクの感じ方', `
Statistically, driving a car is far more dangerous than flying. Yet many people who drive every day without anxiety feel real fear when boarding an airplane. Such discrepancies between measured risk and perceived risk are not simply errors to be corrected by better information; they reveal something about how human beings evaluate danger.

Research suggests that we judge risks not only by their probability but by their character. Risks that are imposed on us seem worse than risks we choose; risks that are unfamiliar seem worse than those we encounter daily; and risks that could kill many people at once seem worse than those that kill the same number one at a time. A driver feels in control of the car, whereas a passenger in an airplane has surrendered control to strangers.

Experts sometimes dismiss such reactions as irrational. But this dismissal assumes that the only thing that matters about a risk is the expected number of deaths. People may reasonably care about other things as well: whether a risk is fairly distributed, whether those responsible can be held accountable, whether it was accepted voluntarily. A society that ignored these concerns in the name of statistical efficiency might make decisions that are technically optimal but widely regarded as unjust.

This is not to say that perception should always prevail over calculation. Fear can be manipulated, and exaggerated concern about rare dangers can divert resources from common ones. The challenge is to treat public perception neither as noise to be eliminated nor as a verdict to be obeyed, but as evidence about what people value.`, [
    q('r5-05-1', 'According to the passage, which kind of risk tends to seem worse?', [
      'A risk that is forced on us rather than chosen', 'A risk that we encounter every day', 'A risk that kills people one at a time', 'A risk that we feel we can control'],
      '「押しつけられたリスクは、自分で選んだリスクより悪く思える」。他の3つは逆。',
      'Risks that are imposed on us seem worse than risks we choose'),
    q('r5-05-2', 'What assumption does the author attribute to experts who dismiss public fears as irrational?', [
      'That the expected number of deaths is the only relevant feature of a risk', 'That the public has access to better information than experts', 'That flying is more dangerous than driving', 'That fear cannot be manipulated'],
      '「その切り捨ては、リスクで重要なのは予想死者数だけだと仮定している」。',
      'this dismissal assumes that the only thing that matters about a risk is the expected number of deaths.'),
    q('r5-05-3', 'Which best summarizes the author\'s position?', [
      'Public perceptions of risk should be taken seriously as information about values, but not followed blindly', 'Public fears should always determine government policy', 'Statistical calculation should replace public opinion entirely', 'Rare dangers deserve more resources than common ones'],
      '「世論の受け止め方を、消すべき雑音とも従うべき判決ともせず、人々が何を大切にするかの証拠として扱う」。',
      'as evidence about what people value.'),
  ]),

  p('r5-06', 5, 'The Expert Problem', '専門家への信頼', `
Modern societies depend on experts to an extent that is rarely acknowledged. Few of us could verify for ourselves that the earth orbits the sun, that a vaccine is safe, or that a bridge will bear the weight of the traffic crossing it. We accept such claims not because we have examined the evidence but because we trust the people and institutions that have.

This dependence is often described as a weakness, a failure to think for ourselves. Yet it is better understood as a division of cognitive labor, comparable to the division of physical labor that makes an economy productive. No individual could master more than a tiny fraction of what is known, and a society in which everyone insisted on checking everything personally would know very little.

The difficulty is that trust, once given, can be abused, and the layperson is by definition poorly placed to tell genuine expertise from its imitation. What, then, can justify trust? Not, in most cases, the content of an expert's claims, which the layperson cannot evaluate, but features of the system in which the claims are made: whether experts are independent of those who would profit from their conclusions, whether their work is open to criticism by other experts, and whether the institution has a record of correcting its own mistakes.

On this view, the appropriate question for a citizen is less "Is this claim true?" than "Is this the kind of source whose claims tend to be corrected when they are false?"`, [
    q('r5-06-1', 'How does the author reinterpret our dependence on experts?', [
      'As a sharing of intellectual work that allows a society to know more', 'As evidence that most people are unable to think', 'As a temporary stage that education will overcome', 'As a weakness that should be eliminated'],
      '「弱さと言われがちだが、むしろ認知的な分業と理解すべきだ」。経済を生産的にする分業と同じ。',
      'Yet it is better understood as a division of cognitive labor'),
    q('r5-06-2', 'According to the passage, why can laypeople not usually judge experts by the content of their claims?', [
      'They lack the knowledge needed to evaluate those claims', 'Experts refuse to explain their conclusions', 'The claims are kept secret by institutions', 'The content of claims changes too quickly'],
      '「素人はその内容を評価できない」ので、内容ではなく制度の特徴で判断するしかない。',
      'Not, in most cases, the content of an expert\'s claims, which the layperson cannot evaluate'),
    q('r5-06-3', 'Which of the following would the author regard as a good reason to trust a source?', [
      'It has a history of admitting and fixing its own errors', 'Its experts are paid by companies that benefit from their findings', 'It never changes its conclusions', 'It is supported by a large number of ordinary citizens'],
      '信頼の根拠の1つは「その機関が自らの誤りを正してきた実績があるか」。利害関係者からの独立も挙げられているので②は逆。',
      'whether the institution has a record of correcting its own mistakes.'),
  ]),

  p('r5-07', 5, 'Translation and Loss', '翻訳で失われるもの', `
It is often said that poetry is what gets lost in translation. The remark contains a truth, but it can also mislead, for it implies that an original text possesses a fixed meaning which a translation either preserves or fails to preserve. The reality of translation is more interesting.

Languages do not simply attach different labels to the same set of objects and ideas. They divide experience differently. Where one language has a single word for a color, another distinguishes two; where one marks whether an event was witnessed or merely reported, another leaves the question open. A translator therefore cannot avoid making decisions that the original author never had to make. To translate a sentence from a language that does not mark gender into one that does, for instance, the translator may be forced to decide whether a character is male or female.

Seen in this light, translation is not a copy but an interpretation, and every translation emphasizes some aspects of the original at the expense of others. This explains why great works are translated again and again: each generation finds in them something that earlier translations had chosen not to bring out.

Loss, then, is only half the story. A translation can also reveal possibilities in a text that readers of the original had overlooked, precisely because the translator has been obliged to look at every word and ask what it really commits the author to.`, [
    q('r5-07-1', 'Why does the author say the remark about poetry "can also mislead"?', [
      'It suggests that a text has a single fixed meaning to be kept or lost', 'It implies that poetry cannot be translated at all', 'It ignores the fact that prose is harder to translate', 'It assumes that translators are poor writers'],
      '「原文には決まった意味があり、翻訳はそれを保つか失うかだ、と示唆してしまう」から誤解を招く。',
      'it implies that an original text possesses a fixed meaning which a translation either preserves or fails to preserve.'),
    q('r5-07-2', 'What does the example of gender illustrate?', [
      'A translator may have to make choices that the original author did not', 'Some languages are more precise than others', 'Translators often change the characters in a story', 'Gender is unimportant in literature'],
      '性を区別しない言語から区別する言語へ訳すとき、訳者は原作者が決めなくてよかったことを決めざるをえない。',
      'A translator therefore cannot avoid making decisions that the original author never had to make.'),
    q('r5-07-3', 'Which statement best reflects the author\'s view in the final paragraph?', [
      'Translation can bring to light aspects of a text that original readers missed', 'Translation always reduces the value of a great work', 'Original readers understand a text better than any translator', 'Great works should be translated only once'],
      '「損失は話の半分にすぎない。翻訳は原文の読者が見落としていた可能性を明らかにしうる」。',
      'A translation can also reveal possibilities in a text that readers of the original had overlooked'),
  ]),

  p('r5-08', 5, 'Antibiotics and Evolution', '抗生物質と進化', `
When antibiotics were introduced in the 1940s, they seemed to promise the end of bacterial disease. Infections that had killed millions could suddenly be cured in days. Less than a century later, the World Health Organization regards antibiotic resistance as one of the most serious threats to global health. How did a triumph turn into a crisis?

The answer lies in evolution by natural selection. In any large population of bacteria, a few individuals may, by chance, carry a genetic variation that allows them to survive a particular drug. When the drug is used, the susceptible bacteria die, and the resistant ones are left to multiply without competition. Because bacteria reproduce extremely quickly, a resistant strain can become dominant within a short period. Bacteria can also pass genes for resistance directly to one another, even across species, which accelerates the process further.

Human behavior has supplied the selective pressure. Antibiotics are frequently prescribed for viral infections, against which they are useless; patients often stop taking them as soon as they feel better, allowing the hardiest bacteria to survive; and in many countries, large quantities are given to farm animals to make them grow faster.

The lesson is that resistance is not a failure of the drugs but a predictable consequence of their use. Every dose favors the bacteria that can withstand it. The goal, therefore, cannot be to defeat bacteria once and for all, but to use antibiotics in ways that slow the evolution of resistance, while developing new treatments to stay ahead of it.`, [
    q('r5-08-1', 'According to the passage, how does a resistant strain become dominant?', [
      'The drug kills the vulnerable bacteria, leaving resistant ones to multiply', 'The drug causes all bacteria to change their genes', 'Resistant bacteria attack and destroy other bacteria', 'Patients transmit the drug to other people'],
      '「薬で感受性のある菌が死に、耐性菌が競争相手なしに増える」。',
      'the susceptible bacteria die, and the resistant ones are left to multiply without competition.'),
    q('r5-08-2', 'Which human behavior is NOT mentioned as contributing to resistance?', [
      'Developing new antibiotics too slowly', 'Using antibiotics against viral infections', 'Stopping treatment once symptoms improve', 'Giving antibiotics to farm animals to promote growth'],
      '本文が挙げるのは「ウイルス感染への処方」「よくなったら服用をやめる」「家畜の成長促進」の3つ。NOT問題。',
      'Human behavior has supplied the selective pressure.'),
    q('r5-08-3', 'What does the author mean by saying resistance is "not a failure of the drugs"?', [
      'Resistance is an expected result of natural selection whenever the drugs are used', 'The drugs were never effective against bacteria', 'Doctors are responsible for every case of resistance', 'New drugs will completely solve the problem'],
      '「耐性は薬の失敗ではなく、使用の予測できる帰結である」。使うたびに耐えられる菌が有利になる。',
      'resistance is not a failure of the drugs but a predictable consequence of their use.'),
  ]),

  p('r5-09', 5, 'The Paradox of Tolerance', '寛容のパラドックス', `
A tolerant society allows its members to hold and express a wide variety of opinions, including opinions that most people find offensive. But should it tolerate those who would, if they gained power, abolish tolerance itself? The philosopher Karl Popper famously argued that it should not: unlimited tolerance, he warned, would lead to the disappearance of tolerance, since the intolerant would exploit the freedom granted to them in order to destroy it.

Popper's argument is often quoted as if it justified suppressing any view that one regards as intolerant. This reading ignores an important qualification. Popper did not recommend silencing intolerant opinions as long as they could be countered by rational argument and kept in check by public opinion. Suppression was justified, in his view, only when the intolerant refused to engage in argument at all and instead taught their followers to answer arguments with violence.

The distinction matters because the label "intolerant" is easily applied to one's opponents. If every disagreement could be redescribed as a threat to tolerance, the principle would become a weapon for silencing dissent, and the society it was meant to protect would itself become intolerant.

The paradox, then, does not offer a simple rule. It marks a boundary that must be drawn with great care: a tolerant society must be prepared to defend itself, but it must also resist the temptation to treat the mere expression of disagreeable ideas as an attack.`, [
    q('r5-09-1', 'Why, according to Popper, would unlimited tolerance lead to the disappearance of tolerance?', [
      'The intolerant could use the freedom they are given to destroy that freedom', 'People would become bored with too many opinions', 'Governments would refuse to protect free speech', 'Offensive opinions would become more popular than tolerant ones'],
      '「不寛容な者は与えられた自由を利用して、それを壊すだろう」。',
      'the intolerant would exploit the freedom granted to them in order to destroy it.'),
    q('r5-09-2', 'Under what condition did Popper consider suppression justified?', [
      'When the intolerant reject argument and encourage violence instead', 'Whenever an opinion is offensive to most people', 'When an opinion is held by a minority', 'Whenever public opinion disagrees with a view'],
      '「不寛容な者が議論を一切拒み、議論に暴力で答えるよう教えるときだけ」正当化される。',
      'Suppression was justified, in his view, only when the intolerant refused to engage in argument at all'),
    q('r5-09-3', 'What danger does the author point out in the third paragraph?', [
      'The principle could be misused to silence people who merely disagree', 'Tolerant societies are too weak to defend themselves', 'Popper\'s argument has been forgotten by most people', 'Rational argument can never defeat intolerant opinions'],
      '「どんな意見の対立も寛容への脅威と言い換えられるなら、原理は異論を封じる武器になる」。',
      'the principle would become a weapon for silencing dissent'),
  ]),

  p('r5-10', 5, 'Why Do We Sleep?', '眠りの謎', `
Sleep is one of the most puzzling of animal behaviors. For several hours each day, an animal becomes unaware of its surroundings and largely unable to respond to danger. From an evolutionary point of view, this seems an extraordinary risk. If sleep served no essential purpose, natural selection should long ago have produced animals that did without it. Yet virtually every animal studied, from fruit flies to whales, shows some form of sleep.

For much of the twentieth century, scientists could say more about what sleep was not than about what it was for. It is not simply rest, since the sleeping brain is in some respects as active as the waking one. Recent research, however, has begun to identify specific functions. During sleep, the brain appears to consolidate memories, strengthening some connections formed during the day and weakening others. Experiments in mice have also shown that the spaces between brain cells expand during sleep, allowing fluid to wash away waste products that accumulate while the animal is awake.

These discoveries do not necessarily mean that sleep evolved for any one of these purposes. It is possible that sleep began for one reason and was later put to other uses, much as feathers may have evolved for warmth before they were used for flight.

What is clear is that sleep is not a passive state of switching off. It is an active process that the brain cannot perform while it is busy dealing with the outside world.`, [
    q('r5-10-1', 'Why does sleep seem puzzling from an evolutionary point of view?', [
      'It leaves animals vulnerable, so it should have disappeared unless it is essential', 'Only a few species of animals sleep', 'Sleeping animals use more energy than waking ones', 'Sleep makes animals more aggressive'],
      '「周囲に気づけず危険に反応できない」という大きなリスク。本質的な目的がなければ淘汰で消えていたはず。',
      'If sleep served no essential purpose, natural selection should long ago have produced animals that did without it.'),
    q('r5-10-2', 'What did experiments in mice show?', [
      'Waste products are cleared from the brain more easily during sleep', 'Mice do not need to sleep at all', 'Brain cells grow larger while mice are awake', 'Memories are erased completely during sleep'],
      '「睡眠中は脳細胞の間のすき間が広がり、液体が老廃物を洗い流す」。',
      'allowing fluid to wash away waste products that accumulate while the animal is awake.'),
    q('r5-10-3', 'What is the point of the comparison with feathers?', [
      'A feature may have arisen for one purpose and later served others', 'Birds sleep more than other animals', 'Sleep evolved in order to keep animals warm', 'Flight is more important than sleep'],
      '羽毛が保温のために進化し後に飛行に使われたように、睡眠も別の理由で始まり、のちに他の用途に使われたのかもしれない。',
      'It is possible that sleep began for one reason and was later put to other uses'),
  ]),

  p('r5-11', 5, 'History and Hindsight', '歴史と後知恵', `
Once we know how events turned out, it becomes difficult to imagine that they could have turned out otherwise. Historians call this tendency hindsight bias. Looking back on a war, a financial crisis, or the fall of a government, we see the warning signs clearly and wonder how anyone could have missed them. But the people living through those events did not have the advantage of knowing which of the countless signals around them would prove significant.

This bias distorts our understanding of the past in two ways. First, it makes history appear more inevitable than it was, obscuring the role of chance, contingency, and individual decisions. Second, it encourages unfair judgments of past actors, who are blamed for failing to foresee outcomes that were genuinely uncertain at the time.

One remedy, some historians suggest, is to try to recover the perspective of the people being studied: to read the newspapers, letters, and diaries of the period without skipping ahead to the ending. Such sources often reveal that what seems obvious to us was a matter of fierce debate, and that many confident predictions turned out to be wrong.

The point is not that past mistakes should be excused. Some failures really were the result of negligence or poor judgment. But to distinguish such failures from bad luck, we must ask not "What should they have known?" but "What could they reasonably have known, given the information available to them?"`, [
    q('r5-11-1', 'Which of the following is described as an effect of hindsight bias?', [
      'It makes past events seem more unavoidable than they really were', 'It makes people forget important historical events', 'It encourages historians to read old newspapers', 'It causes people to overestimate the role of chance'],
      '「歴史を実際より必然的に見せ、偶然や個人の決断の役割を見えにくくする」。④は逆。',
      'it makes history appear more inevitable than it was'),
    q('r5-11-2', 'What do sources such as letters and diaries often reveal?', [
      'Matters that seem obvious now were strongly disputed at the time', 'People in the past could predict the future accurately', 'Historians have misunderstood most past events', 'Past leaders were usually careless'],
      '「今の私たちには明らかに見えることが、激しい議論の的だった」。',
      'what seems obvious to us was a matter of fierce debate'),
    q('r5-11-3', 'What question does the author recommend asking when judging past decisions?', [
      'What people could reasonably have known with the information they had', 'What people should have known about the outcome', 'Whether people were lucky or unlucky', 'Whether historians agree about the event'],
      '「何を知るべきだったか」ではなく「得られた情報から何を合理的に知りえたか」を問う。',
      'What could they reasonably have known, given the information available to them?'),
  ]),

  p('r5-12', 5, 'The Limits of Prediction', '予測の限界', `
Weather forecasts have improved dramatically over the past half century. A five-day forecast today is about as accurate as a one-day forecast was in the 1980s. Yet there appears to be a limit beyond which no amount of computing power will allow us to see. Detailed forecasts more than about two weeks ahead are, and are likely to remain, little better than guesses.

The reason was discovered almost by accident in the 1960s by the meteorologist Edward Lorenz. Running a simple computer model of the atmosphere, he restarted a calculation using numbers rounded to three decimal places instead of six. He expected the result to be almost identical. Instead, after a short period, the two runs diverged completely. Tiny differences in the starting conditions, far smaller than any instrument could measure, had grown until they dominated the outcome.

Systems that behave in this way are called chaotic. They are not random; they follow precise rules. But because their future depends so sensitively on their present state, and because the present can never be measured perfectly, long-range prediction of their exact behavior is impossible in principle, not merely in practice.

This does not mean that nothing can be said about the future of such systems. Although we cannot predict whether it will rain on a particular day next month, we can say with confidence that summer will be warmer than winter. Chaos limits our knowledge of particular events, but it leaves room for knowledge of averages and patterns.`, [
    q('r5-12-1', 'What did Lorenz expect when he restarted his calculation with rounded numbers?', [
      'That the results would be nearly the same as before', 'That the computer would stop working', 'That the two runs would diverge completely', 'That the rounded numbers would produce a better forecast'],
      '「結果はほぼ同じになると予想した」。実際には完全に食い違った。',
      'He expected the result to be almost identical.'),
    q('r5-12-2', 'According to the passage, why is long-range prediction of chaotic systems impossible in principle?', [
      'Their future depends greatly on present conditions that can never be measured perfectly', 'They do not follow any rules', 'Computers are not yet powerful enough', 'Meteorologists use inaccurate instruments'],
      '「未来が現在の状態にきわめて敏感に左右され、現在は決して完全には測れない」。ランダムではなく規則に従う点に注意。',
      'because their future depends so sensitively on their present state, and because the present can never be measured perfectly'),
    q('r5-12-3', 'What is the main point of the final paragraph?', [
      'Even in chaotic systems, general patterns can be known with confidence', 'Chaos makes all knowledge of the future impossible', 'Summer and winter are becoming harder to predict', 'Rain can be predicted a month ahead'],
      '「カオスは個々の出来事の知識を制限するが、平均やパターンの知識の余地は残す」。',
      'Chaos limits our knowledge of particular events, but it leaves room for knowledge of averages and patterns.'),
  ]),
];
