from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = InlineKeyboardMarkup(row_width=2)
menu.add(
    InlineKeyboardButton(text="📝 Create Twin", callback_data="create_twin"),
    InlineKeyboardButton(text="🖼 Open Collection", callback_data="open_collection"),
)
menu.add(InlineKeyboardButton(text="🔎 Help", callback_data="help"))
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Back to menu")]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Выйти в меню", callback_data="menu")]]
) 
