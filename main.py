import os
import threading

import aiohttp
import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from ai import ask_ai
from minecraft import handle_log
from commands import CloudCommands
from admin import AdminCommands
from dashboard import app
from orders import OrderView, TicketView


# =========================
# DISCORD INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True


# =========================
# BOT
# =========================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


cloud_commands = CloudCommands()
admin_commands = AdminCommands()


# =========================
# PROVISIONING CONFIG
# =========================

async def get_guild_config(guild_id):
    """
    Lấy cấu hình của server từ Provisioning Receiver.
    """

    base_url = os.getenv(
        "CONFIG_URL",
        ""
    ).rstrip("/")

    secret = os.getenv(
        "PROVISIONING_SECRET",
        ""
    )

    if not base_url:
        print("❌ Chưa cấu hình CONFIG_URL")
        return None

    headers = {}

    if secret:
        headers["Authorization"] = f"Bearer {secret}"

    url = f"{base_url}/configs/{guild_id}"

    try:
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.get(
                url,
                headers=headers
            ) as response:

                if response.status == 404:
                    print(
                        f"⚠️ Không có config cho server {guild_id}"
                    )
                    return None

                if response.status != 200:
                    print(
                        f"❌ Receiver trả HTTP {response.status}"
                    )
                    return None

                data = await response.json()

                print(
                    f"✅ Đã lấy config server {guild_id}"
                )

                return data

    except Exception as e:
        print(
            f"❌ Không thể kết nối Provisioning Receiver: {e}"
        )

        return None


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():

    print("========================================")
    print(
        f"🤖 Đăng nhập thành công: {bot.user}"
    )
    print("========================================")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="CloudAI V6.3"
        )
    )

    # CloudCommands
    try:

        bot.tree.add_command(
            cloud_commands
        )

        print(
            "✅ CloudCommands đã đăng ký"
        )

    except Exception as e:

        print(
            f"⚠️ CloudCommands: {e}"
        )

    # AdminCommands
    try:

        bot.tree.add_command(
            admin_commands
        )

        print(
            "✅ AdminCommands đã đăng ký"
        )

    except Exception as e:

        print(
            f"⚠️ AdminCommands: {e}"
        )

    # Slash Commands
    try:

        synced = await bot.tree.sync()

        print(
            f"✅ Đồng bộ {len(synced)} Slash Commands"
        )

    except Exception as e:

        print(
            f"❌ Lỗi đồng bộ: {e}"
        )

    # Persistent Views
    try:

        bot.add_view(
            OrderView()
        )

        bot.add_view(
            TicketView()
        )

        print(
            "✅ Order/Ticket View đã đăng ký"
        )

    except Exception as e:

        print(
            f"⚠️ View Error: {e}"
        )


# =========================
# BOT JOIN SERVER
# =========================

@bot.event
async def on_guild_join(guild):

    print(
        f"📥 CloudAI vừa vào server:"
        f" {guild.name} ({guild.id})"
    )

    config = await get_guild_config(
        guild.id
    )

    if config:

        plan = config.get(
            "plan",
            "Không xác định"
        )

        print(
            f"✅ Server {guild.id}"
            f" đã có config hợp lệ."
        )

        print(
            f"📦 Gói: {plan}"
        )

    else:

        print(
            f"⚠️ Server {guild.id}"
            f" chưa có config đơn hàng."
        )


# =========================
# MESSAGE HANDLER
# =========================

@bot.event
async def on_message(message):

    # Không xử lý tin nhắn của bot
    if message.author.bot:
        return

    # =========================
    # MINECRAFT LOG
    # =========================

    try:

        handled = await handle_log(
            message
        )

        if handled:
            return

    except Exception as e:

        print(
            f"[CloudAI] Log Error: {e}"
        )

    # =========================
    # AI CHAT
    # =========================

    if (
        bot.user
        and bot.user in message.mentions
    ):

        # Chỉ xử lý AI trong server
        if not message.guild:

            await bot.process_commands(
                message
            )

            return

        # =========================
        # KIỂM TRA CONFIG SERVER
        # =========================

        config = await get_guild_config(
            message.guild.id
        )

        if not config:

            await message.reply(
                "❌ Server này chưa có "
                "gói CloudAI hợp lệ."
            )

            await bot.process_commands(
                message
            )

            return

        # =========================
        # LẤY CÂU HỎI
        # =========================

        question = message.content

        question = question.replace(
            f"<@{bot.user.id}>",
            ""
        )

        question = question.replace(
            f"<@!{bot.user.id}>",
            ""
        )

        question = question.strip()

        # =========================
        # CHỈ @BOT KHÔNG CÓ CÂU HỎI
        # =========================

        if not question:

            await message.reply(
                "👋 Xin chào! "
                "Hãy hỏi mình điều gì đó nhé."
            )

            await bot.process_commands(
                message
            )

            return

        # =========================
        # GỌI AI
        # =========================

        async with message.channel.typing():

            try:

                answer = await ask_ai(
                    str(message.author.id),
                    question
                )

            except Exception as e:

                print(
                    f"[CloudAI] AI Error: {e}"
                )

                answer = (
                    "❌ AI đang gặp lỗi."
                )

        # =========================
        # GIỚI HẠN DISCORD 2000 KÝ TỰ
        # =========================

        if len(answer) > 2000:

            answer = (
                answer[:1990]
                + "..."
            )

        await message.reply(
            answer
        )

    # =========================
    # COMMANDS
    # =========================

    await bot.process_commands(
        message
    )


# =========================
# DASHBOARD
# =========================

def run_dashboard():

    port = int(
        os.environ.get(
            "PORT",
            8080
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )


threading.Thread(
    target=run_dashboard,
    daemon=True
).start()


# =========================
# START
# =========================

print(
    "🚀 Đang khởi động CloudAI..."
)


bot.run(
    DISCORD_TOKEN
)
