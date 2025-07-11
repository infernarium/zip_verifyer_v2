from abc import ABC, abstractmethod
from app.domain.models.task import TaskResult
from app.domain.schemas.task import TaskUpdateSchema, TestResults, UploadResponseSchema


class TaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task: TaskResult) -> UploadResponseSchema:
        raise NotImplementedError()

    @abstractmethod
    async def task_exists(self, task_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, task_id: str, update_data: TaskUpdateSchema) -> bool:
        raise NotImplementedError()
