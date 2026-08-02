import os
import threading

import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from ai import ask_ai
from minecraft import handle_log
from commands import CloudCommands
from admin import AdminCommands
from dashboard import app

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

cloud_commands = CloudCommands()
admin_commands = AdminCommands()


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 Đăng nhập thành công: {bot.user}")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudAI V6.3"
        )
    )

    try:
        bot.tree.add_command(cloud_commands)
    except Exception:
        pass

    try:
        bot.tree.add_command(admin_commands)
    except Exception:
        pass

    try:
        synced = await bot.tree.sync()
        print(f"✅ Đồng bộ {len(synced)} Slash Commands")
    except Exception as e:
        print("Lỗi Slash Commands:", e)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Phân tích file .log
    handled = await handle_log(message)
    if handled:
        return

    # Chỉ trả lời khi được mention
    if bot.user in message.mentions:

        question = (
            message.content
            .replace(f"<@{bot.user.id}>", "")
            .replace(f"<@!{bot.user.id}>", "")
            .strip()
        )

        if not question:
            await message.reply(
                "👋 Xin chào! Hãy hỏi mình điều gì đó nhé."
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


def run_dashboard():
    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )


threading.Thread(
    target=run_dashboard,
    daemon=True
).start()

bot.run(DISCORD_TOKEN)
