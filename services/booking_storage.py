from datetime import datetime

from pymongo import MongoClient
from config import MONGO_URI
import uuid
from bson import ObjectId



client = MongoClient(MONGO_URI)
db = client['booking']
bookings_collection = db["booking-tg"]




def generate_tracking_code():
    """ساخت کد یکتا برای پیگیری رزرو"""
    return str(uuid.uuid4())[:8].upper()



def add_booking(booking_data: dict):
    """
    booking_data باید شامل حداقل: date, time, full_name, ref_code باشد.
    """
    booking = {
        "date": booking_data.get("date"),
        "time": booking_data.get("time"),
        "name": booking_data.get("full_name"),
        "phone": booking_data.get("phone", ""),
        "service": booking_data.get("service"),
        "notes": booking_data.get("notes"),
        "status": "pending",
        "created_at": datetime.now(),
        "ref_code": booking_data.get("ref_code")  # 👈 مستقیماً ذخیره کن
    }

    result = bookings_collection.insert_one(booking)
    return result.acknowledged

def get_booked_slots(date):
    """بررسی زمان‌های رزرو شده در یک تاریخ خاص"""
    booked_slots = bookings_collection.find({"date": date})
    return [slot["time"] for slot in booked_slots]


def find_booking_by_ref(ref_code):
    return bookings_collection.find_one({'ref_code': ref_code})

def get_all_bookings():
    return list(bookings_collection.find().sort("created_at", -1))

def update_booking_status(ref_code, status):
    result = bookings_collection.update_one({'ref_code': ref_code}, {'$set': {'status': status}})
    return result.modified_count > 0