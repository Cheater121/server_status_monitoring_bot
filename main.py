import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from db import DBService
from server_status_service import ServiceStatusService


allowed_users = settings.ALLOWED_USERS
group_chat_id = settings.GROUP_CHAT_ID
check_time = datetime.time(22, 0)


bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher()


async def daily_check():
    now = datetime.datetime.now().time()
    if now.hour == check_time.hour and now.minute == check_time.minute:
        last_event_date = DBService().get_last_event_date()
        if not last_event_date:
            await bot.send_message(settings.GROUP_CHAT_ID, "There have been no falls yet.")
        else:
            last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d %H:%M:%S.%f")
            days_since_last_event = (datetime.datetime.now() - last_event_date).days
            await bot.send_message(settings.GROUP_CHAT_ID, f"{days_since_last_event} days without fall.")


@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    if message.from_user.id not in settings.ALLOWED_USERS:
        await message.answer("You are not allowed to start the bot.")
        return
    await message.answer("Bot started.")
    while True:
        is_enabled = await ServiceStatusService().check_server_online()
        if not is_enabled:
            DBService().insert_failure_event()
            await bot.send_message(settings.GROUP_CHAT_ID, "Server is not responding.")
        await daily_check()
        await asyncio.sleep(60)


async def on_startup(dp: Dispatcher):
    # ToDo maybe while true -> try/except for infinitive?
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(on_startup(dp))
