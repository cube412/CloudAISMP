import discord
from ai import analyze_log

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

    await message.reply("🔍 Đang phân tích latest.log...")

    result = await analyze_log(text)

    if len(result) > 2000:
        result = result[:1990]

    await message.reply(result)

    return True
