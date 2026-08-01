import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai import ask_ai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 Đăng nhập thành công: {bot.user}")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Cloud SMP | @CloudAI"
        )
    )

    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} slash command")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:

        question = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if question == "":
            await message.reply("👋 Xin chào! Hãy hỏi mình điều gì đó nhé.")
            return

        async with message.channel.typing():
            answer = await ask_ai(question)

        await message.reply(answer)

    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)
