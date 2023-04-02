import asyncio

from cubist_submitter import CubistFiller
from loguru import logger


async def main():
    accounts = list(filter(bool, open(input("Accounts >> ")).read().splitlines()))

    formatted_accounts = []
    for account in accounts:
        if len(account.split("|")) == 1:
            logger.info(f"Account {account} has no proxy")
            formatted_accounts.append((account, None))
        elif len(account.split("|")) == 2:
            logger.info(f"Account {account} has proxy")
            formatted_accounts.append(account.split("|"))
        else:
            logger.warning(f"Invalid account: {account}")

    cubist = CubistFiller(queue=asyncio.Queue())
    await cubist.start_workers(formatted_accounts)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass