from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📅 رزرو وقت"))
    kb.add(KeyboardButton("❌ لغو رزرو"))
    return kb
