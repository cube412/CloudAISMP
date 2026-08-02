import discord

from ai import analyze_log
from guard import scan_log


async def handle_log(message):

    if len(message.attachments) == 0:
        return False

    file = message.attachments[0]

    if not file.filename.endswith(".log"):
        return False

    data = await file.read()

    text = data.decode("utf-8", errors="ignore")

    if len(text) > 30000:
        text = text[-30000:]

    report = scan_log(text)

    await message.reply(
        f"""
🛡 **CloudAI Guard**

❤️ Health: **{report['health']}%**

❌ Error: **{report['errors']}**

⚠ Warning: **{report['warnings']}**

💥 Exception: **{report['exceptions']}**

📦 Plugins:
{', '.join(report['plugins']) if report['plugins'] else 'Không phát hiện'}

🤖 AI đang phân tích sâu...
"""
    )

    result = await analyze_log(text)

    if len(result) > 2000:
        result = result[:1990]

    await message.reply(result)

    return True
