import asyncio

from config import HEADERS
from httpx import AsyncClient, Response
from loguru import logger
from urllib3 import encode_multipart_formdata


class Eluune():
    def __init__(self):
        self._client = AsyncClient(
            headers=HEADERS,
            follow_redirects=True
        )

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._client.aclose())
            else:
                loop.run_until_complete(self._client.aclose())
        except Exception:
            pass

    async def request(self, method: str, url: str, data) -> Response:
        response = await self._client.request(method=method, url=url, data=data)

        logger.info(
            f"{method} {response.url} Response: '{response.status_code} "
            f"{response.reason_phrase}' {response.text}"
        )

        return response

    async def signup_early_access(self, email):
        body, content_type = encode_multipart_formdata({
            "email": email,
        })

        self._client.headers["Content-Type"] = content_type

        return await self.request(
            "POST",
            "https://www.projecteluune.com/",
            data=body
        )


async def subscribe_luune(queue: asyncio.Queue):
    while not queue.empty():
        await Eluune().signup_early_access(await queue.get())
