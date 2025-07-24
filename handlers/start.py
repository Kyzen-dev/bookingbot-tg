from telebot.types import Message
from keyboards.main_menu import main_menu

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message: Message):
        bot.send_message(
            message.chat.id,
            "سلام! به ربات رزرو وقت خوش اومدی. لطفا یک گزینه رو انتخاب کن:",
            reply_markup=main_menu()
        )

    @bot.message_handler(func=lambda m: m.text == "🔙 برگشت به منو")
    def go_back_to_main(message):
        bot.send_message(message.chat.id, "🏠 برگشتید به منوی اصلی", reply_markup=main_menu())

