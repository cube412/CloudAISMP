import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai import ask_ai
from commands import CloudCommands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 Đã đăng nhập: {bot.user}")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudAI | Minecraft"
        )
    )

    try:
        bot.tree.add_command(CloudCommands())
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} Slash Commands")
    except Exception as e:
        print(f"Lỗi đồng bộ Slash Commands: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:

        question = message.content.replace(
            f"<@{bot.user.id}>", ""
        ).strip()

        if question == "":
            await message.reply(
                "👋 Xin chào! Hãy hỏi mình điều gì đó nhé."
            )
            return

        async with message.channel.typing():

            answer = await ask_ai(question)

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await message.reply(answer)

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
