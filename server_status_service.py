import aiohttp

from config import settings


class ServiceStatusService:
    server_url = settings.SERVER_URL

    async def check_server_online(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.server_url) as response:
                    return response.status == 200
        except aiohttp.ClientError:
            return False
