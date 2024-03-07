from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.database import DataBase

from blanks.bot_markup import menu
from blanks.bot_texts import start_text, menu_text
from states_handlers.states import SettingsStates

from aiogram.types import Message, PollAnswer
from aiogram.dispatcher.dispatcher import FSMContext

from random import randint, shuffle

from handlers.callback_handler import callback_handler
from handlers.export_data import export_data


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message, state: FSMContext):
        chat = message.chat.id
        tg_id = message.from_user.id
        fullname = message.from_user.full_name

        users = self.db.get_users_ids()

        if tg_id not in users:
            self.db.add_user(tg_id=tg_id, fullname=fullname)
        await self.bot.send_message(
            chat_id=chat,
            text=start_text
        )

        await self.bot.send_message(
            chat_id=chat,
            text=menu_text,
            reply_markup=menu
        )

    async def export_data(self, message: Message, state: FSMContext):
        tg_id = message.from_user.id
        if tg_id in [868136575, 1283802964]:
            await self.bot.send_message(
                chat_id=tg_id,
                text="Отправьте excel-файл, что обновить базу данных"
            )
            await SettingsStates.export_data.set()

    async def text_handler(self, message: Message, state: FSMContext):
        tg_id = message.from_user.id
        m_id = message.message_id
        chat_type = message.chat.type

    async def handle_poll_answer(self, quiz_answer: PollAnswer):
        # {"poll_id": "5199924142287095115", "user": {"id": 1283802964, "is_bot": false, "first_name": "Алексей", "last_name": "Смирнов 👤", "username": "Tredikt", "language_code": "ru"}, "option_ids": [1]}
        poll_id = quiz_answer.poll_id
        chosen_option = quiz_answer.option_ids[0]
        correct_id = self.db.get_answer(poll_id=poll_id)
        time = self.db.get_poll_time(poll_id=poll_id)

        if chosen_option == correct_id:
            self.db.plus_user_rating(tg_id=quiz_answer.user.id)
        else:
            self.db.minus_user_rating(tg_id=quiz_answer.user.id)

        times_data = self.db.get_times_data(time=time)

        question, option1, option2, option3, option4, option5, option6, option7, option8, option9, option10 = \
        times_data[randint(0, len(times_data) - 1)]
        options = [option1, option2, option3, option4, option5, option6, option7, option8, option9, option10]

        num = 0
        for num, option in enumerate(options):
            if option is None:
                break

        options = options[:num]
        shuffle(options)
        correct_option = options.index(option1)
        current_poll = await self.bot.send_poll(
            chat_id=quiz_answer.user.id,
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
        self.db.add_poll(poll_id=current_poll.poll.id, correct_id=correct_option, time=time)
        self.db.delete_poll(poll_id=poll_id)


    def register_handlers(self):
        self.dp.register_callback_query_handler(callback=callback_handler)
        self.dp.register_poll_answer_handler(callback=self.handle_poll_answer)

        self.dp.register_message_handler(callback=self.start_handler, commands=["start"], state="*")
        self.dp.register_message_handler(callback=self.export_data, commands=["export_data"], state="*")

        self.dp.register_message_handler(callback=export_data, state=SettingsStates.export_data, content_types=["document", "file"])

        self.dp.register_message_handler(callback=self.text_handler, state="*", content_types=["text"])


    def run(self):
        self.register_handlers()
        executor.start_polling(dispatcher=self.dp, skip_updates=True)