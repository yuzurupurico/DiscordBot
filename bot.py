import discord
import random  # おみくじで使用

client = discord.Client()  # 接続に使用するオブジェクト

fincount = 0  # 凸終了人数カウント変数を初期値0で定義する(ここで宣言するとグローバルになって各処理から参照できます)

# 30人分のユーザーの名前リストとIDリスト（discord上で右クリック取得）を作成する
membername = [  # 下のＩＤと同じ並びで設定する。名前をidから動的に取得できれば名前リストは不要です。
"トモ",
"マツリ",
"オウカ",
"ゆずる",
"クウカ",
"ノウェム",
"リマ",
"しずる",
"ばずる",
"じーた",
"からす",
"きつね",
"てんぷら",
"べーこん",
"ご空",
"ちゃおず",
"くりりん",
"桜木",
"やべ",
"かんがえるのが",
"面倒",
"になって",
"きました",
"とにかく",
"でばっぐ",
"ように",
"うめれば",
"おーけー",
"ですすｓ",
"最後の戦士",
]

memberid = [    # メンバーのdiscordユーザーidリスト。上の名前リストと順番を合わせる
0,                  # "トモ"のＩＤ
1,                  # "マツリ",のＩＤ
2,                  # "オウカ",のＩＤ
572012584241201153, # "ゆずる",のＩＤ
4,                  # "クウカ",のＩＤ
5,                  # "ノウェム",のＩＤ
6,                  # "リマ",のＩＤ
7,                  # "しずる",のＩＤ
8,                  # "ばずる",のＩＤ
9,                  # "じーた",のＩＤ
10,                 # "からす",のＩＤ
11,                 # "きつね",のＩＤ
12,                 # "てんぷら",のＩＤ
13,                 # "べーこん",のＩＤ
14,                 # "ご空",のＩＤ
15,                 # "ちゃおず",のＩＤ
16,                 # "くりりん",のＩＤ
17,                 # "桜木",のＩＤ
18,                 # "やべ",のＩＤ
19,                 # "かんがえるのが",のＩＤ
20,                 # "面倒",のＩＤ
21,                 # "になって",のＩＤ
22,                 # "きました",のＩＤ
23,                 # "とにかく",のＩＤ
24,                 # "でばっぐ",のＩＤ
25,                 # "ように",のＩＤ
26,                 # "うめれば",のＩＤ
27,                 # "おーけー",のＩＤ
28,                 # "ですすｓ",のＩＤ
29 ]                # "最後の戦士",のＩＤ


# 30人分の凸数リストを初期値=0で作成する
totsucount = [0] * 30

@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')

@client.event
async def on_message(message):
    global fincount     # グローバルで定義した変数を使用する宣言
    global cname        # グローバルで定義した変数を使用する宣言
    global totsucount   # グローバルで定義した変数を使用する宣言
    """メッセージを処理"""
    if message.author.bot:  # ボットのメッセージをハネる
        return

    if message.content == "!眠たい":
        # チャンネルへメッセージを送信
        await message.channel.send(f"{message.author.mention}さん 寝ましょう")  # f文字列（フォーマット済み文字列リテラル）

    elif message.content == "凸開始":
        # 開始報告した人を名前リストから探し、凸数を更新する
        for i in range(30):                             # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                await message.channel.send(f"{message.author.mention}さん " + str(totsucount[i]+1) + "凸開始です。" )

    elif message.content == "凸終了":
        # 終了報告した人を名前リストから探し、凸数を更新する
        for i in range(30):                             # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                totsucount[i] += 1                      # 凸回数をカウントアップする
                if totsucount[i] == 3:                  # 3なら終わりメッセージも追加
                    fincount += 1                       # fincount（凸終了人数）をカウントアップ（+1）する
                    await message.channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。お疲れ様です！ 凸終わり"+ str(fincount)+ "人目" )
                elif totsucount[i] > 3:                 # 3より大きければエラーメッセージ表示
                    await message.channel.send(f"{message.author.mention}さん 凸報告多すぎですよ" )
                else:                                   # 3より小さいとき
                    await message.channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。" )

    elif message.content == "!凸残り":  # 凸残ってる人だけ表示する場合
        tcount = 0
        for i in range(30):                             # i=0からi=29まで30回繰り返す処理を実行する
            if totsucount[i] < 3:                       # 凸回数3回以下なら残り凸回数を表示する
                await message.channel.send(membername[i] + "さん 残り" + str(3-totsucount[i]) + "凸です。" )
                tcount += 1                             #残り人数をカウントアップする
        await message.channel.send("以上 残り" + str(tcount) + "人です。" )

    elif message.content == "!凸状況":  # 全員の凸状況を把握したいとき
        for i in range(30):                             # i=0からi=29まで30回繰り返す処理を実行する
            await message.channel.send(membername[i] + "さんの現在までの凸完了回数＝" + str(totsucount[i]) + "回です。" )

    elif message.content == "!投票":
        # リアクションアイコンを付けたい
        q = await message.channel.send("あなたは右利きですか？")
        [await q.add_reaction(i) for i in ('⭕', '❌')]  # for文の内包表記

    elif message.content == "!おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '吉', '凶', '大凶')), inline=False)
        await message.channel.send(embed=embed)

    elif message.content == "!ダイレクトメッセージ":
        # ダイレクトメッセージ送信
        dm = await message.author.create_dm()
        await dm.send(f"{message.author.mention}さんにダイレクトメッセージ")

    elif message.content == "!時間":
        # ダイレクトメッセージ送信
        now = datetime.now().strftime('%H:%M')  # 現在の時刻を取得する
        await message.channel.send(now)  # f文字列（フォーマット済み文字列リテラル）

# botの接続と起動
# （botアカウントのアクセストークンを入れてください）
client.run("ここにトークンを打ち込む")

# py C:\Users\owner\Desktop\BOT\bot.py
