from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories.task_repository import TaskRepository
from app.domain.schemas.task import TestResults


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TestResults) -> str: ...

    async def task_exists(self, task_id: str) -> bool: ...
