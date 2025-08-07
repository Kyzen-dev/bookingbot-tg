from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['booking']
bookings_collection = db["booking-tg"]

def add_booking(data: dict):
    return bookings_collection.insert_one(data)

def get_bookings_by_date(date_str: str):
    return list(bookings_collection.find({"date": date_str}))

def is_slot_booked(date: str, time: str):
    return bookings_collection.find_one({"date": date, "time": time}) is not None