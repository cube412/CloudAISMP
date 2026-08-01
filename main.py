import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from ai import ask_ai
from minecraft import handle_log
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
    print(f"🤖 Đăng nhập thành công: {bot.user}")
    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudSMP | @CloudAI"
        )
    )

    try:
        bot.tree.add_command(CloudCommands())
        synced = await bot.tree.sync()
        print(f"✅ Đồng bộ {len(synced)} Slash Commands")
    except Exception as e:
        print(f"Lỗi đồng bộ Slash Commands: {e}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Nếu người dùng gửi latest.log thì xử lý
    handled = await handle_log(message)
    if handled:
        return

    # Chỉ trả lời khi được mention
    if bot.user in message.mentions:

        question = (
            message.content.replace(f"<@{bot.user.id}>", "")
            .replace(f"<@!{bot.user.id}>", "")
            .strip()
        )

        if not question:
            await message.reply("👋 Xin chào! Hãy hỏi mình điều gì đó nhé.")
            return

        async with message.channel.typing():
            answer = await ask_ai(question)

        if len(answer) > 2000:
            answer = answer[:1990] + "..."

        await message.reply(answer)

    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)
