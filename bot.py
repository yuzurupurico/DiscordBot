# インストールした discord.py を読み込む
import discord
import random   # おみくじで使用
import re       # 正規表現に必要（残り体力に使用）
from discord.ext import tasks
from datetime import datetime 
from discord.ext import commands
# スプレッドシート連携用
#import gspread
#import json
#from oauth2client.service_account import ServiceAccountCredentials

fincount    = 0         # 凸終了人数カウント変数を初期値0で定義する(ここで宣言するとグローバルになって各処理から参照できます)
boss        = ["ゴブリングレート","ライライ","シードレイク","ネプテリオン","カルキノス"]
bossindex   = 0

# 自分のBotのアクセストークンに置き換えてください
TOKEN       = 
CHANNEL_R   = 594126353188782111    # 予約チャンネルID
CHANNEL_T   = 594126553403752459    # 凸報告チャンネルID
CHANNEL_S   = 595205005712162816    # 集計チャンネルID
CHANNEL_SYN = 595538019227009035    # 同時ナビ用チャンネル
CHANNEL_RSV = 595538162139267083    # 予約用チャンネル
CHANNEL_FIN = 595538223292219402    # 終わり報告チャンネル
CHANNEL_S   = 595205005712162816    # 集計チャンネルID
roles_mem   = 594126169427804163    # 役職くらめんID

# user情報リスト
memberid    = []            # クラメンのＩＤを取得するリスト
membername  = []            # クラメンの名前を取得するリスト
usercount   = 0             # クラメンの人数
totsucount  = []            # 凸数リスト
hp          = 0             # ボスの残り体力

# 同時凸ナビ用
syn1name    = ""
syn2name    = ""
othername   = ""
synstatus   = 0

#予約システム用
yoyaku1st = []
yoyaku2nd = []
yoyaku3rd = []
yoyaku4th = []
yoyaku5th = []

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
    global CHANNEL_SYN
    global roles_mem
    global memberid
    global membername
    global usercount
    global syn1name
    global syn2name
    global synstatus
    global CHANNEL_SYN
    global othername
    global hp
    global totsucount
    global bossindex
    global yoyaku1st
    global yoyaku2nd
    global yoyaku3rd
    global yoyaku4th
    global yoyaku5th

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

    elif message.content == "凸":
        # 開始報告した人を名前リストから探し、凸数を更新する
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                channel = client.get_channel(CHANNEL_T)
                await channel.send(f"{message.author.mention}さん " + str(totsucount[i]+1) + "凸開始です。" )

    elif message.content == "凸LA":
        # 開始報告した人を名前リストから探し、凸数を更新する
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                channel = client.get_channel(CHANNEL_T)
                await channel.send(f"{message.author.mention}さん " + str(totsucount[i]+1) + "凸LA開始です。" )
                await message.channel.send( "『持ち越しの持ち越し』は出来ません。ご注意ください。" ) 

    elif message.content == "!凸残り":  # 凸残ってる人だけ表示する場合
        tmessage = ""
        tcount = 0
        tcount2 = 0
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if totsucount[i] < 3:                       # 凸回数3回以下なら残り凸回数を表示する
                tmessage = tmessage + membername[i] + "さん 残り" + str(3-totsucount[i]) + "凸です。\n"
                tcount += 1                             #残り人数をカウントアップする
                tcount2 += 3-totsucount[i]
        channel = client.get_channel(CHANNEL_S)
        await channel.send( f'{tmessage}以上 残り{str(tcount)}人、残り凸数合計は{str(tcount2)}です。' )

    elif message.content == "!状況ALL":  # 全員の凸状況を把握したいとき
        tempmessage = ""
        tcount = 0
        channel = client.get_channel(CHANNEL_S)
        await channel.send( f'今のボスは{boss[bossindex]}で残りHPは{str(hp)}です。' )
        for i in range(usercount):      # i=0からi=29まで30回繰り返す処理を実行する
            tempmessage = tempmessage + membername[i] + "さんの現在までの凸完了回数 = " + str(totsucount[i]) + "回です。" + "\n"
            tcount += (3-totsucount[i])
        await channel.send( tempmessage )
        await channel.send( f'全員の残り凸数合計は{str(tcount)}です。' )

    elif message.content == "!状況":
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                tmessage = f'今のボスは{boss[bossindex]}で残りHPは{str(hp)}、{membername[i]}さんの残り凸数は{str(3-totsucount[i])}です。'
                await message.channel.send(tmessage)   

    elif message.content == "/タスキル":
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんがタスキルしました")         
        
    elif message.content == "持ち越し":

        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"{message.author.mention}さんの持ち越しです")   

    ################ 同時凸ナビ用処理 ################
    elif message.content == "!同時":
        channel = client.get_channel(CHANNEL_SYN)
        if synstatus == 0:      # 同時でないとき
            syn1name = message.author.mention
            await channel.send(f"同時凸ナビを開始します。\n {syn1name}さんは待機してください\n同時いく方もう一名は「!同時」を入力してください" )
            synstatus = 1
        elif synstatus == 1:    # 一人だけ同時宣言のとき
            syn2name = message.author.mention
            await channel.send(f"{syn1name}さんと{syn2name}さんは開始5秒で止めてコマンド「/in」を打ってください。\nそれでは戦闘開始してください。" )
            synstatus = 2
        else:
            await channel.send(f"{message.author.mention}さんのコマンドが想定外なので何もしません。" )

    elif message.content == "/in":
        channel = client.get_channel(CHANNEL_SYN)
        if synstatus == 2:
            if message.author.mention == syn1name:
                othername = syn2name
                await channel.send(f"{message.author.mention}さんはそのまま{othername}さんをお待ちください。" )
                synstatus = 3
            elif message.author.mention == syn2name:
                othername = syn1name
                await channel.send(f"{message.author.mention}さんはそのまま{othername}さんをお待ちください。" )
                synstatus = 3
            else:
                await channel.send(f"{message.author.mention}さんは同時対象者ではありません。何もしません。" )
        elif synstatus == 3:
            if othername == message.author.mention:
                await channel.send(f"対象二人の戦闘開始が確認できました。\n{syn1name}さんと{syn2name}さんは戦闘終了5sec前まで進めてコマンド「/last5」を打ってください。\nそれでは戦闘再開してください。" )
                synstatus = 4
            else:
                await channel.send(f"{message.author.mention}さんは同時対象者ではないので何もしません。" )
        else:
            await channel.send(f"{message.author.mention}さんのコマンドが想定外なので何もしません。" )

    elif message.content == "/last5":
        channel = client.get_channel(CHANNEL_SYN)
        if synstatus == 4:
            if message.author.mention == syn1name:
                othername = syn2name
                await channel.send(f"{message.author.mention}さんはそのまま{othername}さんをお待ちください。" )
                synstatus = 5
            elif message.author.mention == syn2name:
                othername = syn1name
                await channel.send(f"{message.author.mention}さんはそのまま{othername}さんをお待ちください。" )
                synstatus = 5
            else:
                await channel.send(f"{message.author.mention}さんは同時対象者ではないので何もしません。" )
        elif synstatus == 5:
            await channel.send(f"{syn1name}さんと{syn2name}さんはどちらが先に通すか決めてください。\n先に通す人は戦闘終了後にコマンド「凸終了@XXX」を忘れず入力してください。\nそれでは先に通す人は戦闘開始してください。" )
            synstatus = 6
        else:
            await channel.send(f"{message.author.mention}さんのコマンドが想定外なので何もしません。" )

    elif message.content == "!同時キャンセル":
        channel = client.get_channel(CHANNEL_SYN)
        await channel.send(f"キャンセルを受け付けました。同時凸ナビを終了します。" )
        syn1name = ""
        syn2name = ""
        synstatus = 0
        othername = ""

    ############## ボスに行きたい人を募集するとき ################
    elif message.content == "予約1st":
        channel = client.get_channel(CHANNEL_RSV)
        await channel.send(f"{message.author.mention}さん {boss[0]}の予約を受け付けました。" )
        yoyaku1st.append( message.author.id )

    elif message.content == "予約2nd":
        channel = client.get_channel(CHANNEL_RSV)
        await channel.send(f"{message.author.mention}さん {boss[1]}の予約を受け付けました。" )
        yoyaku2nd.append( message.author.id )

    elif message.content == "予約3rd":
        channel = client.get_channel(CHANNEL_RSV)
        await channel.send(f"{message.author.mention}さん {boss[2]}の予約を受け付けました。" )
        yoyaku3rd.append( message.author.id )

    elif message.content == "予約4th":
        channel = client.get_channel(CHANNEL_RSV)
        await channel.send(f"{message.author.mention}さん {boss[3]}の予約を受け付けました。" )
        yoyaku4th.append( message.author.id )

    elif message.content == "予約5th":
        channel = client.get_channel(CHANNEL_RSV)
        await channel.send(f"{message.author.mention}さん {boss[4]}の予約を受け付けました。" )
        yoyaku5th.append( message.author.id )

    elif message.content == "/1st":
        bossindex = 0
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        if len(yoyaku1st) == 0:
            await channel.send( '予約はありません。' )
        else:
            tmessage = "予約しているのは"
            for tmember in yoyaku1st:
                tuser = client.get_user(tmember)
                tmessage += f'{tuser.mention}さん '
            tmessage += f'の{str(len(yoyaku1st))}人です。\n今から10分は予約者が優先的に順番を決められます。10分経過後は優先権は消失します。\n{boss[bossindex]}の予約は一度クリアします。'
            yoyaku1st = []
            await channel.send( tmessage )

    elif message.content == "/2nd":
        bossindex = 1
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        if len(yoyaku2nd) == 0:
            await channel.send( '予約はありません。' )
        else:
            tmessage = "予約しているのは"
            for tmember in yoyaku2nd:
                tuser = client.get_user(tmember)
                tmessage += f'{tuser.mention}さん '
            tmessage += f'の{str(len(yoyaku2nd))}人です。\n今から10分は予約者が優先的に順番を決められます。10分経過後は優先権は消失します。\n{boss[bossindex]}の予約は一度クリアします。'
            yoyaku2nd = []
            await channel.send( tmessage )

    elif message.content == "/3rd":
        bossindex = 2
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        if len(yoyaku3rd) == 0:
            await channel.send( '予約はありません。' )
        else:
            tmessage = "予約しているのは"
            for tmember in yoyaku3rd:
                tuser = client.get_user(tmember)
                tmessage += f'{tuser.mention}さん '
            tmessage += f'の{str(len(yoyaku3rd))}人です。\n今から10分は予約者が優先的に順番を決められます。10分経過後は優先権は消失します。\n{boss[bossindex]}の予約は一度クリアします。'
            yoyaku3rd = []
            await channel.send( tmessage )
        
    elif message.content == "/4th":
        bossindex = 3
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        if len(yoyaku4th) == 0:
            await channel.send( '予約はありません。' )
        else:
            tmessage = "予約しているのは"
            for tmember in yoyaku4th:
                tuser = client.get_user(tmember)
                tmessage += f'{tuser.mention}さん '
            tmessage += f'の{str(len(yoyaku4th))}人です。\n今から10分は予約者が優先的に順番を決められます。10分経過後は優先権は消失します。\n{boss[bossindex]}の予約は一度クリアします。'
            yoyaku4th = []
            await channel.send( tmessage )

    elif message.content == "/5th":
        bossindex = 4
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}>" + boss[bossindex])
        if len(yoyaku5th) == 0:
            await channel.send( '予約はありません。' )
        else:
            tmessage = "予約しているのは"
            for tmember in yoyaku5th:
                tuser = client.get_user(tmember)
                tmessage += f'{tuser.mention}さん '
            tmessage += f'の{str(len(yoyaku5th))}人です。\n今から10分は予約者が優先的に順番を決められます。10分経過後は優先権は消失します。\n{boss[bossindex]}の予約は一度クリアします。'
            yoyaku5th = []
            await channel.send( tmessage )
        
    elif message.content == "!予約確認":
        lindex = bossindex
        tmessage = ""
        for i in range(5):
            if lindex >= 4:
                lindex = 0
            else:
                lindex += 1
            tmessage += f'{boss[lindex]}の予約は'
            if lindex == 0:
                if len(yoyaku1st) == 0:
                    tmessage += "ありません。\n"
                else:
                    for tmember in yoyaku1st:
                        tuser = client.get_user(tmember)
                        tmessage += f'{tuser.mention}さん '
                    tmessage += f'の{str(len(yoyaku1st))}人です。\n'
            elif lindex == 1:
                if len(yoyaku2nd) == 0:
                    tmessage += "ありません。\n"
                else:
                    for tmember in yoyaku2nd:
                        tuser = client.get_user(tmember)
                        tmessage += f'{tuser.mention}さん '
                    tmessage += f'の{str(len(yoyaku2nd))}人です。\n'
            elif lindex == 2:
                if len(yoyaku3rd) == 0:
                    tmessage += "ありません。\n"
                else:
                    for tmember in yoyaku3rd:
                        tuser = client.get_user(tmember)
                        tmessage += f'{tuser.mention}さん '
                    tmessage += f'の{str(len(yoyaku3rd))}人です。\n'
            elif lindex == 3:
                if len(yoyaku4th) == 0:
                    tmessage += "ありません。\n"
                else:
                    for tmember in yoyaku4th:
                        tuser = client.get_user(tmember)
                        tmessage += f'{tuser.mention}さん '
                    tmessage += f'の{str(len(yoyaku4th))}人です。\n'
            elif lindex == 4:
                if len(yoyaku5th) == 0:
                    tmessage += "ありません。\n"
                else:
                    for tmember in yoyaku5th:
                        tuser = client.get_user(tmember)
                        tmessage += f'{tuser.mention}さん '
                    tmessage += f'の{str(len(yoyaku5th))}人です。\n'
        await message.channel.send( tmessage )

    elif message.content == "/助けて":
        channel = client.get_channel(CHANNEL_T)
        await channel.send(f"<@&{roles_mem}> 助けてマリオ！")    

    matchOB = re.match( '凸終了(@[0-9]+){1}$', message.content )       # メッセージが「凸終了@XXX(数字)」かどうか？を正規表現でチェックする
    if matchOB:
        # 終了報告した人を名前リストから探し、凸数を更新する
        channel = client.get_channel(CHANNEL_T)
        for i in range(usercount):                      # i=0からi=29まで30回繰り返す処理を実行する
            if memberid[i] == message.author.id:        # 報告者とidが一致したら
                totsucount[i] += 1                      # 凸回数をカウントアップする
                if totsucount[i] == 3:                  # 3なら終わりメッセージも追加
                    fincount += 1                       # fincount（凸終了人数）をカウントアップ（+1）する
                    channel = client.get_channel(CHANNEL_FIN)
                    await channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。お疲れ様です！ 凸終わり"+ str(fincount)+ "人目" )
                    channel = client.get_channel(CHANNEL_T)
                    await channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。" )
                elif totsucount[i] > 3:                 # 3より大きければエラーメッセージ表示
                    await channel.send(f"{message.author.mention}さん 凸報告多すぎですよ" )
                else:                                   # 3より小さいとき
                    await channel.send(f"{message.author.mention}さん " + str(totsucount[i]) + "凸終了です。" )
                # 同時凸ナビの〆処理
                if synstatus == 6:
                    channel = client.get_channel(CHANNEL_SYN)
                    if message.author.mention == syn1name:
                        await channel.send(f"{message.author.mention}さんの凸完了したので{syn2name}さんは戦闘開始してください。" )
                    elif message.author.mention == syn2name:
                        othername = syn1name
                        await channel.send(f"{message.author.mention}さんの凸完了したので{syn1name}さんは戦闘開始してください。" )
                    else:
                        await channel.send("同時凸対象外の凸完了宣言がありました。" )
                    await channel.send("これで同時凸ナビを終了します。お疲れ様でした。" )
                    syn1name = ""
                    syn2name = ""
                    synstatus = 0
                    othername = ""
                    channel = client.get_channel(CHANNEL_T)

        # 残り体力を取得して表示する。
        searchOB = re.search( '[0-9]+', message.content )
        hp = int( searchOB.group() )
        await channel.send( f"{boss[bossindex]}の残りのHPは{str(hp)}です。" )

    elif message.content == "凸終了":
        await message.channel.send('凸終了のあとに@を付けてボスの残り体力(万単位)を加えてください（例：凸終了@216）')

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
