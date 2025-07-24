from tinydb import TinyDB, Query
import os

db_path = os.path.join(os.path.dirname(__file__), 'data\db.json')
db = TinyDB(db_path)

def save_booking(user_id, full_name, date, time):
    db.insert({'user_id': user_id, 'full_name': full_name, 'date': date, 'time': time})


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
