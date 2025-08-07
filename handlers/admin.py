from services.booking_storage import get_all_bookings, update_booking_status

ADMIN_ID = 766810509  # آیدی ادمین تلگرام

def register_handlers(bot):
    @bot.message_handler(commands=['all_bookings'])
    def all_bookings(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "شما اجازه دسترسی ندارید.")
            return
        bookings = get_all_bookings()
        if not bookings:
            bot.reply_to(message, "رزروی ثبت نشده.")
            return
        text = ""
        for b in bookings:
            text += (f"کد: {b.get('ref_code', 'ندارد')}\n"
                     f"نام: {b.get('name', 'ندارد')}\n"
                     f"تاریخ: {b.get('date', 'ندارد')} ساعت: {b.get('time', 'ندارد')}\n"
                     f"وضعیت: {b.get('status', 'pending')}\n\n")
        bot.reply_to(message, text)

    @bot.message_handler(commands=['confirm'])
    def confirm_booking(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "شما اجازه دسترسی ندارید.")
            return
        try:
            ref_code = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, "کد پیگیری را وارد کنید.")
            return
        if update_booking_status(ref_code, "confirmed"):
            bot.reply_to(message, f"رزرو با کد {ref_code} تایید شد.")
        else:
            bot.reply_to(message, "رزرو پیدا نشد.")

    @bot.message_handler(commands=['cancel'])
    def cancel_booking(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "شما اجازه دسترسی ندارید.")
            return
        try:
            ref_code = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, "کد پیگیری را وارد کنید.")
            return
        if update_booking_status(ref_code, "canceled"):
            bot.reply_to(message, f"رزرو با کد {ref_code} لغو شد.")
        else:
            bot.reply_to(message, "رزرو پیدا نشد.")