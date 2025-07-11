# app/infrastructure/repositories/task_repository_impl.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.task import TaskResult
from app.domain.repositories.task_repository import TaskRepository
from app.domain.schemas.task import TaskUpdateSchema, UploadResponseSchema


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TaskResult) -> UploadResponseSchema:
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return UploadResponseSchema(task_id=task.task_id)

    async def task_exists(self, zip_hash: str) -> bool:
        result = await self.db.execute(
            select(TaskResult).where(TaskResult.task_hash == zip_hash)
        )
        return result.scalars().first() is not None

    async def update_task(
        self, task_id: str, update_data: TaskUpdateSchema
    ) -> UploadResponseSchema:  # Возможно возвращает не этот тип
        task = await self.db.get(TaskResult, task_id)
        if not task:
            raise ValueError(f"Задача с id {task_id} не найдена")

        for field, value in update_data.model_dump().items():
            if value is not None:
                setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task
