import uuid
from fastapi import UploadFile
from fastapi.routing import APIRouter
from app.domain.models.task import TaskStatusEnum
from app.domain.schemas.task import ReportResponseSchema, UploadResponseSchema


task_router = APIRouter(tags=["report"])


@task_router.get("/report/{id}", response_model=ReportResponseSchema)
def get_report(id: uuid.UUID) -> ReportResponseSchema:
    return ReportResponseSchema(status=TaskStatusEnum.IN_PROGRESS)


@task_router.post("/upload", response_model=UploadResponseSchema)
def upload(file: UploadFile) -> UploadResponseSchema:
    return UploadResponseSchema(task_id=uuid.uuid1())
