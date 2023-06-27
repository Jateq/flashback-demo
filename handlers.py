from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

from states import Gen

import utils
import keyboards
import text
import db

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await db.add_user(msg.from_user.id)
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name), reply_markup=keyboards.menu
    )


@router.callback_query(F.data == "help")
async def help_handler(clbck: CallbackQuery):
    await clbck.message.answer(text.help_list)


@router.message(Command("help"))
async def help_handler2(msg: Message):
    await msg.answer(text.help_list)


@router.message(Command("menu"))
async def menu_handler(msg: Message):
    await msg.answer(text.menu, reply_markup=keyboards.menu)


@router.message(Command("my_balance"))
async def my_balance_handler(msg: Message):
    cur_balance = await db.get_balance(msg.from_user.id)
    await msg.answer("Your current balance is: {} tokens".format(cur_balance))


@router.message(F.text == "◀️ Back to menu")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=keyboards.menu)


@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.answer(text.gen_text, reply_markup=keyboards.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    check = await db.check_balance(msg.from_user.id)
    if not check:
        return await msg.answer(text.balance_error, reply_markup=keyboards.iexit_kb)
    context = await db.get_request_response(msg.from_user.id)
    prompt = text.prompt_chat.format(
        prev_request=context[0], prev_response=context[1], message=msg.text
    )
    res = await utils.generate_text(prompt)
    if not res:
        return await msg.answer(text.gen_error, reply_markup=keyboards.iexit_kb)
    await db.update_request_response(msg.from_user.id, msg.text, res[0])
    await msg.answer(
        res[0], disable_web_page_preview=True, reply_markup=keyboards.exit_kb
    )
    await db.update_balance(msg.from_user.id, res[1])


@router.callback_query(F.data == "table_menu")
async def input_image_prompt(clbck: CallbackQuery):
    await clbck.message.answer("Sorry, i can't do this yet")
