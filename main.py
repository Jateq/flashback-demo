import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

from openai_setup import setup, generate_response

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
print(OPENAI_TOKEN)
setup(OPENAI_TOKEN)
print(TG_TOKEN)

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        """
    Welcome to Flashback!\nLet's try to create you digital twin)
    """
    )


@dp.message_handler()
async def my_responses(message: types.Message):
    answer = generate_response(message)
    await message.answer(answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
