from telebot.types import Message
from services.db import get_all_bookings

ADMIN_ID = 7190652412  # 🔁 عدد عددی آیدی خودت رو بذار اینجا (نه username)

def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "/admin")
    def handle_admin_panel(message: Message):
        if message.from_user.id != ADMIN_ID:
            return bot.reply_to(message, "⛔️ دسترسی ندارید.")

        bookings = get_all_bookings()
        if not bookings:
            return bot.reply_to(message, "📭 هیچ رزروی ثبت نشده است.")

        text = "📋 لیست رزروها:\n\n"
        for i, booking in enumerate(bookings, 1):
            text += f"{i}. {booking['full_name']} - {booking['date']} {booking['time']}\n"

        bot.reply_to(message, text)
        return None
