import datetime


async def add_user(collection, user_id):
    date = datetime.now().date()
    collection.insert_one(
        {
            "_id": user_id,
            "date": str(date),
        }
    )
