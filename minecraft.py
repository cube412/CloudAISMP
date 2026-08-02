import discord

from ai import analyze_log
from guard import scan_log
from plugin_database import PLUGIN_FIXES


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

    tips = []

    for plugin in report["plugins"]:
        if plugin in PLUGIN_FIXES:
            tips.append(
                f"• **{plugin}**: {PLUGIN_FIXES[plugin]}"
            )

    plugins = (
        "\n".join(f"• {p}" for p in report["plugins"])
        if report["plugins"]
        else "Không phát hiện"
    )

    suggestions = (
        "\n".join(tips)
        if tips
        else "Không có khuyến nghị."
    )

    await message.reply(
        f"""
# 🛡 CloudAI Guard

❤️ **Health:** {report['health']}%

❌ **Errors:** {report['errors']}

⚠ **Warnings:** {report['warnings']}

💥 **Exceptions:** {report['exceptions']}

📦 **Plugins phát hiện:**

{plugins}

💡 **Khuyến nghị:**

{suggestions}

🤖 Đang phân tích AI...
"""
    )

    result = await analyze_log(text)

    if len(result) > 2000:
        result = result[:1990] + "..."

    await message.reply(result)

    return True
