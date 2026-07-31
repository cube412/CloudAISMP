import os
import discord
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Gemini Key:", GEMINI_API_KEY[:10] if GEMINI_API_KEY else "KHÔNG CÓ API KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
SYSTEM_PROMPT = """
Bạn là CloudAI, một trợ lý AI trên Discord.

Quy tắc:
- Luôn trả lời bằng tiếng Việt.
- Thân thiện, ngắn gọn và dễ hiểu.
- Rất giỏi về Minecraft, Paper, Spigot, plugin, LuckPerms, Geyser, ViaVersion...
- Vẫn trả lời được mọi chủ đề khác.
"""

@client.event
async def on_ready():
    print(f"Đã đăng nhập với tên: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user not in message.mentions:
        return

    user_message = message.content.replace(f"<@{client.user.id}>", "").strip()

    if not user_message:
        await message.reply("Xin chào! Hãy hỏi mình bất cứ điều gì nhé 😊")
        return

    try:
        response = model.generate_content(
            SYSTEM_PROMPT + "\n\nNgười dùng: " + user_message
        )

        await message.reply(response.text)

    except Exception as e:
        await message.reply(f"Lỗi: {e}")

client.run(TOKEN)
