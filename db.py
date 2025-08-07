from pymongo import MongoClient
from config import MONGO_URI


client = MongoClient(MONGO_URI)
db = client['booking']


# می‌تونی مثلا اینو اضافه کنی برای تست:
def test_connection():
    try:
        # لیست نام تمام کالکشن‌ها
        print("✅ اتصال برقرار شد. کالکشن‌ها:", db.list_collection_names())
    except Exception as e:
        print("❌ خطا در اتصال به دیتابیس:", e)

test_connection()