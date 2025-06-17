import uuid
from fastapi import UploadFile
from fastapi.routing import APIRouter
from app.api.dependencies import TaskRepositoryDependency
from app.domain.models.task import TaskStatusEnum
from app.domain.schemas.task import ReportResponseSchema, UploadResponseSchema
from app.use_cases.upload_zip import UploadArchiveUseCase


task_router = APIRouter(tags=["report"])


@task_router.get("/report/{id}", response_model=ReportResponseSchema)
def get_report(id: uuid.UUID) -> ReportResponseSchema:
    return ReportResponseSchema(status=TaskStatusEnum.IN_PROGRESS)


@task_router.post("/upload", response_model=UploadResponseSchema)
def upload(
    file: UploadFile,
    storage_service: TaskRepositoryDependency,
    task_repo: TaskRepositoryDependency,
) -> UploadResponseSchema:
    return UploadArchiveUseCase(task_repo, storage_service).execute(
        file_data=file.file.read(), filename=file.filename
    )
