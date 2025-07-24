from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import jdatetime
from datetime import datetime
from config import TIMEZONE
from services.db import db


def convert_jalali_to_gregorian(date_string):
    # ورودی: '1403/04/22 12:00'
    jdate = jdatetime.datetime.strptime(date_string, '%Y/%m/%d %H:%M')
    g_datetime = jdate.togregorian()

    tz = timezone(TIMEZONE)
    g_datetime = tz.localize(g_datetime)  # تبدیل به datetime aware

    return g_datetime


def send_reminder(bot):
    tz = timezone(TIMEZONE)
    now = datetime.now(tz)  # datetime aware با timezone

    for item in db:
        jalali_datetime_str = f"{item['date']} {item['time']}"  # مثل: '1403/04/22 12:00'
        g_datetime = convert_jalali_to_gregorian(jalali_datetime_str)

        delta = (g_datetime - now).total_seconds()

        # یادآوری فقط برای قرارهایی که کمتر از 1 ساعت تا شروع مونده:
        if 0 < delta < 3600:
            bot.send_message(item['user_id'], f"یادآوری: وقت شما در {item['date']} ساعت {item['time']} است.")


def start_scheduler(bot):
    scheduler = BackgroundScheduler(timezone=timezone(TIMEZONE))
    scheduler.add_job(lambda: send_reminder(bot), 'interval', minutes=5)  # هر 5 دقیقه چک کنه
    scheduler.start()
