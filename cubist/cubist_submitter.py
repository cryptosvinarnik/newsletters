import random
from urllib.parse import urlencode

from client import HTTPXClient, solve_by_capmonster
from config import CUBIST_SITE_KEY, CUBIST_URL
from loguru import logger
from utils.worker import WorkFactory


def get_random_bool() -> bool:
    return bool(random.getrandbits(1))


class Cubist(HTTPXClient):
    def __init__(self, proxy: str = None):
        super().__init__(proxy)

    async def submit_form(self, email: str, gresp: str) -> dict:
        response = await self.request(
            "POST",
            "https://webflow.com/api/v1/form/638a2693daaf8527290065a3",
            data=urlencode({
                "name": "beta_access_form",
                "source": "https://cubist.dev/early-access",
                "test": "false",
                "fields[email-telegram]": email,
                "fields[INTERESTS--cross_chain_dev]": get_random_bool(),
                "fields[INTERESTS--bridge_independence]": get_random_bool(),
                "fields[INTERESTS--bridge_safety_monitoring]": get_random_bool(),
                "fields[INTERESTS--private_testnets]": get_random_bool(),
                "fields[INTERESTS--simulation_testing]": get_random_bool(),
                "fields[INTERESTS--ci_integration]": get_random_bool(),
                "fields[INTERESTS--credential_management_smart_contracts]": get_random_bool(),
                "fields[INTERESTS--credential_management_teams]": get_random_bool(),
                "fields[INTERESTS--application-specific_rollups]": get_random_bool(),
                "fields[other-interest]": "",
                "fields[g-recaptcha-response]": gresp,
                "dolphin": "false",
            })
        )

        return response.json()


class CubistFiller(WorkFactory):
    async def worker(self, worker_name: str):
        while not self.queue.empty():
            email, proxy = await self.queue.get()

            tag = f"[{worker_name}] | [{email}] -"

            cubist = Cubist(proxy)

            logger.info(f"{tag} Solving captcha...")

            try:
                gresp = await solve_by_capmonster(CUBIST_URL, CUBIST_SITE_KEY)

                logger.info(f"{tag} Captcha solved")

                response = await cubist.submit_form(email, gresp)

                if response.get("msg") == "ok":
                    logger.success(f"{tag} Successfully subscribed")
                else:
                    logger.error(f"{tag} Failed to subscribe: {response.get('msg')}")
            except Exception as e:
                logger.error(f"{tag} Failed to subscribe due to {e}")
            finally:
                await cubist._client.aclose()