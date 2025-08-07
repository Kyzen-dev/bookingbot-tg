import json
import os

BOOKINGS_FILE = "data/bookings.json"  # مطمئن شو پوشه data وجود داره

def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        return []
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=4)

def is_slot_booked(date_str, time_str):
    bookings = load_bookings()
    for booking in bookings:
        if booking['date'] == date_str and booking['time'] == time_str:
            return True
    return False

def add_booking(date_str, time_str):
    bookings = load_bookings()
    if is_slot_booked(date_str, time_str):
        return False  # این زمان قبلا رزرو شده
    bookings.append({"date": date_str, "time": time_str})
    save_bookings(bookings)
    return True
