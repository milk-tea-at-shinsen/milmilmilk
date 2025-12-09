import discord
from discord.ext import commands
import asyncio
import datetime
import os

# Botの準備
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot起動確認
@bot.event
async def on_ready():
    print(f"起動しました！: {bot.user}")
    print(f"ループ開始： {datetime.datetime.now()}")
    bot.loop.create_task(reminder_loop())

# 空の辞書を定義
reminders = {}

# !remind コマンド
@bot.command()
async def remind(ctx, date_str: str, time_str: str, *message):
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    msg = " ".join(message)

    if dt not in reminders:
        reminders[dt] = []
        reminders[dt].append((ctx.channel.id, msg))

    await ctx.send(f"{dt} にリマインダーをセット！:saluting_face:")

# 通知用ループ
async def reminder_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.datetime.now()
        next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
        wait = (next_minute - now).total_seconds()
        await asyncio.sleep(wait)
        print (f"毎分ゼロ秒に辞書と照合：{datetime.datetime.now()}")

        if next_minute in reminders:
            for channel_id, msg in reminders[next_minute]:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"{msg}")
                    print (f"チャンネルにメッセージを送信：{datetime.datetime.now()}")
                else:
                    print(f"チャンネル取得失敗：{channel_id}")
            del reminders[next_minute]

# スラッシュコマンドのテスト
@bot.slash_command(name="ping", description="テスト用コマンド"):
    async def ping(ctx):
        await ctx.respond("pong!")

# Botを起動
bot.run(os.getenv("DISCORD_TOKEN"))