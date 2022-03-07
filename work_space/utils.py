from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    waiting_new_lang = State()
    waiting_new_rep = State()
    waiting_new_lim = State()