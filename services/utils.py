# utils/dates.py
import jdatetime
from datetime import datetime, timedelta
from services.db import get_all_booked_dates  # باید این تابع رو بسازی که همه تاریخ‌های رزرو شده رو بیاره

def get_available_dates(days_ahead=7):
    today = datetime.today()
    available_dates = []
    booked_dates = get_all_booked_dates()  # ['1403/04/25', '1403/04/27']

    for i in range(days_ahead):
        future_date = today + timedelta(days=i)
        future_jdate = jdatetime.date.fromgregorian(date=future_date)
        date_str = future_jdate.strftime('%Y/%m/%d')
        if date_str not in booked_dates:
            available_dates.append(date_str)

    return available_dates
