from typing import Annotated, AsyncGenerator

from fastapi import Depends

from minio import Minio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.domain.repositories.task_repository import TaskRepository
from app.domain.services.storage_service import StorageService
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.infrastructure.services.minio_storage_service import MinioStorageService
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import db_settings, miniosettings

# TODO: Добавить реальные настройки БД
async_engine = create_async_engine(db_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


def get_minio_client() -> Minio:
    return Minio(**miniosettings)


def get_storage_service(
    minio: Annotated[Minio, Depends(get_minio_client)],
) -> StorageService:
    return MinioStorageService(minio)


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepositoryImpl(session)


StorageServiceDependency = Annotated[StorageService, Depends(get_storage_service)]
TaskRepositoryDependency = Annotated[TaskRepository, Depends(get_task_repository)]
