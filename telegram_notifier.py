import asyncio
import datetime
import aiohttp
import logging

from config import settings
from db import DBService
from server_status_service import ServiceStatusService


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


group_chat_id = settings.GROUP_CHAT_ID
check_time = datetime.time(21, 0)
api_token = settings.API_TOKEN


async def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    payload = {
        'chat_id': group_chat_id,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            if response.status == 200:
                logger.info("Message sent successfully")
            else:
                logger.error(f"Failed to send message. Status code: {response.status}")


async def daily_check():
    now = datetime.datetime.now().time()
    if now.hour == check_time.hour and now.minute == check_time.minute:
        last_event_date = DBService().get_last_event_date()
        if not last_event_date:
            await send_telegram_message("There have been no falls yet.")
        else:
            last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d %H:%M:%S.%f")
            days_since_last_event = (datetime.datetime.now() - last_event_date).days
            await send_telegram_message(f"{days_since_last_event} days without fall.")


async def start_loop():
    while True:
        is_enabled = await ServiceStatusService().check_server_online()
        if not is_enabled:
            DBService().insert_failure_event()
            await send_telegram_message("Server is not responding.")
        await daily_check()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(start_loop())
