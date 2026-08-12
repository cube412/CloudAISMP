from google import genai

from config import GEMINI_API_KEY, AI_MODEL, BOT_NAME
from memory import add_message, get_history

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = f"""
Bạn là {BOT_NAME}, một trợ lý AI Discord.

Luôn trả lời bằng tiếng Việt.

Bạn có kiến thức về:
- Discord
- Python
- Minecraft
- Paper
- Spigot
- Plugin
- Server
- Công nghệ

Hãy trả lời dễ hiểu, thân thiện và ngắn gọn.
Nếu người dùng hỏi về chủ đề khác, vẫn cố gắng hỗ trợ trong khả năng của bạn.
"""


async def ask_ai(user_id, question):

    history = get_history(user_id)

    prompt = SYSTEM_PROMPT + "\n\n"

    for msg in history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += f"Người dùng: {question}"

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        answer = response.text

        add_message(
            user_id,
            "Người dùng",
            question
        )

        add_message(
            user_id,
            "CloudAI",
            answer
        )

        return answer

    except Exception as e:
        return f"❌ Lỗi AI: {e}"


async def analyze_log(log_text):

    prompt = f"""
Bạn là chuyên gia Minecraft server.

Hãy phân tích nội dung log bên dưới.

Hãy:
- Tìm ERROR
- Tìm WARNING
- Tìm plugin gây lỗi
- Tìm nguyên nhân
- Giải thích lỗi bằng tiếng Việt
- Đưa cách sửa
- Nếu không có lỗi nghiêm trọng, nói rõ điều đó

Nội dung log:

{log_text}
"""

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Lỗi phân tích: {e}"
