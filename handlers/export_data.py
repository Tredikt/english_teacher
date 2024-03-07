from pandas import read_excel
from math import isnan
from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import FSMContext

from states_handlers.states import SettingsStates


async def export_data(message: Message, state: FSMContext):
    bot, db = get_bot_and_db()
    chat = message.chat.id
    filename = "files/data.xlsx"
    file = message.document
    await file.download(filename)
    db_words = db.get_words()
    questions = db.get_questions()

    db.delete_words()
    db.delete_times()
    db.create_words()
    db.create_times()

    with open(filename, "rb") as excel:
        words = read_excel(excel, sheet_name="Слова")

        level_list = words["level"]
        word_list = words["word"]
        picture_list = words["picture"]
        translation_list = words["translate"]
        word_type_list = words["type"]
        transcription_list = words["transcription"]
        example_list = words["example"]

        for level, word, picture, translation, word_type, transcription, example in zip(level_list, word_list,
                                                                                        picture_list, translation_list,
                                                                                        word_type_list,
                                                                                        transcription_list,
                                                                                        example_list):
            if word not in db_words and word != "TEXT":
                db.add_word(
                    level=level,
                    word=word,
                    picture=picture,
                    translation=translation,
                    word_type=word_type,
                    transcription=transcription,
                    example=example
                )

        words = read_excel("Бот по англу.xlsx", sheet_name="Времена")

        theme_list = words["theme"]
        text_list = words["text"]
        option1_list = words["option1"]
        option2_list = words["option2"]
        option3_list = words["option3"]
        option4_list = words["option4"]
        option5_list = words["option5"]
        option6_list = words["option6"]
        option7_list = words["option7"]
        option8_list = words["option8"]
        option9_list = words["option9"]
        option10_list = words["option10"]

        for theme, text, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10 in zip(
                theme_list, text_list, option1_list, option2_list, option3_list, option4_list, option5_list,
                option6_list, option7_list, option8_list, option9_list, option10_list):

            if option7 != "TEXT":
                try:
                    option2 = None if isnan(option2) else option2
                    option2 = None
                except TypeError:
                    pass
                try:
                    option3 = None if isnan(option2) else option2
                    option3 = None
                except TypeError:
                    pass
                try:
                    option4 = None if isnan(option2) else option2
                    option4 = None
                except TypeError:
                    pass
                try:
                    option5 = None if isnan(option2) else option2
                    option5 = None
                except TypeError:
                    pass
                try:
                    option6 = None if isnan(option2) else option2
                    option6 = None
                except TypeError:
                    pass
                try:
                    option7 = None if isnan(option2) else option2
                    option7 = None
                except TypeError:
                    pass
                try:
                    option8 = None if isnan(option2) else option2
                    option8 = None
                except TypeError:
                    pass
                try:
                    option9 = None if isnan(option2) else option2
                    option9 = None
                except TypeError:
                    pass
                try:
                    option10 = None if isnan(option2) else option2
                    option10 = None
                except TypeError:
                    pass

            if text not in questions and theme != "TEXT":
                db.add_time(
                    theme=theme,
                    question=text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    option5=option5,
                    option6=option6,
                    option7=option7,
                    option8=option8,
                    option9=option9,
                    option10=option10
                )

    await bot.send_message(
        chat_id=chat,
        text="БД успешно обновлена"
    )
    await SettingsStates.settings.set()

