import logging
import os
import motor.motor_asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from datetime import datetime


# import dbshki

import menus
from openai_setup import generate_response

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

chat_history = ""
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


# setup(OPENAI_TOKEN)

# Initialize bot and dispatcher
bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Twin(StatesGroup):
    Age = State()
    Info = State()
    Chat = State()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    msg = "Welcome to Flashback!"
    await bot.send_message(message.chat.id, msg, reply_markup=menus.menu)

    user_id = message.chat.id
    await db.add_user(collection, user_id)
    await Twin.Age.set()


@dp.callback_query_handler(lambda query: query.data == "open_collection")
async def handle_open_collection(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "It is not available yet")


# @dp.message_handler(state=Twin.Age)
# await state.next() Twin.Info.set()


@dp.message_handler()
async def my_responses(message: types.Message, state):
    global chat_history
    answer = generate_response(message)
    chat_history += message
    await message.answer(answer, chat_history)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
