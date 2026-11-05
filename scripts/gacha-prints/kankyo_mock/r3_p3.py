# -*- coding: utf-8 -*-
# 第3回 Part 3（会話の空所に4つの文から選ぶ。人物・場面は架空）
P3 = {
    'points': 12,
    'type': 'choose',
    'lead': '次の 1〜4 の会話の空所に入れるのにもっとも適切なものを，下の ①〜④ からそれぞれ一つ選び，番号を書きなさい。ただし，同じものを2回以上使ってはいけない。',
    'options': [
        'It’s on the tip of my tongue.',
        'I’m all ears.',
        'Let’s call it a day.',
        'That rings a bell.',
    ],
    'convs': [
        [('A', 'We’ve been painting the fence since eight this morning.'),
         ('B', 'And it’s getting dark now. I’m really tired.'),
         ('A', 'Me too. {blank} We can finish the rest tomorrow.')],
        [('A', 'What’s the name of that actor in the film we saw last week?'),
         ('B', 'Oh, I know it! {blank} Just give me a second.')],
        [('A', 'I have some exciting news about our school trip.'),
         ('B', 'Really? Tell me! {blank}')],
        [('A', 'Have you heard of a café called Blue Lantern?'),
         ('B', 'Hmm, {blank} I think my sister went there last month.')],
    ],
    'answers': [2, 0, 1, 3],
    'expl': [
        '朝から作業して暗くなり，「残りは明日やろう」と続く。「今日はここまでにしよう」の ③。',
        '俳優の名前を「知っている！ちょっと待って」と思い出そうとしている。「（言葉が）のどまで出かかっている」の ①。',
        '「わくわくする知らせがある」と言われて「教えて！」と答える場面。「しっかり聞くよ（耳を傾けている）」の ②。',
        '店の名前を聞かれ，「姉が先月行ったと思う」と続く。「聞き覚えがある（何か思い出させる）」の ④。',
    ],
    'ja': [
        '①のどまで出かかっている。②しっかり聞くよ。③今日はここまでにしよう。④聞き覚えがある。',
        '1　A：朝8時からずっと塀を塗っているね。　B：もう暗くなってきたよ。本当に疲れた。　A：私も。今日はここまでにしよう。残りは明日終わらせればいいよ。',
        '2　A：先週見た映画のあの俳優の名前は何だっけ？　B：ああ，知ってる！のどまで出かかってるんだ。ちょっと待って。',
        '3　A：修学旅行についてわくわくする知らせがあるんだ。　B：本当？教えて！しっかり聞くよ。',
        '4　A：ブルー・ランタンっていうカフェを聞いたことある？　B：うーん，聞き覚えがあるな。姉が先月行ったと思う。',
    ],
}
