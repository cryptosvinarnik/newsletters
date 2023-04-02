import httpx
from loguru import logger

from config import HEADERS


class HTTPXClient:
    def __init__(self, proxy: str = None):
        self._client = httpx.AsyncClient(
            headers=HEADERS,
            proxies={"all://": proxy} if proxy else None,
        )

    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        response = await self._client.request(method=method, url=url, follow_redirects=True, **kwargs)

        logger.info(
            f"{method} {response.url} Response: '{response.status_code}'"
        )

        return response

