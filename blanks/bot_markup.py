from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="🏆Рейтинг🏆",
        callback_data="rating"
    )
).add(
    InlineKeyboardButton(
        text="Слова",
        callback_data="words"
    )
).add(
    InlineKeyboardButton(
        text="Времена",
        callback_data="times"
    )
)

to_menu = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="В меню",
        callback_data="menu"
    )
)

word_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="А1",
        callback_data="A1"
    )
).add(
    InlineKeyboardButton(
        text="A2",
        callback_data="A2"
    )
).add(
    InlineKeyboardButton(
        text="B1",
        callback_data="B1"
    )
).add(
    InlineKeyboardButton(
        text="B2",
        callback_data="B2"
    )
).add(
    InlineKeyboardButton(
        text="C1",
        callback_data="C1"
    )
).add(
    InlineKeyboardButton(
        text="В меню",
        callback_data="menu"
    )
)