import random

from client import HTTPXClient
from loguru import logger
from utils.worker import WorkFactory


def get_random_bool() -> bool:
    return bool(random.getrandbits(1))


class SoulWallet(HTTPXClient):
    def __init__(self, proxy: str = None):
        super().__init__(proxy)

    async def submit_form(self, email: str) -> dict:
        response = await self.request(
            "POST",
            "https://securecenter-poc.soulwallets.me/add-to-list",
            json={"email": email}
        )

        return response.json()


class SoulWalletFiller(WorkFactory):
    async def worker(self, worker_name: str):
        while not self.queue.empty():
            email, proxy = await self.queue.get()

            tag = f"[{worker_name}] | [{email}] -"

            cubist = SoulWallet(proxy)

            try:
                response = await cubist.submit_form(email)

                if response.get("msg") == "Add to list successfully.":
                    logger.success(f"{tag} Successfully subscribed")
                else:
                    logger.error(f"{tag} Failed to subscribe: {response.get('msg')}")
            except Exception as e:
                logger.error(f"{tag} Failed to subscribe due to {e}")
            finally:
                await cubist._client.aclose()