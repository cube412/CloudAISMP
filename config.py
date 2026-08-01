import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BOT_NAME = "CloudAI"

AI_MODEL = "gemini-flash-latest"

PREFIX = "!"

MAX_HISTORY = 10
