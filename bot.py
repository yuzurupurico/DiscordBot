# インストールした discord.py を読み込む
import discord
import random  # おみくじで使用
from discord.ext import tasks
from datetime import datetime 
from discord.ext import commands

fincount    = 0         # 凸終了人数カウント変数を初期値0で定義する(ここで宣言するとグローバルになって各処理から参照できます)
boss        = ["ゴブリングレート","ライライ","シードレイク","ネプテリオン","カルキノス"]
bossindex   = 0

# 自分のBotのアクセストークンに置き換えてください
TOKEN       = 
CHANNEL_R   =     # 予約チャンネルID
CHANNEL_T   =     # 凸報告チャンネルID
CHANNEL_S   =     # 集計チャンネルID
roles_mem   =     # 役職くらめんのID

# user情報リスト
memberid    = []            # クラメンのＩＤを取得するリスト
membername  = []            # クラメンの名前を取得するリスト
usercount   = 0             # クラメンの人数
totsucount  = []            # 凸数リスト

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global fincount
    global totsucoun
    global boss
    global TOKEN
    global CHANNEL_R
    global CHANNEL_T
    global roles_mem
    global memberid
    global membername
    global usercount

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('に”ゃ"あ”あ”あ”あ”あ”ん”！')
    
    # クランメンバー（役職：くらめん）の情報を自動取得して更新する ※メンバーに変化あったら一回実行が必要
    if message.content == '/member':
        usercount   = 0
        memberid    = []            # クラメンのＩＤリストを初期化する
        membername  = []            # クラメンの名前リストを初期化する
        totsucount  = []            # 凸数リストを初期化する
        for member in message.guild.members:    # user情報を全員チェックする
            print( member.name )
            for role in member.roles:           # userのロールをチェックする
                if role.id == roles_mem:        # ロールが「くらめん」なら
                    membername.append(member.name)
                    memberid.append(member.id)
                    totsucount.append(0)
                    usercount += 1              # user数をカウントアップする
        print(membername)
        print(memberid)
        print(totsucount)
        print(usercount)

    
    if message.content == '/obuse':
        await message.channel.send('0:40 クスリ')
    
    if message.content == '/inu':
        await message.channel.send('お゛お゛お゛お゛お゛お゛ん゛!')
            
    if message.content == '/yaaman':
        await message.channel.send('ダメです')

    if message.content == "/ダメです":

        await message.channel.send(f"（ﾌﾞﾘﾌﾞﾘﾌﾞﾘﾌﾞﾘｭﾘｭﾘｭﾘｭﾘｭﾘｭ！！！！！！ﾌﾞﾂﾁﾁﾌﾞﾌﾞﾌﾞﾁﾁﾁﾁﾌﾞﾘﾘｲﾘﾌﾞﾌﾞﾌﾞﾌﾞｩｩｩｩｯｯｯ")
                        
    elif message.content == "!おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '中吉','吉', '小吉', '凶', '大凶')), inline=False)
        await message.channel.send(embed=embed) 

    elif message.content == "!hori":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="hori", description=f"ほりくんの迷言集",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[hori] ", value=random.choice(('ぬそぉ...', 'ちんちんケルベロス', 'ムラムラ','ケルベロス掘りします')), inline=False)
        await message.channel.send(embed=embed) 

        
    elif message.content == "!brain":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="brain", description=f"あなたは何ぶれ？",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[brain] ", value=random.choice(('がばいん','ぶれぶれいん','上ぶれいん', '下ぶれいん', '神ぶれいん', '凶ぶれいん')), inline=False)
        await message.channel.send(embed=embed) 

    elif message.content == "!toroy":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="toroy", description=f"がばいさんかとろいさんか",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[toroy] ", value=random.choice(('がばいです','呼ばれて飛び出てとろいさん','寝落ちしたわ', '寝言行くぜ！')), inline=False)
        await message.channel.send(embed=embed) 

    elif message.content == "凸開始":
        # 開始報告した人を名前リストから探し、凸数を更新する
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                channel = client.get_channel(CHANNEL_T)
                await channel.send(f"{message.author.mention}さん " + str(totsucount[i]+1) + "凸開始です。" )

    elif message.content == "凸終了":
        # 終了報告した人を名前リストから探し、凸数を更新する
        channel = client.get_channel(CHANNEL_T)
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                totsucount[i] += 1                      # 凸回数をカウントアップする
                if totsucount[i] == 3:                  # 3なら終わりメッセージも追加
                    fincount += 1                       # fincount（凸終了人数）をカウントアップ（+1）する
                    await channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。お疲れ様です！ 凸終わり"+ str(fincount)+ "人目" )
                elif totsucount[i] > 3:                 # 3より大きければエラーメッセージ表示
                    await channel.send(f"{message.author.mention}さん 凸報告多すぎですよ" )
                else:                                   # 3より小さいとき
                    await channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。" )

    elif message.content == "!凸残り":  # 凸残ってる人だけ表示する場合
        tmessage = ""
        tcount = 0
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if totsucount[i] < 3:                       # 凸回数3回以下なら残り凸回数を表示する
                tmessage = tmessage + membername[i] + "さん 残り" + str(3-totsucount[i]) + "凸です。\n"
                tcount += 1                             #残り人数をカウントアップする
        channel = client.get_channel(CHANNEL_S)
        await channel.send(tmessage + "以上 残り" + str(tcount) + "人です。" )

    elif message.content == "!凸状況":  # 全員の凸状況を把握したいとき
        tempmessage = ""
        for i in range(usercount):      # i=0からi=29まで30回繰り返す処理を実行する
            tempmessage = tempmessage + membername[i] + "さんの現在までの凸完了回数 = " + str(totsucount[i]) + "回です。" + "\n"
        channel = client.get_channel(CHANNEL_S)
        await channel.send( tempmessage )

    if message.content == "1凸":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの1凸目です") 

    if message.content == "2凸":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの2凸目です")    

    if message.content == "3凸":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの3凸目です")

    if message.content == "/タスキル":
        
        channel = client.get_channel(593482786581643264)
        await channel.send(f"{message.author.mention}さんがタスキルしました")         
        
    if message.content == "持ち越し":

        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの持ち越しです")   

    if message.content == "1凸LA":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの1凸目のLAです")

    if message.content == "2凸LA":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの2凸目のLAです")        

    if message.content == "3凸LA":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの3凸目のLAです")   

    if message.content == "/1st":
        bossindex = 0
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        
    if message.content == "/2nd":
        bossindex = 1
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])

    if message.content == "/3rd":
        bossindex = 2
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        
    if message.content == "/4th":
        bossindex = 3
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        
    if message.content == "/5th":
        bossindex = 4
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        
    if message.content == "/助けて":
        
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}> 助けてマリオ！")    
        

# ボスに行きたい人を募集するとき

# 50秒に一回ループ
@tasks.loop(seconds=50)
async def loop():
    global fincount
    global totsucount

    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '19:00':
        channel = client.get_channel(560495611280097295)
        await channel.send('プリコネの更新1時間前だよ～')  

    elif now == '20:00':
        channel = client.get_channel(560495611280097295)
        await channel.send('プリコネの更新時間だよ～')  
        channel = client.get_channel(584441360506028213)
        await channel.send('今日のクラバトの集計です')  
        fincount = 0
        totsucount = [0] * usercount

#ループ処理実行
loop.start()


# Botの起動とDiscordサーバーへの接続
client.run( TOKEN )
