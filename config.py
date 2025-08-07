import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS=list(map(int, os.getenv("ADMINS").split(",")))
TIMEZONE=os.getenv("TZ","Asia/Tehran")
MONGO_URI ="mongodb://localhost:27017/"
db=[]
