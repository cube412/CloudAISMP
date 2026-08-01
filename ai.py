from google import genai
from config import GEMINI_API_KEY, AI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Bạn là CloudAI.

- Luôn trả lời bằng tiếng Việt.
- Thân thiện.
- Chuyên gia Minecraft.
- Giỏi Paper, Spigot, plugin, Geyser, LuckPerms...
"""

async def ask_ai(question):

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=SYSTEM_PROMPT + "\n\nNgười dùng: " + question
        )

        if response.text:
            return response.text

        return "❌ AI không trả lời."

    except Exception as e:
        return f"❌ Lỗi AI: {e}"
