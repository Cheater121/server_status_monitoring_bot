import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message

from config import settings
from db import DBService
from server_status_service import ServiceStatusService
from statuses import States

allowed_users = settings.ALLOWED_USERS
group_chat_id = settings.GROUP_CHAT_ID
check_time = datetime.time(22, 0)


bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)


async def daily_check():
    now = datetime.datetime.now().time()
    if now.hour == check_time.hour and now.minute == check_time.minute:
        last_event_date = DBService().get_last_event_date()
        if not last_event_date:
            await bot.send_message(group_chat_id, "There have been no falls yet.")
        else:
            last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d %H:%M:%S.%f")
            days_since_last_event = (datetime.datetime.now() - last_event_date).days
            await bot.send_message(group_chat_id, f"{days_since_last_event} days without fall.")


@dp.message(Command(commands=["start"]), StateFilter(None))
async def start_handler(message: Message, state: FSMContext):
    if message.from_user.id not in allowed_users:
        await message.answer("You are not allowed to start the bot.")
        return
    await message.answer("Bot started.")
    await state.set_state(States.started)
    await state.set_data(data={"state": "started"})
    while True:
        data = await state.get_data()
        if not data.get("state"):
            break
        is_enabled = await ServiceStatusService().check_server_online()
        if not is_enabled:
            DBService().insert_failure_event()
            await bot.send_message(group_chat_id, "Server is not responding.")
        await daily_check()
        await asyncio.sleep(60)


@dp.message(Command(commands=["stop"]), States.started)
async def start_handler(message: Message, state: FSMContext):
    if message.from_user.id not in allowed_users:
        await message.answer("You are not allowed to stop the bot.")
        return
    await message.answer("Bot stopped.")
    await state.clear()


async def on_startup(dp: Dispatcher):
    # ToDo maybe while true -> try/except for infinitive?
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(on_startup(dp))
