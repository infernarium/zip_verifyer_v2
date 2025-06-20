from abc import ABC, abstractmethod


class AnalyticsService(ABC):
    @abstractmethod
    async def get_stats(self, file_data: bytes) -> bool: ...
