import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import privacy_policy

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

# 투표 결과 저장 딕셔너리
vote_results = {}
user_votes = {}  # 각 채널에서 사용자의 투표 여부 저장

@bot.event
async def on_ready():
    print(f"Bot logged in : {bot.user}")

@bot.command()
async def bal(ctx, first: str, second: str):
    user = ctx.author.mention
    channel_id = ctx.channel.id  # 채널 ID 기준으로 저장

    # 해당 채널의 투표 결과 초기화 (first, second 저장)
    vote_results[channel_id] = {"1": 0, "2": 0, "first": first, "second": second}
    user_votes[channel_id] = {}  # 사용자 투표 기록 초기화

    await ctx.send(f"## {user} just started balance game!!\n# 1. {first} vs 2. {second}\n")
    await asyncio.sleep(0.5)
    await ctx.send("3")
    await asyncio.sleep(1)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    await ctx.send("Your choice? 1 or 2")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel_id = message.channel.id
    user_id = message.author.id

    if channel_id in vote_results and message.content in ["1", "2"]:
        if user_id in user_votes[channel_id]:
            await message.add_reaction("❌")  # 중복 투표 방지
        else:
            vote_results[channel_id][message.content] += 1
            user_votes[channel_id][user_id] = message.content  # 사용자 투표 기록
            await message.add_reaction("✅")  # 유저가 투표하면 체크 이모지 추가

    await bot.process_commands(message)  # 명령어도 처리할 수 있도록 추가

@bot.command()
async def balresult(ctx):
    channel_id = ctx.channel.id

    if channel_id not in vote_results:
        await ctx.send("Nobody voted yet.")
        return

    votes = vote_results[channel_id]
    first = votes["first"]
    second = votes["second"]

    result_message = f"# Result\n{first}: {votes['1']} votes\n{second}: {votes['2']} votes\n"

    if votes["1"] > votes["2"]:
        result_message += f"# 🏆 {first} Wins!"
    elif votes["1"] < votes["2"]:
        result_message += f"# 🏆 {second} Wins!"
    else:
        result_message += "🤝 Draw!"

    await ctx.send(result_message)

    # 투표 결과 초기화
    del vote_results[channel_id]
    del user_votes[channel_id]

@bot.command()
async def pp(ctx):
    await ctx.send(privacy_policy.privacy_policy)

@bal.error
async def bal_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERR occurred: Missing Required Arguments")

bot.run(TOKEN)
