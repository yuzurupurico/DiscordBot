import discord
import random  # おみくじで使用
from discord.ext import tasks  # 定刻イベントに使用する
from datetime import datetime  # 定刻イベントに使用する

client = discord.Client()  # 接続に使用するオブジェクト

fincount = 0  # 凸終了人数カウント変数をグローバルスコープで初期値0で定義する

@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    channel = client.get_channel(594126553403752459)
    await channel.send('おはよう！')

@client.event
async def on_message(message):
    global fincount # この中で使用するfincountがグローバルだと明示する
    """メッセージを処理"""
    if message.author.bot:  # ボットのメッセージをハネる
        return

    if message.content == "!眠たい":
        # チャンネルへメッセージを送信
        await message.channel.send(f"{message.author.mention}さん 寝ましょう")  # f文字列（フォーマット済み文字列リテラル）

    elif message.content == "!3凸終了":
        fincount += 1
        await message.channel.send(f"{message.author.mention}さん 3凸終了です"+ str(fincount)+ "人目" )  # f文字列（フォーマット済み文字列リテラル）
        if fincount > 30:
            await message.channel.send( "...誰か重複して終了報告してませんか？" )

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

# 30秒に一回ループ
@tasks.loop(seconds=40)
async def timeloopbot():
    now = datetime.now().strftime('%H:%M')  # 現在の時刻を取得する
    channel = client.get_channel(594126553403752459)
    print( channel )
    await message.channel.send(now)
    await message.channel.send("ループからのメッセージです")
    if now == '16:05':
        await message.channel.send("18:00です。スタミナログボの受け取りお忘れなく")

#ループ処理実行
timeloopbot.start()

# botの接続と起動
# （botアカウントのアクセストークンを入れてください）
client.run("NTk0MTI0NzMyMzc1MzY3Njgy.XRX4CA.XdQRnowelwYk1QPL5d0PhD3y7u0")

# py C:\Users\owner\Desktop\BOT\bot.py