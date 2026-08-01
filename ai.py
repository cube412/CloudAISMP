from google import genai
from config import GEMINI_API_KEY, AI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

memory = {}

SYSTEM_PROMPT = """
Bạn là CloudAI.

Luôn trả lời bằng tiếng Việt.

Bạn là chuyên gia:

- Minecraft
- Paper
- Spigot
- Plugin
- Discord
- Python

Trả lời ngắn gọn và dễ hiểu.
"""


async def ask_ai(user_id, question):

    if user_id not in memory:
        memory[user_id] = []

    history = memory[user_id]

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

        history.append({
            "role": "Người dùng",
            "content": question
        })

        history.append({
            "role": "CloudAI",
            "content": answer
        })

        if len(history) > 20:
            history[:] = history[-20:]

        return answer

    except Exception as e:
        return f"Lỗi AI: {e}"


async def analyze_log(log_text):

    prompt = f"""
Bạn là chuyên gia Minecraft.

Đây là file cấu hình hoặc file log.

Hãy:

- Phân tích file
- Tìm lỗi
- Tìm WARNING
- Tìm plugin lỗi
- Giải thích bằng tiếng Việt
- Đưa cách sửa

Nội dung file:

{log_text}
"""

Log:

{log_text}
"""

    try:

        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return str(e)
