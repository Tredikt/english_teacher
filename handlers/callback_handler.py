import os
import cv2
import numpy as np

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.dispatcher import FSMContext
from random import randint, shuffle
from blanks.bot_markup import menu, to_menu, word_keyboard
from blanks.bot_texts import lvl_text, times_text, menu_text


import aspose.slides as slides
import aspose.pydrawing as drawing

from utils.functions.get_bot_and_db import get_bot_and_db
from utils.functions.generate_times_keyboard import generate_times_keyboard
from utils.functions.create_card import create_flash_card


async def callback_handler(call: CallbackQuery, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = call.message.chat.id
    tg_id = call.from_user.id
    fullname = call.from_user.full_name
    callback = call.data
    m_id = call.message.message_id
    levels = ["A1", "A2", "B1", "B2", "C1"]
    print(callback, callback in levels)
    times = db.get_times_list()

    if callback == "menu":
        await bot.edit_message_text(
            chat_id=chat,
            message_id=m_id,
            text=menu_text,
            reply_markup=menu
        )

    elif callback == "rating":
        users_rating = db.get_users_rating()
        if len(users_rating) != 0:
            users_rating = sorted(users_rating, key=lambda x: x[2])
        for_text = users_rating[:10]
        for_text = reversed(for_text)
        num = 1
        my_rating = 0

        for num, rate_tuple in enumerate(users_rating):
            user_id, fullname, my_rating = rate_tuple

            if user_id == tg_id:
                num += 1
                break

        text = "Топ рейтинга:\n"
        for number, rate_tuple in enumerate(for_text):
            user_name = rate_tuple[1]
            rating = rate_tuple[2]
            text += f"{number + 1}. {user_name} - {rating}\n"
        text += f"...\n\n{num}. {fullname} - {my_rating} (Вы)"

        await bot.edit_message_text(
            chat_id=chat,
            message_id=m_id,
            text=text,
            reply_markup=to_menu
        )

    elif callback == "words":
        await bot.delete_message(
            chat_id=chat,
            message_id=m_id
        )

        await bot.send_message(
            chat_id=chat,
            text=lvl_text,
            reply_markup=word_keyboard
        )

    elif callback == "times":
        keyboard = await generate_times_keyboard()
        await bot.delete_message(
            chat_id=chat,
            message_id=m_id
        )

        await bot.send_message(
            chat_id=chat,
            text=times_text,
            reply_markup=keyboard
        )

    elif callback in levels:
        level_words = db.get_words_by_lvl(level=callback, tg_id=tg_id)
        slice = randint(a=0, b=len(level_words) - 1)
        this_word = level_words[slice]

        async with state.proxy() as data:
            data["level"] = callback

        word, picture, translation, type, transcription, example = this_word
        path = create_flash_card(
            word=word,
            picture_link=picture,
            transcription=transcription,
            type_=type,
            level=callback
        )
        png_name = path.replace(".pptx", ".png")
        pres = slides.Presentation(path)

        for index in range(pres.slides.length):
            slide = pres.slides[index]
            size = drawing.Size(1900, 1900)
            slide.get_thumbnail(size).save(png_name.format(i=index), drawing.imaging.ImageFormat.png)

        with open(png_name, "rb") as photo:
            await bot.delete_message(
                chat_id=chat,
                message_id=m_id
            )
            text = f"Перевод: ||{translation}||\n\nПример: ||{example}||"
            text = text.replace("!", "\!").replace(".", "\.").replace("-", "\-")
            await bot.send_photo(
                chat_id=chat,
                photo=photo.read(),
                caption=text,
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Знал",
                        callback_data=f"know_{word}"
                    ),
                    InlineKeyboardButton(
                        text="Не знал",
                        callback_data=f"dontknow_{word}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data="words"
                    )
                )
            )

        os.remove(path)
        os.remove(png_name)

    elif callback[:4] == "know":
        call_word = callback.split("_")[1]
        rate_words = db.get_rating_words(tg_id=tg_id)

        if call_word in rate_words:
            db.plus_word_rating(tg_id=tg_id, word=call_word)
        else:
            db.add_word_rating(tg_id=tg_id, word=call_word)

        async with state.proxy() as data:
            level = data["level"]

        level_words = db.get_words_by_lvl(level=callback, tg_id=tg_id)
        slice = randint(a=0, b=len(level_words) - 1)
        this_word = level_words[slice]

        word, picture, translation, type, transcription, example = this_word
        path = create_flash_card(
            word=word,
            picture_link=picture,
            transcription=transcription,
            type_=type,
            level=level
        )
        png_name = path.replace(".pptx", ".png")
        pres = slides.Presentation(path)

        for index in range(pres.slides.length):
            slide = pres.slides[index]
            size = drawing.Size(1900, 1900)
            slide.get_thumbnail(size).save(png_name.format(i=index), drawing.imaging.ImageFormat.png)

        with open(png_name, "rb") as photo:
            await bot.delete_message(
                chat_id=chat,
                message_id=m_id
            )
            text = f"Перевод: ||{translation}||\n\nПример: ||{example}||"
            text = text.replace("!", "\!").replace(".", "\.").replace("-", "\-")
            await bot.send_photo(
                chat_id=chat,
                photo=photo.read(),
                caption=text,
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Знал",
                        callback_data=f"know_{word}"
                    ),
                    InlineKeyboardButton(
                        text="Не знал",
                        callback_data=f"dontknow_{word}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data="words"
                    )
                )
            )

        os.remove(path)
        os.remove(png_name)

    elif callback[:8] == "dontknow":
        call_word = callback.split("_")[1]
        rate_words = db.get_rating_words(tg_id=tg_id)

        if call_word in rate_words:
            db.minus_word_rating(tg_id=tg_id, word=call_word)
        else:
            db.add_word_rating(tg_id=tg_id, word=call_word)

        async with state.proxy() as data:
            level = data["level"]

        level_words = db.get_words_by_lvl(level=callback, tg_id=tg_id)
        slice = randint(a=0, b=len(level_words) - 1)
        this_word = level_words[slice]

        word, picture, translation, type, transcription, example = this_word
        path = create_flash_card(
            word=word,
            picture_link=picture,
            transcription=transcription,
            type_=type,
            level=level
        )

        png_name = path.replace(".pptx", ".png")
        pres = slides.Presentation(path)

        for index in range(pres.slides.length):
            slide = pres.slides[index]
            size = drawing.Size(1900, 1900)
            slide.get_thumbnail(size).save(png_name.format(i=index), drawing.imaging.ImageFormat.png)

        with open(png_name, "rb") as photo:
            await bot.delete_message(
                chat_id=chat,
                message_id=m_id
            )
            text = f"Перевод: ||{translation}||\n\nПример: ||{example}||"
            text = text.replace("!", "\!").replace(".", "\.").replace("-", "\-")
            await bot.send_photo(
                chat_id=chat,
                photo=photo.read(),
                caption=text,
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Знал",
                        callback_data=f"know_{word}"
                    ),
                    InlineKeyboardButton(
                        text="Не знал",
                        callback_data=f"dontknow_{word}"
                    )
                ).add(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data="words"
                    )
                )
            )

        os.remove(path)
        os.remove(png_name)

    elif callback[:9] == "time_page":
        page_number = int(callback.split("_")[2])

        keyboard = await generate_times_keyboard(page_number=page_number)
        await bot.delete_message(
            chat_id=chat,
            message_id=m_id
        )

        await bot.send_message(
            chat_id=chat,
            text=times_text,
            reply_markup=keyboard
        )


    elif callback in times:
        time = callback.replace("_", " ", 1)
        times_data = db.get_times_data(time=time)

        question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10 = times_data[randint(0, len(times_data) - 1)]
        options = [option1, option2, option3, option4, option5, option6, option7, option8, option9, option10]

        num = 0
        for num, option in enumerate(options):
            if option is None:
                break

        options = options[:num]
        shuffle(options)
        correct_option = options.index(option1)
        current_poll = await bot.send_poll(
            chat_id=chat,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option,
            is_anonymous=False,
            reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data="times"
                    )
                )
        )
        db.add_poll(poll_id=current_poll.poll.id, correct_id=correct_option, time=time)