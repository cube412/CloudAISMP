import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from ai import ask_ai
from minecraft import handle_log
from commands import CloudCommands
from dashboard import app
import threading

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

cloud_commands = CloudCommands()

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 Đã đăng nhập: {bot.user}")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudSMP | @CloudAI"
        )
    )

    try:
        bot.tree.add_command(cloud_commands)
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} Slash Commands")
    except Exception as e:
        print(f"Lỗi Slash Commands: {e}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Nếu có file .log thì phân tích
    handled = await handle_log(message)
    if handled:
        return

    # AI chỉ trả lời khi được mention
    if bot.user in message.mentions:

        question = (
            message.content
            .replace(f"<@{bot.user.id}>", "")
            .replace(f"<@!{bot.user.id}>", "")
            .strip()
        )

        if not question:
            await message.reply(
                "👋 Xin chào! Hãy hỏi mình điều gì đó nhé!"
            )
            return

        async with message.channel.typing():
            answer = await ask_ai(
                str(message.author.id),
                question
            )

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await message.reply(answer)

    await bot.process_commands(message)
   threading.Thread(
    target=lambda: app.run(
        host="0.0.0.0",
        port=8080
    ),
    daemon=True
).start()

bot.run(DISCORD_TOKEN)
