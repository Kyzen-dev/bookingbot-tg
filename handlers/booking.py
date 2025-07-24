from keyboards.booking_menu import date_keyboard, time_keyboard
from services.db import save_booking
from telebot.types import Message
from services.db import cancel_booking, get_user_booking
from keyboards.booking_menu import booking_menu

booking_data = {}

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "📅 رزرو وقت")
    def start_booking(message: Message):
        bot.send_message(message.chat.id, "لطفا تاریخ مورد نظر را انتخاب کنید:", reply_markup=date_keyboard())

    @bot.message_handler(func=lambda m: m.text in ["1403/04/20", "1403/04/21", "1403/04/22"])  # مثال تاریخ
    def select_date(message: Message):
        booking_data[message.chat.id] = {'date': message.text}
        bot.send_message(message.chat.id, "ساعت مورد نظر را انتخاب کنید:", reply_markup=time_keyboard())

    @bot.message_handler(func=lambda m: m.text in ["10:00", "12:00", "14:00"])  # مثال ساعت
    def select_time(message: Message):
        user_data = booking_data.get(message.chat.id, {})
        user_data['time'] = message.text
        save_booking(message.chat.id,message.chat.first_name, user_data['date'], user_data['time'])
        bot.send_message(message.chat.id, f"✅ وقت شما ثبت شد: {user_data['date']} - {user_data['time']}")

    @bot.message_handler(func=lambda m: m.text == "❌ لغو رزرو")
    def handle_cancel_booking(message: Message):
        user_id = message.from_user.id
        booking = get_user_booking(user_id)

        if booking:
            cancel_booking(user_id)
            bot.reply_to(message, "✅ رزرو شما با موفقیت لغو شد.", reply_markup=booking_menu())
        else:
            bot.reply_to(message, "📭 شما رزروی ندارید که لغو شود.", reply_markup=booking_menu())
