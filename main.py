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
from orders import OrderView, TicketView

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

```
await bot.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="CloudAI V6.3"
    )
)

try:
    bot.tree.add_command(cloud_commands)
    print("✅ Đã đăng ký CloudCommands")
except Exception as e:
    print(f"⚠️ CloudCommands: {e}")

try:
    bot.tree.add_command(admin_commands)
    print("✅ Đã đăng ký AdminCommands")
except Exception as e:
    print(f"⚠️ AdminCommands: {e}")

try:
    synced = await bot.tree.sync()
    print(f"✅ Đồng bộ {len(synced)} Slash Commands")
except Exception as e:
    print(f"❌ Lỗi Slash Commands: {e}")

try:
    bot.add_view(OrderView())
    bot.add_view(TicketView())
    print("✅ Đã đăng ký Order/Ticket Views")
except Exception as e:
    print(f"⚠️ View Error: {e}")
```

@bot.event
async def on_message(message):
if message.author.bot:
return

```
try:
    handled = await handle_log(message)

    if handled:
        return

except Exception as e:
    print(f"[CloudAI] Log Handler Error: {e}")

if bot.user and bot.user in message.mentions:
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
        try:
            answer = await ask_ai(
                str(message.author.id),
                question
            )

        except Exception as e:
            print(f"[CloudAI] AI Error: {e}")
            answer = (
                "❌ AI đang gặp lỗi. "
                "Vui lòng thử lại sau."
            )

    if len(answer) > 2000:
        answer = answer[:1990] + "..."

    await message.reply(answer)

await bot.process_commands(message)
```

def run_dashboard():
port = int(
os.environ.get(
"PORT",
8080
)
)

```
app.run(
    host="0.0.0.0",
    port=port
)
```

threading.Thread(
target=run_dashboard,
daemon=True
).start()

print("🚀 Đang khởi động CloudAI...")

bot.run(DISCORD_TOKEN)
