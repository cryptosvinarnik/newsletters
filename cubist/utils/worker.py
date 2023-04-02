import asyncio
from abc import ABC, abstractmethod
from typing import Iterable


class WorkFactory(ABC):
    def __init__(self, queue: asyncio.Queue, workers: int = 5):
        self.workers = workers
        self.queue = queue

    @abstractmethod
    async def worker(self, worker_name: str) -> None:
        """
        :param worker_name: Name of the worker
        :return: None
        """
        ...

    async def start_workers(self, items: Iterable) -> asyncio.Future[list]:
        """
        :param items: Iterable of items to be processed
        :return: Future list of results
        """
        for item in items:
            await self.queue.put(item)

        coros = [self.worker(f"W-{i+1}") for i in range(self.workers)]

        return await asyncio.gather(*coros)