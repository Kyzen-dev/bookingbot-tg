from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from services.booking_db import is_slot_booked
from services.booking_db import get_bookings_by_date

import jdatetime

def get_available_jalali_dates(num_days=7):
    today = jdatetime.date.today()
    return [(today + jdatetime.timedelta(days=i)).strftime('%Y/%m/%d') for i in range(num_days)]




def date_keyboard():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        dates = get_available_jalali_dates()
        buttons = [KeyboardButton(date) for date in dates]
        markup.add(*buttons)
        return markup



def time_keyboard(date_str):
    from telebot import types

    all_times = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
    booked_times = get_booked_slots(date_str)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for time in all_times:
        if time not in booked_times:
            markup.add(time)
    return markup


def booking_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📅 رزرو وقت"), KeyboardButton("❌ لغو رزرو"))
    kb.add(KeyboardButton("🔙 برگشت به منو"))
    return kb

def get_booked_slots(date: str):
    # برای گرفتن لیست ساعت‌های رزروشده
        bookings = get_bookings_by_date(date)
        return [b['time'] for b in bookings]
