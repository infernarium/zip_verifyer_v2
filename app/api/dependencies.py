from typing import Annotated

from fastapi import Depends

from minio import Minio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.domain.repositories.task_repository import TaskRepository
from app.domain.services.analytics_service import AnalyticsService
from app.domain.services.storage_service import StorageService
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.infrastructure.services.minio_storage_service import MinioStorageService
from app.config import project_settings
from app.infrastructure.services.sonarqube_stats_service import (
    SonarqubeAnalyticsService,
)


async_engine = create_async_engine(project_settings.postgres_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
        session.close()


def get_minio_client() -> Minio:
    settings = project_settings.minio_settings
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=False,
    )


def get_storage_service(
    minio: Annotated[Minio, Depends(get_minio_client)],
) -> StorageService:
    return MinioStorageService(minio, settings=project_settings.minio_settings)


def get_task_repository(session: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepositoryImpl(session)


def get_analytics_service() -> AnalyticsService:
    return SonarqubeAnalyticsService()


StorageServiceDependency = Annotated[StorageService, Depends(get_storage_service)]
TaskRepositoryDependency = Annotated[TaskRepository, Depends(get_task_repository)]
AnalyticsServiceDependency = Annotated[AnalyticsService, Depends(get_analytics_service)]
