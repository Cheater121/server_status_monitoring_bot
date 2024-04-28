from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    waiting_for_start = State()
    started = State()
