from dotenv import load_dotenv
import os


load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
GPT_KEY = os.getenv("GPT_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PROXY = os.getenv("PROXY")