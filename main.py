import logging
import os
import motor.motor_asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime

import menus
import db

from openai_setup import setup, generate_response

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# print(MONGO_USER, MONGO_PASSWORD)

connection_string = (
    "mongodb+srv://"
    + MONGO_USER
    + ":"
    + MONGO_PASSWORD
    + "@flashbackmvp.fugosts.mongodb.net/?retryWrites=true&w=majority"
)

cluster = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
db = cluster["Tg-mvp"]
collection = db["Users"]


logging.basicConfig(level=logging.INFO)


setup(OPENAI_TOKEN)

# Initialize bot and dispatcher
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="📝 Create Twin", callback_data="create_twin"),
        InlineKeyboardButton(text="🖼 Open Collection", callback_data="open_collection"),
    )
    menu.add(InlineKeyboardButton(text="🔎 Help", callback_data="help"))

    msg = "Welcome to Flashback!"
    await bot.send_message(message.chat.id, msg, reply_markup=menu)

    user_id = message.chat.id
    await db.add_user(collection, user_id)


@dp.message_handler()
async def my_responses(message: types.Message):
    answer = generate_response(message)
    await message.answer(answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
