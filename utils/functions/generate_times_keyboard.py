from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.functions.get_bot_and_db import get_bot_and_db


async def generate_times_keyboard(page_number=1) -> InlineKeyboardMarkup:
    bot, db = get_bot_and_db()
    times_list = db.get_times_list()
    keyboard = InlineKeyboardMarkup()

    slice_min = page_number * 10 - 10
    slice_max = page_number * 10

    for num, time in enumerate(times_list[slice_min:slice_max]):
        num += 1
        if num == slice_max:
            if page_number == 1:
                button = InlineKeyboardButton(text="-->", callback_data=f"time_page_{page_number + 1}")
            else:
                button = (InlineKeyboardButton(text="<--", callback_data=f"time_page_{page_number - 1}"),
                          InlineKeyboardButton(text="-->", callback_data=f"time_page_{page_number + 1}"))
        else:
            button = InlineKeyboardButton(text=time, callback_data=time)
        keyboard.add(button)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="menu"))

    return keyboard