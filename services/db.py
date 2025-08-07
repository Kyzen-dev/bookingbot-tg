from tinydb import TinyDB, Query
from pymongo import MongoClient
import os
from config import MONGO_URI

db_path = os.path.join(os.path.dirname(__file__), 'data\db.json')
db = TinyDB(db_path)

def save_booking(user_id, full_name, date, time):
    db.insert({'user_id': user_id, 'full_name': full_name, 'date': date, 'time': time})


def get_booked_slots(date_str):
    # date_str مثل "1403/04/30"
    query = "SELECT time FROM bookings WHERE date = ?"
    result = db.execute(query, (date_str,)).fetchall()
    return [row[0] for row in result]


def get_bookings_by_user(user_id):
    booking = Query()
    return db.search(booking.user_id == user_id)


def delete_booking(user_id):
    booking = Query()
    db.remove(booking.user_id == user_id)


def get_user_booking(user_id):
    return db.get(Query().user_id == user_id)


def cancel_booking(user_id):
    db.remove(Query().user_id == user_id)


def get_all_bookings():
    return db.all()


# client = MongoClient(MONGO_URI)  # یا اتصال به MongoDB Atlas
# db = client["booking_bot"]
# bookings_collection = db["bookings"]
#
# def add_booking(user_id, name, date, time):
#     bookings_collection.insert_one({
#         "user_id": user_id,
#         "name": name,
#         "date": date,
#         "time": time
#     })
#
# def get_booked_slots(date):
#     bookings = bookings_collection.find({"date": date})
#     return [b["time"] for b in bookings]
#
# def get_user_bookings(user_id):
#     return list(bookings_collection.find({"user_id": user_id}))
#
