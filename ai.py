from google import genai

from config import (
    GEMINI_API_KEY,
    AI_MODEL,
    BOT_NAME,
    BOT_TOPIC
)

from memory import add_message, get_history


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPT = f"""
Bạn là {BOT_NAME}, một trợ lý AI Discord.

Chủ đề chính của bạn là:
{BOT_TOPIC}

Luôn trả lời bằng tiếng Việt.

Hãy:
- Trả lời dễ hiểu.
- Thân thiện.
- Không bịa thông tin.
- Nếu không biết, hãy nói rõ.
- Nếu người dùng hỏi ngoài chủ đề,
  vẫn cố gắng hỗ trợ nếu có thể.
"""


async def ask_ai(user_id, question):

    history = get_history(user_id)

    prompt = SYSTEM_PROMPT + "\n\n"

    for msg in history:
        prompt += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

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

Hãy phân tích log dưới đây.

Hãy tìm:

- ERROR
- WARNING
- Plugin lỗi
- Nguyên nhân
- Cách sửa

Hãy giải thích bằng tiếng Việt
và dễ hiểu.

LOG:

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
