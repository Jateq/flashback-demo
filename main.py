import logging
import os
import motor.motor_asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


# import dbshki

import menus
from openai_setup import generate_response

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# print(MONGO_USER, MONGO_PASSWORD)

# connection_string = (
#     "mongodb+srv://"
#     + MONGO_USER
#     + ":"
#     + MONGO_PASSWORD
#     + "@flashbackmvp.fugosts.mongodb.net/?retryWrites=true&w=majority"
# )

# cluster = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
# db = cluster["Tg-mvp"]
# collection = db["Users"]


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
    # user_id = message.chat.id
    # await db.add_user(collection, user_id)


@dp.callback_query_handler(lambda query: query.data == "open_collection")
async def handle_open_collection(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_chat_action(callback_query.from_user.id, types.ChatActions.TYPING)
    await bot.send_message(callback_query.from_user.id, "It is not available yet")


@dp.callback_query_handler(lambda query: query.data == "help")
async def help_section(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_chat_action(callback_query.from_user.id, types.ChatActions.TYPING)
    help_message = (
        "Here is the help section:\n\n"
        "1. To create a twin, click on the 'Create Twin' button.\n"
        "2. Give the desired age that you want to recreate.\n"
        "3. Chat with Assistant to give more information.\n"
        "4. Chat with your digital twin\n"
    )

    await bot.send_message(callback_query.from_user.id, help_message)


@dp.callback_query_handler(lambda query: query.data == "create_twin")
async def create_twin(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await bot.send_chat_action(callback_query.from_user.id, types.ChatActions.TYPING)
    
    # Set the initial state to Twin.Age
    await Twin.Age.set()

    # Send a message to ask for the age of the twin
    await bot.send_message(
        callback_query.from_user.id, "Please enter the age of the twin:"
    )


@dp.message_handler(state=Twin.Age)
async def process_age(message: types.Message, state: FSMContext):
    global chat_history
    age = message.text
    # Store the age in the state
    await message.answer_chat_action("typing")
    await state.update_data(age=age)
    await Twin.Info.set()
    await message.reply(
        "Age saved. Please provide additional information about the twin, " 
        "in this way:\n\nWhat was your main goal when you were at your age" 
        "What was your hobby, education and what plans you had for a " 
        "week or month ahead, if you can remember."
    )


@dp.message_handler(state=Twin.Info)
async def process_info(message: types.Message, state: FSMContext):
    info = message.text
    await message.answer_chat_action("typing")
    # Store the info in the state
    await state.update_data(info=info)

    await Twin.Chat.set()
    await message.reply("Information saved. Please provide a chat for the twin:")


# @dp.message_handler(state=Twin.Age)
# await state.next() Twin.Info.set()


@dp.message_handler()
async def my_responses(message: types.Message, state):
    await message.answer_chat_action("typing")
    answer = generate_response(message)
    await message.answer(answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
