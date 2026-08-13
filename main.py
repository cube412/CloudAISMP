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


# =========================================================
# INTENTS
# =========================================================

intents = discord.Intents.default()
intents.message_content = True


# =========================================================
# BOT
# =========================================================

class CloudAIBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

        self.cloud_commands = CloudCommands()
        self.admin_commands = AdminCommands()

    async def setup_hook(self):

        print("🔧 Đang đăng ký Slash Commands...")

        # -------------------------------------------------
        # CLOUD COMMANDS
        # -------------------------------------------------

        try:

            self.tree.add_command(
                self.cloud_commands
            )

            print("✅ Đã đăng ký CloudCommands")

        except discord.app_commands.errors.CommandAlreadyRegistered:

            print("⚠️ CloudCommands đã tồn tại")

        except Exception as e:

            print(
                f"❌ Lỗi CloudCommands: {e}"
            )

        # -------------------------------------------------
        # ADMIN COMMANDS
        # -------------------------------------------------

        try:

            self.tree.add_command(
                self.admin_commands
            )

            print("✅ Đã đăng ký AdminCommands")

        except discord.app_commands.errors.CommandAlreadyRegistered:

            print("⚠️ AdminCommands đã tồn tại")

        except Exception as e:

            print(
                f"❌ Lỗi AdminCommands: {e}"
            )

        # -------------------------------------------------
        # SYNC
        # -------------------------------------------------

        try:

            synced = await self.tree.sync()

            print(
                f"✅ Đồng bộ {len(synced)} Slash Commands"
            )

            for command in synced:

                print(
                    f"   /{command.name}"
                )

        except Exception as e:

            print(
                f"❌ Lỗi đồng bộ Slash Commands: {e}"
            )


# =========================================================
# TẠO BOT
# =========================================================

bot = CloudAIBot()


# =========================================================
# READY
# =========================================================

@bot.event
async def on_ready():

    print("=" * 40)

    print(
        f"🤖 Đăng nhập thành công: {bot.user}"
    )

    print(
        f"🆔 Bot ID: {bot.user.id}"
    )

    print("=" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudAI V6.3"
        )
    )


# =========================================================
# MESSAGE
# =========================================================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    # -----------------------------------------------------
    # PHÂN TÍCH FILE LOG
    # -----------------------------------------------------

    try:

        handled = await handle_log(message)

        if handled:
            return

    except Exception as e:

        print(
            f"❌ Lỗi handle_log: {e}"
        )

    # -----------------------------------------------------
    # AI KHI ĐƯỢC MENTION
    # -----------------------------------------------------

    if bot.user and bot.user in message.mentions:

        question = (
            message.content
            .replace(
                f"<@{bot.user.id}>",
                ""
            )
            .replace(
                f"<@!{bot.user.id}>",
                ""
            )
            .strip()
        )

        if not question:

            await message.reply(
                "👋 Xin chào! Hãy hỏi mình điều gì đó nhé."
            )

            return

        async with message.channel.typing():

            try:

                answer = await ask_ai(
                    str(message.author.id),
                    question
                )

            except Exception as e:

                print(
                    f"❌ Lỗi AI: {e}"
                )

                answer = (
                    "❌ CloudAI đang gặp lỗi khi xử lý câu hỏi."
                )

        if len(answer) > 2000:

            answer = (
                answer[:1990]
                + "..."
            )

        await message.reply(
            answer
        )

    # -----------------------------------------------------
    # PREFIX COMMAND
    # -----------------------------------------------------

    await bot.process_commands(
        message
    )


# =========================================================
# DASHBOARD
# =========================================================

def run_dashboard():

    port = int(
        os.environ.get(
            "PORT",
            8080
        )
    )

    print(
        f"🌐 Dashboard chạy tại port {port}"
    )

    app.run(
        host="0.0.0.0",
        port=port
    )


threading.Thread(
    target=run_dashboard,
    daemon=True
).start()


# =========================================================
# START BOT
# =========================================================

print("🚀 Đang khởi động CloudAI...")

bot.run(
    DISCORD_TOKEN
)
