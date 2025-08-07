from utils.pdf_generator import generate_booking_pdf
from telebot.types import InputFile
from keyboards.booking_menu import date_keyboard, time_keyboard
from telebot.types import Message
from services.db import cancel_booking, get_user_booking
from keyboards.booking_menu import booking_menu
from keyboards.booking_menu import get_available_jalali_dates
from services.booking_storage import  generate_tracking_code, find_booking_by_ref
from services.booking_storage import add_booking
import os




os.makedirs("receipts", exist_ok=True)




booking_data = {}
AVAILABLE_DATES = get_available_jalali_dates()



def send_booking_receipt(bot, message, data):
    safe_date = data['date'].replace('/', '-')
    safe_time = data.get('time', '').replace(':', '-')
    file_path = f"receipts/booking_{message.chat.id}_{safe_date}_{safe_time}.pdf"
    pdf_path = generate_booking_pdf(data, file_path)
    with open(pdf_path, 'rb') as f:
        bot.send_document(message.chat.id, InputFile(f), caption="📄 رسید رزرو شما")



def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "📅 رزرو وقت")
    def start_booking(message: Message):
        bot.send_message(message.chat.id, "لطفا تاریخ مورد نظر را انتخاب کنید:", reply_markup=date_keyboard())

    @bot.message_handler(func=lambda m: m.text and m.text.count('/') == 2)
    def select_date(message: Message):
        booking_data[message.chat.id] = {'date': message.text}
        bot.send_message(message.chat.id, "ساعت مورد نظر را انتخاب کنید:", reply_markup=time_keyboard(message.text))

    @bot.message_handler(
        func=lambda m: m.text and m.text in ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"])
    def select_time(message: Message):
        user_id = message.from_user.id
        if message.chat.id not in booking_data:
            bot.send_message(message.chat.id, "ابتدا تاریخ را انتخاب کنید.")
            return

        booking_data[message.chat.id]['time'] = message.text  # ذخیره ساعت انتخاب شده
        user_info = {
            "name": message.from_user.full_name or message.from_user.first_name or "کاربر",
            "phone": ""  # اگر شماره یا اطلاعات بیشتری داری، اضافه کن
        }
        booking_info = booking_data[message.chat.id]
        ref_code = generate_tracking_code()

        success = add_booking({
            "user_id": user_id,
            "full_name": user_info['name'],
            "date": booking_info['date'],
            "time": booking_info['time'],
            "phone": "",
            "ref_code": ref_code  # 👈 اضافه شد
        })
        combined_data = {
            **user_info,
            **booking_info,
            "ref_code":ref_code
        }
        send_booking_receipt(bot, message, combined_data)
        if success:
            bot.send_message(message.chat.id,
                             f"✅ وقت شما برای {booking_info['date']} ساعت {booking_info['time']} ثبت شد.")
            bot.send_message(message.chat.id, f"✅ رزرو با موفقیت ثبت شد!\nکد پیگیری شما: {ref_code}")
        else:
            bot.send_message(message.chat.id, "⚠️ این ساعت قبلاً رزرو شده است.")

    @bot.message_handler(func=lambda m: m.text == "❌ لغو رزرو")
    def handle_cancel_booking(message: Message):
        user_id = message.from_user.id
        booking = get_user_booking(user_id)

        if booking:
            cancel_booking(user_id)
            bot.reply_to(message, "✅ رزرو شما با موفقیت لغو شد.", reply_markup=booking_menu())
        else:
            bot.reply_to(message, "📭 شما رزروی ندارید که لغو شود.", reply_markup=booking_menu())

    @bot.message_handler(commands=['status'])
    def booking_status(message):
        try:
            ref_code = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, "لطفا کد پیگیری خود را وارد کنید. مثال:\n/status ABCD1234")
            return
        booking = find_booking_by_ref(ref_code)
        if booking:
            bot.reply_to(message,
                         (f"رزرو شما:\nنام: {booking['name']}\n"
                          f"تاریخ: {booking['date']} ساعت: {booking['time']}\n"
                          f"وضعیت: {booking.get('status', 'pending')}"))
        else:
            bot.reply_to(message, "رزروی با این کد پیگیری یافت نشد.")