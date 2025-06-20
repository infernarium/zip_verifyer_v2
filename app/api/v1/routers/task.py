import uuid
from fastapi import UploadFile
from fastapi.routing import APIRouter
from app.api.dependencies import (
    AnalyticsServiceDependency,
    TaskRepositoryDependency,
    StorageServiceDependency,
)
from app.domain.models.task import TaskStatusEnum
from app.domain.schemas.task import ReportResponseSchema, UploadResponseSchema
from app.use_cases.upload_zip import UploadArchiveUseCase


task_router = APIRouter(tags=["report"])


@task_router.get("/report/{id}", response_model=ReportResponseSchema)
async def get_report(id: uuid.UUID) -> ReportResponseSchema:
    return ReportResponseSchema(status=TaskStatusEnum.IN_PROGRESS)


@task_router.post("/upload", response_model=UploadResponseSchema)
async def upload(
    file: UploadFile,
    analytics_service: AnalyticsServiceDependency,
    storage_service: StorageServiceDependency,
    task_repo: TaskRepositoryDependency,
) -> UploadResponseSchema:
    file_data = await file.read()
    return await UploadArchiveUseCase(
        task_repo, storage_service, analytics_service
    ).execute(file_data=file_data, filename=file.filename)
