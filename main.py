import telebot
from config import BOT_TOKEN
from handlers import start, booking, admin
from services.scheduler import start_scheduler

# from services.scheduler import start_scheduler



bot = telebot.TeleBot(BOT_TOKEN)


#conecction_handlers

start.register_handlers(bot)
booking.register_handlers(bot)
admin.register_handlers(bot)

start_scheduler(bot)


print("✅ Bot is running...")



bot.set_webhook(url="https://"https://bookingbot-tg.onrender.com")
