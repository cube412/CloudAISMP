import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Discord
# =========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PREFIX = "!"

BOT_NAME = "CloudAI"

# Discord User ID của Owner
ADMIN_ID = 1514447473748475975

# =========================
# Gemini AI
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

AI_MODEL = "gemini-3.6-flash"

MAX_HISTORY = 10

# =========================
# CloudAI
# =========================

VERSION = "5.0"

EMBED_COLOR = 0x00BFFF
