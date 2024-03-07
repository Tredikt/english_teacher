from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    settings = State()
    export_data = State()
