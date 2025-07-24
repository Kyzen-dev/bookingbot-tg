from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def date_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("1403/04/20"), KeyboardButton("1403/04/21"), KeyboardButton("1403/04/22"))
    return kb

def time_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("10:00"), KeyboardButton("12:00"), KeyboardButton("14:00"))
    return kb

def booking_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📅 رزرو وقت"), KeyboardButton("❌ لغو رزرو"))
    kb.add(KeyboardButton("🔙 برگشت به منو"))
    return kb
