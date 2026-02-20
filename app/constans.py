import os
from dotenv import load_dotenv

load_dotenv()

# database
DATABASE_URL = os.getenv("DATABASE_URL")

# telegram
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
