from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.task import TaskResult
from app.domain.repositories.task_repository import TaskRepository
from app.domain.schemas.task import UploadResponseSchema


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TaskResult) -> UploadResponseSchema:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def task_exists(self, task_id: str) -> bool:
        if await self.db.get(TaskResult, task_id):
            return True
        else:
            return False
