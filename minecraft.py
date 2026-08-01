import discord
from ai import analyze_log

SUPPORTED_FILES = (
    ".log",
    ".yml",
    ".yaml",
    ".properties",
)

async def handle_log(message):

    if len(message.attachments) == 0:
        return False

    file = message.attachments[0]

    if not file.filename.endswith(SUPPORTED_FILES):
        return False

    data = await file.read()

    text = data.decode("utf-8", errors="ignore")

    if len(text) > 30000:
        text = text[-30000:]

    await message.reply(
        f"📄 Đang phân tích **{file.filename}**..."
    )

    result = await analyze_log(text)

    if len(result) > 1990:
        result = result[:1990]

    await message.reply(result)

    return True
