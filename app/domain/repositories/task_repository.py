from abc import ABC, abstractmethod
import uuid
from app.domain.schemas.task import TestResults


class TaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task: TestResults) -> str:
        pass

    @abstractmethod
    async def task_exists(self, task_id: str) -> bool:
        pass
